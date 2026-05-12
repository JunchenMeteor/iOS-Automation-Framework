# AGENTS.md

Guidance for AI coding agents working on `iOS-Automation-Framework`.

This repository is the companion test-code project for MeteorTest. It owns pytest API suites, Appium/XCUITest UI suites, Allure output, and the `meteortest.yml` integration contract used by the platform.

## Working Rules

- Keep changes scoped to the requested test, framework, documentation, or integration behavior.
- Do not commit private credentials, internal URLs, local device identifiers, tokens, or test accounts.
- Do not push directly to `main`; use a `dev/v-peq/<topic>` branch and open a PR against the mother repository.
- Prefer deterministic local validation before claiming behavior in public docs.

## GitHub Workflow Rules

Before creating a new work branch, sync the latest `main` first.

Branch names should use:

```text
dev/v-peq/<lowerCamelOrSnakeName>
```

When direct pushes to `main` are not allowed:

- Create a feature branch.
- Push the branch to the fork or writable remote.
- Create the issue and pull request in the upstream repository.
- Do not push directly to upstream `main`.

Issue and PR titles should start with one of the repository type prefixes below. Use the closest existing type instead of inventing a new prefix:

- `[Feature]` for new features, improvements, refactors, maintenance, and platform capability changes.
- `[Bug]` for defects and regressions.
- `[Test]` for test coverage, validation, fixtures, and CI test behavior.
- `[Documentation]` for README, architecture notes, setup guides, and agent instructions.
- `[Security]` for dependency or security hardening changes.
- `[Smoke test]` for smoke-test work.
- `[Known Issues]` for known issue tracking.

Use the same prefix family for the tracking issue and its PR when they describe the same work. If a change spans multiple areas, choose the dominant user-visible intent.

Add GitHub labels to issues according to the selected prefix when the authenticated account has permission:

- `[Feature]` issues must use `enhancement`.
- `[Bug]` issues must use `bug`.
- `[Test]` and `[Smoke test]` issues must use `test`.
- `[Documentation]` issues must use `documentation`.
- `[Security]` issues must use `security`.
- `[Known Issues]` issues must use `known issue`.

If label permission is missing, state that limitation in the handoff instead of silently claiming the rule was fully applied.

Issue and PR descriptions should use English. Use simple section headings such as `## Summary`, `## Proposed Changes`, and `## Test Plan`.

When an issue tracks the PR work, link it from the PR body with:

```text
Closes #<issue-number>
```

Place the `Closes #<issue-number>` line at the end of the PR description, after the test plan or validation section.

Do not add `Related PR: #<number>` to the issue body.

Use fresh GitHub data when checking issue or PR state. Prefer `gh api --cache 0s` or direct `gh api` calls before deciding whether an issue or PR already exists.

Do not add `Co-Authored-By` or AI attribution to commit messages.

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
