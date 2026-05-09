# Agent CLI Integrations

Concrete wiring for SpecForge into each supported agent CLI. The matrix below is the contract - adding a new tool means a new column, not a fork.

## Supported vendor matrix

| Vendor | Runtime dir | Root context file | Skills | Agents | Commands | Hooks | MCP config |
|---|---|---|---|---|---|---|---|
| Claude Code | `.claude/` | `CLAUDE.md` | folder-per-skill `SKILL.md` + frontmatter | flat `<name>.md` + frontmatter (`name`, `description`, `model`, `color`) | `commands/<name>.md` + frontmatter | `settings.json hooks` - ~27 events; 5 hook types (`command`, `http`, `mcp_tool`, `prompt`, `agent`); see [`hooks/claude/hooks.template.json`](../hooks/claude/hooks.template.json) | `claude_desktop_config.json` |
| Codex | `.codex/` | `AGENTS.md` | folder-per-skill `SKILL.md` (mirrors Claude) | flat `<name>.md` | (via skills with `user-invocable: true`) | `hooks.json` or inline `[hooks]` in `config.toml`; 6 events; Claude-compatible JSON; requires `[features] codex_hooks = true` | `config.toml [mcp_servers]` |
| Gemini CLI | `.gemini/` | `GEMINI.md` (delegation shim) | - | - | `gemini_cli_config.json` JSON command map | `settings.json hooks` - 11 events (Before/AfterTool, Before/AfterAgent, Before/AfterModel, BeforeToolSelection, SessionStart/End, Notification, PreCompress); v0.26.0+ | `settings.json [mcpServers]` |
| Kiro | `.kiro/` | `steering/` files | - | - | - | `*.kiro.hook` JSON - 10 events (file create/save/delete, prompt submit, agent stop, pre/post tool, pre/post task, manual) | - |
| Cursor | `.cursor/rules/` | `.cursorrules` | - | - | - | `hooks.json` v1 - ~19 events with `permission` / `decision` schema; `command` and `prompt` hook types; project + user + enterprise paths | - |
| Windsurf | `.windsurf/rules/` | - | - | - | - | `hooks.json` - 12 events (`pre_*`/`post_*` for read_code, write_code, run_command, mcp_tool_use, plus user_prompt, cascade_response, setup_worktree); only pre-hooks block | - |

This matrix appears in three places (`README.md`, `AGENTS.md`, this file) and must stay in lock-step. If you change one, update all three.

### Hook system depth

All six vendors ship hook systems; the per-vendor depth differs significantly:

| Vendor | Event count | Blocking semantics | Hook types beyond shell |
|---|---|---|---|
| Claude Code | ~27 | rich (per-event) | `http`, `mcp_tool`, `prompt`, `agent` |
| Codex | 6 | per-event JSON | `command` only |
| Gemini CLI | 11 | per-event | `command` only |
| Kiro | 10 | pre-hooks block | `askAgent` (built-in) |
| Cursor | ~19 | `permission` schema | `command`, `prompt` |
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
mv claude_desktop_config.template.json claude_desktop_config.json
mv hooks/hooks.template.json         hooks/hooks.json

# 3. Install hook scripts (copy from this repo's .claude/hooks/ or write your own)
cp /path/to/specforge/.claude/hooks/*.sh /path/to/your/repo/.claude/hooks/scripts/
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

# Mirror skills and agents from your Claude runtime
python3 /path/to/specforge/tools/sync-skills.py --source claude --apply
```

Codex consumes the same `<name>.md` agent shape and the same folder-per-skill `SKILL.md` shape as Claude Code, so most content cross-mirrors. The `config.toml` carries Codex-specific MCP config and approval policy.

### Gemini CLI

```bash
cp -R runtimes/.gemini/ /path/to/your/repo/.gemini/
cd /path/to/your/repo/.gemini
mv settings.template.json           settings.json
mv gemini_cli_config.template.json  gemini_cli_config.json
```

Gemini consumes:

- `settings.json` `mcpServers` (same shape as Claude Desktop's MCP config).
- `gemini_cli_config.json` `commands` (JSON map of shell shortcuts).

It does **not** consume skills, agents, or hooks. To work in Gemini, project conventions surface through:

- `GEMINI.md` (delegation shim → `AGENTS.md`).
- The shared `prompts/` directory (Gemini reads markdown prompts you paste into the conversation).
- `rules/gemini-rules.md` documents what's available.

### Kiro

```bash
cp -R runtimes/.kiro/ /path/to/your/repo/.kiro/
```

Kiro consumes:

- `.kiro/steering/<name>.md` - rule files with `inclusion: always` or `inclusion: fileMatch` frontmatter.
- `.kiro/specs/<feature>/{requirements,design,tasks}.md` - the spec triplet (same shape as the framework-wide `specs/` triplet).
- `.kiro/hooks/<name>.kiro.hook` - JSON hook configurations.

Mirror your project's spec triplet content from `specs/examples/<feature>/` into `.kiro/specs/<feature>/` (or symlink, where supported).

### Cursor

```bash
cp -R runtimes/.cursor/ /path/to/your/repo/.cursor/
```

Cursor consumes:

- `.cursor/rules/*.mdc` - Markdown with frontmatter (`description`, `globs`, `alwaysApply`).
- (legacy) `.cursorrules` at the repo root.

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

Windsurf consumes `.windsurf/rules/*.md` with frontmatter similar to Cursor's. Use `trigger: always` for cross-cutting rules, `trigger: model-decision` with `globs` for context-aware rules.

## MCP single source of truth

Three vendors consume MCP configs in different shapes (Claude Desktop JSON, Codex TOML, Gemini JSON). The canonical source lives in [`runtimes/mcp/servers.yaml`](../runtimes/mcp/servers.yaml). Renderers under [`runtimes/mcp/render/`](../runtimes/mcp/render/) emit per-vendor configs:

```bash
python3 runtimes/mcp/render/render_claude.py > runtimes/.claude/claude_desktop_config.template.json
python3 runtimes/mcp/render/render_codex.py  > runtimes/.codex/config.template.toml
python3 runtimes/mcp/render/render_gemini.py > runtimes/.gemini/settings.template.json
```

When you add or remove an MCP server: edit `servers.yaml`, re-render, commit all four files together so reviewers see the impact in one diff.

## Cross-vendor sync

Two vendors share artifact shapes (Claude Code and Codex agents + skills). To keep them aligned:

```bash
python3 tools/sync-skills.py             # dry-run, reports drift
python3 tools/sync-skills.py --apply     # actually copy
python3 tools/sync-skills.py --source codex --apply   # reverse direction
```

The `/parity` command (in this repo's `.claude/commands/`) is the consumer-facing wrapper.

## Vendor support tiers

| Tier | Vendors | What's supported |
|---|---|---|
| **Full** | Claude Code | Skills, agents, commands, hooks, MCP, root context file, sub-agent delegation |
| **Near-full** | Codex | Skills, agents, MCP, root context file (commands subsumed into skills via `user-invocable`) |
| **Partial** | Gemini CLI | MCP, command map, root context file |
| **Specialized** | Kiro | Steering rules, spec triplet, file-pattern hooks |
| **Rules only** | Cursor, Windsurf | Rule files |

Pick vendors based on what your team uses. The framework's content (PRDs, specs, prompts, rules) works in any of them; the runtime-layer features (skills, agents, commands, hooks) only land where the vendor supports them.

## Adding a new vendor

The `add-vendor` skill walks through this:

1. Create `runtimes/.<vendor>/` with subdirs for what the vendor consumes.
2. Add a row to the matrix in `README.md`, `AGENTS.md`, and this file.
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
