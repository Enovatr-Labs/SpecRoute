# Agent Memory

<!-- sources: agentic-docs/agent-memory.md -->

Per-agent persistent context that survives across conversations. Agents that maintain state — open TODOs, decisions made, where they left off — write notes that they re-read at the start of each session.

For the canonical version, see [`agentic-docs/agent-memory.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/agent-memory.md).

## What it is

A directory per agent, holding markdown notes:

```
.claude/agent-memory/
├── README.md                      explains the convention
├── <agent-name>/
│   ├── <topic>.md                 free-form notes, descriptive filenames
│   └── <topic>.md
└── <agent-name>/
    └── ...
```

The agent's own definition (`.claude/agents/<name>.md`) names the agent's responsibilities; the agent-memory directory holds **state** the agent accumulates over time.

`memory` is a real Claude Code agent frontmatter field. It takes `project`, `user`, or `local`, and it is optional — most agents omit it. An agent that declares `memory: project` auto-reads `.claude/agent-memory/<its-own-name>/` at the start of each session. In this repo the stateful specialists (`sanitization-auditor`, `runtime-architect`, `framework-docs-author`, `docs-currency-auditor`) declare it; the rest don't, because they have no state worth carrying.

## What goes in agent memory

- **Decisions made.** "We chose option A for cursor encoding because option B failed the load test." Saves having the same debate twice.
- **Open TODOs the agent owns.** "Still need to validate index plan in eu-west-1 staging."
- **Where the agent left off.** "Tasks 5–8 done; task 9 in flight; tasks 10+ blocked on Q2 resolution."
- **Cross-agent coordination.** "I have the lock on `src/services/users/search/`; another implementer should not touch this until task 10 lands."
- **Pointers to authoritative external state.**

## What does NOT go in agent memory

These directories are tracked. Do not write:

- **Private project names, customer data, or internal identifiers.** Same sanitization bar as any other tracked file. See [[Sanitization]].
- **Live secrets or credentials.**
- **Information that belongs in a real artifact.** If it's "this PRD said X," update the PRD.
- **Per-conversation working state.** Use task lists for that, not memory.
- **User-level preferences.** Those go in user-level memory at `~/.claude/projects/<flattened-project-path>/memory/`, outside the repo.
- **Anything that names the user-level memory directory** — its absolute path, or the filenames inside it. Both disclose more than they look like they do; write a placeholder and derive the real path at use time. See [[Sanitization]].

## Lifecycle

- **Create** when the agent first needs persistent state. Most agents don't.
- **Read** at the start of every conversation involving the agent. Treat as authoritative.
- **Update** inline when a decision lands, a TODO closes, or coordination state changes. **Not a log.**
- **Prune** when content becomes stale.

## Two layers: project vs user memory

| Layer | Path | Tracked? | Use for |
|---|---|---|---|
| **Project agent memory** | `.claude/agent-memory/<agent-name>/` | Yes | Shared agent state ships with the project |
| **User-level memory** | `~/.claude/projects/<flattened-project-path>/memory/` | No | Per-developer personal context |

Claude Code derives the flattened segment from the repo path by replacing `/` with `-`, so it differs per machine. Never hard-code it into a tracked file.

## Reference implementations

This repo's `.claude/agent-memory/` has working examples for the most stateful implementation agents:

- [`sanitization-auditor/checklist.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/agent-memory/sanitization-auditor/checklist.md) — sanitization wordlist + audit protocol; explicit "intentional placeholders" list.
- [`runtime-architect/vendor-matrix-progress.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/agent-memory/runtime-architect/vendor-matrix-progress.md) — vendor-by-vendor build-out state.
- [`framework-docs-author/docs-status.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/agent-memory/framework-docs-author/docs-status.md) — drafting progress for `agentic-docs/`.

## When agent memory is *not* the right tool

- **Project-wide context all agents need** → `AGENTS.md` (always loaded).
- **Specific PRDs or specs** → `prds/` or `specs/`, not agent memory.
- **Ephemeral conversation state** → conversation's own task list (TaskCreate / TaskUpdate).
- **Knowledge an agent should always know** → the agent's own `.md` body.

Agent memory is specifically for state the agent **accumulates over time** that a fresh agent definition wouldn't carry.

## Vendor support

All six supported vendors now ship subagents, but **persistent per-agent memory is a separate capability** and is not part of that converged set. Native support is still asymmetric:

| Vendor | Native agent-memory support | Workaround |
|---|---|---|
| Claude Code | Yes — an agent auto-reads `.claude/agent-memory/<agent-name>/` when its frontmatter declares `memory: project` (or `user` / `local`) | n/a |
| Codex | Partial — per-agent context via the agent's TOML | Surface key state in the agent's `developer_instructions` |
| Gemini CLI | No native per-agent memory | Use `GEMINI.md` references for project-wide state |
| Kiro | Steering files act as cross-conversation memory | Use `.kiro/steering/` with `inclusion: always` |
| Cursor | No native per-agent memory | Use `.cursor/rules/*.mdc` with `alwaysApply: true` |
| Devin Desktop | No native persistent per-agent memory | Use `AGENTS.md` or `.devin/rules/`; Cascade also accepts `.windsurf/rules/` |

For vendors without native support, surface the same content via the vendor's rule or context-file mechanism.

## Anti-patterns

- **Logging every conversation** — unreadable noise. Update inline.
- **Putting team conventions in memory** — conventions go in `AGENTS.md` or `rules/`.
- **Letting memory get stale** — prune.
- **Cross-pollinating between agents** — share via `AGENTS.md`, not by writing to each other's memory.

## See also

- [[Implementation Team]] — the agents whose memory directories live here
- [[Multi-Vendor Context Files]] — how per-vendor memory mechanisms compare
- [[Rules]] — content standards
