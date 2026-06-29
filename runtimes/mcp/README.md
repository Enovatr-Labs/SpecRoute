# `runtimes/mcp/` - MCP Single Source of Truth

The Model Context Protocol (MCP) server inventory lives here. **All six supported vendors consume MCP**, but there are only **two emit shapes**: a JSON `mcpServers` object (everyone except Codex) and `[mcp_servers]` TOML (Codex). The vendors differ mainly in *where* the config lives:

| Vendor | Shape | Path |
|---|---|---|
| Claude Code | `mcpServers` JSON | `.mcp.json` (project) / `~/.claude.json` (user) |
| Codex | `[mcp_servers.<name>]` TOML | `.codex/config.toml` |
| Gemini CLI | `mcpServers` JSON | `.gemini/settings.json` |
| Kiro | `mcpServers` JSON | `.kiro/settings/mcp.json` |
| Cursor | `mcpServers` JSON | `.cursor/mcp.json` |
| Windsurf / Devin | `mcpServers` JSON | `~/.codeium/windsurf/mcp_config.json` (user scope) |

> Note: `.mcp.json` is the **Claude Code CLI's** file, not the Claude Desktop app's `claude_desktop_config.json`. Same shape, different products.

Maintaining six configs by hand is the failure mode. This directory establishes a **single source of truth** (`servers.yaml`) and per-vendor renderers that emit each config from it.

## Layout

```
runtimes/mcp/
├── README.md                            (this file)
├── servers.yaml                         canonical inventory
└── render/
    ├── render_claude.py                 → .claude/mcp.template.json (Claude Code .mcp.json)
    ├── render_codex.py                  → .codex/config.template.toml
    ├── render_gemini.py                 → .gemini/settings.template.json
    ├── render_kiro.py                   → .kiro/settings/mcp.template.json
    ├── render_cursor.py                 → .cursor/mcp.template.json
    └── render_windsurf.py               → ~/.codeium/windsurf/mcp_config.json (user scope; no committed template)
```

## Workflow

1. **Edit `servers.yaml`** to add, remove, or modify a server.

2. **Re-run the renderers** to regenerate per-vendor configs:

   ```bash
   python3 runtimes/mcp/render/render_claude.py   > runtimes/.claude/mcp.template.json
   python3 runtimes/mcp/render/render_codex.py    > runtimes/.codex/config.template.toml
   python3 runtimes/mcp/render/render_gemini.py   > runtimes/.gemini/settings.template.json
   python3 runtimes/mcp/render/render_kiro.py     > runtimes/.kiro/settings/mcp.template.json
   python3 runtimes/mcp/render/render_cursor.py   > runtimes/.cursor/mcp.template.json
   python3 runtimes/mcp/render/render_windsurf.py > ~/.codeium/windsurf/mcp_config.json   # user scope
   ```

3. **Commit the generated project-scoped files alongside `servers.yaml`** so reviewers see the impact in one diff. (Windsurf/Devin's config is user-scoped, so it has no committed template - render it straight to your home directory.)

## Why YAML?

`servers.yaml` is human-readable and supports light commentary. The renderers use a minimal hand-rolled parser (no PyYAML dependency) because the file shape is intentionally simple.

## What `servers.yaml` captures

For each server:

- `name` - slug used as the map key in vendor configs.
- `description` - human-readable purpose. Not emitted to vendor configs.
- `command` + `args` - how the MCP server starts.
- `requires_env` (optional) - environment variables the server needs (e.g. API tokens).
- `codex_tool_approvals` (optional) - Codex-specific per-tool approval modes; ignored by Claude / Gemini renderers.

## Adding a new server

1. Append a new entry to `servers.yaml`.
2. Re-run all three renderers.
3. Verify the `_comment` field at the top of each generated file is preserved.
4. If the server requires credentials, document them in `requires_env` - never inline secrets.

## Removing a server

1. Delete the entry from `servers.yaml`.
2. Re-run renderers.
3. Communicate the removal to consumers (it'll silently disappear from their MCP servers).

## Adding a new vendor

A new vendor that consumes MCP configs in a new shape gets a new renderer:

1. Add `render/render_<vendor>.py` modeled on the existing renderers.
2. Reuse `parse_yaml_minimal` from `render_claude.py` for parsing.
3. Render to the vendor's expected shape.
4. Add the per-vendor template under `runtimes/.<vendor>/`.
5. Document the vendor's MCP config conventions in `runtimes/.<vendor>/README.md`.

## Anti-patterns

- **Editing per-vendor configs by hand.** They're generated. Edits will be lost on the next render.
- **Per-vendor servers.yaml files.** That defeats the single-source purpose. Per-vendor differences live in renderer logic.
- **Inlining secrets.** Use `requires_env` to document required environment variables; never put credentials in `servers.yaml` or any generated file.

## Reference

- [`agentic-docs/cross-vendor-sync.md`](../../agentic-docs/cross-vendor-sync.md) - the broader cross-vendor sync pattern (skills, agents, MCP).
