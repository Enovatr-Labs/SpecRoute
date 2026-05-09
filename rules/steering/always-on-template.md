---
inclusion: always
---

# Always-On Rule: <Rule Title>

> **Steering rule template - always-on inclusion.** This rule loads into every Kiro conversation. Use sparingly - always-on rules consume context budget.
>
> Cursor analog: frontmatter `alwaysApply: true` (no `globs`).
> Windsurf analog: frontmatter `trigger: always`.
> Claude Code / Codex / Gemini: surface from `AGENTS.md` references.

## When to use always-on

- Cross-cutting rules that apply to every interaction (engineering standards, security baseline).
- Project-wide invariants (vendor matrix, branch strategy, environment naming).
- Sanitization rules - content that must never appear in tracked files.

Don't use always-on for:

- Per-language conventions - those are file-pattern matched.
- Per-domain rules (frontend vs backend) - those are file-pattern matched.
- Rules that only apply to a subset of work - those are file-pattern matched.

## Body

<2–3 paragraphs of the rule. Specific, actionable, terse.>

## Examples

```
TODO: concrete examples of the rule applied
```

## See also

- <related rule files>

---

## How to fill this template

1. Set `inclusion: always` in frontmatter.
2. Replace the title.
3. Write the body - concise, specific, project-specific.
4. Drop into `.kiro/steering/<name>.md` or mirror into the equivalent for your vendor.
