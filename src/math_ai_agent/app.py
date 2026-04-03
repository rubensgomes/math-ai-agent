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

"""The FastAPI web server app.

Launches a FastAPI web server with the following endpoints:
    - `GET /` returns the index.html page.
    - `POST /prompt/` submits user prompt and returns AI response.

From the project root folder run::

    poetry run uvicorn math_ai_agent.app:app --reload
"""

import json
import logging
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from openai.types.chat import ChatCompletion, ChatCompletionMessage

from math_ai_agent.calc_mcp_client import CalcMCPClient
from math_ai_agent.config import configure_logging
from math_ai_agent.llm import OpenAIClient
from math_ai_agent.models import Prompt

configure_logging()
logger = logging.getLogger(__name__)

# GitHub Marketplace Model
_API_KEY = os.environ.get("RUBENS_PAT_TOKEN")
_BASE_URL = "https://models.github.ai/inference"
_MODEL = "openai/gpt-4.1"
# folder to HTML file
_STATIC_DIR = Path(__file__).parent / "static"
# Initial text to provide to the LLM context.
_SYSTEM_INSTRUCTIONS = (
    "You are a careful math assistant tutor helping solve math"
    " problems. Always write a short plan first. Do NOT do"
    " arithmetic in your head. For every math operation, request"
    " a tool call to the calculator. After tool results, continue."
    " Provide final answer with explanation."
)

# -------------------------------------------------
# Create the FastAPI app instance
# -------------------------------------------------
app = FastAPI()
app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")


# -------------------------------------------------
# Helpers
# -------------------------------------------------
async def get_mcp_tools() -> list[dict[str, object]]:
    """Discover available tools from the Calculator MCP server.

    Returns:
        OpenAI-format tool definitions discovered from the
        MCP server.
    """
    logger.debug("Discovering Calculator MCP tools")
    async with CalcMCPClient() as calcmcp_client:
        tools = await calcmcp_client.to_openai_tools()
    logger.debug("Discovered %d MCP tool(s)", len(tools))
    return tools


async def call_tool(tool_name: str, args: dict) -> str:
    """Call a calculator MCP tool over a new connection.

    Args:
        tool_name: The name of the MCP tool to invoke.
        args: The arguments to pass to the tool.

    Returns:
        The string representation of the tool result.

    Raises:
        Exception: If the MCP tool call fails.
    """
    async with CalcMCPClient() as calcmcp_client:
        logger.debug(
            "Calling calculator MCP tool %s with %s",
            tool_name,
            args,
        )
        result = await calcmcp_client.call_tool(tool_name, args)
        logger.debug(
            "Tool %s result:\n%s",
            tool_name,
            json.dumps(result.structured_content, indent=2),
        )
        return str(result.data)


# -------------------------------------------------
# Agent loop
# -------------------------------------------------
async def agent_loop(user_prompt: str) -> str:
    """Run the interactive agent loop with LLM tool calling.

    Discovers MCP tools, sends the user prompt to the LLM, and
    dispatches any tool calls to the calculator MCP server
    until the LLM produces a final text response.

    Args:
        user_prompt: The math question from the user.

    Returns:
        The final text response from the LLM.

    Raises:
        RuntimeError: If the API key is not set, the token
            limit is reached, or the content is blocked by a
            safety filter.
        ValueError: If the LLM returns an unknown finish
            reason.
    """
    logger.debug("Starting AI LLM agent loop")
    if not _API_KEY:
        raise RuntimeError("RUBENS_PAT_TOKEN environment variable is not set.")
    context: list[Any] = [{"role": "system", "content": _SYSTEM_INSTRUCTIONS}]
    tools = await get_mcp_tools()
    llm = OpenAIClient(_API_KEY, _BASE_URL, _MODEL, tools)

    context.append({"role": "user", "content": user_prompt})
    logger.debug("Sending user prompt: %s", user_prompt)
    logger.debug("Starting agent loop.")

    # -------------------------
    # Agent Loop
    # -------------------------
    while True:
        response: ChatCompletion = await llm.create_response(context)
        llm_msg: ChatCompletionMessage = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        match finish_reason:
            case "stop":
                logger.info("Assistant (LLM) response: %s", llm_msg.content)
                break

            case "length":
                error = "Token limit reached."
                logger.error(error)
                raise RuntimeError(error)

            case "tool_calls":
                context.append(llm_msg)
                assert llm_msg.tool_calls is not None
                for tool_call in llm_msg.tool_calls:
                    fn = tool_call.function  # type: ignore[union-attr]
                    tool_name = fn.name
                    tool_call_id = tool_call.id
                    args = json.loads(fn.arguments)
                    logger.debug(
                        "Calling tool_call_id: %s, tool_name: %s",
                        tool_call_id,
                        tool_name,
                    )
                    result = await call_tool(tool_name, args)
                    context.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": result,
                        }
                    )
                continue

            case "content_filter":
                error = (
                    f"The content [{context}] was blocked for safety reasons."
                )
                logger.error(error)
                raise RuntimeError(error)

            case None:
                # Happens during streaming before final chunk
                logger.debug("Streaming before final chunk. Continue ...")
                continue

            case _:
                error = f"Unknown finish_reason: {finish_reason}"
                logger.error(error)
                raise ValueError(error)

    logger.debug("Returning final response message from LLM.")
    return llm_msg.content or ""


# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    """Serve the main HTML page.

    Returns:
        The HTML content of the index page.
    """
    logger.debug("Serving root HTML page: %s%s", _STATIC_DIR, "/index.html")
    return (_STATIC_DIR / "index.html").read_text()


@app.post("/prompt/")
async def prompt(payload: Prompt) -> dict[str, str]:
    """Accept a prompt text from the user and return an answer.

    Args:
        payload: The validated question from the request body.

    Returns:
        A dict containing the `answer` key with the response.

    Raises:
        RuntimeError: If the agent loop encounters a token limit
            or content filter error.
        ValueError: If the LLM returns an unknown finish reason.
    """
    logger.debug("Received prompt: %s", payload.text)
    prompt_text = payload.text.strip()
    logger.debug("Calling LLM with user prompt: %s", prompt_text)
    output = await agent_loop(prompt_text)
    logger.debug("Output:\n%s", json.dumps(output, indent=2))
    return {"answer": output}
