# ADR-001: Use Postgres Indexed Scans for User Search

**Status**: Accepted
**Date**: 2026-05-08
**Deciders**: Tech lead, Database engineer
**Context links**: [`prd.md`](../prds/active/user-search.md), [`design.md`](../specs/user-search/design.md) §12.1

---

## Context

The user-search feature requires sub-200ms p95 latency on a `users` table with tens of thousands of rows growing toward hundreds of thousands. Filters span name (substring), email (substring), role (exact), status (exact), and created-at range. Combined filters must remain fast.

Two reasonable backends were considered: keep the data in Postgres and add indexes, or introduce Elasticsearch (or a similar search engine) and replicate users into it.

The forcing constraint: ship within 4 weeks, no new operational surface unless required.

## Decision

We will use **Postgres indexed scans** with four new indexes on the `users` table:

- `idx_users_name_lc` (`LOWER(name) text_pattern_ops`)
- `idx_users_email_lc` (`LOWER(email) text_pattern_ops`)
- `idx_users_status` (partial on `status='active'`)
- `idx_users_role`

Postgres's bitmap-AND combines indexes for queries with multiple filters; no full-table scans expected at our corpus size.

## Alternatives Considered

### Alternative 1: Elasticsearch

- **What it is**: Replicate users into ES; search there; serve hits from ES.
- **Why rejected**: New operational surface (cluster, monitoring, version upgrades). Inconsistency window between Postgres writes and ES indexing. Adds a backfill / repair workstream when Postgres and ES drift. Postgres indexes are sufficient for our corpus size and filter complexity.

### Alternative 2: In-memory search service

- **What it is**: Stand up a dedicated service that loads the user table into memory and serves searches.
- **Why rejected**: Same complexity argument. Plus memory pressure as the corpus grows; pagination across an in-memory cursor is awkward.

### Alternative 3: Postgres trigram (`pg_trgm`) instead of `text_pattern_ops`

- **What it is**: Use trigram indexes for fuzzy substring matching.
- **Why rejected**: Slower for prefix queries (the common case). `text_pattern_ops` handles `LOWER(name) LIKE 'j%'` well; trigrams are overkill for the substring patterns we expect.

## Consequences

### Positive

- No new operational surface. The migration is forward-compatible (`CREATE INDEX CONCURRENTLY`).
- The team's Postgres expertise applies directly. No new runbook, no new monitoring stack.
- Query plans are well-understood and profilable with `EXPLAIN ANALYZE`.
- Indexes scale to ~1M rows comfortably with our filter shapes.

### Negative

- We accept that full-text search of user-generated content (beyond the columns we index) won't be possible without a future Elasticsearch ADR.
- Index maintenance cost increases marginally on every `INSERT` / `UPDATE` to `users`. Acceptable given the read:write ratio.
- The `idx_users_status` partial index means `status='disabled'` queries don't get an index; we handle this in the query builder by skipping the predicate when matching all statuses.

### Neutral

- We will revisit if the corpus grows past 1M users or relevance ranking becomes a requirement.

## Implementation Implications

- Migration file: `migrations/202605xx_add_user_search_indexes.sql`
- Down migration drops each index `IF EXISTS`
- Query builder uses parameterized `LOWER(<col>) LIKE LOWER(?)` for substring; exact match for role/status; range for created_at
- `EXPLAIN ANALYZE` validation in staging is a Phase 1 gate (task 4)

## Compliance / Security / Performance Notes

- No PII implications - we're indexing existing columns, not adding new ones.
- p95 latency NFR-1.1 (200ms) requires this decision. Without indexed scans, sequential scans on 100k rows hit ~600ms.

## References

- [`design.md`](../specs/user-search/design.md) §3.3 (Indexes), §12.1 (Alternatives Considered)
- [`tasks.md`](../specs/user-search/tasks.md) Task 4 (Index migration)
