# Task 011: Add Observability Instrumentation

> Production task prompt. Phase 1 backend component.

---

## 1. Objective

Wire metrics, structured logs, and trace spans into the search endpoint so every request emits the four NFR-3 signals. Without this, the endpoint ships blind.

After this task: `search.duration_ms` (histogram), `search.filter_usage_total` (counter), `search.errors_total` (counter), and a structured log per request all appear in the project's monitoring system.

## 2. Context

**PRD Reference**: [`../../prds/active/user-search.md`](../../prds/active/user-search.md) Section 8.2 (Observability)
**Spec Reference**: [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) - NFR-3.1, NFR-3.2, NFR-3.3, NFR-3.4
**Architecture Reference**: [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 9
**Phase Master**: [`000_MASTER_backend.md`](000_MASTER_backend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 11. Depends on Phase 0 task 003 (privacy approval for log shape). Decorates components from tasks 5–9. Wired through task 10.
**Current File(s)**: `src/services/users/search/observability.py` (new).

## 3. Agent Assignment

**Primary Agent**: `backend-engineer`
**Supporting Agents**:

- `deployment-validator` - confirms metrics, logs, traces appear in develop's monitoring stack.

## 4. Prerequisites

- [ ] Phase 0 task 003 closed; log shape approved.
- [ ] Project has metrics, logging, tracing libraries configured.

## 5. Task Details

### 5.1 Metrics

| Metric name | Type | Labels |
|---|---|---|
| `search.duration_ms` | histogram | `cache_hit` (bool), `result_count_bucket` (e.g. `0`, `1-10`, `11-50`, `51+`) |
| `search.result_count` | histogram | (none) |
| `search.filter_usage_total` | counter | `filter_name` (`name`, `email`, `role`, `status`, `created_after`, `created_before`) |
| `search.errors_total` | counter | `error_code` (matches the validator's error code enum, plus `internal`) |

Histograms use the project's standard latency buckets (e.g. `[5, 10, 25, 50, 100, 200, 500, 1000, 2500, 5000]` ms).

### 5.2 Structured log

Every request emits exactly one structured log entry at `info` level:

```json
{
  "level": "info",
  "ts": "<iso8601>",
  "request_id": "<from middleware>",
  "service": "users-search",
  "actor_id": "<actor.id>",
  "filter_set_hash": "<sha256 of canonical filter set, hex truncated to 8 chars for readability>",
  "result_count": <int>,
  "duration_ms": <int>,
  "cache_hit": <bool>
}
```

Per the Phase 0 privacy review, **no plaintext query strings** appear in the log. The `filter_set_hash` allows analytics to group by query pattern without exposing values.

### 5.3 Trace spans

A trace span `users.search.handle_request` wraps the request handler. Sub-spans:

- `validate` (task 5)
- `apply_rbac` (task 6)
- `cache.get` (task 9)
- `query.execute` (task 7) - if cache miss
- `cache.populate` (task 9) - if cache miss
- `encode_cursor` (task 8)

Spans link to the parent span from the API gateway.

### 5.4 Files to Modify

| File | Change |
|---|---|
| `src/services/users/search/observability.py` | Create - metric registrations, log helper, span helper |
| `src/services/users/search/handler.py` (from task 10) | Decorate composition with metrics, logs, spans |
| `tests/services/users/search/test_observability.py` | Create - metrics emitted, log shape, span linkage |
| Monitoring dashboards | Update or create dashboards for the new metrics |

## 6. Acceptance Criteria

- [ ] All four metrics emitting with correct labels.
- [ ] Structured log per request, matching the approved shape.
- [ ] Trace spans linked to parent gateway span.
- [ ] Zero plaintext query strings in logs (manual verification + a unit test asserting no `name=` / `email=` field appears in log entries).
- [ ] Dashboards updated.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Alerts on the new metrics - see task 18 (load test) and the project's standard alerting workflow.
- Long-term log retention policy - separate workstream.

## 8. Validation

Unit tests assert metric calls happen at the right points. Integration test (in task 10) confirms metrics actually appear in the test instance of the metrics backend. Smoke against develop confirms dashboards populate.

## 9. Rollback

Observability is additive; rolling back via `git revert` removes the instrumentation but doesn't break the endpoint. Dashboards still work for whatever metrics persist.
