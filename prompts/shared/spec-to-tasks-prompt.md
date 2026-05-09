# Prompt: Spec → Tasks

Derive `tasks.md` from approved `requirements.md` and `design.md`. Use this when the spec triplet's first two files exist but the implementation work plan hasn't been laid out yet.

---

## Role

You are a **spec-author** producing the implementation work plan. Your input is the approved requirements and design; your output is a numbered, phase-organized task list with full requirement back-references.

## Inputs

- `<path/to/spec/requirements.md>` (Status: `Approved`)
- `<path/to/spec/design.md>` (Status: `Approved`)
- (Optional) `<path/to/prd.md>` for migration phase guidance

If either source file is not `Approved`, stop and report.

## Output

`<path/to/spec/tasks.md>` using [`specs/templates/tasks-template.md`](../../specs/templates/tasks-template.md).

## Process

### 1. Identify phases

Read PRD Section 15 (Migration Phases) if available. Otherwise group requirements by:

- **Phase 1: Foundation** - schema, migrations, scaffolding.
- **Phase 2: Core** - the primary user-facing functionality.
- **Phase 3: Edge cases** - error paths, validation, resilience.
- **Phase 4: Operationalization** - observability, runbooks, rollback testing.

Adjust phase boundaries to match the architecture's natural seams.

### 2. Decompose into tasks

For each requirement:

- One or more tasks that, together, satisfy it.
- Each task is small enough to land in one PR (rule of thumb: <2 days of work).
- Each task lists concrete sub-steps.
- Each task ends with `_Requirements: R<N.M>, R<N.M>_` back-references.

For each NFR:

- A task that adds the corresponding measurement (metric, log, trace, test).
- A task that validates the budget is met.

### 3. Sequence tasks

Number tasks globally (1, 2, 3, …, not restarting per phase). Numbering is sticky - tasks merged into `tasks.md` keep their numbers forever.

Order:

- Foundational tasks (schema, scaffolding, contracts) come first.
- Tasks that consume foundational state come after.
- Cross-cutting tasks (observability, validation) come last in their phase.

### 4. Populate coverage table

The coverage table is the gate. Every `R<N.M>` and every `NFR-<N.M>` must map to at least one task.

| Requirement / NFR | Tasks |
|---|---|
| R1.1 | 1, 2 |
| R1.2 | 2 |
| NFR-1.1 | 5 |
| ... | ... |

A row showing `TODO` is a coverage gap - fix it before submitting.

### 5. Done checklist

The done checklist at the bottom of `tasks.md` defines completion. Confirm:

- All tasks checked off (boxes ticked).
- Coverage table fully populated.
- Tests passing for every requirement.
- NFRs measured and within budget.
- PRD acceptance criteria met.

## Quality bar

`tasks.md` is acceptable when:

- Every requirement (R*) and NFR (NFR-*) is in the coverage table with at least one task.
- Every task back-references at least one requirement.
- Tasks are sequenced - no task depends on a later-numbered task.
- Each task is small enough that "merge in one PR" is realistic.

## Anti-patterns to avoid

- **Tasks without back-refs.** Looks like progress until someone asks "what does this satisfy?" and nobody can answer.
- **Tasks that bundle multiple requirements.** Hard to review. Split.
- **Tasks that reference future requirements not yet in `requirements.md`.** That's spec drift; update `requirements.md` first.
- **Coverage gaps.** A requirement without a task is unimplemented - surface it.

## Final step

Run `/audit` for cross-reference validation. Submit `tasks.md` with `Status: Draft`. Promote to `Approved` after the spec-author and a code reviewer have signed off.
