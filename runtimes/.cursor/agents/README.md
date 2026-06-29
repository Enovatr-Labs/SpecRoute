# `.cursor/agents/`

Cursor subagents (since Cursor 2.4). Each subagent is a Markdown file with YAML frontmatter under `.cursor/agents/<name>.md` (project scope) or `~/.cursor/agents/<name>.md` (user scope). Project definitions take precedence.

## Layout

```
.cursor/agents/
├── <name>.md                         subagent: frontmatter + prompt body
└── <name>.md
```

## Frontmatter contract

```yaml
---
name: spec-reviewer        # optional; defaults to the filename. Lowercase + hyphens.
description: <when to delegate to this subagent, with trigger phrases>
model: inherit             # optional; `inherit` (default) or a specific model ID
readonly: true             # optional; true blocks file edits and shell writes
is_background: false        # optional; true runs the subagent as a background task
---
```

All fields are optional. The body after the frontmatter is the subagent's system prompt.

| Field | Required | Default | Values |
|---|---|---|---|
| `name` | No | filename | lowercase letters and hyphens |
| `description` | No | — | any string; include trigger phrases so Cursor knows when to delegate |
| `model` | No | `inherit` | `inherit` or a specific model ID |
| `readonly` | No | `false` | `true` / `false` |
| `is_background` | No | `false` | `true` / `false` |

## Notes

- This mirrors the consumer agent roster under `agents/`. Keep the body content aligned with the Claude agent of the same name; only the frontmatter shape differs.
- Use `readonly: true` for review-only roles (like `spec-reviewer`) so the subagent cannot mutate the working tree.
- See [`agents/roster.md`](../../../agents/roster.md) for the cross-vendor agent inventory.
