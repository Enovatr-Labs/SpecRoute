# ADR-002: Cursor-Based Pagination

**Status**: Accepted
**Date**: 2026-05-08
**Deciders**: Tech lead, Backend engineer
**Context links**: [`design.md`](../specs/user-search/design.md) §12.2

---

## Context

The user-search endpoint returns up to 50 results per page. Total result sets can run into the thousands. Pagination strategy needs to be:

- Stable under concurrent inserts (a new user joining mid-scroll shouldn't shift visible rows).
- Constant-time at any depth (page 1000 should be as fast as page 2).
- Support both forward (`next`) and backward (`prev`) navigation.
- Survive server restarts (no server-side cursor state).

## Decision

We will use **opaque, signed cursor tokens** that encode `(last_sort_key, last_id, timestamp)` from the most recently returned row. The endpoint accepts `cursor=<token>` and `direction=next|prev` query parameters.

## Alternatives Considered

### Alternative 1: Offset/limit pagination

- **What it is**: `?page=N&page_size=50` translates to `OFFSET N*50 LIMIT 50`.
- **Why rejected**:
  - **Stability problem**: a `INSERT` between page 1 and page 2 shifts all subsequent rows; the user sees the same row twice or misses one.
  - **Performance problem**: `OFFSET 10000` makes Postgres scan 10000 rows before returning. Latency grows with page depth.

### Alternative 2: Keyset pagination without signed cursors

- **What it is**: Same `(last_sort_key, last_id)` cursor as our chosen design, but exposed as plaintext URL parameters (e.g. `?after_id=<uuid>&after_created_at=<ts>`).
- **Why rejected**: A user could craft a cursor pointing to an arbitrary `(id, created_at)` pair and bypass RBAC scoping at the cursor layer. Even though the endpoint re-checks RBAC, defense in depth prefers signed cursors.

### Alternative 3: Server-side cursor state

- **What it is**: Server holds the cursor; client sends a session ID.
- **Why rejected**: Server-side state is operationally expensive (where does it live? what's the TTL? what happens on server restart?). Stateless cursors are simpler.

## Consequences

### Positive

- Stable: new rows don't shift existing pages.
- Constant-time: no `OFFSET` cost regardless of page depth.
- Stateless: no server-side cursor storage to operate.
- Tamper-evident: HMAC signature (see [ADR-004](adr-004-hmac-signed-cursors.md)) prevents cursor forgery.

### Negative

- "Jump to page N" is impossible. Users can only navigate sequentially. Acceptable for an admin search workflow; not acceptable for a public catalog.
- Cursor URLs are opaque - users can't bookmark a specific page deterministically across sessions (cursors expire after 24h replay window per ADR-004).
- Implementation is more complex than offset/limit (cursor encoding/decoding, sort-key handling).

### Neutral

- Total-count display ("page 3 of 47") is harder. We don't show total count - acceptable trade-off for an admin search.

## Implementation Implications

- Cursor encoder/decoder: `src/services/users/search/cursor.py` (Phase 1 task 8)
- Cursor predicate in SQL: `(<sort_key>, id) < (?, ?)` for forward, flipped for prev
- Sort always includes `id` as the tiebreaker for determinism
- Frontend `CursorPagination` component manages prev/next cursor state in URL

## Compliance / Security / Performance Notes

- See [ADR-004](adr-004-hmac-signed-cursors.md) for the signing and replay-protection details.
- Performance: each cursor hop is an indexed scan with a range predicate; effectively constant-time.

## References

- [`design.md`](../specs/user-search/design.md) §6 (State Management), §12.2 (Alternatives Considered)
- [`tasks.md`](../specs/user-search/tasks.md) Task 8 (Cursor encode/decode)
- [ADR-004](adr-004-hmac-signed-cursors.md) - the signing scheme
