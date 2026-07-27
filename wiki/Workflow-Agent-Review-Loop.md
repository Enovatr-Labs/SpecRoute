# Workflow: Agent Review Loop

<!-- sources: workflows/agent-review-loop.md -->

How agent-assisted code review works in a SpecRoute-driven project. Pairs an agent's structured analysis with a human's judgment authority.

For the canonical version, see [`workflows/agent-review-loop.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/workflows/agent-review-loop.md).

## Why agent-assisted review

Code review has two distinct workloads:

1. **Mechanical** — walk the diff, check tests against requirements, scan for security patterns, verify frontmatter, check cross-references resolve.
2. **Judgmental** — assess whether the design choice is right, whether the abstraction will hold, whether the change matches team intent.

Agents are excellent at #1 and unreliable at #2. The pattern delegates #1 to agents and reserves #2 for humans.

## The loop

```
PR opened
   ↓
Author runs /audit pre-PR
   ↓
CI runs (tests, lint, security scan)
   ↓
Agent review pass
   ├── Read PR diff
   ├── Read linked task + requirements + design
   ├── Apply prompts/shared/code-review-prompt.md
   └── Output: structured review (Blockers / Concerns / Suggestions / What's good)
   ↓
Human reviewer reads agent review + diff
   ├── Approve  ───────→ Author squash-merges
   └── Request changes → Author addresses; loop
```

## Phases

### Phase 1: Author self-review
Before opening the PR:
1. Run `/audit` (sanitization + frontmatter + vendor matrix + broken links + TODO health).
2. Confirm every back-referenced requirement has a test.
3. Read the diff one more time as if you hadn't written it.

### Phase 2: CI
Standard CI: unit + integration tests, type checks, lint, security scans, dependency audits. Reviewers don't approve red builds.

### Phase 3: Agent review
The agent CLI runs the code-review prompt over the PR. Inputs:
- The PR diff.
- The linked task ID (from PR title or commit messages).
- The corresponding `tasks.md`, `requirements.md`, `design.md`.
- Relevant rules under `rules/`.

The prompt is [`prompts/shared/code-review-prompt.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/prompts/shared/code-review-prompt.md). Output structure:

```
## Summary
<1–2 sentence summary>

## Blockers (request changes)
- <issue: file, line, what's wrong, what to do>

## Concerns (discuss)
- <issue>

## Suggestions (nits)
- <issue>

## What's good
- <thing>
```

The agent posts this as a PR comment.

### Phase 4: Human review
A human reads the agent's review, the PR diff, and the linked spec for context. Then decides:

- **Approve** — agent found nothing material; human concurs.
- **Request changes** — agent's blockers are real, OR human sees something the agent missed.
- **Block** — structural problem (wrong design, wrong scope, wrong abstraction). Often surfaces only at human review.

The human is **not deferring to the agent**. The human reads the agent's findings as a comprehensive checklist and adds judgment on top.

### Phase 5: Address feedback
- For each blocker: fix and push a new commit.
- For concerns: respond inline (defend with rationale, or accept and change).
- For nits: usually fix.

Re-request review when ready. Agent re-runs against updated diff; human re-reads.

### Phase 6: Merge
PR approved + CI green → merge. Check the task box in `tasks.md`.

## What agents catch well

- Missing tests for back-referenced requirements.
- Frontmatter contract violations.
- Security patterns (SQL string concat, missing input validation, unquoted shell vars).
- Sanitization issues (private project names, secrets, absolute paths).
- Broken markdown links.
- Drift between design doc and implementation.
- Performance budgets exceeded.
- Out-of-scope changes.

## What humans must catch

- Whether the design choice is correct in context (vs. correct against `design.md`).
- Whether the abstraction will hold as the system grows.
- Whether the change matches unstated team intent.
- Whether the task as defined was the right task.
- Trade-offs not captured in the spec (cost, ergonomics, future flexibility).

The agent's review is a checklist, not a vote.

## Anti-patterns

- **Approving because the agent approved.** Read the diff yourself.
- **Bikeshedding with the agent.** Agents will debate style if invited. Don't invite.
- **Asking the agent to "fix it."** The author owns the PR; the reviewer requests changes.
- **Replacing reviewers entirely with agents.** Removes the judgment layer.
- **Skipping CI because the agent didn't flag anything.** CI catches different things (timing-dependent failures, integration-environment quirks).

## When to re-prompt the agent

If the agent's review is shallow or wrong:

- Update [`prompts/shared/code-review-prompt.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/prompts/shared/code-review-prompt.md) to be more specific.
- Add the agent's blind spot to its `.md` operating principles.
- Train the team on what the agent does and doesn't catch.

Agent review quality is a function of prompt quality + agent definition quality. Treat both as living artifacts.

## Vendor support

| Vendor | Agent review viability |
|---|---|
| Claude Code | Strong — sub-agents via `Task` tool; can dispatch a `code-reviewer` agent |
| Codex | Strong — skills can be invoked with `$name` or from the `/skills` menu |
| Gemini CLI | Strong — Agent Skills can expose a review workflow and subagents can perform the review |
| Cursor | Limited — rule-based, not workflow-based |
| Kiro | Strong — file-saved hook can trigger review on PR-relevant changes |
| Devin Desktop | Strong — Devin Local supports skills and subagents; Cascade users can invoke the review prompt manually |

For vendors with limited support, fall back to manual prompt invocation.

## See also

- [[Prompts]] — the code-review-prompt template
- [[Rules]] — `code-review-rules.md` documents the bar
- [[Workflow Spec to Implementation]] — the implementation loop the review caps
