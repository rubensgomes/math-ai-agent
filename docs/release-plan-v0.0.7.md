# Release Plan — v0.0.7

## Summary

Refactors the calculator MCP client to extend `fastmcp.Client` directly,
renames files to follow PEP 8 conventions, removes unit tests for
integration test code, and updates all project documentation.

## Changes

### Changed

- Refactored `CalcMCPClient` to extend `fastmcp.Client` (removed wrapper
  delegation pattern with `_client`, `_create_client()`, and `call()`)
- Renamed `CalcMCP` class to `CalcMCPClient`
- Renamed `mcp_calc.py` to `calc_mcp_client.py` (PEP 8 module naming)
- Renamed `calc_mcp_client.py` integration test to
  `test_calc_mcp_client.py` (pytest discovery convention)
- Changed `to_openai_tools()` from static method to async instance method
  that calls `self.list_tools()` internally
- Integration test now prints tools in OpenAI function-calling JSON format
- `__aenter__` no longer pre-populates the tool cache
- Callers use inherited `call_tool()` instead of removed `call()` wrapper

### Removed

- Removed unit tests for integration test source code
- Removed dead `create_client()` function and unused imports from
  integration test

### Fixed

- Fixed stale log message referencing old `CalcMCP.tools` attribute name
- Fixed stale docstrings referencing old "wrapper" architecture
- Updated all documentation (README.md, CLAUDE.md, llms.txt) with current
  file names, project structure, and API descriptions

## Checklist

- [x] Run `poetry run mypy src/` — fix any issues
- [x] Run `poetry run isort src/ tests/` — fix any issues
- [x] Run `poetry run black src/ tests/` — fix any issues
- [x] Run `poetry run pytest` — fix any issues
- [x] Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` — fix any issues
- [x] Update version in `pyproject.toml` to `0.0.7`
- [x] Update `CHANGELOG.md` with release changes
- [x] Commit all changes, create tag `v0.0.7`, push, and create GitHub release
