# Examples

End-to-end worked examples that demonstrate the SpecForge artifact pipeline.

```
examples/
├── README.md                       (this file)
└── sample-feature/                 canonical worked example: user-search
    ├── prd.md                      full 23-section enterprise PRD
    ├── requirements.md             spec triplet pt 1 (stable IDs)
    ├── design.md                   spec triplet pt 2 (architecture, data model, APIs)
    ├── tasks.md                    spec triplet pt 3 (numbered with back-refs)
    ├── agent-roster.md             cross-vendor agent inventory + task assignments
    ├── prompts/                    full phased prompt set: 1 global master, 4 phase masters, 22 task prompts
    │   ├── 000_GLOBAL_MASTER.md
    │   ├── README.md               phase index
    │   ├── phase0_foundation/      tasks 1–3 (Q1, Q2, Q3 spikes / privacy review)
    │   ├── phase1_backend/         tasks 4–12 (indexes, validator, RBAC, query, cursor, cache, endpoint, observability, rate limit)
    │   ├── phase2_frontend/        tasks 13–17 (input, filters, table, pagination, page composition)
    │   └── phase3_validation/      tasks 18–22 (load test, flag, rollout, docs, rollback drill)
    └── implementation-plan.md      operational view (schedule, resources, risks)
```

## What `sample-feature/` demonstrates

The `user-search` feature exercises every artifact shape in SpecForge:

- **PRD** — the full 23-section enterprise template ([`prds/templates/prd-template.md`](../prds/templates/prd-template.md)). Real product framing, success metrics, scope boundaries, performance budgets, security requirements.
- **Spec triplet** — `requirements.md` with stable IDs (`R1.1` through `NFR-4.1`), `design.md` referencing those IDs in every section with `**Satisfies:**` annotations, `tasks.md` with numbered work items each ending in `_Requirements: <ids>_`.
- **Coverage table** — `tasks.md` includes a coverage table mapping every requirement and NFR to the tasks that satisfy it. Every cell is populated.
- **Agent roster** — generic archetypes only (no domain-specific agents), with task-by-task assignments and coordination notes.
- **Phased prompts** — full set: a global master, four phase masters (one per phase), and twenty-two numbered task prompts. Every numbered prompt instantiates the production task-prompt shape (Objective / Context / Agent Assignment / Prerequisites / Task Details with current→target diff blocks / Acceptance Criteria). The detail level varies appropriately — Phase 0 spikes are scoped to exploration; Phase 1 backend prompts are most detailed; Phase 2 frontend prompts are component-scoped; Phase 3 validation prompts are procedural.
- **Implementation plan** — the operational layer that composes everything: schedule, resource assignment, critical path, risks watch, definition of done.

## How to read the example

If you're new to SpecForge, walk it in order:

1. [`sample-feature/prd.md`](sample-feature/prd.md) — start here. Read it as if you're a product reviewer.
2. [`sample-feature/requirements.md`](sample-feature/requirements.md) — see how PRD goals translate into stable-ID requirements.
3. [`sample-feature/design.md`](sample-feature/design.md) — see how requirements drive the architecture.
4. [`sample-feature/tasks.md`](sample-feature/tasks.md) — see how design decomposes into numbered work items with full back-references.
5. [`sample-feature/agent-roster.md`](sample-feature/agent-roster.md) — see how tasks are assigned to agent archetypes.
6. [`sample-feature/prompts/000_GLOBAL_MASTER.md`](sample-feature/prompts/000_GLOBAL_MASTER.md) — the agent CLI entry-point.
7. [`sample-feature/prompts/README.md`](sample-feature/prompts/README.md) — phase index of all 22 task prompts.
8. Open any phase master (e.g. [`phase1_backend/000_MASTER_backend.md`](sample-feature/prompts/phase1_backend/000_MASTER_backend.md)) to see how a phase scopes its tasks.
9. Open any numbered task prompt (e.g. [`phase1_backend/004_index_migration.md`](sample-feature/prompts/phase1_backend/004_index_migration.md) or [`phase1_backend/010_wire_endpoint.md`](sample-feature/prompts/phase1_backend/010_wire_endpoint.md)) — see the production task-prompt shape.
10. [`sample-feature/implementation-plan.md`](sample-feature/implementation-plan.md) — see the operational view.

The flow is the framework's value proposition in concrete form. If a step seems redundant, the redundancy is intentional — the cross-references between artifacts are how the work stays auditable.

## Adding more examples

Future examples should:

1. **Use a generic feature** — no domain-specific business logic (no financial, healthcare, legal, etc.).
2. **Exercise a different shape** — e.g. a refactor (use `technical-spec-template.md`), an architectural decision (use the ADR template), a single-team feature (use `lightweight-prd-template.md` and `feature-spec-template.md`).
3. **Cross-reference real templates** — link to `prds/templates/`, `specs/templates/`, `prompts/shared/` — don't reinvent.
4. **Include the implementation plan layer** — even small examples benefit from the operational view.

Suggested next examples (none built yet):

- **Lightweight feature**: a single-team feature using `lightweight-prd-template.md` + `feature-spec-template.md`.
- **Refactor**: a behavior-preserving refactor using `technical-spec-template.md`.
- **ADR**: a single architectural decision using the ADR template.

## Anti-patterns to avoid in examples

- **Theoretical content** — every section must be filled in concretely. "TODO: insert example" defeats the example's purpose.
- **Domain-specific naming** — generic only.
- **Mismatched cross-references** — the PRD's NFRs must match the requirements' NFRs must match the design's NFRs.
- **Drifted templates** — when SpecForge templates change, examples that exercise those templates need to be re-checked.

The `template-quality-reviewer` agent is the gate; see [`.claude/agents/template-quality-reviewer.md`](../.claude/agents/template-quality-reviewer.md).
