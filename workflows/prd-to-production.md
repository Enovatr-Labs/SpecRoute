# Workflow: PRD to Production

End-to-end execution model. Takes a feature from "idea worth doing" to "live in production with stable metrics." Composes every artifact SpecForge produces.

## Stages

```
1. PRD draft       → 2. PRD review     → 3. PRD approved
                                              │
                                              ▼
4. Spec triplet draft → 5. Spec review → 6. Spec approved
                                              │
                                              ▼
7. Implementation tasks → 8. Implementation → 9. PR review
                                              │
                                              ▼
10. Validation     → 11. Rollout       → 12. Production stable → 13. Closeout
```

Each stage has an entry condition, an output, and an exit gate.

## Stage 1: PRD draft

**Entry**: an idea with named owner.

**Owner**: product / project sponsor (with `prd-author` agent).

**Output**: `prds/active/<slug>.md` with `Status: Draft`. Use [`prds/templates/prd-template.md`](../prds/templates/prd-template.md) for full PRDs or [`prds/templates/lightweight-prd-template.md`](../prds/templates/lightweight-prd-template.md) for small features.

**Exit gate**: every section has at least placeholder content; open questions are listed; success metrics are concrete.

## Stage 2: PRD review

**Entry**: PRD with `Status: Draft` ready for review.

**Owner**: product owner + adjacent stakeholders (engineering, ops, security, compliance).

**Output**: review comments resolved or escalated; open questions assigned owners and dates.

**Exit gate**: all open questions either resolved or have an owner and target date; stakeholders sign off.

## Stage 3: PRD approved

**Owner**: PRD author flips status.

**Output**: `Status: Approved`. The PRD is now the contract.

**Exit gate**: status changed; PRD merged to main if not already.

## Stage 4: Spec triplet draft

**Entry**: PRD with `Status: Approved`.

**Owner**: tech lead (with `spec-author` agent). Use [`prompts/shared/prd-to-spec-prompt.md`](../prompts/shared/prd-to-spec-prompt.md) as the conversion prompt.

**Output**: `specs/examples/<slug>/{requirements,design,tasks}.md` (or single-file [`feature-spec`](../specs/templates/feature-spec-template.md) for lightweight features). Stable IDs, back-references, populated coverage table.

**Exit gate**: every PRD acceptance criterion maps to ≥ 1 requirement; every requirement maps to ≥ 1 task; coverage table has no `TODO` rows.

## Stage 5: Spec review

**Entry**: spec triplet with `Status: Draft`.

**Owner**: tech lead, architect, security reviewer.

**Output**: review comments resolved; cross-references validated; alternatives-considered section captures rejected approaches.

**Exit gate**: open design questions resolved; design doesn't introduce risks the PRD doesn't mention; coverage table fully populated.

## Stage 6: Spec approved

**Owner**: spec author flips status.

**Output**: each of `requirements.md`, `design.md`, `tasks.md` has `Status: Approved`.

**Exit gate**: status changed.

## Stage 7: Implementation tasks

**Entry**: approved spec triplet.

**Owner**: tech lead (with `prompt-engineer` agent if many tasks). Optionally generate a phased master-prompt set per [`prompts/shared/global-master-prompt-template.md`](../prompts/shared/global-master-prompt-template.md).

**Output**: `agent-roster.md` (assignments); `prompts/000_GLOBAL_MASTER.md` and numbered task prompts under `prompts/phase{N}_<name>/` (for multi-week initiatives) using [`prompts/shared/task-prompt-template.md`](../prompts/shared/task-prompt-template.md); an `implementation-plan.md` for the operational view.

**Exit gate**: every task in `tasks.md` has a primary agent assigned; the implementation plan has a defensible schedule.

## Stage 8: Implementation

**Entry**: approved spec + assigned tasks + implementation plan.

**Owner**: each task's primary agent.

**Output**: code, tests, observability instrumentation, documentation updates. Each task back-references requirement IDs in commits and PRs.

**Exit gate**: each task's checkbox in `tasks.md` is checked; PR is open with a clear description.

See [`spec-to-implementation.md`](spec-to-implementation.md) for the inner loop of how a single task gets implemented.

## Stage 9: PR review

**Entry**: a PR linked to a numbered task.

**Owner**: code reviewer (human or `code-reviewer` agent). Use [`prompts/shared/code-review-prompt.md`](../prompts/shared/code-review-prompt.md).

**Output**: approval, change requests, or block.

**Exit gate**: approval; tests pass; `/audit` returns clean; sanitization gate doesn't fire.

See [`agent-review-loop.md`](agent-review-loop.md) for agent-assisted review patterns.

## Stage 10: Validation

**Entry**: all task PRs merged.

**Owner**: QA / test engineer + `template-quality-reviewer` agent for cross-cutting checks.

**Output**: validation report. Confirms every requirement has a passing test; every NFR is measured; performance budgets met.

**Exit gate**: validation report clean; no requirement uncovered; no NFR unmeasured.

See [`testing-and-validation.md`](testing-and-validation.md) for the validation playbook.

## Stage 11: Rollout

**Entry**: validation passed; staging deployment stable.

**Owner**: deployment / SRE.

**Output**: production deployment per the PRD's rollout strategy (typically: feature flag → 10% → 50% → 100% with monitoring at each stage).

**Exit gate**: 100% traffic with stable error rates and latency for the duration specified in the PRD.

See [`release-readiness.md`](release-readiness.md) for the readiness checklist.

## Stage 12: Production stable

**Entry**: 100% rollout completed; monitoring window elapsed.

**Owner**: deployment / SRE → product.

**Output**: confirmation that PRD acceptance criteria (Section 23) are met in production. Success metrics measured against targets.

**Exit gate**: every PRD acceptance criterion checked; success metrics within target.

## Stage 13: Closeout

**Entry**: production stable; metrics validated.

**Owner**: PRD author.

**Output**:

- PRD status flipped to `Shipped`; moved to `prds/archive/`.
- Spec triplet status `Complete`.
- Lessons-learned doc (the team's retrospective).
- Any deferred work surfaces as new PRDs.

**Exit gate**: PRD archived; lessons captured; outstanding follow-ups have owners.

## Skipping stages

For trivial work, some stages collapse:

- **Lightweight feature**: Stages 4–6 use [`feature-spec-template.md`](../specs/templates/feature-spec-template.md) instead of the spec triplet.
- **Refactor with no behavior change**: skip the PRD; use [`technical-spec-template.md`](../specs/templates/technical-spec-template.md) starting at Stage 4.
- **One architectural decision**: use the [ADR template](../specs/templates/architecture-decision-record.md) only.

But: don't skip Stages 9 (review), 10 (validation), and 11 (rollout). Those are the gate.

## Roles map

| Stage | Primary role | Agent (if delegating) |
|---|---|---|
| 1 - PRD draft | Product owner | `prd-author` |
| 2 - PRD review | Stakeholders | (review prompt) |
| 4 - Spec triplet | Tech lead | `spec-author` |
| 7 - Tasks + prompts | Tech lead | `prompt-engineer` |
| 8 - Implementation | Each task's owner | (per task assignment) |
| 9 - PR review | Reviewer | `code-reviewer` (with prompts/shared/code-review-prompt.md) |
| 10 - Validation | QA | `template-quality-reviewer` (for cross-cutting) |
| 11 - Rollout | SRE | `deployment-validator` |

## Worked example

[`examples/sample-feature/`](../examples/sample-feature/) walks this entire workflow for the `user-search` feature. Read it as the canonical demonstration.

## See also

- [`spec-to-implementation.md`](spec-to-implementation.md) - Stage 7–9 in detail.
- [`agent-review-loop.md`](agent-review-loop.md) - Stage 9.
- [`testing-and-validation.md`](testing-and-validation.md) - Stage 10.
- [`release-readiness.md`](release-readiness.md) - Stage 11.
- [`agentic-docs/spec-driven-development.md`](../agentic-docs/spec-driven-development.md) - the underlying philosophy.
