# Task 016: Build CursorPagination Component

> Production task prompt. Phase 2 frontend component.

---

## 1. Objective

Build the `CursorPagination` component — prev/next buttons that consume the cursor metadata from the API response and emit cursor-change events. Reflects the current cursor in the URL for shareability.

After this task: prev/next buttons work, are correctly disabled when no cursor is available, and the current cursor lives in the URL so users can share or refresh without losing pagination state.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 9 (Frontend Impact)
**Spec Reference**: [`../../requirements.md`](../../requirements.md) — R4.1, R4.2
**Architecture Reference**: [`../../design.md`](../../design.md) Section 4.1 (API Contract — cursor fields)
**Phase Master**: [`000_MASTER_frontend.md`](000_MASTER_frontend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 16. Independent of tasks 13, 14, 15. Composed by task 17.
**Current File(s)**: `frontend/components/users/search/CursorPagination.tsx` (new).

## 3. Agent Assignment

**Primary Agent**: `frontend-engineer`
**Supporting Agents**:

- `unit-test-writer` — embedded.

## 4. Prerequisites

- [ ] Phase 1 acceptance met.
- [ ] Project's URL-state management pattern decided (history.pushState directly, or a router-provided primitive).

## 5. Task Details

### 5.1 Component contract

```tsx
type CursorState = {
  prevCursor: string | null;
  nextCursor: string | null;
};

type CursorPaginationProps = {
  state: CursorState;
  onChange: (cursor: string, direction: "next" | "prev") => void;
};

export function CursorPagination(props: CursorPaginationProps): JSX.Element;
```

### 5.2 Behavior

- Render two buttons: "Previous" and "Next".
- Disable "Previous" when `prevCursor === null`.
- Disable "Next" when `nextCursor === null`.
- On click: call `onChange` with the cursor and direction.
- Reset to first page when filter parameters change (page handles this; component just renders state).

### 5.3 URL state (managed by the page, but documented here)

The page (task 17) reads the cursor from the URL on mount and writes the cursor on every change. The format is `?cursor=<token>&direction=<next|prev>`. When the user changes filters, the page clears the cursor from the URL.

### 5.4 Accessibility

- Buttons have clear `aria-label`s ("Previous page", "Next page").
- Disabled buttons use `aria-disabled` + `disabled` attribute.
- Keyboard: Tab navigates to each button; Enter / Space activates.

### 5.5 Files to Modify

| File | Change |
|---|---|
| `frontend/components/users/search/CursorPagination.tsx` | Create |
| `frontend/components/users/search/CursorPagination.test.tsx` | Create — state transitions |
| `frontend/components/users/search/index.ts` | Export |

## 6. Acceptance Criteria

- [ ] Buttons render and disable correctly per the cursor state.
- [ ] `onChange` fires with the right cursor and direction.
- [ ] Keyboard activation works (Enter / Space on each button).
- [ ] Axe accessibility check clean.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- URL state management — owned by the page (task 17).
- Page-size selector — out of v1.
- "Jump to page N" — cursor pagination doesn't support this; out of scope.

## 8. Validation

Unit tests for each state transition. Storybook stories for the four states (no cursors, only next, only prev, both).

## 9. Rollback

`git revert`.
