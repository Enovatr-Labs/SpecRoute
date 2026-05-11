# Spec-Driven Development

<!-- sources: agentic-docs/spec-driven-development.md -->

The core flow SpecForge formalizes:

```
PRD → Spec (requirements + design + tasks) → Implementation → Validation → Review
```

Each stage produces a reviewable artifact. Each stage has a template, an agent assignment, and an acceptance criterion. The point is not ceremony — it's making agent-assisted work auditable.

For the canonical version, see [`agentic-docs/spec-driven-development.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/agentic-docs/spec-driven-development.md).

## Why this order

| Stage | Question it answers | Cheap to change? |
|---|---|---|
| **PRD** | What product problem are we solving? Who for? What's success? | Yes — text. |
| **Requirements** | What must be true for the system to count as solving it? | Yes — text with stable IDs. |
| **Design** | How will the architecture, data, and interfaces meet the requirements? | Mostly — diagrams + contracts. |
| **Tasks** | What are the concrete, ordered, back-referenced units of work? | Yes — checklist with IDs. |
| **Implementation** | How does this translate to code? | Expensive once written. |
| **Validation** | Does the code actually satisfy the requirements? | Expensive — bug-fix cost. |
| **Review** | Does the result meet quality, security, performance bars? | Expensive — refactor cost. |

The further left a defect is caught, the cheaper it is. A misaligned PRD costs minutes to fix; a misaligned implementation costs days.

## Stage-by-stage

### PRD (`prds/`)
- **Owner**: product / sponsor (with `prd-author` agent).
- **Output**: `prds/active/<feature>.md` (full 23-section template) or `<feature>-light.md`.
- **Acceptance**: `Status: Approved`; all sections completed or marked `N/A`; Architecture Reference linked.

See [[PRDs]] for templates and lifecycle.

### Spec triplet (`specs/`)
- **Owner**: tech lead (with `spec-author` agent).
- **Output**: `specs/<feature>/{requirements,design,tasks}.md`.
- **Acceptance**: every task back-references ≥1 requirement; every requirement maps to ≥1 task; coverage table populated.

The triplet exists because conflating these concerns is a known failure mode:

- **`requirements.md`** says *what* (`WHEN <event>, THE <system> SHALL <action>`, stable IDs `R1.1`, `R1.2`, …).
- **`design.md`** says *how* (architecture, data models, API contracts). References requirements; does not restate them.
- **`tasks.md`** says *do this* (numbered checklist with `_Requirements: R1.1, R1.2_` back-refs).

See [[Specs]].

### Implementation (driven by `prompts/`)
- **Owner**: implementer (human or agent).
- **Output**: code that satisfies the tasks.
- **Acceptance**: each task's checkbox is checked, with a PR link.

For multi-week work, use the phased master-prompt pattern:

```
prompts/
├── 000_GLOBAL_MASTER.md          single entry-point
├── phase0_<name>/
│   ├── 000_MASTER_<phase>.md     phase summary, prerequisites, agent assignments
│   ├── 001_<task>.md             production task prompt
│   └── 002_<task>.md
└── phase1_<name>/...
```

See [[Prompts]] and [[Workflow Spec to Implementation]].

### Validation
- **Owner**: QA / test engineer.
- **Output**: validation report; automated test pass.
- **Acceptance**: every requirement has at least one validating check.

See [[Workflow Testing and Validation]].

### Review
- **Owner**: code reviewer (human or agent).
- **Output**: PR approval / change requests.

See [[Workflow Agent Review Loop]].

## When to skip stages

Almost never. Specifically:

- **Skip the PRD** for trivial bug fixes (one-line change, no behavioral impact).
- **Skip the spec triplet** when the lightweight feature spec covers the work and there's a single owner.
- **Skip implementation prompts** when a human is writing code at their terminal — prompts exist for agent execution.

Don't skip validation or review. Those are the gate.

## Anti-patterns

1. **PRD that's actually a design.** Mixing "we need filters" (requirement) with "we'll use Elasticsearch" (design). Fix: use the spec triplet to separate concerns.
2. **Tasks without back-refs.** Looks like progress until someone asks "what requirement does task #14 satisfy?" Fix: enforce back-references in `tasks.md`.
3. **One-shot prompts for multi-week work.** Burns context, loses thread, diverges. Fix: phased master-prompt pattern.
4. **Stale PRDs that don't match the spec.** Fix: PRD is the source of truth — when design must diverge, update PRD first.
5. **No worked example.** Templates without an end-to-end demonstration leave contributors guessing. Fix: see [[Worked Example]].

## Tools that help

- `prd-author`, `spec-author`, `prompt-engineer` agents — see [[Implementation Team]].
- `scaffold-artifact` skill — bootstrap a new PRD / spec / prompt.
- `example-walkthrough` skill — guided end-to-end build.
- `/audit` command — pre-commit comprehensive check.
- `template-quality-reviewer` agent — production-grade bar.

## See also

- [[Philosophy]] — the beliefs that produced this flow
- [[Workflow PRD to Production]] — the outer engineering loop with all 13 stages
- [[Worked Example]] — the canonical example exercising every artifact
