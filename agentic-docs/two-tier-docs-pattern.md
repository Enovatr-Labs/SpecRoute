# Two-Tier Docs Pattern

Keep root context files short; put deep references in a separate directory. The two tiers serve different purposes and have different cost models. Conflating them produces docs that fail at both jobs.

## The pattern

```
Tier 1: Root context files                Tier 2: Deep reference library
(loaded into every conversation)          (read on demand by humans and agents)

AGENTS.md         (~100 lines)            docs/
CLAUDE.md         (~50 lines, shim)       ├── philosophy.md
GEMINI.md         (~30 lines, shim)       ├── spec-driven-development.md
                                          ├── agentic-coding-model.md
                                          ├── automation-decision-framework.md
                                          ├── documentation-structure.md
                                          └── ...
```

**Tier 1** is short, scannable, and load-bearing for every interaction. **Tier 2** is detailed, comprehensive, and read selectively.

## Why two tiers

### The cost of long root context

Every file that the agent CLI loads at session start consumes context budget - every token in `AGENTS.md` is a token unavailable for the user's actual problem. A 2,000-line root context file is a slow leak from the agent's working memory.

It also makes orientation slower. If the user wants to know "what should I do for a security incident?", they don't need the spec-driven-development primer first. The root file should be a navigation surface, not a content dump.

### The cost of fragmented short docs

If everything is split into 50-line files with cross-references, navigation becomes a chore. The reader follows three links to assemble a complete picture.

### The compromise

- **Root files** carry the project's identity, conventions, and pointers. They're optimized for "agent loads this at every session start."
- **Deep references** carry the substance. They're optimized for "reader follows a link when they need this."

This is the same pattern operating systems use (kernel API surface vs. man pages), and that the open-source world has converged on (`README.md` for orientation, `agentic-docs/` for substance).

## Tier 1: what belongs

In `AGENTS.md` (canonical) and per-vendor delegation shims:

- **What this repository is** - one paragraph.
- **Core artifact taxonomy** - a table.
- **Hard constraints** - the rules that aren't obvious from the code (vendor neutrality, sanitization, frontmatter contracts).
- **Pointers to deep references** - "for X, see [`docs/<topic>.md`](docs/<topic>.md)".
- **Vendor-specific overrides** (in the per-vendor shims only).

In `CLAUDE.md` and `GEMINI.md` specifically: ~30–50 lines, mostly pointers. They delegate to `AGENTS.md` and add per-vendor specifics.

## Tier 2: what belongs

In `agentic-docs/`:

- **Philosophy** - why we do things the way we do (`philosophy.md`).
- **Decision frameworks** - when to choose X vs Y (`automation-decision-framework.md`).
- **Patterns** - recurring shapes (`two-tier-docs-pattern.md` - this file; `multi-vendor-context-files.md`).
- **Integration guides** - concrete wiring per vendor (`agent-cli-integrations.md`).
- **Conceptual deep-dives** - anything substantive that doesn't fit in 30 lines.

## How the tiers reference each other

Tier 1 → Tier 2: pointers only.

```markdown
# AGENTS.md

When to choose a skill vs an agent vs a command vs a hook: see
[`agentic-docs/automation-decision-framework.md`](agentic-docs/automation-decision-framework.md).
```

Tier 2 → Tier 1: assume the reader has read it.

```markdown
# agentic-docs/automation-decision-framework.md

(no need to re-explain the artifact taxonomy from AGENTS.md;
the reader has already encountered it)
```

## What goes wrong when you collapse the tiers

### Single huge root file

- Slow context loading.
- Hard to scan.
- Forces every reader through every concept regardless of need.
- The agent's responses degrade because more of its budget is spent re-reading the file each turn.

### Tier 2 only (no root file)

- Agent CLIs have no anchor - they don't know what to load first.
- Conventions get re-explained in every conversation because they're not in the always-loaded surface.
- Tier 2 docs grow to fill the gap, getting longer than they should be.

### Tier 1 with substantive content

- Root file balloons.
- Concepts duplicated between root and `agentic-docs/`.
- Updates require multiple-file edits.

## Sizing rules of thumb

| Tier | Target | Hard cap |
|---|---|---|
| `AGENTS.md` | ~100 lines | ~150 lines |
| `CLAUDE.md`, `GEMINI.md` (delegation shims) | 30–50 lines | 75 lines |
| `docs/<topic>.md` | 100–300 lines | flexible |

If a Tier 1 file passes the hard cap, ask: which sections can move to Tier 2?

## Vendor-specific notes

- **Claude Code** loads `CLAUDE.md` automatically. Keep it short; deep references in `agentic-docs/` are loaded on demand by the agent reading them.
- **Codex** loads `AGENTS.md` automatically.
- **Gemini CLI** loads `GEMINI.md` automatically.
- **Cursor / Windsurf** load rule files (`*.mdc`, `*.md` under `.cursor/rules/`, `.windsurf/rules/`); the two-tier pattern is enforced through which rules are `alwaysApply`-flagged vs glob-scoped.
- **Kiro** loads `.kiro/steering/*.md` per its `inclusion` frontmatter - same pattern, different syntax.

## See also

- [`multi-vendor-context-files.md`](multi-vendor-context-files.md) - how `AGENTS.md` + per-vendor delegation shims work.
- [`documentation-structure.md`](documentation-structure.md) - where new docs go (the broader decision tree).
- [`rules/documentation-rules.md`](../rules/documentation-rules.md) - content standards.
