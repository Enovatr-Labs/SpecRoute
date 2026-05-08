# Specifications

Technical specifications — the *how* layer of the spec-driven flow. Specs translate approved PRDs into actionable engineering plans.

```
specs/
├── templates/
│   ├── requirements-template.md           spec triplet pt 1: WHAT must be true
│   ├── design-template.md                 spec triplet pt 2: HOW it's built
│   ├── tasks-template.md                  spec triplet pt 3: ordered work items
│   ├── feature-spec-template.md           single-file lightweight alternative
│   ├── technical-spec-template.md         non-product-facing work (refactors, migrations)
│   └── architecture-decision-record.md    immutable ADR template
└── examples/                              worked specs
```

## When to use which template

| Template | Use when |
|---|---|
| **Spec triplet** (`requirements` + `design` + `tasks`) | Default for product features. Mandatory for cross-team or multi-week work. The cleanest separation of concerns. |
| `feature-spec-template.md` | Single-team feature, single owner, fits comfortably in one file. The same file holds requirements, design, and tasks in a compact form. |
| `technical-spec-template.md` | Non-product-facing work — refactor, migration, infra change, library upgrade. There is no user-facing PRD. |
| `architecture-decision-record.md` | A single architectural choice and the rationale. ADRs are immutable; corrections come via new ADRs. |

## The spec triplet in detail

The triplet exists because conflating these concerns is a known failure mode:

| File | Question it answers | Stable IDs | Cross-references |
|---|---|---|---|
| `requirements.md` | What must be true? | `R1.1`, `R1.2`, `NFR-1.1`, … | (none upstream) |
| `design.md` | How is it built? | (none — references requirement IDs) | requirement IDs |
| `tasks.md` | What do we do, in order? | task numbers | requirement IDs (back-refs) |

**Stable IDs are load-bearing.** Once `R1.1` is published, that ID never gets reused for a new requirement — when removed, mark it deprecated. This means commits, PRs, and tasks can cross-reference requirements without fear of drift.

**Tasks must back-reference requirements.** Every task in `tasks.md` ends with `_Requirements: R1.1, R1.2_`. A task without a requirement back-reference is unscoped. A requirement without any task is unimplemented.

## Lifecycle

1. **Draft** — author drafts the triplet (or single-file spec) under `specs/examples/<feature>/` or wherever the feature lives.
2. **Review** — tech lead and adjacent owners review.
3. **Approve** — status `Approved` on each file; this is the gate before implementation begins.
4. **Implement** — `tasks.md` status flips to `In Implementation`; tasks get checked off as PRs land.
5. **Complete** — all tasks checked, all requirements have passing tests. Set status `Complete`.

## Frontmatter contract

All spec files include this front-matter block:

```yaml
---
Version: 0.1
Date: YYYY-MM-DD
Author: <name>
Status: Draft | Approved | In Implementation | Complete
Source PRD: <link>
Source Requirements: requirements.md   # design.md and tasks.md only
Source Design: design.md               # tasks.md only
---
```

## Authoring agent

Drafting and reviewing specs is owned by the `spec-author` agent. See `.claude/agents/spec-author.md` for its operating principles.

## Related documents

- [`prds/README.md`](../prds/README.md) — what comes before
- [`prompts/shared/prd-to-spec-prompt.md`](../prompts/shared/prd-to-spec-prompt.md) — reusable prompt to bootstrap the triplet from an approved PRD
- [`prompts/shared/spec-to-tasks-prompt.md`](../prompts/shared/spec-to-tasks-prompt.md) — reusable prompt to derive `tasks.md` from `requirements.md` + `design.md`
- [`docs/spec-driven-development.md`](../docs/spec-driven-development.md) — the end-to-end flow
