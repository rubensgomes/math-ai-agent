# Release Plan v0.0.11

## Pre-Release Checks

- [x] Run `poetry run mypy src/` and fix any issues
- [x] Run `poetry run isort src/ tests/` and fix any issues
- [x] Run `poetry run black src/ tests/` and fix any issues
- [x] Run `poetry run pytest` and fix any issues
- [x] Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` and fix any issues

## Release Steps

- [x] Ensure `CHANGELOG.md` exists and is up to date
- [x] Update `CHANGELOG.md` with current release changes
- [x] Bump version in `pyproject.toml` to `0.0.11`
- [x] Commit all changes to main
- [x] Create version tag `v0.0.11`
- [x] Push commits and tag to remote
- [x] Create GitHub release
