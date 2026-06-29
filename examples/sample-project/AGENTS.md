# AGENTS.md - User Search Sample Project

Canonical, vendor-neutral context file for this project. This is the single source of truth that any agent CLI working in the project should read first. Vendor-specific files ([`CLAUDE.md`](CLAUDE.md)) are slim delegation shims that point here.

## What this project is

A sample feature implementation: paginated, filterable, indexed user-directory search (`GET /api/users/search`). Generic domain - no proprietary business logic.

This project demonstrates the [SpecRoute](https://github.com/Enovatr-Labs/SpecRoute) framework's spec-driven flow concretely. Every artifact you'd produce in a real spec-driven implementation is here, plus the runtime layout (`.claude/`) that lets Claude Code pick up the work without additional setup.

## Spec-driven flow

```
prds/active/user-search.md           business intent (23 sections, "Approved")
└── specs/user-search/requirements.md   what must be true (R1.1, R1.2, ... NFR-1.1, ...)
    └── specs/user-search/design.md     how it's built (references R*)
        └── specs/user-search/tasks.md  22 numbered tasks, back-referencing requirements
            └── prompts/                the phased execution plan
                ├── 000_GLOBAL_MASTER.md
                ├── phase0_foundation/  spikes + privacy review
                ├── phase1_backend/     API endpoint, indexes, RBAC, cache, observability
                ├── phase2_frontend/    search page, filters, pagination
                ├── phase3_validation/  load test, rollout, rollback drill
                └── runtime/            operational (pickup-next-task, daily-checkpoint)
```

[`agent-roster.md`](agent-roster.md) names the agents (defined in [`.claude/agents/`](.claude/agents/)). [`implementation-plan.md`](implementation-plan.md) carries the operational view (schedule, critical path, risks).

## Project structure

```
sample-project/
├── README.md                drop-in instructions
├── AGENTS.md                this file (canonical context)
├── CLAUDE.md                Claude-specific delegation shim
├── prds/                    PRD lifecycle (active/deprecated/archive)
├── specs/                   spec triplets per feature
├── agentic-docs/            framework reference docs (copied from SpecRoute)
├── prompts/                 phased execution plan
├── agent-roster.md          per-task agent assignments
├── implementation-plan.md   operational view
├── .claude/                 Claude Code runtime (Markdown agents)
└── .codex/                  Codex runtime (TOML agents; second-vendor demonstration)
```

## Hard constraints

These are the rules that aren't obvious from the code and must be respected.

1. **Spec-driven order.** PRD -> spec triplet -> tasks -> implementation -> validation -> review. Don't jump straight to code.
2. **Stable IDs.** Every requirement has a stable ID (R1.1, NFR-1.1, ...). Tasks back-reference IDs (`_Requirements: R1.1, R1.2_`). IDs are immutable - removed requirements get marked deprecated.
3. **Sanitization.** Run `/sanitize` before commits. The PreToolUse hook (`.claude/hooks/pre-bash-sanitize.sh`) blocks `git commit` / `git push` if forbidden strings appear in tracked files. Treat hook blocks as hard stops.
4. **Frontmatter contracts.** Agents are flat `<name>.md` with `name`, `description`, `model`, `color`. Skills are folder-per-skill with `SKILL.md` and the full frontmatter contract. Missing required fields = the runtime won't register the artifact.
5. **Two-tier docs.** This file (AGENTS.md) stays short. Deep references live in [`agentic-docs/`](agentic-docs/). See [`agentic-docs/two-tier-docs-pattern.md`](agentic-docs/two-tier-docs-pattern.md).
6. **Generic domain content.** Sample / changelog / fixture content uses generic data ("Jane Example", "jane@example.com"). No real customer names or emails.

## Implementation team

8 agents under [`.claude/agents/`](.claude/agents/) drive the work. Each has trigger phrases that auto-select it; see [`.claude/agents/README.md`](.claude/agents/README.md) for the full roster.

| Agent | Owns |
|---|---|
| `prd-author` | PRD revisions; documentation per task 21 |
| `backend-engineer` | API handlers, validator, RBAC, query, cursor, cache, observability, rate limit |
| `frontend-engineer` | SearchInput, FilterChips, ResultTable, CursorPagination, page composition |
| `database-engineer` | Index migration, EXPLAIN ANALYZE validation |
| `security-auditor` | Privacy review, RBAC boundary, cursor signing, audit log content, rate limit |
| `unit-test-writer` | Tests against requirement IDs |
| `integration-test-generator` | Full request-lifecycle tests, cross-tenant probes, E2E |
| `deployment-validator` | Load test, gradual rollout, rollback drill, migration validation |

## Runtime conventions

- **Hooks** (`.claude/hooks/hooks.json`) - SessionStart status banner, PreToolUse sanitization gate, PostToolUse frontmatter check.
- **Slash commands** - `/sanitize`, `/audit`, `/status`, `/parity`.
- **Sanitization wordlist** - `.claude/.forbidden-strings.txt` (gitignored after rename from `.template.txt`).

## Vendor scope

This sample ships **two runtimes** over one shared spec layer: `.claude/` (Claude Code, Markdown agents) and `.codex/` (Codex, TOML agents). The `.codex/` variant is a worked demonstration of the mid-2026 vendor convergence - the same eight-agent team and MCP server set, expressed in Codex's native shape. The agents do not cross-sync (Markdown vs TOML); update both when an agent's substance changes. See [`.codex/README.md`](.codex/README.md).

To target Gemini / Kiro / Cursor / Windsurf, see the SpecRoute framework's [`runtimes/.<vendor>/`](https://github.com/Enovatr-Labs/SpecRoute/tree/main/runtimes) layouts and adapt the agents, hooks, and commands to that vendor's contract.

## How to start

If you've just copied this folder into a new repo, see [`README.md`](README.md) for the drop-in setup steps. If you're already set up:

1. Read this file end to end.
2. Read [`prompts/000_GLOBAL_MASTER.md`](prompts/000_GLOBAL_MASTER.md).
3. Read [`prds/active/user-search.md`](prds/active/user-search.md) (sections 1-4) and [`specs/user-search/design.md`](specs/user-search/design.md) (sections 1-3).
4. Read [`specs/user-search/tasks.md`](specs/user-search/tasks.md).
5. Open [`prompts/phase0_foundation/000_MASTER_foundation.md`](prompts/phase0_foundation/000_MASTER_foundation.md).
6. Execute task prompts in number order.

Or use the runtime prompt: [`prompts/runtime/pickup-next-task.md`](prompts/runtime/pickup-next-task.md) - it reads `tasks.md`, finds the next unblocked task, and routes to the right agent.
