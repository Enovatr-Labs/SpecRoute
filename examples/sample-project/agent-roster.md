# Agent Roster: User Search

**Project**: SpecRoute worked example
**Date**: 2026-05-08
**Total Agents**: 9

> Cross-vendor agent inventory for the user-search feature. Generic archetypes only; no domain-specific agents. Maps to the archetypes in [`agents/archetypes/`](../../agents/archetypes/).

---

## Department 1: Specification

| Agent | Archetype | Model | Color | Memory | Internet |
|---|---|---|---|---|---|
| `prd-author` | product-agent | opus | blue | project | No |
| `spec-author` | architect-agent | opus | cyan | project | No |

**Purpose:** Drafts the PRD and spec triplet. For this feature, drove `prds/active/user-search.md`, `specs/user-search/requirements.md`, `specs/user-search/design.md`, and `specs/user-search/tasks.md`.

## Department 2: Implementation

| Agent | Archetype | Model | Color | Memory | Internet |
|---|---|---|---|---|---|
| `backend-engineer` | backend-agent | opus | green | project | No |
| `frontend-engineer` | frontend-agent | opus | yellow | project | No |
| `database-engineer` | backend-agent | sonnet | orange | project | No |

**Purpose:** Implements the spec. Tasks 4–17 are split across these three by file ownership (backend module, frontend components, migration files).

## Department 3: Quality

| Agent | Archetype | Model | Color | Memory | Internet |
|---|---|---|---|---|---|
| `unit-test-writer` | qa-agent | sonnet | yellow | project | No |
| `integration-test-generator` | qa-agent | sonnet | red | project | No |
| `security-auditor` | security-agent | opus | red | user | No |

**Purpose:** Writes tests against requirement back-references; reviews PRs for security and correctness.

## Department 4: Operations

| Agent | Archetype | Model | Color | Memory | Internet |
|---|---|---|---|---|---|
| `deployment-validator` | devops-agent | sonnet | pink | project | No |

**Purpose:** Validates the index migration in staging; runs the load test; coordinates the 10/50/100 rollout.

## Task assignments

| Task | Primary Agent | Supporting Agents |
|---|---|---|
| 1. Spike: Cache TTL | `backend-engineer` | `deployment-validator` |
| 2. Spike: Cursor encoding | `backend-engineer` | `security-auditor` |
| 3. Privacy review | `security-auditor` | (privacy lead, human) |
| 4. Index migration | `database-engineer` | `deployment-validator` |
| 5. Request validator | `backend-engineer` | `unit-test-writer` |
| 6. RBAC scoping | `backend-engineer` | `security-auditor`, `unit-test-writer` |
| 7. Query builder | `backend-engineer` | `unit-test-writer` |
| 8. Cursor encode/decode | `backend-engineer` | `security-auditor`, `unit-test-writer` |
| 9. Redis cache layer | `backend-engineer` | `unit-test-writer` |
| 10. Wire endpoint | `backend-engineer` | `integration-test-generator` |
| 11. Observability | `backend-engineer` | `deployment-validator` |
| 12. Rate limiting | `backend-engineer` | `integration-test-generator` |
| 13. SearchInput component | `frontend-engineer` | `unit-test-writer` |
| 14. FilterChips component | `frontend-engineer` | `unit-test-writer` |
| 15. ResultTable component | `frontend-engineer` | `unit-test-writer` |
| 16. CursorPagination component | `frontend-engineer` | `unit-test-writer` |
| 17. Compose `/users/search` page | `frontend-engineer` | `integration-test-generator` |
| 18. Load test | `deployment-validator` | `backend-engineer` |
| 19. Feature flag | `backend-engineer` | `frontend-engineer` |
| 20. Production rollout | `deployment-validator` | `backend-engineer` |
| 21. Documentation | `prd-author` | (`spec-author` for design refs) |
| 22. Rollback drill | `deployment-validator` | `backend-engineer` |

## Coordination notes

- `backend-engineer` and `frontend-engineer` work disjoint code paths; tasks 4–12 vs 13–17 can run in parallel after Phase 0 closes.
- `security-auditor` reviews tasks 6, 8, 11, 12 specifically (RBAC, cursor signing, audit log content, rate limit config).
- `deployment-validator` is the gate for Phase 3 (tasks 18, 20, 22) and runs in parallel with documentation work (task 21).

## Frontmatter examples

Each agent above maps to a flat `<name>.md` file under `agents/examples/` (consumer template) and `runtimes/.claude/agents/` / `runtimes/.codex/agents/` (runtime). Example shape (see [`agents/agent-template.md`](../../agents/agent-template.md)):

```yaml
---
name: backend-engineer
description: General-purpose backend implementer. Owns API handlers, query builders, cache logic, observability instrumentation. Triggers - "implement task #N", "wire the search endpoint", "add the validator".
model: opus
color: green
memory: project
internet: No
---
```
