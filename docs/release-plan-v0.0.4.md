# Release Plan - v0.0.4

**Project:** math-ai-agent
**Repository:** rubensgomes/math-ai-agent
**Target Version:** v0.0.4
**Date:** 2026-03-06

## Pre-flight Checks

- [x] GitHub repository exists and is accessible
- [x] GitHub connectivity tests passed (scripts/test_github.sh)

## Release Steps

- [x] **Step 1:** Run `poetry run mypy src/` and fix any issues (no issues found)
- [x] **Step 2:** Run `poetry run isort src/ tests/` and fix any issues (no changes needed)
- [x] **Step 3:** Run `poetry run black src/ tests/` and fix any issues (8 files unchanged)
- [x] **Step 4:** Run `poetry run pytest` and fix any issues (35 tests passed)
- [x] **Step 5:** Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` and fix any issues (built successfully)
- [x] **Step 6:** Ensure `CHANGELOG.md` exists in project root (confirmed)
- [x] **Step 7:** Update `CHANGELOG.md` with v0.0.4 release changes (updated)
- [x] **Step 8:** Commit all changes to main, create tag v0.0.4, push, and create GitHub release
