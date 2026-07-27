# Cross-Vendor Sync

<!-- sources: agentic-docs/cross-vendor-sync.md, tools/sync-skills.py -->

How a SpecRoute-driven project keeps the artifacts that several vendors consume in lock-step. This is the maintainability story for multi-vendor support.

For the canonical reference, see [`agentic-docs/cross-vendor-sync.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/cross-vendor-sync.md).

## What needs to stay synced

| Artifact | Vendors | Shape |
|---|---|---|
| **Skills** | All six (Claude Code, Codex, Gemini, Kiro, Cursor, Devin Desktop) | Folder-per-skill `SKILL.md`; the body is shared, each vendor's frontmatter dialect differs |
| **MCP server inventory** | All six | Two emit shapes - `mcpServers` JSON for all but Codex's `[mcp_servers]` TOML; see [[MCP Integration]] |
| **Engineering rules** | All vendors | Markdown body; per-vendor frontmatter (Cursor MDC, Kiro inclusion, Devin trigger, etc.) |
| **Prompts** | Any vendor reading markdown | No vendor-specific shape; copy-paste-friendly |
| **Specs** | All vendors (read by humans + agents) | Same in every vendor |

**Agents do NOT cross-sync.** Their formats diverge: Claude/Gemini/Kiro/Cursor use flat Markdown with frontmatter, Codex uses standalone TOML (`<name>.toml`), and Devin uses per-profile `AGENT.md` directories. Maintain agents per vendor.

**Not synced**: vendor-specific config files (`.claude/settings.json`, `.codex/config.toml`, `.gemini/settings.json` + `.gemini/commands/*.toml`) and vendor-specific runtime layouts.

## Tools that maintain sync

### `tools/sync-skills.py` — skills (body-aware)

All six vendors carry folder-per-skill `SKILL.md`, so a skill's *instructions* can be shared everywhere. SpecRoute uses `name` and `description` as its portable publication baseline. Everything else is vendor-specific, so the tool is **body-aware**: it syncs the Markdown body and **preserves each target's own frontmatter**.

```
runtimes/.claude/skills/<slug>/SKILL.md     ← source of truth (default)
runtimes/.codex/skills/<slug>/SKILL.md      ← body mirrored, frontmatter preserved
runtimes/.gemini/skills/<slug>/SKILL.md     ← "
runtimes/.kiro/skills/<slug>/SKILL.md       ← "
runtimes/.cursor/skills/<slug>/SKILL.md     ← "
runtimes/.devin/skills/<slug>/SKILL.md      ← "
```

Because the extensions do not survive a sync, keep nothing load-bearing in them. In particular `allowed-tools` is not a portable permission model - in Claude Code it *pre-approves* tools for the invoking turn rather than restricting them (`disallowed-tools` is the restricting field), and other vendors ignore it entirely.

Usage:

```bash
# Read-only report (claude → every other vendor)
python3 tools/sync-skills.py

# Apply: sync skill bodies from source to all targets
python3 tools/sync-skills.py --apply

# Single target, or a different source of truth
python3 tools/sync-skills.py --target cursor --apply
python3 tools/sync-skills.py --source codex --apply
```

Output categorizes drift as:

- **MISSING** — exists in source but not target.
- **EXTRA** — exists in target but not source. (**Never auto-removed**; you decide whether it's intentional.)
- **DRIFT** — exists in both with different content.

When drift is intentional (for example, a vendor-only integration skill), document it in `runtimes/README.md` so future audits do not regenerate it.

## `.agents/skills/` — the convergence location to watch

A vendor-neutral skills root is emerging: **`.agents/skills/<slug>/SKILL.md`**.
SpecRoute has verified it directly in Codex, and Devin documents it as the
recommended repository location. Support claims for other runtimes remain
ecosystem signals to re-check against current documentation.

This was verified against an **installed Codex 0.145.0 binary**, which carries `.agents/skills` as a repo-level skills root alongside `.agents/plugins/marketplace`, `.agents/plugins/api`, `.agents/hooks`, and `.agents/settings` - and *still* carries `.codex/skills` and `$CODEX_HOME/skills`. The binary check matters because public documentation on this path is inconsistent between vendors and versions.

**Both work today. Do not migrate off `.codex/skills` yet.** The per-vendor directories are not deprecated, and moving early buys nothing but a rollback if the convention shifts again.

If `.agents/skills/` does become universal, **most of the fan-out on this page stops being necessary**. `tools/sync-skills.py` exists because six vendors each want their own copy of the same body under their own directory in their own frontmatter dialect; one shared root collapses that to a single directory. That is a reason to keep skill bodies free of vendor-specific frontmatter dependencies now - a skill that only needs `name` + `description` is already portable to a shared root.

Re-check this before treating it as settled. It is the most volatile claim on this page.

## Plugins and marketplaces

Claude Code, Codex, Cursor, and Gemini CLI all support **plugins** installed from a marketplace - the alternative to the copy-a-runtime-layout model SpecRoute uses. A plugin bundles artifacts that would otherwise be copied in individually (typically some mix of skills, subagents, commands, hooks, and MCP server definitions) behind a manifest, so a team installs and updates them as one unit.

| | Copied runtime layout (what SpecRoute ships) | Plugin |
|---|---|---|
| Install | Copy `runtimes/.<vendor>/` into your repo | Install from a marketplace by name |
| Ownership | Yours immediately; edit freely | Upstream's; you take updates |
| Intended for | A starting point you are expected to modify | A finished capability consumed as-is |
| Versioning | Your repo's git history | The plugin's own version |

SpecRoute's layouts are deliberately the first column - templates meant to be read, edited, and committed into a consuming project, which is a poor fit for something you install and update. Once a skill set has stabilised and you want other teams to consume it unchanged, packaging it as a plugin is the better delivery mechanism. Manifest formats differ per vendor and are still moving.

### `runtimes/mcp/render/` — MCP server configs

Render from one canonical YAML to per-vendor shapes. See [[MCP Integration]] for the full workflow.

### `/parity` command — quick check

The `/parity` slash command runs skill-body and MCP source-of-truth checks and reports drift without writing. Agents are deliberately excluded because their native formats diverge.

## Sync cadence

When to run sync tools:

- **Before every commit** that touches a runtime skill — confirm the change reached all intended targets, or that the asymmetry is intentional.
- **After editing `runtimes/mcp/servers.yaml`** — re-render and commit.
- **Pre-PR** — `/parity` as part of `/audit`.
- **Periodically** — even without active changes, run `tools/sync-skills.py` weekly. Drift sneaks in via merge conflicts.

## When parity should NOT be the goal

Some artifacts genuinely belong to only one vendor:

- A vendor-only integration skill may depend on a tool or configuration surface another runtime does not expose.
- A Gemini command is TOML-shaped and does not apply verbatim to other vendors.
- A Claude hook script's behavior depends on the Claude Code hook protocol; Kiro's hooks have different protocols.

Document these asymmetries explicitly in `runtimes/README.md` so audits don't regenerate them:

> **Vendor-only skills** (intentional, will not mirror):
> - `<skill-slug>` — depends on `<vendor-specific capability>`; no verified equivalent in the other target runtimes.

## Anti-patterns

- **Editing per-vendor configs by hand when a renderer exists** — your edits will be lost on the next render.
- **Per-vendor `servers.yaml` files** — defeats the single-source purpose.
- **Inconsistent skill names across vendors** — a skill called `audit-changes` in Claude and `audit-diff` in Codex is two skills, not one.
- **Frontmatter drift** — a skill with `model: opus` in Claude and `model: sonnet` in Codex is silently wrong. Run sync.
- **Skipping sync because "the diff is small"** — small drift compounds; the small change today is the merge conflict next quarter.

## Adding a new sync target

A new vendor that consumes shapes other vendors also consume gets an entry in the sync tool:

1. **For skills** — add the vendor slug to `SKILL_VENDORS` in `tools/sync-skills.py`. The body-aware sync handles the differing frontmatter automatically.
2. **For agents** — nothing to wire. Agent formats diverge across vendors, so agents are maintained per vendor.
3. **For MCP** — add a renderer under `runtimes/mcp/render/`.

See [[Adding a Vendor]] for the broader walkthrough.

## Owner agent

Cross-vendor sync utilities are owned by the `runtime-architect` agent.

## See also

- [[Agent CLI Integrations]] — concrete vendor wiring
- [[Multi-Vendor Context Files]] — root context-file pattern
- [[MCP Integration]] — MCP renderers in detail
- [[Vendor Matrix]] — the supported-CLI contract
