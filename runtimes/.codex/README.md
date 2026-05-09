# `.codex/` - Codex runtime layout

Drop this directory into the root of your project. Codex reads from these paths automatically.

## Layout

```
.codex/
├── config.toml                      MCP servers + approval policy
├── agents/<name>.md                 flat-file agents (same shape as Claude)
├── skills/<slug>/SKILL.md           folder-per-skill (same shape as Claude)
└── scripts/                         project-internal scripts
```

## Setup

1. Copy `config.template.toml` → `.codex/config.toml`. Adjust `approval_policy` and `sandbox_mode` for your team's risk posture.

2. **MCP servers** - `config.toml` carries the MCP server inventory under `[mcp_servers.<name>]` blocks. Maintain `runtimes/mcp/servers.yaml` as the canonical source and run `runtimes/mcp/render/render_codex.py` to regenerate.

3. **Agents** - copy from `runtimes/.codex/agents/` (or mirror from `.claude/agents/`). Same frontmatter contract.

4. **Skills** - copy from `runtimes/.codex/skills/` (or mirror from `.claude/skills/`). Folder-per-skill with `SKILL.md`.

5. **Cross-vendor sync** - run `tools/sync-skills.py --dry-run` to verify Claude / Codex parity.

## What's tracked vs gitignored

| Path | Tracked? |
|---|---|
| `.codex/config.toml` | Yes (sans secrets) |
| `.codex/agents/*.md` | Yes |
| `.codex/skills/<slug>/SKILL.md` | Yes |
| `.codex/scripts/*` | Yes |

Secrets (e.g. `GITHUB_PERSONAL_ACCESS_TOKEN`) belong in environment variables or a gitignored `.env`, never inline in `config.toml`.

## Mirroring with Claude Code

Codex shares two file shapes with Claude Code: agents (`<name>.md`) and skills (`<slug>/SKILL.md`). The third (commands) lives in two different places:

| Concept | Claude path | Codex path |
|---|---|---|
| Agent | `.claude/agents/<name>.md` | `.codex/agents/<name>.md` (identical) |
| Skill | `.claude/skills/<slug>/SKILL.md` | `.codex/skills/<slug>/SKILL.md` (identical) |
| Slash command | `.claude/commands/<name>.md` | `.codex/skills/<slug>/SKILL.md` with `user-invocable: true` |
| Hook | `.claude/hooks/hooks.json` + scripts | (no first-class equivalent in Codex) |

To keep Claude and Codex in sync: `tools/sync-skills.py`.
