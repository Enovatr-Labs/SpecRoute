# Task 012: Add Rate Limiting

> Production task prompt. Phase 1 backend gateway-level configuration.

---

## 1. Objective

Configure the API gateway to rate-limit `/api/users/search` to 100 requests / minute / actor. The 101st request within a minute returns HTTP 429 with a `Retry-After` header.

After this task: rate limiting is enforced; an integration test confirms the limit fires and recovers.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 17 (Security Requirements — enumeration mitigation)
**Spec Reference**: [`../../requirements.md`](../../requirements.md) — NFR-2.4
**Architecture Reference**: [`../../design.md`](../../design.md) Section 8 (Security Considerations)
**Phase Master**: [`000_MASTER_backend.md`](000_MASTER_backend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 12. Independent of tasks 4–11; runs at the API gateway, not in application code. Ships in parallel with task 10.
**Current File(s)**: API gateway routing config (project-specific path).

## 3. Agent Assignment

**Primary Agent**: `backend-engineer`
**Supporting Agents**:

- `integration-test-generator` — drafts the rate-limit integration test.

## 4. Prerequisites

- [ ] API gateway supports per-route rate limits (most modern gateways do).
- [ ] The rate-limit key derives from the authenticated actor's id (not just IP, which fails behind shared NATs).

## 5. Task Details

### 5.1 Goal

Configure the gateway:

- Route: `GET /api/users/search`
- Limit: 100 requests per 60 seconds per `actor_id`
- Response on limit: HTTP 429 with `Retry-After: <seconds>` header
- Response body: `{"error": "rate_limited", "retry_after": <seconds>}`

### 5.2 Choice of bucket

A "fixed window" or "token bucket" algorithm is fine. The test asserts the limit fires; it doesn't care which algorithm.

### 5.3 What to NOT rate-limit

- Health checks against `/health`.
- Internal service-to-service calls (those use a different auth path and shouldn't go through this rate limit).

### 5.4 Files to Modify

| File | Change |
|---|---|
| API gateway config (project-specific) | Add the rate limit rule for `/api/users/search` |
| `tests/integration/users_search_rate_limit_test.py` | Create — 101st request returns 429 |

## 6. Acceptance Criteria

- [ ] 100 requests in 60s succeed.
- [ ] 101st request returns 429 with `Retry-After`.
- [ ] After the window passes, the next request succeeds.
- [ ] The limit is per-actor (two different actors don't share a bucket).
- [ ] Health checks and internal traffic are not affected.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Cross-endpoint rate limiting (e.g. "1000 requests across all endpoints per minute") — separate concern.
- Adaptive rate limiting based on user role — could be a v2 enhancement.

## 8. Validation

Integration test runs 110 requests in a tight loop, asserts request 101 returns 429, then waits 60 seconds and asserts the next request succeeds.

## 9. Rollback

Remove the rate-limit rule from the gateway config. The endpoint reverts to ungated.
