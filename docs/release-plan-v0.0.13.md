# Release Plan v0.0.13

**Repository:** rubensgomes/math-ai-agent
**Date:** 2026-04-03
**Release type:** Patch

## Changes in this release

### Changed

- Renamed `main.py` to `app.py` (FastAPI application module)
- Renamed `tests/test_main.py` to `tests/test_app.py`
- Renamed `tests/integration/app.py` to `tests/integration/test_app.py`
- Refactored `get_mcp_tools()` to use `async with` context manager, fixing
  resource leak from manual `__aenter__()` call
- Removed leaky `get_calcmcp_client()` helper function
- Changed `_SYSTEM_INSTRUCTIONS` from triple-quoted string to implicit
  concatenation, removing leading newline
- Updated all docstrings in `app.py` to follow Google Python Style Guide
  (added `Args`, `Returns`, `Raises` sections)
- Improved `get_mcp_tools()` return type from `list[dict]` to
  `list[dict[str, object]]`
- Fixed `agent_loop` return type annotation from `None` to `str`
- Fixed `None` finish_reason case to `continue` instead of falling through
- Replaced f-string logging with `%s` lazy formatting
- Updated `CLAUDE.md`, `README.md`, `llms.txt` with renamed file references
- Updated `TODO.md` with completed docstring review item

### Removed

- Removed commented-out `_MODEL = "openai/gpt-5"` dead code
- Removed redundant MCP connection/discovery in `/prompt/` endpoint
- Removed stale numbered step comments in `/prompt/` handler

## Release steps

- [x] 1. Run `poetry run mypy src/` and fix any issues
- [x] 2. Run `poetry run isort src/ tests/` and fix any issues
- [x] 3. Run `poetry run black src/ tests/` and fix any issues
- [x] 4. Run `poetry run pytest` and fix any issues
- [x] 5. Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` and fix any issues
- [x] 6. Update `CHANGELOG.md` with current release changes
- [x] 7. Bump version to `0.0.13` in `pyproject.toml`
- [x] 8. Commit all changes to main, create tag `v0.0.13`, push, and create GitHub release
