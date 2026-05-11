# Workflows

<!-- sources: workflows/README.md -->

End-to-end engineering execution models. These are **operational playbooks** — what to do, in what order, when a recurring task comes up. Distinct from `agentic-docs/` (which answers conceptual questions) and `rules/` (which captures standing constraints).

For the canonical index, see [`workflows/README.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/workflows/README.md).

## Workflow map

```
                          ┌──────────────────────────────┐
                          │   Workflow PRD to Production │
                          │   (the outer workflow)       │
                          └──────────────┬───────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
   ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
   │ Workflow Spec to    │   │ Workflow Testing    │   │ Workflow Release    │
   │ Implementation      │   │ and Validation      │   │ Readiness           │
   │                     │   │                     │   │                     │
   │ inner loop per task │   │ pre-rollout gate    │   │ rollout playbook    │
   └──────────┬──────────┘   └─────────────────────┘   └─────────────────────┘
              │
              ▼
   ┌─────────────────────┐
   │ Workflow Agent      │
   │ Review Loop         │
   │ Stage 9 in detail   │
   └─────────────────────┘
```

## When to read which

| You're about to … | Read |
|---|---|
| Take a feature from idea to production | [[Workflow PRD to Production]] |
| Implement a single task from `tasks.md` | [[Workflow Spec to Implementation]] |
| Review a PR (human or agent) | [[Workflow Agent Review Loop]] |
| Validate a feature before rollout | [[Workflow Testing and Validation]] |
| Roll out to production | [[Workflow Release Readiness]] |

## What's in scope

Workflows describe **how to execute recurring engineering work**:

- The order of stages.
- The entry condition for each stage.
- The deliverable at each stage.
- The exit gate that promotes to the next stage.
- The role / agent that owns each stage.
- Common failure modes and how to recover.

## What's NOT in scope

| Question | Goes in |
|---|---|
| What is X? Why does Y exist? | `agentic-docs/` — see [[Documentation Structure]] |
| What standard must always hold? | `rules/` — see [[Rules]] |
| How is the runtime layout for Claude Code structured? | `runtimes/.claude/README.md` |
| How do I write a PRD? | `prds/templates/prd-template.md` — see [[PRDs]] |
| What's the canonical worked example? | [[Worked Example]] |

## Vendor-neutral

Workflow content is vendor-neutral. **Agent assignments** may differ by vendor (the agent CLI in use determines the available agent surface), but the workflow stages are the same.

## Owner agent

Workflows are owned by `framework-docs-author`. Updates that affect a specific stage's owner agent should be coordinated with that agent's owner.

## See also

- [[Spec-Driven Development]] — the underlying philosophy
- [[Automation Decision Framework]] — when to reach for skills / agents / commands / hooks during a workflow
- [[Worked Example]] — every workflow exercised on a real feature (`user-search`)
