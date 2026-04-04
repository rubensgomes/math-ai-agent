# Release Plan v0.0.15

## Summary

Update project documentation (`CLAUDE.md`, `README.md`, `TODO.md`, `llms.txt`,
`.claude/commands/release-plan.md`) to reflect the v0.0.14 refactoring that
moved modules into `llm/` and `mcp/` sub-packages, and renamed test files.

## Changes

### Changed

- Fixed stale integration test command in `CLAUDE.md` (`test_calc_mcp_client.py`
  → `test_calc_client.py`)
- Updated project structure in `README.md` to show `llm/` and `mcp/`
  sub-packages and renamed test files
- Updated architecture description and project structure in `llms.txt` to
  reflect four-component design with `llm/` and `mcp/` sub-packages
- Updated `TODO.md` to reference `llm/llm.py` instead of `app.py`, removed
  completed modularization item
- Added documentation review step to `.claude/commands/release-plan.md`

## Checklist

- [x] Run `poetry run mypy src/` and fix any issues
- [x] Run `poetry run isort src/ tests/` and fix any issues
- [x] Run `poetry run black src/ tests/` and fix any issues
- [x] Run `poetry run pytest` and fix any issues
- [x] Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` and fix any issues
- [x] Verify `CHANGELOG.md` exists
- [x] Update `CHANGELOG.md` with v0.0.15 changes
- [x] Bump version to 0.0.15 in `pyproject.toml`
- [ ] Commit all changes, tag, push, and create GitHub release
