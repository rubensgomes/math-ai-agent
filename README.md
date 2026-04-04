# math-ai-agent

A Math AI Agent that uses an LLM with Rubens'
[calculator-mcp](https://rubens-calculator-mcp.fastmcp.app/mcp) server to
answer math questions. The project provides a FastAPI web interface where users
submit math questions and receive answers powered by the LLM and MCP tool
integration.

## Features

- **FastAPI web UI** — simple form-based interface for submitting prompts
- **MCP client** — connects to a remote calculator MCP server via
  [FastMCP](https://github.com/jlowin/fastmcp), with optional OAuth
  authentication
- **Configurable** — server URL, OAuth settings, timeouts, and logging are all
  driven by `config.yaml`

## Project Structure

```
src/math_ai_agent/
  app.py                # FastAPI application (web UI + /prompt endpoint)
  config.py             # Configuration helpers (loads config.yaml, logging)
  config.yaml           # Server, OAuth, and logging configuration
  models.py             # Pydantic models (Prompt) for request validation
  llm/
    llm.py              # OpenAI client wrapper and agent loop
  mcp/
    calc_client.py      # Calculator MCP client and helper functions
  static/
    index.html          # Web UI served at /
tests/
  integration/
    test_calc_client.py      # Integration test for the MCP client
    test_openai_client.py    # Integration test for the raw OpenAI SDK
    test_llm.py              # Integration test for the OpenAIClient wrapper
    test_llm_tool.py         # Integration test for LLM with tool calling
    test_app.py              # FastAPI integration test application
    app_text.txt             # Sample text fixture for integration tests
  test_calc_client.py        # Unit tests for calc_client.py
  test_config.py             # Unit tests for config.py
  test_llm.py                # Unit tests for llm.py
  test_app.py                # Unit tests for app.py
```

## Configuration

All settings live in `src/math_ai_agent/config.yaml`:

- **`server.calculator_mcp.url`** — MCP server endpoint
- **`server.calculator_mcp.is_oauth`** — enable/disable OAuth authentication
- **`server.calculator_mcp.token_dir`** — directory for storing OAuth tokens
- **`server.calculator_mcp.callback_port`** — fixed port for the OAuth callback
- **`server.calculator_mcp.timeout`** — HTTP client timeout in seconds
- **`logging`** — Python `logging.config.dictConfig` block

Override the config file path by setting the `CALCULATOR_MCP_CONFIG` environment
variable. When OAuth is enabled, set `OAUTH_STORAGE_ENCRYPTION_KEY` to a
Fernet-compatible key.

## Setup

See [SETUP.md](SETUP.md) for detailed instructions on setting up the
development environment (pyenv, poetry, virtual environment, PyCharm, etc.).

### Quick Start

```bash
# Clone and install
git clone https://github.com/rubensgomes/math-ai-agent
cd math-ai-agent
poetry install

# Run the FastAPI server
poetry run uvicorn math_ai_agent.app:app --reload

# Change to the project root folder
cd $(git rev-parse --show-toplevel) || exit
# Run the MCP integration test client
poetry run python tests/integration/test_calc_client.py
# Run the FastAPI web server test
poetry run uvicorn tests.integration.test_app:app --reload
```

## License

See the disclaimer headers in each source file for copyright and warranty
information.
