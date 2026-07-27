# Cross-Vendor Sync

How a SpecRoute-driven project keeps the artifacts that several vendors consume in lock-step. This is the maintainability story for multi-vendor support.

## What needs to stay synced

| Artifact | Vendors | Shape |
|---|---|---|
| **Skills** | All six (Claude, Codex, Gemini, Kiro, Cursor, Devin Desktop) | Folder-per-skill `SKILL.md`; the body is shared, but each vendor's frontmatter contract differs |
| **MCP server inventory** | All six | One JSON `mcpServers` shape for everyone except Codex (TOML); see "MCP rendering" below |
| **Engineering rules** | All vendors | Markdown body; per-vendor loading contract (Cursor MDC, Kiro inclusion, Devin Local `AGENTS.md`, and Cascade rules) |
| **Prompts** | Any vendor that reads markdown | No vendor-specific shape; copy-paste-friendly |
| **Specs** | All vendors (read by humans + agents) | Markdown; same in every vendor |

**Agents do NOT cross-sync.** Their formats diverge: Claude/Gemini/Kiro/Cursor use flat Markdown frontmatter, Codex uses standalone TOML (`<name>.toml`), and Devin uses per-profile `AGENT.md` directories. Maintain agents per vendor.

Things that don't need syncing: vendor-specific config files (`.claude/settings.json`, `.codex/config.toml`, `.gemini/settings.json`) and vendor-specific runtime layouts.

## Tools that maintain sync

### `tools/sync-skills.py` - skills (body-aware)

All six vendors carry folder-per-skill `SKILL.md`, so a skill's *instructions* can be
shared everywhere. The [Agent Skills standard](https://agentskills.io) requires only
`name` (max 64 chars, matching the enclosing directory) and `description` (max 1024);
`license`, `compatibility`, and `metadata` are the other standard fields. Everything else
is a **vendor extension**, and that is where the contracts diverge: Claude Code adds
`argument-hint`/`user-invocable`/`allowed-tools`/`disallowed-tools`; the shipped
Codex/Gemini/Kiro/Cursor templates carry only `name`/`description`; Devin Desktop uses a YAML list of lowercase tool ids
where Claude uses space-separated capitalised names. So the tool is **body-aware**: it syncs
the Markdown body below the frontmatter and **preserves each target's own frontmatter**.
Auxiliary files inside a skill folder sync verbatim.

Because the extensions do not survive a sync, keep nothing load-bearing in them. In
particular `allowed-tools` is not a portable permission model - in Claude Code it
*pre-approves* tools for the invoking turn rather than restricting them (`disallowed-tools`
is the restricting field), and other vendors ignore it entirely. Confinement belongs in each
runtime's permission settings and hooks, not in a synced skill header.

```
runtimes/.claude/skills/<slug>/SKILL.md     ← source of truth (default)
runtimes/.codex/skills/<slug>/SKILL.md      ← body mirrored, frontmatter preserved
runtimes/.gemini/skills/<slug>/SKILL.md     ← "
runtimes/.kiro/skills/<slug>/SKILL.md       ← "
runtimes/.cursor/skills/<slug>/SKILL.md     ← "
runtimes/.devin/skills/<slug>/SKILL.md      ← "
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

When drift is intentional (for example, a vendor-only integration skill), document it in `runtimes/README.md` so future audits do not regenerate it.

## `.agents/skills/` - the convergence location to watch

A vendor-neutral skills root is emerging: **`.agents/skills/<slug>/SKILL.md`**. SpecRoute has verified it directly in Codex and Devin Desktop; support claims for other runtimes remain ecosystem signals to re-check against their current documentation.

This was verified against an **installed Codex 0.145.0 binary**, which carries `.agents/skills` as a repo-level skills root alongside `.agents/plugins/marketplace`, `.agents/plugins/api`, `.agents/hooks`, and `.agents/settings` - and *still* carries `.codex/skills` and `$CODEX_HOME/skills`. The binary check matters because public documentation on this path is inconsistent between vendors and between versions.

**Both work today. Do not migrate off `.codex/skills` yet.** The per-vendor directories are not deprecated, and moving early buys nothing except a rollback if the convention shifts again.

What it would mean if `.agents/skills/` does become universal: **most of the fan-out this document describes stops being necessary.** `tools/sync-skills.py` exists because six vendors each want their own copy of the same body under their own directory with their own frontmatter dialect. One shared root collapses that to a single directory, and the tool's remaining job shrinks to whatever frontmatter dialects survive. That is the outcome to hope for, and the reason to keep skill bodies free of vendor-specific frontmatter dependencies in the meantime - a skill that only needs `name` + `description` is already portable to a shared root.

What to do now:

- Keep authoring under `runtimes/.<vendor>/skills/`. That is what SpecRoute's layouts, `/parity`, and the sync tool assume.
- If you are consuming SpecRoute in a repo that only targets `.agents/`-aware CLIs, dropping the skill folders into `.agents/skills/` is a legitimate simplification - just don't expect every other runtime to pick them up.
- Re-check this before assuming it is settled. It is the most volatile claim in this document.

## Plugins and marketplaces

Claude Code, Codex, Cursor, and Gemini CLI all now support **plugins** installed from a marketplace. This is a distribution mechanism, and it is worth understanding because it is the alternative to the copy-a-runtime-layout model SpecRoute uses.

A plugin bundles artifacts that would otherwise be copied in individually - typically some combination of skills, subagents, commands, hooks, and MCP server definitions - behind a manifest, so a team installs and updates them as one unit.

| | Copied runtime layout (what SpecRoute ships) | Plugin |
|---|---|---|
| Install | Copy `runtimes/.<vendor>/` into your repo | Install from a marketplace by name |
| Ownership | Yours immediately; edit freely | Upstream's; you take updates |
| Intended for | A starting point you are expected to modify | A finished capability you consume as-is |
| Versioning | Your repo's git history | The plugin's own version |

SpecRoute's layouts are deliberately the first column: they are templates meant to be read, edited, and committed into a consuming project, which is a poor fit for something you install and update. If you have stabilised a skill set and want to hand it to other teams unchanged, packaging it as a plugin is the better delivery mechanism.

Manifest formats differ per vendor and are still moving; check your vendor's current documentation rather than assuming portability between marketplaces.

### `runtimes/mcp/render/` - MCP server configs

All six vendors consume MCP configs. There are only two emit shapes - a JSON `mcpServers` object (everyone except Codex) and `[mcp_servers]` TOML (Codex) - but the paths differ:

| Vendor | Shape | Path |
|---|---|---|
| Claude Code | `mcpServers` JSON object | `.mcp.json` (project) / `~/.claude.json` (user) |
| Codex | `[mcp_servers.<name>]` TOML sections | `.codex/config.toml` |
| Gemini CLI | `mcpServers` JSON object | `.gemini/settings.json` |
| Kiro | `mcpServers` JSON object | `.kiro/settings/mcp.json` |
| Cursor | `mcpServers` JSON object | `.cursor/mcp.json` |
| Devin Desktop | `mcpServers` JSON object | `.devin/config.json` (project scope) |

Maintaining six emitted configurations by hand is the failure mode. The canonical inventory lives in [`runtimes/mcp/servers.yaml`](../runtimes/mcp/servers.yaml); a renderer emits each target's shape:

```bash
python3 runtimes/mcp/render/render_claude.py   > runtimes/.claude/mcp.template.json
python3 runtimes/mcp/render/render_codex.py    > runtimes/.codex/config.template.toml
python3 runtimes/mcp/render/render_gemini.py   > runtimes/.gemini/settings.template.json
python3 runtimes/mcp/render/render_kiro.py     > runtimes/.kiro/settings/mcp.template.json
python3 runtimes/mcp/render/render_cursor.py   > runtimes/.cursor/mcp.template.json
python3 runtimes/mcp/render/render_devin.py    > runtimes/.devin/config.template.json
```

Cascade, the compatibility agent inside Devin Desktop, still reads the
user-scoped `~/.codeium/windsurf/mcp_config.json`. That compatibility path does
not define a seventh SpecRoute runtime or renderer; translate the same canonical
server inventory only when maintaining an existing Cascade installation.

Workflow when adding a server:

1. Edit `servers.yaml`.
2. Re-run the renderers.
3. Commit `servers.yaml` + the rendered project-scoped files in one commit.

This is an architectural choice with a maintenance benefit: source of truth is one file, divergence is impossible.

### `/parity` command - quick check

The `/parity` slash command runs skill-body and MCP source-of-truth checks and reports drift without writing. Agents are deliberately excluded because their native formats diverge.

## Sync cadence

When to run sync tools:

- **Before every commit that touches a runtime skill** - confirm the change reached all intended targets, or that the asymmetry is intentional.
- **After editing `runtimes/mcp/servers.yaml`** - re-render and commit.
- **Pre-PR** - `/parity` as part of `/audit`.
- **Periodically** - even without active changes, run `tools/sync-skills.py` weekly. Drift can sneak in via merge conflicts.

## When vendor parity should NOT be the goal

Some artifacts genuinely belong to only one vendor:

- A vendor-only integration skill may depend on a tool or configuration surface another runtime does not expose.
- A Gemini command (TOML prompt template under `.gemini/commands/`) is Gemini-shaped and doesn't apply verbatim to other vendors.
- A Claude hook script's behavior depends on the Claude Code hook protocol; Kiro's hooks have different protocols.

Document these asymmetries explicitly in `runtimes/README.md` so audits don't regenerate them. The form is:

> **Vendor-only skills** (intentional, will not mirror):
> - `<skill-slug>` - depends on `<vendor-specific capability>`; no verified equivalent in the other target runtimes.

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
