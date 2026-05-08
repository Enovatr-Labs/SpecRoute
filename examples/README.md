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
    ├── prompts/
    │   ├── 000_master.md           global master prompt (entry-point)
    │   ├── 001_index_migration.md  production task prompt (Phase 1)
    │   └── 002_implement_search_endpoint.md   production task prompt (Phase 1)
    └── implementation-plan.md      operational view (schedule, resources, risks)
```

## What `sample-feature/` demonstrates

The `user-search` feature exercises every artifact shape in SpecForge:

- **PRD** — the full 23-section enterprise template ([`prds/templates/prd-template.md`](../prds/templates/prd-template.md)). Real product framing, success metrics, scope boundaries, performance budgets, security requirements.
- **Spec triplet** — `requirements.md` with stable IDs (`R1.1` through `NFR-4.1`), `design.md` referencing those IDs in every section with `**Satisfies:**` annotations, `tasks.md` with numbered work items each ending in `_Requirements: <ids>_`.
- **Coverage table** — `tasks.md` includes a coverage table mapping every requirement and NFR to the tasks that satisfy it. Every cell is populated.
- **Agent roster** — generic archetypes only (no domain-specific agents), with task-by-task assignments and coordination notes.
- **Phased prompts** — a master prompt that links the PRD, design, and task list; two numbered task prompts (the migration and the endpoint composition) showing the production task-prompt shape (Objective / Context / Agent Assignment / Prerequisites / Task Details with current→target diff blocks / Acceptance Criteria).
- **Implementation plan** — the operational layer that composes everything: schedule, resource assignment, critical path, risks watch, definition of done.

A real project would have one numbered prompt per task in `tasks.md` (so 22 prompts for this feature). The two shown here exercise the production prompt template end to end.

## How to read the example

If you're new to SpecForge, walk it in order:

1. [`sample-feature/prd.md`](sample-feature/prd.md) — start here. Read it as if you're a product reviewer.
2. [`sample-feature/requirements.md`](sample-feature/requirements.md) — see how PRD goals translate into stable-ID requirements.
3. [`sample-feature/design.md`](sample-feature/design.md) — see how requirements drive the architecture.
4. [`sample-feature/tasks.md`](sample-feature/tasks.md) — see how design decomposes into numbered work items with full back-references.
5. [`sample-feature/agent-roster.md`](sample-feature/agent-roster.md) — see how tasks are assigned to agent archetypes.
6. [`sample-feature/prompts/000_master.md`](sample-feature/prompts/000_master.md) — see the agent CLI entry-point.
7. [`sample-feature/prompts/001_index_migration.md`](sample-feature/prompts/001_index_migration.md) and [`002_implement_search_endpoint.md`](sample-feature/prompts/002_implement_search_endpoint.md) — see the production task-prompt shape.
8. [`sample-feature/implementation-plan.md`](sample-feature/implementation-plan.md) — see the operational view.

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
