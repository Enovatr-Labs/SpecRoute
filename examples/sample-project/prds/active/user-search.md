# PRD: User Search

**Version**: 1.0
**Date**: 2026-05-08
**Author**: SpecRoute worked example
**Status**: Approved
**Architecture Reference**: [`../../specs/user-search/design.md`](../../specs/user-search/design.md)
**Scope**: Add a paginated, filterable, indexed user-directory search to the platform's admin and self-service surfaces. In scope: API + frontend + observability. Out of scope: bulk export (separate PRD), cross-tenant federation.

> This is the canonical worked example for SpecRoute. It exercises every artifact shape end-to-end: a 23-section PRD; a spec triplet (`../../specs/user-search/requirements.md`, `../../specs/user-search/design.md`, `../../specs/user-search/tasks.md`); an agent roster; the full phased prompt set (1 global master, 4 phase masters, 22 numbered task prompts under `prompts/`); and an implementation plan. Generic feature, no proprietary domain.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Background and Motivation](#2-background-and-motivation)
3. [Goals and Success Metrics](#3-goals-and-success-metrics)
4. [Scope and Boundaries](#4-scope-and-boundaries)
5. [Target Architecture](#5-target-architecture)
6. [Domain / Module Specifications](#6-domain--module-specifications)
7. [Data Strategy](#7-data-strategy)
8. [Infrastructure](#8-infrastructure)
9. [Frontend Impact](#9-frontend-impact)
10. [Backend / Integration Contracts](#10-backend--integration-contracts)
11. [Deployment and Operations Tooling](#11-deployment-and-operations-tooling)
12. [Documentation Plan](#12-documentation-plan)
13. [Script and Tooling Changes](#13-script-and-tooling-changes)
14. [Testing Strategy](#14-testing-strategy)
15. [Migration / Rollout Phases](#15-migration--rollout-phases)
16. [Multi-Cloud / Multi-Env Deployment](#16-multi-cloud--multi-env-deployment)
17. [Security Requirements](#17-security-requirements)
18. [Performance Requirements](#18-performance-requirements)
19. [Rollback Strategy](#19-rollback-strategy)
20. [Non-Functional Requirements](#20-non-functional-requirements)
21. [Risks and Mitigations](#21-risks-and-mitigations)
22. [Dependencies](#22-dependencies)
23. [Acceptance Criteria](#23-acceptance-criteria)

---

## 1. Executive Summary

The platform supports tens of thousands of registered users. Today, finding a specific user requires either knowing their exact email or scrolling a paginated list. This PRD adds a search capability - paginated, filterable, indexed - that returns matches in p95 < 200ms across the full corpus.

The change is scoped to one new API endpoint (`GET /api/users/search`), one new UI surface (the user-directory search page), and the matching observability. No data migration is required; an index addition at deploy time is sufficient.

By the numbers: cuts time-to-find from ~30s (manual scroll) to <2s (search-result render); enables admin workflows currently blocked by the lookup gap.

## 2. Background and Motivation

### 2.1 Current State

The platform has a `/users` admin page that paginates the user table 50 rows at a time, ordered by `created_at desc`. There is no search; admins find users by:

- Knowing the email (and pasting it into a URL filter parameter).
- Scrolling.

Roughly 18% of admin sessions involve at least one user lookup; current latency is bounded by the user's scroll patience, not by the system.

### 2.2 Why Now

Three converging signals:

- Support tickets containing "I can't find user X" tripled in the last quarter as registration grew.
- Admin sessions that include a user lookup are 3.4× longer than those that don't, indicating real friction.
- A planned RBAC redesign (separate PRD) requires admins to find users by role, which is impossible today.

### 2.3 Industry / Internal Precedent

Standard pattern. Indexed search with cursor-based pagination on a `users` table is a well-trod path. No novel problem here; the cost is execution time, not research.

### 2.4 Alignment

Unblocks the RBAC PRD; reduces support ticket volume; improves admin onboarding. No conflict with in-flight initiatives.

---

## 3. Goals and Success Metrics

### 3.1 Goals

In priority order:

1. **Cut admin time-to-find a user from ~30s to <2s** - measured via session telemetry.
2. **Enable filter-by-role and filter-by-status** - required by the RBAC redesign.
3. **Stay within the platform's p95 latency budget** - search adds load, must not regress neighbors.

### 3.2 Non-Goals

- **Bulk export** - separate PRD owns CSV/JSON export of search results.
- **Cross-tenant federation** - search is single-tenant scoped.
- **Free-text search beyond name + email** - no full-document search; columns only.
- **Saved searches / shared searches** - out of scope for v1.

### 3.3 Success Metrics

| Metric | Baseline | Target | Measurement method |
|---|---|---|---|
| Time-to-find (median) | ~30s | < 2s | Session telemetry: time between admin nav and result-row click |
| Search-page p95 latency | n/a | < 200ms | API metric `search.duration_ms` |
| Admin session length when lookup is involved | 3.4× baseline | 1.5× baseline | Session telemetry comparison |
| Support tickets with "can't find user" | rising | < baseline | Ticket tag counts month-over-month |

---

## 4. Scope and Boundaries

### 4.1 In Scope

- One API endpoint: `GET /api/users/search`.
- One UI surface: the user-directory search page (replaces `/users` table view; the table view remains as fallback).
- Filters: name (substring), email (substring), role (exact), status (active / disabled), created-at range.
- Sort: name asc/desc, created-at, last-activity.
- Pagination: cursor-based.
- Indexing: deferred forward-compatible migration adds two indexes.
- Observability: latency histogram, result-count gauge, filter-usage counter.

### 4.2 Out of Scope

- Bulk export of search results - separate PRD.
- Cross-tenant search - explicitly disallowed by tenant isolation.
- Full-text search of user-generated content - different scope, different infrastructure.
- Saved / shared searches - v2.
- Search personalization (boosted recent contacts) - v2.

### 4.3 Open Questions

| Question | Owner | Resolution target |
|---|---|---|
| Should the search log query strings for analytics? Privacy review needed. | Privacy lead | Before Phase 1 starts |
| Cache TTL - 60s or 300s? Performance vs freshness trade-off. | Performance lead | Phase 0 spike |
| Cursor encoding - opaque base64 vs structured ID? | Tech lead | Phase 0 spike |

---

## 5. Target Architecture

```
┌─────────────────────────┐       ┌────────────────────────┐
│  Frontend               │       │  Backend (Search)      │
│  /users/search page     │──────▶│  GET /api/users/search │
│  ────────────           │       │  ────────────────────  │
│  - Search input         │       │  - Auth (RBAC)         │
│  - Filter chips         │       │  - Query validator     │
│  - Result table         │       │  - Cache lookup (60s)  │
│  - Cursor pagination    │       │  - DB query (indexed)  │
└─────────────────────────┘       │  - Cache populate      │
                                   │  - Metrics emission    │
                                   └──────────┬─────────────┘
                                              │
                                   ┌──────────▼─────────────┐
                                   │  Postgres (users)      │
                                   │  + idx_users_name_lc   │
                                   │  + idx_users_email_lc  │
                                   │  + idx_users_status    │
                                   │  + idx_users_role      │
                                   └────────────────────────┘
```

The architecture is a single new endpoint backed by indexed Postgres queries with a short-TTL cache layer. No new services. No new infrastructure components.

See [`../../specs/user-search/design.md`](../../specs/user-search/design.md) for the full design including sequence diagrams.

---

## 6. Domain / Module Specifications

### 6.1 `search` module (backend)

- **Responsibility**: Validate, plan, execute user-directory queries. Emit metrics. Cache repeated queries.
- **Inputs**: HTTP `GET /api/users/search?<filters>`.
- **Outputs**: JSON result page + cursor + metadata.
- **Owner**: Platform team.

### 6.2 `users.search` (frontend)

- **Responsibility**: Render the search input, filter chips, results table, and pagination controls. Wire cursor-based fetch.
- **Inputs**: User keystrokes + filter selections.
- **Outputs**: API calls to `/api/users/search` + rendered results.
- **Owner**: Platform team.

---

## 7. Data Strategy

### 7.1 Data Stores

| Store | Purpose | Schema owner | Migration plan |
|---|---|---|---|
| Postgres `users` table (existing) | User record source of truth | Platform team | Forward-compatible - only adds indexes |
| Redis (existing) | 60s TTL cache for search results | Platform team | No schema change; uses existing instance |

### 7.2 Schema Changes

No column changes. Four new indexes:

```sql
CREATE INDEX CONCURRENTLY idx_users_name_lc       ON users (LOWER(name) text_pattern_ops);
CREATE INDEX CONCURRENTLY idx_users_email_lc      ON users (LOWER(email) text_pattern_ops);
CREATE INDEX CONCURRENTLY idx_users_status        ON users (status) WHERE status = 'active';
CREATE INDEX CONCURRENTLY idx_users_role          ON users (role);
```

`CREATE INDEX CONCURRENTLY` avoids long locks. Migration is forward-compatible.

### 7.3 Data Retention and Privacy

- Query strings are not logged in plaintext if they contain email patterns (privacy lead approval pending; see Section 4.3).
- Cache entries expire at 60s; no long-term storage of query patterns.
- Result rows include only public-profile fields (name, email, role, last-activity-date) - no PII beyond what's already in the user record.

---

## 8. Infrastructure

### 8.1 Compute and Networking

No new services. The existing `api` gateway routes `/api/users/search` to the existing `users` service.

### 8.2 Observability

- Metric `search.duration_ms` (histogram, labels: `cache_hit`, `result_count_bucket`).
- Metric `search.result_count` (histogram).
- Metric `search.filter_usage_total` (counter, label: `filter_name`).
- Log: structured entry on every search with `request_id`, `actor_id`, `filter_set_hash`, `result_count`, `duration_ms`.
- Trace: search spans linked to API gateway span.

### 8.3 Secrets Management

No new secrets. Uses existing DB credentials and Redis credentials provisioned via the project's secrets management pattern.

---

## 9. Frontend Impact

### 9.1 New UI Surfaces

- `/users/search` - new page; the user-directory search UI.

### 9.2 Modified Surfaces

- `/users` - existing user-table page; add a "Search users" button that links to the new page.

### 9.3 UX Considerations

- **Accessibility**: Search input has a clear label, `aria-live` region for result count updates, full keyboard navigation through filters and results.
- **Error states**: Network failure, validation failure, "no results" each have explicit UI.
- **Loading states**: Debounced 300ms; show spinner only on long queries (>500ms).
- **Responsive**: Mobile layout collapses filters into a drawer.

---

## 10. Backend / Integration Contracts

### 10.1 New APIs

| Endpoint | Method | Purpose | Auth |
|---|---|---|---|
| `/api/users/search` | GET | Paginated, filterable user search | Required; RBAC-scoped |

See [`../../specs/user-search/design.md`](../../specs/user-search/design.md) Section 4.1 for the full request/response schema.

### 10.2 Modified APIs

None.

### 10.3 Event Contracts

None - search is read-only.

---

## 11. Deployment and Operations Tooling

- New CI step: index-migration validation in staging.
- No new runbook entries; existing user-service runbooks cover the search surface.
- Rollback procedure: feature flag `users.search.enabled` (Section 19).

---

## 12. Documentation Plan

| Document | Action | Owner |
|---|---|---|
| API reference | add `/api/users/search` endpoint | Platform team |
| Admin user guide | add search-page walkthrough | Docs |
| `docs/data-model/users.md` | note the new indexes | Platform team |

---

## 13. Script and Tooling Changes

- New migration: `migrations/202605xx_add_user_search_indexes.sql`.
- No new operational scripts.

---

## 14. Testing Strategy

### 14.1 Unit Tests

- Query builder produces expected SQL for each filter combination.
- Cursor encoding round-trips.
- Cache key derivation is deterministic.

### 14.2 Integration Tests

- Full request → DB → response cycle for representative queries.
- Cache hit / miss paths.
- RBAC enforcement (admin sees all; regular user sees own org only).

### 14.3 End-to-End Tests

- Admin navigates to `/users/search`, types a name, sees results.
- Filter combinations produce correct results.
- Pagination cursor works in both directions.
- Empty state, error state.

### 14.4 Performance and Load Tests

- p95 latency < 200ms for queries returning ≤ 50 results.
- Concurrent load: 100 RPS sustained without latency regression on neighbors.

### 14.5 Security Tests

- SQLi attempt via filter values blocked at validation.
- Cross-tenant query attempt blocked at auth.
- Rate-limiting prevents enumeration attacks.

---

## 15. Migration / Rollout Phases

| Phase | Duration | Goals | Acceptance |
|---|---|---|---|
| Phase 0 | 1 week | Spikes (cache TTL, cursor encoding); privacy review | Open questions resolved |
| Phase 1 | 1 week | Backend: index migration + endpoint + tests | API endpoint passes integration tests |
| Phase 2 | 1 week | Frontend: search page + filter wiring | E2E tests pass |
| Phase 3 | 1 week | Observability + load test + rollout to 10% | p95 < 200ms confirmed in production |

---

## 16. Multi-Cloud / Multi-Env Deployment

| Environment | Branch | Cloud / Region | Notes |
|---|---|---|---|
| local-dev | `develop` | Local | Index migration runs on docker-compose Postgres |
| develop | `develop` | Example dev region (`us-east-1`) | Migrate first; validate before staging promotion |
| staging | `staging` | Example staging region (`us-east-2`) | Full E2E + load test gate |
| production | `main` | Example production region (`us-west-2`) | 10% → 50% → 100% rollout via feature flag |

---

## 17. Security Requirements

- **Authentication**: Required; existing session auth. Anonymous requests rejected.
- **Authorization**: RBAC-scoped - admin role sees all users; regular roles see users within their organization only.
- **Audit logging**: Every search logged with actor, filter hash, result count.
- **Compliance**: GDPR - search-result rows include only fields the actor is authorized to see; query logging excludes PII patterns (privacy review pending).
- **Threat model**: Enumeration attack is the primary concern; rate limiting (100/min/user) and audit logging mitigate.

---

## 18. Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| API p95 latency | < 200ms | For queries returning ≤ 50 results |
| API p99 latency | < 500ms | Worst-case bound |
| Cache hit rate (steady state) | > 40% | Repeated admin queries hit cache |
| Concurrent throughput | ≥ 100 RPS | Without latency regression on neighbors |
| Frontend page load | < 1s | Including initial render of empty results |

Performance regressions block merge; not follow-ups.

---

## 19. Rollback Strategy

### 19.1 Triggers

- p95 latency > 500ms sustained for 5 minutes.
- Error rate > 1% sustained for 5 minutes.
- Customer-reported correctness regression.

### 19.2 Procedure

1. Toggle feature flag `users.search.enabled` to `false`. Frontend falls back to the existing `/users` table view.
2. Verify error rates drop below threshold within 1 minute.
3. Open incident ticket; investigate.

### 19.3 Recovery

- Indexes are forward-compatible; no DB rollback needed.
- Cache flushes naturally at TTL expiry.
- Re-enable the feature flag after fix lands and is validated in staging.

---

## 20. Non-Functional Requirements

- **Availability**: 99.9% (existing user-service SLO).
- **Reliability**: RPO/RTO match the user service.
- **Maintainability**: Search module ≤ 800 LOC; tests ≥ 80% line coverage.
- **Observability**: Metrics, logs, traces per Section 8.2.
- **Cost ceiling**: Indexes add < 5% to user-table storage; cache uses existing Redis budget.

---

## 21. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Index creation locks the users table | Low | High | `CREATE INDEX CONCURRENTLY`; tested in staging |
| Cache stampede on a popular query | Medium | Medium | Single-flight pattern at cache layer |
| Privacy approval delays Phase 0 | Medium | Medium | Engage privacy lead at PRD review; have fallback to no-query-logging variant |
| RBAC bypass via crafted cursor | Low | High | Cursor opaque + signed; auth re-checks on every page |

---

## 22. Dependencies

### 22.1 Internal

| Dependency | Owner | Status |
|---|---|---|
| Existing user service | Platform team | Ready |
| Existing API gateway | Platform team | Ready |
| Existing Redis instance | SRE | Ready |

### 22.2 External

None. No new vendor relationships.

---

## 23. Acceptance Criteria

The PRD is satisfied when **all** of the following are true:

- [ ] `GET /api/users/search` deployed to production behind a feature flag.
- [ ] Frontend `/users/search` page deployed and reachable from `/users`.
- [ ] All five filters working (name, email, role, status, created-at range).
- [ ] Cursor-based pagination working in both directions.
- [ ] p95 latency < 200ms confirmed in production.
- [ ] Cache hit rate > 40% in steady state.
- [ ] Audit log entries for every search.
- [ ] RBAC enforcement validated by integration tests + a manual cross-tenant test.
- [ ] Documentation (Section 12) updated.
- [ ] Rollback procedure tested in staging.
- [ ] Open questions (Section 4.3) resolved.
- [ ] Time-to-find metric measured at < 2s median.

---

## Appendix

### A. Glossary

| Term | Definition |
|---|---|
| Cursor-based pagination | Pagination using an opaque token from the previous page's last row, rather than offset/limit. Stable across inserts. |
| RBAC | Role-Based Access Control. Determines which users an actor can see based on the actor's role. |
| Stampede | Many concurrent requests hitting the database simultaneously when a cache entry expires. Mitigated by single-flight. |

### B. References

- [`../../specs/user-search/design.md`](../../specs/user-search/design.md) - full technical design.
- [`../../specs/user-search/requirements.md`](../../specs/user-search/requirements.md) - formal requirements with stable IDs.
- [`../../specs/user-search/tasks.md`](../../specs/user-search/tasks.md) - work plan with task numbers and back-references.
