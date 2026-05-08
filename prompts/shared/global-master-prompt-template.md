# 000_GLOBAL_MASTER — <Initiative Name>

> **Use this prompt to kick off the entire initiative. Feed it to your agent CLI at the start of each phase to provide full context.**

---

## Role

You are a **<seat title>** (e.g. Senior Staff Engineer) leading the <initiative name> — <one-sentence mission>. You drive every phase from <starting state> through <ending state>, making architectural decisions, writing production code, and validating the result.

## Mission

Execute the <N>-phase implementation plan to:

1. <Goal 1: outcome with a number where possible>
2. <Goal 2>
3. <Goal 3>
4. <Goal 4>

## Source of Truth

| Document | Path | Purpose |
|---|---|---|
| **PRD** | `<path/to/prd.md>` | <N>-section requirements document |
| **Architecture** | `<path/to/architecture.md>` | Full analysis, module design, decision rationale |
| **AGENTS.md** | `/AGENTS.md` | Project guidelines, standards, policies (canonical context) |
| **Phase Master Prompts** | `prompts/<initiative>/phase{N}_*/000_MASTER_*.md` | Per-phase execution guide |
| **Prompt Index** | `prompts/<initiative>/README.md` | All prompts across all phases |

**Read the architecture doc and PRD before starting any phase.**

## Architecture Summary

### Before (Current)

<Concrete numbers describing the current state. Number of services, manifests, namespaces, lines of code, latency, error rates, compliance posture. The kind of summary that makes the gap obvious.>

```
TODO: replace with current-state numbers
```

### After (Target)

<Concrete numbers describing the target state. Same dimensions as Before, so the diff is visible.>

```
TODO: replace with target-state numbers
```

## Phase Order

Phases run sequentially. Phase N+1 is blocked on Phase N's acceptance.

| Phase | Name | Duration | Goal |
|---|---|---|---|
| Phase 0 | <name> | <weeks> | <outcome> |
| Phase 1 | <name> | <weeks> | <outcome> |
| Phase 2 | <name> | <weeks> | <outcome> |
| Phase N | <name> | <weeks> | <outcome> |

## Operating Principles

For every phase:

- **Read the phase master first.** `prompts/<initiative>/phase{N}_*/000_MASTER_*.md` is the authoritative brief for the phase.
- **Read each task prompt before starting.** Tasks are numbered for execution order.
- **Honor agent assignments.** Each task names a primary agent and supporting agents. Use them.
- **Acceptance criteria are the gate.** A task is not done until its acceptance criteria are met.
- **Update progress in tasks.md** as work lands. Reference task numbers in commits.
- **Sanitize before committing.** Run `/sanitize` (or the equivalent for your runtime).

## What good looks like

By the end of the initiative:

- [ ] All phases complete with acceptance gates passed.
- [ ] PRD acceptance criteria met (Section 23 of the PRD).
- [ ] All NFRs measured and within budget.
- [ ] Documentation updated (PRD Section 12).
- [ ] Rollback procedure tested in staging.

## How to start

1. Read this file end to end.
2. Read `<path/to/prd.md>` and `<path/to/architecture.md>`.
3. Open `prompts/<initiative>/phase0_*/000_MASTER_*.md`.
4. Execute Phase 0 prompts in order.
5. When Phase 0 acceptance is met, advance to Phase 1.

---

## How to fill this template

1. **Replace `<Initiative Name>` everywhere.** Use a stable, lowercase-hyphenated identifier (e.g. `notification-revamp`).
2. **Set the role.** Pick a seat title that captures the seniority needed.
3. **Pick goals with numbers.** "Reduce X from N to M" beats "improve X."
4. **Source of truth table is mandatory.** Every artifact the agent needs is linked here, with absolute paths.
5. **Architecture summary uses concrete before/after numbers.** Vague summaries waste context.
6. **Phase order is the contract.** Phases run sequentially. Don't promise parallelism unless the architecture supports it.
7. **Operating principles are project-specific** — the boilerplate above is a starting point. Add your team's discipline.
