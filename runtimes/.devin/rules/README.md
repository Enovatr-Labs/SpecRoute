# `.devin/rules/`

Cascade-compatible rule files for Devin Desktop. Devin Local uses `AGENTS.md`
as its recommended project rules mechanism; Cascade reads `*.md` under
`.devin/rules/`.

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
trigger: glob
globs:
  - "src/**/*.tsx"
---
```

Valid triggers are `always_on`, `model_decision`, `glob`, and `manual`.
`always_on` loads every time, `model_decision` lets the agent decide, `glob`
activates on matching files, and `manual` requires an explicit mention. Use
`globs` only with `trigger: glob`.

## Suggested files

Mirror `rules/` content. Common patterns:

| File | Trigger |
|---|---|
| `spec-driven-workflow.md` | always_on |
| `coding-preferences.md` | always_on |
| `engineering-rules.md` | always_on |
| `security-rules.md` | always_on |
| `frontend.md` | glob (with appropriate globs) |
| `backend.md` | model_decision |

The canonical example here is [`spec-driven-workflow.md`](spec-driven-workflow.md).
See [`../../../rules/devin-rules.md`](../../../rules/devin-rules.md) for
Devin Desktop guidance.
