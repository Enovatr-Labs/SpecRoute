# Documentation Structure: User Search Project

Where this project's docs live and why.

## Two-tier docs

Following the [framework's two-tier pattern](two-tier-docs-pattern.md):

- **Root context files** - short, loaded at every Claude Code session start.
- **Deep references** - read on demand.

| Tier | Files | Loaded |
|---|---|---|
| Root context | [`AGENTS.md`](../AGENTS.md), [`CLAUDE.md`](../CLAUDE.md) | every session |
| Deep references | [`agentic-docs/*`](.) | on demand |

## Where each doc lives

```
sample-project/
├── README.md                    drop-in setup walkthrough
├── AGENTS.md                    canonical context (~60 lines)
├── CLAUDE.md                    Claude-specific delegation shim
│
├── prds/active/user-search.md   PRD (the business intent)
├── specs/user-search/           spec triplet (requirements/design/tasks)
├── adrs/                        architectural decisions
│
├── agentic-docs/                deep references (this directory)
│   ├── philosophy.md            our operating beliefs
│   ├── spec-driven-development.md  how the flow plays out concretely
│   ├── agentic-coding-model.md  how skills/agents/commands/hooks compose
│   ├── automation-decision-framework.md  when to reach for which
│   ├── documentation-structure.md  this file
│   ├── two-tier-docs-pattern.md  short root + deep references
│   └── agent-memory.md          per-agent persistent context
│
├── prompts/                     execution plan
├── agent-roster.md              per-task agent assignments
├── implementation-plan.md       schedule, critical path, risks
└── .claude/                     Claude Code runtime
```

## What goes where (decision tree)

When you need to add documentation, ask:

1. **Is it about a single artifact?** (a specific PRD, spec, agent definition)
   -> Lives **with that artifact**, not in `agentic-docs/`.

2. **Is it conceptual or framework-level?** (philosophy, decision frameworks)
   -> Lives in **`agentic-docs/`**.

3. **Is it about how to do a recurring engineering task?**
   -> The framework has [`workflows/`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/workflows/) with playbooks. This project consumes those; we don't replicate.

4. **Is it an architectural decision?**
   -> Lives in **`adrs/`** as a numbered ADR.

5. **Is it directory-level guidance?** (what's in this directory, how do I add a file here)
   -> Lives in **that directory's `README.md`**.

6. **Is it root context an agent CLI loads at session start?**
   -> Lives in **`AGENTS.md`** (canonical) or [`CLAUDE.md`](../CLAUDE.md) (per-vendor shim).

## Sizing guidance

| File | Target |
|---|---|
| `AGENTS.md` | 50-100 lines (loaded every session) |
| `CLAUDE.md` (delegation shim) | 20-40 lines |
| Files in `agentic-docs/` | 60-120 lines each |
| ADR | 60-120 lines |
| README in any directory | 20-50 lines |
| PRD | as long as the 23 sections require |
| Spec triplet | as long as the spec requires |

A doc that grows past these targets is usually trying to be two things; consider splitting.

## Anti-patterns we avoid

- **Conceptual content in directory READMEs.** "Why does this matter?" belongs in `agentic-docs/`. The README answers "what's here and how do I add to it?"
- **Duplicating framework content.** We link to upstream SpecRoute docs rather than duplicate; only the project-specific contextualization lives here.
- **`agentic-docs/some-guide.md` that's actually a workflow.** Workflows live in the framework's `workflows/`; we consume them.
- **TODO markers as a placeholder for missing thinking.** TODOs are intentional - they mark places where a real value will be added later, not gaps in reasoning.

## See also

- The framework's canonical [`agentic-docs/documentation-structure.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/documentation-structure.md) for the broader doc-organization pattern.
- [`two-tier-docs-pattern.md`](two-tier-docs-pattern.md) for the root-vs-deep-reference distinction.
