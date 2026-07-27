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

The example above deliberately shows every field. Only `name` and `description` are required - that is the Agent Skills standard (`agentskills.io`) minimum, which Devin implements. `allowed-tools` is strongly recommended so the skill declares its own surface. `model`, `subagent`, `agent`, `permissions`, and `triggers` are optional; `triggers` defaults to `[user, model]`.

## Suggested skills

Mirror [`../../.claude/skills/`](../../.claude/skills/). The canonical example here is [`audit-artifact/`](audit-artifact/SKILL.md).

## Invoking a skill

Invoke Devin Local skills by filename:

```
/all-hands review the changes
```

The folder name is the `/skill-name` identifier. Devin Local also discovers
`.agents/skills/` and can invoke a skill autonomously when `triggers` includes
`model`.
