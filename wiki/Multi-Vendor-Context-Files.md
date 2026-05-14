# Multi-Vendor Context Files

<!-- sources: agentic-docs/multi-vendor-context-files.md -->

How a SpecRoute-driven repository uses one canonical context file (`AGENTS.md`) and small per-vendor delegation shims (`CLAUDE.md`, `GEMINI.md`) to support multiple agent CLIs without N parallel root files drifting apart.

For the canonical version, see [`agentic-docs/multi-vendor-context-files.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/multi-vendor-context-files.md).

## The pattern

```
repo-root/
├── AGENTS.md           ← canonical, vendor-neutral context (single source of truth)
├── CLAUDE.md           ← short delegation shim for Claude Code
├── GEMINI.md           ← short delegation shim for Gemini CLI
├── (.cursorrules)      ← Cursor-specific delegation, if needed
└── ...
```

**`AGENTS.md`** carries the substance: project identity, artifact taxonomy, vendor matrix, hard constraints, conventions.

**`CLAUDE.md`**, **`GEMINI.md`**, and any other vendor root files are **delegation shims** — they say "for project context, read `AGENTS.md`" and add only per-vendor overrides.

## Why this pattern

Each agent CLI uses its own root context file:

- Claude Code: `CLAUDE.md`
- Codex: `AGENTS.md`
- Gemini CLI: `GEMINI.md`
- And more will appear.

Without a convention, projects targeting multiple vendors end up with N copies of the same content, drifting independently. The delegation-shim convention solves it: one canonical file, each vendor's root file points at it.

## Anatomy of a delegation shim

```markdown
# CLAUDE.md

Claude Code shim for this repository. Read `AGENTS.md` first; it is the canonical
vendor-neutral source of truth.

## Source of truth
For repository overview, artifact taxonomy, vendor matrix, hard constraints, and
the spec-driven flow: read AGENTS.md. This file holds only Claude-Code-specific overrides.

## Claude-Code-specific notes
### .claude/ runtime is the SpecRoute implementation team
...
### Sanitization gate is active
...
### Frontmatter contracts (Claude-Code-specific)
...
```

Three things distinguish the shim:

1. **First non-trivial section is "Source of truth"** — pointing at the canonical file.
2. **Body holds vendor-specific behaviors only** — sanitization gates, frontmatter contracts unique to that vendor, MCP config locations.
3. **Length: 30–50 lines** — enough for vendor specifics; not enough to hold substance.

## What lives where

| In the canonical `AGENTS.md` | In per-vendor shims |
|---|---|
| Project identity | Vendor's runtime directory and what it consumes |
| Artifact taxonomy | Vendor-specific frontmatter contracts |
| Vendor matrix | Vendor-specific tooling |
| Hard constraints | Vendor-specific gotchas |
| Spec-driven flow summary | Pointers back to `AGENTS.md` |
| Pointers to deep references | |

## Vendor-specific runtime locations

| Vendor | Root context file | Auto-loaded? |
|---|---|---|
| Claude Code | `CLAUDE.md` | Yes (in repo root) |
| Codex | `AGENTS.md` | Yes (in repo root) |
| Gemini CLI | `GEMINI.md` | Yes (in repo root) |
| Cursor | `.cursorrules` (legacy) or `.cursor/rules/*.mdc` | Yes |
| Kiro | `.kiro/steering/*.md` (with `inclusion: always`) | Yes |
| Windsurf | `.windsurf/rules/*.md` | Yes |

For Cursor / Kiro / Windsurf, the "delegation shim" translates differently: there's no single root file, but their always-on rule files can each be a thin pointer to the canonical content. See [[Vendor Matrix]] and per-runtime READMEs under `runtimes/.<vendor>/`.

## Updating the canonical content

When you edit `AGENTS.md`:

1. Read each vendor shim. Confirm none duplicate the section you just edited (or, if they do, propagate the change).
2. Run `/audit` — vendor matrix consistency is one of the audit's checks.
3. Verify cross-references in `agentic-docs/` still resolve.

Most edits to `AGENTS.md` don't require shim changes. The shims are for vendor-specific overrides, not duplicates.

## When NOT to delegate

- The vendor doesn't auto-load any root file (no current major vendor has this).
- The project is single-vendor and only ever will be (then `CLAUDE.md` etc. can carry substance — but this prevents future multi-vendor support).
- Bootstrapping — early-stage projects often have only one root file; migrate to the delegation pattern when adding a second vendor.

## Anti-patterns

- **Duplicating substance across `AGENTS.md` and `CLAUDE.md`** → they drift.
- **Skipping the canonical `AGENTS.md` "because we only use Claude Code"** → adding a second vendor later requires a refactor.
- **Putting vendor specifics in `AGENTS.md`** → vendor specifics belong in the shim.
- **Ballooning shims** → if `CLAUDE.md` > 75 lines, ask which sections are actually Claude-specific.

## Worked examples (in this repo)

- [`AGENTS.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/AGENTS.md) — canonical
- [`CLAUDE.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/CLAUDE.md) — delegation shim
- [`GEMINI.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/GEMINI.md) — delegation shim

## See also

- [[Two-Tier Docs Pattern]] — short root context vs. deep references
- [[Agent CLI Integrations]] — concrete wiring per vendor
- [[Vendor Matrix]] — the supported-CLI contract
