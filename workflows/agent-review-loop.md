# Workflow: Agent Review Loop

How agent-assisted code review works in a SpecForge-driven project. Pairs an agent's structured analysis with a human's judgment authority.

## Why agent-assisted review

Code review has two distinct workloads:

1. **Mechanical**: walk the diff, check tests against requirements, scan for security patterns, verify frontmatter, check cross-references resolve.
2. **Judgmental**: assess whether the design choice is right, whether the abstraction will hold, whether the change matches the team's intent.

Agents are excellent at #1 and unreliable at #2. The agent-assisted review pattern delegates #1 to agents and reserves #2 for humans.

## The loop

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  PR opened                                                      │
│    │                                                            │
│    ▼                                                            │
│  Author runs /audit pre-PR                                      │
│    │                                                            │
│    ▼                                                            │
│  CI runs (tests, lint, security scan)                           │
│    │                                                            │
│    ▼                                                            │
│  ┌─ Agent review pass ──────────────────────────────────┐       │
│  │  - Read PR diff                                      │       │
│  │  - Read linked task + requirements + design          │       │
│  │  - Apply prompts/shared/code-review-prompt.md        │       │
│  │  - Output: structured review (blockers/concerns/...)  │       │
│  └──────────────────────────┬───────────────────────────┘       │
│                             │                                   │
│    ▼                                                            │
│  Human reviewer reads agent review + diff                       │
│    │                                                            │
│    ├─ Approve  ───────────────────► Author squash-merges        │
│    │                                                            │
│    └─ Request changes  ────────► Author addresses; loop         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Phase 1: Author self-review

Before opening the PR, the author:

1. Runs `/audit` (sanitization + frontmatter + vendor matrix + broken links + TODO health).
2. Confirms every back-referenced requirement has a test.
3. Reads the diff one more time as if they hadn't written it.

This phase catches the cheap errors before they reach reviewers.

## Phase 2: CI

Standard CI: unit tests, integration tests, type checks, lint, security scans, dependency audits. CI is non-negotiable; reviewers don't approve red builds.

## Phase 3: Agent review

The agent CLI runs the code-review prompt over the PR. Inputs:

- The PR diff.
- The linked task ID (from PR title or commit messages).
- The corresponding `tasks.md`, `requirements.md`, `design.md`.
- Relevant rules under `rules/`.

The prompt is [`prompts/shared/code-review-prompt.md`](../prompts/shared/code-review-prompt.md). Output structure:

```
## Summary
<1–2 sentence summary of overall posture>

## Blockers (request changes)
- <issue 1: file, line, what's wrong, what to do>

## Concerns (discuss)
- <issue 1>

## Suggestions (nits)
- <issue 1>

## What's good
- <thing 1>
```

The agent posts this as a PR comment.

## Phase 4: Human review

A human reviewer reads:

1. The agent's review.
2. The PR diff.
3. The linked spec for context.

Then decides:

- **Approve**: agent found nothing material; human concurs.
- **Request changes**: agent's blockers are real, OR the human sees something the agent missed.
- **Block**: structural problem — wrong design choice, wrong scope, wrong abstraction. Often surfaces only at human review.

The human is not deferring to the agent. The human reads the agent's findings as a comprehensive checklist and adds judgment on top.

## Phase 5: Address feedback

The author addresses requested changes:

- For each blocker: fix and push a new commit.
- For concerns: respond inline (defend the choice with rationale, or accept and change).
- For nits: usually fix.

When the author thinks the PR is ready again, re-request review. The agent re-runs against the updated diff; the human re-reads.

## Phase 6: Merge

When the PR is approved and CI is green: merge. Check the task box in `tasks.md`.

## What the agent catches well

Agents reliably catch:

- Missing tests for back-referenced requirements.
- Frontmatter contract violations.
- Security patterns (SQL string concatenation, missing input validation, unquoted shell variables).
- Sanitization issues (private project names, secrets, absolute paths).
- Broken markdown links.
- Drift between design doc and implementation.
- Performance budgets exceeded.
- Out-of-scope changes.

## What humans must catch

Agents are unreliable at:

- Whether the design choice is correct in context (vs. correct against `design.md`).
- Whether the abstraction will hold as the system grows.
- Whether the change matches unstated team intent.
- Whether the task as defined was the right task.
- Trade-offs that aren't captured in the spec (cost, ergonomics, future flexibility).

For these, defer to the human reviewer. The agent's review is a checklist, not a vote.

## Anti-patterns

- **Approving because the agent approved.** The agent is a co-pilot, not a sign-off. Read the diff yourself.
- **Bikeshedding with the agent.** Agents will engage in long debates about style if invited. Don't invite.
- **Asking the agent to "fix it."** The author owns the PR. The reviewer requests changes; the author decides how to address.
- **Replacing reviewers entirely with agents.** Removes the judgment layer the loop was designed around.
- **Skipping CI because the agent didn't flag anything.** CI catches different things than agent review (timing-dependent failures, integration-environment quirks). Both gate.

## When to re-prompt the agent

If the agent's review is shallow or wrong:

- Update [`prompts/shared/code-review-prompt.md`](../prompts/shared/code-review-prompt.md) to be more specific.
- Add the agent's blind spot to the agent's `.md` operating principles.
- Train the team on what the agent does and doesn't catch.

Agent review quality is a function of prompt quality + agent definition quality. Treat both as living artifacts.

## Vendor support

| Vendor | Agent review viability |
|---|---|
| Claude Code | Strong — sub-agents via `Task` tool; can dispatch a code-reviewer agent |
| Codex | Strong — skills with `user-invocable: true` work as review entry points |
| Gemini CLI | Limited — no skill primitive; review prompts pasted directly |
| Cursor | Limited — rule-based, not workflow-based |
| Kiro | Strong — file-saved hook can trigger review on PR-relevant changes |
| Windsurf | Limited |

For vendors with limited agent-review support, fall back to manual prompt invocation: paste the code-review-prompt + diff into a conversation.

## Authoring agent

The agent that performs the review is project-specific (e.g. `code-reviewer`, `security-auditor`, `template-quality-reviewer`). The pattern itself is owned by `framework-docs-author`.

## See also

- [`prompts/shared/code-review-prompt.md`](../prompts/shared/code-review-prompt.md) — the actual prompt.
- [`rules/code-review-rules.md`](../rules/code-review-rules.md) — the rules the review applies.
- [`spec-to-implementation.md`](spec-to-implementation.md) — the implementation loop the review caps.
