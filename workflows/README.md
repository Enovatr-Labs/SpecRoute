# Workflows

End-to-end engineering execution models. These are operational playbooks - what to do, in what order, when a recurring task comes up. Distinct from `agentic-docs/` (which answers conceptual questions) and `rules/` (which captures standing constraints).

```
workflows/
├── README.md                           (this file)
├── prd-to-production.md                outer workflow: PRD → live in production
├── spec-to-implementation.md           inner workflow: one task → merged code
├── agent-review-loop.md                how agent-assisted review runs
├── testing-and-validation.md           the validation gate before rollout
└── release-readiness.md                the rollout playbook
```

## Workflow map

```
                          ┌──────────────────────────────┐
                          │   prd-to-production.md       │
                          │   (the outer workflow)       │
                          └──────────────┬───────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
   ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
   │ spec-to-            │   │ testing-and-        │   │ release-            │
   │ implementation.md   │   │ validation.md       │   │ readiness.md        │
   │                     │   │                     │   │                     │
   │ inner loop per task │   │ pre-rollout gate    │   │ rollout playbook    │
   └──────────┬──────────┘   └─────────────────────┘   └─────────────────────┘
              │
              ▼
   ┌─────────────────────┐
   │ agent-review-loop.md│
   │ Stage 9 in detail   │
   └─────────────────────┘
```

## When to read which

| You're about to … | Read |
|---|---|
| Take a feature from idea to production | [`prd-to-production.md`](prd-to-production.md) |
| Implement a single task from `tasks.md` | [`spec-to-implementation.md`](spec-to-implementation.md) |
| Review a PR (human or agent) | [`agent-review-loop.md`](agent-review-loop.md) |
| Validate a feature before rollout | [`testing-and-validation.md`](testing-and-validation.md) |
| Roll out to production | [`release-readiness.md`](release-readiness.md) |

## What's in scope here

Workflows describe **how to execute recurring engineering work**:

- The order of stages.
- The entry condition for each stage.
- The deliverable at each stage.
- The exit gate that promotes to the next stage.
- The role / agent that owns each stage.
- Common failure modes and how to recover.

## What's NOT in scope here

| Question | Goes in |
|---|---|
| What is X? Why does Y exist? | `agentic-docs/` |
| What standard must always hold? | `rules/` |
| How is the runtime layout for Claude Code structured? | `runtimes/.claude/README.md` |
| How do I write a PRD? | `prds/templates/prd-template.md` + `prds/README.md` |
| What's the canonical worked example? | `examples/sample-feature/` |

## Vendor-neutral

Workflow content is vendor-neutral. Agent assignments may differ by vendor (the agent CLI in use determines the available agent surface), but the workflow stages are the same.

## Authoring agent

Workflows are owned by `framework-docs-author`. Updates to a workflow that affect a specific stage's owner agent should be coordinated with that agent's owner.

## See also

- [`agentic-docs/spec-driven-development.md`](../agentic-docs/spec-driven-development.md) - the underlying philosophy.
- [`agentic-docs/automation-decision-framework.md`](../agentic-docs/automation-decision-framework.md) - when to reach for skills vs agents vs commands vs hooks during a workflow.
- [`examples/sample-feature/implementation-plan.md`](../examples/sample-feature/implementation-plan.md) - a worked example of these workflows in operation.
