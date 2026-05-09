# Task 018: Load Test Against Staging

> Production task prompt. Phase 3 validation gate.

---

## 1. Objective

Run a load test against the staging environment with the full backend + frontend stack deployed. Confirm performance budgets (NFR-1.x) hold under sustained 100 RPS and identify any neighbor regressions.

After this task: load test report attached to the PRD; p95 < 200ms and p99 < 500ms confirmed; no regressions on neighboring endpoints; Phase 3 advances.

## 2. Context

**PRD Reference**: [`../../prds/active/user-search.md`](../../prds/active/user-search.md) Section 18 (Performance Requirements)
**Spec Reference**: [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) - NFR-1.1, NFR-1.2, NFR-1.3
**Architecture Reference**: [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 7 (Performance Considerations)
**Phase Master**: [`000_MASTER_validation.md`](000_MASTER_validation.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 18. Depends on Phase 1 + Phase 2 acceptance. Gates task 020 (production rollout).

## 3. Agent Assignment

**Primary Agent**: `deployment-validator`
**Supporting Agents**:

- `backend-engineer` - interprets latency profile; identifies optimization opportunities if budgets are exceeded.

## 4. Prerequisites

- [ ] Phase 2 acceptance met.
- [ ] Staging environment matches production schema and approximate scale.
- [ ] Existing load-test harness available, or one provisioned for this exercise.
- [ ] Baseline latency captured for neighboring endpoints (so regression detection is meaningful).

## 5. Task Details

### 5.1 Profile

- **Tool**: project's standard load runner (k6 / locust / Gatling / equivalent).
- **Duration**: 10 minutes sustained.
- **Throughput**: 100 RPS sustained against `/api/users/search`.
- **Query mix**: ~40% repeated within the cache TTL (test cache hit path), ~40% repeated within 60s–300s, ~20% unique. Match against admin telemetry distribution if available.
- **Filter mix**: realistic distribution of single-filter, two-filter, and multi-filter queries.
- **RBAC mix**: ~80% admin actor, ~20% non-admin actor.

### 5.2 Metrics to capture

| Metric | Target | Capture source |
|---|---|---|
| Endpoint p50 | < 50ms | `search.duration_ms{quantile="0.50"}` |
| Endpoint p95 | < 200ms | `search.duration_ms{quantile="0.95"}` (NFR-1.1) |
| Endpoint p99 | < 500ms | `search.duration_ms{quantile="0.99"}` (NFR-1.2) |
| Cache hit rate (steady state) | > 40% | `search.cache_hit_rate` |
| Error rate | < 0.1% | `search.errors_total / search.requests_total` |
| Neighbor endpoint p95 (e.g. `/api/users` legacy) | within 10% of pre-test baseline | `users.list.duration_ms{quantile="0.95"}` |
| Database CPU | < 70% sustained | database host CPU dashboard |
| Redis CPU | < 50% sustained | Redis host CPU dashboard |

### 5.3 Pass / fail decision

PASS if all targets met. FAIL otherwise - investigate and fix before advancing. Possible fix paths:

- p95 high → investigate query plan; possibly add an index missed in task 4.
- Cache hit rate low → revisit the TTL choice from Phase 0 task 001.
- Neighbor regression → investigate connection pool sizing; Postgres connection contention.

### 5.4 Files to Modify

| File | Change |
|---|---|
| `tests/load/users-search.<extension>` (or equivalent) | Create - load test script |
| Validation report | Append the load test results |
| [`../../prds/active/user-search.md`](../../prds/active/user-search.md) | Update Section 18 with measured numbers |

## 6. Acceptance Criteria

- [ ] Load test ran against staging for 10 minutes at 100 RPS.
- [ ] All metrics in the table captured.
- [ ] All targets met.
- [ ] Report attached to PRD.
- [ ] No regressions on neighboring endpoints.

## 7. Out of Scope

- Production load testing - out of v1; production validation comes from the gradual rollout.
- Stress testing beyond 100 RPS - out of scope unless budgets fail.

## 8. Validation

The load test itself is the validation. Re-run if any infrastructure changes between this task and production rollout.

## 9. Rollback

If the load test fails: stop. Don't advance to production rollout. Investigate, fix, re-run.
