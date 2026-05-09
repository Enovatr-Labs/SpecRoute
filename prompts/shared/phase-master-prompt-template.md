# 000_MASTER_<Phase Name> - Phase <N>: <Phase Title>

> Per-phase entry-point. Read this before any task in the phase.

---

## Phase Summary

<2–3 paragraphs explaining what this phase accomplishes and why it's grouped this way. Reference the global master at `000_GLOBAL_MASTER.md` for higher-level context.>

## Goals

By the end of this phase:

1. <Goal 1>
2. <Goal 2>
3. <Goal 3>

## Prerequisites

Before starting Phase <N>, confirm:

- [ ] Phase <N-1> acceptance criteria met (or this is Phase 0).
- [ ] PRD reviewed and approved.
- [ ] Architecture doc reviewed.
- [ ] <Phase-specific prerequisite>.
- [ ] <Phase-specific prerequisite>.

## Task Prompts

Tasks run in numbered order. Each task has its own prompt file with full context.

| # | Task | Primary Agent | Supporting Agents |
|---|---|---|---|
| 001 | `001_<task-name>.md` | `<agent>` | `<agent>` |
| 002 | `002_<task-name>.md` | `<agent>` | `<agent>` |
| 003 | `003_<task-name>.md` | `<agent>` | `<agent>` |
| 004 | `004_<task-name>.md` | `<agent>` | `<agent>` |
| ... | ... | ... | ... |

## Agent Assignments

Agents involved in this phase:

- **`<agent-1>`** - <responsibility in this phase>
- **`<agent-2>`** - <responsibility>
- **`<agent-3>`** - <responsibility>

Read each agent's `.md` file (under `.claude/agents/` or `agents/examples/`) for its operating principles before invoking it.

## Acceptance Criteria

Phase <N> is complete when **all** of the following are true:

- [ ] All numbered tasks (001 through N) merged.
- [ ] <Phase-specific acceptance criterion>.
- [ ] <Phase-specific acceptance criterion>.
- [ ] No regressions in <area>.
- [ ] Documentation updated for changes in this phase.
- [ ] `/audit` returns clean.

## Risks Specific to This Phase

| Risk | Mitigation |
|---|---|
| <risk 1> | <mitigation> |
| <risk 2> | <mitigation> |

## How to Execute

1. Read the global master (`000_GLOBAL_MASTER.md`).
2. Read this file end to end.
3. Confirm prerequisites are met.
4. Open `001_<task-name>.md` and follow it.
5. When task 001 is complete, advance to 002.
6. After every 2–3 tasks, run `/audit` to catch drift.
7. When all tasks are merged, validate against acceptance criteria.
8. Promote to Phase <N+1>.

---

## How to fill this template

1. **Phase numbering.** Phases are zero-indexed (Phase 0 is the foundation; Phase N is the last).
2. **Filename pattern.** This file is always `000_MASTER_<phase>.md` inside the phase directory `phase{N}_<name>/`. The `000_` prefix sorts it first.
3. **Task numbering.** Task prompts are `001_<name>.md`, `002_<name>.md`, … with leading zeros for sortable lexicographic order. Numbering is sticky - don't renumber to insert.
4. **Agent assignments are first-class.** Every task names a primary agent and (optionally) supporting agents. Without this, agent CLI selection is guesswork.
5. **Acceptance criteria are the gate.** Phase N+1 is blocked on Phase N's acceptance. Be specific - vague criteria don't gate.
6. **Risks specific to the phase.** General initiative risks live in the PRD; this section is for risks unique to this phase.
