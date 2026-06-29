# `.codex/` - Codex runtime layout

Drop this directory into the root of your project. Codex reads from these paths automatically.

## Layout

```
.codex/
├── config.toml                      MCP servers + approval policy
├── agents/<name>.toml               standalone TOML subagents (NOT Claude's Markdown shape)
├── skills/<slug>/SKILL.md           folder-per-skill (same shape as Claude)
├── hooks.json                       lifecycle hooks (10 events; enabled by default)
└── scripts/                         project-internal scripts
```

## Setup

1. Copy `config.template.toml` → `.codex/config.toml`. Adjust `approval_policy` and `sandbox_mode` for your team's risk posture.

2. **MCP servers** - `config.toml` carries the MCP server inventory under `[mcp_servers.<name>]` blocks. Maintain `runtimes/mcp/servers.yaml` as the canonical source and run `runtimes/mcp/render/render_codex.py` to regenerate.

3. **Agents** - author standalone TOML files under `.codex/agents/<name>.toml` with required fields `name`, `description`, `developer_instructions` (see [`agents/spec-reviewer.toml`](agents/spec-reviewer.toml)). This is a **different shape** from Claude's flat Markdown agents, so agents do not cross-mirror automatically.

4. **Skills** - copy from `runtimes/.codex/skills/` (or mirror from `.claude/skills/`). Folder-per-skill with `SKILL.md` - identical to Claude.

5. **Hooks** - hooks are enabled by default (the `hooks` feature; `codex_hooks` is a deprecated alias). Copy [`hooks/codex/hooks.template.json`](../../hooks/codex/hooks.template.json) to `.codex/hooks.json`, or merge the inline `[hooks]` table into `config.toml`. 10 lifecycle events; Claude-compatible JSON schema.

6. **Cross-vendor sync** - run `tools/sync-skills.py --dry-run` to verify Claude / Codex **skill** parity. Agents are excluded (formats differ).

## What's tracked vs gitignored

| Path | Tracked? |
|---|---|
| `.codex/config.toml` | Yes (sans secrets) |
| `.codex/agents/*.toml` | Yes |
| `.codex/skills/<slug>/SKILL.md` | Yes |
| `.codex/hooks.json` | Yes |
| `.codex/scripts/*` | Yes |

Secrets (e.g. `GITHUB_PERSONAL_ACCESS_TOKEN`) belong in environment variables or a gitignored `.env`, never inline in `config.toml`.

## Mirroring with Claude Code

Codex shares **one** file shape with Claude Code outright - skills (`<slug>/SKILL.md`). Agents, commands, and hooks each map differently:

| Concept | Claude path | Codex path |
|---|---|---|
| Agent | `.claude/agents/<name>.md` (Markdown + frontmatter) | `.codex/agents/<name>.toml` (TOML: `name`, `description`, `developer_instructions`) - **format differs** |
| Skill | `.claude/skills/<slug>/SKILL.md` | `.codex/skills/<slug>/SKILL.md` (identical) |
| Slash command | `.claude/commands/<name>.md` | a skill invoked via `/skills` or `$mention` |
| Hook | `.claude/hooks/hooks.json` + scripts | `.codex/hooks.json` or `[hooks]` in `config.toml` (Claude-compatible JSON; 10 events; default-on) |

To keep Claude and Codex **skills** in sync: `tools/sync-skills.py`. Agents are not synced - the TOML/Markdown formats diverge.
