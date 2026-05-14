# Code Review Rules

How to review a PR (human or agent-authored) against SpecRoute standards. Reuses [`prompts/shared/code-review-prompt.md`](../prompts/shared/code-review-prompt.md) as the operational prompt.

## What every review checks

1. **Task linkage.** PR title or commits reference a task ID (`#N`) from `tasks.md`. If not, ask "what task is this?" before deeper review.

2. **Requirement coverage.** Every requirement back-referenced by the linked task has at least one passing test. Missing tests for a back-referenced requirement is a blocker.

3. **Scope.** Diff matches the task description. Adjacent "while I'm here" cleanups belong in separate PRs.

4. **Correctness.** Code implements what `design.md` specifies. Boundaries respect the component map.

5. **Security.** Per [`security-rules.md`](security-rules.md). Input validation, output encoding, secret handling, auth posture.

6. **Performance.** Per the design's performance section and `engineering-rules.md` rule 9. Regressions block merge.

7. **Tests.** Real assertions, deterministic, no over-mocking. See `engineering-rules.md` rule 14.

8. **Observability.** New code paths emit the metrics/logs/traces the spec requires.

9. **Docs.** PRD Section 12 documentation updates landed (or are explicitly out of scope).

10. **Sanitization.** Run `/sanitize` (or equivalent) - no forbidden strings in tracked content.

## Review structure

Output as a punch list:

```
## Summary
<approve / request changes / block - one sentence>

## Blockers
- <file:line> <issue> <fix>

## Concerns
- <issue, optional>

## Suggestions (nits)
- <issue, optional>

## What's good
- <positive callout>
```

Be specific. "Section 5 is unclear" is not actionable; "function `foo` does X but variable `bar` implies Y - rename or split" is.

## Approval bar

- [ ] Linked task acceptance criteria met.
- [ ] All back-referenced requirements have passing tests.
- [ ] No security findings.
- [ ] No performance regressions.
- [ ] Docs updated.
- [ ] `/audit` returns clean.
- [ ] PR description quality bar met.

If any blocker remains, request changes. Do not approve "with caveats."

## What's *not* the reviewer's job

- **Re-running the design discussion.** That happened at design approval.
- **Bikeshedding style.** Style nits are suggestions, not blockers.
- **Adding scope.** "While you're at it, fix this other thing too" is a separate task.
- **Approving without checking tests.** Tests are the contract; verify them.

## Agent-assisted review

The `code-review-prompt.md` under `prompts/shared/` is a reusable prompt for agent-driven review. Workflow:

1. Open the PR.
2. Run the prompt with the PR diff and the linked task as inputs.
3. The agent produces a structured review.
4. A human reviewer consumes the review, decides on blockers vs concerns, and posts.

The agent does the heavy lifting (reading the diff, the spec, the rules); the human keeps judgment authority.

## Anti-patterns

- **Approving a PR with unresolved comments.** If you have a blocker, request changes.
- **Re-reviewing the same PR forever.** Two rounds of changes; if a third is needed, escalate.
- **Reviewing without the spec triplet open.** You can't tell if the PR is in-scope.
- **Letting CI replace human review.** CI catches the easy stuff; reviewers catch architecture, security, and intent.
