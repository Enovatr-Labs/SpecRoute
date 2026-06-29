# `.windsurf/skills/`

> **Legacy.** Windsurf is now Devin Desktop. Devin reads `.devin/skills/` in preference to this directory; `.windsurf/skills/` is a read-only fallback retained for Cascade installs until EOL (2026-07-01). New skills belong under [`../../.devin/skills/`](../../.devin/skills/).

Skills are reusable, multi-step procedures Cascade can invoke. Each skill is a folder containing a `SKILL.md`.

## Layout

```
.windsurf/skills/
└── <slug>/
    └── SKILL.md                      one folder per skill
```

## Frontmatter contract

```yaml
---
name: <slug>
description: <what it does; shown in completions>
argument-hint: "[path] [options]"
allowed-tools:
  - read
  - grep
  - glob
  - exec
---
```

`model`, `subagent`, `agent`, `permissions`, and `triggers` are also supported. The folder name is the invocation identifier.

## Suggested skills

Mirror [`../../.claude/skills/`](../../.claude/skills/). The canonical example here is [`audit-artifact/`](audit-artifact/SKILL.md).
