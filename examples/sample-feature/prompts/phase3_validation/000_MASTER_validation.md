# 000_MASTER_validation - Phase 3: Validation and Rollout

> Phase entry-point. Read this before any task in Phase 3.

---

## Phase Summary

Phase 3 validates the feature against its spec and rolls it to production. This is procedural work - the implementation is done; this phase is about gates, monitoring, and the deliberate ramp from 0 → 100% production traffic.

The phase opens with a load test (task 18) and closes with the rollback drill (task 22) executed in staging. Production rollout (task 20) runs over the 7-day soak window described in `release-readiness.md`.

## Goals

By the end of Phase 3:

1. Load test confirms NFR-1.x performance budgets met.
2. Feature flag `users.search.enabled` works on/off; develop deploy gated.
3. Production at 100% traffic with stable metrics for 7 days.
4. Documentation updated per PRD Section 12.
5. Rollback procedure drilled and confirmed.
6. PRD acceptance criteria (Section 23) all checked.

## Prerequisites

- [ ] Phase 2 acceptance met.
- [ ] Develop environment runs the full stack.
- [ ] Staging environment mirrors production.
- [ ] On-call team identified for production rollout window.

## Task Prompts

| # | Task | Primary Agent | Supporting Agents |
|---|---|---|---|
| 018 | [`018_load_test.md`](018_load_test.md) | `deployment-validator` | `backend-engineer` |
| 019 | [`019_feature_flag.md`](019_feature_flag.md) | `backend-engineer` | `frontend-engineer` |
| 020 | [`020_production_rollout.md`](020_production_rollout.md) | `deployment-validator` | `backend-engineer` |
| 021 | [`021_documentation.md`](021_documentation.md) | `prd-author` | `spec-author` |
| 022 | [`022_rollback_drill.md`](022_rollback_drill.md) | `deployment-validator` | `backend-engineer` |

### Execution order

```
    018 (load test)
       │
       ▼
    019 (feature flag wiring)         021 (documentation)
       │                                 │
       ▼                                 │
    022 (rollback drill in staging)      │
       │                                 │
       └────────► 020 (production rollout) ◄──┘
                  │
                  ▼
              (7-day soak)
```

021 (documentation) and 022 (rollback drill) gate 020 (rollout). 018 (load test) gates 019 (feature flag).

## Agent Assignments

- **`deployment-validator`** - load test, rollback drill, production rollout.
- **`backend-engineer`** - feature flag wiring; supports rollout monitoring.
- **`frontend-engineer`** - feature flag on the frontend side (fallback to existing `/users` page).
- **`prd-author`** - documentation updates (API reference, admin user guide, changelog).

## Acceptance Criteria

Phase 3 is complete when **all** of the following are true:

- [ ] Load test report attached to PRD: p95 < 200ms, p99 < 500ms, no neighbor regression at 100 RPS sustained.
- [ ] Feature flag works: off → 404 endpoint + frontend falls back to `/users`; on → full feature.
- [ ] Rollback drilled in staging; documented in PRD Section 19.
- [ ] Documentation merged: API reference, admin guide, changelog (per PRD Section 12).
- [ ] Production rollout: 10% → 50% → 100% completed.
- [ ] 100% traffic stable for 7 days (no P0/P1 incidents related to user search; success metrics within target).
- [ ] All PRD acceptance criteria (Section 23) checked.
- [ ] `/audit` returns clean.

## Risks Specific to Phase 3

| Risk | Mitigation |
|---|---|
| Load test reveals latency regression on neighboring endpoints | Investigate before flagging on; optimize index usage or DB connection pool |
| Feature flag fails to propagate cleanly | Test on/off in staging before production rollout |
| Production rollout uncovers a regression at 10% | Toggle flag off; investigate via structured logs (filter by `request_id`); fix; re-test in staging |
| 7-day soak window slips because of an unrelated incident | Pause the rollout at current % until the unrelated incident resolves; resume from there |

## How to Execute

1. Read [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md).
2. Read this file end to end.
3. Confirm Phase 2 acceptance is met.
4. Run task 018 (load test). Block on green.
5. Wire the feature flag (task 019).
6. Run the rollback drill in staging (task 022).
7. In parallel: write the docs (task 021).
8. Begin production rollout (task 020): 10% for 24h, 50% for 24h, 100% for 7d.
9. Validate against acceptance criteria.
10. Closeout per [`../../../workflows/release-readiness.md`](../../../workflows/release-readiness.md) and PRD Section 23.
