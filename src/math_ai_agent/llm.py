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

"""Async OpenAI client wrapper for LLM chat completions.

Provides the ``OpenAIClient`` class that manages a shared
``AsyncOpenAI`` instance and sends chat completion requests
to the configured LLM model with tool definitions.
"""

import logging
from typing import Any, Optional

from openai import AsyncOpenAI

from math_ai_agent.config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class OpenAIClient:
    """Singleton async OpenAI client for LLM chat completions.

    Class variables are initialized once on first instantiation;
    subsequent calls to ``__init__`` are no-ops.
    """

    openai_client: Optional[AsyncOpenAI] = None
    calcmcp_tools: Optional[list[dict[str, Any]]] = None
    model: Optional[str] = None

    def __init__(
        self,
        _api_key: str,
        _base_url: str,
        _model: str,
        _calcmcp_tools: list[dict],
    ) -> None:
        """Initialize the OpenAI client once with the given parameters."""
        if OpenAIClient.openai_client is not None:
            logger.debug("OpenAIClient already initialized, skipping")
            return
        if not _api_key:
            logger.error("_api_key is empty or None")
            raise ValueError("_api_key must not be empty")
        if not _base_url:
            logger.error("_base_url is empty or None")
            raise ValueError("_base_url must not be empty")
        if not _model:
            logger.error("_model is empty or None")
            raise ValueError("_model must not be empty")
        if not _calcmcp_tools:
            logger.error("_calcmcp_tools is empty or None")
            raise ValueError("_calcmcp_tools must not be empty")
        logger.info(
            "Initializing OpenAIClient with base_url=%s, model=%s",
            _base_url,
            _model,
        )
        logger.debug("Registering %d tool(s)", len(_calcmcp_tools))
        OpenAIClient.openai_client = AsyncOpenAI(
            api_key=_api_key,
            base_url=_base_url,
        )
        OpenAIClient.calcmcp_tools = _calcmcp_tools
        OpenAIClient.model = _model
        logger.info("OpenAIClient initialized successfully")

    async def create_response(self, messages: list[dict[str, Any]]) -> str:
        """Send messages to the LLM and return the response text."""
        logger.debug(
            "Sending %d message(s) to model %s",
            len(messages),
            OpenAIClient.model,
        )
        logger.debug(
            "Using %d tool(s)", len(OpenAIClient.calcmcp_tools)  # type: ignore[arg-type]
        )
        response = await OpenAIClient.openai_client.chat.completions.create(  # type: ignore[union-attr]
            model=OpenAIClient.model,  # type: ignore[arg-type]
            messages=messages,  # type: ignore[arg-type]
            tools=OpenAIClient.calcmcp_tools,  # type: ignore[arg-type]
        )
        logger.debug("Finish reason: %s", response.choices[0].finish_reason)
        message = response.choices[0].message
        logger.debug(
            "Message attributes: role=%s, content=%s, "
            "tool_calls=%s, function_call=%s, refusal=%s",
            message.role,
            message.content,
            message.tool_calls,
            message.function_call,
            message.refusal,
        )
        if message.content is None:
            logger.warning(
                "Model %s returned tool calls instead of text",
                OpenAIClient.model,
            )
            if message.tool_calls:
                for tc in message.tool_calls:
                    logger.debug(
                        "Tool call requested: %s(%s)",
                        tc.function.name,  # type: ignore[union-attr]
                        tc.function.arguments,  # type: ignore[union-attr]
                    )
            return ""
        logger.info("Received response from model %s", OpenAIClient.model)
        logger.debug("Response text: %s", message.content)
        return message.content
