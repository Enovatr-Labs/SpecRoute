# `.devin/rules/`

Devin rule files - always-on instructions and context that guide the agent in every session. Devin consumes `*.md` under `.devin/rules/`.

## Layout

```
.devin/rules/
├── <rule-name>.md                   rule files (markdown, optional frontmatter)
└── <rule-name>.md
```

## Frontmatter contract

```yaml
---
description: <brief description>
trigger: always | manual | model-decision
globs:
  - "src/**/*.tsx"
---
```

`trigger: always` rules load in every session; `model-decision` rules load when relevant to the glob; `manual` rules load on request.

## Suggested files

Mirror `rules/` content. Common patterns:

| File | Trigger |
|---|---|
| `spec-driven-workflow.md` | always |
| `coding-preferences.md` | always |
| `engineering-rules.md` | always |
| `security-rules.md` | always |
| `frontend.md` | model-decision (with appropriate globs) |
| `backend.md` | model-decision |

The canonical example here is [`spec-driven-workflow.md`](spec-driven-workflow.md). See [`../../../rules/windsurf-rules.md`](../../../rules/windsurf-rules.md) for vendor-specific guidance.
