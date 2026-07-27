# Agent CLI Integrations

Concrete wiring for SpecRoute into each supported agent CLI. The matrix below is the contract - adding a new tool means a new column, not a fork.

## Supported vendor matrix

| Vendor | Runtime dir | Root context file | Skills | Agents | Commands | Hooks | MCP config |
|---|---|---|---|---|---|---|---|
| Claude Code | `.claude/` | `CLAUDE.md` | folder-per-skill `SKILL.md` | flat `<name>.md` + frontmatter | `commands/<name>.md` (merged into skills) | `settings.json` `hooks` (30 events; 5 handler types) | `.mcp.json` / `~/.claude.json` |
| Codex | `.codex/` | `AGENTS.md` | folder-per-skill `SKILL.md` | `agents/<name>.toml` | skills (`/skills`, `$mention`) | `hooks.json` or `config.toml [hooks]` (11 events; Claude-compatible names) | `config.toml [mcp_servers]` |
| Gemini CLI / Antigravity | `.gemini/` | `GEMINI.md` (delegation shim) | `skills/<slug>/SKILL.md` | `agents/<name>.md` | TOML in `.gemini/commands/` | `settings.json` `hooks` (11 events; `Before*` / `After*` names) | `settings.json [mcpServers]` |
| Kiro | `.kiro/` | `steering/` files | `skills/<slug>/SKILL.md` | `agents/<name>.md` | `/skill` + manual steering | `.kiro/hooks/<name>.json` v1 (10 triggers) | `.kiro/settings/mcp.json` |
| Cursor | `.cursor/` | `.cursor/rules/*.mdc` / `AGENTS.md` | `skills/<slug>/SKILL.md` | `agents/<name>.md` | `commands/*.md` | `.cursor/hooks.json` v1 (21 events, camelCase) | `.cursor/mcp.json` |
| Devin Desktop | `.devin/` | `AGENTS.md` | `.agents/skills/` (recommended) / `.devin/skills/` | `.devin/agents/<name>/AGENT.md` (experimental) | skills (`/skill-name`); Cascade workflows | `.devin/hooks.v1.json` (8 events); Cascade hooks | `.devin/config.json [mcpServers]`; Cascade MCP |

This matrix appears in four places (`README.md`, `AGENTS.md`, `wiki/Vendor-Matrix.md`, this file) and must stay in lock-step. The table body is byte-identical in all four - copy the whole table rather than editing a single cell. The implementation notes and source evidence are centralized here and mirrored to the dedicated wiki page so the README can remain an overview. All six tools ship the same capability *classes*; that is not the same as convergence (see [Capability convergence](#vendor-capability-convergence) below).

### Vendor notes and sources

- **Root context files.** Claude Code reads `CLAUDE.md`, **not** `AGENTS.md` - the official documentation says so directly. Gemini CLI reads `GEMINI.md` and only picks up `AGENTS.md` when you opt in via `context.fileName`; the upstream issue asking for default support was closed as not planned. Bridge either with an `@AGENTS.md` import inside the vendor file, or a symlink. Codex, Cursor, and Devin Desktop read `AGENTS.md` natively.
- **Claude Code hooks.** Claude Code loads hooks from `settings.json` (user / project / local), managed policy settings, a **plugin's** `hooks/hooks.json`, and skill or agent frontmatter. A bare project-level `.claude/hooks/hooks.json` is **not** a hook source - keep it as the authoring artifact and merge its `hooks` key into `.claude/settings.json`. The five handler types are `command`, `http`, `mcp_tool`, `prompt`, and `agent`.
- **Codex hooks.** Verified against an installed `codex-cli` 0.145.0 binary: `SessionStart`, `SessionEnd`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`. Codex adopted Claude Code's event names and handler JSON (`hookSpecificOutput`, `permissionDecision`, `decision: "block"`) almost verbatim - but the match is close, not total: Claude's `PostToolUseFailure` has no Codex counterpart, and only `type: "command"` actually executes in Codex (`prompt` and `agent` handlers are parsed, then skipped). Hooks are **enabled by default**; the canonical `[features]` key is `hooks`, with `codex_hooks` retained as a deprecated alias. Disable with `[features] hooks = false`.
- **Gemini CLI / Antigravity.** Google redirected consumer access to **Antigravity CLI** on 2026-06-18 for free and Google AI Pro / Ultra tiers. Paid Gemini Code Assist Standard / Enterprise and qualifying API-key users retain Gemini CLI access. The `.gemini/` integration layout remains valid across both.
- **Kiro hooks.** Kiro IDE 1.0 (2026-06-25) replaced the `*.kiro.hook` format with `.kiro/hooks/<name>.json` (root `"version": "v1"`). Triggers (10): `SessionStart`, `Stop`, `PreToolUse`, `PostToolUse`, `PreTaskExec`, `PostTaskExec`, `UserPromptSubmit`, `PostFileCreate`, `PostFileSave`, `PostFileDelete`. The 0.x `Manual` trigger was **retired** - manual invocation is now a steering file. Actions are `action.type: "command"` or `"agent"`, replacing `runCommand` / `askAgent`. Legacy `*.kiro.hook` files show an upgrade badge and no longer execute.
- **Cursor rules.** `.cursorrules` has been removed from Cursor's documentation entirely and is reported non-functional in current versions. Treat it as removed rather than legacy-but-supported; use `.cursor/rules/*.mdc`. Cursor also ships Skills, Subagents, Hooks, and a Plugins marketplace.
- **Devin Desktop.** Devin Desktop is the new name for Windsurf. Devin Local uses the `.devin/` paths shown above and is intended to become the primary local agent. Cascade remains available and still uses `.windsurf/workflows/*.md`, `.windsurf/hooks.json`, and `~/.codeium/windsurf/mcp_config.json`; `.windsurf/rules/` and `.windsurf/skills/` remain accepted compatibility locations. These are Devin Desktop configuration namespaces, not a separate vendor or runtime. Do not infer `.devin/workflows/`, `.devin/hooks.json`, or `.devin/mcp.json`.

### Per-vendor detail behind the cells

The matrix cells are deliberately terse so the four mirrors can stay byte-identical. The detail that used to live inside them:

- **Claude Code** - skill and command files also carry frontmatter; agents require only `name` and `description` (`model` and `color` are SpecRoute convention, not runtime requirements). Template: [`hooks/claude/hooks.template.json`](../hooks/claude/hooks.template.json).
- **Codex** - agent TOML keys are `name`, `description`, `developer_instructions`. Hooks may be a standalone `hooks.json` or an inline `[hooks]` table in `config.toml`.
- **Gemini CLI** - command TOML takes a required `prompt` and an optional `description`. The 11 hook events are `BeforeTool` / `AfterTool`, `BeforeAgent` / `AfterAgent`, `BeforeModel` / `AfterModel`, `BeforeToolSelection`, `SessionStart` / `SessionEnd`, `Notification`, `PreCompress`.
- **Kiro** - steering files use `inclusion: manual` for `/skill`-style invocation. Hook shape and the full trigger list: [`hooks/kiro/README.md`](../hooks/kiro/README.md).
- **Cursor** - hooks resolve from project, user, and enterprise paths, with a `permission` / `decision` response schema.
- **Devin Desktop** - Devin Local uses eight lifecycle events and skills invoked
  as `/skill-name`. Cascade remains a compatibility agent with its older
  12-event hook and workflow surfaces.

### Hook system depth

All six vendors ship hook systems, and they have **not** converged. Claude Code,
Codex, Kiro, and Devin Local share several core event names; their payload and
decision schemas still differ. Cursor and Gemini CLI retain distinct
vocabularies. **Skills, not hooks, are where cross-vendor convergence is
near-total.**

| Vendor | Event count | Naming vocabulary | Blocking semantics | Handler types |
|---|---|---|---|---|
| Claude Code | 30 | `PreToolUse` / `PostToolUse` / … | rich (per-event) | `command`, `http`, `mcp_tool`, `prompt`, `agent` |
| Codex | 11 | Claude-compatible | per-event JSON | `command` (only type that executes) |
| Gemini CLI | 11 | `BeforeTool` / `AfterModel` / `BeforeToolSelection` | per-event | `command` |
| Kiro | 10 | Claude-compatible since IDE 1.0 | pre-hooks block | `command`, `agent` |
| Cursor | 21 | camelCase (`beforeShellExecution`, …) | exit 2 = deny; fail-open unless `failClosed: true` | `command`, `prompt` |
| Devin Desktop | 8 | `PreToolUse` / `SessionStart` style | exit 2 blocks | `command`, `prompt` |

Claude Code's 30 events are: `SessionStart`, `Setup`, `UserPromptSubmit`, `UserPromptExpansion`, `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Stop`, `StopFailure`, `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `TeammateIdle`, `Notification`, `MessageDisplay`, `ConfigChange`, `CwdChanged`, `FileChanged`, `PreCompact`, `PostCompact`, `WorktreeCreate`, `WorktreeRemove`, `InstructionsLoaded`, `Elicitation`, `ElicitationResult`, `SessionEnd`.

For the full per-vendor event list, see [`hooks/README.md`](../hooks/README.md). Per-vendor templates: [`hooks/<vendor>/`](../hooks/).

## How to wire each vendor

### Claude Code

```bash
# 1. Drop the runtime layout
cp -R runtimes/.claude/ /path/to/your/repo/.claude/

# 2. Rename templates
cd /path/to/your/repo/.claude
mv settings.template.json            settings.json
mv settings.local.template.json      settings.local.json    # then customize for your machine
mv mcp.template.json                 ../.mcp.json           # Claude Code reads .mcp.json at repo root
mv hooks/hooks.template.json         hooks/hooks.json       # authoring artifact only - see step 3

# 3. Merge the hooks into settings.json - the file the CLI actually reads.
#    A bare project-level .claude/hooks/hooks.json is NOT a hook source; that
#    filename is only a hook source inside a *plugin*. Stop here and your hooks
#    never fire.
/path/to/specroute/tools/sync-hooks-to-settings.sh \
  /path/to/your/repo/.claude/hooks/hooks.json \
  /path/to/your/repo/.claude/settings.json

# 4. Install hook scripts (copy from this repo's .claude/hooks/ or write your own)
cp /path/to/specroute/.claude/hooks/*.sh /path/to/your/repo/.claude/hooks/scripts/
chmod +x /path/to/your/repo/.claude/hooks/scripts/*.sh

# 5. Create the gitignored sanitization wordlist
cat > /path/to/your/repo/.claude/.forbidden-strings.txt <<'EOF'
# One forbidden term per line
EOF

# 6. Add to .gitignore
echo ".claude/settings.local.json" >> /path/to/your/repo/.gitignore
echo ".claude/.forbidden-strings.txt" >> /path/to/your/repo/.gitignore

# 7. Populate agents/, skills/, commands/ as your project requires
```

**Where Claude Code reads hooks from.** `settings.json` at user (`~/.claude/`), project (`.claude/`), and local (`.claude/settings.local.json`) scope; managed policy settings; a **plugin's** `hooks/hooks.json`; and skill or agent frontmatter. That list does not include a project-level `.claude/hooks/hooks.json`. SpecRoute keeps `hooks.json` as the authoring artifact - it is the vendor-neutral shape, it can carry `_comment` annotations that would be noise in `settings.json`, and it is what other vendors' runtimes mirror - and `tools/sync-hooks-to-settings.sh` copies its `hooks` key into the file that executes.

### Codex

```bash
cp -R runtimes/.codex/ /path/to/your/repo/.codex/
cd /path/to/your/repo/.codex
mv config.template.toml config.toml

# Mirror skills from your Claude runtime (skills share the SKILL.md shape across both)
python3 /path/to/specroute/tools/sync-skills.py --source claude --apply
```

Codex consumes the same folder-per-skill `SKILL.md` shape as Claude Code, so skills cross-mirror directly. **Agents differ in format**: Codex agents are standalone TOML files (`.codex/agents/<name>.toml` with `name`, `description`, `developer_instructions`), not Claude's flat Markdown - `sync-skills.py` therefore syncs skills only, not agents. The `config.toml` carries Codex-specific MCP config and approval policy.

Codex hooks are enabled by default. The canonical feature key is `[features] hooks`, with `codex_hooks` retained as a deprecated alias. Codex's 11 hook events use Claude Code's names verbatim (`SessionStart`, `SessionEnd`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`) and the same handler JSON, but the overlap is close rather than total: there is no `PostToolUseFailure`, and only `type: "command"` handlers actually execute - `prompt` and `agent` handlers parse and are then skipped.

**`.agents/` is emerging as a vendor-neutral location.** Verified against an installed Codex 0.145.0 binary rather than documentation, because public docs are inconsistent on it: the binary carries `.agents/skills` as a repo-level skills root (error string `failed to stat repo skills root`), `.agents/plugins/marketplace.json`, `.agents/plugins/api_marketplace.json`, and enumerates `.agents` beside `.claude` and `.cursor` when detecting external agent configuration. The same binary **still** carries `.codex/skills` and `$CODEX_HOME/skills`. Both work today - SpecRoute records `.agents/skills/` as the convergence point to watch and does **not** recommend migrating off `.codex/skills` yet.

### Gemini CLI

```bash
cp -R runtimes/.gemini/ /path/to/your/repo/.gemini/
cd /path/to/your/repo/.gemini
mv settings.template.json           settings.json
# commands are TOML files under .gemini/commands/ — copy and edit the example(s)
```

Hooks landed in Gemini CLI v0.26.0; every release since consumes the full stack. Check `gemini --version` against the upstream changelog rather than trusting a pinned "current stable" number here - that field rots faster than anything else on this page.

- `settings.json` `mcpServers` (JSON object) **and** the `hooks` block (11 lifecycle events: `BeforeTool` / `AfterTool`, `BeforeAgent` / `AfterAgent`, `BeforeModel` / `AfterModel`, `BeforeToolSelection`, `SessionStart` / `SessionEnd`, `Notification`, `PreCompress`). Note these names are Gemini's own - they do **not** match Claude Code's or Codex's vocabulary.
- `.gemini/commands/*.toml` — custom commands (required `prompt`, optional `description`; subdirectories namespace as `/parent:child`). This replaces the old (never-real) `gemini_cli_config.json` map.
- `.gemini/skills/<slug>/SKILL.md` — Agent Skills (open standard), activated via the `activate_skill` tool.
- `.gemini/agents/<name>.md` — subagents (frontmatter `name`, `description`, `kind`, `tools`, `model`, …).
- `GEMINI.md` (delegation shim → `AGENTS.md`) and `rules/gemini-rules.md` document conventions.

> **Transition note:** On 2026-06-18 Google moved free and Google AI Pro / Ultra consumer access to Antigravity CLI. Paid Gemini Code Assist Standard / Enterprise and qualifying API-key users retain Gemini CLI access.

### Kiro

```bash
cp -R runtimes/.kiro/ /path/to/your/repo/.kiro/
```

Kiro consumes:

- `.kiro/steering/<name>.md` - rule files; `inclusion:` is one of `always`, `fileMatch` (+ `fileMatchPattern`), `manual` (referenced via `#name`), or `auto`.
- `.kiro/specs/<feature>/{requirements,design,tasks}.md` - the spec triplet (same shape as the framework-wide `specs/` triplet).
- `.kiro/hooks/<name>.json` - JSON hook configurations, root `"version": "v1"`. Shape, the 10 triggers, and the migration checklist off the dead `*.kiro.hook` format: [`hooks/kiro/README.md`](../hooks/kiro/README.md). Examples: [`hooks/kiro/examples/`](../hooks/kiro/examples/).
- `.kiro/settings/mcp.json` - MCP servers (`mcpServers` JSON; Kiro has had MCP since launch).
- `.kiro/skills/<slug>/SKILL.md` and `.kiro/agents/<name>.md` - Agent Skills and subagents.

Mirror your project's spec triplet content from `specs/examples/<feature>/` into `.kiro/specs/<feature>/` (or symlink, where supported).

> **Breaking change - Kiro IDE 1.0 (2026-06-25):** Kiro replaced `*.kiro.hook` with `.kiro/hooks/<name>.json`, moved to Claude-compatible trigger names, and swapped `askAgent` / `runCommand` for `action.type: "command"` or `"agent"`. Legacy files show an upgrade badge and do not execute until migrated. Any documentation that presents the 0.x format as current is stale.

### Cursor

```bash
cp -R runtimes/.cursor/ /path/to/your/repo/.cursor/
```

Cursor consumes far more than rules - earlier SpecRoute matrices understated it, and Skills, Subagents, Hooks and Plugins are all recent additions:

- `.cursor/rules/*.mdc` - Markdown with frontmatter (`description`, `globs`, `alwaysApply`); `AGENTS.md` is also natively read. **`.cursorrules` is gone** - removed from Cursor's documentation entirely and reported non-functional in current versions. Treat it as removed, not as legacy-but-supported, and migrate to `.cursor/rules/*.mdc`.
- `.cursor/mcp.json` - MCP servers (`mcpServers` JSON).
- `.cursor/skills/<slug>/SKILL.md` - Skills, the same open-standard shape as Claude Code and Codex.
- `.cursor/agents/<name>.md` - Subagents (since 2.4).
- `.cursor/commands/*.md` - custom slash commands (since 1.6).
- `.cursor/hooks.json` - lifecycle Hooks, `version: 1`. **21 events, camelCase** (`beforeShellExecution`, `afterFileEdit`, …) - Cursor's own vocabulary, not Claude's. Handler types are `command` and `prompt`. A hook exiting **2 denies** the action; hooks **fail open** on error unless the entry sets `failClosed: true`. Project, user, and enterprise paths all resolve.
- **Plugins / Marketplace** - Cursor now distributes rules, skills, and hooks as installable plugins.

For each rule file in `rules/`, create a corresponding `.mdc` in `.cursor/rules/`:

```yaml
---
description: <one-line>
alwaysApply: true       # or
globs: ["src/**/*.tsx"]  # for context-aware loading
---

(rule body - copy from rules/<topic>.md)
```

### Devin Desktop

```bash
cp -R runtimes/.devin/ /path/to/your/repo/.devin/
```

Devin Desktop's Devin Local agent uses `AGENTS.md`, skills under
`.devin/skills/`, experimental subagents under `.devin/agents/`,
`.devin/hooks.v1.json`, and `.devin/config.json`. Skills are the command
surface and are invoked as `/skill-name`.

The seven documented hook events are `PreToolUse`, `PostToolUse`,
`PermissionRequest`, `UserPromptSubmit`, `Stop`, `SessionStart`, and
`SessionEnd`; hook types are `command` and `prompt`.

Cascade remains available during the transition and still uses
`.windsurf/workflows/`, `.windsurf/hooks.json`, and
`~/.codeium/windsurf/mcp_config.json`. Those strings are compatibility paths
inside Devin Desktop, not a second SpecRoute vendor or runtime.

## MCP single source of truth

All six vendors consume MCP configs, in different shapes and paths - Claude Code `.mcp.json` (project) / `~/.claude.json` (user), Codex `[mcp_servers]` TOML, Gemini `.gemini/settings.json`, Kiro `.kiro/settings/mcp.json`, Cursor `.cursor/mcp.json`, and Devin Desktop `.devin/config.json`. Apart from Codex's TOML, every vendor uses the same `mcpServers` JSON object. The canonical source lives in [`runtimes/mcp/servers.yaml`](../runtimes/mcp/servers.yaml). Six renderers under [`runtimes/mcp/render/`](../runtimes/mcp/render/) emit one config per vendor:

```bash
python3 runtimes/mcp/render/render_claude.py   > runtimes/.claude/mcp.template.json
python3 runtimes/mcp/render/render_codex.py    > runtimes/.codex/config.template.toml
python3 runtimes/mcp/render/render_gemini.py   > runtimes/.gemini/settings.template.json
python3 runtimes/mcp/render/render_kiro.py     > runtimes/.kiro/settings/mcp.template.json
python3 runtimes/mcp/render/render_cursor.py   > runtimes/.cursor/mcp.template.json
python3 runtimes/mcp/render/render_devin.py    > runtimes/.devin/config.template.json
```

Cascade's compatibility MCP file accepts the same `mcpServers` object at
`~/.codeium/windsurf/mcp_config.json`, so it does not need a seventh renderer.
When you add or remove a server, edit `servers.yaml`, re-render, and commit the
project templates together.

> **Spec change in flight:** an MCP specification revision dated **2026-07-28** removes sessions and the `Mcp-Session-Id` header - the protocol goes stateless - and formally deprecates HTTP+SSE in favour of streamable HTTP. Treat this as imminent rather than shipped, and check the published revision date before relying on it. SpecRoute's `servers.yaml` schema is unaffected either way; only transport wiring changes.

## Cross-vendor sync

Claude Code and Codex share the folder-per-skill `SKILL.md` shape, so skills cross-mirror directly. Their **agents do not** share a format — Claude agents are flat Markdown, Codex agents are standalone TOML (`.codex/agents/<name>.toml`) — so `sync-skills.py` syncs skills only, not agents. To keep skills aligned:

```bash
python3 tools/sync-skills.py             # dry-run, reports drift
python3 tools/sync-skills.py --apply     # actually copy
python3 tools/sync-skills.py --source codex --apply   # reverse direction
```

The `/parity` command (in this repo's `.claude/commands/`) is the consumer-facing wrapper.

## Vendor capability convergence

Earlier SpecRoute releases sorted vendors into capability tiers (Full / Near-full / Partial / Specialized / Rules-only). **As of mid-2026 that tiering no longer holds** - every supported tool ships every capability class: the [Agent Skills open standard](https://agentskills.io) (`SKILL.md`), subagents, custom commands, lifecycle hooks, and MCP.

Two different claims used to share one table here, and conflating them is what produced the drift. They are separated below.

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

All six runtime layouts ship hook assets. Gemini differs in shape: its hooks
live under the `hooks` key inside `.gemini/settings.json`, so the layout ships a
merge snippet rather than a standalone file.

### What has actually converged

Vendors differ in **file format and conventions** - Codex agents are TOML where the others are Markdown; Gemini commands are TOML where Claude / Cursor are Markdown (Codex routes commands through skills); MCP config is JSON for most but TOML for Codex.

- **Skills: converged.** The `SKILL.md` shape is portable across all six with little more than a path change. This is the one near-total convergence, and it is the reason `tools/sync-skills.py` works at all.
- **Hooks: not converged.** Three vendors share an event vocabulary; three do not. See [Hook system depth](#hook-system-depth).
- **MCP: converged on the payload**, split on the container - one `mcpServers` JSON object everywhere except Codex's TOML.

Pick vendors based on what your team uses; the framework's **content** (PRDs, specs, prompts, rules) and **runtime-layer artifacts** (skills, agents, commands, hooks) land in any of them, each in its native shape.

## Adding a new vendor

The `add-vendor` skill walks through this:

1. Create `runtimes/.<vendor>/` with subdirs for what the vendor consumes.
2. Add a row to the matrix in all four mirrors: `README.md`, `AGENTS.md`, `wiki/Vendor-Matrix.md`, and this file.
3. Add `rules/<vendor>-rules.md` documenting the per-vendor format conventions.
4. Add an MCP renderer under `runtimes/mcp/render/` if the vendor consumes MCP.
5. Update `tools/sync-skills.py` if the vendor shares skill or agent shapes with Claude or Codex.
6. Update [`cross-vendor-sync.md`](cross-vendor-sync.md) if there's a sync target.

See [`.claude/skills/add-vendor/SKILL.md`](../.claude/skills/add-vendor/SKILL.md) for the interactive walkthrough.

## See also

- [`multi-vendor-context-files.md`](multi-vendor-context-files.md) - `AGENTS.md` + delegation-shim pattern.
- [`cross-vendor-sync.md`](cross-vendor-sync.md) - how `tools/sync-skills.py` and the MCP renderers maintain parity.
- [`runtimes/README.md`](../runtimes/README.md) - runtime layout overview.
- The per-runtime READMEs under [`runtimes/.<vendor>/README.md`](../runtimes/) - the most concrete setup steps.
