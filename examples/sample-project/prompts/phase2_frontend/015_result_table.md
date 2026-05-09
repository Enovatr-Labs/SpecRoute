# Task 015: Build ResultTable Component

> Production task prompt. Phase 2 frontend component.

---

## 1. Objective

Build the `ResultTable` component - renders user-search results with five columns (name, email, role, status, last activity) and handles empty / error / loading states. Row clicks emit a navigation event consumed by the page.

After this task: component renders all four states, exposes a clean row-click contract, and is keyboard-navigable.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 9 (Frontend Impact)
**Spec Reference**: [`../../requirements.md`](../../requirements.md) - R1.1–R3.1, NFR-1.4
**Architecture Reference**: [`../../design.md`](../../design.md) Section 4.1 (API Contract - response shape)
**Phase Master**: [`000_MASTER_frontend.md`](000_MASTER_frontend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 15. Independent of tasks 13, 14, 16. Composed by task 17.
**Current File(s)**: `frontend/components/users/search/ResultTable.tsx` (new).

## 3. Agent Assignment

**Primary Agent**: `frontend-engineer`
**Supporting Agents**:

- `unit-test-writer` - embedded.

## 4. Prerequisites

- [ ] Phase 1 acceptance met (response shape is stable).
- [ ] Project's table / list primitive available.

## 5. Task Details

### 5.1 Component contract

```tsx
type UserRow = {
  id: string;
  name: string;
  email: string;
  role: string;
  status: "active" | "disabled";
  lastActivityAt: string | null;   // ISO date or null
};

type ResultTableProps = {
  state:
    | { kind: "loading" }
    | { kind: "empty"; message?: string }
    | { kind: "error"; message: string; onRetry: () => void }
    | { kind: "results"; rows: UserRow[] };
  onRowClick: (user: UserRow) => void;
};

export function ResultTable(props: ResultTableProps): JSX.Element;
```

### 5.2 States

- **Loading**: spinner shown only after 500ms (avoid flash on fast queries). Non-blocking text "Searching…".
- **Empty**: rendered when `rows.length === 0` after a successful search. Message defaults to "No users found".
- **Error**: rendered with retry button.
- **Results**: table with five columns; rows clickable.

### 5.3 Accessibility

- Table semantics: `<table>`, `<thead>`, `<tbody>`. Don't fake with divs.
- Header cells use `<th scope="col">`.
- Each row is keyboard-focusable; Enter triggers `onRowClick`.
- Loading state has `aria-live="polite"` so screen readers announce it.
- Empty / error states are also announced.

### 5.4 Last activity display

Render `lastActivityAt` as a relative time (e.g. "2 hours ago"). Null displays as "Never".

### 5.5 Files to Modify

| File | Change |
|---|---|
| `frontend/components/users/search/ResultTable.tsx` | Create - the component |
| `frontend/components/users/search/ResultTable.test.tsx` | Create - each state |
| `frontend/components/users/search/index.ts` | Export |

## 6. Acceptance Criteria

- [ ] Each state renders correctly.
- [ ] Loading spinner appears only after 500ms.
- [ ] Empty / error / loading states are announced (`aria-live`).
- [ ] Row click + Enter both fire `onRowClick`.
- [ ] Table semantics correct (axe check clean).
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Pagination controls - task 16.
- Composing into the page - task 17.
- Sorting (the table is read-only; sort is dispatched via the page's sort selector).

## 8. Validation

Unit tests for each state. Storybook stories for each state. Cross-browser smoke (Chrome, Firefox, Safari).

## 9. Rollback

`git revert`.
