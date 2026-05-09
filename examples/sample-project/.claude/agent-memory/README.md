# `.claude/agent-memory/`

Per-agent persistent context. Each subdirectory matches an agent in [`../agents/`](../agents/) and holds free-form markdown notes the agent re-reads at the start of each conversation.

```
.claude/agent-memory/
├── README.md              (this file)
└── <agent-name>/          one directory per agent that maintains state
    └── <topic>.md         free-form notes; descriptive filenames
```

By default this directory is sparsely populated - agents create entries here as the project progresses (e.g. `backend-engineer/phase0-decisions.md`, `deployment-validator/rollout-progress.md`).

For the conceptual pattern - what to put here vs. in real artifacts - see [`../../agentic-docs/agent-memory.md`](../../agentic-docs/agent-memory.md).
