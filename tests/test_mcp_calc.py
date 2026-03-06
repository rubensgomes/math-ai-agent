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

"""Unit tests for :mod:`math_ai_agent.mcp_calc`."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from cryptography.fernet import Fernet
from fastmcp import Client

from math_ai_agent import mcp_calc
from math_ai_agent.mcp_calc import CalcMCP

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clear_tools_cache():
    """Reset the class-level tool cache before each test."""
    CalcMCP.tools = []
    yield
    CalcMCP.tools = []


def _make_mock_client(tools=None, call_result="42"):
    """Return an ``AsyncMock`` that quacks like a ``fastmcp.Client``."""
    mock = AsyncMock()
    mock.ping = AsyncMock()
    mock.list_tools = AsyncMock(return_value=tools or [])
    mock.call_tool = AsyncMock(return_value=call_result)
    mock.__aenter__ = AsyncMock(return_value=mock)
    mock.__aexit__ = AsyncMock(return_value=False)
    return mock


# ---------------------------------------------------------------------------
# _create_client — no OAuth
# ---------------------------------------------------------------------------


@patch.object(mcp_calc, "is_oauth", return_value=False)
@patch.object(mcp_calc, "get_url", return_value="http://localhost:9000/mcp")
def test_create_client_no_oauth(mock_url, mock_oauth):
    client = CalcMCP._create_client()
    assert isinstance(client, Client)
    mock_url.assert_called_once()
    mock_oauth.assert_called_once()


# ---------------------------------------------------------------------------
# _create_client — with OAuth
# ---------------------------------------------------------------------------


@patch.object(mcp_calc, "get_callback_port", return_value=10000)
@patch.object(mcp_calc, "get_token_dir", return_value="/tmp/test-tokens")
@patch.object(mcp_calc, "is_oauth", return_value=True)
@patch.object(mcp_calc, "get_url", return_value="http://localhost:9000/mcp")
def test_create_client_with_oauth(
    mock_url, mock_oauth, mock_token_dir, mock_port, monkeypatch
):
    key = Fernet.generate_key().decode()
    monkeypatch.setenv("OAUTH_STORAGE_ENCRYPTION_KEY", key)
    client = CalcMCP._create_client()
    assert isinstance(client, Client)
    mock_url.assert_called_once()
    mock_token_dir.assert_called_once()
    mock_port.assert_called_once()


@patch.object(mcp_calc, "get_callback_port", return_value=10000)
@patch.object(mcp_calc, "get_token_dir", return_value="/tmp/test-tokens")
@patch.object(mcp_calc, "is_oauth", return_value=True)
@patch.object(mcp_calc, "get_url", return_value="http://localhost:9000/mcp")
def test_create_client_oauth_missing_env_raises(
    mock_url, mock_oauth, mock_token_dir, mock_port, monkeypatch
):
    monkeypatch.delenv("OAUTH_STORAGE_ENCRYPTION_KEY", raising=False)
    with pytest.raises(KeyError):
        CalcMCP._create_client()


# ---------------------------------------------------------------------------
# __init__
# ---------------------------------------------------------------------------


@patch.object(CalcMCP, "_create_client", return_value=AsyncMock())
def test_init_creates_client(mock_create):
    calc = CalcMCP()
    mock_create.assert_called_once()
    assert calc._client is mock_create.return_value


# ---------------------------------------------------------------------------
# async context manager (__aenter__ / __aexit__)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_aenter_pings_and_populates_tools():
    tools = [
        SimpleNamespace(name="add", description="Add two numbers"),
    ]
    mock_client = _make_mock_client(tools=tools)

    with patch.object(CalcMCP, "_create_client", return_value=mock_client):
        async with CalcMCP() as calc:
            mock_client.ping.assert_awaited_once()
            assert CalcMCP.tools == tools
            assert calc is not None


@pytest.mark.asyncio
async def test_aexit_delegates_to_client():
    mock_client = _make_mock_client()

    with patch.object(CalcMCP, "_create_client", return_value=mock_client):
        async with CalcMCP():
            pass

    mock_client.__aexit__.assert_awaited_once()


# ---------------------------------------------------------------------------
# ensure_tools — caching behaviour
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_ensure_tools_fetches_when_empty():
    tools = [SimpleNamespace(name="sqrt", description="Square root")]
    mock_client = _make_mock_client(tools=tools)

    with patch.object(CalcMCP, "_create_client", return_value=mock_client):
        calc = CalcMCP()
        result = await calc.ensure_tools()

    assert result == tools
    assert CalcMCP.tools == tools
    mock_client.list_tools.assert_awaited_once()


@pytest.mark.asyncio
async def test_ensure_tools_returns_cache_on_second_call():
    tools = [SimpleNamespace(name="add", description="Add")]
    mock_client = _make_mock_client(tools=tools)

    with patch.object(CalcMCP, "_create_client", return_value=mock_client):
        calc = CalcMCP()
        first = await calc.ensure_tools()
        second = await calc.ensure_tools()

    assert first is second
    # list_tools should only have been called once (cache hit)
    mock_client.list_tools.assert_awaited_once()


# ---------------------------------------------------------------------------
# call
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_call_delegates_to_client():
    mock_client = _make_mock_client(call_result="5")

    with patch.object(CalcMCP, "_create_client", return_value=mock_client):
        calc = CalcMCP()
        result = await calc.call("add", {"a": 2, "b": 3})

    assert result == "5"
    mock_client.call_tool.assert_awaited_once_with("add", {"a": 2, "b": 3})


@pytest.mark.asyncio
async def test_call_with_empty_arguments():
    mock_client = _make_mock_client(call_result="ok")

    with patch.object(CalcMCP, "_create_client", return_value=mock_client):
        calc = CalcMCP()
        result = await calc.call("noop", {})

    assert result == "ok"
    mock_client.call_tool.assert_awaited_once_with("noop", {})


# ---------------------------------------------------------------------------
# Full round-trip (context manager + call)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_full_round_trip():
    tools = [
        SimpleNamespace(name="multiply", description="Multiply"),
    ]
    mock_client = _make_mock_client(tools=tools, call_result="21")

    with patch.object(CalcMCP, "_create_client", return_value=mock_client):
        async with CalcMCP() as calc:
            assert CalcMCP.tools == tools
            result = await calc.call("multiply", {"a": 3, "b": 7})
            assert result == "21"
