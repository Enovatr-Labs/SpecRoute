---
inclusion: manual
---

# Pre-commit coverage check

When invoked manually, inspect `git diff --cached --name-only`. For each source
file under `src/`, verify that a corresponding test exists under `tests/` or
alongside the source using the project's test naming convention.

Report missing coverage as a punch list. Do not edit files or block a commit
unless the user explicitly asks for enforcement.
