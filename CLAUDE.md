# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

SpecForge is an open-source framework for spec-driven agentic software engineering — a collection of PRDs, specs, prompts, agents, skills, workflows, and engineering rules intended to be reused by both Codex and Claude Code. It is **markdown content, not an application**. There is no package manager, no build step, no test suite, and no lint config. Do not look for `package.json` or try to run tests; treat this as a documentation/templates repository.

## Current state

The repo is a skeleton. At the moment it contains only `README.md`, `LICENSE`, this file, and a local-only `initial.md` bootstrap spec (gitignored). **`initial.md` is not part of the published repo** — it's a local construction reference that describes the target directory structure and content the repo should grow into. If present, read it before adding new top-level structure, and keep new work consistent with it.

The intended structure (from `initial.md`):

```
prds/         specs/        agents/       skills/
prompts/      workflows/    rules/        examples/    docs/
```

Examples under `examples/<feature>/` should follow the spec-driven flow and include: `prd.md`, `spec.md`, `agent-roster.md`, `prompts.md`, `implementation-plan.md`.

## Hard constraints

These are repo-specific rules that aren't obvious from the code and must be respected:

1. **Vendor neutrality.** Codex and Claude Code are both first-class execution environments. Prompts live in three parallel trees: `prompts/codex/`, `prompts/claude/`, and `prompts/shared/`. Do not fold one into the other or treat Claude as the default.

2. **Sanitization.** Patterns in this repo are generalized from internal codebases. Never commit proprietary business logic, domain models, customer data, private endpoints, credentials, or internal product details. Generalize before adding.

3. **Spec-driven order.** The canonical flow is PRD → Spec → Tasks → Implementation → Validation → Review. New examples and workflows should reflect that order rather than jumping straight to code.

4. **TODO markers are intentional.** `initial.md` calls for `TODO` markers where real examples will be added later. Don't silently fill them in with invented content; either leave them or flag clearly that the example is illustrative.

5. **Templates over theory.** Templates should be practical and immediately usable, not abstract checklists.

## Working in this repo

- Edits are almost always to markdown files. Use `Edit`/`Write` directly; there is nothing to compile or run.
- When adding a new artifact (PRD, spec, agent, skill, prompt, workflow, rule), check `initial.md` for the intended location and the sibling files for the established shape before creating a new pattern.
- If a directory in the intended structure doesn't exist yet, it's fine to create it as part of the work — but include the `README.md` for that directory at the same time.

## SpecForge implementation runtime

This repo's own `.claude/` directory is wired up as the SpecForge implementation team. It does **not** contain consumer-facing templates (those live in `agents/`, `skills/`, `commands/`, `hooks/`).

| Path | What's there |
|---|---|
| `.claude/agents/` | 11 implementation agents (`prd-author`, `spec-author`, `agent-roster-architect`, `skill-author`, `prompt-engineer`, `command-author`, `hooks-author`, `runtime-architect`, `framework-docs-author`, `sanitization-auditor`, `template-quality-reviewer`) — see `.claude/agents/README.md` for the roster |
| `.claude/skills/` | 4 contributor skills: `scaffold-artifact`, `add-vendor`, `example-walkthrough`, `frontmatter-lint` |
| `.claude/commands/` | 4 slash commands: `/sanitize`, `/status`, `/audit`, `/parity` |
| `.claude/hooks/` | `hooks.json` + 3 scripts: SessionStart status banner, PreToolUse sanitization gate on `git commit`/`git push`, PostToolUse frontmatter check on agent/skill/command edits |
| `.claude/agent-memory/` | Per-agent persistent context (currently for `sanitization-auditor`, `runtime-architect`, `framework-docs-author`) |

**Before any commit or PR**: run `/sanitize` (string-level scan) or `/audit` (comprehensive). The PreToolUse hook will block `git commit` / `git push` if forbidden strings are found in tracked files.

**When adding a new top-level artifact**, prefer invoking the corresponding agent over freestyling — they own the contracts.
