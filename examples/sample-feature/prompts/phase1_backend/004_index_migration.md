# Task 004: Add User Search Indexes Migration

> Production task prompt. First task of Phase 1 (Backend Implementation).

---

## 1. Objective

Add four Postgres indexes to the `users` table to support indexed scans for every filter combination the search endpoint exposes. The migration must be forward-compatible and run safely under load (no long table locks).

After this task lands, `EXPLAIN ANALYZE` on representative search queries shows index scans (or bitmap index combinations); the table is ready to receive search traffic.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 7 (Data Strategy)
**Spec Reference**: [`../../requirements.md`](../../requirements.md) — Requirements: R1.1, R1.2, R2.1, R3.1, NFR-1.1
**Architecture Reference**: [`../../design.md`](../../design.md) Section 3 (Data Model), Section 3.4 (Migrations)
**Phase Master**: [`000_MASTER_backend.md`](000_MASTER_backend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: this is task 4 in [`../../tasks.md`](../../tasks.md). Phase 0 spikes (tasks 1–3) must be complete before starting.
**Current File(s)**: `migrations/` (no existing search-related migration).

The platform already has indexes on `users.id` (PK), `users.email` (unique), and `users.organization_id` (FK). For search, we need additional indexes on the lowered name and email (substring search), the `status` column (filter), and the `role` column (filter). The `status` index is partial (only on `status='active'`) because the vast majority of search traffic is scoped to active users; this keeps the index small and the partial-index plan well-understood.

## 3. Agent Assignment

**Primary Agent**: `database-engineer` (see [`../../agent-roster.md`](../../agent-roster.md))
**Supporting Agents**:

- `deployment-validator` — runs the migration in staging and validates with `EXPLAIN ANALYZE`.
- `unit-test-writer` — writes the smoke test that confirms each index exists.

## 4. Prerequisites

- [ ] Phase 0 complete: tasks 1 (cache TTL spike), 2 (cursor encoding), 3 (privacy review) all closed.
- [ ] Open questions Q1, Q2, Q3 resolved and recorded in the PRD / design.
- [ ] `EXPLAIN ANALYZE` baseline captured for current `/users` queries (so we have something to compare against).
- [ ] Staging Postgres mirrors production schema and approximate row count.

## 5. Task Details

### 5.1 Goal

Add four indexes via `CREATE INDEX CONCURRENTLY` so search filter combinations resolve to indexed scans (or bitmap-AND).

### 5.2 Current State

```sql
-- Existing on users table:
-- PRIMARY KEY (id)
-- UNIQUE (email)
-- INDEX (organization_id)
-- (no indexes for search)
```

`EXPLAIN ANALYZE SELECT * FROM users WHERE LOWER(name) LIKE 'john%' LIMIT 50;` currently shows a sequential scan. Latency at 100k rows: ~600ms. Unacceptable.

### 5.3 Target State

```sql
-- After this migration:
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_name_lc
  ON users (LOWER(name) text_pattern_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email_lc
  ON users (LOWER(email) text_pattern_ops);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_status
  ON users (status) WHERE status = 'active';
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_role
  ON users (role);
```

`EXPLAIN ANALYZE` of the same query now shows `Index Scan using idx_users_name_lc`. Latency: < 50ms.

### 5.4 Step-by-step

1. Create `migrations/202605xx_add_user_search_indexes.sql` with the four `CREATE INDEX CONCURRENTLY` statements (in the order above).
2. Add a corresponding `down` migration that drops each index `IF EXISTS`.
3. In CI, run the migration against a synthetic dataset (~100k rows) and capture timing.
4. Run `EXPLAIN ANALYZE` for each filter combination listed in the test matrix below; confirm each uses an index.
5. Run the migration in staging during low-traffic window. Monitor lock-pid counts (should stay flat — `CONCURRENTLY` is non-blocking).
6. Add a smoke test under `tests/migrations/` that asserts each index exists after migration.
7. Have `deployment-validator` sign off on the staging run before merging.

### 5.5 Files to Modify

| File | Change |
|---|---|
| `migrations/202605xx_add_user_search_indexes.sql` | Create — the new migration |
| `tests/migrations/test_user_search_indexes.py` (or equivalent) | Create — smoke test |

### 5.6 Files to Create

See above.

### 5.7 Files to Delete

None.

## 6. Acceptance Criteria

- [ ] Migration file created at `migrations/202605xx_add_user_search_indexes.sql`.
- [ ] All four indexes use `CREATE INDEX CONCURRENTLY IF NOT EXISTS`.
- [ ] Down migration drops each index `IF EXISTS`.
- [ ] Smoke test asserts all four indexes exist after migration.
- [ ] `EXPLAIN ANALYZE` for representative queries (see test matrix below) shows index usage in staging.
- [ ] Staging migration completes without table-lock observation.
- [ ] PR description includes the `EXPLAIN ANALYZE` outputs as evidence.
- [ ] `/audit` returns clean.

### Test matrix for EXPLAIN ANALYZE

| Filter combination | Expected plan |
|---|---|
| `LOWER(name) LIKE 'j%'` | Index Scan on `idx_users_name_lc` |
| `LOWER(email) LIKE '%@example.com'` | Index Scan on `idx_users_email_lc` (or sequential, depending on selectivity) |
| `status='active'` | Index Scan on `idx_users_status` (partial) |
| `role='admin'` | Index Scan on `idx_users_role` |
| `LOWER(name) LIKE 'j%' AND role='admin'` | Bitmap Index Scan combining both |

## 7. Out of Scope

- Endpoint implementation — task 10.
- Cache layer — task 9.
- Frontend — Phase 2.
- Removing existing indexes — they remain.

## 8. Validation

1. Smoke test passes: `pytest tests/migrations/test_user_search_indexes.py`.
2. Staging migration logged with no error.
3. `EXPLAIN ANALYZE` outputs attached to the PR.

## 9. Rollback

If the migration causes unexpected production load:

1. Run the down migration: `DROP INDEX IF EXISTS idx_users_name_lc, idx_users_email_lc, idx_users_status, idx_users_role;`. Each runs concurrently and is non-blocking.
2. Confirm load returns to baseline.
3. Investigate root cause before retrying.

(Most likely the index creation itself is the only load source; once an index exists, normal queries don't suffer.)
