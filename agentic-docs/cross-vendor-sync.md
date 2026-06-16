# Cross-Vendor Sync

How a SpecRoute-driven project keeps the artifacts that several vendors consume in lock-step. This is the maintainability story for multi-vendor support.

## What needs to stay synced

| Artifact | Vendors | Shape |
|---|---|---|
| **Skills** | All six (Claude, Codex, Gemini, Kiro, Cursor, Windsurf/Devin) | Folder-per-skill `SKILL.md`; the body is shared, but each vendor's frontmatter contract differs |
| **MCP server inventory** | All six | One JSON `mcpServers` shape for everyone except Codex (TOML); see "MCP rendering" below |
| **Engineering rules** | All vendors | Markdown body; per-vendor frontmatter (Cursor MDC, Kiro inclusion, Windsurf/Devin trigger, etc.) |
| **Prompts** | Any vendor that reads markdown | No vendor-specific shape; copy-paste-friendly |
| **Specs** | All vendors (read by humans + agents) | Markdown; same in every vendor |

**Agents do NOT cross-sync.** Their formats diverge: Claude/Gemini/Kiro/Cursor use flat Markdown frontmatter, Codex uses standalone TOML (`<name>.toml`), and Devin uses per-profile `AGENT.md` directories. Maintain agents per vendor.

Things that don't need syncing: vendor-specific config files (`.claude/settings.json`, `.codex/config.toml`, `.gemini/settings.json`) and vendor-specific runtime layouts.

## Tools that maintain sync

### `tools/sync-skills.py` - skills (body-aware)

All six vendors carry folder-per-skill `SKILL.md`, so a skill's *instructions* can be
shared everywhere. But each vendor's skill **frontmatter contract differs** (Claude/Codex
use `argument-hint`/`user-invocable`/`allowed-tools`; Kiro/Cursor use just
`name`/`description`; Gemini rewrites `allowed-tools` to its own tool ids). So the tool is
**body-aware**: it syncs the Markdown body below the frontmatter and **preserves each
target's own frontmatter**. Auxiliary files inside a skill folder sync verbatim.

```
runtimes/.claude/skills/<slug>/SKILL.md     ← source of truth (default)
runtimes/.codex/skills/<slug>/SKILL.md      ← body mirrored, frontmatter preserved
runtimes/.gemini/skills/<slug>/SKILL.md     ← "
runtimes/.kiro/skills/<slug>/SKILL.md       ← "
runtimes/.cursor/skills/<slug>/SKILL.md     ← "
runtimes/.windsurf/skills/<slug>/SKILL.md   ← "  (and runtimes/.devin/)
```

```bash
# Read-only report (claude → every other vendor)
python3 tools/sync-skills.py

# Apply: sync skill bodies from source to all targets
python3 tools/sync-skills.py --apply

# Single target, or a different source of truth
python3 tools/sync-skills.py --target cursor --apply
python3 tools/sync-skills.py --source codex --apply
```

Agents are **not** synced by this tool - their formats diverge across vendors.

Output categorizes drift as:

- **MISSING** - exists in source but not target.
- **EXTRA** - exists in target but not source. (Never auto-removed; you decide if it's intentional.)
- **DRIFT** - exists in both with different content.

When drift is intentional (a skill that uses Claude's `Task` tool has no Codex equivalent), document it in `runtimes/README.md` so future audits don't regenerate it.

### `runtimes/mcp/render/` - MCP server configs

All six vendors consume MCP configs. There are only two emit shapes - a JSON `mcpServers` object (everyone except Codex) and `[mcp_servers]` TOML (Codex) - but the paths differ:

| Vendor | Shape | Path |
|---|---|---|
| Claude Code | `mcpServers` JSON object | `.mcp.json` (project) / `~/.claude.json` (user) |
| Codex | `[mcp_servers.<name>]` TOML sections | `.codex/config.toml` |
| Gemini CLI | `mcpServers` JSON object | `.gemini/settings.json` |
| Kiro | `mcpServers` JSON object | `.kiro/settings/mcp.json` |
| Cursor | `mcpServers` JSON object | `.cursor/mcp.json` |
| Windsurf / Devin | `mcpServers` JSON object | `~/.codeium/windsurf/mcp_config.json` (user scope) |

Maintaining six files by hand is the failure mode. The canonical inventory lives in [`runtimes/mcp/servers.yaml`](../runtimes/mcp/servers.yaml); a renderer emits each vendor's shape:

```bash
python3 runtimes/mcp/render/render_claude.py   > runtimes/.claude/mcp.template.json
python3 runtimes/mcp/render/render_codex.py    > runtimes/.codex/config.template.toml
python3 runtimes/mcp/render/render_gemini.py   > runtimes/.gemini/settings.template.json
python3 runtimes/mcp/render/render_kiro.py     > runtimes/.kiro/settings/mcp.template.json
python3 runtimes/mcp/render/render_cursor.py   > runtimes/.cursor/mcp.template.json
python3 runtimes/mcp/render/render_windsurf.py > ~/.codeium/windsurf/mcp_config.json   # user scope
```

Workflow when adding a server:

1. Edit `servers.yaml`.
2. Re-run the renderers.
3. Commit `servers.yaml` + the rendered project-scoped files in one commit.

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
- A Gemini command (TOML prompt template under `.gemini/commands/`) is Gemini-shaped and doesn't apply verbatim to other vendors.
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

1. **For skills**: add the vendor slug to `SKILL_VENDORS` in `tools/sync-skills.py`. The body-aware sync handles differing frontmatter automatically.
2. **For agents**: nothing to wire - agent formats diverge across vendors, so agents are maintained per vendor.
3. **For MCP**: add a renderer under `runtimes/mcp/render/`.

See [`agent-cli-integrations.md`](agent-cli-integrations.md) for the broader "add a new vendor" walkthrough.

## Authoring agent

Cross-vendor sync utilities are owned by the `runtime-architect` agent. See [`.claude/agents/runtime-architect.md`](../.claude/agents/runtime-architect.md).

## See also

- [`agent-cli-integrations.md`](agent-cli-integrations.md) - concrete vendor wiring.
- [`multi-vendor-context-files.md`](multi-vendor-context-files.md) - root context-file pattern.
- [`tools/sync-skills.py`](../tools/sync-skills.py) - the sync tool itself.
- [`runtimes/mcp/`](../runtimes/mcp/) - MCP single source of truth and renderers.
