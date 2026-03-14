# Release Plan v0.0.9

**Date:** 2026-03-14
**Repository:** rubensgomes/math-ai-agent

## Pre-release Checks

- [x] Verify GitHub repository exists and is accessible
- [x] Run `scripts/test_github.sh rubensgomes/math-ai-agent` successfully

## Release Steps

- [x] Run `poetry run mypy src/` and fix any issues
- [x] Run `poetry run isort src/ tests/` and fix any issues
- [x] Run `poetry run black src/ tests/` and fix any issues
- [x] Run `poetry run pytest` and fix any issues
- [x] Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` and fix any issues
- [x] Ensure `CHANGELOG.md` exists and update with current release changes
- [x] Bump version in `pyproject.toml` to `0.0.9`
- [x] Commit all changes to main, create tag `v0.0.9`, push, and create GitHub release

## Changes in This Release

### Changed

- Refactored `OpenAIClient` in `llm.py` to accept `_api_key`, `_base_url`, `_model`, and `_calcmcp_tools` as constructor parameters (removed module-level constants)
- Replaced synchronous `OpenAI` client with `AsyncOpenAI` for proper async support
- Updated module docstring and class docstring in `llm.py` to reflect current architecture
- Updated `README.md` project structure with `models.py`, `test_llm.py`, and corrected `llm.py` description

### Added

- `tests/integration/test_llm.py` integration test for the `OpenAIClient` wrapper
- Input validation in `OpenAIClient.__init__` for all constructor parameters
- Singleton guard to ensure `OpenAIClient` class variables are initialized only once
- Comprehensive logging across all functions in `src/` modules
- Logging in `tests/integration/test_openai_client.py` with timing and model/API type display
- Try/except error handling in `tests/integration/test_openai_client.py`
- Docstrings to all classes and functions in `src/` modules
- Guard for `None` content in `create_response` when LLM returns tool calls
- Debug logging of all message attributes in `create_response`

### Fixed

- Fixed `OpenAIClient.__init__` assigning to local variables instead of class variables
- Fixed circular dependency in `config.py` where `logger.debug` was called before logger was initialized
- Fixed `test_llm.py`: corrected method name (`send_messages` to `create_response`), fixed nested `_SYSTEM_INSTRUCTIONS` dict, added `asyncio.run()`, proper `CalcMCPClient` context manager usage
- Removed unused imports (`os`, `json`, `time`, `OpenAI`) from `llm.py` and `test_llm.py`
