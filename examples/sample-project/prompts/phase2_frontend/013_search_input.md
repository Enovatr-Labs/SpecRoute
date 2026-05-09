# Task 013: Build SearchInput Component

> Production task prompt. Phase 2 frontend component.

---

## 1. Objective

Build the `SearchInput` component - a debounced text input that emits a search query when the user pauses typing. The component is reused for both the name and email substring filters.

After this task: component renders, debounces 300ms, emits the right events, has full keyboard navigation, passes accessibility checks, and has unit tests for each behavior.

## 2. Context

**PRD Reference**: [`../../prds/active/user-search.md`](../../prds/active/user-search.md) Section 9 (Frontend Impact)
**Spec Reference**: [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) - R1.1, R1.2, NFR-1.4
**Architecture Reference**: [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 2.2 (Components)
**Phase Master**: [`000_MASTER_frontend.md`](000_MASTER_frontend.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 13. Independent of tasks 14, 15, 16. Composed by task 17.
**Current File(s)**: `frontend/components/users/search/SearchInput.tsx` (new; path varies by project).

## 3. Agent Assignment

**Primary Agent**: `frontend-engineer`
**Supporting Agents**:

- `unit-test-writer` - embedded.

## 4. Prerequisites

- [ ] Phase 1 acceptance met (endpoint accepts requests).
- [ ] Project's component library / UI kit available.
- [ ] Test infrastructure for components configured (jest / vitest / equivalent + testing-library).

## 5. Task Details

### 5.1 Component contract

```tsx
type SearchInputProps = {
  placeholder: string;
  initialValue?: string;
  onQueryChange: (query: string) => void;   // fires after debounce
  ariaLabel: string;
  debounceMs?: number;                       // default 300
};

export function SearchInput(props: SearchInputProps): JSX.Element;
```

### 5.2 Behavior

- Render a single `<input>` with a search icon and clear button.
- Debounce typing by `debounceMs` (default 300). Emit `onQueryChange(value)` once the user pauses.
- Emit immediately on Enter (no debounce).
- Emit immediately when the user clears the input.
- Render the `aria-label` on the input.
- Trim leading/trailing whitespace before emitting.

### 5.3 Accessibility

- `aria-label` is mandatory.
- The clear button has `aria-label="Clear search"`.
- Tab navigation: input → clear button (when value is non-empty).
- Esc clears the input and emits an empty query.

### 5.4 Files to Modify

| File | Change |
|---|---|
| `frontend/components/users/search/SearchInput.tsx` | Create - the component |
| `frontend/components/users/search/SearchInput.test.tsx` | Create - unit tests |
| `frontend/components/users/search/index.ts` (if used) | Export |

## 6. Acceptance Criteria

- [ ] Renders with the documented props.
- [ ] Debounce timing tested (typing fires after 300ms; Enter fires immediately; Esc fires immediately).
- [ ] Trim behavior tested.
- [ ] Keyboard navigation tested (Tab, Esc).
- [ ] `aria-label` present and verified.
- [ ] Axe accessibility check clean.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Composing the input into the page - task 17.
- Network calls - the component just emits; the page (task 17) wires the API call.
- Server-side validation - task 5.

## 8. Validation

Unit tests cover each behavior. Storybook story (if the project uses Storybook) demonstrates the component in isolation.

## 9. Rollback

`git revert`. Component removal doesn't affect anything else until task 17 wires it into the page.
