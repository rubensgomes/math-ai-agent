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

"""Integration test for the OpenAIClient LLM wrapper.

Connects to the calculator MCP server, discovers tools, then sends
a math prompt to the LLM via ``OpenAIClient``.  Run standalone with::

    poetry run python tests/integration/test_llm.py
"""

import asyncio
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

_SYSTEM_INSTRUCTIONS = {
    "role": "system",
    "content": (
        "You are a math tutor.\n"
        "Always write a short plan first.\n"
        "Do NOT do arithmetic in your head.\n"
        "For every arithmetic operation, request a tool call to the calculator.\n"
        "After tool results, continue. Provide final answer with explanation.\n"
    ),
}


async def get_mcp_tools() -> list[dict]:
    """Connect to the Calculator MCP server, and list the tools."""
    logger.info("Connecting to Calculator MCP server")
    async with CalcMCPClient() as calcmcp_client:
        tools = await calcmcp_client.to_openai_tools()
        logger.info("Discovered %d MCP tool(s)", len(tools))
        return tools


async def prompt_llm() -> None:
    """Connect to LLM and send a prompt."""
    logger.info("Starting LLM prompt test")
    tools = await get_mcp_tools()
    logger.debug(
        "Creating OpenAIClient with base_url=%s, model=%s",
        _BASE_URL,
        _MODEL,
    )
    llm = OpenAIClient(_API_KEY, _BASE_URL, _MODEL, tools)
    messages = [
        _SYSTEM_INSTRUCTIONS,
        {"role": "user", "content": "4+4?"},
    ]
    logger.debug("Sending prompt: %s", messages[-1]["content"])
    result = await llm.create_response(messages)
    logger.info("LLM response: %s", result)


async def main() -> None:
    """Entry point for the OpenAI client."""
    logger.info("Running integration test for OpenAIClient")
    await prompt_llm()
    logger.info("Integration test completed")


if __name__ == "__main__":
    asyncio.run(main())
