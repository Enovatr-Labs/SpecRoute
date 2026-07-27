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
├── .cursor/rules/      ← Cursor-specific delegation, if needed (MDC rule files)
└── ...
```

**`AGENTS.md`** carries the substance: project identity, artifact taxonomy, vendor matrix, hard constraints, conventions.

**`CLAUDE.md`**, **`GEMINI.md`**, and any other vendor root files are **delegation shims** — they say "for project context, read `AGENTS.md`" and add only per-vendor overrides.

**The shim has to actually pull the file in.** Of the six supported CLIs,
**Codex, Cursor, and Devin Desktop read `AGENTS.md` natively**. Claude Code does
not — its documentation says plainly that it reads `CLAUDE.md` — and neither
does Gemini CLI without an opt-in. So a shim that merely *mentions*
`AGENTS.md` leaves the canonical content unloaded at launch; bridge it with an
`@AGENTS.md` import inside the vendor file, or make the vendor file a symlink
to it. Claims of universal native support are still wrong; the shim is what
makes the pattern work for runtimes that do not load it.

`AGENTS.md` itself is a convention, not a schema: it began at OpenAI, is now stewarded by the Agentic AI Foundation under the Linux Foundation, and specifies **no required fields, no frontmatter, and no schema**. Nested `AGENTS.md` files are spec'd behaviour — an agent reads the nearest one up the directory tree.

## Why this pattern

Each agent CLI uses its own root context file:

- Claude Code: `CLAUDE.md`, plus `.claude/rules/*.md` for modular instruction files
- Codex: `AGENTS.md`
- Gemini CLI / Antigravity: `GEMINI.md` (and *only* `GEMINI.md` without an opt-in — see below)
- Kiro: `.kiro/steering/*.md`
- Cursor: `.cursor/rules/*.mdc`; also natively reads `AGENTS.md`
- Devin Desktop: `AGENTS.md` natively, plus `.devin/rules/*.md`; Cascade also
  accepts `.windsurf/rules/*.md`
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
| Claude Code | `CLAUDE.md`, plus `.claude/rules/*.md` | Yes (in repo root) |
| Codex | `AGENTS.md` | Yes (in repo root) |
| Gemini CLI / Antigravity | `GEMINI.md` | Yes — but **`AGENTS.md` is not**, see below |
| Cursor | `.cursor/rules/*.mdc`; `AGENTS.md` also natively read | Yes |
| Kiro | `.kiro/steering/*.md` (with `inclusion: always`) | Yes |
| Devin Desktop | `AGENTS.md`; `.devin/rules/*.md` (Cascade also accepts `.windsurf/rules/*.md`) | Yes |

`.cursorrules` used to appear here as Cursor's legacy root file. It is now **absent from Cursor's documentation entirely and reported non-functional in current versions** — treat it as removed, not as a working fallback, and put Cursor's pointer content in `.cursor/rules/*.mdc` or `AGENTS.md`.

Cursor and Devin Desktop read the canonical `AGENTS.md` directly. For Kiro,
the delegation shim translates into an always-on steering file that points to
the canonical content. See [[Vendor Matrix]] and per-runtime READMEs under
`runtimes/.<vendor>/`.

### The Gemini exception

**Gemini CLI does not read `AGENTS.md` by default.** It reads `GEMINI.md`. Loading `AGENTS.md` requires opting in via the `context.fileName` setting in `.gemini/settings.json`, and the upstream request to read it by default was closed as not planned.

This is where the pattern's core assumption — every vendor's root file can point at the canonical one — buys less than it looks. A `GEMINI.md` that only says "read `AGENTS.md`" leaves Gemini with almost nothing at launch; the model can still follow the link once working, but nothing is loaded up front.

Two ways to close the gap, in order of preference:

1. **Opt in.** Commit `{"context": {"fileName": ["GEMINI.md", "AGENTS.md"]}}` in `.gemini/settings.json`. The shim stays slim and the canonical file loads alongside it. Commit it so teammates get the same behaviour.
2. **Let `GEMINI.md` carry the must-have content.** Duplication, which is exactly what this pattern avoids — so restrict it to standards that genuinely must be in context at launch.

Don't quietly assume option 1 is in place. If `.gemini/settings.json` isn't in the repo, Gemini is running on `GEMINI.md` alone.

### Claude Code has a second surface

`.claude/rules/*.md` are modular instruction files discovered recursively. Without frontmatter they load at launch at the **same priority as `CLAUDE.md`**; with a `paths:` glob list (the only frontmatter field) they load only when a matching file is touched. User-level `~/.claude/rules/` loads before project rules.

This is a better home than a growing `CLAUDE.md` for standing project substance — keep `CLAUDE.md` as the shim and put the bulk in `.claude/rules/`. `paths:` also gives Claude Code the file-scoped loading Cursor gets from `globs` and Kiro from `inclusion: fileMatch`. Note the naming collision with SpecRoute's own top-level `rules/` directory, which is documentation rather than a runtime surface; see [[Rules]].

### `.agents/` — the emerging neutral location

Alongside `AGENTS.md`, a vendor-neutral **`.agents/` directory** is emerging as the shared home for runtime artifacts. SpecRoute records this from an installed Codex 0.145.0 binary rather than from documentation, because the public docs are inconsistent on it: the binary carries `.agents/skills` as a repo-level skills root, plus `.agents/plugins/marketplace.json`, and enumerates `.agents` beside `.claude` and `.cursor` when detecting external agent configuration.

The same binary **still** carries `.codex/skills` and `$CODEX_HOME/skills`, and both work today. Treat `.agents/` as the convergence point to watch — not yet a reason to migrate off the per-vendor paths.

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
