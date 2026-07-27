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

## Invoking a skill

Use your runtime's skill prefix. In Claude Code both work once the skill is registered:

```
/all-hands review the changes        # skill/command menu
@all-hands review the changes        # mention picker - lists files AND registered skills
```

A correctly registered skill appears in the `@` picker with type **Skill**. If you see only
directories and no `Skill` row, it did not register - and the cause is almost always
frontmatter:

- **`disable-model-invocation: true` hides it** from the model-facing registry the `@` picker
  completes against. Omit it unless you want the skill reachable *only* from the `/` menu.
- **`allowed-tools` is comma-separated** (`Read, Grep, Glob, Bash, Agent`). Space separation
  and stale tool names (`Task` was superseded by `Agent`) fail silently.
- **The folder name must equal the `name` field.**

Each skill's `SKILL.md` carries a per-runtime invocation table.
