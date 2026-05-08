# CLAUDE.md

This file provides Claude Code-specific guidance for working in this repository.

## Source of truth

For repository overview, artifact taxonomy, vendor matrix, hard constraints, and the spec-driven flow: read [`AGENTS.md`](AGENTS.md). It is the canonical, vendor-neutral context file. This file holds only Claude-Code-specific overrides.

## Claude-Code-specific notes

### `.claude/` runtime is the SpecForge implementation team

The `.claude/` directory in this repo is wired up to build SpecForge itself. It is **not** the consumer-facing template (those live under `runtimes/.claude/`). Roster:

- **Agents** (`.claude/agents/`) — 11 specialists; see `.claude/agents/README.md`. Invoke them by name when adding artifacts (`prd-author`, `spec-author`, `agent-roster-architect`, `skill-author`, `prompt-engineer`, `command-author`, `hooks-author`, `runtime-architect`, `framework-docs-author`, `sanitization-auditor`, `template-quality-reviewer`).
- **Skills** (`.claude/skills/`) — `scaffold-artifact`, `add-vendor`, `example-walkthrough`, `frontmatter-lint`.
- **Commands** (`.claude/commands/`) — `/sanitize`, `/status`, `/audit`, `/parity`.
- **Hooks** (`.claude/hooks/`) — SessionStart status banner, PreToolUse sanitization gate on `git commit`/`git push`, PostToolUse frontmatter validation on agent/skill/command writes.

### Sanitization gate is active

`.claude/hooks/pre-bash-sanitize.sh` blocks `git commit`, `git push`, `gh pr create`, and `gh release create` if `git grep` finds any term from `.claude/.forbidden-strings.txt` (gitignored, per-installation) in tracked files. Treat a hook block as a hard stop — fix the source, don't bypass.

### Frontmatter contracts (Claude-Code-specific)

Claude Code reads:

- **Agents**: `name`, `description`, `model` (`opus` | `sonnet` | `haiku`), `color`. The `description` must include trigger phrases or the agent won't be auto-selected.
- **Skills** (folder-per-skill, file is `SKILL.md`): `name`, `description`, `argument-hint`, `user-invocable`, `allowed-tools`.
- **Commands** (`.claude/commands/<name>.md`): `description`. Body is the prompt the slash command expands to.

The PostToolUse hook validates these on every Write/Edit and surfaces missing fields on stderr.

### Per-user vs tracked settings

- `.claude/settings.json` — tracked, project-wide settings.
- `.claude/settings.local.json` — gitignored, per-user overrides.
- `.claude/.forbidden-strings.txt` — gitignored, per-installation sanitization wordlist.

## Before any commit or PR

Run `/sanitize` (string-level scan) or `/audit` (comprehensive). The PreToolUse hook will block publish-style git operations if forbidden strings are found, but catch issues earlier — don't rely on the gate.

## Working in this repo

Read [`AGENTS.md`](AGENTS.md). Then read this file for the Claude-specific bits. That's it.
