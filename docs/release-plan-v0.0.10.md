# Release Plan v0.0.10

**Repository:** rubensgomes/math-ai-agent
**Date:** 2026-03-15
**Previous version:** 0.0.9

## Changes in this release

### Added

- `tests/integration/test_llm_tool.py` integration test for LLM tool calling with interactive agent loop
- `tests/test_llm.py` unit tests for `OpenAIClient` (12 tests, 100% coverage on `llm.py`)
- `tests` and `__main__` logger entries in `config.yaml` for test log visibility
- Module docstring in `models.py`
- Return type annotation and Args/Returns docstrings in `main.py` functions
- Args/Returns docstrings in `test_llm_tool.py` functions

### Fixed

- Fixed `test_llm_tool.py`: wrong attribute `tool_call.tool_name` to `tool_call.function.name`
- Fixed `test_llm_tool.py`: missing `await` on `call_tool()` async function
- Fixed `test_llm_tool.py`: duplicate assistant message appended to memory
- Fixed `test_llm_tool.py`: agent loop now handles multiple tool calls and multi-round tool calling
- Fixed `test_llm_tool.py`: assistant message with `tool_calls` preserved (not stripped to plain content)
- Updated stale `llm.py` description in `llms.txt` (was "system instructions", now "async OpenAI client wrapper")
- Updated stale `litellm` dependency to `openai` in `llms.txt`
- Added missing `models.py`, `test_llm.py`, `test_llm_tool.py` to project structure in `README.md` and `llms.txt`
- Fixed Python version `3.14.2` to `3.14.3` in `SETUP.md`
- Aligned `gh` CLI version prerequisite in `RELEASE.md` to match `SETUP.md`

## Release steps

- [x] 1. Run `poetry run mypy src/` — fix any issues
- [x] 2. Run `poetry run isort src/ tests/` — fix any issues
- [x] 3. Run `poetry run black src/ tests/` — fix any issues
- [x] 4. Run `poetry run pytest` — fix any issues
- [x] 5. Run `export SOURCE_DATE_EPOCH=$(date +%s); poetry build -v` — fix any issues
- [x] 6. Ensure `CHANGELOG.md` exists and update with release changes
- [ ] 7. Commit all changes to main, create tag `v0.0.10`, push, and create GitHub release

## Status

- [ ] Release complete
