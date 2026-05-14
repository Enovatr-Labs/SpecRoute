# Cross-Vendor Sync

How a SpecRoute-driven project keeps the artifacts that several vendors consume in lock-step. This is the maintainability story for multi-vendor support.

## What needs to stay synced

| Artifact | Vendors | Shape |
|---|---|---|
| **Agents** | Claude Code, Codex | Flat `<name>.md` with frontmatter (`name`, `description`, `model`, `color`) |
| **Skills** | Claude Code, Codex | Folder-per-skill `SKILL.md` with frontmatter |
| **MCP server inventory** | Claude Desktop, Codex, Gemini CLI | Different shapes; see "MCP rendering" below |
| **Engineering rules** | All vendors | Markdown body; per-vendor frontmatter (Cursor MDC, Kiro inclusion, etc.) |
| **Prompts** | Any vendor that reads markdown | No vendor-specific shape; copy-paste-friendly |
| **Specs** | All vendors (read by humans + agents) | Markdown; same in every vendor |

Things that don't need syncing: vendor-specific config files (`.claude/settings.json`, `.codex/config.toml`, `.gemini/gemini_cli_config.json`) and vendor-specific runtime layouts.

## Tools that maintain sync

### `tools/sync-skills.py` - agents + skills

Two vendors (Claude Code and Codex) consume the same agent and skill shapes. They live in two parallel directories:

```
runtimes/.claude/agents/<name>.md
runtimes/.codex/agents/<name>.md          ← should mirror

runtimes/.claude/skills/<slug>/SKILL.md
runtimes/.codex/skills/<slug>/SKILL.md    ← should mirror
```

`tools/sync-skills.py` diffs and copies between them:

```bash
# Read-only report
python3 tools/sync-skills.py

# Apply: copy missing or drifted items from source to target
python3 tools/sync-skills.py --apply

# Reverse direction
python3 tools/sync-skills.py --source codex --apply
```

Output categorizes drift as:

- **MISSING** - exists in source but not target.
- **EXTRA** - exists in target but not source. (Never auto-removed; you decide if it's intentional.)
- **DRIFT** - exists in both with different content.

When drift is intentional (a skill that uses Claude's `Task` tool has no Codex equivalent), document it in `runtimes/README.md` so future audits don't regenerate it.

### `runtimes/mcp/render/` - MCP server configs

Three vendors consume MCP configs in different shapes:

| Vendor | Shape | Path |
|---|---|---|
| Claude Desktop | `mcpServers` JSON object | `.claude/claude_desktop_config.json` |
| Codex | `[mcp_servers.<name>]` TOML sections | `.codex/config.toml` |
| Gemini CLI | `mcpServers` JSON object | `.gemini/settings.json` |

Maintaining three files by hand is the failure mode. The canonical inventory lives in [`runtimes/mcp/servers.yaml`](../runtimes/mcp/servers.yaml); renderers emit each vendor's shape:

```bash
python3 runtimes/mcp/render/render_claude.py > runtimes/.claude/claude_desktop_config.template.json
python3 runtimes/mcp/render/render_codex.py  > runtimes/.codex/config.template.toml
python3 runtimes/mcp/render/render_gemini.py > runtimes/.gemini/settings.template.json
```

Workflow when adding a server:

1. Edit `servers.yaml`.
2. Re-run all three renderers.
3. Commit `servers.yaml` + the three rendered files in one commit.

This is an architectural choice with a maintenance benefit: source of truth is one file, divergence is impossible.

### `/parity` command - quick check

The `/parity` slash command runs both checks (skills/agents and MCP source-of-truth alignment) and reports drift without writing. Use as a pre-commit gate.

## Sync cadence

When to run sync tools:

- **Before every commit that touches `runtimes/.claude/` or `runtimes/.codex/`** - confirm the change applied to both, or that the asymmetry is intentional.
- **After editing `runtimes/mcp/servers.yaml`** - re-render and commit.
- **Pre-PR** - `/parity` as part of `/audit`.
- **Periodically** - even without active changes, run `tools/sync-skills.py` weekly. Drift can sneak in via merge conflicts.

## When vendor parity should NOT be the goal

Some artifacts genuinely belong to only one vendor:

- A skill that uses Claude's `Task` tool delegation has no Codex equivalent.
- A Gemini command that's just a shell shortcut is JSON-only and doesn't apply to other vendors.
- A Claude hook script's behavior depends on the Claude Code hook protocol; Kiro's hooks have different protocols.

Document these asymmetries explicitly in `runtimes/README.md` so audits don't regenerate them. The form is:

> **Claude-only skills** (intentional, will not mirror to Codex):
> - `<skill-slug>` - uses Claude's `Task` tool for sub-agent delegation; no Codex equivalent.

## Anti-patterns

- **Editing per-vendor configs by hand when a renderer exists.** They're regenerated on the next render; your edits will be lost.
- **Per-vendor `servers.yaml` files.** That defeats the single-source purpose.
- **Inconsistent skill names across vendors.** A skill called `audit-changes` in Claude and `audit-diff` in Codex is two skills, not one.
- **Frontmatter drift.** A skill with `model: opus` in Claude and `model: sonnet` in Codex is silently wrong. Run sync.
- **Skipping sync because "the diff is small."** Small drift compounds; the small change today is the merge conflict next quarter.

## Adding a new sync target

A new vendor that consumes shapes other vendors also consume gets an entry in the sync tool:

1. **For agents**: extend `tools/sync-skills.py` to include the new vendor's agents directory in the diff/copy logic.
2. **For skills**: same.
3. **For MCP**: add a renderer under `runtimes/mcp/render/`.

See [`agent-cli-integrations.md`](agent-cli-integrations.md) for the broader "add a new vendor" walkthrough.

## Authoring agent

Cross-vendor sync utilities are owned by the `runtime-architect` agent. See [`.claude/agents/runtime-architect.md`](../.claude/agents/runtime-architect.md).

## See also

- [`agent-cli-integrations.md`](agent-cli-integrations.md) - concrete vendor wiring.
- [`multi-vendor-context-files.md`](multi-vendor-context-files.md) - root context-file pattern.
- [`tools/sync-skills.py`](../tools/sync-skills.py) - the sync tool itself.
- [`runtimes/mcp/`](../runtimes/mcp/) - MCP single source of truth and renderers.
