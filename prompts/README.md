# Prompts

Reusable prompts - global masters, phase masters, task prompts, and per-vendor prompt sets.

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
| Global master | [`shared/global-master-prompt-template.md`](shared/global-master-prompt-template.md) |
| Phase master | [`shared/phase-master-prompt-template.md`](shared/phase-master-prompt-template.md) |
| Task prompt | [`shared/task-prompt-template.md`](shared/task-prompt-template.md) |

The task-prompt template is the load-bearing one. Its shape - Objective / Context (with PRD/spec/architecture cross-refs) / Agent Assignment / Prerequisites / Task Details (with current→target diff blocks) / Acceptance Criteria - is far richer than a generic implementation prompt and is what makes phased work auditable.

## Cross-vendor prompts

`shared/` holds prompts that work across all vendors. Use these by default; reach for `codex/` or `claude/` only when the prompt requires vendor-specific tooling (e.g. Claude's `Task` tool delegation, Codex's workspace-write sandbox).

## Per-vendor prompts

Each of `codex/` and `claude/` ships the same four prompts:

- `implementation-prompt.md` - short ad-hoc implementation prompt (use the `task-prompt-template` for production work)
- `refactor-prompt.md` - behavior-preserving refactor
- `test-generation-prompt.md` - generate tests against requirement IDs
- `repo-bootstrap-prompt.md` - populate a new repo with SpecRoute structure

Gemini, Kiro, Cursor, and Devin Desktop don't have dedicated prompt directories yet. The `shared/` prompts work in any agent CLI that can read a markdown prompt; the per-vendor directories grow as we identify vendor-specific tooling worth capturing.

## Phase index pattern

For a multi-phase initiative, maintain a `prompts/<initiative>/README.md` as the phase index. It enumerates phases, prerequisites, master prompts, and task counts. See [`shared/global-master-prompt-template.md`](shared/global-master-prompt-template.md) for the index pattern at the global-master level.

## Authoring agent

Designing and reviewing prompts is owned by the `prompt-engineer` agent. See `.claude/agents/prompt-engineer.md` for its operating principles.
