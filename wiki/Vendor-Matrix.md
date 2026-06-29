# Vendor Matrix

<!-- sources: README.md, AGENTS.md, agentic-docs/agent-cli-integrations.md -->

The supported-CLI contract. **Adding a new tool means a new column, not a fork.** This matrix is the single most important table in SpecRoute — it appears in `README.md`, `AGENTS.md`, and `agentic-docs/agent-cli-integrations.md` and must stay in lock-step across all three.

| Vendor | Runtime dir | Root context file | Skills | Agents | Commands | Hooks | MCP config |
|---|---|---|---|---|---|---|---|
| **Claude Code** | `.claude/` | `CLAUDE.md` | folder-per-skill `SKILL.md` | flat `<name>.md` + frontmatter | `commands/<name>.md` (merged into skills) | `settings.json hooks` (~30 events, 5 hook types) | `.mcp.json` / `~/.claude.json` |
| **Codex** | `.codex/` | `AGENTS.md` | folder-per-skill `SKILL.md` | `agents/<name>.toml` | skills (`/skills`, `$mention`) | `hooks.json` or `config.toml [hooks]` (10 events; default-on) | `config.toml [mcp_servers]` |
| **Gemini CLI** [^antigravity] | `.gemini/` | `GEMINI.md` (delegation shim) | `skills/<slug>/SKILL.md` | `agents/<name>.md` | TOML in `.gemini/commands/` | `settings.json hooks` (11 events; v0.26.0+) | `settings.json [mcpServers]` |
| **Kiro** | `.kiro/` | `steering/` files | `skills/<slug>/SKILL.md` | `agents/<name>.md` | `/skill` + manual steering | `*.kiro.hook` (10 events incl. file/agent/task triggers) | `.kiro/settings/mcp.json` |
| **Cursor** | `.cursor/` | `.cursor/rules/*.mdc` / `AGENTS.md` | `skills/` `SKILL.md` | `agents/<name>.md` | `commands/*.md` | `hooks.json` v1 (~21 events; permission/decision schema) | `.cursor/mcp.json` |
| **Windsurf / Devin** [^devin] | `.windsurf/` · `.devin/` | `.devin/rules/*.md` (pref) / `.windsurf/rules/` (legacy) | Cascade `SKILL.md` | subagents | `.windsurf/workflows/*.md` | `hooks.json` (12 events; pre-hooks block, post-hooks observe) | `~/.codeium/windsurf/mcp_config.json` |

[^antigravity]: Google began superseding the standalone Gemini CLI with **Antigravity CLI** on 2026-06-18 for free / Google-One tiers (paid Gemini Code Assist / Enterprise retain access). The `.gemini/` integration shape below remains valid for current installs.
[^devin]: Windsurf was acquired by Cognition and is being relaunched as **Devin Desktop** (docs at `docs.devin.ai`); Cascade reaches end-of-life 2026-07-01, succeeded by Devin Local. `.devin/rules/` now takes precedence over the legacy `.windsurf/rules/`.

## Capability convergence

Earlier SpecRoute releases sorted vendors into capability tiers (Full / Near-full / Partial / Specialized / Rules-only). **As of mid-2026 that distinction no longer holds.** All six supported tools have converged on a common capability set — the [Agent Skills open standard](https://agentskills.io) (`SKILL.md`), subagents, custom commands, lifecycle hooks, and MCP:

| Vendor | Skills | Agents | Commands | Hooks | MCP |
|---|:--:|:--:|:--:|:--:|:--:|
| Claude Code | ✅ | ✅ | ✅ | ✅ | ✅ |
| Codex | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini CLI | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kiro | ✅ | ✅ | ✅ | ✅ | ✅ |
| Cursor | ✅ | ✅ | ✅ | ✅ | ✅ |
| Windsurf / Devin | ✅ | ✅ | ✅ | ✅ | ✅ |

Vendors now differ in **file format and conventions**, not capability class — Codex agents are TOML where the others are Markdown; Gemini commands are TOML where Claude/Cursor are Markdown; MCP config lives in JSON for most but TOML for Codex. Pick vendors based on what your team uses; the framework's **content** (PRDs, specs, prompts, rules) and **runtime-layer artifacts** (skills, agents, commands, hooks) now land in any of them, each in its native shape.

## Hook system depth

All six vendors ship hooks; per-vendor depth differs significantly:

| Vendor | Event count | Blocking semantics | Hook types beyond shell |
|---|---|---|---|
| Claude Code | ~30 | rich (per-event) | `http`, `mcp_tool`, `prompt`, `agent` |
| Codex | 10 | per-event JSON | `command` only |
| Gemini CLI | 11 | per-event | `command` only |
| Kiro | 10 | pre-hooks block | `askAgent`, `runCommand` |
| Cursor | ~21 | `permission` schema | `command`, `prompt` |
| Windsurf | 12 | pre-hooks only | `command`, `powershell` |

See [[Hooks]] for the per-vendor event matrix.

## Root context files (load-bearing)

Every vendor auto-loads at least one context file at session start:

| Vendor | Auto-loaded file | What goes there |
|---|---|---|
| Claude Code | `CLAUDE.md` | Delegation shim → `AGENTS.md` + Claude-specific overrides |
| Codex | `AGENTS.md` | Canonical, vendor-neutral substance |
| Gemini CLI | `GEMINI.md` | Delegation shim → `AGENTS.md` + Gemini-specific overrides |
| Cursor | `.cursor/rules/*.mdc` or `AGENTS.md` (`.cursorrules` legacy) | Rule files, MDC frontmatter; native `AGENTS.md` support |
| Kiro | `.kiro/steering/*.md` (`inclusion: always`) | Steering rules |
| Windsurf / Devin | `.devin/rules/*.md` (pref) or `.windsurf/rules/*.md` (`trigger: always_on`) | Rule files |

The canonical pattern: `AGENTS.md` carries substance; `CLAUDE.md` / `GEMINI.md` etc. are short delegation shims. See [[Multi-Vendor Context Files]].

## MCP support

All six vendors now consume MCP server configurations, in **different shapes**:

| Vendor | Shape | Path |
|---|---|---|
| Claude Code | `mcpServers` JSON object | `.mcp.json` (project) / `~/.claude.json` (user) |
| Codex | `[mcp_servers.<name>]` TOML sections | `.codex/config.toml` |
| Gemini CLI | `mcpServers` JSON object | `.gemini/settings.json` |
| Kiro | `mcpServers` JSON object | `.kiro/settings/mcp.json` |
| Cursor | `mcpServers` JSON object | `.cursor/mcp.json` |
| Windsurf / Devin | `mcpServers` JSON object | `~/.codeium/windsurf/mcp_config.json` |

Maintaining these by hand is the failure mode. SpecRoute ships a **single source of truth** at `runtimes/mcp/servers.yaml` with per-vendor renderers (Claude `.mcp.json`, Codex TOML, Gemini JSON today; the remaining JSON-shaped vendors reuse the same `mcpServers` object). See [[MCP Integration]].

> **Note:** `claude_desktop_config.json` is the **Claude Desktop app's** MCP file, not Claude Code's. The Claude Code CLI reads `.mcp.json` (project, committed) and `~/.claude.json` (user). Earlier SpecRoute releases pointed at the Desktop file in error.

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
