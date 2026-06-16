# `.devin/skills/`

Skills are reusable, multi-step procedures Devin can invoke. Each skill is a folder containing a `SKILL.md`; the folder name is the invocation identifier.

## Layout

```
.devin/skills/
└── <slug>/
    └── SKILL.md                      one folder per skill
```

## Frontmatter contract

```yaml
---
name: <slug>
description: <what it does; shown in completions>
argument-hint: "[path] [options]"
model: sonnet
subagent: true
allowed-tools:
  - read
  - grep
  - glob
  - exec
permissions:
  allow:
    - Read(src/**)
  ask:
    - Write(**)
triggers:
  - user
  - model
---
```

`name`, `description`, and `allowed-tools` are the core fields. `model`, `subagent`, `agent`, `permissions`, and `triggers` are optional. `triggers` defaults to `[user, model]`.

## Suggested skills

Mirror [`../../.claude/skills/`](../../.claude/skills/). The canonical example here is [`audit-artifact/`](audit-artifact/SKILL.md).
