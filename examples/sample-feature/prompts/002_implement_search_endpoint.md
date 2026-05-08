# Task 002: Implement `GET /api/users/search` Endpoint

> Production task prompt. Phase 1 mid-point (composes earlier Phase 1 components).

---

## 1. Objective

Wire `GET /api/users/search` end-to-end: accept the request, validate, RBAC-scope, cache lookup, query, response shape, observability. After this task, the endpoint serves real traffic in develop with full filter coverage and meets p95 < 200ms in synthetic load.

## 2. Context

**PRD Reference**: [`../prd.md`](../prd.md) Section 5 (Target Architecture), Section 10 (Backend / Integration Contracts)
**Spec Reference**: [`../requirements.md`](../requirements.md) — Requirements: R1.1, R1.2, R1.3, R2.1, R3.1, R4.1, R4.2, R5.1, R5.2, R5.3, NFR-1.1, NFR-2.1, NFR-2.2, NFR-2.3, NFR-3.1, NFR-3.3, NFR-3.4
**Architecture Reference**: [`../design.md`](../design.md) Section 2 (Architecture), Section 4 (API Contracts), Section 7 (Performance), Section 8 (Security), Section 9 (Observability)
**Phase Master**: [`000_master.md`](000_master.md)
**Related Tasks**: this is task 10 in [`../tasks.md`](../tasks.md). Depends on tasks 4 (indexes), 5 (validator), 6 (RBAC scoping), 7 (query builder), 8 (cursor), 9 (cache), 11 (observability). Task 12 (rate limiting) ships in parallel.
**Current File(s)**: `src/services/users/search/` (new module).

By the time this task runs, the components built in tasks 5–9 and 11 exist as separate units. This task composes them into the request handler that serves `/api/users/search`.

## 3. Agent Assignment

**Primary Agent**: `backend-engineer` (see [`../agent-roster.md`](../agent-roster.md))
**Supporting Agents**:

- `integration-test-generator` — drafts the integration tests covering the full request lifecycle.
- `security-auditor` — reviews the auth → RBAC → query path for boundary correctness.

## 4. Prerequisites

- [ ] Task 4 complete: indexes exist in develop and staging.
- [ ] Task 5 complete: `search.validate_request()` returns either a structured filter set or a 400 error.
- [ ] Task 6 complete: RBAC scoping injects `organization_id` for non-admin actors.
- [ ] Task 7 complete: query builder produces parameterized SQL for every filter combination.
- [ ] Task 8 complete: cursor encode/decode round-trips and rejects tampered/expired cursors.
- [ ] Task 9 complete: Redis cache layer has hit/miss paths working.
- [ ] Task 11 complete (or in flight): observability instrumentation can be wired in.
- [ ] API gateway routing config writable (this task adds a route).

## 5. Task Details

### 5.1 Goal

Compose validator → cache → query → response shape into a request handler exported as `search.handle_request(request, actor)`. Wire it into the API gateway at `GET /api/users/search`.

### 5.2 Current State

The repo has the building blocks from tasks 5–9 and 11 but no endpoint registered. Hitting `/api/users/search` returns 404.

### 5.3 Target State

```
GET /api/users/search?name=john&role=admin&status=active
  ⮕ HTTP 200
     {
       "results": [...50 user rows...],
       "page": {"size": 50, "next_cursor": "...", "prev_cursor": null},
       "metadata": {"result_count": 50, "cache_hit": false}
     }
```

Endpoint sequence:

```
def handle_request(request, actor):
    # 1. Validate and parse filters
    filters = search.validate_request(request.query, actor)   # Task 5
    if isinstance(filters, ValidationError):
        return http_400(filters.body)

    # 2. RBAC scoping
    filters = search.apply_rbac(filters, actor)               # Task 6

    # 3. Cache lookup
    cache_key = search.derive_cache_key(filters)
    cached = redis.get(cache_key)                             # Task 9
    if cached:
        emit_metrics(cache_hit=True, ...)
        return cached

    # 4. Cache miss: query
    rows, has_next = search.execute_query(filters)            # Task 7
    next_cursor = search.encode_cursor(rows[-1]) if has_next else None    # Task 8
    prev_cursor = filters.cursor if filters.direction == "next" else None

    response = {
        "results": rows[:filters.page_size],
        "page": {"size": filters.page_size, "next_cursor": next_cursor, "prev_cursor": prev_cursor},
        "metadata": {"result_count": len(rows[:filters.page_size]), "cache_hit": False},
    }

    # 5. Cache populate (single-flight via Task 9)
    redis.setex(cache_key, TTL, response)

    # 6. Emit observability                                   # Task 11
    emit_metrics(cache_hit=False, result_count=...)
    log.info("search", actor_id=actor.id, filter_set_hash=..., result_count=..., duration_ms=...)
    trace.span("users.search", ...)

    return http_200(response)
```

### 5.4 Step-by-step

1. Create `src/services/users/search/handler.py` (or equivalent) with the `handle_request` composition above.
2. Register the route in the API gateway: `GET /api/users/search → users_service.search.handle_request`.
3. Add the `users.search.enabled` feature flag check at the top of `handle_request` (return 404 when disabled).
4. Wire the integration test under `tests/integration/users_search_test.py`:
   - Seed 100 users across 3 organizations and 4 roles.
   - Test admin sees all; non-admin sees only own org.
   - Test each filter combination in the spec.
   - Test cursor pagination (next, prev, end-of-list).
   - Test cache hit and miss paths.
   - Test 400 cases (bad role, bad status, malformed cursor, page_size > 100).
   - Test 401 case (no auth).
5. Run integration tests against a local Postgres + Redis (use existing fixtures).
6. Local synthetic load: 100 RPS for 60s; confirm p95 < 200ms.
7. Merge once acceptance criteria pass and `security-auditor` signs off.

### 5.5 Files to Modify

| File | Change |
|---|---|
| API gateway routing config (path varies by project) | Add `/api/users/search` route. |
| `src/services/users/__init__.py` (or equivalent) | Export `search` module. |

### 5.6 Files to Create

| File | Purpose |
|---|---|
| `src/services/users/search/handler.py` | `handle_request` composition. |
| `tests/integration/users_search_test.py` | Full request-lifecycle tests. |

### 5.7 Files to Delete

None.

## 6. Acceptance Criteria

- [ ] `GET /api/users/search` returns 200 with the documented response shape.
- [ ] All five filter parameters (`name`, `email`, `role`, `status`, `created_*`) work end-to-end.
- [ ] Cursor pagination (next + prev) works.
- [ ] RBAC scoping enforced: non-admin actor sees only own organization (R5.3).
- [ ] Authenticated requests required (R5.1, NFR-2.1).
- [ ] All error cases (400 invalid input, 401 unauthenticated, 429 rate-limited) return structured bodies.
- [ ] Feature flag `users.search.enabled` controls the endpoint (404 when off).
- [ ] Observability instrumentation emits the four metrics, the structured log, and the trace span (NFR-3.1, NFR-3.2, NFR-3.3, NFR-3.4).
- [ ] Integration tests cover every requirement (R1.1–R5.3) — coverage table updated in [`../tasks.md`](../tasks.md).
- [ ] Local synthetic 100 RPS load: p95 < 200ms.
- [ ] `/audit` returns clean.
- [ ] `security-auditor` signed off on the auth → RBAC → query path.

## 7. Out of Scope

- Rate limiting at the gateway — task 12.
- Frontend integration — Phase 2 (tasks 13–17).
- Production load testing — task 18.
- Production rollout — task 20.
- Documentation updates — task 21.

## 8. Validation

1. Integration tests pass: every test case in `users_search_test.py`.
2. Local synthetic load report (script attached to PR): p95, p99, error rate, cache hit rate.
3. Manual smoke against develop env: hit the endpoint with curl from each role; confirm the response and the audit log entry.
4. `EXPLAIN ANALYZE` (re-run from task 4) still shows index usage under the new traffic pattern.

## 9. Rollback

If the endpoint misbehaves in develop:

1. Toggle feature flag `users.search.enabled` to false. Endpoint returns 404 cleanly.
2. Verify error rate drops to baseline.
3. Investigate via the structured logs (filter by `request_id`).
4. Fix and re-deploy; flag back on.

The endpoint is read-only and stateless beyond cache. No data rollback needed.
