# `.cursor/rules/`

Cursor rule files. Cursor consumes `*.mdc` (Markdown with Cursor-specific frontmatter) under `.cursor/rules/`.

## Layout

```
.cursor/rules/
├── <rule-name>.mdc                  always-on or context-aware rule
└── <rule-name>.mdc
```

## Frontmatter contract

```yaml
---
description: <brief description of the rule>
globs:
  - "src/**/*.tsx"      # optional; if present, rule applies only to matching files
alwaysApply: true        # set to true for always-on; false (default) for context-aware
---
```

When `alwaysApply: true`, the rule is loaded into every Cursor conversation. When `globs` is set without `alwaysApply: true`, the rule is loaded only when the user is working with a matching file.

## Suggested files

Mirror the project's `rules/` content into Cursor MDC files:

| File | alwaysApply | Globs |
|---|---|---|
| `coding-preferences.mdc` | true | (none) |
| `engineering-rules.mdc` | true | (none) |
| `security-rules.mdc` | true | (none) |
| `frontend.mdc` | false | `src/**/*.tsx`, `src/**/*.ts` |
| `backend.mdc` | false | `src/services/**/*.py` |

## Source content

Rule body content can be sourced from `rules/<topic>-rules.md`. Either copy directly with the MDC frontmatter prepended, or maintain Cursor-specific phrasing if helpful.

See [`../../../rules/cursor-rules.md`](../../../rules/cursor-rules.md) for vendor-specific guidance.
