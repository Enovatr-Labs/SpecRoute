# `.cursor/skills/`

Cursor Agent Skills (the Agent Skills open standard). Each skill is a folder containing a `SKILL.md` under `.cursor/skills/<slug>/SKILL.md` (project scope) or `~/.cursor/skills/<slug>/SKILL.md` (user scope).

## Layout

```
.cursor/skills/
└── <slug>/
    └── SKILL.md                      frontmatter + multi-step workflow body
```

## Frontmatter contract

```yaml
---
name: audit-artifact       # optional; skill identifier
description: <what the skill does, with trigger phrases>
paths:                     # optional; glob patterns that scope when the skill applies
  - "specs/**/*.md"
---
```

All fields are optional; leave `paths` unset to make the skill universally available. The Markdown body holds the actual multi-step workflow.

| Field | Required | Notes |
|---|---|---|
| `name` | No | skill identifier; defaults from the folder name |
| `description` | No | include trigger phrases so the agent knows when to invoke |
| `paths` | No | glob patterns (e.g. `"**/*.tsx"`); restricts the skill to matching files |

## Invocation

- Type `/<slug>` in chat to invoke a skill.
- Use `@<slug>` to attach it as context.

## Notes

- Skills are multi-step, on-demand workflows - not always-on rules. Use [`../rules/`](../rules/) for short, always-on guidelines.
- Keep the body aligned with the Claude skill of the same slug; only the frontmatter shape differs (Cursor omits `argument-hint`, `user-invocable`, and `allowed-tools`).
