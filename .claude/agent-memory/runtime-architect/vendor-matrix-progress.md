# Runtime Architect - Vendor Matrix Progress

Tracks the build-out state of each supported vendor's runtime layout. Update on every commit that adds or modifies a `runtimes/.<vendor>/` directory.

## Supported vendors

The matrix is defined in `README.md`. Adding a vendor: see the `add-vendor` skill.

| Vendor | Runtime dir | Skills | Agents | Commands | Hooks | MCP | Rules | Status |
|---|---|---|---|---|---|---|---|---|
| Claude Code | `runtimes/.claude/` | done | done | done | done | done | done | done |
| Codex | `runtimes/.codex/` | done | done | done | done | done | done | done |
| Gemini CLI | `runtimes/.gemini/` | done | done | done | done | done | done | done |
| Kiro | `runtimes/.kiro/` | done | done | done | done | done | done | done |
| Cursor | `runtimes/.cursor/` | done | done | done | done | done | done | done |
| Windsurf | `runtimes/.windsurf/` | done | done | done | done | done | done | done |
| Devin | `runtimes/.devin/` | done | done | done | done | done | done | done |

`n/a` = vendor doesn't support the feature; `TODO` = supported but not yet built; `done` = template + at least one example present. All vendors have been built out to the converged capability set (skills/agents/commands/hooks/MCP); Gemini commands are TOML files under `.gemini/commands/*.toml`.

## MCP single-source-of-truth

Status: done.

`runtimes/mcp/servers.yaml` is the canonical inventory. Renderers in `runtimes/mcp/render/` emit:

- `runtimes/.claude/mcp.template.json` (Claude Code reads `.mcp.json` at project scope, `~/.claude.json` at user scope)
- `runtimes/.codex/config.template.toml [mcp_servers]`
- `runtimes/.gemini/settings.template.json [mcpServers]`

Default server set (vendor-neutral, non-proprietary): `filesystem`, `github`, `memory`, `sequential-thinking`, `playwright`. Add more only with rationale.

## Cross-vendor sync (`tools/sync-skills.py`)

Status: done.

Scope:
- Diff `runtimes/.claude/skills/` vs `runtimes/.codex/skills/` (folder-per-skill, both vendors)
- Diff `runtimes/.claude/agents/` vs `runtimes/.codex/agents/` (flat .md, both vendors)
- Report drift; with `--apply`, copy the canonical version

## Build order (completed)

1. `runtimes/.claude/` (most complete vendor; reference for others)
2. `runtimes/mcp/servers.yaml` + Claude renderer
3. `runtimes/.codex/` (mirror Claude skills + agents; add Codex MCP renderer)
4. `tools/sync-skills.py` (now that two runtimes exist with overlap)
5. `runtimes/.gemini/` (commands as `.gemini/commands/*.toml` + skills + agents + MCP renderer)
6. `runtimes/.kiro/` (steering + hooks + skills + agents + MCP)
7. `runtimes/.cursor/`, `runtimes/.windsurf/` (rules + skills + agents + MCP)
8. `runtimes/.devin/`

All six original vendors plus Devin are now built out to the converged capability set (skills/agents/commands/hooks/MCP).

## Open questions

- Should `runtimes/.codex/` include a `scripts/sync.py` that mirrors `tools/sync-skills.py` for in-runtime use? (Common pattern in upstream private references.) Probably yes - but make it a thin wrapper.
- Cursor `.mdc` vs `.md` - confirm current Cursor expectation before building.
