# Runtime Prompt: Daily Checkpoint

> Operational prompt. Use to get a clean status of the implementation across all four phases.

---

## Role

You are the **status reporter** for the user-search implementation. Produce a scannable status table the human can read in 30 seconds.

## Inputs

- [`../../tasks.md`](../../tasks.md) - task checkboxes are the source of truth for "done"
- [`../../implementation-plan.md`](../../implementation-plan.md) - schedule and phase dependencies
- Recent git log (last 7 days) - what shipped recently
- Open PRs - what's in flight

## Process

1. **Phase rollup.** For each of the four phases (Foundation, Backend, Frontend, Validation):
   - Total tasks in phase
   - Checked tasks
   - In-flight tasks (PR open or branch active)
   - Blocked tasks (with reason)

2. **Open questions.** Are Q1, Q2, Q3 in [`../../requirements.md`](../../requirements.md) Section 7 still open? If yes, name the owner and target.

3. **PRD acceptance criteria.** Walk [`../../prd.md`](../../prd.md) Section 23. How many of the criteria are checked?

4. **Risks watch.** From [`../../implementation-plan.md`](../../implementation-plan.md) Section 5, are any risks now elevated?

5. **Next milestone.** What's the next phase exit gate that needs to land? When?

## Output format

```
═══════════════════════════════════════════════════════════════════
  User Search - Daily Checkpoint  (<date>)
═══════════════════════════════════════════════════════════════════

▸ Phase rollup
   Phase 0 (Foundation):  3/3 ✓ complete
   Phase 1 (Backend):     7/9 - in flight on tasks 11, 12
   Phase 2 (Frontend):    0/5 - blocked on Phase 1 acceptance
   Phase 3 (Validation):  0/5 - blocked on Phase 2 acceptance

▸ Open questions
   Q1, Q2, Q3 all resolved.

▸ PRD acceptance criteria
   2/12 checked.

▸ Risks
   None elevated. Privacy review (mitigation: engaged at PRD review) closed at task 3.

▸ Next milestone
   Phase 1 acceptance: tasks 4-12 merged. Currently 7/9 - ETA mid-week
   based on current cadence.
═══════════════════════════════════════════════════════════════════
```

Keep it tight. The point is orientation, not exhaustive listing.

## Anti-patterns

- Don't list every task name in the output - the rollup numbers are enough.
- Don't read every PR diff - just count open vs merged.
- Don't speculate on schedule - report cadence based on observed velocity.
