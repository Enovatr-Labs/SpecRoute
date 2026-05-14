# Two-Tier Docs Pattern in This Project

Why root context files stay short, and why we have an `agentic-docs/` directory.

## The pattern

```
Tier 1 (loaded every session)    Tier 2 (read on demand)

AGENTS.md          (~60 lines)    agentic-docs/
CLAUDE.md          (~30 lines)    ├── philosophy.md
                                  ├── spec-driven-development.md
                                  ├── agentic-coding-model.md
                                  ├── automation-decision-framework.md
                                  ├── documentation-structure.md
                                  ├── two-tier-docs-pattern.md (this file)
                                  └── agent-memory.md
```

## Why two tiers

Every line in [`AGENTS.md`](../AGENTS.md) and [`CLAUDE.md`](../CLAUDE.md) is loaded at session start. Tokens spent on those files are tokens unavailable for the user's actual question. A 2,000-line root context file is a slow leak from the agent's working memory.

It also makes orientation slower for humans. If a contributor wants to know "what should I do for a security incident?", they don't need the spec-driven-development primer first. The root file should be a **navigation surface**, not a content dump.

## What lives in Tier 1 (`AGENTS.md`, `CLAUDE.md`)

- What this project is.
- The core artifact taxonomy (and where each lives).
- Hard constraints (vendor neutrality, sanitization, frontmatter contracts).
- Pointers to the deep references in `agentic-docs/`.
- Vendor-specific overrides (in [`CLAUDE.md`](../CLAUDE.md) only, since we're Claude-only).

## What lives in Tier 2 (`agentic-docs/`)

- **Philosophy** ([`philosophy.md`](philosophy.md)) - operating beliefs.
- **Methodology** ([`spec-driven-development.md`](spec-driven-development.md)) - how the spec-driven flow plays out concretely.
- **Composition** ([`agentic-coding-model.md`](agentic-coding-model.md)) - how the four primitives (skills, agents, commands, hooks) compose.
- **Decisions framework** ([`automation-decision-framework.md`](automation-decision-framework.md)) - when to reach for each primitive.
- **Doc structure** ([`documentation-structure.md`](documentation-structure.md)) - where new docs go.
- **This file** ([`two-tier-docs-pattern.md`](two-tier-docs-pattern.md)) - the pattern itself.
- **Agent memory** ([`agent-memory.md`](agent-memory.md)) - per-agent persistent context pattern.

Each Tier 2 file is ~60-120 lines. Read on demand. Linked from Tier 1.

## How references go between tiers

**Tier 1 -> Tier 2: pointers only.**

Example, from [`AGENTS.md`](../AGENTS.md):

```markdown
## Hard constraints

5. **Two-tier docs.** This file (AGENTS.md) stays short. Deep references live
   in [`agentic-docs/`](agentic-docs/). See [`agentic-docs/two-tier-docs-pattern.md`].
```

Tier 2 -> Tier 1: assume the reader has read it.

Example, from this file:

> "Every line in `AGENTS.md` and `CLAUDE.md` is loaded at session start..."

We don't re-explain what `AGENTS.md` is here; the reader has it as context.

## What goes wrong without the pattern

### Single huge root file

- Slow context loading.
- Hard to scan.
- Forces every reader through every concept regardless of need.
- Agent's responses degrade because more of its budget is spent re-reading the file each turn.

### Tier 2 only (no root file)

- Agent CLIs have no anchor - they don't know what to load first.
- Conventions get re-explained in every conversation because they're not in the always-loaded surface.

### Tier 1 with substantive content

- Root file balloons.
- Concepts duplicated between root and deep references.
- Updates require multiple-file edits.

## Sizing rules of thumb

| Tier | Target | Hard cap |
|---|---|---|
| `AGENTS.md` | ~60 lines | ~150 |
| `CLAUDE.md` (shim) | 20-40 lines | 75 |
| `agentic-docs/<topic>.md` | 60-120 lines | flexible |

If `AGENTS.md` passes the cap, ask: which sections can move to `agentic-docs/`?

## Why we have an `agentic-docs/` (and not just a `docs/`)

Many projects already have a top-level `docs/` for product documentation, runbooks, ADRs (we have `adrs/` separately), API references, etc. Calling our framework reference layer `agentic-docs/` keeps it clearly distinct from the consumer-project's `docs/` and makes it obvious that these are agentic-engineering reference docs rather than product docs.

The framework convention (per its own [`agentic-docs/two-tier-docs-pattern.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/two-tier-docs-pattern.md)) is `agentic-docs/`. We follow it.

## See also

- The framework's canonical [`agentic-docs/two-tier-docs-pattern.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/two-tier-docs-pattern.md) for the broader pattern theory.
- [`documentation-structure.md`](documentation-structure.md) - where each doc type lives in this project.
- [`AGENTS.md`](../AGENTS.md), [`CLAUDE.md`](../CLAUDE.md) - this project's Tier 1 files.
