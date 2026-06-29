# `.devin/agents/`

Subagent profiles for **Devin Local** (the Rust harness that succeeds Cascade). Each subagent is a folder containing an `AGENT.md`; the folder name is the profile identifier.

> Cascade had no first-class subagents. Subagents require Devin Local. Devin also auto-imports Claude Code agents from `.claude/agents/*.md`, so a project with a populated `.claude/agents/` gets those subagents for free.

## Layout

```
.devin/agents/
└── <name>/
    └── AGENT.md                      one folder per subagent profile
```

## Frontmatter contract

```yaml
---
name: <profile-name>
description: <shown to the agent when selecting a profile>
model: sonnet
allowed-tools:
  - read
  - grep
  - glob
permissions:
  allow:
    - Read(**)
  ask:
    - Write(**)
max-nesting: 1
---
```

| Field | Notes |
|---|---|
| `name` | Defaults to the directory name; must not conflict with built-in profiles. |
| `description` | Shown to the agent when selecting a profile. |
| `model` | Optional; overrides the default subagent model. |
| `allowed-tools` | Restricts the subagent's tools. Claude Code's `tools` is also accepted. |
| `permissions` | Optional `allow` / `deny` / `ask` overrides. |
| `max-nesting` | Optional; lets this subagent spawn its own (default: cannot). |

By default a subagent cannot spawn further subagents - set `max-nesting` to opt in.

## Suggested agents

Mirror [`../../.claude/agents/`](../../.claude/agents/). The canonical example here is [`spec-reviewer/`](spec-reviewer/AGENT.md).
