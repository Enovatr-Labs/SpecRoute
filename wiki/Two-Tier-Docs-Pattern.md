# Two-Tier Docs Pattern

<!-- sources: agentic-docs/two-tier-docs-pattern.md -->

Keep root context files short; put deep references in a separate directory. The two tiers serve different purposes and have different cost models. Conflating them produces docs that fail at both jobs.

For the canonical version, see [`agentic-docs/two-tier-docs-pattern.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/agentic-docs/two-tier-docs-pattern.md).

## The pattern

```
Tier 1: Root context files                Tier 2: Deep reference library
(loaded into every conversation)          (read on demand by humans and agents)

AGENTS.md         (~100 lines)            agentic-docs/
CLAUDE.md         (~50 lines, shim)       ├── philosophy.md
GEMINI.md         (~30 lines, shim)       ├── spec-driven-development.md
                                          ├── agentic-coding-model.md
                                          ├── automation-decision-framework.md
                                          ├── ...
```

**Tier 1** is short, scannable, and load-bearing for every interaction. **Tier 2** is detailed, comprehensive, and read selectively.

## Why two tiers

### The cost of long root context
Every file the agent CLI loads at session start consumes context budget. A 2,000-line root context file is a slow leak from the agent's working memory. It also makes orientation slower — the user wanting "what should I do for a security incident?" doesn't need the spec-driven primer first.

### The cost of fragmented short docs
If everything is split into 50-line files with cross-references, navigation becomes a chore. The reader follows three links to assemble a complete picture.

### The compromise
- **Root files** carry the project's identity, conventions, and pointers. Optimized for "agent loads this at every session start."
- **Deep references** carry the substance. Optimized for "reader follows a link when they need this."

Same pattern operating systems use (kernel API surface vs. man pages), and the open-source world has converged on (`README.md` for orientation, `agentic-docs/` for substance).

## Tier 1: what belongs

In `AGENTS.md` (canonical) and per-vendor delegation shims:

- **What this repository is** — one paragraph.
- **Core artifact taxonomy** — a table.
- **Hard constraints** — the rules that aren't obvious from the code.
- **Pointers to deep references** — "for X, see `agentic-docs/<topic>.md`".
- **Vendor-specific overrides** (in the per-vendor shims only).

## Tier 2: what belongs

In `agentic-docs/`:

- **Philosophy** — why we do things the way we do.
- **Decision frameworks** — when to choose X vs Y.
- **Patterns** — recurring shapes.
- **Integration guides** — concrete wiring per vendor.
- **Conceptual deep-dives** — anything substantive that doesn't fit in 30 lines.

## How the tiers reference each other

Tier 1 → Tier 2: pointers only.

```markdown
# AGENTS.md
When to choose a skill vs an agent vs a command vs a hook: see
[`agentic-docs/automation-decision-framework.md`](agentic-docs/automation-decision-framework.md).
```

Tier 2 → Tier 1: assume the reader has read it. No need to re-explain the artifact taxonomy.

## Sizing rules of thumb

| Tier | Target | Hard cap |
|---|---|---|
| `AGENTS.md` | ~100 lines | ~150 lines |
| `CLAUDE.md`, `GEMINI.md` (delegation shims) | 30–50 lines | 75 lines |
| `agentic-docs/<topic>.md` | 100–300 lines | flexible |

If a Tier 1 file passes the hard cap, ask which sections can move to Tier 2.

## What goes wrong when you collapse tiers

- **Single huge root file** → slow context loading, hard to scan, agent response quality degrades.
- **Tier 2 only (no root file)** → agent CLIs have no anchor; conventions get re-explained in every conversation.
- **Tier 1 with substantive content** → root file balloons; concepts duplicated between tiers; updates require multi-file edits.

## Vendor-specific notes

- **Claude Code** loads `CLAUDE.md` automatically. Keep it short; deep references in `agentic-docs/` are loaded on demand.
- **Codex** loads `AGENTS.md` automatically.
- **Gemini CLI** loads `GEMINI.md` automatically.
- **Cursor / Windsurf** load rule files; the two-tier pattern is enforced through which rules are `alwaysApply`-flagged vs glob-scoped.
- **Kiro** loads `.kiro/steering/*.md` per `inclusion` frontmatter.

See [[Multi-Vendor Context Files]] for the canonical-shim-pattern in full.

## See also

- [[Multi-Vendor Context Files]] — how the canonical `AGENTS.md` and per-vendor shims work
- [[Documentation Structure]] — where new docs go
- [[Rules]] — content standards including documentation rules
