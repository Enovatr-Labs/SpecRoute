# `.gemini/` - Gemini CLI runtime layout

Drop this directory into the root of your project. Gemini reads from these paths. Current Gemini CLI builds back the full SpecRoute capability matrix: skills, subagents, commands, hooks, and MCP servers.

## Layout

```
.gemini/
├── settings.json                MCP servers (mcpServers) + hooks block
├── skills/
│   └── <slug>/SKILL.md          Agent Skills open standard (enabled by default)
├── agents/
│   └── <name>.md                subagents (Markdown + YAML frontmatter)
└── commands/
    └── <name>.toml              custom commands (prompt + optional description)
```

## Setup

1. Copy the settings template:

   ```bash
   cp runtimes/.gemini/settings.template.json .gemini/settings.json
   ```

2. **MCP servers** - `settings.json`'s `mcpServers` map mirrors the canonical `runtimes/mcp/servers.yaml`. Run `runtimes/mcp/render/render_gemini.py` to regenerate it.

3. **Hooks** - merge the `hooks` block from `hooks/gemini/hooks-settings.template.json` into `settings.json`. It covers the 11 Gemini lifecycle events (SessionStart, BeforeTool, AfterTool, ...). See that template and `hooks/gemini/scripts/` for the contract.

4. **Skills** - copy `runtimes/.gemini/skills/` to `.gemini/skills/`. One folder per skill with a `SKILL.md`; see [`skills/README.md`](skills/README.md) for the frontmatter contract.

5. **Subagents** - copy `runtimes/.gemini/agents/` to `.gemini/agents/`. One Markdown file per subagent; see [`agents/README.md`](agents/README.md).

6. **Commands** - copy `runtimes/.gemini/commands/` to `.gemini/commands/`. One TOML file per command; subdirectories namespace as `/parent:child`. See [`commands/README.md`](commands/README.md).

## Capability matrix

| Concept | Available in Gemini? | Where |
|---|---|---|
| Skills | Yes | `.gemini/skills/<slug>/SKILL.md` |
| Subagents | Yes | `.gemini/agents/<name>.md` |
| Slash commands | Yes | `.gemini/commands/<name>.toml` (TOML, not the old JSON map) |
| Hooks | Yes | `settings.json` `hooks` block (11 events) |
| MCP servers | Yes | `settings.json` `mcpServers` |
| Engineering rules | Indirect | root `GEMINI.md` and rules referenced from there |
| Prompts | Yes | `prompts/` works in any agent CLI that reads markdown |

## Root context file

Gemini reads `GEMINI.md` at repo root. It should be a short delegation shim pointing to `AGENTS.md`. See [`../../GEMINI.md`](../../GEMINI.md) for an example.

## What's tracked vs gitignored

| Path | Tracked? |
|---|---|
| `.gemini/settings.json` | Yes (sans secrets) |
| `.gemini/skills/`, `.gemini/agents/`, `.gemini/commands/` | Yes |

Secrets and personal preferences belong in environment variables or `.env` (gitignored).

## Transition note

Google began superseding the standalone Gemini CLI with the Antigravity CLI on 2026-06-18 for free and Google One tiers; paid tiers retain Gemini CLI access. The `.gemini/` layout described here remains valid for current installs, and the skills/agents/commands artifacts are portable to whatever runtime ships next.
