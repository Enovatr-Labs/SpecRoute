# 000_MASTER_frontend - Phase 2: Frontend Implementation

> Phase entry-point. Read this before any task in Phase 2.

---

## Phase Summary

Phase 2 builds the `/users/search` page that consumes the Phase 1 endpoint. Four reusable components (`SearchInput`, `FilterChips`, `ResultTable`, `CursorPagination`) are built independently in parallel, then composed into the page (task 17). E2E tests cover the user stories from `requirements.md`.

The endpoint deployed in Phase 1 is the API contract for this phase. If a frontend task discovers the API doesn't match what the design specified, fix the API (re-open Phase 1) - don't paper over with frontend workarounds.

## Goals

By the end of Phase 2:

1. Four reusable components shipped, individually unit-tested.
2. `/users/search` page composed and reachable.
3. E2E tests pass for every user story (Story 1 through Story 6 in `requirements.md`).
4. Initial page load < 1 second on a reference network.
5. Empty / error / loading states all rendering correctly.
6. Mobile layout collapses filters into a drawer.
7. Accessibility: keyboard navigation, `aria-label` / `aria-live` regions, screen-reader friendly.

## Prerequisites

- [ ] Phase 1 acceptance met.
- [ ] Endpoint in develop returns the documented response shape.
- [ ] Feature flag `users.search.enabled` works (off → 404).
- [ ] E2E test infrastructure available against develop.

## Task Prompts

| # | Task | Primary Agent | Supporting Agents |
|---|---|---|---|
| 013 | [`013_search_input.md`](013_search_input.md) | `frontend-engineer` | `unit-test-writer` |
| 014 | [`014_filter_chips.md`](014_filter_chips.md) | `frontend-engineer` | `unit-test-writer` |
| 015 | [`015_result_table.md`](015_result_table.md) | `frontend-engineer` | `unit-test-writer` |
| 016 | [`016_cursor_pagination.md`](016_cursor_pagination.md) | `frontend-engineer` | `unit-test-writer` |
| 017 | [`017_compose_page.md`](017_compose_page.md) | `frontend-engineer` | `integration-test-generator` |

### Execution order

```
    013, 014, 015, 016    (parallel - independent components)
            │
            ▼
           017             (compose into the page)
```

## Agent Assignments

- **`frontend-engineer`** - owns all five tasks.
- **`unit-test-writer`** - embedded; one test file per component.
- **`integration-test-generator`** - handles the E2E for task 017.

## Acceptance Criteria

Phase 2 is complete when **all** of the following are true:

- [ ] Tasks 013–017 merged.
- [ ] `/users/search` page reachable from `/users` link.
- [ ] All four components unit-tested (render states, keyboard handling, debouncing, cursor state transitions).
- [ ] E2E test exercises: type a name → see results → click through pagination → empty state → error state.
- [ ] Page load < 1s confirmed via lighthouse or equivalent.
- [ ] A11y check passes (axe or equivalent).
- [ ] Mobile layout exercised in E2E.
- [ ] `/audit` returns clean.

## Risks Specific to Phase 2

| Risk | Mitigation |
|---|---|
| Bundle size regression (NFR for initial JS bundle) | Code-split the search page; lazy-load FilterChips drawer |
| Debounce timing too aggressive - feels laggy | 300ms standard; revisit only if user testing flags |
| API contract drift discovered late | E2E tests run against develop; mismatches surface before merge |
| Cursor URL state gets unwieldy | Cursors are opaque; store only the current cursor in the URL, not the full filter state if it's bulky |

## How to Execute

1. Read [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md).
2. Read this file end to end.
3. Confirm Phase 1 acceptance is met.
4. Build tasks 013–016 (parallel if possible).
5. Compose into the page (task 017).
6. Run E2E suite.
7. Validate against acceptance criteria.
8. Promote to Phase 3 ([`../phase3_validation/000_MASTER_validation.md`](../phase3_validation/000_MASTER_validation.md)).
