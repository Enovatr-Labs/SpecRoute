# Agent Memory in This Project

Per-agent persistent context that survives across conversations. Each `.claude/agents/<name>.md` agent can have a corresponding directory under `.claude/agent-memory/<name>/` holding free-form notes the agent re-reads at session start.

## Layout

```
.claude/agent-memory/
├── README.md             explains the convention
└── <agent-name>/
    └── <topic>.md        free-form notes; descriptive filenames
```

In this project the directory exists but is sparsely populated by default - agents accumulate memory as the project progresses.

## What a project-specific memory entry might look like

For `backend-engineer`, after Phase 0 spikes finish, an example memory entry:

`.claude/agent-memory/backend-engineer/phase0-decisions.md`:

```markdown
# Phase 0 Decisions Affecting Phase 1 Work

- Cache TTL: 60s (per ADR-003). Read this from config; do not hardcode.
- Cursor format: HMAC-SHA256 signed base64 (per ADR-004). Signing key from
  secrets manager; verify path tries current then previous key for rotation.
- Logging: filter-set hash only (per ADR-005). No plaintext query strings
  in any log line; unit test asserts this.

## Open follow-ups
- Q4: Should we expose `cache_hit` in the response metadata? Currently yes,
  for client-side observability. Revisit if it's misleading to admins.
```

For `deployment-validator`, an entry tracking the rollout state:

`.claude/agent-memory/deployment-validator/rollout-progress.md`:

```markdown
# User-Search Rollout Progress

- 10% rollout: 2026-05-12, stable for 24h. p95: 142ms (under budget).
- 50% rollout: 2026-05-13, in progress. Watching cache hit rate (currently 38%,
  expected to climb past 40% as steady state stabilizes).
- 100% rollout: scheduled 2026-05-14.
```

These are notes that survive across conversations - "where did we leave off?" - without polluting the codebase.

## What does NOT go in agent memory

- **Anything that should be a real artifact.** If a decision is worth tracking, it's an ADR. If it's a project convention, update `AGENTS.md` or a rule. Memory is for state, not for content that should be discoverable through the spec-driven flow.
- **Live secrets or credentials.**
- **Customer / actor PII.**
- **Anything proprietary to upstream codebases.** Memory files are tracked. They ship with the project.

## When to write a memory entry vs an artifact

| Content | Memory or artifact? |
|---|---|
| "We decided cache TTL is 60s" | Artifact (ADR-003) |
| "Notes on the trade-offs that surfaced during the cache TTL spike" | Artifact (ADR-003 alternatives section) |
| "Rollout currently at 50%, watching cache hit rate" | Memory (operational state) |
| "I noticed the staging Postgres is on the older minor version; opened a ticket" | Memory (not yet codified) -> if the issue persists, escalate to a real artifact |
| "Backend-engineer's preferred test file naming convention" | Memory (preference) -> if team-wide, update `rules/code-review-rules.md` in the framework |

## Vendor parity note

This project is Claude-only, so memory lives only at `.claude/agent-memory/`. If we added Codex support later, mirroring memory directly into `.codex/agent-memory/` may not make sense - memory is per-agent operational state, and the Codex agents would have their own corresponding state.

## See also

- The framework's canonical [`agentic-docs/agent-memory.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/agent-memory.md) for the broader pattern.
- [`.claude/agents/README.md`](../.claude/agents/README.md) - the agent roster (each agent can have a memory dir).
- [`adrs/`](../adrs/) - where decisions go (vs operational state, which goes in memory).
