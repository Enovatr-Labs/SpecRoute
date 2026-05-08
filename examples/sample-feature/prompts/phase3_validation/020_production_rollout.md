# Task 020: Production Rollout 10% → 50% → 100%

> Production task prompt. Phase 3 — the actual go-live.

---

## 1. Objective

Roll out `users.search.enabled` to production traffic gradually. Monitor metrics and triggers at each stage. Advance only when metrics are stable. Total wall-clock duration: at least 9 days (1d at 10%, 1d at 50%, 7d at 100%).

After this task: 100% production traffic with stable error rates and latency for 7 days; PRD success metrics measured against targets.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 19 (Rollback Strategy), Section 23 (Acceptance Criteria)
**Spec Reference**: (rollout, not requirement-specific)
**Architecture Reference**: [`../../design.md`](../../design.md) Section 11 (Rollout Considerations)
**Phase Master**: [`000_MASTER_validation.md`](000_MASTER_validation.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 20. Depends on tasks 18 (load test passed), 019 (feature flag wired), 021 (docs ready), 022 (rollback drill). All must be complete.

## 3. Agent Assignment

**Primary Agent**: `deployment-validator`
**Supporting Agents**:

- `backend-engineer` — on call for triage if metrics regress.

## 4. Prerequisites

- [ ] Tasks 18, 019, 021, 022 complete.
- [ ] On-call team briefed.
- [ ] Customer comms drafted (if applicable).
- [ ] Monitoring dashboards live and accessible.
- [ ] No active P0/P1 incidents.

## 5. Task Details

### 5.1 Stage 20a: 10% rollout

- Toggle `users.search.enabled` to 10% of actors in production.
- Monitor for 24 hours:
  - Error rate stays within baseline + 0.1%.
  - p95 latency stays within budget (NFR-1.1 < 200ms).
  - p99 latency within budget (NFR-1.2 < 500ms).
  - No P0/P1 incidents related to the search endpoint.
  - Customer reports: zero negative.
- If any metric breaches: trigger rollback per Section 9. Fix; re-run from staging through 18 → 020a.

### 5.2 Stage 20b: 50% rollout

- After 24h of stable 10%, advance to 50%.
- Monitor for 24 hours with the same gates as 20a.
- Watch for cache stampede patterns at the higher traffic.
- If any metric breaches: rollback to 10% (or off, depending on severity).

### 5.3 Stage 20c: 100% rollout

- After 24h of stable 50%, advance to 100%.
- Monitor for 7 days.
- Compare measured success metrics (PRD Section 3.3) against targets:
  - Time-to-find median < 2s.
  - Cache hit rate > 40% steady state.
  - Admin session length when lookup is involved < 1.5× baseline.

### 5.4 Communication plan

| Milestone | Notify |
|---|---|
| 10% begins | Engineering team, product owner |
| 50% begins | Engineering team |
| 100% begins | Engineering team, product owner, support |
| 100% stable for 7 days | All stakeholders + customers (if user-visible) |

## 6. Acceptance Criteria

- [ ] 10% stage stable for 24h.
- [ ] 50% stage stable for 24h.
- [ ] 100% stage stable for 7 days.
- [ ] Success metrics measured at 100% and within targets.
- [ ] PRD acceptance criteria (Section 23) all checked.
- [ ] No active P0/P1 incidents related to user search.

## 7. Out of Scope

- Marketing announcements — handled separately by product / marketing.
- Customer support training — handled by the support handover before this task.
- Post-launch enhancements — out of v1; queue as new PRDs.

## 8. Validation

Validation is continuous monitoring during the rollout. The metrics dashboards are the authoritative view.

## 9. Rollback

Triggers (per PRD Section 19.1):

- p95 latency > 500ms sustained for 5 minutes.
- Error rate > 1% sustained for 5 minutes.
- Customer-reported correctness regression with reproduction.

Procedure:

1. Toggle `users.search.enabled` to 0% (full off).
2. Frontend falls back to `/users`.
3. Verify error rates drop below threshold within 1 minute.
4. Open incident ticket. Investigate.
5. Fix in develop, validate in staging (re-run task 18), re-attempt rollout from 10%.

The rollback drill in task 022 validated that this procedure works.
