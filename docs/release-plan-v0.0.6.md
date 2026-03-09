# Release Plan v0.0.6

## Pre-release Checklist

- [x] Run `poetry run mypy src/` -- no issues
- [x] Run `poetry run isort src/ tests/` -- no issues
- [x] Run `poetry run black src/ tests/` -- 1 file reformatted
- [x] Run `poetry run pytest` -- 53 passed
- [x] Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` -- built successfully
- [x] Verify `CHANGELOG.md` exists
- [x] Update `CHANGELOG.md` with v0.0.6 changes
- [x] Bump version in `pyproject.toml` to 0.0.6

## Release Checklist

- [x] Commit all changes to main
- [x] Create version tag `v0.0.6`
- [x] Push commits and tag to origin
- [x] Create GitHub release

## Changes in This Release

### Added

- `OLLAMA.md` documentation for installing and running Ollama with local LLM models
- `llm.py` module with system instructions for the math tutor LLM
- `openai` DEBUG-level logger in `config.yaml` for OpenAI SDK request/response tracing
- Logging integration in `tests/integration/openai_client.py` using project config

### Changed

- Renamed `OLLAMAmd` to `OLLAMA.md` (proper Markdown extension)
- Fixed typo in `OLLAMA.md`: "Linus" to "Linux"
