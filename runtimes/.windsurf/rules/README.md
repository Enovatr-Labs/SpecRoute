# `.windsurf/rules/`

Windsurf rule files. Windsurf consumes `*.md` (or `*.mdc` in some configurations) under `.windsurf/rules/`.

## Layout

```
.windsurf/rules/
├── <rule-name>.md                   rule files (markdown, optional frontmatter)
└── <rule-name>.md
```

## Frontmatter contract

Windsurf's rule frontmatter conventions are similar to Cursor's. Common fields:

```yaml
---
description: <brief description>
trigger: always | manual | model-decision
globs:
  - "src/**/*.tsx"
---
```

Check your Windsurf version for the exact supported fields.

## Suggested files

Mirror `rules/` content. Common patterns:

| File | Trigger |
|---|---|
| `coding-preferences.md` | always |
| `engineering-rules.md` | always |
| `security-rules.md` | always |
| `frontend.md` | model-decision (with appropriate globs) |
| `backend.md` | model-decision |

See [`../../../rules/windsurf-rules.md`](../../../rules/windsurf-rules.md) for vendor-specific guidance.
