# `.cursor/commands/`

Cursor custom commands (since Cursor 1.6). Each command is a Markdown file under `.cursor/commands/<name>.md` (project scope) or `~/.cursor/commands/<name>.md` (user scope). Invoke with `/<name>` in chat.

## Layout

```
.cursor/commands/
├── <name>.md                         optional frontmatter + prompt body
└── <name>.md
```

## Frontmatter contract

YAML frontmatter is optional. When present, `description` documents the command in the picker; the Markdown body is the prompt that runs.

```yaml
---
description: <one-line summary shown in the command picker>
---
```

The user's text after the invocation is appended to the prompt body, so reference it as "the path the user provides" rather than a named variable.

## Notes

- Commands are deterministic, user-invoked wrappers around a fixed workflow. For multi-step, model-driven workflows use [`../skills/`](../skills/) instead.
- Keep the body aligned with the Claude command of the same name; Cursor's command body has no `$ARGUMENTS` token, so phrase argument handling in prose.
