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

Provides the ``OpenAIClient`` class that wraps an
``AsyncOpenAI`` instance and sends chat completion requests
to the configured LLM model with tool definitions.
"""

import json
import logging
from typing import Any

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from math_ai_agent.config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class OpenAIClient:
    """Async OpenAI client for LLM chat completions.

    Each instance holds its own ``AsyncOpenAI`` client,
    model name, and tool definitions.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        calcmcp_tools: list[dict],
    ) -> None:
        """Create an ``AsyncOpenAI`` client for chat completions.

        All parameters are validated and must be non-empty.

        Args:
            api_key: API key for the OpenAI-compatible service.
            base_url: Base URL of the inference endpoint.
            model: Model identifier to use for completions.
            calcmcp_tools: OpenAI-format tool definitions from
                the calculator MCP server.

        Raises:
            ValueError: If any parameter is empty or ``None``.
        """
        if not api_key:
            logger.error("api_key is empty or None")
            raise ValueError("api_key must not be empty")
        if not base_url:
            logger.error("base_url is empty or None")
            raise ValueError("base_url must not be empty")
        if not model:
            logger.error("model is empty or None")
            raise ValueError("model must not be empty")
        if not calcmcp_tools:
            logger.error("calcmcp_tools is empty or None")
            raise ValueError("calcmcp_tools must not be empty")
        logger.info(
            "Initializing OpenAIClient with "
            "base_url=%s, model=%s, tool_count=%d",
            base_url,
            model,
            len(calcmcp_tools),
        )
        logger.debug(
            "Tool definitions:\n%s",
            json.dumps(calcmcp_tools, indent=2),
        )
        self.openai_client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.calcmcp_tools = calcmcp_tools
        self.model = model

    async def create_response(
        self, messages: list[dict[str, Any]]
    ) -> ChatCompletion:
        """Send messages to the LLM and return the response.

        Args:
            messages: Conversation history as a list of
                role/content dicts.

        Returns:
            The ``ChatCompletion`` from the configured model.
        """
        logger.debug(
            "Sending %d message(s) to model %s",
            len(messages),
            self.model,
        )
        response: ChatCompletion = (
            await self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore[arg-type]
                tools=self.calcmcp_tools,  # type: ignore[arg-type]
            )
        )
        logger.debug(
            "LLM response:\n%s",
            json.dumps(response.model_dump(), indent=2),
        )
        return response
