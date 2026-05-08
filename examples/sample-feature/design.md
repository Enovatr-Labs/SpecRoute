# Design: User Search

**Version**: 1.0
**Date**: 2026-05-08
**Author**: SpecForge worked example
**Status**: Approved
**Source PRD**: [`prd.md`](prd.md)
**Source Requirements**: [`requirements.md`](requirements.md)

> **Spec triplet — part 2 of 3.** References requirement IDs from `requirements.md`. Companion: [`tasks.md`](tasks.md).

---

## 1. Overview

The design adds a single REST endpoint (`GET /api/users/search`) backed by indexed Postgres queries with a 60s Redis cache layer. No new services. The endpoint validates input, derives a deterministic cache key from the filter set, checks Redis, falls through to a parameterized SQL query, populates Redis, and returns results with cursor-based pagination metadata.

The frontend adds one new page (`/users/search`) that wires the existing search-input component to the new endpoint. RBAC enforcement happens at request validation; the SQL query receives a pre-scoped `organization_id` filter that the validator injects based on the actor's role.

The technical insight is that all filter combinations resolve to indexed scans — there are no full-table scans even with combined filters, because the four indexes cover the discriminating columns and Postgres's bitmap-AND combines them.

## 2. Architecture

### 2.1 Component Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   /users/search (frontend page)                                     │
│   ├── SearchInput (debounced 300ms)                                 │
│   ├── FilterChips (role, status, date)                              │
│   ├── ResultTable                                                   │
│   └── CursorPagination                                              │
│                          │                                          │
│                          ▼                                          │
│   GET /api/users/search?<filters>                                   │
│                          │                                          │
└──────────────────────────┼──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│   Backend: search module                                            │
│                                                                     │
│   1. Auth middleware (existing) — validates session, attaches actor │
│   2. RBAC: derive (organization_id, role)                           │
│   3. Validator: parse + sanitize filter set; reject HTTP 400 on bad │
│   4. Cache key: hash(filter_set_with_actor_scope)                   │
│   5. Cache lookup (Redis, 60s TTL)                                  │
│   6. On miss: parameterized SQL against users table                 │
│   7. Cache populate                                                 │
│   8. Emit metrics + log + trace span                                │
│   9. Return JSON                                                    │
│                                                                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│   Postgres users table                                              │
│   + idx_users_name_lc          LOWER(name) text_pattern_ops         │
│   + idx_users_email_lc         LOWER(email) text_pattern_ops        │
│   + idx_users_status           status WHERE status='active'         │
│   + idx_users_role             role                                 │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Components

| Component | Responsibility | Owner |
|---|---|---|
| `SearchInput` (frontend) | Accept user typing; debounce; call API on settle | Platform team |
| `FilterChips` (frontend) | Render filter selectors; manage filter state | Platform team |
| `ResultTable` (frontend) | Render result rows; emit row-click events | Platform team |
| `CursorPagination` (frontend) | Render prev/next controls; manage cursor state | Platform team |
| `search` module (backend) | Validate, query, cache, emit observability | Platform team |
| Postgres `users` indexes | Make all filter combinations indexed | Platform team |
| Redis cache layer | Short-TTL result caching keyed by filter set + actor scope | Platform team |

### 2.3 Data Flow

#### Operation: search users

```
SearchInput (user types "john")
    │ debounce 300ms
    ▼
GET /api/users/search?name=john
    │
    ▼
Auth middleware                            ─── existing infra
    │
    ▼
search.validate_request(filters, actor)
    │
    ▼
search.derive_cache_key(filters, actor.org_id, actor.role)
    │
    ▼
Redis GET <cache_key>
    │
    ├── HIT  ─────────────────────────────► return cached page
    │
    └── MISS
        ▼
        SELECT ... FROM users
            WHERE LOWER(name) LIKE LOWER(?)
              AND organization_id = ?       ─── only for non-admin
              ORDER BY ... LIMIT 51
        │
        ▼
        Build response (slice 50, derive next_cursor)
        │
        ▼
        Redis SETEX <cache_key> 60 <response>
        │
        ▼
        Emit metrics + log + trace
        │
        ▼
        Return JSON
```

**Satisfies:** R1.1, R1.2, R1.3, R2.1, R3.1, R4.1, R4.2, R5.1, R5.2, R5.3, NFR-1.1, NFR-3.1, NFR-3.2, NFR-3.3, NFR-3.4.

## 3. Data Model

### 3.1 Entities

#### `users` (existing table)

| Field | Type | Constraints | Purpose |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Stable user identifier |
| `name` | TEXT | NOT NULL | Display name |
| `email` | TEXT | NOT NULL UNIQUE | Login identifier |
| `role` | TEXT | NOT NULL | RBAC role |
| `status` | TEXT | NOT NULL CHECK IN ('active', 'disabled') | Account lifecycle |
| `organization_id` | UUID | NOT NULL REFERENCES organizations(id) | Tenancy |
| `created_at` | TIMESTAMPTZ | NOT NULL | For sort + filter |
| `last_activity_at` | TIMESTAMPTZ | nullable | For sort |

No column changes required.

### 3.2 Relationships

`users.organization_id → organizations.id`. Used by RBAC scoping in non-admin queries.

### 3.3 Indexes

| Index | Columns | Reason |
|---|---|---|
| `idx_users_name_lc` | `LOWER(name) text_pattern_ops` | Substring search on name (R1.1) |
| `idx_users_email_lc` | `LOWER(email) text_pattern_ops` | Substring search on email (R1.2) |
| `idx_users_status` | `status WHERE status = 'active'` | Partial index, status filter (R3.1) — most queries scope to active |
| `idx_users_role` | `role` | Role filter (R2.1) |

Postgres's bitmap-AND combines indexes for queries with multiple filters. No full-table scans expected.

### 3.4 Migrations

```sql
-- migrations/202605xx_add_user_search_indexes.sql
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_name_lc
  ON users (LOWER(name) text_pattern_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email_lc
  ON users (LOWER(email) text_pattern_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_status
  ON users (status) WHERE status = 'active';
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_role
  ON users (role);
```

`CONCURRENTLY` avoids long table locks. Safe to run during traffic.

## 4. API Contracts

### 4.1 Endpoint: `GET /api/users/search`

**Purpose:** Paginated, filterable search over the user directory.
**Auth:** Required (existing session-cookie auth).
**Satisfies:** R1.1, R1.2, R1.3, R2.1, R3.1, R4.1, R4.2, R5.1, R5.2, R5.3.

#### Request

```http
GET /api/users/search?name=john&role=admin&status=active&page_size=50&cursor=<opaque>&direction=next HTTP/1.1
Cookie: session=<...>
```

| Query parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | no | Substring; case-insensitive |
| `email` | string | no | Substring; case-insensitive |
| `role` | enum | no | Exact match; one of the recognized roles |
| `status` | enum | no | `active` or `disabled` |
| `created_after` | RFC3339 timestamp | no | Inclusive |
| `created_before` | RFC3339 timestamp | no | Inclusive |
| `sort` | enum | no | `name_asc`, `name_desc`, `created_desc` (default), `last_activity_desc` |
| `page_size` | int | no | 1–100; default 50 |
| `cursor` | opaque string | no | From a prior response |
| `direction` | enum | no | `next` (default) or `prev`, only meaningful with `cursor` |

#### Response (200)

```json
{
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "John Example",
      "email": "john@example.com",
      "role": "member",
      "status": "active",
      "last_activity_at": "2026-05-07T14:32:18Z"
    }
  ],
  "page": {
    "size": 50,
    "next_cursor": "eyJpZCI6IjU1MGU4NDAwLi4uIiwidHMiOiIyMDI2LTA1LTA3In0=",
    "prev_cursor": null
  },
  "metadata": {
    "result_count": 1,
    "cache_hit": false
  }
}
```

#### Errors

| Status | Reason | Response body |
|---|---|---|
| 400 | Invalid filter value | `{"error": "invalid_role", "valid": ["admin", "member", "guest"]}` |
| 400 | `page_size > 100` | `{"error": "page_size_too_large", "max": 100}` |
| 400 | Malformed cursor | `{"error": "invalid_cursor"}` |
| 401 | Unauthenticated | `{"error": "unauthenticated"}` |
| 429 | Rate limit (100/min/actor) | `Retry-After: <seconds>` |
| 500 | Internal | `{"error": "internal", "request_id": "..."}` |

## 5. Event Contracts

None. Search is read-only.

## 6. State Management

The endpoint is stateless from the application's perspective. State lives in:

- **Postgres**: source of truth for users.
- **Redis**: 60s-TTL cache, keyed by deterministic hash of `(filter_set, organization_id, actor_role)`. Cache invalidation = TTL expiry. No active invalidation needed for v1; admin updates that affect search results may show up to 60s later.
- **Frontend**: cursor state held in component state; URL reflects the current cursor for shareable links.

Cursors are opaque, signed (HMAC-SHA256), and contain `(last_id, last_sort_key)` plus a timestamp for replay protection. The signing key is read from existing secrets.

## 7. Performance Considerations

| Concern | Approach | Budget |
|---|---|---|
| Query throughput | Indexed scans + bitmap-AND for combined filters | NFR-1.1 (p95 < 200ms) |
| Cache hit ratio | 60s TTL on filter+actor key; admin re-searches typically hit | > 40% steady state |
| Cache stampede | Single-flight at cache layer using Redis SETNX lock | n/a |
| Hot path latency | Avoid serialization in fast path; pre-allocate response buffer | NFR-1.1 |
| Concurrent load | Postgres connection pool sized for 100 RPS without saturation | NFR-1.3 |

## 8. Security Considerations

| Concern | Approach |
|---|---|
| Authentication | Required; existing session auth (NFR-2.1) |
| Authorization | RBAC: `organization_id` filter injected for non-admin actors (R5.2, R5.3, NFR-2.2) |
| Input validation | Server-side: length, character set, allowed values for enums; regex for email substring (NFR-2.3) |
| Output encoding | JSON-encoded; no HTML in responses |
| Secrets handling | Cursor signing key from existing secrets manager |
| Audit logging | Every search logged with actor, filter hash, result count (NFR-3.3) |
| Rate limiting | 100/min/actor at API gateway (NFR-2.4) |
| Threat: enumeration | Rate limit + audit log + RBAC scoping |
| Threat: SQL injection | Parameterized queries only; no string-concatenated SQL |
| Threat: cursor tampering | HMAC signature; timestamp replay protection |

## 9. Observability

| Signal | What's emitted | Dashboard / alert |
|---|---|---|
| Metric | `search.duration_ms` (histogram, labels: `cache_hit`, `result_count_bucket`) | latency dashboard; alert on p95 > 200ms |
| Metric | `search.result_count` (histogram) | volume dashboard |
| Metric | `search.filter_usage_total` (counter, label: `filter_name`) | usage analytics |
| Metric | `search.errors_total` (counter, label: `error_code`) | error-rate alert |
| Log | structured: `request_id`, `actor_id`, `filter_set_hash`, `result_count`, `duration_ms`, `cache_hit` | log search and incident triage |
| Trace | search spans linked to API gateway span | trace dashboards |

**Satisfies:** NFR-3.1, NFR-3.2, NFR-3.3, NFR-3.4.

## 10. Failure Modes and Mitigations

| Failure | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Postgres slow query under high load | Medium | Latency regression | Query plan validated in staging; alert on p95 |
| Redis unavailable | Low | Latency regression (no cache) | Fall through to DB; emit metric; degrade gracefully |
| Cursor tampering | Low | Auth bypass | HMAC signing; replay protection; auth re-check |
| Filter combination produces full-table scan | Low | Latency regression | Validated index plan in staging; load test exercises all combinations |

## 11. Rollout Considerations

- **Feature flag**: `users.search.enabled`. Frontend page checks the flag; backend endpoint also checks (defense in depth).
- **Migration ordering**: index migration runs first (forward-compatible); endpoint deploys after; frontend deploys last.
- **Backwards compatibility**: existing `/users` page remains functional. No breaking changes.
- **Rollout schedule**: 10% → 50% → 100% traffic via feature flag, with 24h between stages.

## 12. Alternatives Considered

### 12.1 Use Elasticsearch for search instead of Postgres indexes

- **Chosen**: Postgres indexed scans.
- **Alternative considered**: introduce Elasticsearch for search.
- **Why chosen**: Adding ES introduces a new operational surface, sync complexity, and an inconsistency window. Postgres indexes are sufficient for the corpus size and filter complexity; the bitmap-AND plan is well-understood. Revisit if v2 scope grows to include full-text or relevance ranking.

### 12.2 Offset-based pagination

- **Chosen**: Cursor-based.
- **Alternative considered**: offset/limit pagination.
- **Why chosen**: Offset-based pagination has stable-page issues under concurrent inserts (rows shift between pages) and gets slower as offset grows. Cursor-based is stable and constant-time. The added cursor complexity is contained in 50 LOC of encode/decode.

### 12.3 No cache layer

- **Chosen**: 60s Redis cache.
- **Alternative considered**: hit Postgres on every request.
- **Why chosen**: Admin search workflows have high repeat rates (same user looking for the same person across sessions). Cache hit > 40% expected, materially reducing DB load. 60s TTL keeps freshness acceptable.

## 13. Open Questions

| ID | Question | Resolution required by |
|---|---|---|
| Q1 | Privacy review for query-string logging | Phase 1 start |
| Q2 | Cache TTL — 60s or 300s | Phase 0 spike |
| Q3 | Cursor encoding — opaque base64 vs structured ID | Phase 0 spike |

---

## Appendix: Requirement → Component Map

| Requirement | Components Involved |
|---|---|
| R1.1 | search module (validator, query builder), Postgres `idx_users_name_lc` |
| R1.2 | search module (validator, query builder), Postgres `idx_users_email_lc` |
| R1.3 | search module (query builder) |
| R2.1 | search module (validator, query builder), Postgres `idx_users_role` |
| R3.1 | search module (query builder), Postgres `idx_users_status` |
| R4.1 | search module (cursor encoder/decoder), CursorPagination (frontend) |
| R4.2 | search module (cursor encoder/decoder), CursorPagination (frontend) |
| R5.1 | Auth middleware (existing) |
| R5.2 | search module (RBAC scoping) |
| R5.3 | search module (RBAC scoping) |
| NFR-1.1 | Postgres indexes, Redis cache, search module fast path |
| NFR-2.1 | Auth middleware |
| NFR-2.2 | search module (RBAC scoping) |
| NFR-2.3 | search module (validator) |
| NFR-2.4 | API gateway (rate limit) |
| NFR-3.1 | search module (metrics emitter) |
| NFR-3.2 | search module (metrics emitter) |
| NFR-3.3 | search module (logger) |
| NFR-3.4 | search module (tracer) |
| NFR-4.1 | Existing user-service infra |
