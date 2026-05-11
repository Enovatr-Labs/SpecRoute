# Specs

<!-- sources: specs/README.md -->

Technical specifications — the **how** layer of the spec-driven flow. Specs translate approved PRDs into actionable engineering plans.

For the canonical reference, see [`specs/README.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/specs/README.md).

## Directory layout

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
| **Spec triplet** (`requirements` + `design` + `tasks`) | Default for product features. Mandatory for cross-team or multi-week work. |
| `feature-spec-template.md` | Single-team feature, single owner, fits in one file. Combines requirements, design, and tasks in a compact form. |
| `technical-spec-template.md` | Non-product-facing work — refactor, migration, infra change, library upgrade. No user-facing PRD. |
| `architecture-decision-record.md` | A single architectural choice and its rationale. **ADRs are immutable**; corrections come via new ADRs. |

## The spec triplet in detail

The triplet exists because conflating concerns is a known failure mode:

| File | Question | Stable IDs | Cross-references |
|---|---|---|---|
| `requirements.md` | What must be true? | `R1.1`, `R1.2`, `NFR-1.1`, … | (none upstream) |
| `design.md` | How is it built? | (none — references requirement IDs) | requirement IDs via `**Satisfies:** R1.1` annotations |
| `tasks.md` | What do we do, in order? | task numbers | requirement IDs (back-refs) |

### Stable IDs are load-bearing
Once `R1.1` is published, that ID never gets reused. When a requirement is removed, mark it deprecated. This means commits, PRs, tests, and tasks can cross-reference requirements without drift.

### Tasks must back-reference requirements
Every task in `tasks.md` ends with `_Requirements: R1.1, R1.2_`. A task without a back-ref is unscoped. A requirement without any task is unimplemented. The **coverage table** in `tasks.md` makes the mapping explicit — every cell populated, no `TODO` rows.

## Lifecycle

1. **Draft** — author drafts the triplet under `specs/<feature>/` (or wherever the feature lives).
2. **Review** — tech lead + adjacent owners.
3. **Approve** — `Status: Approved` on each file. **Gate before implementation begins.**
4. **Implement** — `tasks.md` flips to `In Implementation`; tasks check off as PRs land.
5. **Complete** — all tasks checked, all requirements have passing tests. `Status: Complete`.

## Frontmatter contract

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

## ADRs

An **Architecture Decision Record** captures a single architectural choice and the rationale. Properties:

- **Immutable** once accepted. Superseding requires a new ADR that explicitly supersedes the prior one.
- Each ADR has stable identity (number + short title).
- Contains: context, decision, alternatives considered (with rejection reasons), consequences (positive and negative).
- Lives alongside the spec triplet or the technical spec it accompanies.

## Owner agent

Drafting and reviewing specs is owned by the `spec-author` agent. ADRs are also owned by `spec-author`. See [[Implementation Team]].

## Prompts for spec work

- [`prompts/shared/prd-to-spec-prompt.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/prompts/shared/prd-to-spec-prompt.md) — convert an approved PRD into the spec triplet.
- [`prompts/shared/spec-to-tasks-prompt.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/prompts/shared/spec-to-tasks-prompt.md) — derive `tasks.md` from `requirements.md` + `design.md`.

## See also

- [[PRDs]] — what comes before
- [[Workflow Spec to Implementation]] — the inner loop of turning a task into merged code
- [[Spec-Driven Development]] — the end-to-end flow
- [[Worked Example]] — the canonical `user-search` spec triplet with 11 requirements + 11 NFRs + full coverage table
