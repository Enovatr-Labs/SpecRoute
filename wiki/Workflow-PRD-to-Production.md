# Workflow: PRD to Production

<!-- sources: workflows/prd-to-production.md -->

The outer engineering loop. Takes a feature from "idea worth doing" to "live in production with stable metrics." Composes every artifact SpecRoute produces.

For the canonical version, see [`workflows/prd-to-production.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/workflows/prd-to-production.md).

## The 13 stages

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

## Stage summaries

### 1. PRD draft
**Owner**: product / sponsor (with `prd-author` agent).
**Output**: `prds/active/<slug>.md` with `Status: Draft`.
**Exit**: every section has at least placeholder content; open questions listed; success metrics concrete.

### 2. PRD review
**Owner**: product owner + stakeholders (eng, ops, security, compliance).
**Exit**: open questions resolved or assigned owner + date; stakeholders sign off.

### 3. PRD approved
**Output**: `Status: Approved`. The PRD is now the contract.

### 4. Spec triplet draft
**Owner**: tech lead (with `spec-author` agent). Use [`prompts/shared/prd-to-spec-prompt.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/prompts/shared/prd-to-spec-prompt.md).
**Output**: `specs/<slug>/{requirements,design,tasks}.md` with stable IDs, back-refs, populated coverage table.
**Exit**: every PRD acceptance criterion maps to ≥1 requirement; every requirement maps to ≥1 task; coverage table has no `TODO` rows.

### 5. Spec review
**Owner**: tech lead, architect, security reviewer.
**Exit**: open design questions resolved; design doesn't introduce risks the PRD doesn't mention.

### 6. Spec approved
**Output**: each of `requirements.md`, `design.md`, `tasks.md` has `Status: Approved`.

### 7. Implementation tasks
**Owner**: tech lead (with `prompt-engineer` agent if many tasks).
**Output**: `agent-roster.md` + (for multi-week initiatives) `prompts/000_GLOBAL_MASTER.md` and numbered task prompts under `prompts/phase{N}_<name>/`; an `implementation-plan.md`.
**Exit**: every task in `tasks.md` has a primary agent assigned; implementation plan has a defensible schedule.

### 8. Implementation
**Owner**: each task's primary agent.
**Output**: code, tests, observability, doc updates. Each task back-references requirement IDs in commits and PRs.
**Exit**: each task's checkbox is checked; PR is open.

See [[Workflow Spec to Implementation]] for the inner loop.

### 9. PR review
**Owner**: code reviewer (human or `code-reviewer` agent).
**Use**: [`prompts/shared/code-review-prompt.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/prompts/shared/code-review-prompt.md).
**Exit**: approval; tests pass; `/audit` clean; sanitization gate doesn't fire.

See [[Workflow Agent Review Loop]].

### 10. Validation
**Owner**: QA / test engineer + `template-quality-reviewer` agent for cross-cutting checks.
**Output**: validation report. Every requirement has a passing test; every NFR is measured; performance budgets met.
**Exit**: validation report clean.

See [[Workflow Testing and Validation]].

### 11. Rollout
**Owner**: deployment / SRE.
**Output**: production deployment per the PRD's rollout strategy (typically feature flag → 10% → 50% → 100% with monitoring at each stage).
**Exit**: 100% traffic with stable error rates and latency for the duration specified in the PRD.

See [[Workflow Release Readiness]].

### 12. Production stable
**Owner**: deployment / SRE → product.
**Exit**: every PRD acceptance criterion checked; success metrics within target.

### 13. Closeout
**Owner**: PRD author.
**Output**: PRD `Shipped` + moved to `prds/archive/`; spec triplet `Complete`; lessons-learned doc; any deferred work surfaces as new PRDs.

## Skipping stages

For trivial work, some stages collapse:

- **Lightweight feature** — Stages 4–6 use [`feature-spec-template.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/specs/templates/feature-spec-template.md) instead of the spec triplet.
- **Refactor with no behavior change** — skip the PRD; use [`technical-spec-template.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/specs/templates/technical-spec-template.md) starting at Stage 4.
- **One architectural decision** — use the [ADR template](https://github.com/Enovatr-Labs/SpecRoute/blob/main/specs/templates/architecture-decision-record.md) only.

**Don't skip Stages 9 (review), 10 (validation), or 11 (rollout). Those are the gate.**

## Roles map

| Stage | Primary role | Agent (if delegating) |
|---|---|---|
| 1 — PRD draft | Product owner | `prd-author` |
| 2 — PRD review | Stakeholders | (review prompt) |
| 4 — Spec triplet | Tech lead | `spec-author` |
| 7 — Tasks + prompts | Tech lead | `prompt-engineer` |
| 8 — Implementation | Each task's owner | (per task assignment) |
| 9 — PR review | Reviewer | `code-reviewer` |
| 10 — Validation | QA | `template-quality-reviewer` |
| 11 — Rollout | SRE | `deployment-validator` |

## Worked example

The canonical example walks this entire workflow for the `user-search` feature. See [[Worked Example]].

## See also

- [[Workflow Spec to Implementation]] — Stages 7–9 in detail
- [[Workflow Agent Review Loop]] — Stage 9
- [[Workflow Testing and Validation]] — Stage 10
- [[Workflow Release Readiness]] — Stage 11
- [[Spec-Driven Development]] — the philosophy
