# Cross-Vendor Sync

<!-- sources: agentic-docs/cross-vendor-sync.md, tools/README.md -->

How a SpecForge-driven project keeps the artifacts that several vendors consume in lock-step. This is the maintainability story for multi-vendor support.

For the canonical reference, see [`agentic-docs/cross-vendor-sync.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/agentic-docs/cross-vendor-sync.md).

## What needs to stay synced

| Artifact | Vendors | Shape |
|---|---|---|
| **Agents** | Claude Code, Codex | Flat `<name>.md` with frontmatter (`name`, `description`, `model`, `color`) |
| **Skills** | Claude Code, Codex | Folder-per-skill `SKILL.md` with frontmatter |
| **MCP server inventory** | Claude Desktop, Codex, Gemini CLI | Different shapes; see [[MCP Integration]] |
| **Engineering rules** | All vendors | Markdown body; per-vendor frontmatter (Cursor MDC, Kiro inclusion, etc.) |
| **Prompts** | Any vendor reading markdown | No vendor-specific shape; copy-paste-friendly |
| **Specs** | All vendors (read by humans + agents) | Same in every vendor |

**Not synced**: vendor-specific config files (`.claude/settings.json`, `.codex/config.toml`, `.gemini/gemini_cli_config.json`) and vendor-specific runtime layouts.

## Tools that maintain sync

### `tools/sync-skills.py` — agents + skills

Claude Code and Codex consume the same agent and skill shapes:

```
runtimes/.claude/agents/<name>.md
runtimes/.codex/agents/<name>.md          ← should mirror

runtimes/.claude/skills/<slug>/SKILL.md
runtimes/.codex/skills/<slug>/SKILL.md    ← should mirror
```

Usage:

```bash
# Read-only report
python3 tools/sync-skills.py

# Apply: copy missing or drifted items from source to target
python3 tools/sync-skills.py --apply

# Reverse direction
python3 tools/sync-skills.py --source codex --apply
```

Output categorizes drift as:

- **MISSING** — exists in source but not target.
- **EXTRA** — exists in target but not source. (**Never auto-removed**; you decide whether it's intentional.)
- **DRIFT** — exists in both with different content.

When drift is intentional (a skill that uses Claude's `Task` tool has no Codex equivalent), document it in `runtimes/README.md` so future audits don't regenerate it.

### `runtimes/mcp/render/` — MCP server configs

Render from one canonical YAML to per-vendor shapes. See [[MCP Integration]] for the full workflow.

### `/parity` command — quick check

The `/parity` slash command runs both checks (skills/agents and MCP source-of-truth alignment) and reports drift without writing. Use as a pre-commit gate.

## Sync cadence

When to run sync tools:

- **Before every commit** that touches `runtimes/.claude/` or `runtimes/.codex/` — confirm the change applied to both, or that the asymmetry is intentional.
- **After editing `runtimes/mcp/servers.yaml`** — re-render and commit.
- **Pre-PR** — `/parity` as part of `/audit`.
- **Periodically** — even without active changes, run `tools/sync-skills.py` weekly. Drift sneaks in via merge conflicts.

## When parity should NOT be the goal

Some artifacts genuinely belong to only one vendor:

- A skill using Claude's `Task` tool delegation has no Codex equivalent.
- A Gemini command that's just a shell shortcut is JSON-only and doesn't apply to other vendors.
- A Claude hook script's behavior depends on the Claude Code hook protocol; Kiro's hooks have different protocols.

Document these asymmetries explicitly in `runtimes/README.md` so audits don't regenerate them:

> **Claude-only skills** (intentional, will not mirror to Codex):
> - `<skill-slug>` — uses Claude's `Task` tool for sub-agent delegation; no Codex equivalent.

## Anti-patterns

- **Editing per-vendor configs by hand when a renderer exists** — your edits will be lost on the next render.
- **Per-vendor `servers.yaml` files** — defeats the single-source purpose.
- **Inconsistent skill names across vendors** — a skill called `audit-changes` in Claude and `audit-diff` in Codex is two skills, not one.
- **Frontmatter drift** — a skill with `model: opus` in Claude and `model: sonnet` in Codex is silently wrong. Run sync.
- **Skipping sync because "the diff is small"** — small drift compounds; the small change today is the merge conflict next quarter.

## Adding a new sync target

A new vendor that consumes shapes other vendors also consume gets an entry in the sync tool:

1. **For agents** — extend `tools/sync-skills.py` to include the new vendor's agents directory in the diff/copy logic.
2. **For skills** — same.
3. **For MCP** — add a renderer under `runtimes/mcp/render/`.

See [[Adding a Vendor]] for the broader walkthrough.

## Owner agent

Cross-vendor sync utilities are owned by the `runtime-architect` agent.

## See also

- [[Agent CLI Integrations]] — concrete vendor wiring
- [[Multi-Vendor Context Files]] — root context-file pattern
- [[MCP Integration]] — MCP renderers in detail
- [[Vendor Matrix]] — the supported-CLI contract
