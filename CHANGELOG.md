# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.2] - 2026-02-21

### Added

- FastAPI web application with root endpoint serving HTML UI
- POST `/prompt/` endpoint accepting math questions via JSON
- MathQuestion Pydantic model for request validation
- Static file serving for frontend assets
- Bootstrap-based dark theme frontend with question/response form
- Comprehensive test suite (14 tests) covering endpoints, validation, and model

## [0.0.1] - 2026-02-20

### Added

- Initial project scaffolding with Poetry build system
- Project structure with `src/math_ai_agent` package layout
- Development tooling: pytest, mypy, black, isort, pylint, coverage
- GitHub connectivity test script (`scripts/test_github.sh`)
- CHANGELOG, LICENSE, README, and SETUP documentation

