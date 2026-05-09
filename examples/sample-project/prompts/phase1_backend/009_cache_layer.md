# Task 009: Implement Redis Cache Layer

> Production task prompt. Phase 1 backend component.

---

## 1. Objective

Implement the Redis cache layer between request handler and DB query. Cache key derives from `(filter_set, organization_id, role)`. TTL set per the Phase 0 cache-TTL spike outcome. Single-flight via SETNX prevents stampedes when a cache entry expires.

After this task: identical queries from the same actor scope return from cache (sub-ms latency); cache misses populate the cache atomically; cache stampedes are bounded.

## 2. Context

**PRD Reference**: [`../../prds/active/user-search.md`](../../prds/active/user-search.md) Section 18 (Performance Requirements)
**Spec Reference**: [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) - NFR-1.1
**Architecture Reference**: [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 7 (Performance Considerations)
**Phase Master**: [`000_MASTER_backend.md`](000_MASTER_backend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 9. Depends on Phase 0 task 001 (TTL choice). Consumed by task 10 (endpoint composition).
**Current File(s)**: `src/services/users/search/cache.py` (new).

## 3. Agent Assignment

**Primary Agent**: `backend-engineer`
**Supporting Agents**:

- `unit-test-writer` - embedded.

## 4. Prerequisites

- [ ] Phase 0 task 001 closed; TTL recorded in `design.md` Section 7.
- [ ] Redis client and connection pool configured at project level.

## 5. Task Details

### 5.1 Goal

```python
def derive_cache_key(filters: Filters) -> str
def get_or_compute(key: str, compute: Callable[[], Response], ttl: int) -> Response
```

`derive_cache_key` produces a deterministic SHA-256 hash of the canonical filter set including `organization_id` and `role` (so different scopes get different cache entries even for the same human-readable filter).

`get_or_compute` is the single-flight wrapper:

```
1. GET key. If hit, return.
2. SETNX <lock_key> with short TTL (e.g. 5s).
3. If lock acquired:
     a. Run compute().
     b. SETEX key TTL <result>.
     c. DEL lock_key.
     d. Return result.
4. If lock not acquired:
     a. Wait briefly (50–200ms).
     b. GET key. If hit, return.
     c. Else compute() directly (lock holder may have failed); don't repopulate cache.
```

The wait+retry path bounds stampede impact while keeping correctness if the lock holder crashes.

### 5.2 Cache key shape

```
users.search.<sha256(filter_canonical_json)>
```

Where `filter_canonical_json` is the filter dataclass serialized with sorted keys, including `organization_id` and `role`.

### 5.3 What to cache

The full response body (results + page metadata + `cache_hit: false`). When returning from cache, flip `cache_hit` to `true` for observability.

### 5.4 What NOT to cache

- Per-row sensitive fields (the response shape only includes public-profile fields, so this is naturally satisfied).
- Personally identifiable raw query strings (the cache key is a hash; the cached value is the response body which doesn't echo the query).

### 5.5 Files to Modify

| File | Change |
|---|---|
| `src/services/users/search/cache.py` | Create - cache key + single-flight wrapper |
| `src/services/users/search/__init__.py` | Export |
| `tests/services/users/search/test_cache.py` | Create - hit, miss, stampede simulation |

## 6. Acceptance Criteria

- [ ] `derive_cache_key` is deterministic across runs.
- [ ] `get_or_compute` returns from cache on a second identical call.
- [ ] Stampede test: 100 concurrent first-call clients result in exactly one `compute()` invocation (or close to it within stampede-bound tolerance).
- [ ] Cache key includes `organization_id` and `role` - different scopes don't share cache entries.
- [ ] TTL value reads from config (per Phase 0 decision).
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Cache invalidation beyond TTL expiry - out of v1.
- Multi-tier cache (local + Redis) - out of v1.
- Cache warming - out of v1.

## 8. Validation

Unit tests cover hit / miss. Stampede test uses a thread pool or async client to simulate concurrent first-call clients. Integration confirmation lands in task 10.

## 9. Rollback

If the cache misbehaves: pass through to direct compute (configure a "bypass cache" flag). Stale entries expire naturally at TTL.
