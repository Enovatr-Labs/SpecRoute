# Task 006: Implement RBAC Scoping

> Production task prompt. Phase 1 backend component.

---

## 1. Objective

Implement `search.apply_rbac(filters, actor)` — derives the actor's `(organization_id, role)` and injects an `organization_id` filter for non-admin actors. After RBAC scoping, the query builder (task 7) cannot return users outside the actor's authorized scope.

After this task: admin actors see the full corpus; non-admin actors see only users in their own organization. A cross-tenant probe (manual integration test) is rejected.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 17 (Security Requirements)
**Spec Reference**: [`../../requirements.md`](../../requirements.md) — R5.1, R5.2, R5.3, NFR-2.1, NFR-2.2
**Architecture Reference**: [`../../design.md`](../../design.md) Section 8 (Security Considerations)
**Phase Master**: [`000_MASTER_backend.md`](000_MASTER_backend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 6 in [`../../tasks.md`](../../tasks.md). Depends on task 5 (validator). Consumed by task 10 (compose endpoint).
**Current File(s)**: `src/services/users/search/rbac.py` (new).

This is the security gate. Forgetting RBAC scoping at this layer turns the endpoint into an enumeration attack. The validator runs first; this runs second; the query builder runs third — defense in depth.

## 3. Agent Assignment

**Primary Agent**: `backend-engineer`
**Supporting Agents**:

- `security-auditor` — reviews the boundary between authenticated and validated; reviews the test that confirms a forged cursor or filter can't bypass.
- `unit-test-writer` — embedded.

## 4. Prerequisites

- [ ] Task 5 (validator) merged.
- [ ] Auth middleware exposes the actor's `id`, `role`, `organization_id` reliably.
- [ ] The roles enum is finalized.

## 5. Task Details

### 5.1 Goal

A pure function that augments the validated filter set with RBAC scoping:

```python
def apply_rbac(filters: Filters, actor: Actor) -> Filters
```

For `actor.role == "admin"`: pass through.
For all other roles: set `filters.organization_id = actor.organization_id`. If the original filters specified a different `organization_id`, override with the actor's.

### 5.2 Validation matrix

| Actor role | Original `organization_id` | After RBAC |
|---|---|---|
| `admin` | not set | not set (full corpus) |
| `admin` | `org-X` | `org-X` (admin can scope explicitly) |
| `member` | not set | actor's `organization_id` |
| `member` | actor's own `organization_id` | actor's own (no change) |
| `member` | other org's id | actor's own (override) |
| `guest` | (any) | actor's own |

### 5.3 Anti-pattern to avoid

Do not derive `organization_id` from any filter parameter the user controls. The actor's organization comes from the authenticated session, not the request body. Mistaking this is the standard auth-boundary bug.

### 5.4 Files to Modify

| File | Change |
|---|---|
| `src/services/users/search/rbac.py` | Create — `apply_rbac` |
| `src/services/users/search/__init__.py` | Export |
| `tests/services/users/search/test_rbac.py` | Create — full validation matrix |
| `tests/integration/users_search_rbac_test.py` | Create — cross-tenant probe (manual or scripted) |

## 6. Acceptance Criteria

- [ ] `apply_rbac` exists with the signature above.
- [ ] Every row of the validation matrix has a passing test.
- [ ] A cross-tenant integration probe is rejected (a non-admin can't see users in another organization, even by setting `organization_id` explicitly in the request).
- [ ] `security-auditor` signs off on the boundary.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Authentication itself (existing middleware).
- Per-row authorization beyond organization scoping (e.g. row-level masking) — out of v1.
- Audit logging — task 11.

## 8. Validation

Unit tests cover the matrix. Integration test uses two actors in two organizations:

1. Admin sees both.
2. Member of org-A sees only org-A users.
3. Member of org-A explicitly requests `organization_id=org-B`; the response contains only org-A users (override happened).

## 9. Rollback

Pure function; `git revert`.
