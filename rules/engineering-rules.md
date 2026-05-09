# Engineering Rules

Vendor-neutral engineering standards. These apply to all code in any project that adopts SpecForge - language- and framework-agnostic by design.

## 1. Specs first, code second

Do not write production code without a written spec. The minimum bar is:

- A PRD (full or lightweight) with `Status: Approved`.
- A spec triplet (`requirements.md` + `design.md` + `tasks.md`) or a single-file feature spec.
- Stable requirement IDs that tasks back-reference.

If the work is a refactor with no behavior change, use [`specs/templates/technical-spec-template.md`](../specs/templates/technical-spec-template.md). If the work is one architectural decision, use an [ADR](../specs/templates/architecture-decision-record.md).

"I'll figure it out as I go" produces unreviewable change sets.

## 2. Match scope to the request

A bug fix doesn't need a refactor. A refactor doesn't need new features. A one-shot script doesn't need a helper module. Three similar lines beat a premature abstraction.

When in doubt, ship the smaller change.

## 3. No dead code

- Don't add error handling for scenarios that can't happen.
- Don't add fallbacks for inputs that are validated upstream.
- Don't keep deprecated paths "just in case" - delete them and rely on git history.
- Don't write comments that restate the code.

## 4. Comments explain *why*, not *what*

Default to writing no comments. Only add one when the WHY is non-obvious: a hidden constraint, a subtle invariant, a workaround for a specific bug. If removing the comment wouldn't confuse a future reader, don't write it.

Don't reference the current task or PR in code comments - those belong in commit messages and PR descriptions and rot as the codebase evolves.

## 5. Readability over cleverness

- Descriptive names beat single letters everywhere except short loops.
- Functions that do one thing beat functions that do five.
- Modules with one cohesive responsibility beat utility-belt modules.
- An obvious abstraction beats a clever one.

## 6. Validate at boundaries

Validate at system boundaries (user input, external APIs, file parsers). Don't re-validate values that are already typed and validated within your own code. Trust internal contracts.

## 7. Deterministic over flexible

Code that does one thing predictably beats code that does many things based on flags. Feature flags exist for rollout, not for permanent multi-mode behavior.

If a function has more than 3 parameters, consider whether it should be split. If it has a `mode` argument, it probably should be split.

## 8. Errors are first-class

- Every error path is documented.
- Every error returned to a user has a structured shape.
- Don't swallow exceptions silently - log, propagate, or fail loudly.
- Don't use exceptions for control flow.

## 9. Performance budgets are non-negotiable

If your spec defines an NFR like "p95 latency < 200ms" or "initial JS bundle < 200KB," those are gates, not aspirations. Performance regressions block merge - they don't get logged as follow-ups.

## 10. Observability ships with the feature

Metrics, logs, traces are part of the feature, not added later. The PR that adds new functionality includes the observability for that functionality. "We'll add metrics next sprint" is a recipe for blind production.

## 11. No half-implementations

A feature that's 80% done and shipped behind a flag is a maintenance liability. Either ship the full feature behind a flag (with a documented ramp), or don't ship.

## 12. Backwards compatibility is opt-in, not default

Don't add backwards-compat shims, deprecated aliases, or `// kept for compatibility` comments unless an actual external consumer requires them. Internal code can be refactored freely; there's git history.

## 13. The diff is the deliverable

Every PR is reviewable on its own. If a reviewer needs to read three other PRs to understand this one, the change is too coupled - break it up.

PR description includes:

- The task ID being implemented.
- A one-paragraph description of what changed and why.
- Anything reviewers need to verify manually.

## 14. Tests over implementation

When a test catches the bug a unit was supposed to prevent, the test wins. When a test breaks during refactor without behavior change, the test is wrong (or the refactor changed behavior - investigate).

Mocks at external boundaries only. Don't mock the system under test.

## See also

- [`code-review-rules.md`](code-review-rules.md) - review-specific standards
- [`security-rules.md`](security-rules.md) - security-specific standards
- [`documentation-rules.md`](documentation-rules.md) - doc-specific standards
- The per-vendor rule files (`{codex,claude,gemini,cursor,windsurf}-rules.md`) for vendor-specific format conventions
