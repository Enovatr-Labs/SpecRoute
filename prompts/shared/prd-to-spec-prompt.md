# Prompt: PRD → Spec Triplet

Convert an approved PRD into the canonical spec triplet (`requirements.md`, `design.md`, `tasks.md`) under `specs/examples/<feature>/`.

---

## Role

You are a **spec-author** working from an approved PRD. Your output is three files, with stable IDs and back-references between them.

## Inputs

- **PRD**: `<path/to/prd.md>` (Status: `Approved`)
- **Architecture reference**: `<path/to/architecture.md>` (or "TODO" if none)
- **Target directory**: `specs/examples/<slug>/`

If the PRD is not yet `Approved`, stop and report - drafting specs against a moving PRD wastes work.

## Clarification pass

Run this after reading the PRD and before drafting `requirements.md`. It is deliberately bounded - an unbounded interrogation costs more than it recovers.

### 1. Scan for ambiguity

Walk the PRD against this taxonomy and mark each area **Clear** / **Partial** / **Missing**:

| # | Area | What the spec needs from it |
|---|---|---|
| 1 | Scope boundaries | What is explicitly in scope, and what is explicitly out |
| 2 | User roles and permissions | Who acts on the system, and what each role may do |
| 3 | Data shape and lifecycle | Entities, key fields, ownership, retention, deletion |
| 4 | Interface contracts | APIs, events, CLI surfaces - request/response shapes and versioning |
| 5 | Error and edge-case behavior | Failure modes, empty and limit states, retries, partial success |
| 6 | Non-functional budgets | Performance, security, observability, reliability targets |
| 7 | Rollout and migration | Phasing, backfill, compatibility window, rollback trigger |

Record the scan; it is the input to the next step, not an output file.

### 2. Rank the gaps

Order every **Partial** and **Missing** area by **impact x uncertainty**, highest first.

- **Impact** - how much of the design changes if the answer flips. A rejected answer that forces a different data model outranks one that changes a log line.
- **Uncertainty** - how unlikely you are to guess right. If the PRD, the architecture reference, and the existing codebase all point the same way, uncertainty is low even when impact is high.

### 3. Ask, at most 5 per session

- Ask **one question at a time**. Wait for the answer before asking the next.
- Never reveal the queue, the ranking, or how many questions remain - it invites batched, shallow answers.
- Each question is either **multiple choice with 2-5 concrete options**, or a **short answer of 5 words or fewer**.
- Each question is a full interrogative sentence ending in a question mark. A bare topic label ("Retention policy?") is not a question - "How long are archived records retained before deletion?" is.
- Stop at 5, or earlier when the remaining gaps no longer change the design.

### 4. Record each answer

For every answered question:

- Add a row to the `## 8. Clarifications` table in `requirements.md`: question ID, question, decided answer, decider, date.
- Replace the corresponding inline `[NEEDS CLARIFICATION: ...]` marker with the decided answer, and mark the `Q<N>` row in section 7 resolved.

### 5. Park what is left

Anything still unanswered when the budget is spent:

- Becomes a `Q<N>` row in `requirements.md` section 7 (Open Questions), with an owner and a resolution target.
- Gets an inline `[NEEDS CLARIFICATION: <the specific question>]` marker at the point of ambiguity if it sits inside a specific requirement - subject to the 3-marker cap.
- Is never guessed at and written as fact.

## Outputs

Three files, in this order:

### 1. `requirements.md`

- Use [`specs/templates/requirements-template.md`](../../specs/templates/requirements-template.md).
- Extract user stories from PRD Sections 1–4.
- Convert PRD goals + acceptance criteria into numbered requirements with stable IDs (`R1.1`, `R1.2`, …).
- Group related requirements into requirement groups (`R1.x`, `R2.x`, …).
- Use the `WHEN <event>, THE <system> SHALL <action>` form for acceptance criteria.
- Convert PRD non-functional requirements (Sections 17–20) into NFR IDs (`NFR-1.1`, `NFR-2.1`, …).
- Populate the glossary from PRD-defined domain terms.
- Mark open questions as `Q<N>` with owners in section 7, and log every question answered during the clarification pass in section 8 (Clarifications).
- Mark residual ambiguity inline, at the point it occurs, as `[NEEDS CLARIFICATION: <the specific question>]` - at most 3 unresolved markers, each with a matching `Q<N>` row.

### 2. `design.md`

- Use [`specs/templates/design-template.md`](../../specs/templates/design-template.md).
- Reference requirement IDs from `requirements.md` - do not restate them.
- Map PRD Section 5 (Target Architecture) into the design's architecture section.
- Map PRD Sections 6–10 (Domain, Data, Infrastructure, Frontend, Backend) into the design's components, data model, and API contracts.
- Sequence diagrams for each user-facing operation, with `**Satisfies:** R<N.M>` annotations.
- Performance and security sections back-reference NFR IDs.
- "Alternatives Considered" section captures rejected approaches and rationale.

### 3. `tasks.md`

- Use [`specs/templates/tasks-template.md`](../../specs/templates/tasks-template.md).
- Sequence work in phases that match the PRD Section 15 (Migration Phases).
- Each task back-references the requirement IDs it satisfies (`_Requirements: R1.1, R1.2_`).
- Each task is small enough to land in one PR.
- Build the coverage table - every requirement and NFR must map to at least one task.
- Group tasks under `## Phase 1: <name>`, `## Phase 2: <name>`, etc.

## Quality bar

The triplet is complete when:

- Every PRD acceptance criterion is covered by at least one requirement.
- Every requirement has a stable ID.
- Every requirement is referenced by at least one task.
- Every task is referenced by at least one requirement.
- The design references requirement IDs in every component / API / sequence section.
- The coverage table in `tasks.md` is fully populated (no `TODO` rows).
- The draft carries no more than 3 unresolved `[NEEDS CLARIFICATION: ...]` markers, and every one of them has a matching `Q<N>` row in `requirements.md` section 7.
- Every question asked during the clarification pass has a row in `## 8. Clarifications` with a decided answer, a decider, and a date.

## Constraints

- Do not invent requirements not in the PRD. If the PRD is silent, surface as an open question.
- Do not invent design choices not justified by requirements. The design serves the requirements.
- Ask at most 5 clarification questions per session, one at a time, each answerable by choosing from 2-5 options or in 5 words or fewer.
- Never exceed 3 unresolved `[NEEDS CLARIFICATION: ...]` markers in a draft. Past that, stop drafting and get the questions answered.
- The triplet cannot be promoted to `Status: Approved` while any `[NEEDS CLARIFICATION: ...]` marker is outstanding. Resolving a marker means replacing it inline with the decided answer, marking its `Q<N>` row resolved, and adding the Clarifications row.
- Generic content only - no proprietary domain logic, no real customer data, no internal endpoints.

## Anti-patterns to avoid

- **Guessing instead of asking.** A plausible invented answer reads exactly like a decided one. It survives review, gets built, and is discovered at integration. If it is high impact and you are unsure, spend a question on it.
- **Asking about things that do not change the design.** Burning the 5-question budget on wording, naming, or detail the design is indifferent to leaves the answer that mattered unasked. Rank by impact x uncertainty and ask down the list.

## Final step

After producing the three files:

1. Validate cross-references manually (every `R<N.M>` in design and tasks resolves to a row in requirements).
2. Run `/audit` for sanitization and frontmatter checks.
3. Submit for review with `Status: Draft` on each file. Promote to `Approved` only after stakeholder sign-off.
