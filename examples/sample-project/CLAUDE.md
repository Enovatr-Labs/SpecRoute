# CLAUDE.md - User Search Sample Project

Claude Code project context. **This is a self-contained worked example** — copy this folder to a new repository and Claude Code can drive the implementation end to end.

## What this project is

A sample feature implementation: paginated, filterable, indexed user-directory search (`GET /api/users/search`). Generic domain, no proprietary business logic.

The point of this sample is to demonstrate the **SpecForge** framework's spec-driven flow concretely — every artifact you'd produce in a real spec-driven implementation is here, plus the runtime layout (`.claude/`) that lets Claude Code pick up the work without additional setup.

## Spec-driven flow

```
prd.md                           business intent (23 sections, "Approved")
└── requirements.md              what must be true (R1.1, R1.2, ... NFR-1.1, ...)
    └── design.md                how it's built (references R*)
        └── tasks.md             22 numbered tasks, back-referencing requirements
            └── prompts/         the phased execution plan
                ├── 000_GLOBAL_MASTER.md
                ├── phase0_foundation/    spikes + privacy review
                ├── phase1_backend/       API endpoint, indexes, RBAC, cache, observability
                ├── phase2_frontend/      search page, filters, pagination
                └── phase3_validation/    load test, rollout, rollback drill
```

`agent-roster.md` names the agents (defined in `.claude/agents/`). `implementation-plan.md` carries the operational view (schedule, critical path, risks).

## Implementation team (`.claude/agents/`)

8 agents drive the work. Each has trigger phrases that auto-select it:

| Agent | Owns |
|---|---|
| `prd-author` | The PRD; documentation per task 21 |
| `backend-engineer` | API handlers, validator, RBAC, query builder, cursor, cache, observability, rate limiting |
| `frontend-engineer` | SearchInput, FilterChips, ResultTable, CursorPagination, page composition |
| `database-engineer` | Index migration, EXPLAIN ANALYZE validation |
| `security-auditor` | Privacy review, RBAC boundary, cursor signing, audit log content, rate limit policy |
| `unit-test-writer` | Tests against requirement IDs - validator rules, RBAC matrix, cursor round-trips |
| `integration-test-generator` | Full request-lifecycle tests, cross-tenant probes, E2E |
| `deployment-validator` | Load test, gradual rollout, rollback drill, migration validation in staging |

## Runtime conventions

- **Hooks** (`.claude/hooks/hooks.json`) - SessionStart status banner, PreToolUse sanitization gate (blocks `git commit`/`git push` if `.claude/.forbidden-strings.txt` matches in tracked files), PostToolUse frontmatter validation.
- **Slash commands** - `/sanitize`, `/audit`, `/status`, `/parity`.
- **Sanitization wordlist** - `.claude/.forbidden-strings.txt` (gitignored after rename from `.template.txt`). Treat hook blocks as hard stops.

## How to start

If you've just copied this folder into a new repo, see [`README.md`](README.md) for the drop-in setup steps. If you're already set up:

1. Read `prompts/000_GLOBAL_MASTER.md` end to end.
2. Open the relevant phase master under `prompts/phase{N}_<phase>/000_MASTER_<phase>.md`.
3. Execute task prompts in number order.
4. Use `prompts/runtime/` for operational moves (pick up next task, daily checkpoint).

## Vendor scope

This sample is **Claude-Code-only**. To target Codex / Gemini / Kiro / Cursor / Windsurf, see the SpecForge framework's `runtimes/.<vendor>/` layouts and adapt the agents, hooks, and commands to that vendor's contract.
