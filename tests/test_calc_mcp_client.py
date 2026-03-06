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

"""Unit tests for :mod:`tests.integration.calc_mcp_client`."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from cryptography.fernet import Fernet
from fastmcp import Client

from tests.integration import calc_mcp_client

# ---------------------------------------------------------------------------
# _SAMPLE_ARGS
# ---------------------------------------------------------------------------


def test_sample_args_is_dict():
    assert isinstance(calc_mcp_client._SAMPLE_ARGS, dict)


def test_sample_args_has_expected_tools():
    expected = {
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
        "nth_root",
        "modulo",
        "floor_divide",
        "sqrt",
        "absolute",
        "floor",
        "ceil",
        "log10",
        "ln",
        "exp",
        "round_number",
    }
    assert set(calc_mcp_client._SAMPLE_ARGS.keys()) == expected


def test_sample_args_values_are_dicts():
    for name, args in calc_mcp_client._SAMPLE_ARGS.items():
        assert isinstance(args, dict), f"{name} args should be a dict"


# ---------------------------------------------------------------------------
# create_client — no OAuth
# ---------------------------------------------------------------------------


@patch.object(calc_mcp_client, "is_oauth", return_value=False)
@patch.object(
    calc_mcp_client, "get_url", return_value="http://localhost:9000/mcp"
)
def test_create_client_no_oauth(mock_url, mock_oauth):
    client = calc_mcp_client.create_client()
    assert isinstance(client, Client)
    mock_url.assert_called_once()
    mock_oauth.assert_called_once()


# ---------------------------------------------------------------------------
# create_client — with OAuth
# ---------------------------------------------------------------------------


@patch.object(calc_mcp_client, "get_callback_port", return_value=10000)
@patch.object(calc_mcp_client, "get_token_dir", return_value="/tmp/test-tokens")
@patch.object(calc_mcp_client, "is_oauth", return_value=True)
@patch.object(
    calc_mcp_client, "get_url", return_value="http://localhost:9000/mcp"
)
def test_create_client_with_oauth(
    mock_url, mock_oauth, mock_token_dir, mock_port, monkeypatch
):
    key = Fernet.generate_key().decode()
    monkeypatch.setenv("OAUTH_STORAGE_ENCRYPTION_KEY", key)
    client = calc_mcp_client.create_client()
    assert isinstance(client, Client)
    mock_url.assert_called_once()
    mock_token_dir.assert_called_once()
    mock_port.assert_called_once()


@patch.object(calc_mcp_client, "get_callback_port", return_value=10000)
@patch.object(calc_mcp_client, "get_token_dir", return_value="/tmp/test-tokens")
@patch.object(calc_mcp_client, "is_oauth", return_value=True)
@patch.object(
    calc_mcp_client, "get_url", return_value="http://localhost:9000/mcp"
)
def test_create_client_oauth_missing_env_var_raises(
    mock_url, mock_oauth, mock_token_dir, mock_port, monkeypatch
):
    monkeypatch.delenv("OAUTH_STORAGE_ENCRYPTION_KEY", raising=False)
    with pytest.raises(KeyError):
        calc_mcp_client.create_client()


# ---------------------------------------------------------------------------
# run_client
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_run_client(capsys):
    tool = SimpleNamespace(name="add", description="Add two numbers")
    mock_client = AsyncMock()
    mock_client.ping = AsyncMock()
    mock_client.list_tools = AsyncMock(return_value=[tool])
    mock_client.call_tool = AsyncMock(return_value="5")
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch.object(
        calc_mcp_client, "create_client", return_value=mock_client
    ):
        await calc_mcp_client.run_client()

    mock_client.ping.assert_awaited_once()
    mock_client.list_tools.assert_awaited_once()
    mock_client.call_tool.assert_awaited_once_with("add", {"a": 2, "b": 3})

    output = capsys.readouterr().out
    assert "1 tools available" in output
    assert "add: Add two numbers" in output
    assert "=> 5" in output


@pytest.mark.asyncio
async def test_run_client_unknown_tool_uses_empty_args():
    tool = SimpleNamespace(name="unknown_op", description="Mystery tool")
    mock_client = AsyncMock()
    mock_client.ping = AsyncMock()
    mock_client.list_tools = AsyncMock(return_value=[tool])
    mock_client.call_tool = AsyncMock(return_value="ok")
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch.object(
        calc_mcp_client, "create_client", return_value=mock_client
    ):
        await calc_mcp_client.run_client()

    mock_client.call_tool.assert_awaited_once_with("unknown_op", {})


@pytest.mark.asyncio
async def test_run_client_multiple_tools(capsys):
    tools = [
        SimpleNamespace(name="add", description="Add"),
        SimpleNamespace(name="sqrt", description="Square root"),
    ]
    mock_client = AsyncMock()
    mock_client.ping = AsyncMock()
    mock_client.list_tools = AsyncMock(return_value=tools)
    mock_client.call_tool = AsyncMock(return_value="result")
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch.object(
        calc_mcp_client, "create_client", return_value=mock_client
    ):
        await calc_mcp_client.run_client()

    assert mock_client.call_tool.await_count == 2
    output = capsys.readouterr().out
    assert "2 tools available" in output


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def test_main_calls_asyncio_run():
    with patch.object(calc_mcp_client.asyncio, "run") as mock_run:
        calc_mcp_client.main()
        mock_run.assert_called_once()
