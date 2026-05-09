# Sample Project: User Search

A self-contained, copy-and-run worked example. Paginated, filterable, indexed user-directory search (`GET /api/users/search`). Generic domain — no proprietary business logic.

This folder is **drop-in runnable**. Copy it into a new repo, do a small amount of post-copy setup, open Claude Code, and the agents can drive the implementation end to end against your stack.

## What's in here

```
sample-project/
├── README.md                   this file (drop-in instructions)
├── CLAUDE.md                   project context for Claude Code
├── prd.md                      full 23-section PRD
├── requirements.md             spec triplet pt 1 (R1.1 ... NFR-4.1)
├── design.md                   spec triplet pt 2 (architecture, API, data model)
├── tasks.md                    spec triplet pt 3 (22 numbered tasks + coverage table)
├── agent-roster.md             cross-vendor agent inventory + task assignments
├── implementation-plan.md      schedule, critical path, risks, definition of done
├── prompts/                    full phased prompt set
│   ├── 000_GLOBAL_MASTER.md
│   ├── README.md
│   ├── phase0_foundation/      tasks 1-3 (Q1, Q2, Q3 spikes / privacy review)
│   ├── phase1_backend/         tasks 4-12
│   ├── phase2_frontend/        tasks 13-17
│   ├── phase3_validation/      tasks 18-22
│   └── runtime/                operational prompts (pickup-next-task, daily-checkpoint)
└── .claude/                    Claude Code runtime
    ├── settings.json                       project-wide settings
    ├── settings.local.template.json        rename to settings.local.json after copy
    ├── claude_desktop_config.template.json rename to claude_desktop_config.json after copy
    ├── .forbidden-strings.template.txt     rename to .forbidden-strings.txt after copy
    ├── agents/                             8 implementation-team agents
    ├── commands/                           /sanitize, /audit, /status, /parity
    ├── hooks/                               hooks.json + 3 scripts
    └── agent-memory/
```

## Drop-in setup (5 minutes)

```bash
# 1. Copy this folder to your new repository.
cp -R /path/to/specforge/examples/sample-project/. /path/to/your-new-repo/

# 2. Move into your new repo.
cd /path/to/your-new-repo/

# 3. Rename the .template files (these are gitignored after rename).
mv .claude/settings.local.template.json     .claude/settings.local.json
mv .claude/claude_desktop_config.template.json .claude/claude_desktop_config.json
mv .claude/.forbidden-strings.template.txt  .claude/.forbidden-strings.txt

# 4. Add the renamed files to your project's .gitignore.
cat >> .gitignore <<'EOF'
.claude/settings.local.json
.claude/.forbidden-strings.txt
EOF

# 5. (Optional) Populate .claude/.forbidden-strings.txt with any private upstream
#    project names, internal identifiers, etc., that must never appear in tracked files.

# 6. (Optional) Set up a real git repo if you haven't.
git init
git add .
git commit -m "Bootstrap from SpecForge sample-project"
```

## Running the implementation

Once setup is done, open the repo with Claude Code and:

```
1. Read CLAUDE.md.
2. Read prompts/000_GLOBAL_MASTER.md end to end.
3. Read prd.md (sections 1-4) and design.md (sections 1-3).
4. Read tasks.md.
5. Open phase0_foundation/000_MASTER_foundation.md.
6. Execute tasks in order.
```

Or, for the fast path, use the runtime prompt:

```
Run prompts/runtime/pickup-next-task.md.
```

The agent will read `tasks.md`, find the lowest-numbered unchecked task whose prerequisites are met, name the primary agent (per `agent-roster.md`), and hand off.

## What the implementation team will do

The 8 agents under `.claude/agents/` will, between them:

1. **Phase 0** — `backend-engineer` runs cache-TTL + cursor-encoding spikes; `security-auditor` runs the privacy review. Output: decisions recorded in `design.md`.

2. **Phase 1** — `database-engineer` ships the index migration; `backend-engineer` builds the validator, RBAC scoping, query builder, cursor encoder, cache layer, observability instrumentation, rate limiting, and composes the endpoint. `unit-test-writer` and `integration-test-generator` author tests against requirement IDs. `security-auditor` reviews the boundary-critical PRs.

3. **Phase 2** — `frontend-engineer` builds the four UI components and composes the search page. E2E tests cover each user story.

4. **Phase 3** — `deployment-validator` runs the load test, validates the feature flag, executes the rollback drill in staging, and runs the 10% → 50% → 100% production rollout. `prd-author` updates docs per Section 12.

## Per-task work flow

For each task in `tasks.md`:

1. Open the task prompt at `prompts/phase{N}_<phase>/<NNN>_<task>.md`.
2. The prompt names a primary agent in Section 3 (Agent Assignment).
3. Invoke the agent with the task prompt as input.
4. The agent reads the back-referenced requirements, the relevant design sections, and the prerequisite checklist before starting.
5. The agent implements, writes tests for back-referenced requirement IDs, runs `/audit`, and opens a PR.
6. Check the task's box in `tasks.md`. Move on.

## Adapting to your stack

This sample is generic — Postgres / Redis / REST / web. Adapt for your specifics:

- **Different DB**: rewrite `database-engineer.md`'s operating principles + the index migration in `tasks.md` task 4.
- **Different API style** (GraphQL, RPC): rewrite `design.md` Section 4 + `backend-engineer.md`.
- **Different frontend framework**: rewrite the four component contracts in `design.md` + `frontend-engineer.md`.
- **No frontend** (API-only product): drop Phase 2 entirely; `frontend-engineer.md`; tasks 13-17.
- **Different domain**: rename `users/search` to your domain (e.g. `articles/search`, `events/search`); update the seven-or-so places it appears in the PRD and design.

The framework's contracts (frontmatter, spec triplet, phased prompts, hook protocol) stay constant.

## Vendor scope

This sample is **Claude-Code-only**. To target other agent CLIs (Codex, Gemini, Kiro, Cursor, Windsurf), see the SpecForge framework's `runtimes/.<vendor>/` layouts and adapt this sample's `.claude/` to the equivalent vendor directory.

For multi-vendor projects, you can keep `.claude/` here and add `.codex/`, `.gemini/`, etc. alongside; the spec triplet, prompts, and roster work in any agent CLI that reads markdown.

## See also

- [`../README.md`](../README.md) - the parent `examples/` README explaining the SpecForge worked-example pattern
- The SpecForge framework's [`agentic-docs/spec-driven-development.md`](../../agentic-docs/spec-driven-development.md) - the underlying methodology
- The framework's [`agentic-docs/automation-decision-framework.md`](../../agentic-docs/automation-decision-framework.md) - when to reach for skill / agent / command / hook
