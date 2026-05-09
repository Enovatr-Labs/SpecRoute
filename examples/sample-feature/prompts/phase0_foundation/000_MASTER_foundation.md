# 000_MASTER_foundation - Phase 0: Foundation and Spikes

> Phase entry-point. Read this before any task in Phase 0.

---

## Phase Summary

Phase 0 resolves the open questions from the PRD and design that block Phase 1 implementation. There are three open questions (Q1, Q2, Q3 from `requirements.md` Section 7) plus an index-plan validation that needs staging access. None of these are coding work in the strict sense - they're spikes, reviews, and validations.

The output of Phase 0 is decisions, not code. Phase 1 starts only when the decisions are recorded in the design doc and the privacy review is signed off.

## Goals

By the end of Phase 0:

1. Cache TTL choice made (Q2 resolved).
2. Cursor encoding choice made (Q3 resolved).
3. Privacy review signed off (Q1 resolved).

## Prerequisites

- [ ] PRD `Status: Approved`.
- [ ] Spec triplet `Status: Approved`.
- [ ] Staging Postgres available with synthetic data approximately matching production scale.
- [ ] Privacy lead identified and engaged.

## Task Prompts

| # | Task | Primary Agent | Supporting Agents |
|---|---|---|---|
| 001 | [`001_cache_ttl_spike.md`](001_cache_ttl_spike.md) | `backend-engineer` | `deployment-validator` |
| 002 | [`002_cursor_encoding_spike.md`](002_cursor_encoding_spike.md) | `backend-engineer` | `security-auditor` |
| 003 | [`003_privacy_review.md`](003_privacy_review.md) | `security-auditor` | (privacy lead, human) |

Tasks 001 and 002 can run in parallel. Task 003 runs in parallel with both - it's blocking on a human reviewer, not on engineering work.

## Agent Assignments

- **`backend-engineer`** - runs the cache TTL and cursor encoding spikes.
- **`security-auditor`** - leads the privacy review; advises the cursor encoding spike on signature/replay-protection trade-offs.
- **`deployment-validator`** - runs staging measurements during the cache TTL spike.

Read each agent's `.md` file under `.claude/agents/` (or the project's equivalent) for operating principles.

## Acceptance Criteria

Phase 0 is complete when **all** of the following are true:

- [ ] Cache TTL decided; recorded in [`../../design.md`](../../design.md) Section 7 and Section 12 (Alternatives Considered).
- [ ] Cursor encoding decided; recorded in [`../../design.md`](../../design.md) Section 6 (State Management).
- [ ] Privacy review signed off; recorded in [`../../prd.md`](../../prd.md) Section 17.
- [ ] Q1, Q2, Q3 in [`../../requirements.md`](../../requirements.md) Section 7 marked resolved.
- [ ] No new requirements added without a follow-up `requirements.md` revision.

## Risks Specific to Phase 0

| Risk | Mitigation |
|---|---|
| Privacy review delays Phase 1 | Engage privacy lead at PRD review; have a fallback "no-query-logging" variant prepared if approval is denied for the rich variant. |
| Spike findings invalidate the design | Update `design.md` first; re-circulate for a quick re-approval; do not start Phase 1 against a stale design. |
| Spikes turn into implementation work | Stop the spike at decision time. Implementation belongs to Phase 1. |

## How to Execute

1. Read [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md).
2. Read this file end to end.
3. Confirm prerequisites.
4. Open and execute the three tasks (in any order; they're independent).
5. After each task, update the design / PRD / requirements as the task specifies.
6. When all three tasks are closed, validate against the acceptance criteria.
7. Promote to Phase 1 (open [`../phase1_backend/000_MASTER_backend.md`](../phase1_backend/000_MASTER_backend.md)).
