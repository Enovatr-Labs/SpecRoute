# Vendor Matrix

<!-- sources: README.md, AGENTS.md, agentic-docs/agent-cli-integrations.md -->

The supported-CLI contract. **Adding a new tool means a new column, not a fork.** This matrix is the single most important table in SpecForge — it appears in `README.md`, `AGENTS.md`, and `agentic-docs/agent-cli-integrations.md` and must stay in lock-step across all three.

| Vendor | Runtime dir | Root context file | Skills | Agents | Commands | Hooks | MCP config |
|---|---|---|---|---|---|---|---|
| **Claude Code** | `.claude/` | `CLAUDE.md` | folder-per-skill `SKILL.md` | flat `<name>.md` + frontmatter | `commands/<name>.md` | `settings.json hooks` (~27 events, 5 hook types) | `claude_desktop_config.json` |
| **Codex** | `.codex/` | `AGENTS.md` | folder-per-skill `SKILL.md` | flat `<name>.md` | via skills (`user-invocable: true`) | `hooks.json` or `config.toml [hooks]` (6 events; flag `codex_hooks=true`) | `config.toml [mcp_servers]` |
| **Gemini CLI** | `.gemini/` | `GEMINI.md` (delegation shim) | – | – | `gemini_cli_config.json` | `settings.json hooks` (11 events; v0.26.0+) | `settings.json [mcpServers]` |
| **Kiro** | `.kiro/` | `steering/` files | – | – | – | `*.kiro.hook` (10 events incl. file / agent / task triggers) | – |
| **Cursor** | `.cursor/rules/` | `.cursorrules` | – | – | – | `hooks.json` v1 (~19 events; permission/decision schema) | – |
| **Windsurf** | `.windsurf/rules/` | – | – | – | – | `hooks.json` (12 events; pre/post for read/write/run/mcp) | – |

## Vendor support tiers

| Tier | Vendors | What's supported |
|---|---|---|
| **Full** | Claude Code | Skills, agents, commands, hooks, MCP, root context file, sub-agent delegation |
| **Near-full** | Codex | Skills, agents, MCP, root context file (commands subsumed into skills via `user-invocable`) |
| **Partial** | Gemini CLI | MCP, command map, root context file |
| **Specialized** | Kiro | Steering rules, spec triplet, file-pattern hooks |
| **Rules only** | Cursor, Windsurf | Rule files |

Pick vendors based on what your team uses. The framework's **content** (PRDs, specs, prompts, rules) works in any of them; the **runtime-layer features** (skills, agents, commands, hooks) only land where the vendor supports them.

## Hook system depth

All six vendors ship hooks; per-vendor depth differs significantly:

| Vendor | Event count | Blocking semantics | Hook types beyond shell |
|---|---|---|---|
| Claude Code | ~27 | rich (per-event) | `http`, `mcp_tool`, `prompt`, `agent` |
| Codex | 6 | per-event JSON | `command` only |
| Gemini CLI | 11 | per-event | `command` only |
| Kiro | 10 | pre-hooks block | `askAgent` (built-in) |
| Cursor | ~19 | `permission` schema | `command`, `prompt` |
| Windsurf | 12 | pre-hooks only | `command`, `powershell` |

See [[Hooks]] for the per-vendor event matrix.

## Root context files (load-bearing)

Every vendor auto-loads at least one context file at session start:

| Vendor | Auto-loaded file | What goes there |
|---|---|---|
| Claude Code | `CLAUDE.md` | Delegation shim → `AGENTS.md` + Claude-specific overrides |
| Codex | `AGENTS.md` | Canonical, vendor-neutral substance |
| Gemini CLI | `GEMINI.md` | Delegation shim → `AGENTS.md` + Gemini-specific overrides |
| Cursor | `.cursorrules` (legacy) or `.cursor/rules/*.mdc` | Rule files, MDC frontmatter |
| Kiro | `.kiro/steering/*.md` (`inclusion: always`) | Steering rules |
| Windsurf | `.windsurf/rules/*.md` (`trigger: always`) | Rule files |

The canonical pattern: `AGENTS.md` carries substance; `CLAUDE.md` / `GEMINI.md` etc. are short delegation shims. See [[Multi-Vendor Context Files]].

## MCP support

Three vendors consume MCP server configurations in **different shapes**:

| Vendor | Shape | Path |
|---|---|---|
| Claude Desktop | `mcpServers` JSON object | `.claude/claude_desktop_config.json` |
| Codex | `[mcp_servers.<name>]` TOML sections | `.codex/config.toml` |
| Gemini CLI | `mcpServers` JSON object | `.gemini/settings.json` |

Maintaining three by hand is the failure mode. SpecForge ships a **single source of truth** at `runtimes/mcp/servers.yaml` with per-vendor renderers. See [[MCP Integration]].

## Vendor neutrality is the contract

- Don't fold one vendor into another.
- Don't treat any vendor as the default.
- Every artifact declares which vendors it targets and uses each vendor's **native shape**.
- Don't drift the matrix between `README.md`, `AGENTS.md`, and `agentic-docs/agent-cli-integrations.md` — when one changes, all three change.

## See also

- [[Agent CLI Integrations]] — concrete per-vendor wiring (copy commands)
- [[Cross-Vendor Sync]] — `tools/sync-skills.py` + MCP renderers keep things aligned
- [[Adding a Vendor]] — process for adding a new column
- [[Multi-Vendor Context Files]] — the `AGENTS.md` + delegation-shim pattern
