# Examples

End-to-end worked examples that demonstrate the SpecRoute artifact pipeline. The canonical example is **drop-in runnable** — copy the folder into a new repository and Claude Code can drive the implementation end to end.

```
examples/
├── README.md                       (this file)
└── sample-project/                 canonical worked example: user-search
    ├── README.md                   drop-in setup + run instructions
    ├── CLAUDE.md                   project context for Claude Code
    ├── prd.md                      full 23-section enterprise PRD
    ├── requirements.md             spec triplet pt 1 (stable IDs R1.1 ... NFR-4.1)
    ├── design.md                   spec triplet pt 2 (architecture, data model, APIs)
    ├── tasks.md                    spec triplet pt 3 (22 tasks + coverage table)
    ├── agent-roster.md             agent inventory + per-task assignments
    ├── implementation-plan.md      schedule, critical path, risks, definition of done
    ├── prompts/                    full phased prompt set
    │   ├── 000_GLOBAL_MASTER.md    entry-point
    │   ├── README.md               phase index
    │   ├── phase0_foundation/      tasks 1-3 (spikes + privacy review)
    │   ├── phase1_backend/         tasks 4-12 (indexes -> endpoint composition + rate limit)
    │   ├── phase2_frontend/        tasks 13-17 (4 components + page composition)
    │   ├── phase3_validation/      tasks 18-22 (load test, flag, rollout, docs, rollback drill)
    │   └── runtime/                operational prompts (pickup-next-task, daily-checkpoint)
    └── .claude/                    Claude Code runtime layout
        ├── settings.json                       project-wide settings
        ├── settings.local.template.json        rename after copy (gitignored)
        ├── mcp.template.json                   rename after copy
        ├── .forbidden-strings.template.txt     rename after copy (gitignored)
        ├── agents/                             9 implementation-team agents
        ├── commands/                           /sanitize, /audit, /status, /parity
        ├── hooks/                              hooks.json + 3 hook scripts
        └── agent-memory/
```

## Two modes of use

### A. Read the example (5 minutes)

Walk the artifacts in spec-driven order to see how SpecRoute fits together:

1. [`sample-project/prds/active/user-search.md`](sample-project/prds/active/user-search.md) - start here, read as a product reviewer.
2. [`sample-project/specs/user-search/requirements.md`](sample-project/specs/user-search/requirements.md) - see how PRD goals translate into stable-ID requirements.
3. [`sample-project/specs/user-search/design.md`](sample-project/specs/user-search/design.md) - see how requirements drive the architecture.
4. [`sample-project/specs/user-search/tasks.md`](sample-project/specs/user-search/tasks.md) - see how design decomposes into numbered work items with full back-references.
5. [`sample-project/agent-roster.md`](sample-project/agent-roster.md) - see how tasks map to agents.
6. [`sample-project/prompts/000_GLOBAL_MASTER.md`](sample-project/prompts/000_GLOBAL_MASTER.md) - the agent CLI entry-point.
7. [`sample-project/prompts/README.md`](sample-project/prompts/README.md) - phase index for all 22 task prompts plus the runtime/ operational prompts.
8. Open any phase master, e.g. [`phase1_backend/000_MASTER_backend.md`](sample-project/prompts/phase1_backend/000_MASTER_backend.md), then any numbered task prompt e.g. [`004_index_migration.md`](sample-project/prompts/phase1_backend/004_index_migration.md).
9. [`sample-project/implementation-plan.md`](sample-project/implementation-plan.md) - the operational view.

The flow is the framework's value proposition in concrete form. If a step seems redundant, the redundancy is intentional - the cross-references between artifacts are how the work stays auditable.

### B. Run the example (15 minutes)

Copy the folder into a new repo and let Claude Code drive:

```bash
# 1. Copy.
cp -R examples/sample-project/. /path/to/your-new-repo/

# 2. Move into the new repo.
cd /path/to/your-new-repo/

# 3. Rename the .template files (these become gitignored).
mv .claude/settings.local.template.json     .claude/settings.local.json
mv .claude/mcp.template.json                .mcp.json
mv .claude/.forbidden-strings.template.txt  .claude/.forbidden-strings.txt

# 4. Add the renamed files to .gitignore.
cat >> .gitignore <<'EOF'
.claude/settings.local.json
.claude/.forbidden-strings.txt
EOF

# 5. (Optional) git init && git add . && git commit -m "Bootstrap from SpecRoute"

# 6. Open the repo with Claude Code.
```

Then in Claude Code:

```
Read prompts/000_GLOBAL_MASTER.md, then run prompts/runtime/pickup-next-task.md.
```

The agent reads the spec triplet, finds the next unblocked task, and routes to the right primary agent (per `.claude/agents/`). The implementation team will:

- Run Phase 0 spikes + privacy review.
- Build the API endpoint with full filter coverage, RBAC scoping, cursor pagination, cache layer, observability, rate limiting (Phase 1).
- Build the search page with all four components and full E2E coverage (Phase 2).
- Run the load test, validate the feature flag, drill the rollback in staging, and execute the gradual production rollout (Phase 3).

See [`sample-project/README.md`](sample-project/README.md) for the full drop-in walkthrough including stack-adaptation notes.

## What this example demonstrates

The `user-search` feature exercises every artifact shape in SpecRoute:

- **PRD** - the full 23-section enterprise template ([`prds/templates/prd-template.md`](../prds/templates/prd-template.md)). Real product framing, success metrics, scope boundaries, performance budgets, security requirements.
- **Spec triplet** - `requirements.md` with stable IDs (`R1.1` through `NFR-4.1`), `design.md` referencing those IDs in every section with `**Satisfies:**` annotations, `tasks.md` with numbered work items each ending in `_Requirements: <ids>_`.
- **Coverage table** - `tasks.md` includes a coverage table mapping every requirement and NFR to the tasks that satisfy it. Every cell is populated.
- **Agent roster** - generic archetypes only (no domain-specific agents), with task-by-task assignments and coordination notes.
- **Phased prompts** - full set: a global master, four phase masters, and twenty-two numbered task prompts plus two runtime operational prompts. Every numbered prompt instantiates the production task-prompt shape (Objective / Context / Agent Assignment / Prerequisites / Task Details with current→target diff blocks / Acceptance Criteria).
- **Runtime layout** - a working `.claude/` with 9 implementation-team agents, 4 slash commands, 3 hook scripts, and the sanitization wordlist scaffolding. Drop-in functional.
- **Implementation plan** - the operational layer that composes everything: schedule, resource assignment, critical path, risks watch, definition of done.

## Adapting to your stack

`sample-project/` is generic — Postgres / Redis / REST / web. The framework's contracts (frontmatter, spec triplet, phased prompts, hook protocol) hold across stacks; what changes is the implementation specifics. See `sample-project/README.md` "Adapting to your stack" for the seven-or-so places that need swapping for different languages, DBs, API styles, or domains.

## Adding more examples

Future examples should:

1. **Use a generic feature** - no domain-specific business logic (no financial, healthcare, legal, etc.).
2. **Exercise a different shape** - e.g. a refactor (use `technical-spec-template.md`), an architectural decision (use the ADR template), a single-team feature (use `lightweight-prd-template.md` and `feature-spec-template.md`).
3. **Cross-reference real templates** - link to `prds/templates/`, `specs/templates/`, `prompts/shared/` - don't reinvent.
4. **Include the runtime layer** - if it's meant to be drop-in runnable, ship a working `.claude/` (or `.codex/`, etc.) alongside the artifacts.

Suggested next examples (none built yet):

- **Lightweight feature**: a single-team feature using `lightweight-prd-template.md` + `feature-spec-template.md`.
- **Refactor**: a behavior-preserving refactor using `technical-spec-template.md`.
- **ADR**: a single architectural decision using the ADR template.
- **Codex variant** of `sample-project/`: same artifacts, with `.codex/` runtime instead of `.claude/`.

## Anti-patterns to avoid

- **Theoretical content** - every section must be filled in concretely. Placeholder-only text defeats the example's purpose.
- **Domain-specific naming** - generic only.
- **Mismatched cross-references** - the PRD's NFRs must match the requirements' NFRs must match the design's NFRs.
- **Drifted templates** - when SpecRoute templates change, examples that exercise those templates need to be re-checked.

The `template-quality-reviewer` agent is the gate; see [`.claude/agents/template-quality-reviewer.md`](../.claude/agents/template-quality-reviewer.md).
