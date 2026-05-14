# Implementation Plan: User Search

**Version**: 1.0
**Date**: 2026-05-08
**Author**: SpecRoute worked example
**Status**: Approved
**Source PRD**: [`prds/active/user-search.md`](prds/active/user-search.md)
**Source Spec Triplet**: [`specs/user-search/requirements.md`](specs/user-search/requirements.md), [`specs/user-search/design.md`](specs/user-search/design.md), [`specs/user-search/tasks.md`](specs/user-search/tasks.md)
**Source Agent Roster**: [`agent-roster.md`](agent-roster.md)
**Source Master Prompt**: [`prompts/000_GLOBAL_MASTER.md`](prompts/000_GLOBAL_MASTER.md)

> The implementation plan is the operational view: who does what, when, with which dependencies, and how we know it landed cleanly. It composes the PRD, spec triplet, agent roster, and prompts into a single execution document.

---

## 1. Phase summary

| Phase | Duration | Tasks | Goal |
|---|---|---|---|
| 0 - Foundation | 1 week | 1, 2, 3 | Resolve open questions; validate index plan |
| 1 - Backend | 1 week | 4, 5, 6, 7, 8, 9, 10, 11, 12 | API endpoint working in develop |
| 2 - Frontend | 1 week | 13, 14, 15, 16, 17 | Search page wired and E2E tested |
| 3 - Validation & rollout | 1 week | 18, 19, 20, 21, 22 | Production at 100% with stable metrics |

Total: ~4 weeks, 22 tasks.

## 2. Critical path

The longest dependency chain runs through:

```
Task 4 (indexes)
   │
   ▼
Tasks 5, 6, 7, 8, 9, 11 (parallel sub-tasks)
   │
   ▼
Task 10 (compose endpoint)
   │
   ▼
Task 17 (compose frontend page) ─── depends on Task 10 + Tasks 13-16
   │
   ▼
Task 18 (load test)
   │
   ▼
Task 20 (production rollout)
```

Tasks **5, 6, 7, 8, 9, 11** are independent and can be parallelized after Task 4. Tasks **13, 14, 15, 16** are independent frontend components and can be parallelized.

Compression target: with two backend engineers and one frontend engineer working in parallel, this fits in 3 weeks. With one engineer per discipline, 4 weeks.

## 3. Resource assignment

Per [`agent-roster.md`](agent-roster.md):

| Role | Agent | Tasks owned |
|---|---|---|
| PRD / docs | `prd-author` | 21 |
| Backend implementation | `backend-engineer` | 5–12, 18, 19, 20, 22 (with `deployment-validator`) |
| Database | `database-engineer` | 4 |
| Frontend implementation | `frontend-engineer` | 13–17, 19 |
| Test authoring | `unit-test-writer`, `integration-test-generator` | embedded in implementation tasks |
| Security review | `security-auditor` | reviews tasks 6, 8, 10, 11, 12 |
| Operations | `deployment-validator` | 4 (validation), 18, 20, 22 |

A real project replaces these with real engineers; the agent assignments are the operational interface to either humans or AI agents driving the work.

## 4. Schedule

### Week 1: Phase 0

| Day | Task | Owner | Deliverable |
|---|---|---|---|
| Mon–Tue | Task 3 (privacy review) | `security-auditor` + privacy lead | Sign-off; PRD Section 17 updated |
| Mon–Wed | Task 1 (cache TTL spike) | `backend-engineer` + `deployment-validator` | TTL choice; design doc updated |
| Mon–Wed | Task 2 (cursor encoding spike) | `backend-engineer` + `security-auditor` | Encoding choice; design doc updated |
| Thu–Fri | Phase 0 review + Phase 1 kickoff prep | All | All Phase 0 tasks merged |

### Week 2: Phase 1

| Day | Task(s) | Owner | Deliverable |
|---|---|---|---|
| Mon | Task 4 (indexes migration) | `database-engineer` | Migration in develop; staging validation in flight |
| Tue–Thu | Tasks 5, 6, 7, 8, 9, 11 in parallel | `backend-engineer` | Components individually tested |
| Thu | Task 12 (rate limiting) | `backend-engineer` | Gateway config + integration test |
| Fri | Task 10 (compose endpoint) | `backend-engineer` | Endpoint live in develop |

### Week 3: Phase 2

| Day | Task(s) | Owner | Deliverable |
|---|---|---|---|
| Mon–Wed | Tasks 13, 14, 15, 16 in parallel | `frontend-engineer` | Components individually tested |
| Thu | Task 17 (compose page) | `frontend-engineer` | Page live in develop with E2E tests |
| Fri | Cross-team integration smoke | All | Develop env exercised end-to-end |

### Week 4: Phase 3

| Day | Task | Owner | Deliverable |
|---|---|---|---|
| Mon | Task 18 (load test) | `deployment-validator` | Load report; p95 < 200ms confirmed |
| Tue | Task 19 (feature flag wiring) | `backend-engineer` + `frontend-engineer` | Flag works on/off in staging |
| Tue–Wed | Task 22 (rollback drill) | `deployment-validator` | Rollback validated in staging |
| Wed | Task 21 (documentation) | `prd-author` | Docs PR merged |
| Thu | Task 20a (10% production rollout) | `deployment-validator` | Stable for 24h |
| Fri | Task 20b (50% rollout) | `deployment-validator` | Stable for 24h |
| Following week | Task 20c (100% rollout) | `deployment-validator` | Stable for 7 days; declare complete |

## 5. Risks watch

Pulled forward from PRD Section 21:

| Risk | Trigger | Owner | Mitigation in flight? |
|---|---|---|---|
| Privacy review delays Phase 1 | Q1 not resolved by end of week 1 | `security-auditor` | Yes - engaged at PRD review |
| Index creation locks production table | Long lock observed in staging | `database-engineer` | Validated `CONCURRENTLY` in staging week 2 |
| Cache stampede on popular query | First-week production traffic | `backend-engineer` | Single-flight implemented in Task 9 |
| RBAC bypass via crafted cursor | Detected by `security-auditor` review | `backend-engineer` | HMAC-signed cursors; replay protection |

## 6. Definition of done

The implementation is complete when **every** item in PRD Section 23 is checked **and**:

- [ ] All 22 tasks marked complete in `specs/user-search/tasks.md`.
- [ ] Coverage table in `specs/user-search/tasks.md` fully populated.
- [ ] Open questions Q1, Q2, Q3 resolved.
- [ ] Production traffic at 100% with stable metrics for 7 days.
- [ ] No active P0 / P1 incidents related to user search.
- [ ] Documentation PR merged (Task 21).
- [ ] Rollback drill executed in staging (Task 22).

## 7. Communication plan

- **Daily**: brief async update in the project channel - what shipped, what's blocked.
- **Weekly**: phase-review meeting at end of each week. Confirm phase exit criteria are met before advancing.
- **Incidents**: standard incident protocol; the rollback feature flag is the first lever.
- **PRD updates**: any scope change goes through PRD revision before implementation pivots.

## 8. Post-implementation

Two weeks after 100% rollout:

- **Metrics review**: do we hit the targets in PRD Section 3.3? Time-to-find < 2s? p95 < 200ms? Cache hit > 40%?
- **Lessons-learned doc**: written by `prd-author` based on the team's retrospective.
- **PRD status**: flip from `In Implementation` to `Shipped`; move to `prds/archive/`.
- **Spec triplet**: status `Complete`. Move to `specs/archive/<feature>/` if the project archives specs.
- **Open follow-ups**: any deferred items become new PRDs (e.g. saved searches, bulk export).

---

## Appendix: Cross-references

This document is the operational view. The authoritative content lives elsewhere:

| Question | Read |
|---|---|
| What are we building and why? | [`prds/active/user-search.md`](prds/active/user-search.md) |
| What must be true? | [`specs/user-search/requirements.md`](specs/user-search/requirements.md) |
| How do we build it? | [`specs/user-search/design.md`](specs/user-search/design.md) |
| What's the work plan? | [`specs/user-search/tasks.md`](specs/user-search/tasks.md) |
| Who runs each task? | [`agent-roster.md`](agent-roster.md) |
| How do agents pick up the work? | [`prompts/000_GLOBAL_MASTER.md`](prompts/000_GLOBAL_MASTER.md) and the numbered task prompts |
