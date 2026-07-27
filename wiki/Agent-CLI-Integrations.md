# Agent CLI Integrations

<!-- sources: agentic-docs/agent-cli-integrations.md, runtimes/README.md -->

Concrete wiring for SpecRoute into each supported agent CLI. Copy commands per vendor.

For the canonical reference, see [`agentic-docs/agent-cli-integrations.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/agent-cli-integrations.md). For the supported matrix and the vendor notes intentionally kept out of the root README, see [[Vendor Matrix]].

## Claude Code

```bash
# 1. Drop the runtime layout
cp -R runtimes/.claude/ /path/to/your/repo/.claude/

# 2. Rename templates
cd /path/to/your/repo/.claude
mv settings.template.json              settings.json
mv settings.local.template.json        settings.local.json     # customize per-machine
mv mcp.template.json                   ../.mcp.json            # Claude Code CLI reads .mcp.json at repo root
mv hooks/hooks.template.json           hooks/hooks.json        # authoring artifact only - see step 3

# 3. Merge the hooks into settings.json - the file the CLI actually reads.
#    A bare project-level .claude/hooks/hooks.json is NOT a hook source.
/path/to/specroute/tools/sync-hooks-to-settings.sh \
  /path/to/your/repo/.claude/hooks/hooks.json \
  /path/to/your/repo/.claude/settings.json

# 4. Install hook scripts
cp /path/to/specroute/.claude/hooks/*.sh /path/to/your/repo/.claude/hooks/scripts/
chmod +x /path/to/your/repo/.claude/hooks/scripts/*.sh

# 5. Create the gitignored sanitization wordlist
touch /path/to/your/repo/.claude/.forbidden-strings.txt

# 6. Add to .gitignore
echo ".claude/settings.local.json"        >> /path/to/your/repo/.gitignore
echo ".claude/.forbidden-strings.txt"     >> /path/to/your/repo/.gitignore

# 7. Populate agents/, skills/, commands/ as your project requires.
```

**Claude Code reads hooks from** `settings.json` (user / project / local), managed policy settings, a **plugin's** `hooks/hooks.json`, and skill or agent frontmatter - **not** from a project-level `.claude/hooks/hooks.json`. SpecRoute keeps `hooks.json` as the annotated authoring artifact and syncs its `hooks` key into `settings.json`. Claude Code has 30 hook events and 5 handler types (`command`, `http`, `mcp_tool`, `prompt`, `agent`).

Per-runtime details: [`runtimes/.claude/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/runtimes/.claude/README.md).

## Codex

```bash
cp -R runtimes/.codex/ /path/to/your/repo/.codex/
cd /path/to/your/repo/.codex
mv config.template.toml config.toml

# Mirror skills from your Claude runtime (skills only - agent formats differ)
python3 /path/to/specroute/tools/sync-skills.py --source claude --apply
```

Codex consumes the **same** folder-per-skill `SKILL.md` shape as Claude Code, so skills cross-mirror directly. **Agents do not**: Codex agents are standalone TOML (`.codex/agents/<name>.toml` with `name`, `description`, `developer_instructions`) where Claude's are flat Markdown, which is why `sync-skills.py` syncs skills only. The `config.toml` carries Codex-specific MCP config and approval policy.

Codex hooks are enabled by default. The canonical feature key is `[features] hooks`; `codex_hooks` remains a deprecated alias. Its 11 events reuse Claude Code's names verbatim (`SessionStart`, `SessionEnd`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`), but the overlap is close, not total: no `PostToolUseFailure`, and only `type: "command"` handlers execute.

**`.agents/` is the emerging vendor-neutral location.** Verified against an installed Codex 0.145.0 binary, not documentation: it carries `.agents/skills` as a repo-level skills root plus `.agents/plugins/marketplace.json`. It **still** carries `.codex/skills` and `$CODEX_HOME/skills` too - both work today, so do not migrate off `.codex/skills` yet.

Per-runtime details: [`runtimes/.codex/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/runtimes/.codex/README.md).

## Gemini CLI

```bash
cp -R runtimes/.gemini/ /path/to/your/repo/.gemini/
cd /path/to/your/repo/.gemini
mv settings.template.json            settings.json
# commands are TOML files under .gemini/commands/ — copy and edit the example(s)
```

Hooks landed in Gemini CLI v0.26.0; every release since consumes the full stack. Check `gemini --version` against the upstream changelog rather than trusting a pinned "current stable" number here.

- `settings.json` `mcpServers` (JSON object) **and** the `hooks` block (11 lifecycle events: `BeforeTool` / `AfterTool`, `BeforeAgent` / `AfterAgent`, `BeforeModel` / `AfterModel`, `BeforeToolSelection`, `SessionStart` / `SessionEnd`, `Notification`, `PreCompress` - Gemini's own vocabulary, not Claude's).
- `.gemini/commands/*.toml` — custom commands (required `prompt`, optional `description`; subdirectories namespace as `/parent:child`). This replaces the old `gemini_cli_config.json` JSON command map.
- `.gemini/skills/<slug>/SKILL.md` — Agent Skills (open standard), activated via the `activate_skill` tool.
- `.gemini/agents/<name>.md` — subagents (frontmatter `name`, `description`, `kind`, `tools`, `model`, …).
- `GEMINI.md` (delegation shim → `AGENTS.md`) and `rules/gemini-rules.md` document conventions.

> **Transition note:** On 2026-06-18 Google moved free and Google AI Pro / Ultra consumer access to Antigravity CLI. Paid Gemini Code Assist Standard / Enterprise and qualifying API-key users retain Gemini CLI access.

Per-runtime details: [`runtimes/.gemini/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/runtimes/.gemini/README.md).

## Kiro

```bash
cp -R runtimes/.kiro/ /path/to/your/repo/.kiro/
```

Kiro consumes:

- `.kiro/steering/<name>.md` — rule files with `inclusion: always` or `inclusion: fileMatch` frontmatter.
- `.kiro/specs/<feature>/{requirements,design,tasks}.md` — the spec triplet (same shape as the framework-wide `specs/` triplet).
- `.kiro/hooks/<name>.json` - JSON hook configurations, root `"version": "v1"`.
- `.kiro/skills/<slug>/SKILL.md` and `.kiro/agents/<name>.md` - Agent Skills and subagents.
- `.kiro/settings/mcp.json` - MCP servers (`mcpServers` JSON).

Mirror your project's spec triplet content from `specs/<feature>/` into `.kiro/specs/<feature>/` (or symlink, where supported).

> **Breaking change - Kiro IDE 1.0 (2026-06-25):** Kiro replaced `*.kiro.hook` with `.kiro/hooks/<name>.json`, moved to ten Claude-compatible trigger names (`SessionStart`, `Stop`, `PreToolUse`, `PostToolUse`, `PreTaskExec`, `PostTaskExec`, `UserPromptSubmit`, `PostFileCreate`, `PostFileSave`, `PostFileDelete`), and swapped `askAgent` / `runCommand` for `action.type: "command"` or `"agent"`. `Manual` was retired; use a manual steering file. Legacy files show an upgrade badge and do not execute until migrated. Shape and migration checklist: [`hooks/kiro/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/hooks/kiro/README.md).

Per-runtime details: [`runtimes/.kiro/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/runtimes/.kiro/README.md).

## Cursor

```bash
cp -R runtimes/.cursor/ /path/to/your/repo/.cursor/
```

Cursor consumes far more than rules - earlier SpecRoute matrices understated it, and Skills, Subagents, Hooks and Plugins are all recent additions:

- `.cursor/rules/*.mdc` - Markdown with frontmatter (`description`, `globs`, `alwaysApply`); `AGENTS.md` is also natively read. **`.cursorrules` is gone** - removed from Cursor's documentation entirely and reported non-functional in current versions. Treat it as removed, not legacy-but-supported.
- `.cursor/mcp.json` — MCP servers (`mcpServers` JSON).
- `.cursor/skills/<slug>/SKILL.md` - Skills, the same open-standard shape as Claude Code and Codex.
- `.cursor/agents/<name>.md` - Subagents.
- `.cursor/commands/*.md` - custom slash commands.
- `.cursor/hooks.json` - lifecycle Hooks, `version: 1`. **21 events, camelCase** (`beforeShellExecution`, `afterFileEdit`, …), handler types `command` and `prompt`. Exit code **2 denies** the action; hooks **fail open** on error unless the entry sets `failClosed: true`.
- **Plugins / Marketplace** - Cursor distributes rules, skills, and hooks as installable plugins.

For each rule file in `rules/`, create a corresponding `.mdc` in `.cursor/rules/`:

```yaml
---
description: <one-line>
alwaysApply: true             # or
globs: ["src/**/*.tsx"]       # for context-aware loading
---

(rule body — copy from rules/<topic>.md)
```

Per-runtime details: [`runtimes/.cursor/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/runtimes/.cursor/README.md).

## Devin Desktop

```bash
cp -R runtimes/.devin/ /path/to/your/repo/.devin/
```

The runtime targets **Devin Local**, the next-generation agent harness shared
with Devin CLI and intended to become Devin Desktop's primary local agent:

- `AGENTS.md` — native root and nested project instructions.
- `.agents/skills/<name>/SKILL.md` (recommended) or
  `.devin/skills/<name>/SKILL.md` — reusable skills, invoked as
  `/skill-name`.
- `.devin/agents/<name>/AGENT.md` — experimental custom subagent profiles.
- `.devin/hooks.v1.json` — eight lifecycle events (`PreToolUse`,
  `PostToolUse`, `PermissionRequest`, `UserPromptSubmit`, `Stop`,
  `PostCompaction`, `SessionStart`, `SessionEnd`) with `command` and `prompt`
  handlers.
- `.devin/config.json` — project configuration, including the `mcpServers`
  object. Keep personal values in `.devin/config.local.json`.

Devin Desktop still includes Cascade during the transition. Cascade continues
to use `.windsurf/workflows/*.md`, `.windsurf/hooks.json`, and
`~/.codeium/windsurf/mcp_config.json`; `.windsurf/rules/` and
`.windsurf/skills/` remain accepted compatibility locations. These literal
paths are Devin Desktop compatibility namespaces, not a separate vendor or
runtime. Do not infer `.devin/workflows/`, `.devin/hooks.json`, or
`.devin/mcp.json`.

Per-runtime details: [`runtimes/.devin/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/runtimes/.devin/README.md).

## MCP single source of truth

All six vendors consume MCP configs, in different shapes and paths - Claude Code `.mcp.json` (project) / `~/.claude.json` (user), Codex `[mcp_servers]` TOML, Gemini `.gemini/settings.json`, Kiro `.kiro/settings/mcp.json`, Cursor `.cursor/mcp.json`, and Devin Desktop `.devin/config.json`. Apart from Codex's TOML, every vendor uses the same `mcpServers` JSON object. There are **six** renderers:

```bash
python3 runtimes/mcp/render/render_claude.py   > runtimes/.claude/mcp.template.json
python3 runtimes/mcp/render/render_codex.py    > runtimes/.codex/config.template.toml
python3 runtimes/mcp/render/render_gemini.py   > runtimes/.gemini/settings.template.json
python3 runtimes/mcp/render/render_kiro.py     > runtimes/.kiro/settings/mcp.template.json
python3 runtimes/mcp/render/render_cursor.py   > runtimes/.cursor/mcp.template.json
python3 runtimes/mcp/render/render_devin.py    > runtimes/.devin/config.template.json
```

Cascade's compatibility path
`~/.codeium/windsurf/mcp_config.json` accepts the same `mcpServers` object, so
the Devin renderer covers both destinations. Edit `runtimes/mcp/servers.yaml`,
re-render, and commit the canonical source and rendered files together so
reviewers see the impact in one diff. See [[MCP Integration]].

> **Spec change in flight:** as of 2026-07-27, the MCP revision dated **2026-07-28** is a release candidate, not a published specification. Re-check the final revision before changing transport wiring. SpecRoute's `servers.yaml` schema is unaffected.

> **Note:** `claude_desktop_config.json` is the **Claude Desktop app's** MCP file, not the Claude Code CLI's — the CLI reads `.mcp.json` / `~/.claude.json`.

## Cross-vendor sync

Skills share one shape across every vendor - that is the layer where cross-vendor convergence is near-total. `sync-skills.py` mirrors skill bodies across all six runtime layouts while preserving each vendor's native frontmatter; it deliberately excludes agents because their formats diverge. To keep skills aligned:

```bash
python3 tools/sync-skills.py             # dry-run, reports drift
python3 tools/sync-skills.py --apply     # actually copy
python3 tools/sync-skills.py --source codex --apply   # reverse direction
```

The `/parity` command (in this repo's `.claude/commands/`) is the consumer-facing wrapper. See [[Cross-Vendor Sync]].

## See also

- [[Vendor Matrix]] — what each vendor supports
- [[Multi-Vendor Context Files]] — `AGENTS.md` + delegation shims
- [[Adding a Vendor]] — the process for adding a new column
- [[MCP Integration]] — single source of truth for MCP server inventory
