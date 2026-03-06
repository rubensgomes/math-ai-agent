# CLAUDE.md

## Project Overview

Math AI Agent -- a Python application that uses an LLM with a remote calculator
MCP server to answer math questions via a FastAPI web interface.

## Build & Run

```bash
# Install dependencies
poetry install

# Run the FastAPI server
poetry run uvicorn math_ai_agent.main:app --reload

# Run the MCP client standalone
poetry run python -m math_ai_agent.calc_mcp_client
```

## Code Quality

```bash
# Type checking
poetry run mypy src/

# Sort imports
poetry run isort src/ tests/

# Format code (line length 80)
poetry run black src/ tests/

# Run tests
poetry run pytest

# Run tests with coverage (minimum 90%)
poetry run pytest --cov=src/ --cov-report=term-missing

# Full cleanup
poetry run poe clean
```

## Project Conventions

- **Package layout:** `src/math_ai_agent/` with tests in `tests/`
- **Python version:** >= 3.12
- **Line length:** 80 (black + isort)
- **Formatting:** black with isort (profile "black")
- **Type checking:** mypy with `ignore_missing_imports = true`
- **Test framework:** pytest with `asyncio_mode = "auto"`
- **Coverage:** branch coverage, minimum 90% (`fail_under = 90`)
- **Build system:** Poetry 2.3+ with `poetry-core` backend

## Source File Headers

All source files include a disclaimer header with AI content notice, copyright
status, limitation of liability, and no-warranty disclaimer. New source files
must include this same header. Use the `/generate-disclaimer` skill to add it.

## Configuration

- Config is in `src/math_ai_agent/config.yaml`
- Override path via `CALCULATOR_MCP_CONFIG` environment variable
- OAuth requires `OAUTH_STORAGE_ENCRYPTION_KEY` (Fernet key)

## Release Process

- Only Rubens Gomes is authorized to push releases
- Releases use the `/release-plan` slash command in Claude Code
- Release plans are saved in `docs/release-plan-v{VERSION}.md`
- Changelog follows Keep a Changelog format in `CHANGELOG.md`
