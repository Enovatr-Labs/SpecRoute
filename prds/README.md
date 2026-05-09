# PRDs

Product Requirements Documents - the business intent layer of the spec-driven flow.

```
prds/
├── templates/
│   ├── prd-template.md                  full 23-section enterprise PRD
│   ├── lightweight-prd-template.md      single-page alternative
│   └── platform-srs-template.md         system-wide SRS (distinct from feature PRDs)
├── active/                              in-flight PRDs
├── deprecated/                          superseded PRDs (kept for context)
├── archive/                             shipped or abandoned PRDs (historical record)
└── examples/                            illustrative worked PRDs
```

## When to use which template

| Template | Use when |
|---|---|
| `prd-template.md` (full) | Multi-team feature, multi-week effort, cross-service impact, or significant architectural change. Default choice for non-trivial work. |
| `lightweight-prd-template.md` | Single owner, single team, single acceptance criterion, fits on one page. |
| `platform-srs-template.md` | Specifying the platform as a whole. One per platform; revise rather than duplicate. |

**Rule of thumb:** if you're unsure, start with the lightweight template. If filling it in produces an awkward doc that wants to be longer, escalate to the full template.

## Lifecycle

1. **Draft** in `prds/active/` with status `Draft`.
2. **Review** - promote to status `Under Review` once the author considers it ready.
3. **Approve** - flip to status `Approved` when stakeholders sign off; this is the gate before spec-triplet work begins.
4. **Implement** - status `In Implementation` while the matching `specs/examples/<feature>/` is being built and the work is in flight.
5. **Ship** - status `Shipped` and move to `prds/archive/`.
6. **Deprecate** - when superseded, move to `prds/deprecated/` with a pointer to the replacement PRD.

Filenames in `active/` should be `<slug>.md` (e.g. `notification-preferences.md`). Filenames in `archive/` should prefix the year for sorting (e.g. `2026-04-notification-preferences.md`).

## Frontmatter contract

All PRDs (full and lightweight) include this front-matter block at the top:

```yaml
---
Version: 0.1
Date: YYYY-MM-DD
Author: <name>
Status: Draft | Under Review | Approved | In Implementation | Shipped | Deprecated
Architecture Reference: <link or "TODO">
Scope: <one-line scope statement>
---
```

A PRD without `Status` is not actionable - reviewers can't tell what gate it's at. A PRD without `Architecture Reference` is missing context downstream stages need.

## Authoring agent

Drafting and reviewing PRDs is owned by the `prd-author` agent. See `.claude/agents/prd-author.md` for its operating principles.

## Related documents

- [`specs/README.md`](../specs/README.md) - what comes after the PRD is approved
- [`agentic-docs/spec-driven-development.md`](../agentic-docs/spec-driven-development.md) - the end-to-end flow
- [`prompts/shared/prd-to-spec-prompt.md`](../prompts/shared/prd-to-spec-prompt.md) - a reusable prompt for converting a PRD into the spec triplet
