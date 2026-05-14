# Documentation Structure

<!-- sources: agentic-docs/documentation-structure.md -->

Where new documentation goes. A decision tree for contributors so the framework's docs stay coherent as it grows.

For the canonical version, see [`agentic-docs/documentation-structure.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/documentation-structure.md).

## Quick decision tree

When you need to add documentation, ask:

1. **About a single artifact you're producing right now?** (a specific PRD / spec / agent definition) → with that artifact. PRDs in `prds/active/`; specs in `specs/<feature>/`; agents in `agents/examples/`.
2. **Conceptual or framework-level?** (philosophy, decision frameworks, integration patterns) → `agentic-docs/`.
3. **About how to do a recurring engineering task?** (PRD-to-production, spec-to-implementation, release readiness) → `workflows/`.
4. **An engineering rule or standard?** → `rules/`.
5. **Directory-level guidance?** (what does this directory contain, how do I add a new file here) → that directory's `README.md`.
6. **Root context — something an agent CLI loads at session start?** → `AGENTS.md` (canonical) or a delegation shim (`CLAUDE.md`, `GEMINI.md`).

## Where each doc type lives

```
specroute/
├── README.md                            project overview, vendor matrix, getting-started
├── AGENTS.md                            canonical root context
├── CLAUDE.md / GEMINI.md                vendor-specific delegation shims
├── CONTRIBUTING.md / SECURITY.md / etc. governance
├── ROADMAP.md                           project trajectory
│
├── agentic-docs/                        conceptual, framework-level
│   ├── philosophy.md
│   ├── spec-driven-development.md
│   ├── agentic-coding-model.md
│   ├── automation-decision-framework.md
│   ├── two-tier-docs-pattern.md
│   ├── multi-vendor-context-files.md
│   ├── agent-cli-integrations.md
│   ├── cross-vendor-sync.md
│   ├── agent-memory.md
│   └── documentation-structure.md
│
├── workflows/                           recurring engineering tasks
├── rules/                               engineering standards
└── (per-directory READMEs)              directory-level guidance
```

## Why these distinctions

### `agentic-docs/` vs `workflows/`

- **`agentic-docs/`** answers *conceptual* questions: *what is X? why does Y exist?* Read once, refer back occasionally.
- **`workflows/`** answers *procedural* questions: *what do I do, in what order, when X is needed?* Operational playbooks — read every time you do that thing.

Mixing the two produces hybrid docs that satisfy neither audience.

### `rules/` vs `workflows/`

- **`rules/`** are *standing constraints* — things that are always true. "Tests must have real assertions."
- **`workflows/`** are *time-ordered sequences* — what to do first, second, third.

A rule is a noun (a standard); a workflow is a verb (a procedure).

### Per-directory `README.md` vs `agentic-docs/`

A directory's `README.md` answers questions specific to **that directory**: what files belong here, what frontmatter is required, how to add a new entry. Terse and operational. `agentic-docs/` covers concepts that span directories.

## What does NOT belong in `agentic-docs/`

- **Specific PRDs or specs** — live with the artifact.
- **Operational runbooks** for a specific service — alongside the service or in `workflows/`.
- **Per-agent operating principles** — in the agent's `.md` file.
- **Per-skill documentation** — in `SKILL.md`.
- **Per-vendor integration details that fit in 5 lines** — in the vendor's runtime README.

## Sizing guidance

| File type | Sweet spot |
|---|---|
| Root context file (`AGENTS.md`, `CLAUDE.md`) | 50–150 lines |
| `agentic-docs/<topic>.md` | 100–300 lines |
| `workflows/<flow>.md` | 100–250 lines |
| `rules/<topic>.md` | 80–200 lines |
| Directory `README.md` | 30–100 lines |
| Template (PRD, spec) | as long as the template requires |
| Worked example | as long as the artifact requires |

A doc growing past these targets is usually trying to be two things — consider splitting.

## Anti-patterns

- **Conceptual content in directory READMEs.** "Why does this matter?" belongs in `agentic-docs/`.
- **Duplicating a rule in multiple places.** Rules live in `rules/`; other docs reference them.
- **`agentic-docs/<x>.md` that's actually a workflow.** If it has numbered steps to follow, it's a workflow.
- **Workflows that re-explain concepts.** Link to `agentic-docs/` instead.

## See also

- [[Two-Tier Docs Pattern]] — short root context vs. deep references
- [[Rules]] — content quality standards
- [[Repository Structure]] — the directory map
