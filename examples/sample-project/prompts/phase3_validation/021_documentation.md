# Task 021: Documentation Updates

> Production task prompt. Phase 3 - documentation gate before rollout.

---

## 1. Objective

Update documentation per the PRD's Section 12 (Documentation Plan). The new endpoint, the new admin surface, and the index migration all need entries before rollout - late docs are stale docs.

After this task: API reference describes `/api/users/search`; admin user guide includes the search-page walkthrough; data-model doc notes the new indexes; changelog entry drafted.

## 2. Context

**PRD Reference**: [`../../prd.md`](../../prd.md) Section 12 (Documentation Plan)
**Spec Reference**: (none directly; this is documentation work)
**Architecture Reference**: [`../../design.md`](../../design.md) Section 4 (API Contract)
**Phase Master**: [`000_MASTER_validation.md`](000_MASTER_validation.md)
**Global Master**: [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md)
**Related Tasks**: task 21. Independent of tasks 18, 019, 020, 022. Gates task 020 (production rollout) per the release-readiness checklist.

## 3. Agent Assignment

**Primary Agent**: `prd-author`
**Supporting Agents**:

- `spec-author` - confirms cross-references to design doc are correct.

## 4. Prerequisites

- [ ] Phase 1 + Phase 2 acceptance met (so the docs describe reality, not aspiration).
- [ ] Project's API doc tooling available.

## 5. Task Details

### 5.1 API reference

Add an entry for `GET /api/users/search`:

- Request shape (query parameters from design Section 4.1).
- Response shape (200 success).
- Error responses (400, 401, 429, 500).
- Examples for each response.

Reference [`design.md`](../../design.md) Section 4 as the source.

### 5.2 Admin user guide

Add a section walking through the search workflow:

- How to navigate to the search page.
- How to use each filter.
- How to interpret the result columns.
- Edge cases: empty result, network error, rate limit.

Use screenshots if the project's docs include them. Generic data only - no real user names, real emails, etc. (Use placeholders like "Jane Example", "jane@example.com".)

### 5.3 Data-model documentation

Update the data-model doc (typically `docs/data-model/users.md` or similar) to note the four new indexes added by task 4. List them:

- `idx_users_name_lc`
- `idx_users_email_lc`
- `idx_users_status` (partial)
- `idx_users_role`

Brief rationale for each.

### 5.4 Changelog / release notes

Draft a changelog entry:

```markdown
## <Release version> - <date>

### Added

- **User search**: paginated, filterable search over the user directory at /users/search. Filter by name, email, role, status, and creation date. RBAC-scoped (admins see all users; non-admin actors see only their organization's users).
```

The product owner finalizes the customer-facing copy.

### 5.5 Files to Modify

| File | Change |
|---|---|
| API reference | Add `/api/users/search` entry |
| Admin user guide | Add search-page section |
| Data-model docs | List the new indexes |
| Changelog | Draft the entry |

## 6. Acceptance Criteria

- [ ] API reference entry merged.
- [ ] Admin user guide entry merged.
- [ ] Data-model doc updated.
- [ ] Changelog entry drafted (final wording can iterate up to release).
- [ ] All cross-references resolve.
- [ ] `/audit` returns clean.

## 7. Out of Scope

- Marketing copy - separate workstream.
- Internal architecture docs beyond the data-model entry - out of scope for this task.
- Customer email comms - handled by product / marketing.

## 8. Validation

Run `/audit` to confirm broken-link check passes. Spot-check the API reference against the live endpoint in develop.

## 9. Rollback

`git revert` the doc PR. Docs revert to pre-launch state. Acceptable.
