# Vendor Matrix

<!-- sources: README.md, AGENTS.md, agentic-docs/agent-cli-integrations.md -->

The supported-CLI contract. **Adding a new tool means a new column, not a fork.** This matrix is the single most important table in SpecRoute - it is mirrored in four files (`README.md`, `AGENTS.md`, `agentic-docs/agent-cli-integrations.md`, and this page) and must stay in lock-step across all four.

| Vendor | Runtime dir | Root context file | Skills | Agents | Commands | Hooks | MCP config |
|---|---|---|---|---|---|---|---|
| Claude Code | `.claude/` | `CLAUDE.md` | folder-per-skill `SKILL.md` | flat `<name>.md` + frontmatter | `commands/<name>.md` (merged into skills) | `settings.json` `hooks` (30 events; 5 handler types) | `.mcp.json` / `~/.claude.json` |
| Codex | `.codex/` | `AGENTS.md` | folder-per-skill `SKILL.md` | `agents/<name>.toml` | skills (`/skills`, `$mention`) | `hooks.json` or `config.toml [hooks]` (11 events; Claude-compatible names) | `config.toml [mcp_servers]` |
| Gemini CLI / Antigravity | `.gemini/` | `GEMINI.md` (delegation shim) | `skills/<slug>/SKILL.md` | `agents/<name>.md` | TOML in `.gemini/commands/` | `settings.json` `hooks` (11 events; `Before*` / `After*` names) | `settings.json [mcpServers]` |
| Kiro | `.kiro/` | `steering/` files | `skills/<slug>/SKILL.md` | `agents/<name>.md` | `/skill` + manual steering | `.kiro/hooks/<name>.json` v1 (10 triggers) | `.kiro/settings/mcp.json` |
| Cursor | `.cursor/` | `.cursor/rules/*.mdc` / `AGENTS.md` | `skills/<slug>/SKILL.md` | `agents/<name>.md` | `commands/*.md` | `.cursor/hooks.json` v1 (21 events, camelCase) | `.cursor/mcp.json` |
| Devin Desktop | `.devin/` | `AGENTS.md` | `.agents/skills/` (recommended) / `.devin/skills/` | `.devin/agents/<name>/AGENT.md` (experimental) | skills (`/skill-name`); Cascade workflows | `.devin/hooks.v1.json` (8 events); Cascade hooks | `.devin/config.json [mcpServers]`; Cascade MCP |

## Vendor notes and sources

- **Root context files.** Claude Code reads `CLAUDE.md`, **not** `AGENTS.md` - the official documentation says so directly. Gemini CLI reads `GEMINI.md` and only picks up `AGENTS.md` when you opt in via `context.fileName`; the upstream issue asking for default support was closed as not planned. Bridge either with an `@AGENTS.md` import inside the vendor file, or a symlink. Codex, Cursor, and Devin Desktop read `AGENTS.md` natively.
- **Claude Code hooks.** Claude Code loads hooks from `settings.json` (user / project / local), managed policy settings, a **plugin's** `hooks/hooks.json`, and skill or agent frontmatter. A bare project-level `.claude/hooks/hooks.json` is **not** a hook source - keep it as the authoring artifact and merge its `hooks` key into `.claude/settings.json`. The five handler types are `command`, `http`, `mcp_tool`, `prompt`, and `agent`.
- **Codex hooks.** Verified against an installed `codex-cli` 0.145.0 binary: `SessionStart`, `SessionEnd`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`. Codex adopted Claude Code's event names and handler JSON (`hookSpecificOutput`, `permissionDecision`, `decision: "block"`) almost verbatim - but the match is close, not total: Claude's `PostToolUseFailure` has no Codex counterpart, and only `type: "command"` actually executes in Codex (`prompt` and `agent` handlers are parsed, then skipped). Hooks are **enabled by default**; the canonical `[features]` key is `hooks`, with `codex_hooks` retained as a deprecated alias. Disable with `[features] hooks = false`.
- **Gemini CLI / Antigravity.** Google redirected consumer access to **Antigravity CLI** on 2026-06-18 for free and Google AI Pro / Ultra tiers. Paid Gemini Code Assist Standard / Enterprise and qualifying API-key users retain Gemini CLI access. The `.gemini/` integration layout remains valid across both.
- **Kiro hooks.** Kiro IDE 1.0 (2026-06-25) replaced the `*.kiro.hook` format with `.kiro/hooks/<name>.json` (root `"version": "v1"`). Triggers (10): `SessionStart`, `Stop`, `PreToolUse`, `PostToolUse`, `PreTaskExec`, `PostTaskExec`, `UserPromptSubmit`, `PostFileCreate`, `PostFileSave`, `PostFileDelete`. The 0.x `Manual` trigger was **retired** - manual invocation is now a steering file. Actions are `action.type: "command"` or `"agent"`, replacing `runCommand` / `askAgent`. Legacy `*.kiro.hook` files show an upgrade badge and no longer execute.
- **Cursor rules.** `.cursorrules` has been removed from Cursor's documentation entirely and is reported non-functional in current versions. Treat it as removed rather than legacy-but-supported; use `.cursor/rules/*.mdc`. Cursor also ships Skills, Subagents, Hooks, and a Plugins marketplace.
- **Devin Desktop.** Devin Desktop is the new name for Windsurf. Devin Local uses the `.devin/` paths shown above and is intended to become the primary local agent. Cascade remains available and still uses `.windsurf/workflows/*.md`, `.windsurf/hooks.json`, and `~/.codeium/windsurf/mcp_config.json`; `.windsurf/rules/` and `.windsurf/skills/` remain accepted compatibility locations. These are Devin Desktop configuration namespaces, not a separate vendor or runtime. Do not infer `.devin/workflows/`, `.devin/hooks.json`, or `.devin/mcp.json`.

## Capability convergence

Earlier SpecRoute releases sorted vendors into capability tiers (Full / Near-full / Partial / Specialized / Rules-only). **As of mid-2026 that tiering no longer holds** - every supported tool ships every capability class: the [Agent Skills open standard](https://agentskills.io) (`SKILL.md`), subagents, custom commands, lifecycle hooks, and MCP.

Two different claims used to be collapsed into one table here, and that conflation is what produced the drift. They are now separated.

### 1. Does the vendor support the capability?

| Vendor | Skills | Agents | Commands | Hooks | MCP |
|---|:--:|:--:|:--:|:--:|:--:|
| Claude Code | ✅ | ✅ | ✅ | ✅ | ✅ |
| Codex | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini CLI / Antigravity | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kiro | ✅ | ✅ | ✅ | ✅ | ✅ |
| Cursor | ✅ | ✅ | ✅ | ✅ | ✅ |
| Devin Desktop | ✅ | ✅ | ✅ | ✅ | ✅ |

### 2. Does SpecRoute ship a runtime layout for it?

Measured against `runtimes/` on disk, not against vendor capability. A dash means that artifact is absent from the SpecRoute runtime layout; the note below distinguishes intentional omissions from open gaps.

| Runtime layout | Skills | Agents | Commands | Hooks | MCP |
|---|:--:|:--:|:--:|:--:|:--:|
| Claude Code - `runtimes/.claude` | ✅ | ✅ | ✅ `commands/` | ✅ `hooks/` | ✅ `mcp.template.json` |
| Codex - `runtimes/.codex` | ✅ | ✅ | - (skills serve as commands) | ✅ `hooks/` | ✅ `config.template.toml` |
| Gemini CLI - `runtimes/.gemini` | ✅ | ✅ | ✅ `commands/` | ✅ `hooks/` (snippet) | ✅ `settings.template.json` |
| Kiro - `runtimes/.kiro` | ✅ | ✅ | - (steering + `/skill`) | ✅ `hooks/` | ✅ `settings/mcp.template.json` |
| Cursor - `runtimes/.cursor` | ✅ | ✅ | ✅ `commands/` | ✅ `hooks/` | ✅ `mcp.template.json` |
| Devin Desktop - `runtimes/.devin` | ✅ | ✅ | skills (`/name`) | ✅ `hooks/` | ✅ `config.template.json` |

All six runtime layouts ship hook assets. Gemini is the one exception in shape:
its hooks live under the `hooks` key inside `.gemini/settings.json`, so the
layout ships a documented merge snippet rather than a standalone file.

### What has actually converged

Vendors differ in **file format and conventions** - Codex agents are TOML where the others are Markdown; Gemini commands are TOML where Claude / Cursor are Markdown; MCP config is JSON for most but TOML for Codex.

- **Skills: converged.** The `SKILL.md` shape is portable across all six with little more than a path change. This is the one near-total convergence.
- **Hooks: not converged.** See below.
- **MCP: converged on the payload**, split on the container - one `mcpServers` JSON object everywhere except Codex's TOML.

## Hook system depth

All six vendors ship hooks; the systems have **not** converged. Claude Code,
Codex, Kiro, and Devin Local share several core event names, but their payload
and decision schemas still differ. Cursor and Gemini CLI retain distinct
vocabularies.

| Vendor | Event count | Naming vocabulary | Blocking semantics | Handler types |
|---|---|---|---|---|
| Claude Code | 30 | `PreToolUse` / `PostToolUse` / … | rich (per-event) | `command`, `http`, `mcp_tool`, `prompt`, `agent` |
| Codex | 11 | Claude-compatible | per-event JSON | `command` (only type that executes) |
| Gemini CLI | 11 | `BeforeTool` / `AfterModel` / `BeforeToolSelection` | per-event | `command` |
| Kiro | 10 | Claude-compatible since IDE 1.0 | pre-hooks block | `command`, `agent` |
| Cursor | 21 | camelCase (`beforeShellExecution`, …) | exit 2 = deny; fail-open unless `failClosed: true` | `command`, `prompt` |
| Devin Desktop | 8 | `PreToolUse` / `SessionStart` style | exit 2 blocks | `command`, `prompt` |

See [[Hooks]] for the per-vendor event matrix.

## Root context files (load-bearing)

Every vendor auto-loads at least one context file at session start. **Codex,
Cursor, and Devin Desktop auto-load `AGENTS.md`.** Claude Code's documentation
states plainly that it reads `CLAUDE.md`, not `AGENTS.md`; Gemini CLI reads
`GEMINI.md` and treats `AGENTS.md` as opt-in via `context.fileName`. The
sanctioned bridge for both is an `@AGENTS.md` import inside the vendor file, or
a symlink.

| Vendor | Auto-loaded file | Reads `AGENTS.md` natively? | What goes there |
|---|---|:--:|---|
| Claude Code | `CLAUDE.md` | no - bridge via `@AGENTS.md` import or symlink | Delegation shim → `AGENTS.md` + Claude-specific overrides |
| Codex | `AGENTS.md` | yes | Canonical, vendor-neutral substance |
| Gemini CLI | `GEMINI.md` | no - opt in via `context.fileName` | Delegation shim → `AGENTS.md` + Gemini-specific overrides |
| Cursor | `.cursor/rules/*.mdc` or `AGENTS.md` | yes | Rule files, MDC frontmatter; native `AGENTS.md` support. `.cursorrules` is **removed**, not legacy - it is gone from Cursor's docs and reported non-functional |
| Kiro | `.kiro/steering/*.md` (`inclusion: always`) | no | Steering rules |
| Devin Desktop | `AGENTS.md` | yes | Canonical rules; `.devin/rules/` is an additional rule location |

The canonical pattern: `AGENTS.md` carries substance; `CLAUDE.md` / `GEMINI.md` etc. are short delegation shims. See [[Multi-Vendor Context Files]].

### The `AGENTS.md` convention itself

`AGENTS.md` started as an OpenAI convention and is now stewarded by the **Agentic AI Foundation** under the Linux Foundation, with 60,000+ repositories using it. It specifies **no required fields, no frontmatter, and no schema** - plain Markdown, contents entirely up to the project. Nested `AGENTS.md` files are spec'd behaviour: an agent reads the nearest one up the directory tree.

A vendor-neutral **`.agents/` directory** is emerging as the companion location for runtime artifacts. SpecRoute verified this against an installed Codex 0.145.0 binary rather than documentation, because public docs are inconsistent: the binary carries `.agents/skills` as a repo-level skills root (error string `failed to stat repo skills root`), `.agents/plugins/marketplace.json`, `.agents/plugins/api_marketplace.json`, and enumerates `.agents` beside `.claude` and `.cursor` when detecting external agent configuration. The same binary **still** carries `.codex/skills` and `$CODEX_HOME/skills`, so both work today - do not migrate off `.codex/skills` yet.

## MCP support

All six vendors now consume MCP server configurations, in **different shapes**:

| Vendor | Shape | Path |
|---|---|---|
| Claude Code | `mcpServers` JSON object | `.mcp.json` (project) / `~/.claude.json` (user) |
| Codex | `[mcp_servers.<name>]` TOML sections | `.codex/config.toml` |
| Gemini CLI / Antigravity | `mcpServers` JSON object | `.gemini/settings.json` |
| Kiro | `mcpServers` JSON object | `.kiro/settings/mcp.json` |
| Cursor | `mcpServers` JSON object | `.cursor/mcp.json` |
| Devin Desktop | `mcpServers` JSON object | `.devin/config.json` |

Maintaining these by hand is the failure mode. SpecRoute ships a **single
source of truth** at `runtimes/mcp/servers.yaml` with six per-vendor renderers:
`render_claude.py`, `render_codex.py`, `render_gemini.py`, `render_kiro.py`,
`render_cursor.py`, and `render_devin.py`. See [[MCP Integration]].

> **Spec change in flight:** an MCP specification revision dated **2026-07-28** removes sessions and the `Mcp-Session-Id` header - the protocol goes stateless - and formally deprecates HTTP+SSE in favour of streamable HTTP. Treat this as imminent rather than shipped, and check the revision date before relying on it. SpecRoute's `servers.yaml` shape is unaffected either way; only transport wiring is.

> **Note:** `claude_desktop_config.json` is the **Claude Desktop app's** MCP file, not Claude Code's. The Claude Code CLI reads `.mcp.json` (project, committed) and `~/.claude.json` (user). Earlier SpecRoute releases pointed at the Desktop file in error.

## Vendor neutrality is the contract

- Don't fold one vendor into another.
- Don't treat any vendor as the default.
- Every artifact declares which vendors it targets and uses each vendor's **native shape**.
- Don't drift the matrix between `README.md`, `AGENTS.md`, `agentic-docs/agent-cli-integrations.md`, and this page - when one changes, all four change. The table body is byte-identical across all four by design; copy the whole table rather than editing one cell. Supporting notes live here and in the integration reference instead of the README.
- Don't conflate "the vendor supports it" with "SpecRoute ships a runtime layout for it". Those are the two tables under [Capability convergence](#capability-convergence), and merging them is what caused the last round of drift.

## See also

- [[Agent CLI Integrations]] — concrete per-vendor wiring (copy commands)
- [[Cross-Vendor Sync]] — `tools/sync-skills.py` + MCP renderers keep things aligned
- [[Adding a Vendor]] — process for adding a new column
- [[Multi-Vendor Context Files]] — the `AGENTS.md` + delegation-shim pattern
