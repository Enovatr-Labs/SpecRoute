# ADR-003: 60-Second Redis Cache Layer for Search Results

**Status**: Accepted
**Date**: 2026-05-08
**Deciders**: Backend engineer, Performance lead
**Context links**: Phase 0 spike (Q2), [`design.md`](../specs/user-search/design.md) §12.3

---

## Context

The user-search endpoint targets p95 < 200ms (NFR-1.1). Admin search workflows have high repeat rates - the same admin searching for the same person across sessions is a common pattern. Without a cache, every search hits Postgres.

Phase 0 task 001 (cache TTL spike) ran a one-week shadow trial in staging with two TTLs (60s and 300s) and measured cache hit rate, freshness gap, and p95 miss latency.

## Decision

We will use a **60-second Redis cache layer** keyed by `sha256(filter_set + organization_id + role)`. Cache hits return in sub-millisecond; cache misses fall through to Postgres and populate.

We use **single-flight via Redis SETNX lock** to bound stampede impact when a popular query expires.

## Alternatives Considered

### Alternative 1: 300-second TTL

- **What it is**: Same caching pattern, longer TTL.
- **Why rejected**: Phase 0 measurements showed cache hit rate at 300s (~52%) was only marginally better than at 60s (~44%). The extra 240 seconds of staleness was not worth 8 percentage points of hit-rate improvement. A user added to an organization 5 minutes ago should appear in admin search; admins find the 5-minute gap irritating but acceptable, the 5-minute gap unacceptable.

### Alternative 2: No cache

- **What it is**: Hit Postgres on every search.
- **Why rejected**: At 100 RPS sustained, the cache shaves 40-50% of read load off the DB. Without it, Postgres connection pool saturation became a Phase 0 staging concern.

### Alternative 3: Multi-tier cache (in-process + Redis)

- **What it is**: First check an in-process LRU; fall through to Redis; fall through to Postgres.
- **Why rejected**: Marginal latency improvement at significant complexity cost. In-process cache adds invalidation complexity across multiple service replicas. Postpone to a future ADR if profiling shows Redis is the bottleneck.

## Consequences

### Positive

- Cache hit rate ~44% in steady state; meaningful DB load reduction.
- Single-flight bounds stampede impact - a popular query expiring doesn't trigger N concurrent DB queries.
- Cache invalidation is implicit (TTL); no active invalidation logic to maintain.

### Negative

- Up to 60-second staleness on user updates. Acceptable for admin workflow; documented in PRD §3.3.
- New operational dependency on Redis. The team already runs Redis for other services, so no new infra; but it's a failure mode the search endpoint inherits.

### Neutral

- TTL is a config knob; we can revisit (5s? 30s? 120s?) if production data suggests a different optimum.

## Implementation Implications

- Cache layer: `src/services/users/search/cache.py` (Phase 1 task 9)
- Cache key derivation includes `organization_id` and `role` so different RBAC scopes don't share entries
- Single-flight via `SETNX <lock_key>` with 5s lock TTL (lock holder crash is bounded)
- On cache miss: query DB, populate cache with `SETEX <key> 60 <response>`, return
- On cache hit: return cached response with `cache_hit: true` flag for observability
- Cached payload is the full response body (results + page metadata) - no per-request shaping needed

## Compliance / Security / Performance Notes

- Cached values do NOT include plaintext query strings - the cache key is a hash; the cached value is the response (which doesn't echo the query).
- Different RBAC scopes get different cache entries by construction (organization_id + role in the key).

## References

- [`design.md`](../specs/user-search/design.md) §7 (Performance Considerations), §12.3 (Alternatives Considered)
- [`tasks.md`](../specs/user-search/tasks.md) Tasks 1 (TTL spike), 9 (cache layer implementation)
