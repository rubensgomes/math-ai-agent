# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

