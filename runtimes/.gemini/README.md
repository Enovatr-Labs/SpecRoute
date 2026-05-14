# `.gemini/` - Gemini CLI runtime layout

Drop this directory into the root of your project. Gemini reads from these paths.

## Layout

```
.gemini/
├── settings.json                    MCP server config
└── gemini_cli_config.json           command map (shell shortcuts)
```

## Setup

1. Copy templates:

   ```bash
   cp runtimes/.gemini/settings.template.json .gemini/settings.json
   cp runtimes/.gemini/gemini_cli_config.template.json .gemini/gemini_cli_config.json
   ```

2. **MCP servers** - `settings.json`'s `mcpServers` map mirrors the canonical `runtimes/mcp/servers.yaml`. Run `runtimes/mcp/render/render_gemini.py` to regenerate.

3. **Commands** - `gemini_cli_config.json`'s `commands` map is Gemini's slash-command equivalent. Each entry runs a shell command (not a prompt). Customize for your project.

## What Gemini does NOT support

- Skills (folder-per-skill `SKILL.md`) - N/A
- Agents (flat-file frontmatter) - N/A
- Hooks - N/A

The shared concepts SpecRoute ships are:

| Concept | Available in Gemini? |
|---|---|
| Slash commands | Yes (JSON map) |
| MCP servers | Yes |
| Engineering rules | Indirect - via root `GEMINI.md` and rules referenced from there |
| Prompts | Yes - the `prompts/` directory works in any agent CLI that reads markdown |

## Root context file

Gemini reads `GEMINI.md` at repo root. It should be a short delegation shim pointing to `AGENTS.md`. See [`../../GEMINI.md`](../../GEMINI.md) for an example.

## What's tracked vs gitignored

| Path | Tracked? |
|---|---|
| `.gemini/settings.json` | Yes (sans secrets) |
| `.gemini/gemini_cli_config.json` | Yes |

Secrets and personal preferences belong in environment variables or `.env` (gitignored).
