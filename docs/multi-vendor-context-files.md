# Multi-Vendor Context Files

How a SpecForge-driven repository uses one canonical context file (`AGENTS.md`) and small per-vendor delegation shims (`CLAUDE.md`, `GEMINI.md`) to support multiple agent CLIs without N parallel root files drifting apart.

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

**`CLAUDE.md`**, **`GEMINI.md`**, and any other vendor-specific root files are slim **delegation shims** - they say "for the project context, read `AGENTS.md`" and add only per-vendor overrides.

## Why this pattern

Each agent CLI vendor has historically used its own root context file:

- Claude Code: `CLAUDE.md`
- Codex: `AGENTS.md`
- Gemini CLI: `GEMINI.md`
- Aider: `.aider.conf.yml` and others
- (and more vendors will appear)

Without a convention, projects targeting multiple vendors end up with N copies of the same content, drifting independently. When a convention changes (a new artifact type, a new vendor), every copy needs an update - and someone misses one, and the docs disagree, and the agent CLIs surface inconsistent guidance to the developer.

The delegation-shim convention solves this:

- One canonical file (`AGENTS.md`) - the substance lives here.
- Each vendor's root file points at the canonical file plus per-vendor specifics.
- Updating the substance is one edit; per-vendor specifics are local to their shim.

## Anatomy of a delegation shim

```markdown
# CLAUDE.md

This file provides Claude Code-specific guidance for working in this repository.

## Source of truth

For repository overview, artifact taxonomy, vendor matrix, hard constraints,
and the spec-driven flow: read [`AGENTS.md`](AGENTS.md). It is the canonical,
vendor-neutral context file. This file holds only Claude-Code-specific overrides.

## Claude-Code-specific notes

### `.claude/` runtime is the SpecForge implementation team
...

### Sanitization gate is active
...

### Frontmatter contracts (Claude-Code-specific)
...
```

Three things distinguish the shim from a substantive context file:

1. **First non-trivial section is "Source of truth"** - pointing at the canonical file.
2. **Body holds vendor-specific behaviors only** - sanitization gates, frontmatter contracts unique to that vendor, MCP config locations, hook conventions.
3. **Length: 30–50 lines** - enough for vendor specifics; not enough to hold project substance.

## What lives in the canonical `AGENTS.md`

- Project identity and what it is.
- Artifact taxonomy.
- Vendor matrix.
- Hard constraints (rules that aren't obvious from the code).
- Spec-driven flow summary.
- Pointers to deep references (`docs/`, `workflows/`, `rules/`).

## What lives in per-vendor shims

- The vendor's runtime directory and what it consumes.
- Vendor-specific frontmatter contracts.
- Vendor-specific tooling (slash commands, sub-agents, hook scripts).
- Vendor-specific gotchas.
- Pointers back to `AGENTS.md` for the substance.

## Vendor-specific runtime locations (recap)

The matrix (also in [`AGENTS.md`](../AGENTS.md) and [`README.md`](../README.md)):

| Vendor | Root context file | Auto-loaded? |
|---|---|---|
| Claude Code | `CLAUDE.md` | Yes (in repo root) |
| Codex | `AGENTS.md` | Yes (in repo root) |
| Gemini CLI | `GEMINI.md` | Yes (in repo root) |
| Cursor | `.cursorrules` (legacy) or `.cursor/rules/*.mdc` | Yes |
| Kiro | `.kiro/steering/*.md` (with `inclusion: always`) | Yes |
| Windsurf | `.windsurf/rules/*.md` | Yes |

For Cursor / Kiro / Windsurf, the "delegation shim" pattern translates differently: there's no single root file, but their always-on rule files can each be a thin pointer to the canonical content. See [`runtimes/.<vendor>/`](../runtimes/) for templates.

## Updating the canonical content

When you edit `AGENTS.md`:

1. Read each vendor shim. Confirm none of them duplicate the section you just edited (or, if they do, propagate the change).
2. Run `/audit` (or equivalent) - vendor matrix consistency is one of the audit's checks.
3. Verify cross-references in `docs/` still resolve.

Most edits to `AGENTS.md` don't require shim changes. The shims are for vendor-specific overrides, not duplicates.

## When to NOT delegate

A few cases where a vendor shim might carry substantive content rather than delegating:

- The vendor doesn't auto-load any root file by default (then the shim is the only context surface). Currently no major vendor has this constraint.
- The project is single-vendor and only ever will be. Then `CLAUDE.md` (or whichever) can carry the substance directly. But this prevents future multi-vendor support.
- Bootstrapping - early-stage projects often have only one root file. Migrate to the delegation pattern when adding a second vendor.

## Anti-patterns

- **Duplicating substance across `AGENTS.md` and `CLAUDE.md`.** They drift; readers get conflicting guidance. The shim should pointer-and-add, not pointer-and-restate.
- **Skipping the canonical `AGENTS.md` "because we only use Claude Code."** Adding a second vendor later requires a refactor that's harder than starting with the pattern.
- **Putting vendor specifics in `AGENTS.md`.** Vendor specifics belong in the shim. `AGENTS.md` is vendor-neutral.
- **Ballooning shims.** If `CLAUDE.md` grows past 75 lines, ask: which sections are actually Claude-specific, and which are project substance that should move to `AGENTS.md`?

## Authoring agent

Multi-vendor context-file structure is owned by the `framework-docs-author` agent. See [`.claude/agents/framework-docs-author.md`](../.claude/agents/framework-docs-author.md).

## See also

- [`two-tier-docs-pattern.md`](two-tier-docs-pattern.md) - short root context vs. deep references.
- [`agent-cli-integrations.md`](agent-cli-integrations.md) - concrete wiring per vendor.
- [`AGENTS.md`](../AGENTS.md) - the canonical context file in this repo.
- [`CLAUDE.md`](../CLAUDE.md), [`GEMINI.md`](../GEMINI.md) - worked examples of delegation shims.
