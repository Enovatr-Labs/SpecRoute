# 000_GLOBAL_MASTER — User Search

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
5. Open `001_index_migration.md` (Phase 1's first task) when Phase 0 is complete; until then, work Phase 0 tasks (1, 2, 3) which don't have prompts here — they're spike work, not implementation.
6. Execute tasks in order. Don't skip Phase 0.

---

## What's in this directory

| File | Purpose |
|---|---|
| `000_master.md` | This file. Always read first. |
| `001_index_migration.md` | Task 4: add user search indexes (Phase 1 entry point). |
| `002_implement_search_endpoint.md` | Task 10: wire the API endpoint (Phase 1 mid-point). |

**Note:** This worked example shows the *shape* of the phased prompt pattern with two illustrative task prompts. A real initiative would have one prompt file per task in `tasks.md`. The two shown here exercise the production task-prompt template ([`../../../prompts/shared/task-prompt-template.md`](../../../prompts/shared/task-prompt-template.md)) end to end.
