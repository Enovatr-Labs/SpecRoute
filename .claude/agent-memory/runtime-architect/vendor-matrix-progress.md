# Runtime Architect - Vendor Matrix Progress

Tracks the build-out state of each supported vendor's runtime layout. Update on every commit that adds or modifies a `runtimes/.<vendor>/` directory.

## Supported vendors

The matrix is defined in `README.md`. Adding a vendor: see the `add-vendor` skill.

| Vendor | Runtime dir | Skills | Agents | Commands | Hooks | MCP | Rules | Status |
|---|---|---|---|---|---|---|---|---|
| Claude Code | `runtimes/.claude/` | TODO | TODO | TODO | TODO | TODO | TODO | not started |
| Codex | `runtimes/.codex/` | TODO | TODO | TODO | n/a | TODO | TODO | not started |
| Gemini CLI | `runtimes/.gemini/` | n/a | n/a | TODO | n/a | TODO | TODO | not started |
| Kiro | `runtimes/.kiro/` | n/a | n/a | n/a | TODO | n/a | TODO | not started |
| Cursor | `runtimes/.cursor/` | n/a | n/a | n/a | n/a | n/a | TODO | not started |
| Windsurf | `runtimes/.windsurf/` | n/a | n/a | n/a | n/a | n/a | TODO | not started |

`n/a` = vendor doesn't support the feature; `TODO` = supported but not yet built; `done` = template + at least one example present.

## MCP single-source-of-truth

Status: not started.

When built, `runtimes/mcp/servers.yaml` is the canonical inventory. Renderers in `runtimes/mcp/render/` emit:

- `runtimes/.claude/claude_desktop_config.template.json`
- `runtimes/.codex/config.template.toml [mcp_servers]`
- `runtimes/.gemini/settings.template.json [mcpServers]`

Default server set (vendor-neutral, non-proprietary): `filesystem`, `github`, `memory`, `sequential-thinking`, `playwright`. Add more only with rationale.

## Cross-vendor sync (`tools/sync-skills.py`)

Status: not started.

Scope (when built):
- Diff `runtimes/.claude/skills/` vs `runtimes/.codex/skills/` (folder-per-skill, both vendors)
- Diff `runtimes/.claude/agents/` vs `runtimes/.codex/agents/` (flat .md, both vendors)
- Report drift; with `--apply`, copy the canonical version

## Build order suggestion

1. `runtimes/.claude/` (most complete vendor; reference for others)
2. `runtimes/mcp/servers.yaml` + Claude renderer
3. `runtimes/.codex/` (mirror Claude skills + agents; add Codex MCP renderer)
4. `tools/sync-skills.py` (now that two runtimes exist with overlap)
5. `runtimes/.gemini/` (commands JSON + MCP renderer; no skills/agents)
6. `runtimes/.kiro/` (steering + hooks)
7. `runtimes/.cursor/`, `runtimes/.windsurf/` (rules only)

## Open questions

- Should `runtimes/.codex/` include a `scripts/sync.py` that mirrors `tools/sync-skills.py` for in-runtime use? (Common pattern in upstream private references.) Probably yes - but make it a thin wrapper.
- Cursor `.mdc` vs `.md` - confirm current Cursor expectation before building.
