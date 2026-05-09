# Requirements: User Search

## Overview

Add a tenant-scoped user search endpoint and UI surface so administrators can find users by name, email, role, status, and created-at range.

## Requirements

### R1: Search Query

**User story:** As an administrator, I want to search users by name or email so I can find a user without scrolling the full directory.

**Acceptance criteria:**

- **R1.1** The API accepts `q` as a case-insensitive substring search over name and email.
- **R1.2** Empty `q` is allowed only when at least one filter is present.
- **R1.3** Results are scoped to the caller's tenant.

### R2: Filters

**User story:** As an administrator, I want to filter by role, status, and created-at range so I can narrow broad result sets.

**Acceptance criteria:**

- **R2.1** Role and status filters are exact matches.
- **R2.2** Created-at range supports inclusive `created_after` and `created_before` parameters.
- **R2.3** Invalid filters return a structured validation error.

### R3: Pagination

**User story:** As an administrator, I want cursor-based pagination so result lists stay stable across pages.

**Acceptance criteria:**

- **R3.1** The response includes `next_cursor` when another page exists.
- **R3.2** Cursor contents are opaque to clients.
- **R3.3** Page size is capped at 50.

## Non-Functional Requirements

- **NFR-1.1** p95 API latency is under 200ms for indexed searches.
- **NFR-1.2** Search emits latency, result-count, and error metrics.
- **NFR-1.3** Query strings containing email patterns are not logged in plaintext.
