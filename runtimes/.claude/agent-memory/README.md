# `.claude/agent-memory/`

Per-agent persistent context. Each subdirectory matches an agent's name (from `.claude/agents/<name>.md`) and holds free-form markdown notes the agent re-reads at the start of each conversation.

## Layout

```
.claude/agent-memory/
├── README.md                       (this file)
└── <agent-name>/
    └── <topic>.md                  free-form notes, descriptive filenames
```

## What goes in here

- **State that persists across conversations** but doesn't belong in the codebase: which decisions have been made, what TODOs the agent owns, where it left off.
- **Cross-agent coordination notes**: which agent has the lock on a shared file.
- **Pointers to authoritative external state** that lives outside the repo (user-level memory, external dashboards).

## What does NOT go in here

These files are tracked and ship as part of the project. Treat them with the same content bar as any other tracked file:

- No secrets or credentials.
- No proprietary domain logic.
- No customer or account data.
- Nothing that belongs in a real artifact (PRD, spec, doc) - write the artifact instead.

## Reference implementations

See the SpecRoute framework's own agent-memory at [`.claude/agent-memory/`](../../../.claude/agent-memory/) (relative to repo root):

- `sanitization-auditor/checklist.md` - pointer to the canonical sanitization wordlist + audit protocol.
- `runtime-architect/vendor-matrix-progress.md` - vendor matrix build-out state.
- `framework-docs-author/docs-status.md` - drafting progress and refresh triggers.

Use these as worked examples of the appropriate level of detail.
