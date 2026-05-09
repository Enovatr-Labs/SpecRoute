# Task 014: Build FilterChips Component

> Production task prompt. Phase 2 frontend component.

---

## 1. Objective

Build the `FilterChips` component - chips for role, status, and created-at range filters. On desktop the chips render inline; on mobile they collapse into a drawer.

After this task: component renders all three filter types, manages selection state, dispatches updates, and adapts to mobile layout.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 9 (Frontend Impact)
**Spec Reference**: [`../../requirements.md`](../../requirements.md) - R2.1, R3.1
**Architecture Reference**: [`../../design.md`](../../design.md) Section 2.2 (Components)
**Phase Master**: [`000_MASTER_frontend.md`](000_MASTER_frontend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 14. Independent of tasks 13, 15, 16. Composed by task 17.
**Current File(s)**: `frontend/components/users/search/FilterChips.tsx` (new).

## 3. Agent Assignment

**Primary Agent**: `frontend-engineer`
**Supporting Agents**:

- `unit-test-writer` - embedded.

## 4. Prerequisites

- [ ] Phase 1 acceptance met.
- [ ] Project's responsive breakpoints defined (desktop/tablet/mobile).
- [ ] List of valid roles is sourced from the same enum the backend uses.

## 5. Task Details

### 5.1 Component contract

```tsx
type FilterValue = {
  role?: string;
  status?: "active" | "disabled";
  createdAfter?: string;     // ISO date
  createdBefore?: string;    // ISO date
};

type FilterChipsProps = {
  value: FilterValue;
  validRoles: string[];                       // from backend's roles enum
  onChange: (next: FilterValue) => void;
};

export function FilterChips(props: FilterChipsProps): JSX.Element;
```

### 5.2 Behavior

- Render three chips: Role (dropdown), Status (toggle), Created (date range picker).
- Each chip shows the selected value or a default label ("All roles", "Any status", "Any date").
- Clicking a chip opens its picker.
- Selecting a value calls `onChange` with the updated `FilterValue`.
- Clearing a chip's selection clears that key in the FilterValue.
- On viewports < 768px: collapse into a drawer with a "Filters" button. The drawer contains all three pickers stacked.

### 5.3 Accessibility

- Each chip has an `aria-label` describing its current state.
- Drawer has `role="dialog"` with focus management on open.
- Date pickers use the project's accessible date-picker component (don't roll your own).

### 5.4 Files to Modify

| File | Change |
|---|---|
| `frontend/components/users/search/FilterChips.tsx` | Create - the component |
| `frontend/components/users/search/FilterChips.test.tsx` | Create - unit tests |
| `frontend/components/users/search/index.ts` | Export |

## 6. Acceptance Criteria

- [ ] All three chips render with default labels when no values are set.
- [ ] Selecting a value updates the chip label and dispatches the change.
- [ ] Clearing a value removes the key.
- [ ] Mobile breakpoint (< 768px) renders the drawer.
- [ ] Drawer focus management tested.
- [ ] Axe accessibility check clean.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Composing into the page - task 17.
- Persisting filter state in URL - task 17 owns URL state.
- Sort selector - that lives in the page (task 17), not in this component.

## 8. Validation

Unit tests for each chip type, mobile layout, and drawer behavior. Storybook story for the component in isolation.

## 9. Rollback

`git revert`.
