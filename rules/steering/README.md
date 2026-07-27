# Steering Rule Templates

Templates for the two rule-loading modes that several vendors support: always-on and file-pattern-matched.

```
rules/steering/
├── README.md                       (this file)
├── always-on-template.md           inclusion: always
└── file-match-template.md          inclusion: fileMatch + fileMatchPattern
```

## Inclusion modes

| Mode | Loaded when | Suitable for |
|---|---|---|
| **Always-on** | Every conversation | Cross-cutting standards, sanitization, project-wide invariants |
| **File-pattern-matched** | User works with matching files | Per-language, per-domain, per-component rules |

Use always-on sparingly - every always-on rule consumes context budget. Most rules should be file-pattern-matched.

## Vendor mapping

The two modes appear in different vendors with different frontmatter:

| Vendor | Always-on syntax | File-match syntax |
|---|---|---|
| Kiro | `inclusion: always` | `inclusion: fileMatch` + `fileMatchPattern: "..."` |
| Cursor (MDC) | `alwaysApply: true` | `globs: ["..."]` (without `alwaysApply`) |
| Devin Desktop (Cascade rules) | `trigger: always_on` | `trigger: glob` + `globs: "..."` |
| Claude Code | `CLAUDE.md` references | per-agent `description` triggers |
| Codex | `AGENTS.md` references | per-agent / per-skill scoping |
| Gemini | `GEMINI.md` references | not supported natively |

## How to use these templates

1. Decide whether your rule is always-on or file-pattern-matched.
2. Copy the appropriate template.
3. Adjust frontmatter for your target vendor (use the table above).
4. Drop into `.kiro/steering/`, `.cursor/rules/`, or `.devin/rules/` as appropriate.
5. For Claude Code / Codex / Gemini, surface the rule by linking from the root context file.

## See also

- [`runtimes/.kiro/steering/README.md`](../../runtimes/.kiro/steering/README.md) - Kiro steering layout.
- [`runtimes/.cursor/rules/README.md`](../../runtimes/.cursor/rules/README.md) - Cursor rules layout.
- [`runtimes/.devin/rules/README.md`](../../runtimes/.devin/rules/README.md) - Cascade-facing rules within the Devin Desktop layout.
- [`../engineering-rules.md`](../engineering-rules.md) - vendor-neutral engineering rules.
