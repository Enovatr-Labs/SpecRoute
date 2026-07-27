# `runtimes/mcp/` — MCP single source of truth

The canonical MCP server inventory lives in `servers.yaml`. All six supported
vendors consume it. Five renderers emit a JSON `mcpServers` object; Codex emits
`[mcp_servers]` TOML.

| Vendor | Shape | Install path |
|---|---|---|
| Claude Code | `mcpServers` JSON | `.mcp.json` / `~/.claude.json` |
| Codex | `[mcp_servers.<name>]` TOML | `.codex/config.toml` |
| Gemini CLI / Antigravity | `mcpServers` JSON | `.gemini/settings.json` |
| Kiro | `mcpServers` JSON | `.kiro/settings/mcp.json` |
| Cursor | `mcpServers` JSON | `.cursor/mcp.json` |
| Devin Desktop | `mcpServers` JSON | `.devin/config.json` |

## Layout

```text
runtimes/mcp/
├── README.md
├── servers.yaml
└── render/
    ├── render_claude.py
    ├── render_codex.py
    ├── render_gemini.py
    ├── render_kiro.py
    ├── render_cursor.py
    └── render_devin.py
```

`render_claude.py` also provides the shared stdlib-only YAML parser and the
environment-note helper used by renderers whose config formats do not provide
a portable tracked-template expansion form.

## Regenerate

```bash
python3 runtimes/mcp/render/render_claude.py > runtimes/.claude/mcp.template.json
python3 runtimes/mcp/render/render_codex.py > runtimes/.codex/config.template.toml
python3 runtimes/mcp/render/render_gemini.py > runtimes/.gemini/settings.template.json
python3 runtimes/mcp/render/render_kiro.py > runtimes/.kiro/settings/mcp.template.json
python3 runtimes/mcp/render/render_cursor.py > runtimes/.cursor/mcp.template.json
python3 runtimes/mcp/render/render_devin.py > runtimes/.devin/config.template.json
```

All six outputs are project templates and can be reviewed with the source
inventory. Install the Devin output as `.devin/config.json`; put personal
credentials in the gitignored `.devin/config.local.json`.

## Inventory fields

- `name` — key used in the rendered config.
- `description` — documentation only.
- `command` and `args` — server launch command.
- `requires_env` — credential names a consumer must supply.
- `codex_tool_approvals` — Codex-only approval metadata.

Renderers never inline credential values. Most renderers turn `requires_env`
into a comment so the requirement remains visible without committing a secret.
The Devin renderer uses Devin Local's documented `${env:VAR}` substitution in
the server's `env` map, so its generated config contains only references to
shell environment variables.

## Adding or removing a server

1. Edit `servers.yaml`.
2. Run all six renderers.
3. Parse every JSON/TOML output.
4. Confirm each required environment variable is still named.
5. Commit only placeholder-free, project-scoped templates.

Cascade compatibility remains available inside Devin Desktop during the
transition. Cascade reads `~/.codeium/windsurf/mcp_config.json`; merge the same
rendered `mcpServers` object there only when a project still uses Cascade. It is
not a seventh renderer or a separate vendor.

See [`agentic-docs/cross-vendor-sync.md`](../../agentic-docs/cross-vendor-sync.md)
for the broader synchronization model.
