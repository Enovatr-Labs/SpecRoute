# Prompts: User Search

Phase index for the user-search worked example. This is the canonical demonstration of the SpecForge phased master-prompt pattern: one global master, four phase masters, twenty-two numbered task prompts.

## Layout

```
prompts/
├── 000_GLOBAL_MASTER.md             always read first
├── README.md                        this file (phase index)
├── phase0_foundation/
│   ├── 000_MASTER_foundation.md     phase entry-point
│   ├── 001_cache_ttl_spike.md       Q2: cache TTL choice
│   ├── 002_cursor_encoding_spike.md Q3: cursor encoding choice
│   └── 003_privacy_review.md        Q1: query-string logging policy
│
├── phase1_backend/
│   ├── 000_MASTER_backend.md
│   ├── 004_index_migration.md       Postgres indexes (CONCURRENTLY)
│   ├── 005_request_validator.md     pure validator function
│   ├── 006_rbac_scoping.md          organization filter injection
│   ├── 007_query_builder.md         parameterized SQL
│   ├── 008_cursor_encoding.md       HMAC-signed cursor with replay protection
│   ├── 009_cache_layer.md           Redis with single-flight stampede protection
│   ├── 010_wire_endpoint.md         compose validator → cache → query → response
│   ├── 011_observability.md         metrics + structured log + traces
│   └── 012_rate_limiting.md         100/min/actor at the gateway
│
├── phase2_frontend/
│   ├── 000_MASTER_frontend.md
│   ├── 013_search_input.md          debounced text input
│   ├── 014_filter_chips.md          role / status / created-at filters; mobile drawer
│   ├── 015_result_table.md          rows + empty / error / loading states
│   ├── 016_cursor_pagination.md     prev / next + URL state
│   └── 017_compose_page.md          /users/search page; E2E suite
│
├── phase3_validation/
│   ├── 000_MASTER_validation.md
│   ├── 018_load_test.md             100 RPS in staging; budgets confirmed
│   ├── 019_feature_flag.md          flag wiring (defense-in-depth)
│   ├── 020_production_rollout.md    10% → 50% → 100%, 7-day soak
│   ├── 021_documentation.md         API ref + admin guide + changelog
│   └── 022_rollback_drill.md        execute the rollback in staging
│
└── runtime/                         operational prompts (not task-implementation)
    ├── pickup-next-task.md          find the next unblocked task; route to its agent
    └── daily-checkpoint.md          scannable status across all four phases
```

## Operational (runtime) prompts

Two prompts under `runtime/` aren't tied to a specific task - they're the daily-driver prompts you run during execution:

- **`pickup-next-task.md`** - "what's next?" Reads `tasks.md`, finds the next unblocked task, identifies the primary agent, hands off cleanly.
- **`daily-checkpoint.md`** - "where are we?" Phase rollup, open questions, PRD acceptance criteria check, risks, next milestone.

## Phase summary

| Phase | Duration | Tasks | Goal |
|---|---|---|---|
| 0 - Foundation | 1 week | 1, 2, 3 | Resolve PRD open questions Q1–Q3 |
| 1 - Backend | 1 week | 4–12 | API endpoint live in develop |
| 2 - Frontend | 1 week | 13–17 | Search page wired and E2E tested |
| 3 - Validation | 1 week + 7d soak | 18–22 | Production at 100% with stable metrics |

Total: ~4 weeks elapsed (with parallel work; longer if serialized).

## How to read this directory

1. **Always start with [`000_GLOBAL_MASTER.md`](000_GLOBAL_MASTER.md).** It carries role, mission, source-of-truth references, architecture summary, and phase order.
2. Then the relevant phase master: `phase0_foundation/000_MASTER_foundation.md`, etc.
3. Then numbered task prompts in order.

Task prompts use the global task number from [`../tasks.md`](../tasks.md) (so `004_index_migration.md` implements task 4 in the work plan; `017_compose_page.md` implements task 17). The numbering is sticky; if a task is split or removed, surrounding tasks keep their numbers.

## What this demonstrates

This is the canonical example of the framework's phased master-prompt pattern. Read these alongside the templates in [`../../../prompts/shared/`](../../../prompts/shared/):

- [`global-master-prompt-template.md`](../../../prompts/shared/global-master-prompt-template.md) - the entry-point template that `000_GLOBAL_MASTER.md` instantiates.
- [`phase-master-prompt-template.md`](../../../prompts/shared/phase-master-prompt-template.md) - the phase-master template that each `000_MASTER_<phase>.md` instantiates.
- [`task-prompt-template.md`](../../../prompts/shared/task-prompt-template.md) - the production task-prompt shape that every numbered task prompt instantiates.

The detail level varies appropriately:

- **Phase 0** prompts are scoped to spikes / reviews - output is a decision, not code. Shorter.
- **Phase 1** prompts are full production task prompts - exhaustive Files-to-Modify, Step-by-step, Acceptance Criteria. Most detailed.
- **Phase 2** prompts are component-scoped - clean component contracts, accessibility checklists, state matrices.
- **Phase 3** prompts are procedural - load-test profiles, rollout stages, communication plans.

## Cross-references that resolve

Every prompt back-references:

- The PRD section that motivates the task.
- The requirement IDs from `requirements.md` (R*, NFR-*).
- The design section that specifies the implementation.
- The phase master and global master.
- Adjacent tasks (predecessors, successors, parallels).

These cross-references make the prompt set navigable. A reader at any prompt can quickly find the PRD context, the spec requirement, the design contract, and the upstream/downstream dependencies.

## Adapting this pattern

For your own initiative:

1. Use [`global-master-prompt-template.md`](../../../prompts/shared/global-master-prompt-template.md) as your `000_GLOBAL_MASTER.md`.
2. Pick a phase structure that fits your work (4 phases is a common shape; could be 2 or 8).
3. For each phase, use [`phase-master-prompt-template.md`](../../../prompts/shared/phase-master-prompt-template.md).
4. For each numbered task, use [`task-prompt-template.md`](../../../prompts/shared/task-prompt-template.md). Adjust the detail level to match the task's complexity.
5. Number tasks globally (matching `tasks.md` numbering) - makes cross-references trivial.

The discipline is in the cross-references. Without them, the prompt set drifts; with them, the implementation team has a single coherent execution document.
