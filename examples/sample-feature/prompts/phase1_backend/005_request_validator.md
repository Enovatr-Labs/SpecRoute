# Task 005: Implement Search Request Validator

> Production task prompt. Phase 1 backend component.

---

## 1. Objective

Implement `search.validate_request(filters, actor)` — the gate that converts raw HTTP query parameters into a typed, sanitized filter set or a structured 400 error. Every request to `/api/users/search` passes through this validator first.

After this task: validator function exists, unit tests cover every validation rule, and structured 400 errors are returned for every invalid input shape documented in `design.md`.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 17 (Security)
**Spec Reference**: [`../../requirements.md`](../../requirements.md) — R1.1, R1.2, R2.1, R3.1, R4.1, NFR-2.3
**Architecture Reference**: [`../../design.md`](../../design.md) Section 4.1 (API Contract — error table)
**Phase Master**: [`000_MASTER_backend.md`](000_MASTER_backend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: this is task 5 in [`../../tasks.md`](../../tasks.md). Independent of tasks 4, 6, 7, 8, 9. Consumed by task 10 (compose endpoint).
**Current File(s)**: `src/services/users/search/validator.py` (new).

The validator runs before the cache lookup. Invalid requests fail fast without touching DB or cache. The function is pure — no I/O — which makes it easy to unit-test exhaustively.

## 3. Agent Assignment

**Primary Agent**: `backend-engineer` (see [`../../agent-roster.md`](../../agent-roster.md))
**Supporting Agents**:

- `unit-test-writer` — drafts the unit tests against each validation rule.

## 4. Prerequisites

- [ ] Phase 0 complete.
- [ ] Project scaffold for the `users/search/` module exists (or this task creates it).

## 5. Task Details

### 5.1 Goal

A pure function that:

```python
def validate_request(query: dict, actor: Actor) -> Filters | ValidationError
```

returns either a `Filters` dataclass (typed, sanitized, defaults applied) or a `ValidationError` (with HTTP status + structured body).

### 5.2 Validation rules

| Field | Rule | Error code if invalid |
|---|---|---|
| `name` | length ≤ 100; no control chars | `invalid_name` |
| `email` | length ≤ 255; characters from email-friendly set | `invalid_email` |
| `role` | one of recognized roles enum | `invalid_role` (with `valid: [...]`) |
| `status` | one of `active`, `disabled` | `invalid_status` |
| `created_after`, `created_before` | RFC3339 timestamp | `invalid_date` |
| `created_after` ≤ `created_before` | range coherence | `invalid_date_range` |
| `sort` | one of `name_asc`, `name_desc`, `created_desc`, `last_activity_desc` | `invalid_sort` |
| `page_size` | integer in [1, 100]; default 50 | `page_size_too_large` or `page_size_too_small` |
| `cursor` | non-empty if provided; must decode (validated in task 8) | `invalid_cursor` |
| `direction` | `next` (default) or `prev`; only meaningful with `cursor` | `invalid_direction` |

### 5.3 Error response shape

```json
{
  "error": "<error_code>",
  "field": "<field_name>",
  "valid": ["..."]   // optional; for enum errors
}
```

HTTP status: 400 for all validation errors. The framework's error middleware adds `request_id` to the response.

### 5.4 Files to Modify

| File | Change |
|---|---|
| `src/services/users/search/validator.py` | Create — `validate_request` + `Filters` dataclass + `ValidationError` |
| `src/services/users/search/__init__.py` | Export the new symbols |
| `tests/services/users/search/test_validator.py` | Create — exhaustive validation tests |

## 6. Acceptance Criteria

- [ ] `validate_request` exists with the signature above.
- [ ] Every rule in the table has at least one passing test.
- [ ] Every error code returns the documented response shape.
- [ ] Defaults applied where the spec specifies (e.g. `page_size=50`).
- [ ] Pure function — no I/O, no DB, no cache.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- RBAC scoping based on the actor — task 6.
- Cursor decoding — task 8 (validator just checks "non-empty if provided").
- DB query — task 7.
- Rate limiting — task 12 (gateway-level).

## 8. Validation

Unit tests cover every row of the validation rules table. Mutation check: temporarily relax a rule (e.g. allow `page_size=999`); confirm a test fails. Restore.

## 9. Rollback

Pure function in a new module; rollback is `git revert`.
