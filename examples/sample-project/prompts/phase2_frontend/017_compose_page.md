# Task 017: Compose `/users/search` Page

> Production task prompt. Phase 2 final task - wires the four components into the page.

---

## 1. Objective

Compose `SearchInput`, `FilterChips`, `ResultTable`, and `CursorPagination` into the `/users/search` page. Wire the API call to `GET /api/users/search`, manage URL state for shareable searches, and add a link from `/users` to the new page.

After this task: the page is reachable in develop, exercises the full user flow, and passes E2E tests for every user story in `requirements.md`.

## 2. Context

**PRD Reference**: [`../../prds/active/user-search.md`](../../prds/active/user-search.md) Section 9 (Frontend Impact)
**Spec Reference**: [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) - R1.1–R5.3, NFR-1.4
**Architecture Reference**: [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 2 (Architecture)
**Phase Master**: [`000_MASTER_frontend.md`](000_MASTER_frontend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 17. Depends on tasks 13, 14, 15, 16. Phase 2 final.
**Current File(s)**: `frontend/pages/users/search.tsx` (new; path varies by framework).

## 3. Agent Assignment

**Primary Agent**: `frontend-engineer`
**Supporting Agents**:

- `integration-test-generator` - drafts the E2E tests covering each user story.

## 4. Prerequisites

- [ ] Tasks 013, 014, 015, 016 merged.
- [ ] Backend endpoint serving in develop behind feature flag.
- [ ] Feature flag `users.search.enabled` reads correctly on the frontend.

## 5. Task Details

### 5.1 Page composition

```
┌─────────────────────────────────────────────────────────────┐
│ <SearchInput placeholder="Search by name" />                │
├─────────────────────────────────────────────────────────────┤
│ <SearchInput placeholder="Search by email" />               │
├─────────────────────────────────────────────────────────────┤
│ <FilterChips ... />            <SortSelector ... />          │
├─────────────────────────────────────────────────────────────┤
│ <ResultTable ... />                                          │
├─────────────────────────────────────────────────────────────┤
│ <CursorPagination ... />                                     │
└─────────────────────────────────────────────────────────────┘
```

The page owns: filter state, cursor state, sort state, URL synchronization, API call orchestration.

### 5.2 State management

- Local component state for the in-progress filter/sort/cursor values.
- URL reflects the current filter/sort/cursor - readers can refresh and get the same view.
- On filter or sort change: clear the cursor (return to the first page).
- On cursor change: keep filters/sort.

### 5.3 API call

Use the project's HTTP client. Construct the query string from current state, call `GET /api/users/search`, handle:

- 200 → update results table state.
- 400 → display the error code in a banner; don't blow up.
- 401 → redirect to login.
- 429 → display "Too many requests; please wait" banner with a countdown.
- 5xx → render error state with retry.

### 5.4 Feature flag

If `users.search.enabled` is false: render a fallback message linking back to `/users`. Don't render the search UI.

### 5.5 Link from `/users`

Add a "Search users" button on the `/users` page that links here. Don't change the `/users` page otherwise.

### 5.6 Files to Modify

| File | Change |
|---|---|
| `frontend/pages/users/search.tsx` | Create - page component |
| `frontend/pages/users/index.tsx` | Add the "Search users" link |
| `frontend/pages/users/search.test.tsx` | Create - page-level integration tests |
| `e2e/users-search.spec.ts` (or equivalent) | Create - E2E covering each user story |

## 6. Acceptance Criteria

- [ ] Page reachable at `/users/search`.
- [ ] All four components composed and functional.
- [ ] URL reflects filter/sort/cursor state; refresh preserves it.
- [ ] Filter or sort change clears the cursor.
- [ ] Each user story (Story 1 through Story 6 in `requirements.md`) covered by an E2E test.
- [ ] Error states handled (400, 401, 429, 5xx).
- [ ] Feature flag respected.
- [ ] "Search users" link on `/users` works.
- [ ] Page load < 1s on a reference network.
- [ ] Axe accessibility check clean.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Bulk export - separate PRD.
- Saved searches - v2.
- Cross-tenant federation - out of scope.

## 8. Validation

E2E suite runs against develop and covers:

- Search by name returns matching users.
- Search by email returns matching users.
- Filter by role.
- Filter by status.
- Cursor next + prev work in both directions.
- Empty state when no users match.
- Error state on 5xx.

## 9. Rollback

Toggle feature flag off. Page renders the fallback. No data side effects.
