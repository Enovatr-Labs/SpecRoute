# `.devin/agents/`

Custom subagent profiles for Devin Local. Custom profiles are experimental, so
verify the installed Devin release before depending on optional fields.

## Layout

```text
.devin/agents/
└── <name>/
    └── AGENT.md
```

The directory name is the profile identifier. `.agents/agents/<name>/AGENT.md`
is also supported.

## Frontmatter

```yaml
---
name: reviewer
description: Reviews changes for correctness and maintainability
model: sonnet
allowed-tools:
  - read
  - grep
  - glob
max-nesting: 1
---
```

`name` defaults to the directory name. `description`, `model`,
`allowed-tools`, and `max-nesting` are optional. `allowed-tools` restricts the
subagent's tools. Nested spawning is disabled unless `max-nesting` opts in.

The canonical example is [`spec-reviewer/AGENT.md`](spec-reviewer/AGENT.md).
