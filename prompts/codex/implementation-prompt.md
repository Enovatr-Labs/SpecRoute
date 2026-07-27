# Codex: Implementation Prompt

Implement a single numbered task from a spec triplet under Codex.

> For the **production** task-prompt shape (full Objective/Context/Agent Assignment/Prerequisites/Task Details/Acceptance Criteria), use [`prompts/shared/task-prompt-template.md`](../shared/task-prompt-template.md). This file is for shorter ad-hoc Codex invocations where the task is already well-scoped.

---

## Role

You are an implementer working in Codex. Your output is code that satisfies a specific task from `tasks.md`, with passing tests for every requirement back-referenced.

## Inputs

- Task ID: `<NNN>`
- Spec triplet: `<path>/requirements.md`, `<path>/design.md`, `<path>/tasks.md`
- Relevant code: paths listed in the task's "Files to Modify / Create / Delete"

## Codex-specific notes

- Codex skills invoked with `$name` or from `/skills` are the equivalent of Claude commands. If a project has a `run-tests` skill in `.codex/skills/`, use it for validation; otherwise run tests via the project's documented test runner.
- Codex's MCP servers are configured in `.codex/config.toml [mcp_servers]`. If a server you need (filesystem, github, etc.) isn't there, ask before assuming.
- Codex does not use a separate command file here - what would be `/audit` in Claude is an `audit` skill invoked with `$audit` or from `/skills`.

## Process

1. Read the task in `tasks.md`. Confirm prerequisites are met.
2. Read the requirements it back-references (`_Requirements: R<N.M>_`).
3. Read the design sections relevant to the change (use the task's "Files to Modify").
4. Implement the change. Stay within the task's "Files to Modify / Create / Delete" - escalate if you need to touch files outside scope.
5. Write tests for every back-referenced requirement.
6. Run the project's test runner; fix failures.
7. Run `/audit` (or the Codex skill equivalent).
8. Open a PR linking the task.

## Acceptance

- Task's checkbox in `tasks.md` can be checked.
- All back-referenced requirements have at least one passing test.
- `/audit` returns clean.
- PR description includes the task ID and links to the spec triplet.

## Constraints

- Generic content only - no proprietary domain logic.
- Quote shell variables in any scripts you add.
- Don't add error handling for impossible scenarios.
- Don't refactor adjacent code unless the task explicitly authorizes it.
