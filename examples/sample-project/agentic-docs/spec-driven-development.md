# Spec-Driven Development in This Project

How the spec-driven flow plays out concretely for user-search.

## The flow, with file pointers

```
prds/active/user-search.md           PRD (Status: Approved)
└── specs/user-search/requirements.md   stable IDs (R1.1 ... NFR-4.1)
    └── specs/user-search/design.md     architecture, data model, APIs
        └── specs/user-search/tasks.md  22 numbered tasks; back-refs to R*
            └── prompts/                phased execution
                ├── 000_GLOBAL_MASTER.md
                ├── phase0_foundation/  3 spike + review prompts
                ├── phase1_backend/     9 backend implementation prompts
                ├── phase2_frontend/    5 frontend implementation prompts
                └── phase3_validation/  5 validation + rollout prompts
```

`adrs/` captures specific architectural decisions surfaced during the flow.

## Stage gates we observe

| Stage | Output | Gate |
|---|---|---|
| PRD draft | [`prds/active/user-search.md`](../prds/active/user-search.md) Draft | All 23 sections populated; open questions listed |
| PRD approved | Status: Approved | Stakeholder sign-off; Q1, Q2, Q3 either resolved or have owners + dates |
| Spec triplet drafted | `specs/user-search/{requirements,design,tasks}.md` | Coverage table fully populated |
| Spec approved | Status: Approved on each | Open design questions resolved; alternatives-considered section captures rejected approaches |
| Implementation | Tasks merged with PRs | Each task back-references requirement IDs; each requirement has a passing test |
| Validation | Phase 3 load test pass | NFR-1.1 (p95 < 200ms), NFR-1.2 (p99 < 500ms), NFR-1.3 (100 RPS) all met in staging |
| Rollout complete | Status: Shipped | 7-day soak at 100% traffic with stable metrics; PRD §23 acceptance criteria all checked |

## Cross-references that survive across stages

The reason the flow works is that the artifacts are **linked**, not just sequenced:

- **PRD §3 Goals** drive **requirements user stories** which drive **specific R-IDs**.
- **R-IDs** appear in **`design.md`** sections (`**Satisfies:** R1.1, NFR-1.1`) so it's clear which design choice satisfies which requirement.
- **R-IDs** appear in **`tasks.md`** as back-refs (`_Requirements: R1.1, R1.2_`) so it's clear which task implements which requirement.
- **Task numbers** appear in **task prompts** ("this is task 4 in `tasks.md`").
- **Task numbers** appear in **agent-roster.md** under task assignments.
- **R-IDs** appear in **test names** (`test_when_<event>_then_<system>_<action>`) so test failures point to the requirement.

When all these survive, a reviewer can land at any point in the chain and trace forward or backward.

## Open questions are first-class

Q1, Q2, Q3 (in `requirements.md` §7 originally) blocked Phase 1 entry. They were resolved in Phase 0:

- **Q1** (privacy review for query logging) -> [ADR-005](../adrs/adr-005-filter-set-hash-logging.md)
- **Q2** (cache TTL choice) -> [ADR-003](../adrs/adr-003-redis-cache-60s-ttl.md)
- **Q3** (cursor encoding) -> [ADR-004](../adrs/adr-004-hmac-signed-cursors.md)

## What this looks like in agents' day-to-day

When an agent picks up a task:

1. Reads the task in `tasks.md` (e.g. task 7).
2. Reads each `R-ID` the task back-references.
3. Reads the relevant `design.md` sections (the task names them in its Section 2 Context block).
4. Implements only what the task specifies (Files to Modify / Create / Delete).
5. Writes tests that name the back-referenced requirement IDs.
6. Opens a PR linking the task.

If reality conflicts with the design, the agent stops and updates `design.md` first - not silently diverges.

## See also

- The framework's canonical [`agentic-docs/spec-driven-development.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/agentic-docs/spec-driven-development.md) for the methodology in general.
- [`implementation-plan.md`](../implementation-plan.md) for the schedule and phase dependencies in this project.
- [`prompts/runtime/pickup-next-task.md`](../prompts/runtime/pickup-next-task.md) - the daily-driver "what's next?" prompt.
