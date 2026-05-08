# Prompt: PRD → Spec Triplet

Convert an approved PRD into the canonical spec triplet (`requirements.md`, `design.md`, `tasks.md`) under `specs/examples/<feature>/`.

---

## Role

You are a **spec-author** working from an approved PRD. Your output is three files, with stable IDs and back-references between them.

## Inputs

- **PRD**: `<path/to/prd.md>` (Status: `Approved`)
- **Architecture reference**: `<path/to/architecture.md>` (or "TODO" if none)
- **Target directory**: `specs/examples/<slug>/`

If the PRD is not yet `Approved`, stop and report — drafting specs against a moving PRD wastes work.

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
- Mark open questions as `Q<N>` with owners.

### 2. `design.md`

- Use [`specs/templates/design-template.md`](../../specs/templates/design-template.md).
- Reference requirement IDs from `requirements.md` — do not restate them.
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
- Build the coverage table — every requirement and NFR must map to at least one task.
- Group tasks under `## Phase 1: <name>`, `## Phase 2: <name>`, etc.

## Quality bar

The triplet is complete when:

- Every PRD acceptance criterion is covered by at least one requirement.
- Every requirement has a stable ID.
- Every requirement is referenced by at least one task.
- Every task is referenced by at least one requirement.
- The design references requirement IDs in every component / API / sequence section.
- The coverage table in `tasks.md` is fully populated (no `TODO` rows).

## Constraints

- Do not invent requirements not in the PRD. If the PRD is silent, surface as an open question.
- Do not invent design choices not justified by requirements. The design serves the requirements.
- Generic content only — no proprietary domain logic, no real customer data, no internal endpoints.

## Final step

After producing the three files:

1. Validate cross-references manually (every `R<N.M>` in design and tasks resolves to a row in requirements).
2. Run `/audit` for sanitization and frontmatter checks.
3. Submit for review with `Status: Draft` on each file. Promote to `Approved` only after stakeholder sign-off.
