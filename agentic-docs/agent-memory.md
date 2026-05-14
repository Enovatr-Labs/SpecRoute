# Agent Memory

Per-agent persistent context that survives across conversations. Agents that maintain state - open TODOs, decisions made, where they left off - write notes that they re-read at the start of each session.

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

The agent's own definition (`.claude/agents/<name>.md`) names the agent's responsibilities; the agent-memory directory holds *state* the agent accumulates over time.

## What goes in agent memory

Good candidates:

- **Decisions made.** "We chose option A for cursor encoding because option B failed the load test." Saves having the same debate twice.
- **Open TODOs the agent owns.** "Still need to validate index plan in eu-west-1 staging."
- **Where the agent left off.** "Tasks 5–8 done; task 9 in flight; tasks 10+ blocked on Q2 resolution."
- **Cross-agent coordination.** "I have the lock on `src/services/users/search/`; another implementer should not touch this until task 10 lands."
- **Pointers to authoritative external state.** "The forbidden-strings list is at `.claude/.forbidden-strings.txt`; this file is gitignored, repopulate from `~/.claude/projects/.../memory/specroute_public_release.md` if missing."

## What does NOT go in agent memory

These directories are tracked. They ship with the project and persist publicly. Do not write:

- **Private project names, customer data, or internal identifiers.** Same sanitization bar as any other tracked file.
- **Live secrets or credentials.**
- **Information that belongs in a real artifact.** If it's "this PRD said X," update the PRD or write the spec - don't note it in agent memory.
- **Per-conversation working state.** Use task lists for that, not memory.
- **User-level preferences.** Those go in user-level memory at `~/.claude/projects/<project>/memory/`, which is outside the repo.

## Lifecycle

- **Create** when the agent first needs persistent state. Most agents don't need any; create the directory only when there's content for it.
- **Read** at the start of every conversation that involves the agent. Treat as authoritative.
- **Update** whenever a decision lands, a TODO closes, or coordination state changes. Write the update inline rather than appending - this isn't a log.
- **Prune** when content becomes stale. A note from six months ago that's no longer relevant is noise; delete it.

## Two layers: project vs user memory

| Layer | Path | Tracked? | Use for |
|---|---|---|---|
| **Project agent memory** | `.claude/agent-memory/<agent-name>/` | Yes | Project-scoped state ships with the project; visible to all contributors |
| **User-level memory** | `~/.claude/projects/<project>/memory/` | No | User-scoped state stays local; per-developer preferences and local-only sanitization rules |

The project layer is for shared agent state that the team collectively benefits from. The user layer is for personal context (e.g. "I'm Chika, my role is X") that doesn't belong in the team's tracked files.

## Reference implementations

This repo's `.claude/agent-memory/` directory has working examples for the most stateful implementation agents:

- [`sanitization-auditor/checklist.md`](../.claude/agent-memory/sanitization-auditor/checklist.md) - pointer to the canonical sanitization wordlist + audit protocol; explicit "intentional placeholders" list to avoid false positives.
- [`runtime-architect/vendor-matrix-progress.md`](../.claude/agent-memory/runtime-architect/vendor-matrix-progress.md) - vendor-by-vendor build-out state: which runtime layouts are wired, which features are TODO, suggested build order.
- [`framework-docs-author/docs-status.md`](../.claude/agent-memory/framework-docs-author/docs-status.md) - drafting progress for `agentic-docs/`, refresh triggers when the matrix changes.

Read these as worked examples of the appropriate level of detail.

## When agent memory is *not* the right tool

- **For project-wide context all agents need**: that goes in `AGENTS.md` (always loaded).
- **For specific PRDs or specs**: they live in `prds/` or `specs/`, not in agent memory.
- **For ephemeral conversation state**: use the conversation's own task list (TaskCreate / TaskUpdate), not memory.
- **For knowledge an agent should always know**: put it in the agent's own `.md` file's operating principles.

Agent memory is specifically for state the agent **accumulates over time** that a fresh agent definition wouldn't carry.

## Vendor support

| Vendor | Native agent-memory support | Workaround |
|---|---|---|
| Claude Code | Yes - agents auto-read `.claude/agent-memory/<agent-name>/` if their frontmatter declares `memory: project` or `memory: user` | n/a |
| Codex | Partial - depends on Codex version; some support per-agent context | Surface key state from agent memory in the agent's own `.md` body |
| Gemini CLI | No native support | Use `GEMINI.md` references for project-wide state |
| Kiro | Steering files act as cross-conversation memory | Use `.kiro/steering/` with `inclusion: always` |
| Cursor / Windsurf | No native support | Use rules with `alwaysApply: true` |

For vendors without native support, the SpecRoute convention is to surface the same content via the vendor's rule or context-file mechanism.

## Anti-patterns

- **Logging every conversation in agent memory.** It becomes unreadable noise. Update inline, don't append.
- **Putting team conventions in agent memory.** Conventions go in `AGENTS.md` or `rules/`. Agent memory is for what *changes*.
- **Letting memory get stale.** A six-month-old note about "current state" is misleading. Prune.
- **Cross-pollinating between agents.** If two agents need to share state, surface it in `AGENTS.md` (always loaded) or a shared doc, not by both writing to each other's memory.

## Authoring agent

The pattern itself is owned by `framework-docs-author`. Each individual agent's memory is owned by that agent.

## See also

- [`.claude/agent-memory/README.md`](../.claude/agent-memory/README.md) - directory-level guidance with reference implementations.
- [`runtimes/.claude/agent-memory/README.md`](../runtimes/.claude/agent-memory/README.md) - consumer-facing template.
- [`rules/documentation-rules.md`](../rules/documentation-rules.md) - broader doc standards.
