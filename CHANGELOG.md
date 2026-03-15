# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.10] - 2026-03-15

### Added

- `tests/integration/test_llm_tool.py` integration test for LLM tool calling with interactive agent loop
- `tests/test_llm.py` unit tests for `OpenAIClient` (12 tests, 100% coverage on `llm.py`)
- `tests` and `__main__` logger entries in `config.yaml` for test log visibility
- Module docstring in `models.py`
- Return type annotation and Args/Returns docstrings in `main.py` functions
- Args/Returns docstrings in `test_llm_tool.py` functions

### Fixed

- Fixed `test_llm_tool.py`: wrong attribute `tool_call.tool_name` to `tool_call.function.name`
- Fixed `test_llm_tool.py`: missing `await` on `call_tool()` async function
- Fixed `test_llm_tool.py`: duplicate assistant message appended to memory
- Fixed `test_llm_tool.py`: agent loop now handles multiple tool calls and multi-round tool calling
- Fixed `test_llm_tool.py`: assistant message with `tool_calls` preserved (not stripped to plain content)
- Updated stale `llm.py` description in `llms.txt`
- Updated stale `litellm` dependency to `openai` in `llms.txt`
- Added missing `models.py`, `test_llm.py`, `test_llm_tool.py` to project structure in `README.md` and `llms.txt`
- Fixed Python version `3.14.2` to `3.14.3` in `SETUP.md`
- Aligned `gh` CLI version prerequisite in `RELEASE.md` to match `SETUP.md`

## [0.0.9] - 2026-03-14

### Changed

- Refactored `OpenAIClient` in `llm.py` to accept `_api_key`, `_base_url`, `_model`, and `_calcmcp_tools` as constructor parameters (removed module-level constants)
- Replaced synchronous `OpenAI` client with `AsyncOpenAI` for proper async support
- Updated module and class docstrings in `llm.py` to reflect current architecture
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
- Fixed `test_llm.py`: corrected method name, fixed nested dict, added `asyncio.run()`, proper context manager usage
- Removed unused imports from `llm.py` and `test_llm.py`

## [0.0.8] - 2026-03-09

### Changed

- Renamed `tests/integration/openai_client.py` to `test_openai_client.py` (pytest discovery convention)

### Fixed

- Fixed `chat.completions` response handling: replaced invalid `response.output_text` with `response.choices[0].message.content`
- Updated docstring run command to reference renamed filename
- Updated README.md, CHANGELOG.md, and llms.txt with renamed filename

## [0.0.7] - 2026-03-08

### Changed

- Refactored `CalcMCPClient` to extend `fastmcp.Client` directly (removed wrapper delegation pattern)
- Renamed `CalcMCP` class to `CalcMCPClient`
- Renamed `mcp_calc.py` to `calc_mcp_client.py` (PEP 8 module naming)
- Renamed integration test to `test_calc_mcp_client.py` (pytest discovery convention)
- Changed `to_openai_tools()` from static method to async instance method
- Integration test now prints tools in OpenAI function-calling JSON format
- Callers use inherited `call_tool()` instead of removed `call()` wrapper

### Removed

- Removed unit tests for integration test source code
- Removed dead `create_client()` function and unused imports from integration test

### Fixed

- Fixed stale log message referencing old `CalcMCP.tools` attribute name
- Fixed stale docstrings and documentation with current file names and architecture
- Updated README.md, CLAUDE.md, and llms.txt to reflect current project structure

## [0.0.6] - 2026-03-07

### Added

- `OLLAMA.md` documentation for installing and running Ollama with local LLM models
- `llm.py` module with system instructions for the math tutor LLM
- `openai` DEBUG-level logger in `config.yaml` for OpenAI SDK request/response tracing
- Logging integration in `tests/integration/test_openai_client.py` using project config

### Changed

- Renamed `OLLAMAmd` to `OLLAMA.md` (proper Markdown extension)
- Fixed typo in `OLLAMA.md`: "Linus" to "Linux"

## [0.0.5] - 2026-03-06

### Added

- `CalcMCP` async context manager class (`mcp_calc.py`) wrapping the calculator MCP server with tool caching and `call()` API
- Unit tests for `mcp_calc.py` (11 tests, 100% coverage)
- `tests/integration/` directory for integration test scripts
- Disclaimer headers and module docstrings to all source and test files

### Changed

- Moved `calc_mcp_client.py` from `src/math_ai_agent/` to `tests/integration/` (integration test utility, not part of the distributed package)
- Updated `main.py` with module docstring, endpoint docstrings, and return type annotations
- Updated README.md, CLAUDE.md, and llms.txt to reflect new project structure

## [0.0.4] - 2026-03-06

### Added

- MCP client module (`calc_mcp_client.py`) with OAuth-authenticated connection to remote calculator MCP server
- Configuration module (`config.py`) loading settings from `config.yaml` with environment variable override
- YAML configuration file (`config.yaml`) for server, OAuth, and logging settings
- Unit tests for `config.py` (11 tests) and `calc_mcp_client.py` (10 tests)
- CLAUDE.md with project conventions and instructions for Claude Code
- `llms.txt` with LLM-friendly project documentation
- `py-key-value-aio[disk]` runtime dependency for encrypted OAuth token storage

### Changed

- Removed unused imports (`Annotated`, `Form`) from `main.py`
- Changed `httpx` logger level from DEBUG to INFO in `config.yaml`
- Updated README.md with current project structure and documentation
- Updated SETUP.md with current tool versions and instructions
- Reformatted test files to comply with black line-length rules

## [0.0.3] - 2026-02-21

### Changed

- Version bump to 0.0.3
- Updated release plan documentation

## [0.0.2] - 2026-02-21

### Added

- FastAPI web application with root endpoint serving HTML UI
- POST `/prompt/` endpoint accepting math questions via JSON
- MathQuestion Pydantic model for request validation
- Static file serving for frontend assets
- Bootstrap-based dark theme frontend with question/response form
- Comprehensive test suite (14 tests) covering endpoints, validation, and model

## [0.0.1] - 2026-02-20

### Added

- Initial project scaffolding with Poetry build system
- Project structure with `src/math_ai_agent` package layout
- Development tooling: pytest, mypy, black, isort, pylint, coverage
- GitHub connectivity test script (`scripts/test_github.sh`)
- CHANGELOG, LICENSE, README, and SETUP documentation

