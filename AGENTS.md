# AGENTS.md

Guidance for AI coding agents working on `iOS-Automation-Framework`.

This repository is the companion test-code project for MeteorTest. It owns pytest API suites, Appium/XCUITest UI suites, Allure output, and the `meteortest.yml` integration contract used by the platform.

## Working Rules

- Keep changes scoped to the requested test, framework, documentation, or integration behavior.
- Do not commit private credentials, internal URLs, local device identifiers, tokens, or test accounts.
- Do not push directly to `main`; use a `dev/v-peq/<topic>` branch and open a PR against the mother repository.
- Prefer deterministic local validation before claiming behavior in public docs.

## Synchronization Rule

When backend behavior, test behavior, interaction flow, environment variables, ports, commands, integration contracts, mock services, or capability/status claims change, update all affected surfaces in the same change:

- implementation code
- tests
- `meteortest.yml` when platform commands or suite behavior change
- English README
- Chinese README
- related project documentation

Do not treat a code-only or documentation-only update as complete if another surface still describes or implements the old behavior.

## Terminology

- English technical docs may use `contract` for `meteortest.yml` and integration boundaries.
- Chinese public docs should prefer `协议` instead of `契约`.

## Validation

Use the project virtual environment when available:

```powershell
.venv\Scripts\python.exe -m pytest tests -q -n 0
.venv\Scripts\python.exe -m pytest API_Automation\cases -v -n 0 -m smoke
.venv\Scripts\python.exe -m compileall API_Automation UI_Automation tools tests
```

For API smoke tests, set `API_BASE_URL` explicitly. The local mock API default is:

```powershell
.venv\Scripts\python.exe -m tools.mock_api.server --host 127.0.0.1 --port 8010
$env:API_BASE_URL="http://127.0.0.1:8010"
```
