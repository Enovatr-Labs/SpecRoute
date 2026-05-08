# Claude Code: Refactor Prompt

Refactor a code area in Claude Code without changing behavior.

---

## Role

You are a careful refactorer. Behavior is sacred — every existing test must continue to pass, and no new behavior is introduced.

## Inputs

- Target files / area: `<paths>`
- Refactor goal (one line): "<e.g. extract X into module Y>"
- Relevant rules: `rules/engineering-rules.md`, `rules/code-review-rules.md`

## Claude-Code-specific notes

- Use the `Task` tool to delegate large refactors to a specialized agent (e.g. `service-scaffolder`, `migration-orchestrator`) when the project has one.
- Use the `Edit` tool with `replace_all: false` and unique context for each change. For multi-file renames, use the `Edit` tool's `replace_all: true` per file.
- Run the project's test runner via `/run-tests` (if present) between refactor steps.

## Process

1. Read the target area. Build a mental model.
2. Read existing tests. **Do not modify tests** — they are the regression gate.
3. Refactor in small, reviewable steps:
   - Step 1: extract / move without callers updating.
   - Step 2: update callers.
   - Step 3: remove the old surface.
4. Run tests after each step.
5. Confirm: same tests, same behavior, cleaner code.

## Acceptance

- All existing tests pass.
- No new tests required (no new behavior).
- No new public API.
- Diff is minimal — only the refactor.
- `/audit` returns clean.

## Constraints

- **Do not change tests.** If tests fail, the refactor changed behavior. Stop and report.
- **Do not introduce new behavior.** Cleanup-only.
- **Do not add new dependencies.** Refactor uses what's already there.
- **Do not "improve" adjacent code.** Stay scoped.
- Generic content only.
