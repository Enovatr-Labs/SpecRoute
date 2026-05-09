# CLAUDE.md - User Search Sample Project

Claude Code shim. Read [`AGENTS.md`](AGENTS.md) first; it is the canonical, vendor-neutral source of truth for this project.

## Claude-Specific Context

- This project's `.claude/` is the **consumer runtime** (not the SpecForge framework's implementation team). It carries 8 implementation-team agents specific to user-search.
- Agents: `prd-author`, `backend-engineer`, `frontend-engineer`, `database-engineer`, `security-auditor`, `unit-test-writer`, `integration-test-generator`, `deployment-validator`. See [`.claude/agents/README.md`](.claude/agents/README.md).
- Commands: `/sanitize`, `/audit`, `/status`, `/parity`.
- Hooks: SessionStart status, PreToolUse sanitization gate, PostToolUse frontmatter check.
- Per-agent memory: [`.claude/agent-memory/`](.claude/agent-memory/) - sparsely populated by default; agents accumulate state as the project progresses.

## Frontmatter Contracts

| Artifact | Required fields |
|---|---|
| Agent (`.claude/agents/<name>.md`) | `name`, `description` (with trigger phrases), `model` (`opus` \| `sonnet` \| `haiku`), `color` |
| Skill (`.claude/skills/<slug>/SKILL.md`) | `name`, `description`, `argument-hint`, `user-invocable`, `allowed-tools` |
| Command (`.claude/commands/<name>.md`) | `description` |

The PostToolUse hook surfaces missing fields on stderr at write time.

## Sanitization Gate

`.claude/hooks/pre-bash-sanitize.sh` blocks `git commit`, `git push`, `gh pr create`, and `gh release create` if `git grep` finds any term from `.claude/.forbidden-strings.txt` in tracked files. Treat hook blocks as hard stops - generalize the source content; do not bypass.

## Per-User vs Tracked Settings

- `.claude/settings.json` - tracked, project-wide.
- `.claude/settings.local.json` - **gitignored** after rename from `.template.json`, per-user overrides.
- `.claude/.forbidden-strings.txt` - **gitignored** after rename from `.template.txt`, per-installation sanitization wordlist.

## Before Publishing

Run `/audit` (comprehensive sweep) or `/sanitize` (string scan). For deeper review, see [`agentic-docs/automation-decision-framework.md`](agentic-docs/automation-decision-framework.md) and the framework's [`workflows/release-readiness.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/workflows/release-readiness.md).

## Deep references

For project-level conceptual content (philosophy, spec-driven flow, doc structure, agent-memory pattern), read [`agentic-docs/`](agentic-docs/). Each file is project-specific; for the broader framework theory, links lead to upstream SpecForge.
