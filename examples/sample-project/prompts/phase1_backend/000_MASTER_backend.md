# 000_MASTER_backend - Phase 1: Backend Implementation

> Phase entry-point. Read this before any task in Phase 1.

---

## Phase Summary

Phase 1 ships the API endpoint with full filter coverage, RBAC scoping, cursor pagination, cache layer, observability, and rate limiting. By the end of this phase, `GET /api/users/search` works in develop, integration tests cover every backend requirement, and synthetic load shows p95 < 200ms.

The phase opens with the index migration (task 4), continues with a fan-out of independent backend components (tasks 5–9, 11, 12), then converges on the endpoint composition (task 10).

## Goals

By the end of Phase 1:

1. `GET /api/users/search` deployed to develop behind a feature flag.
2. All five filters (name, email, role, status, created-at range) working.
3. Cursor pagination working both directions.
4. RBAC scoping enforced (admin sees full corpus; non-admin scoped to own organization).
5. Synthetic load p95 < 200ms.
6. Observability: metrics, logs, traces, audit log all emitting.
7. Rate limiting (100/min/actor) enforced at the gateway.

## Prerequisites

- [ ] Phase 0 acceptance met.
- [ ] Q1, Q2, Q3 resolved.
- [ ] `design.md` reflects Phase 0 decisions.
- [ ] CI runs against synthetic Postgres + Redis fixtures.

## Task Prompts

| # | Task | Primary Agent | Supporting Agents |
|---|---|---|---|
| 004 | [`004_index_migration.md`](004_index_migration.md) | `database-engineer` | `deployment-validator`, `unit-test-writer` |
| 005 | [`005_request_validator.md`](005_request_validator.md) | `backend-engineer` | `unit-test-writer` |
| 006 | [`006_rbac_scoping.md`](006_rbac_scoping.md) | `backend-engineer` | `security-auditor`, `unit-test-writer` |
| 007 | [`007_query_builder.md`](007_query_builder.md) | `backend-engineer` | `unit-test-writer` |
| 008 | [`008_cursor_encoding.md`](008_cursor_encoding.md) | `backend-engineer` | `security-auditor`, `unit-test-writer` |
| 009 | [`009_cache_layer.md`](009_cache_layer.md) | `backend-engineer` | `unit-test-writer` |
| 010 | [`010_wire_endpoint.md`](010_wire_endpoint.md) | `backend-engineer` | `integration-test-generator` |
| 011 | [`011_observability.md`](011_observability.md) | `backend-engineer` | `deployment-validator` |
| 012 | [`012_rate_limiting.md`](012_rate_limiting.md) | `backend-engineer` | `integration-test-generator` |

### Execution order

```
        004 (indexes)
              │
        ┌─────┴────────────────────────────┐
        ▼                                  │
    005, 006, 007, 008, 009    (parallel - independent components)
        │                                  │
        └──────────► 010 ◄─────────────────┘
                     │
                     ├── 011 (observability - wired via 010 decoration)
                     │
                     └── 012 (rate limiting - gateway-level, parallel with 010)
```

005–009 can run in any order or in parallel. 010 composes them. 011 wires observability into 010's components. 012 is gateway-level configuration that runs parallel to all of the above.

## Agent Assignments

- **`backend-engineer`** - owns the search module (validator, RBAC scoping, query builder, cursor encoding, cache layer, endpoint composition, rate limiting). 7 of 9 tasks.
- **`database-engineer`** - owns the index migration.
- **`security-auditor`** - reviews RBAC scoping, cursor signing, audit log content, rate limit config.
- **`unit-test-writer`** / **`integration-test-generator`** - embedded in implementation tasks.
- **`deployment-validator`** - validates the migration in staging; runs synthetic load test.

## Acceptance Criteria

Phase 1 is complete when **all** of the following are true:

- [ ] Tasks 004–012 merged.
- [ ] Endpoint serves in develop behind feature flag `users.search.enabled`.
- [ ] Integration tests cover every backend requirement (R1.1, R1.2, R1.3, R2.1, R3.1, R4.1, R4.2, R5.1, R5.2, R5.3) and the backend NFRs (NFR-1.1, NFR-2.1, NFR-2.2, NFR-2.3, NFR-2.4, NFR-3.1, NFR-3.2, NFR-3.3, NFR-3.4).
- [ ] Synthetic load (100 RPS, 60s) shows p95 < 200ms.
- [ ] Coverage table in [`../../specs/user-search/tasks.md`](../../specs/user-search/tasks.md) updated; backend rows fully populated.
- [ ] `/audit` returns clean.
- [ ] `security-auditor` signed off on tasks 6, 8, 11, 12.

## Risks Specific to Phase 1

| Risk | Mitigation |
|---|---|
| Index creation locks production-scale staging table | `CREATE INDEX CONCURRENTLY`; staging dry-run in task 4 |
| Cache stampede on a popular query | Single-flight pattern in task 9 |
| RBAC bypass via crafted cursor | HMAC signing + replay protection in task 8; `security-auditor` reviews task 8 |
| Rate limit too tight, blocks legitimate admin workflow | 100/min is generous for human admin patterns; revisit in task 18 if load test shows otherwise |

## How to Execute

1. Read [`../000_GLOBAL_MASTER.md`](../000_GLOBAL_MASTER.md).
2. Read this file end to end.
3. Confirm Phase 0 acceptance is met.
4. Run task 004 first.
5. Fan out tasks 005–009 (parallel where you have engineers; serial otherwise).
6. After 005–009 land, run task 010 to compose.
7. Wire 011 (observability) into 010's components.
8. Run task 012 (rate limiting) parallel to 010 - they don't conflict.
9. Validate against acceptance criteria.
10. Promote to Phase 2 ([`../phase2_frontend/000_MASTER_frontend.md`](../phase2_frontend/000_MASTER_frontend.md)).
