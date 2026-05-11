# Task 019: Wire Feature Flag

> Production task prompt. Phase 3 - defense-in-depth feature flagging.

---

## 1. Objective

Configure the `users.search.enabled` feature flag end-to-end. Backend endpoint returns 404 when off; frontend page redirects to `/users` when off. The flag is the kill-switch for production rollout per the PRD's rollback strategy.

After this task: flag works on/off in staging and develop; integration tests confirm both states.

## 2. Context

**PRD Reference**: [`../../prds/active/user-search.md`](../../prds/active/user-search.md) Section 19 (Rollback Strategy)
**Spec Reference**: [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) - none directly; this is rollout infrastructure
**Architecture Reference**: [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 11 (Rollout Considerations)
**Phase Master**: [`000_MASTER_validation.md`](000_MASTER_validation.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 19. Depends on Phase 2 acceptance. Gates task 020 (production rollout) and task 022 (rollback drill).

## 3. Agent Assignment

**Primary Agent**: `backend-engineer`
**Supporting Agents**:

- `frontend-engineer` - wires the flag check on the frontend side.

## 4. Prerequisites

- [ ] Project's feature-flag service is operational (LaunchDarkly / Statsig / project-internal / equivalent).
- [ ] Staging and production both have the flag service available.

## 5. Task Details

### 5.1 Backend wiring

The handler from task 010 already includes a flag check at the top:

```python
def handle_request(request, actor):
    if not feature_flags.get("users.search.enabled", actor):
        return http_404({"error": "not_found"})
    # ... rest of the composition
```

If the flag check isn't there yet, add it. Default to `false` in the flag service's UI (off until explicitly enabled).

### 5.2 Frontend wiring

The page from task 017 already includes a flag check. Verify it:

- Flag off: render a fallback message ("This feature is not available; use `/users` instead.").
- Flag on: render the search UI.

### 5.3 Flag scoping

Per-actor or per-organization scoping (per the project's flag service capabilities). Cumulative rollout strategies (10% → 50% → 100%) require percentage-based targeting; confirm the flag service supports it.

### 5.4 Files to Modify

| File | Change |
|---|---|
| Backend handler (from task 010) | Verify or add the flag check |
| Frontend page (from task 017) | Verify or add the flag check |
| `tests/integration/users_search_flag_test.py` | Create - flag off → 404; flag on → 200 |
| Feature flag service config | Register `users.search.enabled` as a new flag (default off) |

## 6. Acceptance Criteria

- [ ] Backend returns 404 with the flag off; 200 (or other documented status) with the flag on.
- [ ] Frontend renders the fallback with the flag off; the search UI with the flag on.
- [ ] Integration test exercises both states.
- [ ] Flag works in staging.
- [ ] Default flag value is `false`.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Per-actor / percentage-based targeting - handled by the flag service itself.
- Flag value change UI - handled by the flag service's UI.

## 8. Validation

Toggle the flag in staging via the flag service UI and confirm the behavior change within the flag service's propagation window (typically seconds).

## 9. Rollback

The flag itself IS the rollback. If post-launch the feature misbehaves, toggling the flag to off is the recovery path. The integration test that confirms the off state matters precisely for this scenario.
