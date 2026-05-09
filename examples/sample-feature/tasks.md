# Tasks: User Search

**Version**: 1.0
**Date**: 2026-05-08
**Author**: SpecForge worked example
**Status**: Approved
**Source PRD**: [`prd.md`](prd.md)
**Source Requirements**: [`requirements.md`](requirements.md)
**Source Design**: [`design.md`](design.md)

> **Spec triplet - part 3 of 3.** Numbered work plan with requirement back-references.

---

## Phase 0: Foundation and Spikes

Goal: resolve open questions; validate index plan; design cursor encoding.

### 1. Spike: Cache TTL choice (Q2)

- Run a one-week shadow trial in staging with two cache TTLs (60s and 300s).
- Measure: cache hit rate, freshness complaints, p95 latency for misses.
- Decide TTL; record in design doc.
- _Requirements: NFR-1.1_

### 2. Spike: Cursor encoding choice (Q3)

- Prototype both opaque base64 (HMAC-signed) and structured-ID variants.
- Measure: encode/decode latency, cursor size in URLs, cross-version stability.
- Decide; record in design doc.
- _Requirements: R4.1, R4.2_

### 3. Privacy review for query logging (Q1)

- Submit a privacy review describing what's logged: actor_id, filter_set_hash, result_count, duration_ms.
- Confirm no plaintext query strings logged.
- Get sign-off; record in PRD Section 17.
- _Requirements: NFR-3.3_

## Phase 1: Backend Implementation

Goal: ship the API endpoint with full filter coverage, RBAC scoping, and observability.

### 4. Add user search indexes migration

- Create migration file `migrations/202605xx_add_user_search_indexes.sql`.
- Use `CREATE INDEX CONCURRENTLY IF NOT EXISTS` for all four indexes.
- Add a smoke test that confirms each index exists after migration.
- Validate query plans in staging using `EXPLAIN ANALYZE` on representative filter combinations.
- _Requirements: R1.1, R1.2, R2.1, R3.1, NFR-1.1_

### 5. Implement search request validator

- Create `search.validate_request(filters, actor)` function.
- Validate name and email substring length and character set.
- Validate `role` against the recognized-roles enum.
- Validate `status` against `{active, disabled}`.
- Validate `created_after` / `created_before` are RFC3339 timestamps.
- Validate `page_size` in `[1, 100]`; default to 50.
- Reject invalid input with HTTP 400 and structured error body.
- Unit tests: every validation rule.
- _Requirements: R1.1, R1.2, R2.1, R3.1, R4.1, NFR-2.3_

### 6. Implement RBAC scoping in validator

- Derive `(organization_id, role)` from the authenticated actor.
- For non-admin actors, inject `organization_id` filter into the query parameters.
- For admin actors, leave the query unscoped.
- Unit tests: admin sees full corpus; non-admin sees only own org.
- Integration test: a manual cross-tenant probe rejected.
- _Requirements: R5.1, R5.2, R5.3, NFR-2.2_

### 7. Implement search query builder

- Build parameterized SQL based on the validated filter set.
- Use `LOWER(name) LIKE LOWER(?)` for name substring; same for email.
- Use exact match for `role` and `status`.
- Use range for `created_at`.
- Apply `ORDER BY <sort_key>, id` to ensure stable sort.
- Limit by `page_size + 1` to detect "has next page".
- Unit tests: every filter combination produces expected SQL.
- _Requirements: R1.1, R1.2, R1.3, R2.1, R3.1_

### 8. Implement cursor encode/decode

- Per Phase 0 decision (Task 2), implement encode/decode.
- HMAC-SHA256 signature (key from existing secrets manager).
- Round-trip property test: encode(x) → decode → x.
- Tampering detection test: modified cursor → 400.
- Replay protection: timestamp older than 24h → 400.
- _Requirements: R4.1, R4.2_

### 9. Implement Redis cache layer

- Cache key: `users.search.<sha256(filter_set + organization_id + role)>`.
- TTL: per Phase 0 decision (Task 1).
- Single-flight using SETNX lock to prevent stampede.
- On cache miss: query DB, populate cache, return.
- On cache hit: return cached payload; emit `cache_hit=true` metric.
- Unit tests: hit and miss paths.
- _Requirements: NFR-1.1_

### 10. Wire `GET /api/users/search` endpoint

- Register endpoint in the API gateway routing.
- Compose: auth → validator → cache → query → response shaping.
- Unit tests: full request lifecycle.
- _Requirements: R1.1–R5.3_

### 11. Add observability instrumentation

- Histogram `search.duration_ms` with labels `cache_hit`, `result_count_bucket`.
- Counter `search.filter_usage_total` with label `filter_name`.
- Counter `search.errors_total` with label `error_code`.
- Structured log on every search.
- Trace span linked to API gateway span.
- Unit tests: metrics are emitted with correct labels.
- _Requirements: NFR-3.1, NFR-3.2, NFR-3.3, NFR-3.4_

### 12. Add rate limiting

- Configure API gateway rate limit: 100 requests / minute / actor for `/api/users/search`.
- Integration test: 101st request within a minute returns 429 with `Retry-After`.
- _Requirements: NFR-2.4_

## Phase 2: Frontend Implementation

Goal: ship the search page wired to the API.

### 13. Build SearchInput component

- Debounced input (300ms).
- `aria-label`, full keyboard navigation.
- Unit tests: debounce timing, keyboard handlers.
- _Requirements: R1.1, NFR-1.4_

### 14. Build FilterChips component

- Role selector (dropdown of recognized roles).
- Status selector (active / disabled / both).
- Created-at range picker.
- Mobile: collapse into drawer.
- Unit tests: each filter dispatches the correct query update.
- _Requirements: R2.1, R3.1_

### 15. Build ResultTable component

- Columns: name, email, role, status, last activity.
- Empty state, error state, loading state (spinner only on >500ms).
- Row-click emits a navigation event.
- Unit tests: each render state.
- _Requirements: R1.1–R3.1, NFR-1.4_

### 16. Build CursorPagination component

- Prev/next buttons.
- Reflect current cursor in URL for shareability.
- Disable prev when on first page; disable next when no `next_cursor`.
- Unit tests: cursor state transitions.
- _Requirements: R4.1, R4.2_

### 17. Compose `/users/search` page

- Wire SearchInput + FilterChips + ResultTable + CursorPagination.
- Fetch from `/api/users/search`.
- Manage URL state for shareable searches.
- Add link from `/users` to the new page.
- E2E test: type a name, see results, click through pagination.
- _Requirements: R1.1–R5.3, NFR-1.4_

## Phase 3: Validation and Rollout

Goal: confirm performance and roll out gradually.

### 18. Load test against staging

- Tool: existing load-test harness.
- Profile: 100 RPS sustained for 10 minutes; 50/50 cache-hit/miss mix.
- Verify p95 < 200ms, p99 < 500ms, no neighbor regression.
- Record results in `examples/sample-feature/implementation-plan.md`.
- _Requirements: NFR-1.1, NFR-1.2, NFR-1.3_

### 19. Wire feature flag

- Flag name: `users.search.enabled`.
- Frontend: hide the search page when disabled; fallback link to `/users`.
- Backend: return 404 on the search endpoint when disabled (defense in depth).
- Integration test: flag off → 404; flag on → 200.
- _Requirements: (rollout)_

### 20. Production rollout 10% → 50% → 100%

- 10% traffic: 24 hours; monitor latency, error rate, support tickets.
- 50% traffic: 24 hours; same monitoring.
- 100% traffic: monitor for 7 days before declaring complete.
- _Requirements: (rollout)_

### 21. Documentation updates

- Update API reference with `/api/users/search`.
- Update admin user guide with search-page walkthrough.
- Update `docs/data-model/users.md` (or equivalent) with the new indexes.
- _Requirements: (PRD Section 12)_

### 22. Rollback drill in staging

- Simulate a triggered rollback: toggle `users.search.enabled` off in staging.
- Verify error rate drops; verify frontend falls back cleanly.
- Re-enable; verify recovery.
- Record outcome in PRD Section 19.
- _Requirements: (PRD Section 19)_

---

## Coverage check

| Requirement / NFR | Tasks |
|---|---|
| R1.1 | 4, 5, 7, 10, 13, 15, 17 |
| R1.2 | 4, 5, 7, 10, 15, 17 |
| R1.3 | 7, 10, 17 |
| R2.1 | 4, 5, 7, 10, 14, 15, 17 |
| R3.1 | 4, 5, 7, 10, 14, 15, 17 |
| R4.1 | 2, 5, 8, 10, 16, 17 |
| R4.2 | 2, 5, 8, 10, 16, 17 |
| R5.1 | 6, 10, 17 |
| R5.2 | 6, 10, 17 |
| R5.3 | 6, 10, 17 |
| NFR-1.1 | 1, 4, 9, 10, 18 |
| NFR-1.2 | 18 |
| NFR-1.3 | 18 |
| NFR-1.4 | 13, 15, 17 |
| NFR-2.1 | 6, 10 |
| NFR-2.2 | 6, 10 |
| NFR-2.3 | 5, 10 |
| NFR-2.4 | 12 |
| NFR-3.1 | 11 |
| NFR-3.2 | 11 |
| NFR-3.3 | 3, 11 |
| NFR-3.4 | 11 |
| NFR-4.1 | (existing infra) |

Every requirement maps to ≥ 1 task. Every NFR maps to ≥ 1 task.

## Done checklist

- [ ] All tasks (1–22) complete.
- [ ] Coverage table fully populated.
- [ ] All requirements have at least one passing test.
- [ ] All NFRs have a measurement or attestation.
- [ ] PRD acceptance criteria (Section 23) all met.
- [ ] Open questions (Q1, Q2, Q3) resolved.
- [ ] Documentation (PRD Section 12) updated.
