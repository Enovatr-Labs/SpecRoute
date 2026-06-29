# Agent CLI Integrations

Concrete wiring for SpecRoute into each supported agent CLI. The matrix below is the contract - adding a new tool means a new column, not a fork.

## Supported vendor matrix

| Vendor | Runtime dir | Root context file | Skills | Agents | Commands | Hooks | MCP config |
|---|---|---|---|---|---|---|---|
| Claude Code | `.claude/` | `CLAUDE.md` | folder-per-skill `SKILL.md` + frontmatter | flat `<name>.md` + frontmatter (`name`, `description`, `model`, `color`) | `commands/<name>.md` + frontmatter (merged into skills) | `settings.json hooks` - ~30 events; 5 hook types (`command`, `http`, `mcp_tool`, `prompt`, `agent`); see [`hooks/claude/hooks.template.json`](../hooks/claude/hooks.template.json) | `.mcp.json` (project) / `~/.claude.json` (user) |
| Codex | `.codex/` | `AGENTS.md` | folder-per-skill `SKILL.md` (mirrors Claude) | `agents/<name>.toml` (`name`, `description`, `developer_instructions`) | skills, invoked `/skills` or `$mention` | `hooks.json` or inline `[hooks]` in `config.toml`; 10 events; Claude-compatible JSON; enabled by default (`[features] hooks`) | `config.toml [mcp_servers]` |
| Gemini CLI [^antigravity] | `.gemini/` | `GEMINI.md` (delegation shim) | `skills/<slug>/SKILL.md` | `agents/<name>.md` | TOML in `.gemini/commands/` (`prompt` + `description`) | `settings.json hooks` - 11 events (Before/AfterTool, Before/AfterAgent, Before/AfterModel, BeforeToolSelection, SessionStart/End, Notification, PreCompress); v0.26.0+ | `settings.json [mcpServers]` |
| Kiro | `.kiro/` | `steering/` files | `skills/<slug>/SKILL.md` | `agents/<name>.md` | `/skill` + `inclusion: manual` steering | `*.kiro.hook` JSON - 10 events (file create/save/delete, prompt submit, agent stop, pre/post tool, pre/post task, manual); actions `askAgent` / `runCommand` | `.kiro/settings/mcp.json` |
| Cursor | `.cursor/` | `.cursor/rules/*.mdc` / `AGENTS.md` | `.cursor/skills/` `SKILL.md` | `.cursor/agents/<name>.md` | `.cursor/commands/*.md` | `hooks.json` v1 - ~21 events with `permission` / `decision` schema; `command` and `prompt` hook types; project + user + enterprise paths | `.cursor/mcp.json` |
| Windsurf / Devin [^devin] | `.windsurf/` · `.devin/` | `.devin/rules/*.md` (pref) / `.windsurf/rules/` (legacy) | Cascade `SKILL.md` | subagents | `.windsurf/workflows/*.md` (`/workflow-name`) | `hooks.json` - 12 events (`pre_*`/`post_*` for read_code, write_code, run_command, mcp_tool_use, plus user_prompt, cascade_response, setup_worktree); only pre-hooks block | `~/.codeium/windsurf/mcp_config.json` |

[^antigravity]: Google began superseding the standalone Gemini CLI with **Antigravity CLI** on 2026-06-18 (free / Google-One tiers; paid retains access). The `.gemini/` shape here remains valid for current installs.
[^devin]: Windsurf was acquired by Cognition and is relaunching as **Devin Desktop** (`docs.devin.ai`); Cascade reaches EOL 2026-07-01 → Devin Local. `.devin/rules/` now takes precedence over legacy `.windsurf/rules/`.

This matrix appears in four places (`README.md`, `AGENTS.md`, `wiki/Vendor-Matrix.md`, this file) and must stay in lock-step. If you change one, update all. **As of mid-2026 all six tools have converged** on the same capability set — they differ in file format, not capability class (see [Capability convergence](#vendor-capability-convergence) below).

### Hook system depth

All six vendors ship hook systems; the per-vendor depth differs significantly:

| Vendor | Event count | Blocking semantics | Hook types beyond shell |
|---|---|---|---|
| Claude Code | ~30 | rich (per-event) | `http`, `mcp_tool`, `prompt`, `agent` |
| Codex | 10 | per-event JSON | `command` only |
| Gemini CLI | 11 | per-event | `command` only |
| Kiro | 10 | pre-hooks block | `askAgent`, `runCommand` |
| Cursor | ~21 | `permission` schema | `command`, `prompt` |
| Windsurf | 12 | pre-hooks only | `command`, `powershell` |

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
mv hooks/hooks.template.json         hooks/hooks.json

# 3. Install hook scripts (copy from this repo's .claude/hooks/ or write your own)
cp /path/to/specroute/.claude/hooks/*.sh /path/to/your/repo/.claude/hooks/scripts/
chmod +x /path/to/your/repo/.claude/hooks/scripts/*.sh

# 4. Create the gitignored sanitization wordlist
cat > /path/to/your/repo/.claude/.forbidden-strings.txt <<'EOF'
# One forbidden term per line
EOF

# 5. Add to .gitignore
echo ".claude/settings.local.json" >> /path/to/your/repo/.gitignore
echo ".claude/.forbidden-strings.txt" >> /path/to/your/repo/.gitignore

# 6. Populate agents/, skills/, commands/ as your project requires
```

### Codex

```bash
cp -R runtimes/.codex/ /path/to/your/repo/.codex/
cd /path/to/your/repo/.codex
mv config.template.toml config.toml

# Mirror skills from your Claude runtime (skills share the SKILL.md shape across both)
python3 /path/to/specroute/tools/sync-skills.py --source claude --apply
```

Codex consumes the same folder-per-skill `SKILL.md` shape as Claude Code, so skills cross-mirror directly. **Agents differ in format**: Codex agents are standalone TOML files (`.codex/agents/<name>.toml` with `name`, `description`, `developer_instructions`), not Claude's flat Markdown — `sync-skills.py` therefore syncs skills only, not agents. Hooks are **enabled by default** (the `codex_hooks` feature flag was renamed `hooks` and is on); the `config.toml` carries Codex-specific MCP config and approval policy.

### Gemini CLI

```bash
cp -R runtimes/.gemini/ /path/to/your/repo/.gemini/
cd /path/to/your/repo/.gemini
mv settings.template.json           settings.json
# commands are TOML files under .gemini/commands/ — copy and edit the example(s)
```

As of v0.26.0 (current stable v0.45.0) Gemini CLI consumes the full stack:

- `settings.json` `mcpServers` (JSON object) **and** the `hooks` block (11 lifecycle events).
- `.gemini/commands/*.toml` — custom commands (required `prompt`, optional `description`; subdirectories namespace as `/parent:child`). This replaces the old (never-real) `gemini_cli_config.json` map.
- `.gemini/skills/<slug>/SKILL.md` — Agent Skills (open standard), activated via the `activate_skill` tool.
- `.gemini/agents/<name>.md` — subagents (frontmatter `name`, `description`, `kind`, `tools`, `model`, …).
- `GEMINI.md` (delegation shim → `AGENTS.md`) and `rules/gemini-rules.md` document conventions.

> **Transition note:** Google began superseding the standalone Gemini CLI with Antigravity CLI on 2026-06-18 for free / Google-One tiers (paid Gemini Code Assist / Enterprise retain access).

### Kiro

```bash
cp -R runtimes/.kiro/ /path/to/your/repo/.kiro/
```

Kiro consumes:

- `.kiro/steering/<name>.md` - rule files; `inclusion:` is one of `always`, `fileMatch` (+ `fileMatchPattern`), `manual` (referenced via `#name`), or `auto`.
- `.kiro/specs/<feature>/{requirements,design,tasks}.md` - the spec triplet (same shape as the framework-wide `specs/` triplet).
- `.kiro/hooks/<name>.kiro.hook` - JSON hook configurations (actions `askAgent` or `runCommand`).
- `.kiro/settings/mcp.json` - MCP servers (`mcpServers` JSON; Kiro has had MCP since launch).
- `.kiro/skills/<slug>/SKILL.md` and `.kiro/agents/<name>.md` - Agent Skills and subagents (since Kiro 0.9).

Mirror your project's spec triplet content from `specs/examples/<feature>/` into `.kiro/specs/<feature>/` (or symlink, where supported).

### Cursor

```bash
cp -R runtimes/.cursor/ /path/to/your/repo/.cursor/
```

Cursor consumes (far more than rules — earlier SpecRoute matrices understated it):

- `.cursor/rules/*.mdc` - Markdown with frontmatter (`description`, `globs`, `alwaysApply`); `AGENTS.md` is also natively read. `.cursorrules` at the repo root is legacy/deprecated.
- `.cursor/mcp.json` - MCP servers (`mcpServers` JSON).
- `.cursor/agents/<name>.md` - subagents (since 2.4); `.cursor/skills/` `SKILL.md`; `.cursor/commands/*.md` - custom slash commands (since 1.6).
- `.cursor/hooks.json` - lifecycle hooks (`version: 1`).

For each rule file in `rules/`, create a corresponding `.mdc` in `.cursor/rules/`:

```yaml
---
description: <one-line>
alwaysApply: true       # or
globs: ["src/**/*.tsx"]  # for context-aware loading
---

(rule body - copy from rules/<topic>.md)
```

### Windsurf

```bash
cp -R runtimes/.windsurf/ /path/to/your/repo/.windsurf/
```

Windsurf consumes `.windsurf/rules/*.md` with frontmatter similar to Cursor's. Use `trigger: always_on` for cross-cutting rules, `trigger: model-decision` with `globs` for context-aware rules. Beyond rules it also reads `.windsurf/workflows/*.md` (invoked as `/workflow-name`), Cascade `SKILL.md` skills, subagents, `hooks.json` lifecycle hooks, and MCP servers at `~/.codeium/windsurf/mcp_config.json`.

> **Transition note:** Windsurf was acquired by Cognition and relaunched as **Devin Desktop** (June 2026; docs at `docs.devin.ai`). The Cascade local agent reaches EOL on 2026-07-01, succeeded by Devin Local (a Rust rewrite with subagent support). `.devin/rules/*.md` now takes precedence over the legacy `.windsurf/rules/`; the layouts are otherwise compatible.

## MCP single source of truth

All six vendors consume MCP configs, in different shapes and paths — Claude Code `.mcp.json` (project) / `~/.claude.json` (user), Codex `[mcp_servers]` TOML, Gemini `.gemini/settings.json`, Kiro `.kiro/settings/mcp.json`, Cursor `.cursor/mcp.json`, Windsurf/Devin `~/.codeium/windsurf/mcp_config.json`. Apart from Codex's TOML, every vendor uses the same `mcpServers` JSON object. The canonical source lives in [`runtimes/mcp/servers.yaml`](../runtimes/mcp/servers.yaml). Renderers under [`runtimes/mcp/render/`](../runtimes/mcp/render/) emit per-vendor configs:

```bash
python3 runtimes/mcp/render/render_claude.py > runtimes/.claude/mcp.template.json
python3 runtimes/mcp/render/render_codex.py  > runtimes/.codex/config.template.toml
python3 runtimes/mcp/render/render_gemini.py > runtimes/.gemini/settings.template.json
```

The remaining JSON-shaped vendors (Kiro, Cursor, Windsurf/Devin) reuse the same `mcpServers` object the Claude renderer emits — drop it into their respective paths. When you add or remove an MCP server: edit `servers.yaml`, re-render, and commit the rendered files together so reviewers see the impact in one diff.

## Cross-vendor sync

Claude Code and Codex share the folder-per-skill `SKILL.md` shape, so skills cross-mirror directly. Their **agents do not** share a format — Claude agents are flat Markdown, Codex agents are standalone TOML (`.codex/agents/<name>.toml`) — so `sync-skills.py` syncs skills only, not agents. To keep skills aligned:

```bash
python3 tools/sync-skills.py             # dry-run, reports drift
python3 tools/sync-skills.py --apply     # actually copy
python3 tools/sync-skills.py --source codex --apply   # reverse direction
```

The `/parity` command (in this repo's `.claude/commands/`) is the consumer-facing wrapper.

## Vendor capability convergence

Earlier SpecRoute releases sorted vendors into capability tiers (Full / Near-full / Partial / Specialized / Rules-only). **As of mid-2026 that distinction no longer holds.** All six supported tools have converged on a common capability set — the [Agent Skills open standard](https://agentskills.io) (`SKILL.md`), subagents, custom commands, lifecycle hooks, and MCP:

| Vendor | Skills | Agents | Commands | Hooks | MCP |
|---|:--:|:--:|:--:|:--:|:--:|
| Claude Code | ✅ | ✅ | ✅ | ✅ | ✅ |
| Codex | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini CLI | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kiro | ✅ | ✅ | ✅ | ✅ | ✅ |
| Cursor | ✅ | ✅ | ✅ | ✅ | ✅ |
| Windsurf / Devin | ✅ | ✅ | ✅ | ✅ | ✅ |

Vendors now differ in **file format and conventions**, not capability class — Codex agents are TOML where the others are Markdown; Gemini commands are TOML where Claude/Cursor are Markdown (Codex routes commands through skills); MCP config is JSON for most but TOML for Codex. Pick vendors based on what your team uses; the framework's **content** (PRDs, specs, prompts, rules) and **runtime-layer artifacts** (skills, agents, commands, hooks) now land in any of them, each in its native shape.

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
