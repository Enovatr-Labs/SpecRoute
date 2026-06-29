# Agent CLI Integrations

<!-- sources: agentic-docs/agent-cli-integrations.md, runtimes/README.md -->

Concrete wiring for SpecRoute into each supported agent CLI. Copy commands per vendor.

For the canonical reference, see [`agentic-docs/agent-cli-integrations.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/agent-cli-integrations.md). For the supported matrix, see [[Vendor Matrix]].

## Claude Code

```bash
# 1. Drop the runtime layout
cp -R runtimes/.claude/ /path/to/your/repo/.claude/

# 2. Rename templates
cd /path/to/your/repo/.claude
mv settings.template.json              settings.json
mv settings.local.template.json        settings.local.json     # customize per-machine
mv mcp.template.json                   ../.mcp.json            # Claude Code CLI reads .mcp.json at repo root
mv hooks/hooks.template.json           hooks/hooks.json

# 3. Install hook scripts
cp /path/to/specroute/.claude/hooks/*.sh /path/to/your/repo/.claude/hooks/scripts/
chmod +x /path/to/your/repo/.claude/hooks/scripts/*.sh

# 4. Create the gitignored sanitization wordlist
touch /path/to/your/repo/.claude/.forbidden-strings.txt

# 5. Add to .gitignore
echo ".claude/settings.local.json"        >> /path/to/your/repo/.gitignore
echo ".claude/.forbidden-strings.txt"     >> /path/to/your/repo/.gitignore

# 6. Populate agents/, skills/, commands/ as your project requires.
```

Per-runtime details: [`runtimes/.claude/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/runtimes/.claude/README.md).

## Codex

```bash
cp -R runtimes/.codex/ /path/to/your/repo/.codex/
cd /path/to/your/repo/.codex
mv config.template.toml config.toml

# Mirror skills and agents from your Claude runtime
python3 /path/to/specroute/tools/sync-skills.py --source claude --apply
```

Codex consumes the **same** `<name>.md` agent shape and the **same** folder-per-skill `SKILL.md` shape as Claude Code, so most content cross-mirrors. The `config.toml` carries Codex-specific MCP config and approval policy.

Codex hooks are **enabled by default** (the `codex_hooks` feature flag was renamed `hooks` and is on).

Per-runtime details: [`runtimes/.codex/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/runtimes/.codex/README.md).

## Gemini CLI

```bash
cp -R runtimes/.gemini/ /path/to/your/repo/.gemini/
cd /path/to/your/repo/.gemini
mv settings.template.json            settings.json
# commands are TOML files under .gemini/commands/ — copy and edit the example(s)
```

As of v0.26.0 (current stable v0.45.0) Gemini CLI consumes the full stack:

- `settings.json` `mcpServers` (JSON object) **and** the `hooks` block (11 lifecycle events).
- `.gemini/commands/*.toml` — custom commands (required `prompt`, optional `description`; subdirectories namespace as `/parent:child`). This replaces the old `gemini_cli_config.json` JSON command map.
- `.gemini/skills/<slug>/SKILL.md` — Agent Skills (open standard), activated via the `activate_skill` tool.
- `.gemini/agents/<name>.md` — subagents (frontmatter `name`, `description`, `kind`, `tools`, `model`, …).
- `GEMINI.md` (delegation shim → `AGENTS.md`) and `rules/gemini-rules.md` document conventions.

> **Transition note:** Google began superseding the standalone Gemini CLI with Antigravity CLI on 2026-06-18 for free / Google-One tiers (paid Gemini Code Assist / Enterprise retain access).

Per-runtime details: [`runtimes/.gemini/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/runtimes/.gemini/README.md).

## Kiro

```bash
cp -R runtimes/.kiro/ /path/to/your/repo/.kiro/
```

Kiro consumes:

- `.kiro/steering/<name>.md` — rule files with `inclusion: always` or `inclusion: fileMatch` frontmatter.
- `.kiro/specs/<feature>/{requirements,design,tasks}.md` — the spec triplet (same shape as the framework-wide `specs/` triplet).
- `.kiro/hooks/<name>.kiro.hook` — JSON hook configurations.

Mirror your project's spec triplet content from `specs/<feature>/` into `.kiro/specs/<feature>/` (or symlink, where supported).

Per-runtime details: [`runtimes/.kiro/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/runtimes/.kiro/README.md).

## Cursor

```bash
cp -R runtimes/.cursor/ /path/to/your/repo/.cursor/
```

Cursor consumes (far more than rules — earlier SpecRoute matrices understated it):

- `.cursor/rules/*.mdc` — Markdown with frontmatter (`description`, `globs`, `alwaysApply`); `AGENTS.md` is also natively read. `.cursorrules` at the repo root is legacy/deprecated.
- `.cursor/mcp.json` — MCP servers (`mcpServers` JSON).
- `.cursor/agents/<name>.md` — subagents; `.cursor/skills/` `SKILL.md`; `.cursor/commands/*.md` — custom slash commands.
- `.cursor/hooks.json` — lifecycle hooks (`version: 1`).

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

## Windsurf

```bash
cp -R runtimes/.windsurf/ /path/to/your/repo/.windsurf/
```

Windsurf consumes `.windsurf/rules/*.md` with frontmatter similar to Cursor's. Use `trigger: always_on` for cross-cutting rules, `trigger: model-decision` with `globs` for context-aware rules. Beyond rules it also reads `.windsurf/workflows/*.md` (invoked as `/workflow-name`), Cascade `SKILL.md` skills, subagents, `hooks.json` lifecycle hooks, and MCP servers at `~/.codeium/windsurf/mcp_config.json`.

> **Transition note:** Windsurf was acquired by Cognition and relaunched as **Devin Desktop** (June 2026; docs at `docs.devin.ai`). The Cascade local agent reaches EOL on 2026-07-01, succeeded by Devin Local. `.devin/rules/*.md` now takes precedence over the legacy `.windsurf/rules/`; the layouts are otherwise compatible.

Per-runtime details: [`runtimes/.windsurf/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/runtimes/.windsurf/README.md).

## MCP single source of truth

All six vendors consume MCP configs, in different shapes and paths — Claude Code `.mcp.json` (project) / `~/.claude.json` (user), Codex `[mcp_servers]` TOML, Gemini `.gemini/settings.json`, Kiro `.kiro/settings/mcp.json`, Cursor `.cursor/mcp.json`, Windsurf/Devin `~/.codeium/windsurf/mcp_config.json`. Apart from Codex's TOML, every vendor uses the same `mcpServers` JSON object. There are six renderers — render `claude` / `codex` / `gemini` / `kiro` / `cursor` / `windsurf`:

```bash
python3 runtimes/mcp/render/render_claude.py  > runtimes/.claude/mcp.template.json
python3 runtimes/mcp/render/render_codex.py   > runtimes/.codex/config.template.toml
python3 runtimes/mcp/render/render_gemini.py  > runtimes/.gemini/settings.template.json
python3 runtimes/mcp/render/render_kiro.py    > runtimes/.kiro/settings/mcp.template.json
python3 runtimes/mcp/render/render_cursor.py  > runtimes/.cursor/mcp.template.json
python3 runtimes/mcp/render/render_windsurf.py > runtimes/.windsurf/mcp_config.template.json
```

Edit `runtimes/mcp/servers.yaml` and re-render. Commit the canonical source and the rendered files together so reviewers see the impact in one diff. See [[MCP Integration]].

> **Note:** `claude_desktop_config.json` is the **Claude Desktop app's** MCP file, not the Claude Code CLI's — the CLI reads `.mcp.json` / `~/.claude.json`.

## Cross-vendor sync

Two vendors share artifact shapes (Claude / Codex). To keep them aligned:

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
