# Documentation Structure

Where new documentation goes. A decision tree for contributors so the framework's docs stay coherent as it grows.

## Quick decision tree

When you need to add documentation, ask:

1. **Is it about a single artifact you're producing right now?** (a specific PRD, a specific spec, a specific agent definition)
   → Lives **with that artifact**, not in `agentic-docs/`. PRDs go in `prds/active/`; specs go in `specs/examples/<feature>/`; agents in `agents/examples/`.

2. **Is it conceptual or framework-level?** (philosophy, decision frameworks, integration patterns)
   → Lives in **`agentic-docs/`**.

3. **Is it about how to do a recurring engineering task?** (PRD-to-production, spec-to-implementation, release readiness)
   → Lives in **`workflows/`**.

4. **Is it an engineering rule or standard?**
   → Lives in **`rules/`**.

5. **Is it directory-level guidance?** (what does this directory contain, how do I add a new file here)
   → Lives in **that directory's `README.md`**.

6. **Is it root context - something an agent CLI loads at session start?**
   → Lives in **`AGENTS.md`** (canonical) or a delegation shim (`CLAUDE.md`, `GEMINI.md`).

## Where each doc type lives

```
specroute/
├── README.md                            project overview, vendor matrix, getting-started
├── AGENTS.md                            canonical root context (single source of truth)
├── CLAUDE.md / GEMINI.md                vendor-specific delegation shims
├── CONTRIBUTING.md / SECURITY.md / etc. governance
├── ROADMAP.md                           project trajectory
│
├── agentic-docs/                        conceptual, framework-level
│   ├── philosophy.md
│   ├── spec-driven-development.md
│   ├── agentic-coding-model.md
│   ├── automation-decision-framework.md
│   ├── documentation-structure.md       (this file)
│   ├── two-tier-docs-pattern.md
│   ├── multi-vendor-context-files.md
│   ├── agent-cli-integrations.md
│   ├── cross-vendor-sync.md
│   ├── agent-memory.md
│   └── multi-agent-orchestration.md
│
├── workflows/                           recurring engineering tasks
│   ├── prd-to-production.md
│   ├── spec-to-implementation.md
│   ├── agent-review-loop.md
│   ├── testing-and-validation.md
│   └── release-readiness.md
│
├── rules/                               engineering standards
│   ├── engineering-rules.md
│   ├── code-review-rules.md
│   ├── security-rules.md
│   ├── documentation-rules.md
│   ├── codex-rules.md / claude-rules.md / etc.
│   └── steering/                        rule-loading mode templates
│
├── prds/, specs/, agents/, skills/, ... templates and examples; each has a README
└── examples/                            worked examples; each has a README
```

## Why these distinctions

### `agentic-docs/` vs `workflows/`

**`agentic-docs/`** answers conceptual questions: *what is X? why does Y exist?* These are the framework's intellectual content - read once, refer back occasionally.

**`workflows/`** answers procedural questions: *what do I do, in what order, when X is needed?* These are operational playbooks - read every time you do that thing.

Mixing the two produces hybrid docs that satisfy neither audience.

### `rules/` vs `workflows/`

**`rules/`** are *standing constraints* - things that are always true. "Tests must have real assertions." "Secrets never live in tracked files."

**`workflows/`** are *time-ordered sequences* - what to do first, second, third. "Open a PR. Run /audit. Fix findings. Request review."

A rule is a noun (a standard); a workflow is a verb (a procedure).

### Per-directory `README.md` vs `agentic-docs/`

A directory's `README.md` answers questions specific to **that directory**: what files belong here, what frontmatter is required, how to add a new entry. It's terse and operational.

`agentic-docs/` covers concepts that span directories or are framework-level. The PRD template's body lives in `prds/templates/`; the *philosophy* of "specs first, code second" lives in `agentic-docs/philosophy.md`.

## What does NOT belong in `agentic-docs/`

- **Specific PRDs or specs.** Those live with the artifact.
- **Operational runbooks** for a specific service or environment. Those go alongside the service or in `workflows/`.
- **Per-agent operating principles.** Those go in the agent's `.md` file.
- **Per-skill documentation.** Goes in `SKILL.md`.
- **Per-vendor integration details that fit in 5 lines.** Goes in the vendor's runtime README.

## Sizing guidance

| File type | Sweet spot |
|---|---|
| Root context file (`AGENTS.md`) | ~100 lines, hard cap ~150 |
| Delegation shim (`CLAUDE.md`, `GEMINI.md`) | 30–50 lines, hard cap 75 |
| `docs/<topic>.md` | 100–300 lines |
| `workflows/<flow>.md` | 100–250 lines |
| `rules/<topic>.md` | 80–200 lines |
| Directory `README.md` | 30–100 lines |
| Template (PRD, spec) | as long as the template requires |
| Worked example | as long as the artifact requires |

A doc that grows past these targets is usually trying to be two things; consider splitting.

## Anti-patterns

- **Conceptual content in directory READMEs.** "Why does this matter?" belongs in `agentic-docs/`. The README answers "what's here and how do I add to it?"
- **Duplicating a rule in multiple places.** Rules live in `rules/`; other docs reference them.
- **`docs/some-guide.md` that's actually a workflow.** If it has numbered steps to follow, it's a workflow.
- **Workflows that re-explain concepts.** If the reader needs to understand the *why*, link to `agentic-docs/`.

## Authoring agent

Documentation structure is owned by the `framework-docs-author` agent. See [`.claude/agents/framework-docs-author.md`](../.claude/agents/framework-docs-author.md) for its operating principles.

## See also

- [`two-tier-docs-pattern.md`](two-tier-docs-pattern.md) - short root context + deep references.
- [`multi-agent-orchestration.md`](multi-agent-orchestration.md) - the all-hands pattern; a composition of the four primitives, not a fifth one.
- [`rules/documentation-rules.md`](../rules/documentation-rules.md) - content quality standards.
