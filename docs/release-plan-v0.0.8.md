# Release Plan v0.0.8

**Repository:** rubensgomes/math-ai-agent
**Date:** 2026-03-09
**Previous Version:** 0.0.7
**New Version:** 0.0.8

## Summary of Changes

- Renamed `tests/integration/openai_client.py` to `test_openai_client.py`
  (pytest discovery convention)
- Fixed `chat.completions` response attribute: replaced `response.output_text`
  with `response.choices[0].message.content`
- Updated docstring run command to reference new filename
- Updated README.md, CHANGELOG.md, and llms.txt with renamed file

## Release Steps

- [x] Run `poetry run mypy src/` — no issues
- [x] Run `poetry run isort src/ tests/` — no issues
- [x] Run `poetry run black src/ tests/` — reformatted test_openai_client.py
- [x] Run `poetry run pytest` — 42 passed
- [x] Run `poetry build -v` — built successfully
- [x] Ensure `CHANGELOG.md` exists and is updated for v0.0.8
- [x] Bump version in `pyproject.toml` to 0.0.8
- [ ] Commit all changes to main
- [ ] Create version tag `v0.0.8`
- [ ] Push commit and tag to remote
- [ ] Create GitHub release for v0.0.8
