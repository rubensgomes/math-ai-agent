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

"""Async context-managed wrapper around the calculator MCP server.

Provides the ``CalcMCP`` class which connects to a remote calculator
MCP server, caches its tool list, and exposes a ``call()`` method to
invoke individual tools by name.
"""

import asyncio
import logging
import os

import mcp.types
from cryptography.fernet import Fernet
from fastmcp import Client
from fastmcp.client.auth import OAuth
from fastmcp.client.client import CallToolResult
from key_value.aio.stores.disk import DiskStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper

from math_ai_agent.config import (
    get_callback_port,
    get_token_dir,
    get_url,
    is_oauth,
)

logger = logging.getLogger(__name__)


class CalcMCP:
    """Async context manager for the calculator MCP server.

    Maintains a class-level cache of available tools (populated on
    first connection) and delegates tool invocations to the underlying
    ``fastmcp.Client``.

    Usage::

        async with CalcMCP() as calc:
            result = await calc.call("add", {"a": 1, "b": 2})
    """

    tools: list[mcp.types.Tool] = []
    _lock = asyncio.Lock()

    def __init__(self) -> None:
        logger.debug("Instantiating CalcMCP")
        self._client: Client = CalcMCP._create_client()

    async def __aenter__(self) -> "CalcMCP":
        """Connect to the MCP server and populate the tool cache."""
        logger.debug("Connecting to Calculator MCP server")
        await self._client.__aenter__()
        logger.debug("Pinging MCP server")
        await self._client.ping()
        await self.ensure_tools()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Disconnect from the MCP server."""
        logger.debug("Closing CalcMCP")
        await self._client.__aexit__(exc_type, exc, tb)

    async def ensure_tools(self) -> list[mcp.types.Tool]:
        """Populate the class-level tool cache if empty.

        Thread-safe via an ``asyncio.Lock``.  Subsequent calls return
        the cached list without contacting the server.

        Returns:
            The list of tools available on the MCP server.
        """
        async with CalcMCP._lock:
            if not CalcMCP.tools:
                logger.debug("CalcMCP.tools is empty: fetching from MCP server")
                CalcMCP.tools = await self._client.list_tools()
            return CalcMCP.tools

    async def call(self, tool_name: str, arguments: dict) -> CallToolResult:
        """Invoke a tool on the MCP server.

        Args:
            tool_name: Name of the tool to call.
            arguments: Keyword arguments for the tool.

        Returns:
            The ``CallToolResult`` returned by the MCP server.
        """
        result = await self._client.call_tool(tool_name, arguments)
        return result

    @staticmethod
    def _create_client() -> Client:
        """Create and return an MCP Client based on config.yaml settings.

        Returns:
            A ``fastmcp.Client`` configured for the calculator MCP server,
            with OAuth authentication when enabled in config.yaml.
        """
        url = get_url()
        logger.info("Creating HTTP MCP client: %s", url)

        if is_oauth():
            logger.info("OAuth enabled, using OAuthClient")
            token_dir = get_token_dir()
            logger.debug(
                "Creating encrypted disk storage for OAuth tokens: %s",
                token_dir,
            )
            encrypted_storage = FernetEncryptionWrapper(
                key_value=DiskStore(directory=token_dir),
                fernet=Fernet(os.environ["OAUTH_STORAGE_ENCRYPTION_KEY"]),
            )
            oauth = OAuth(
                token_storage=encrypted_storage,
                callback_port=get_callback_port(),
                additional_client_metadata={
                    "token_endpoint_auth_method": "client_secret_post",
                },
            )
            return Client(url, auth=oauth)

        return Client(url)
