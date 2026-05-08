# Codex: Refactor Prompt

Refactor a code area in Codex without changing behavior. Use this for cleanup, consolidation, or modernization that has no functional impact.

---

## Role

You are a careful refactorer. Behavior is sacred — every existing test must continue to pass, and no new behavior is introduced.

## Inputs

- Target files / area: `<paths>`
- Refactor goal (one line): "<e.g. extract X into module Y>"
- Relevant rules: `rules/engineering-rules.md`, `rules/code-review-rules.md`

## Codex-specific notes

- Codex has aggressive refactor capabilities; use the workspace-write sandbox when available.
- For multi-file refactors that touch boundaries, use a Codex skill if your project provides one (e.g. `migration-orchestrator`); otherwise invoke step-by-step.

## Process

1. Read the target area. Build a mental model of the current state.
2. Read existing tests covering the area. **Do not modify tests** — they are the regression gate.
3. Make the refactor in small, reviewable steps:
   - Step 1: extract / move without callers updating.
   - Step 2: update callers.
   - Step 3: remove the old surface.
4. Run tests after each step. If any test fails, the refactor changed behavior — fix or back out.
5. Confirm: same tests, same behavior, cleaner code.

## Acceptance

- All existing tests pass.
- No new tests required (no new behavior).
- No new public API.
- Diff is minimal — only the refactor is in the change set.
- `/audit` (or Codex skill equivalent) returns clean.

## Constraints

- **Do not change tests.** If tests fail, the refactor changed behavior. Stop and report.
- **Do not introduce new behavior.** Cleanup-only.
- **Do not add new dependencies.** Refactor uses what's already there.
- **Do not "improve" adjacent code.** Stay scoped.
- Generic content only — no proprietary domain logic introduced.

## Anti-patterns to avoid

- Mixing refactor with feature work in one PR.
- Renaming public APIs without a deprecation window.
- "While I'm here" cleanups that bloat the diff.
- Changes that break a downstream consumer for a hypothetical future benefit.
