# Requirements: User Search

**Version**: 1.0
**Date**: 2026-05-08
**Author**: SpecForge worked example
**Status**: Approved
**Source PRD**: [`../../prds/active/user-search.md`](../../prds/active/user-search.md)

> **Spec triplet - part 1 of 3.** Companion documents: [`design.md`](design.md), [`tasks.md`](tasks.md).

---

## 1. Introduction

User search adds a paginated, filterable, indexed lookup over the platform's user directory. Reduces admin time-to-find from ~30s to <2s and unblocks the planned RBAC redesign which requires filter-by-role.

## 2. Glossary

| Term | Definition |
|---|---|
| **Actor** | The authenticated user making the search request. |
| **Search corpus** | The set of users the actor is authorized to see (RBAC-scoped). |
| **Cursor** | An opaque, signed token representing a position in the result set. |
| **Filter set** | A combination of filter parameters (name, email, role, status, date range). |
| **Filter set hash** | A deterministic hash of the filter set, used as the cache key. |

## 3. User Stories

### Story 1: Find a specific user by name

**As an** admin, **I want** to search the user directory by partial name match, **so that** I can find the user without remembering their email.

Linked requirements: R1.1, R1.2, R1.3.

### Story 2: Filter users by role

**As an** admin doing an RBAC review, **I want** to filter users by role, **so that** I can find all users assigned a specific role.

Linked requirements: R2.1.

### Story 3: Filter users by status

**As an** admin, **I want** to filter to only active (or only disabled) users, **so that** I can focus on the relevant subset.

Linked requirements: R3.1.

### Story 4: Page through large result sets

**As an** admin, **I want** results to paginate, **so that** the page loads quickly even when the corpus is large.

Linked requirements: R4.1, R4.2.

### Story 5: Search results respect my permissions

**As a** non-admin user with limited visibility, **I want** search to return only users I'm authorized to see, **so that** I can't enumerate users in other organizations.

Linked requirements: R5.1, R5.2, R5.3.

### Story 6: Search is fast

**As an** admin, **I want** results to return in under 200ms p95, **so that** the workflow feels instant.

Linked requirements: NFR-1.1.

## 4. Requirements

### Requirement Group 1: Search by name and email

#### R1.1 - Substring search on name

**User Story:** Story 1.

**Acceptance Criteria:**

1. WHEN an actor submits a search with `name=<substring>`, THE system SHALL return users whose name contains `<substring>` (case-insensitive).
2. WHEN the substring is empty, THE system SHALL not apply the name filter.
3. WHEN the substring contains only whitespace, THE system SHALL treat it as empty.

#### R1.2 - Substring search on email

**User Story:** Story 1.

**Acceptance Criteria:**

1. WHEN an actor submits a search with `email=<substring>`, THE system SHALL return users whose email contains `<substring>` (case-insensitive).
2. WHEN the substring contains characters invalid in email addresses (e.g. spaces, control chars), THE system SHALL reject the request with HTTP 400.

#### R1.3 - Combined name and email search

**User Story:** Story 1.

**Acceptance Criteria:**

1. WHEN both `name` and `email` filters are provided, THE system SHALL return users matching **both** (logical AND).

### Requirement Group 2: Filter by role

#### R2.1 - Filter by role

**User Story:** Story 2.

**Acceptance Criteria:**

1. WHEN an actor submits a search with `role=<role>`, THE system SHALL return only users whose role exactly matches `<role>`.
2. IF `<role>` is not a recognized role, THE system SHALL respond with HTTP 400 and an error body listing valid roles.

### Requirement Group 3: Filter by status

#### R3.1 - Filter by active or disabled

**User Story:** Story 3.

**Acceptance Criteria:**

1. WHEN an actor submits a search with `status=active`, THE system SHALL return only users with `status='active'`.
2. WHEN an actor submits a search with `status=disabled`, THE system SHALL return only users with `status='disabled'`.
3. WHEN no status filter is provided, THE system SHALL return both active and disabled users.

### Requirement Group 4: Pagination

#### R4.1 - Cursor-based pagination forward

**User Story:** Story 4.

**Acceptance Criteria:**

1. WHEN the result set exceeds the page size, THE system SHALL include a `next_cursor` field in the response.
2. WHEN an actor submits a search with `cursor=<token>`, THE system SHALL return the page following the position the cursor encodes.
3. WHEN the page size is not specified, THE system SHALL default to 50.
4. WHEN the page size is greater than 100, THE system SHALL respond with HTTP 400.

#### R4.2 - Cursor-based pagination backward

**User Story:** Story 4.

**Acceptance Criteria:**

1. WHEN a cursor is consumed forward, THE system SHALL also include a `prev_cursor` field for the previous page.
2. WHEN an actor submits a search with `cursor=<prev_token>` and `direction=prev`, THE system SHALL return the page preceding the cursor's position.

### Requirement Group 5: Authorization

#### R5.1 - Authentication required

**User Story:** Story 5.

**Acceptance Criteria:**

1. WHEN an unauthenticated request hits `/api/users/search`, THE system SHALL respond with HTTP 401.

#### R5.2 - Admin sees the full corpus

**User Story:** Story 5.

**Acceptance Criteria:**

1. WHEN an actor with role `admin` searches, THE system SHALL include all users in the corpus.

#### R5.3 - Non-admin sees only own organization

**User Story:** Story 5.

**Acceptance Criteria:**

1. WHEN an actor without `admin` role searches, THE system SHALL include only users with `organization_id` matching the actor's organization.
2. WHEN a result row would otherwise reveal a user outside the actor's organization, THE system SHALL exclude it (not redact - exclude entirely).

## 5. Non-Functional Requirements

### NFR-1: Performance

- **NFR-1.1** - The system SHALL respond within p95 of 200ms for queries returning ≤ 50 results.
- **NFR-1.2** - The system SHALL respond within p99 of 500ms for queries returning ≤ 50 results.
- **NFR-1.3** - The system SHALL sustain 100 RPS without latency regression on neighboring endpoints.
- **NFR-1.4** - The frontend page SHALL load within 1 second on a reference network.

### NFR-2: Security

- **NFR-2.1** - All requests to `/api/users/search` SHALL require authentication.
- **NFR-2.2** - All requests SHALL be authorized against the actor's role (RBAC).
- **NFR-2.3** - All filter values SHALL be validated server-side (length, character set, allowed values).
- **NFR-2.4** - The system SHALL rate-limit search requests to 100 per minute per actor.

### NFR-3: Observability

- **NFR-3.1** - The system SHALL emit a metric `search.duration_ms` (histogram) on every request, labeled with `cache_hit` and `result_count_bucket`.
- **NFR-3.2** - The system SHALL emit a metric `search.filter_usage_total` (counter) labeled with the filter name(s) used.
- **NFR-3.3** - The system SHALL emit a structured log entry on every search with `request_id`, `actor_id`, `filter_set_hash`, `result_count`, `duration_ms`.
- **NFR-3.4** - The system SHALL emit a trace span linked to the API gateway span.

### NFR-4: Reliability

- **NFR-4.1** - The endpoint SHALL meet the existing user-service SLO of 99.9% availability.

## 6. Out of Scope

- Bulk export of search results (separate PRD).
- Cross-tenant federated search.
- Saved or shared searches.
- Personalization (recent contacts boosted).
- Full-text search of user-generated content beyond the columns defined here.

## 7. Open Questions

| ID | Question | Owner | Resolution target |
|---|---|---|---|
| Q1 | Should the search log query strings for analytics? Privacy review needed. | Privacy lead | Before Phase 1 |
| Q2 | Cache TTL - 60s or 300s? | Performance lead | Phase 0 spike |
| Q3 | Cursor encoding - opaque base64 vs structured ID? | Tech lead | Phase 0 spike |

---

## Appendix: Requirement → User Story Map

| Requirement | User Story |
|---|---|
| R1.1 | Story 1 |
| R1.2 | Story 1 |
| R1.3 | Story 1 |
| R2.1 | Story 2 |
| R3.1 | Story 3 |
| R4.1 | Story 4 |
| R4.2 | Story 4 |
| R5.1 | Story 5 |
| R5.2 | Story 5 |
| R5.3 | Story 5 |
| NFR-1.1 | Story 6 |
