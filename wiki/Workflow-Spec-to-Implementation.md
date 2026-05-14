# Workflow: Spec to Implementation

<!-- sources: workflows/spec-to-implementation.md -->

The inner loop. How a single approved task becomes merged code. Runs once per task in `tasks.md`.

For the canonical version, see [`workflows/spec-to-implementation.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/workflows/spec-to-implementation.md).

## Entry conditions

Before starting a task:

- [ ] PRD has `Status: Approved`.
- [ ] Spec triplet has `Status: Approved`.
- [ ] The specific task in `tasks.md` is the next unblocked task in execution order.
- [ ] The task's prerequisites checklist is satisfied.
- [ ] The implementer has access to the relevant code paths.

If any entry condition is missing, surface it and stop. Don't proceed with partial state.

## Stages

### A. Read

Read in order:

1. The task in `tasks.md` — title, sub-steps, requirement back-references, prerequisites.
2. The corresponding task prompt under `<feature>/prompts/<NNN>_*.md` if one exists.
3. Each requirement back-referenced (`R<N.M>`, `NFR-<N.M>`) in `requirements.md`.
4. Design sections relevant to "Files to Modify" in `design.md`.
5. The agent's own `.md` file (operating principles, boundaries) if delegating.
6. Existing code in the "Files to Modify" paths.

**Non-negotiable.** Tasks fail when implementers skip context.

### B. Plan (in your head, not in another doc)

Write the change in your head before writing it in files:

- Smallest set of edits that satisfies the task?
- Existing utilities / types / patterns this composes with?
- Test plan — which requirements does each test cover?
- Rollback plan if the task ships and is found broken?

Don't produce a planning document. The exception: if the task itself produces a doc (an ADR, a runbook), that's the deliverable.

### C. Implement

Make the changes. Small commits if multi-step.

Discipline:

- **Stay in scope.** Don't refactor adjacent code unless the task authorizes it.
- **Match the design.** If the design doesn't fit reality, update `design.md` first, then implement.
- **Quote shell variables; avoid `eval`; validate at boundaries.** See [[Rules]].
- **Write tests as you go**, not after. Each back-referenced requirement needs at least one test.

### D. Test

For every back-referenced requirement:

- One or more tests assert the behavior described in the requirement's acceptance criteria.
- Tests are **real** — actual assertions, not `assert true` or logging-only.
- Mocks at external boundaries only. Don't mock the system under test.
- Deterministic — no real network, no real clock without injection.

For NFRs:

- **Performance NFRs** — a measurement (load test, benchmark).
- **Observability NFRs** — a test that asserts the metric / log / trace is emitted.
- **Security NFRs** — a negative test (tampered cursor → 400, cross-tenant access → forbidden).

Mutation check: temporarily break the implementation; the test should fail. Restore.

### E. Pre-PR validation

```bash
/audit                                   # comprehensive
/sanitize                                # quick string-level scan
git status --short                       # confirm only intended files staged
git diff --cached                        # final read-through
```

If `/audit` flags anything, fix it. Sanitization gate hooks block `git commit` if something's wrong — treat as a hard stop. See [[Sanitization]].

### F. PR open

Open the PR with:

- **Title**: `<type>: implement task #<N> - <task title>` (or `fix: <description>`).
- **Description**: links the task in `tasks.md`, summarizes the change in 2–3 sentences, calls out anything the reviewer needs to verify manually.
- **Labels**: project-specific; often `feature`, `task-<N>`, the module name.
- **Reviewers**: at least one human. For agent-assisted review, also tag the review agent.

### G. Address review

- For **blockers**: implement the fix. Push a new commit (don't amend — readers want to see what changed since their last review).
- For **concerns**: respond with rationale or change accordingly.
- For **nits**: usually fix; cheap.

Re-request review when ready.

### H. Merge

When approved:

- Confirm CI is green.
- Squash-merge if your project squashes; else merge with the PR's commits.
- Check the box for the task in `tasks.md`.
- Reference the merged commit in the PR.

### I. Post-merge

- **Observability tasks** — validate the metric / log / trace appears in the dev environment.
- **Data tasks** — validate the migration ran cleanly.
- **API tasks** — smoke-test the endpoint.

## Common failure modes

### "I read the task but the prerequisites weren't actually met"
Surface this before implementing. Going ahead with broken prerequisites either produces partial work or implements assumptions that don't hold.

### "The design doesn't actually fit the constraint I'm hitting"
Update `design.md` first. Then return to implementation. Bypassing produces drift between design and code.

### "The test is hard to write — I'll add it next sprint"
The test isn't an after-hours task. If the test is hard, the implementation is probably wrong (boundaries unclear, dependencies excessive). Refactor toward testability.

### "The PR is too big to review"
The task was too big. Reviewers can't catch issues in 1,000-line PRs. Split: land smaller PRs that reference the same task.

### "The reviewer asked for a refactor that's out of scope"
Scope discipline cuts both ways. If the refactor is genuinely out of scope, decline politely with a pointer to a follow-up task. If the reviewer is right that the work won't land cleanly without the refactor, expand the task in `tasks.md` (or split off a precursor task).

## See also

- [[Workflow PRD to Production]] — the outer workflow
- [[Workflow Agent Review Loop]] — Stage G in detail
- [[Workflow Testing and Validation]] — Stage D in depth
- [[Prompts]] — the task-prompt template that drives Stage A
