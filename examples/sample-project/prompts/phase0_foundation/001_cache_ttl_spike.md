# Task 001: Spike - Cache TTL Choice

> Phase 0 spike. Output is a decision, not code.

---

## 1. Objective

Decide the Redis cache TTL for `/api/users/search` results. The PRD's open question Q2 (`requirements.md` Section 7) frames the trade-off: 60s gives strong freshness; 300s gives a higher cache hit rate. We need real numbers to choose.

After this spike: a number is recorded in [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 7 (Performance Considerations) and Section 12 (Alternatives Considered).

## 2. Context

**PRD Reference**: [`../../prds/active/user-search.md`](../../prds/active/user-search.md) Section 18 (Performance Requirements)
**Spec Reference**: [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) Q2; NFR-1.1
**Architecture Reference**: [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 7
**Phase Master**: [`000_MASTER_foundation.md`](000_MASTER_foundation.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)

The cache layer (built in task 9, Phase 1) materially impacts latency. A short TTL means more cache misses → more DB load. A long TTL means stale results when admins update users, but lower DB load.

Real admin search workflows have high repeat rates (same query across sessions when looking for the same user). Longer TTL favors hit rate.

The freshness cost is bounded: a user added 60s ago doesn't appear in search until the TTL expires. For admin workflows, this is usually acceptable; for self-service workflows where a user expects to see themselves immediately after registration, it isn't.

## 3. Agent Assignment

**Primary Agent**: `backend-engineer` (see [`../../agent-roster.md`](../../agent-roster.md))
**Supporting Agents**:

- `deployment-validator` - runs the staging measurement.

## 4. Prerequisites

- [ ] Staging Postgres + Redis available with synthetic data approximating production scale.
- [ ] Synthetic load generator runs against the existing `/users` page (so we have a baseline).

## 5. Task Details

### 5.1 Goal

Run a one-week shadow trial in staging with two cache TTLs (60s, 300s) for the search endpoint. Capture cache hit rate, freshness complaints, p95 latency for misses. Decide.

### 5.2 Approach

1. Build the endpoint behind the feature flag (uses the in-flight Phase 1 work; this spike's variant uses a feature flag override that picks the TTL from a config knob).
2. Generate a representative query distribution: 60% repeated within 60s, 20% repeated within 60–300s, 20% unique. (Match against admin telemetry baselines if available.)
3. Run for 24h with TTL=60s; capture metrics.
4. Run for 24h with TTL=300s; capture metrics.
5. Compare: cache hit rate, p95 miss latency, freshness sensitivity.

### 5.3 Variables to capture

| Metric | TTL=60s capture | TTL=300s capture |
|---|---|---|
| Cache hit rate (%) | `search.cache_hit_rate{ttl="60"}` | `search.cache_hit_rate{ttl="300"}` |
| p95 miss latency (ms) | `search.miss_latency_ms{ttl="60",quantile="0.95"}` | `search.miss_latency_ms{ttl="300",quantile="0.95"}` |
| Freshness gap p99 (s) | `search.freshness_gap_seconds{ttl="60",quantile="0.99"}` | `search.freshness_gap_seconds{ttl="300",quantile="0.99"}` |

### 5.4 Decision criteria

- If hit rate at TTL=300s is ≥ 1.5× hit rate at TTL=60s **and** p95 miss latency holds, choose 300s.
- Else default to 60s (privileges freshness for admin workflows).

### 5.5 Files to Modify

| File | Change |
|---|---|
| [`../../specs/user-search/design.md`](../../specs/user-search/design.md) | Section 7: record decision and rationale |
| [`../../specs/user-search/design.md`](../../specs/user-search/design.md) | Section 12.3: update "Alternatives Considered" with the spike outcome |
| [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) | Section 7: mark Q2 resolved |

## 6. Acceptance Criteria

- [ ] One-week shadow trial complete in staging.
- [ ] Metrics captured for both TTL values.
- [ ] Decision recorded in `design.md` Section 7 with the actual numbers.
- [ ] Q2 marked resolved in `requirements.md` Section 7.
- [ ] Phase 1 cache layer (task 9) reads the chosen TTL.

## 7. Out of Scope

- Implementing the production cache layer - that's task 9.
- Multi-tier caching (e.g. local + Redis) - out of scope for v1.
- Cache invalidation beyond TTL expiry - also out of scope.

## 8. Validation

The decision is validated by Phase 1's task 9 and Phase 3's task 18 (load test). If the load test reveals the TTL is wrong, return to this spike.

## 9. Rollback

The spike is non-production; no rollback needed. If the decision turns out wrong post-launch, change the TTL config (one-line edit) and ship in the next deploy.
