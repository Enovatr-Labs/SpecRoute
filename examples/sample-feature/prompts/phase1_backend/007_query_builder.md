# Task 007: Implement Search Query Builder

> Production task prompt. Phase 1 backend component.

---

## 1. Objective

Implement `search.execute_query(filters)` - converts a validated, RBAC-scoped filter set into parameterized SQL against the `users` table and returns rows + a "has next page" flag. No string concatenation of SQL; no untrusted input in queries.

After this task: query builder produces correct SQL for every filter combination; `EXPLAIN ANALYZE` against staging confirms index usage matches the plan from task 4.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 7 (Data Strategy)
**Spec Reference**: [`../../requirements.md`](../../requirements.md) - R1.1, R1.2, R1.3, R2.1, R3.1
**Architecture Reference**: [`../../design.md`](../../design.md) Section 3 (Data Model), Section 4 (API Contract)
**Phase Master**: [`000_MASTER_backend.md`](000_MASTER_backend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 7. Depends on task 4 (indexes), task 5 (validator), task 6 (RBAC scoping). Consumed by task 10.
**Current File(s)**: `src/services/users/search/query.py` (new).

## 3. Agent Assignment

**Primary Agent**: `backend-engineer`
**Supporting Agents**:

- `unit-test-writer` - embedded; one test per filter combination.

## 4. Prerequisites

- [ ] Task 4 (indexes) merged in develop.
- [ ] Tasks 5, 6 (validator, RBAC) merged.
- [ ] Postgres connection pool configured at the project level.

## 5. Task Details

### 5.1 Goal

```python
def execute_query(filters: Filters) -> tuple[list[UserRow], bool]
```

Returns `(rows, has_next)` where `rows` are the up-to-`page_size` matching users and `has_next` is True if there's at least one more page.

### 5.2 Query construction rules

- Use parameterized SQL exclusively. No string concatenation.
- For substring filters: `LOWER(<column>) LIKE LOWER(?)` with `%<value>%`. Index `idx_users_name_lc` (or `idx_users_email_lc`) handles the prefix; full substring scans the bitmap.
- For exact filters (`role`, `status`): `<column> = ?`.
- For range filters (`created_after`, `created_before`): `created_at >= ?` / `created_at <= ?`.
- For RBAC scope: `organization_id = ?` (set by task 6).
- `ORDER BY <sort_key>, id` - always include `id` as the tiebreaker for stable cursor pagination.
- `LIMIT <page_size> + 1` - fetch one extra to detect "has next page". Slice off the extra row before returning.

### 5.3 Cursor handling

If `filters.cursor` is set, append a cursor predicate. For `direction=next` and `sort=created_desc`:

```sql
AND (created_at, id) < (?, ?)   -- (last_sort_key, last_id) from cursor
```

For `direction=prev`, flip to `>` and reverse the result list. Task 8 owns cursor decoding; this task assumes the cursor's payload is available as `(last_sort_key, last_id)`.

### 5.4 Files to Modify

| File | Change |
|---|---|
| `src/services/users/search/query.py` | Create - `execute_query` |
| `src/services/users/search/__init__.py` | Export |
| `tests/services/users/search/test_query.py` | Create - every filter combination |

## 6. Acceptance Criteria

- [ ] `execute_query` exists with the signature above.
- [ ] Unit tests cover: each single filter; combined filters (`name + role`, `email + status`, etc.); each sort order; cursor predicates in both directions.
- [ ] `EXPLAIN ANALYZE` outputs (in PR description) show index usage for representative queries.
- [ ] No SQL string concatenation anywhere - `ruff` / `bandit` / equivalent SAST clean.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Cursor encoding/decoding - task 8.
- Cache layer - task 9.
- RBAC scoping - task 6 (already injected).

## 8. Validation

Unit tests assert SQL correctness; integration tests (in task 10) confirm end-to-end behavior. Mutation check: change a filter's column predicate (e.g. `role` → `name`); confirm the corresponding test fails.

## 9. Rollback

`git revert`.
