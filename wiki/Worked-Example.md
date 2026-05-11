# Worked Example

<!-- sources: examples/README.md -->

The canonical demonstration. **`examples/sample-project/`** is drop-in runnable: copy the folder into a new repository and Claude Code drives the implementation end to end.

For the directory's README, see [`examples/README.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/examples/README.md). For the example itself, see [`examples/sample-project/`](https://github.com/Enovatr-Labs/SpecForge/tree/main/examples/sample-project).

## What it demonstrates

The `user-search` feature exercises every artifact shape in SpecForge:

| Artifact | What's there |
|---|---|
| **PRD** | Full 23-section enterprise PRD. Real product framing, success metrics, scope, performance budgets, security requirements |
| **Spec triplet** | `requirements.md` with stable IDs `R1.1` → `NFR-4.1`, `design.md` with `**Satisfies:**` annotations everywhere, `tasks.md` with 22 numbered tasks, each ending in `_Requirements: <ids>_` |
| **Coverage table** | Every requirement and NFR mapped to the tasks that satisfy it. No `TODO` rows |
| **Agent roster** | Generic archetypes only (no domain agents), task-by-task assignments, coordination notes |
| **Phased prompts** | 1 global master + 4 phase masters + 22 numbered task prompts + 2 runtime operational prompts = 29 files |
| **Runtime layout** | Working `.claude/` with 8 agents, 4 slash commands, 3 hooks, sanitization wordlist scaffolding |
| **Implementation plan** | Schedule, resource assignment, critical path, risks watch, definition of done |
| **5 ADRs** | Postgres indexed scans, cursor pagination, Redis cache TTL, HMAC-signed cursors, filter-set hash logging |

## Two modes of use

### A. Read the example (5 minutes)

Walk the artifacts in spec-driven order:

1. [`prds/active/user-search.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/examples/sample-project/prds/active/user-search.md) — read as a product reviewer.
2. [`specs/user-search/requirements.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/examples/sample-project/specs/user-search/requirements.md) — PRD goals → stable-ID requirements.
3. [`specs/user-search/design.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/examples/sample-project/specs/user-search/design.md) — requirements → architecture.
4. [`specs/user-search/tasks.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/examples/sample-project/specs/user-search/tasks.md) — design → numbered work items with back-refs.
5. [`agent-roster.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/examples/sample-project/agent-roster.md) — tasks → agents.
6. [`prompts/000_GLOBAL_MASTER.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/examples/sample-project/prompts/000_GLOBAL_MASTER.md) — entry-point.
7. [`prompts/README.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/examples/sample-project/prompts/README.md) — phase index.
8. Any phase master + any numbered task prompt.
9. [`implementation-plan.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/examples/sample-project/implementation-plan.md) — the operational view.

If a step seems redundant, **the redundancy is intentional**. The cross-references between artifacts are how the work stays auditable.

### B. Run the example (15 minutes)

Copy the folder into a new repo and let Claude Code drive:

```bash
# 1. Copy.
cp -R examples/sample-project/. /path/to/your-new-repo/

# 2. Move into the new repo.
cd /path/to/your-new-repo/

# 3. Rename the .template files (they become gitignored).
mv .claude/settings.local.template.json     .claude/settings.local.json
mv .claude/claude_desktop_config.template.json .claude/claude_desktop_config.json
mv .claude/.forbidden-strings.template.txt  .claude/.forbidden-strings.txt

# 4. Add the renamed files to .gitignore.
cat >> .gitignore <<'EOF'
.claude/settings.local.json
.claude/.forbidden-strings.txt
EOF

# 5. (Optional) git init && git add . && git commit -m "Bootstrap from SpecForge"

# 6. Open the repo with Claude Code.
```

Then in Claude Code:

```
Read prompts/000_GLOBAL_MASTER.md, then run prompts/runtime/pickup-next-task.md.
```

The agent reads the spec triplet, finds the next unblocked task, routes to the right primary agent. The implementation team will:

- Run Phase 0 spikes + privacy review.
- Build the API endpoint with full filter coverage, RBAC scoping, cursor pagination, cache layer, observability, rate limiting (Phase 1).
- Build the search page with all four components and full E2E coverage (Phase 2).
- Run the load test, validate the feature flag, drill the rollback in staging, and execute the gradual production rollout (Phase 3).

## Directory layout

```
examples/sample-project/
├── README.md                       drop-in setup + run instructions
├── CLAUDE.md                       project context
├── prds/active/user-search.md      full 23-section PRD
├── specs/user-search/
│   ├── requirements.md             11 requirements + 11 NFRs
│   ├── design.md                   architecture, data model, APIs
│   └── tasks.md                    22 tasks + coverage table
├── adrs/                           5 architecture decision records
├── agentic-docs/                   7 project-specific deep references
├── agent-roster.md                 agent inventory + per-task assignments
├── implementation-plan.md          schedule, critical path, risks
├── prompts/
│   ├── 000_GLOBAL_MASTER.md        entry-point
│   ├── README.md                   phase index
│   ├── phase0_foundation/          tasks 1–3 (spikes + privacy review)
│   ├── phase1_backend/             tasks 4–12 (indexes → endpoint composition)
│   ├── phase2_frontend/            tasks 13–17 (4 components + page composition)
│   ├── phase3_validation/          tasks 18–22 (load test, flag, rollout, docs)
│   └── runtime/                    operational prompts
└── .claude/
    ├── settings.json
    ├── settings.local.template.json
    ├── claude_desktop_config.template.json
    ├── .forbidden-strings.template.txt
    ├── agents/                     8 implementation-team agents
    ├── commands/                   /sanitize, /audit, /status, /parity
    ├── hooks/                      hooks.json + 3 hook scripts
    └── agent-memory/
```

## Adapting to your stack

`sample-project/` is generic — Postgres / Redis / REST / web. The **framework's contracts** (frontmatter, spec triplet, phased prompts, hook protocol) hold across stacks; what changes is the implementation specifics. See `sample-project/README.md` "Adapting to your stack" for the seven-or-so places that need swapping for different languages / DBs / API styles / domains.

## Future examples (not built yet)

Suggested next worked examples:

- **Lightweight feature** — single-team feature using `lightweight-prd-template.md` + `feature-spec-template.md`.
- **Refactor** — behavior-preserving refactor using `technical-spec-template.md`.
- **ADR** — single architectural decision using the ADR template.
- **Codex variant** of `sample-project/` — same artifacts, `.codex/` runtime instead of `.claude/`.

## Anti-patterns to avoid (in any new examples)

- **Theoretical content** — every section must be filled in concretely.
- **Domain-specific naming** — keep examples generic (no financial, healthcare, legal specifics).
- **Mismatched cross-references** — PRD NFRs must match requirements NFRs must match design NFRs.
- **Drifted templates** — when SpecForge templates change, examples that exercise those templates need to be re-checked.

The `template-quality-reviewer` agent is the gate. See [[Implementation Team]].

## See also

- [[Quickstart]] — how to use the example to bootstrap your own repo
- [[Spec-Driven Development]] — the flow the example embodies
- [[Workflow PRD to Production]] — the outer workflow exercised in full
- [[Implementation Team]] — the 8 agents `sample-project/.claude/` ships with
