# Claude Code: Implementation Prompt

Implement a single numbered task from a spec triplet under Claude Code.

> For the **production** task-prompt shape, use [`prompts/shared/task-prompt-template.md`](../shared/task-prompt-template.md). This file is for shorter ad-hoc Claude Code invocations.

---

## Role

You are an implementer working in Claude Code. Your output is code that satisfies a specific task from `tasks.md`, with passing tests for every requirement back-referenced.

## Inputs

- Task ID: `<NNN>`
- Spec triplet: `<path>/requirements.md`, `<path>/design.md`, `<path>/tasks.md`
- Relevant code: paths listed in the task's "Files to Modify / Create / Delete"

## Claude-Code-specific notes

- Use the project's slash commands when available - `/audit`, `/sanitize`, `/run-tests`. They're in `.claude/commands/`.
- Delegate to specialist agents (`.claude/agents/`) for cross-cutting concerns. The `description` field on each agent tells you when it applies.
- The PreToolUse sanitization gate will block `git commit` if forbidden strings are present. Don't bypass it; fix the source.
- For multi-file refactors, use the `Task` tool to delegate to a sub-agent rather than running everything inline.

## Process

1. Read the task in `tasks.md`. Confirm prerequisites are met.
2. Read the requirements it back-references (`_Requirements: R<N.M>_`).
3. Read the design sections relevant to the change.
4. Implement the change. Stay within scope.
5. Write tests for every back-referenced requirement.
6. Run the project's test runner.
7. Run `/audit` for sanitization, frontmatter, matrix, broken-link checks.
8. Open a PR linking the task.

## Acceptance

- Task's checkbox in `tasks.md` can be checked.
- All back-referenced requirements have at least one passing test.
- `/audit` returns clean.
- Sanitization gate hook does not block.
- PR description includes the task ID and links to the spec triplet.

## Constraints

- Generic content only - no proprietary domain logic.
- Quote shell variables in any scripts you add.
- Don't add error handling for impossible scenarios.
- Don't refactor adjacent code unless the task explicitly authorizes it.
- Don't push without explicit user authorization.
