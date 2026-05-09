# Workflow: Spec to Implementation

The inner loop of how a single approved task becomes merged code. Runs once per task in `tasks.md`.

## Entry conditions

Before starting a task:

- [ ] PRD has `Status: Approved`.
- [ ] Spec triplet has `Status: Approved`.
- [ ] The specific task in `tasks.md` is the next unblocked task in execution order.
- [ ] The task's prerequisites checklist is satisfied.
- [ ] The implementer has access to the relevant code paths.

If any entry condition is missing, surface it and stop. Don't proceed with partial state.

## Stage A: Read

Read these in order:

1. The task in `tasks.md` - title, sub-steps, requirement back-references, prerequisites.
2. The corresponding task prompt under `<feature>/prompts/<NNN>_*.md` if one exists.
3. Each requirement back-referenced (`R<N.M>`, `NFR-<N.M>`) in `requirements.md`.
4. Design sections relevant to the task's "Files to Modify" in `design.md`.
5. The agent's own `.md` file (operating principles, "Don't use for" boundaries) if delegating.
6. Existing code in the "Files to Modify" paths.

This stage is non-negotiable. Tasks fail when implementers skip context.

## Stage B: Plan (in code, not in another doc)

Write the change in your head before writing it in files:

- What's the smallest set of edits that satisfies the task?
- Which existing utilities, types, or patterns does this work compose with?
- What's the test plan - which requirements does each test cover?
- What's the rollback plan if the task ships and is found broken?

Don't produce a planning document. Internal thinking, not external artifact. The exception: if the task itself produces a doc (an ADR, a runbook), that's the deliverable.

## Stage C: Implement

Make the changes. In small commits if the task is multi-step.

Discipline:

- **Stay in scope.** Don't refactor adjacent code unless the task authorizes it. "While I'm here" cleanup is a separate task.
- **Match the design.** If you find the design doesn't fit reality, update `design.md` first; then implement.
- **Quote shell variables.** Avoid `eval`. Validate at boundaries. (See [`rules/engineering-rules.md`](../rules/engineering-rules.md).)
- **Write tests as you go**, not after. Each requirement back-referenced needs at least one test.

## Stage D: Test

For every back-referenced requirement:

- One or more tests assert the behavior described in the requirement's acceptance criteria.
- Tests are real - actual assertions, not `assert true` or logging-only.
- Mocks at external boundaries only. Don't mock the system under test.
- Deterministic - no real network, no real clock without injection.

For NFRs back-referenced:

- Performance NFRs: a measurement (load test, benchmark).
- Observability NFRs: a test that asserts the metric / log / trace is emitted.
- Security NFRs: a negative test (e.g. tampered cursor → 400, cross-tenant access → forbidden).

Run tests locally. They pass. The mutation check: temporarily break the implementation; the test should fail. Restore.

## Stage E: Pre-PR validation

Before opening the PR:

```bash
/audit                                   # comprehensive: sanitization + frontmatter + matrix + links
/sanitize                                # quick string-level scan
git status --short                       # confirm only intended files staged
git diff --cached                        # final read-through
```

If `/audit` flags anything, fix it. Sanitization gate hooks will block `git commit` if something's wrong; treat that as a hard stop.

## Stage F: PR open

Open the PR with:

- **Title**: `<type>: implement task #<N> - <task title>` (or for fixes: `fix: <description>`).
- **Description**: links the task in `tasks.md`, summarizes the change in 2–3 sentences, calls out anything the reviewer needs to verify manually.
- **Labels** (project-specific): often `feature`, `task-<N>`, the relevant module name.
- **Reviewers**: at least one human. For agent-assisted review, also tag the review agent.

## Stage G: Address review

When the reviewer requests changes:

- Read every comment.
- For blockers: implement the fix. Push a new commit (don't amend the original - readers want to see what changed since their last review).
- For concerns: respond with rationale or change accordingly. Reviewer's call which.
- For nits: usually fix; cheap.

Re-request review when ready.

## Stage H: Merge

When the PR is approved:

- Confirm CI is green.
- Squash-merge if your project squashes; else merge with the PR's commits.
- Check the box for the task in `tasks.md`.
- Reference the merged commit in the PR (helps trace through git history later).

## Stage I: Post-merge

After merge:

- If the task is observability-related, validate the metric / log / trace is appearing in the dev environment.
- If the task is data-related, validate the migration ran cleanly.
- If the task is API-related, smoke-test the endpoint manually.

## Common failure modes

### "I read the task but the prerequisites weren't actually met"

Surface this before implementing. Going ahead with broken prerequisites either produces partial work or implements assumptions that don't hold.

### "The design doesn't actually fit the constraint I'm hitting"

Update `design.md` first. Then return to implementation. Bypassing this produces drift between design and code.

### "The test is hard to write - I'll add it next sprint"

The test isn't an after-hours task. If the test is hard, the implementation is probably wrong (e.g. boundaries are unclear, dependencies are excessive). Refactor toward testability.

### "The PR is too big to review"

The task was too big. Reviewers can't catch issues in 1,000-line PRs. Split: land smaller PRs that reference the same task.

### "The reviewer asked for a refactor that's out of scope"

Scope discipline cuts both ways. If the refactor is genuinely out of scope, decline politely with a pointer to a follow-up task. If the reviewer is right that the work won't land cleanly without the refactor, expand the task in `tasks.md` (or split off a precursor task).

## Loop until done

Stages A–I run once per task. The PRD-to-production workflow ([`prd-to-production.md`](prd-to-production.md)) wraps this inner loop.

## See also

- [`prd-to-production.md`](prd-to-production.md) - the outer workflow.
- [`agent-review-loop.md`](agent-review-loop.md) - Stage G in detail.
- [`testing-and-validation.md`](testing-and-validation.md) - Stage D in depth.
- [`prompts/shared/task-prompt-template.md`](../prompts/shared/task-prompt-template.md) - the prompt shape that drives Stage A.
