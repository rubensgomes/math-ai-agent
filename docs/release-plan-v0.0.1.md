# Release Plan - v0.0.1

**Project:** math-ai-agent
**Repository:** rubensgomes/math-ai-agent
**Target Version:** v0.0.1
**Date:** 2026-02-20

## Pre-flight Checks

- [x] GitHub repository exists and is accessible
- [x] GitHub connectivity tests passed (scripts/test_github.sh)

## Release Steps

- [x] **Step 1:** Run `poetry run mypy src/` and fix any issues
- [x] **Step 2:** Run `poetry run isort src/ tests/` and fix any issues
- [x] **Step 3:** Run `poetry run black src/ tests/` and fix any issues
- [x] **Step 4:** Run `poetry run pytest` and fix any issues (no tests collected - expected for initial release)
- [x] **Step 5:** Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` and fix any issues (updated version to 0.0.1)
- [x] **Step 6:** Ensure `CHANGELOG.md` exists in project root
- [x] **Step 7:** Update `CHANGELOG.md` with v0.0.1 release changes
- [ ] **Step 8:** Commit all changes to main, create tag v0.0.1, push, and create GitHub release
