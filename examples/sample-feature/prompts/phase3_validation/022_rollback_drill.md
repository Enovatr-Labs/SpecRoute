# Task 022: Rollback Drill in Staging

> Production task prompt. Phase 3 - final gate before production rollout.

---

## 1. Objective

Execute the rollback procedure in staging end-to-end. Confirm the procedure works, the metrics drop as expected, and the recovery path is clean. An untested rollback is no rollback.

After this task: rollback drill outcome recorded in PRD Section 19; staging recovers to baseline within 5 minutes of trigger.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 19 (Rollback Strategy)
**Spec Reference**: (rollout, not requirement-specific)
**Architecture Reference**: [`../../design.md`](../../design.md) Section 11 (Rollout Considerations)
**Phase Master**: [`000_MASTER_validation.md`](000_MASTER_validation.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 22. Depends on task 019 (feature flag wired) and task 18 (load test passed). Gates task 020 (production rollout).

## 3. Agent Assignment

**Primary Agent**: `deployment-validator`
**Supporting Agents**:

- `backend-engineer` - observes the rollback; confirms recovery in metrics.

## 4. Prerequisites

- [ ] Task 019 (feature flag) merged.
- [ ] Staging environment running the full release candidate.
- [ ] Metrics dashboards live in staging.
- [ ] On-call team aware (so they don't think a real incident is happening).

## 5. Task Details

### 5.1 Drill scenario

Simulate a triggered rollback scenario: the search endpoint exhibits sustained latency regression in staging. Use the rollback procedure documented in PRD Section 19.2.

### 5.2 Procedure to execute

1. **Setup**: Enable `users.search.enabled` in staging at 100%. Run the load test from task 18 to establish baseline metrics.
2. **Inject**: Introduce a synthetic latency regression - e.g. add a 1-second sleep to the cache hit path, or force the cache to always miss. The goal is to make p95 cross the 500ms rollback threshold.
3. **Detect**: Confirm the on-call alert fires (or simulate the trigger if alerts haven't been wired yet).
4. **Trigger**: Toggle `users.search.enabled` to 0%.
5. **Recover**: Watch metrics. Within 1 minute, error rate and latency should drop to baseline (no requests are reaching the regression).
6. **Verify**: Frontend `/users/search` shows the fallback message. The `/users` page works normally.
7. **Reset**: Remove the synthetic regression. Re-enable the flag. Re-run a brief load test to confirm clean state.

### 5.3 Files to Modify

| File | Change |
|---|---|
| [`../../prd.md`](../../prd.md) | Update Section 19 with the drill date and outcome |
| Validation report | Record the drill |
| (Synthetic regression code) | Remove after the drill - never ship to production |

## 6. Acceptance Criteria

- [ ] Drill executed end-to-end in staging.
- [ ] Trigger fires (or is documented as a known gap if alerts aren't wired).
- [ ] Toggle off → metrics recover within 1 minute.
- [ ] Frontend falls back cleanly.
- [ ] After re-enable, system returns to clean state.
- [ ] PRD Section 19 updated with drill date and outcome.
- [ ] Synthetic regression removed.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Production rollback drill - production rollout itself is the test of the rollback at scale.
- Multi-failure scenarios (e.g. cache + DB both regressed) - out of scope for v1; standard playbooks cover compounded failures.

## 8. Validation

The drill itself is the validation. Recovery time is the metric - under 5 minutes from trigger to baseline is acceptable; under 1 minute is the target.

## 9. Rollback

If the drill goes wrong (e.g. the synthetic regression causes a real outage in staging that doesn't recover): treat as a real staging incident. Standard incident playbooks apply.

This task is fundamentally a deliberate failure exercise - having a runbook for "the drill itself failed" is appropriate.
