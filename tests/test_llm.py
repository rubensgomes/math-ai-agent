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

"""Unit tests for :mod:`math_ai_agent.llm`."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from math_ai_agent.llm import OpenAIClient

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_API_KEY = "test-api-key"
_BASE_URL = "http://localhost:11434/v1"
_MODEL = "test-model"
_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        },
    }
]


@pytest.fixture(autouse=True)
def _reset_singleton():
    """Reset OpenAIClient class variables before each test."""
    OpenAIClient.openai_client = None
    OpenAIClient.calcmcp_tools = None
    OpenAIClient.model = None
    yield
    OpenAIClient.openai_client = None
    OpenAIClient.calcmcp_tools = None
    OpenAIClient.model = None


def _make_chat_completion(content="42", tool_calls=None, finish_reason="stop"):
    """Build a fake ChatCompletion-like response object."""
    message = SimpleNamespace(
        role="assistant",
        content=content,
        tool_calls=tool_calls,
        function_call=None,
        refusal=None,
    )
    choice = SimpleNamespace(
        message=message,
        finish_reason=finish_reason,
    )
    return SimpleNamespace(choices=[choice])


# ---------------------------------------------------------------------------
# __init__ — validation
# ---------------------------------------------------------------------------


def test_init_sets_class_variables():
    """First instantiation sets class variables."""
    client = OpenAIClient(_API_KEY, _BASE_URL, _MODEL, _TOOLS)
    assert OpenAIClient.openai_client is not None
    assert OpenAIClient.calcmcp_tools is _TOOLS
    assert OpenAIClient.model == _MODEL
    assert isinstance(client, OpenAIClient)


def test_init_singleton_skips_second_init():
    """Second instantiation is a no-op."""
    OpenAIClient(_API_KEY, _BASE_URL, _MODEL, _TOOLS)
    original_client = OpenAIClient.openai_client

    OpenAIClient("other-key", "other-url", "other-model", [{"x": 1}])
    assert OpenAIClient.openai_client is original_client
    assert OpenAIClient.model == _MODEL


def test_init_empty_api_key_raises():
    """Empty api_key raises ValueError."""
    with pytest.raises(ValueError, match="_api_key must not be empty"):
        OpenAIClient("", _BASE_URL, _MODEL, _TOOLS)


def test_init_empty_base_url_raises():
    """Empty base_url raises ValueError."""
    with pytest.raises(ValueError, match="_base_url must not be empty"):
        OpenAIClient(_API_KEY, "", _MODEL, _TOOLS)


def test_init_empty_model_raises():
    """Empty model raises ValueError."""
    with pytest.raises(ValueError, match="_model must not be empty"):
        OpenAIClient(_API_KEY, _BASE_URL, "", _TOOLS)


def test_init_empty_tools_raises():
    """Empty tools list raises ValueError."""
    with pytest.raises(ValueError, match="_calcmcp_tools must not be empty"):
        OpenAIClient(_API_KEY, _BASE_URL, _MODEL, [])


def test_init_none_api_key_raises():
    """None api_key raises ValueError."""
    with pytest.raises(ValueError, match="_api_key must not be empty"):
        OpenAIClient(None, _BASE_URL, _MODEL, _TOOLS)


# ---------------------------------------------------------------------------
# create_response — text response
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_response_returns_completion():
    """create_response returns the ChatCompletion from the API."""
    fake_response = _make_chat_completion(content="The answer is 8")
    client = OpenAIClient(_API_KEY, _BASE_URL, _MODEL, _TOOLS)

    mock_create = AsyncMock(return_value=fake_response)
    OpenAIClient.openai_client.chat = SimpleNamespace(
        completions=SimpleNamespace(create=mock_create)
    )

    messages = [{"role": "user", "content": "4+4?"}]
    result = await client.create_response(messages)

    assert result is fake_response
    assert result.choices[0].message.content == "The answer is 8"
    mock_create.assert_awaited_once_with(
        model=_MODEL,
        messages=messages,
        tools=_TOOLS,
    )


@pytest.mark.asyncio
async def test_create_response_with_tool_calls():
    """create_response handles a response with tool_calls."""
    tool_call = SimpleNamespace(
        id="call_123",
        function=SimpleNamespace(
            name="add",
            arguments='{"a": 2, "b": 3}',
        ),
    )
    fake_response = _make_chat_completion(
        content=None,
        tool_calls=[tool_call],
        finish_reason="tool_calls",
    )
    client = OpenAIClient(_API_KEY, _BASE_URL, _MODEL, _TOOLS)

    mock_create = AsyncMock(return_value=fake_response)
    OpenAIClient.openai_client.chat = SimpleNamespace(
        completions=SimpleNamespace(create=mock_create)
    )

    messages = [{"role": "user", "content": "2+3?"}]
    result = await client.create_response(messages)

    assert result is fake_response
    assert result.choices[0].message.content is None
    assert len(result.choices[0].message.tool_calls) == 1
    assert result.choices[0].message.tool_calls[0].function.name == "add"


@pytest.mark.asyncio
async def test_create_response_with_none_content_no_tool_calls():
    """create_response handles None content without tool_calls."""
    fake_response = _make_chat_completion(
        content=None,
        tool_calls=None,
        finish_reason="stop",
    )
    client = OpenAIClient(_API_KEY, _BASE_URL, _MODEL, _TOOLS)

    mock_create = AsyncMock(return_value=fake_response)
    OpenAIClient.openai_client.chat = SimpleNamespace(
        completions=SimpleNamespace(create=mock_create)
    )

    messages = [{"role": "user", "content": "hello"}]
    result = await client.create_response(messages)

    assert result.choices[0].message.content is None
    assert result.choices[0].message.tool_calls is None


@pytest.mark.asyncio
async def test_create_response_passes_all_messages():
    """create_response forwards the full message history."""
    fake_response = _make_chat_completion(content="done")
    client = OpenAIClient(_API_KEY, _BASE_URL, _MODEL, _TOOLS)

    mock_create = AsyncMock(return_value=fake_response)
    OpenAIClient.openai_client.chat = SimpleNamespace(
        completions=SimpleNamespace(create=mock_create)
    )

    messages = [
        {"role": "system", "content": "You are a math tutor."},
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": "4"},
        {"role": "user", "content": "And 3+3?"},
    ]
    await client.create_response(messages)

    mock_create.assert_awaited_once_with(
        model=_MODEL,
        messages=messages,
        tools=_TOOLS,
    )


@pytest.mark.asyncio
async def test_create_response_multiple_tool_calls():
    """create_response handles multiple tool calls in one response."""
    tool_calls = [
        SimpleNamespace(
            id="call_1",
            function=SimpleNamespace(name="add", arguments='{"a": 1, "b": 2}'),
        ),
        SimpleNamespace(
            id="call_2",
            function=SimpleNamespace(name="add", arguments='{"a": 3, "b": 4}'),
        ),
    ]
    fake_response = _make_chat_completion(
        content=None,
        tool_calls=tool_calls,
        finish_reason="tool_calls",
    )
    client = OpenAIClient(_API_KEY, _BASE_URL, _MODEL, _TOOLS)

    mock_create = AsyncMock(return_value=fake_response)
    OpenAIClient.openai_client.chat = SimpleNamespace(
        completions=SimpleNamespace(create=mock_create)
    )

    messages = [{"role": "user", "content": "(1+2) + (3+4)?"}]
    result = await client.create_response(messages)

    assert len(result.choices[0].message.tool_calls) == 2
