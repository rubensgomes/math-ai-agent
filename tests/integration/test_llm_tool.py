# General Disclaimer
#
# **AI Generated Content**
#
# This project's source code and documentation were generated predominantly
# by an Artificial Intelligence Large Language Model (AI LLM). The project
# lead, [Rubens Gomes](https://rubensgomes.com), provided initial prompts,
# reviewed, and made refinements to the generated output. While human review and
# refinement have occurred, users should be aware that the output may contain
# inaccuracies, errors, or security vulnerabilities
#
# **Third-Party Content Notice**
#
# This software may include components or snippets derived from third-party
# sources. The software's users and distributors are responsible for ensuring
# compliance with any underlying licenses applicable to such components.
#
# **Copyright Status Statement**
#
# Copyright protection, if any, is limited to the original
# human contributions and modifications made to this project.
# The AI-generated portions of the code and
# documentation are not subject to copyright and are considered to be in the
# public domain.
#
# **Limitation of liability**
#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR
# OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#
# **No-Warranty Disclaimer**
#
# THIS SOFTWARE IS PROVIDED 'AS IS,' WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT.

"""Integration test for LLM tool calling via the OpenAIClient.

Connects to the calculator MCP server, discovers tools, then runs
an interactive agent loop that sends math prompts to the LLM and
dispatches tool calls back to the MCP server.  Run standalone with::

    poetry run python tests/integration/test_llm_tool.py
"""

import asyncio
import json
import logging
import os

from math_ai_agent.calc_mcp_client import CalcMCPClient
from math_ai_agent.config import configure_logging
from math_ai_agent.llm import OpenAIClient

configure_logging()
logger = logging.getLogger(__name__)

# GitHub Marketplace Model
_API_KEY = os.environ.get("RUBENS_PAT_TOKEN")
_BASE_URL = "https://models.github.ai/inference"
# _MODEL = "openai/gpt-5"
_MODEL = "openai/gpt-4.1"

# 1. Tool / Function Calling Prompt (Agent Pattern)
# This pattern allows the model to decide when to use external tools (APIs,
# calculators, databases).

_SYSTEM_INSTRUCTIONS = """
You are a careful math assistant tutor helping solve math problems. Always 
write a short plan first. Do NOT do arithmetic in your head. For every
math operation, request a tool call to the calculator. After tool results,
continue. Provide final answer with explanation.
"""


async def get_mcp_tools() -> list[dict]:
    """Connect to the Calculator MCP server, and list the tools."""
    logger.info("Connecting to Calculator MCP server")
    async with CalcMCPClient() as calcmcp_client:
        tools = await calcmcp_client.to_openai_tools()
        logger.info("Discovered %d MCP tool(s)", len(tools))
        return tools


async def call_tool(tool_name: str, args) -> str:
    """Call a Calculator MCP server tool.

    Args:
        tool_name: The name of the MCP tool to invoke.
        args: The arguments dict to pass to the tool.

    Returns:
        The string representation of the tool result.
    """
    logger.info("Connecting to Calculator MCP server")
    async with CalcMCPClient() as calcmcp_client:
        logger.info("Calling calculator MCP tool %s with %s", tool_name, args)
        result = await calcmcp_client.call_tool(tool_name, args)
        # TODO: how to propertly process result?
        return str(result.data)


async def prompt_llm() -> None:
    """Run the interactive agent loop with LLM tool calling.

    Discovers MCP tools, then enters a loop that reads user input,
    sends it to the LLM, and dispatches any tool calls to the
    calculator MCP server until the LLM produces a final text
    response.
    """
    logger.info("Starting LLM prompt test")
    memory = [{"role": "system", "content": _SYSTEM_INSTRUCTIONS}]
    tools = await get_mcp_tools()
    llm = OpenAIClient(_API_KEY, _BASE_URL, _MODEL, tools)

    # -------------------------
    # Agent Loop
    # -------------------------
    while True:

        user_input = input("User: ")

        memory.append({"role": "user", "content": user_input})
        logger.debug("Sending user prompt: %s", user_input)

        response = await llm.create_response(memory)
        logger.info("LLM response: %s", response)

        message = response.choices[0].message
        memory.append(message)

        # Keep looping while the model requests tool calls
        while message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_call_id = tool_call.id
                args = json.loads(tool_call.function.arguments)
                logger.info(
                    "Calling calculator tool: %s(%s)",
                    tool_name,
                    args,
                )
                result = await call_tool(tool_name, args)
                memory.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": result,
                    }
                )

            followup = await llm.create_response(memory)
            message = followup.choices[0].message
            memory.append(message)

        logger.info("Assistant: %s", message.content)
        print("Assistant:", message.content)


async def main() -> None:
    """Entry point for the LLM tool-calling integration test."""
    logger.info("Running integration test for OpenAIClient")
    await prompt_llm()
    logger.info("Integration test completed")


if __name__ == "__main__":
    asyncio.run(main())
