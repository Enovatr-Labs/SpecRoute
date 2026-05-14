# CLAUDE.md

Claude Code shim for this repository. Read [`AGENTS.md`](AGENTS.md) first; it is the canonical vendor-neutral source of truth for SpecRoute.

## Claude-Specific Context

- `.claude/` is this repo's implementation-team runtime, not the consumer template. Consumer-facing files live in [`runtimes/.claude/`](runtimes/.claude/).
- Agents live in `.claude/agents/`; see [`.claude/agents/README.md`](.claude/agents/README.md) for the roster of 11 specialists.
- Skills live in `.claude/skills/`: `scaffold-artifact`, `add-vendor`, `example-walkthrough`, `frontmatter-lint`.
- Commands live in `.claude/commands/`: `/sanitize`, `/status`, `/audit`, `/parity`.
- Hooks live in `.claude/hooks/`: SessionStart status banner, PreToolUse sanitization gate, PostToolUse frontmatter check.
- Per-agent persistent context lives in `.claude/agent-memory/<agent-name>/`.

## Frontmatter Contracts

| Artifact | Required fields |
|---|---|
| Agent (`.claude/agents/<name>.md`) | `name`, `description` (with trigger phrases), `model` (`opus` \| `sonnet` \| `haiku`), `color` |
| Skill (`.claude/skills/<slug>/SKILL.md`) | `name`, `description`, `argument-hint`, `user-invocable`, `allowed-tools` |
| Command (`.claude/commands/<name>.md`) | `description` |

Missing required fields = the runtime won't register the artifact. The PostToolUse hook surfaces violations on stderr at write time.

## Sanitization Gate

`.claude/hooks/pre-bash-sanitize.sh` blocks `git commit`, `git push`, `gh pr create`, and `gh release create` if `git grep` finds any term from `.claude/.forbidden-strings.txt` in tracked files. Treat a hook block as a hard stop - generalize the source content; do not bypass.

## Per-User vs Tracked Settings

- `.claude/settings.json` - tracked, project-wide.
- `.claude/settings.local.json` - **gitignored**, per-user overrides (permissions, MCP enables).
- `.claude/.forbidden-strings.txt` - **gitignored**, per-installation sanitization wordlist.

## Before Publishing

Run `/audit` for the comprehensive sweep (sanitization + frontmatter + vendor matrix consistency + broken-link check) or `/sanitize` for a quick string-level scan. For a deeper logic-level review, invoke the `sanitization-auditor` agent.
