# math-ai-agent

A Math AI Agent that uses an LLM with Rubens'
[calculator-mcp](https://rubens-calculator-mcp.fastmcp.app/mcp) server to
answer math questions. The project provides a FastAPI web interface where users
submit math questions and receive answers powered by the LLM and MCP tool
integration.

## Features

- **FastAPI web UI** — simple form-based interface for submitting math questions
- **MCP client** — connects to a remote calculator MCP server via
  [FastMCP](https://github.com/jlowin/fastmcp), with optional OAuth
  authentication
- **Configurable** — server URL, OAuth settings, timeouts, and logging are all
  driven by `config.yaml`

## Project Structure

```
src/math_ai_agent/
  main.py               # FastAPI application (web UI + /prompt endpoint)
  calc_mcp_client.py    # Calculator MCP client (extends fastmcp.Client)
  llm.py                # Async OpenAI client wrapper for LLM chat completions
  models.py             # Pydantic models for request validation
  config.py             # Configuration helpers (loads config.yaml, logging)
  config.yaml           # Server, OAuth, and logging configuration
  static/
    index.html          # Web UI served at /
tests/
  integration/
    test_calc_mcp_client.py  # Integration test for the MCP client
    test_openai_client.py    # Integration test for the OpenAI client
    test_llm.py              # Integration test for the OpenAIClient wrapper
  test_calc_mcp_client.py    # Unit tests for calc_mcp_client.py
  test_config.py             # Unit tests for config.py
  test_main.py               # Unit tests for main.py
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
poetry run uvicorn math_ai_agent.main:app --reload

# Run the MCP integration test client
poetry run python tests/integration/test_calc_mcp_client.py
```

## License

See the disclaimer headers in each source file for copyright and warranty
information.
