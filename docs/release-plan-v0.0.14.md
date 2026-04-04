# Release Plan v0.0.14

## Summary

Restructure project into `mcp` and `llm` sub-packages, move modules and
functions to their new locations, and rename files for consistency.

## Checklist

- [x] Run `poetry run mypy src/` and fix any issues
- [x] Run `poetry run isort src/ tests/` and fix any issues
- [x] Run `poetry run black src/ tests/` and fix any issues
- [x] Run `poetry run pytest` and fix any issues
- [x] Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` and fix any issues
- [x] Update `CHANGELOG.md` with v0.0.14 changes
- [x] Bump version in `pyproject.toml` to 0.0.14
- [x] Commit all changes to main, create tag, push, and create GitHub release
