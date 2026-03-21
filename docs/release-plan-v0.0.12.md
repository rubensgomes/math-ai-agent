# Release Plan v0.0.12

## Release Summary

Rename `MathQuestion` model to `Prompt` (field `question` → `text`), add
FastAPI integration test application, bump dependencies, and update frontend
and documentation.

## Steps

- [x] Run `poetry run mypy src/` and fix any issues
- [x] Run `poetry run isort src/ tests/` and fix any issues
- [x] Run `poetry run black src/ tests/` and fix any issues
- [x] Run `poetry run pytest` and fix any issues
- [x] Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` and fix any issues
- [x] Ensure `CHANGELOG.md` exists and is up to date
- [x] Update `CHANGELOG.md` with current release changes
- [x] Bump version to 0.0.12 in `pyproject.toml`
- [ ] Commit all changes, create tag `v0.0.12`, push, and create GitHub release
