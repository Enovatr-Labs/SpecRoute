# 000_GLOBAL_MASTER - User Search

> Single entry-point. Read this before opening any phase or task prompt.

---

## Role

You are a **Senior Engineer** leading the user-search implementation. You drive every phase from index migration through production rollout, making implementation decisions, writing production code, and validating the result.

## Mission

Execute the 4-phase implementation plan to:

1. Cut admin time-to-find a user from ~30s to < 2s.
2. Add filter-by-role and filter-by-status to unblock the planned RBAC redesign.
3. Maintain p95 latency < 200ms for queries returning ≤ 50 results.
4. Stay within existing performance and reliability budgets.

## Source of Truth

| Document | Path | Purpose |
|---|---|---|
| **PRD** | [`../prd.md`](../prd.md) | 23-section requirements document |
| **Architecture** | [`../design.md`](../design.md) | Design, data model, API contracts |
| **Requirements** | [`../requirements.md`](../requirements.md) | Stable IDs (R*, NFR-*) |
| **Tasks** | [`../tasks.md`](../tasks.md) | Numbered work plan with back-references |
| **Agent Roster** | [`../agent-roster.md`](../agent-roster.md) | Agent assignments per task |
| **AGENTS.md** | [`../../../AGENTS.md`](../../../AGENTS.md) | Project context, conventions, vendor matrix |

**Read the PRD and design doc before starting any phase.**

## Architecture Summary

### Before (Current)

- No search capability. Admins find users by knowing the email or scrolling.
- 30s median time-to-find. Support tickets containing "can't find user X" tripled last quarter.
- Existing infrastructure: API gateway, user service, Postgres `users` table, Redis cache layer, session auth.

### After (Target)

- `GET /api/users/search` endpoint with five filters and cursor pagination.
- `< 2s` median time-to-find; `< 200ms` p95 latency.
- Four new Postgres indexes (forward-compatible migration).
- 60s Redis cache layer with single-flight stampede protection.
- Full observability (metrics, logs, traces); audit log per search.
- New frontend page `/users/search` with link from existing `/users`.

## Phase Order

| Phase | Goal | Tasks |
|---|---|---|
| Phase 0: Foundation | Resolve open questions; validate index plan | 1, 2, 3 |
| Phase 1: Backend | Index migration + endpoint + tests + observability | 4–12 |
| Phase 2: Frontend | Search page + filter wiring + E2E | 13–17 |
| Phase 3: Validation | Load test + feature flag + rollout + docs | 18–22 |

## Operating Principles

- **Read tasks.md first.** Each task names a primary agent, prerequisites, and back-referenced requirements.
- **Honor agent assignments.** See `agent-roster.md` for who runs each task.
- **Acceptance criteria are the gate.** Tasks aren't done until criteria are met.
- **Cross-reference everything.** Code references task numbers; PRs reference tasks; commit messages name the task.
- **Sanitize before committing.** Run the project's `/sanitize` (or equivalent) before each commit.

## What good looks like

- [ ] All 22 tasks complete.
- [ ] All requirements (R1.1–R5.3) have ≥ 1 passing test.
- [ ] All NFRs measured and within budget.
- [ ] PRD acceptance criteria (Section 23) all checked.
- [ ] Rollback procedure tested in staging.
- [ ] Documentation updated per PRD Section 12.
- [ ] Production traffic at 100% with stable metrics for 7 days.

## How to start

1. Read this file end to end.
2. Read [`../prd.md`](../prd.md) Sections 1–4 (executive summary through scope).
3. Read [`../design.md`](../design.md) Sections 1–3 (overview through data model).
4. Read [`../tasks.md`](../tasks.md) end to end.
5. Open the phase master for the current phase: start with [`phase0_foundation/000_MASTER_foundation.md`](phase0_foundation/000_MASTER_foundation.md).
6. Work tasks in number order within the phase. Run the phase's exit gate before advancing.
7. Don't skip Phase 0 - the spikes' decisions feed Phase 1.

---

## What's in this directory

```
prompts/
├── 000_GLOBAL_MASTER.md             this file (always read first)
├── README.md                        phase index
├── phase0_foundation/
│   ├── 000_MASTER_foundation.md     phase entry-point
│   ├── 001_cache_ttl_spike.md       task 1
│   ├── 002_cursor_encoding_spike.md task 2
│   └── 003_privacy_review.md        task 3
├── phase1_backend/
│   ├── 000_MASTER_backend.md        phase entry-point
│   ├── 004_index_migration.md       task 4
│   ├── 005_request_validator.md     task 5
│   ├── 006_rbac_scoping.md          task 6
│   ├── 007_query_builder.md         task 7
│   ├── 008_cursor_encoding.md       task 8
│   ├── 009_cache_layer.md           task 9
│   ├── 010_wire_endpoint.md         task 10
│   ├── 011_observability.md         task 11
│   └── 012_rate_limiting.md         task 12
├── phase2_frontend/
│   ├── 000_MASTER_frontend.md       phase entry-point
│   ├── 013_search_input.md          task 13
│   ├── 014_filter_chips.md          task 14
│   ├── 015_result_table.md          task 15
│   ├── 016_cursor_pagination.md     task 16
│   └── 017_compose_page.md          task 17
└── phase3_validation/
    ├── 000_MASTER_validation.md     phase entry-point
    ├── 018_load_test.md             task 18
    ├── 019_feature_flag.md          task 19
    ├── 020_production_rollout.md    task 20
    ├── 021_documentation.md         task 21
    └── 022_rollback_drill.md        task 22
```

**Filename convention:** Task prompts use the global task number from [`../tasks.md`](../tasks.md) (`004_*` implements task 4). Phase masters always start with `000_MASTER_<phase>` so they sort first within their phase directory. The global master is `000_GLOBAL_MASTER` so it sorts first overall.

This worked example exercises the production task-prompt template ([`../../../prompts/shared/task-prompt-template.md`](../../../prompts/shared/task-prompt-template.md)) across all 22 tasks. The detail level varies appropriately: spike prompts (Phase 0) are scoped to exploration; backend implementation prompts (Phase 1) are most detailed; frontend prompts (Phase 2) are component-scoped; validation prompts (Phase 3) are procedural.
