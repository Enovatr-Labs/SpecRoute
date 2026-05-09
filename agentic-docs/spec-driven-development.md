# Spec-Driven Development

The core flow SpecForge formalizes:

```
PRD → Spec (requirements + design + tasks) → Implementation → Validation → Review
```

Each stage produces a reviewable artifact. Each stage has a template, an agent assignment, and an acceptance criterion. The point is not ceremony - it's making agent-assisted work auditable.

## Why this order

| Stage | Question it answers | Cheap to change? |
|---|---|---|
| **PRD** | What product problem are we solving? Who for? What's success? | Yes - it's text. |
| **Requirements** | What must be true for the system to count as solving it? | Yes - text with stable IDs. |
| **Design** | How will the architecture, data, and interfaces meet the requirements? | Mostly - diagrams and contracts. |
| **Tasks** | What are the concrete, ordered, back-referenced units of work? | Yes - checklist with IDs. |
| **Implementation** | How does this translate to code? | Expensive once written. |
| **Validation** | Does the code actually satisfy the requirements? | Expensive - bug-fix cost. |
| **Review** | Does the result meet quality, security, performance, and maintainability bars? | Expensive - refactor cost. |

The further left a defect is caught, the cheaper it is. A misaligned PRD costs minutes to fix; a misaligned implementation costs days.

## Stage-by-stage

### PRD (`prds/`)

**Owner**: product / project sponsor (with `prd-author` agent assistance).
**Output**: `prds/active/<feature>.md` (full 23-section template) or `prds/active/<feature>-light.md` (lightweight).
**Acceptance**: status field set to `Approved`, all 23 sections completed (or explicitly marked `N/A`), Architecture Reference linked.

A PRD without business intent is a memo. A PRD without acceptance criteria is unfalsifiable. SpecForge's full template has both, and a Table of Contents because PRDs are long enough to benefit from one.

For features that genuinely fit on one page (single owner, single team, single acceptance criterion), use `lightweight-prd-template.md`. Features that cross two services or two teams use the full template - the structure is what surfaces the cross-team coordination cost.

### Spec triplet (`specs/`)

**Owner**: tech lead (with `spec-author` agent).
**Output**: `specs/examples/<feature>/{requirements,design,tasks}.md`.
**Acceptance**: every task back-references at least one requirement ID; every requirement has at least one task; design references resolve.

The triplet exists because conflating these three concerns is a known failure mode:

- **`requirements.md`** says *what* (user stories, acceptance criteria in `WHEN <event>, THE <system> SHALL <action>` form, stable IDs `R1.1`, `R1.2`, …).
- **`design.md`** says *how* (architecture, data models, API contracts, sequence diagrams, technology choices). It references requirements; it does not restate them.
- **`tasks.md`** says *do this* (numbered checklist with requirement back-refs `_Requirements: R1.1, R1.2_`). Each task is small enough to land in one PR.

When all three are coherent, the implementation prompt practically writes itself.

### Implementation (driven by `prompts/`)

**Owner**: implementer (human or agent).
**Output**: code that satisfies the tasks.
**Acceptance**: each task's checkbox is checked, with a PR link.

This is where the phased master-prompt pattern earns its keep. For multi-week work, the structure is:

```
prompts/
├── 000_GLOBAL_MASTER.md          single entry-point: role, mission, source-of-truth table, phase order
├── phase0_<name>/
│   ├── 000_MASTER_<phase>.md     phase summary, prerequisites, agent assignments
│   ├── 001_<task>.md             production task prompt (Objective, Context, Agent Assignment, Prerequisites, Task Details with current→target diff blocks, Acceptance Criteria)
│   └── 002_<task>.md
└── phase1_<name>/
    └── …
```

Numbered files, sorted phases, explicit agent assignments. The `task-prompt-template.md` shape is far richer than a flat "implement this" - it links to PRD, requirements, and design; it lists prerequisites; it shows current and target state side-by-side; it has explicit acceptance criteria. See `prompts/shared/task-prompt-template.md`.

### Validation

**Owner**: QA / test engineer (with `template-quality-reviewer` agent or domain agents).
**Output**: validation report, automated test pass.
**Acceptance**: every requirement has at least one validating check (test, manual procedure, or attestation).

For framework changes within SpecForge itself, "validation" means running `/audit` (sanitization + frontmatter + matrix consistency + broken links).

### Review

**Owner**: code reviewer (human or agent).
**Output**: PR approval / change requests.
**Acceptance**: review checklist completed; non-trivial concerns resolved.

See [`workflows/agent-review-loop.md`](../workflows/agent-review-loop.md) for the agent-assisted review pattern.

## When to skip stages

Almost never. Specifically:

- **Skipping the PRD** is appropriate for trivial bug fixes (one-line change, no behavioral impact, no user-facing surface).
- **Skipping the spec triplet** is appropriate when the lightweight feature spec covers the work in one page and there's a single owner.
- **Skipping implementation prompts** is appropriate when the implementer is a human writing code at their terminal - the prompts exist for agent execution.

Don't skip validation or review. Those are the gate.

## Anti-patterns we've seen

1. **PRD that's actually a design.** Mixing "we need to support filters" (requirement) with "we'll use Elasticsearch" (design). Solution: use the spec triplet to separate concerns.
2. **Tasks without back-refs.** Looks like progress until someone asks "what requirement does task #14 satisfy?" and nobody can answer. Solution: enforce back-references in `tasks.md`.
3. **One-shot implementation prompts for multi-week work.** Burns context, loses thread, diverges. Solution: phased master-prompt pattern.
4. **Stale PRDs that don't match the spec.** PRD said one thing, design diverged, nobody updated the PRD. Solution: PRD is the source of truth - when design must diverge, update the PRD first.
5. **No worked example.** Templates without an end-to-end demonstration leave contributors guessing. Solution: `examples/sample-project/` exists for this reason.

## Tools that help here

- `prd-author`, `spec-author`, `prompt-engineer` agents - see `.claude/agents/` for their operating principles.
- `scaffold-artifact` skill - bootstrap a new PRD, spec triplet, or prompt with the right frontmatter.
- `example-walkthrough` skill - guided end-to-end build of `examples/sample-project/`.
- `/audit` command - pre-commit comprehensive check.
- `template-quality-reviewer` agent - production-grade-and-immediately-usable bar for templates.
