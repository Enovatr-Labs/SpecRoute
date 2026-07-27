# Prompts

<!-- sources: prompts/README.md -->

Reusable prompts — global masters, phase masters, task prompts, and per-vendor prompt sets.

For the canonical reference, see [`prompts/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/prompts/README.md).

## Directory layout

```
prompts/
├── shared/                              vendor-neutral prompts
│   ├── global-master-prompt-template.md       000_GLOBAL_MASTER pattern
│   ├── phase-master-prompt-template.md        000_MASTER_<phase> pattern
│   ├── task-prompt-template.md                production task-prompt shape
│   ├── prd-to-spec-prompt.md                  convert PRD into spec triplet
│   ├── spec-to-tasks-prompt.md                derive tasks.md from req+design
│   └── code-review-prompt.md                  vendor-neutral code review
├── codex/                               Codex-specific prompts
│   ├── implementation-prompt.md
│   ├── refactor-prompt.md
│   ├── test-generation-prompt.md
│   └── repo-bootstrap-prompt.md
└── claude/                              Claude Code-specific prompts
    ├── implementation-prompt.md
    ├── refactor-prompt.md
    ├── test-generation-prompt.md
    └── repo-bootstrap-prompt.md
```

## The phased master-prompt pattern

The strongest spec-driven artifact in this framework. For multi-week initiatives:

```
prompts/<initiative>/
├── 000_GLOBAL_MASTER.md             single entry-point: role, mission, source-of-truth, phase order
├── phase0_<name>/
│   ├── 000_MASTER_<phase>.md        phase summary, prerequisites, agent assignments
│   ├── 001_<task>.md                production task prompt
│   ├── 002_<task>.md
│   └── ...
├── phase1_<name>/
│   └── ...
└── README.md                         phase index
```

Templates for the three layers:

| Layer | Template |
|---|---|
| Global master | [`shared/global-master-prompt-template.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/prompts/shared/global-master-prompt-template.md) |
| Phase master | [`shared/phase-master-prompt-template.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/prompts/shared/phase-master-prompt-template.md) |
| Task prompt | [`shared/task-prompt-template.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/prompts/shared/task-prompt-template.md) |

## The task-prompt shape (load-bearing)

The `task-prompt-template.md` is the heart of the framework. Its shape:

- **Objective** — one-line statement of what this task accomplishes.
- **Context** — cross-references to PRD, requirements, design, related tasks, ADRs.
- **Agent Assignment** — primary agent + any consulting agents.
- **Prerequisites** — tasks / state that must be done first.
- **Task Details** — current state → target state diff blocks for every file modification.
- **Acceptance Criteria** — testable, requirement-back-referenced.

This shape is far richer than a generic "implement this" prompt. It is what makes phased work auditable.

## Cross-vendor prompts

`shared/` holds prompts that work across all vendors. Use these by default; reach for `codex/` or `claude/` only when the prompt requires vendor-specific tooling (Claude's `Task` tool delegation, Codex's workspace-write sandbox, etc.).

## Per-vendor prompts

Each of `codex/` and `claude/` ships the same four prompts:

- `implementation-prompt.md` — short ad-hoc implementation prompt (use `task-prompt-template` for production work).
- `refactor-prompt.md` — behavior-preserving refactor.
- `test-generation-prompt.md` — generate tests against requirement IDs.
- `repo-bootstrap-prompt.md` — populate a new repo with SpecRoute structure.

Gemini, Kiro, Cursor, and Devin Desktop don't have dedicated prompt directories yet. The `shared/` prompts work in any agent CLI that reads markdown.

## Phase index pattern

For a multi-phase initiative, maintain `prompts/<initiative>/README.md` as the phase index. It enumerates phases, prerequisites, master prompts, and task counts. See `prompts/shared/global-master-prompt-template.md` for the index pattern.

## Owner agent

Designing and reviewing prompts is owned by the `prompt-engineer` agent.

## Worked example

The canonical `examples/sample-project/prompts/` directory has the **full phased prompt set** for the `user-search` feature:

- 1 global master (`000_GLOBAL_MASTER.md`).
- 4 phase masters (foundation / backend / frontend / validation).
- 22 numbered task prompts.
- 2 runtime operational prompts (`pickup-next-task.md`, `daily-checkpoint.md`).

Every numbered prompt instantiates the production task-prompt shape. See [[Worked Example]].

## See also

- [[Specs]] — `prd-to-spec` and `spec-to-tasks` prompts are the bridges from PRD to implementation
- [[Workflow Spec to Implementation]] — how a single task prompt drives merged code
- [[Worked Example]] — 28 prompt files in one feature
