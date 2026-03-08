# Release Plan v0.0.5

## Pre-release Checklist

- [x] Run `poetry run mypy src/` and fix any issues
- [x] Run `poetry run isort src/ tests/` and fix any issues
- [x] Run `poetry run black src/ tests/` and fix any issues
- [x] Run `poetry run pytest` and fix any issues (46 passed, 100% coverage)
- [x] Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` and fix any issues
- [x] Ensure `CHANGELOG.md` exists and update with current release changes
- [x] Bump version in `pyproject.toml` to `0.0.5`
- [x] Commit all changes to main, create tag `v0.0.5`, push, and create GitHub release

## Changes in This Release

### Added
- `CalcMCP` async context manager class (`mcp_calc.py`) wrapping the calculator MCP server with tool caching and `call()` API
- Unit tests for `mcp_calc.py` (11 tests, 100% coverage)
- `tests/integration/` directory for integration test scripts
- Disclaimer headers and module docstrings to all source and test files

### Changed
- Moved `calc_mcp_client.py` from `src/math_ai_agent/` to `tests/integration/` (integration test utility, not part of the distributed package)
- Updated `main.py` with module docstring, endpoint docstrings, and return type annotations
- Updated README.md, CLAUDE.md, and llms.txt to reflect new project structure
