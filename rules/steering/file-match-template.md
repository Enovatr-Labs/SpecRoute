---
inclusion: fileMatch
fileMatchPattern: "src/**/*.tsx"
---

# File-Pattern-Matched Rule: <Rule Title>

> **Steering rule template - file-pattern-matched inclusion.** This rule loads only when the user is working with files matching `fileMatchPattern`. Use to scope rules to specific contexts.
>
> Cursor analog: `globs: ["src/**/*.tsx"]` without `alwaysApply: true`.
> Devin Desktop Cascade analog: `trigger: glob` + `globs: "..."`.
> Claude Code / Codex / Gemini: not natively pattern-matched; surface via agent or skill scoping.

## When to use file-match

- Rules that apply only to certain languages (frontend `.tsx`, backend `.py`, infrastructure `.tf`).
- Rules that apply only to certain components (UI components, services, migrations).
- Domain-specific rules (auth-touching files, secrets-touching files, public-API files).

## Suggested patterns

| Domain | `fileMatchPattern` |
|---|---|
| Frontend | `src/**/*.tsx`, `src/**/*.jsx`, `src/components/**`, `src/pages/**` |
| Backend (Python) | `src/services/**/*.py`, `src/**/*.py` |
| Backend (Node) | `src/services/**/*.ts`, `src/api/**/*.ts` |
| Database | `migrations/**/*.sql`, `**/*schema*.{ts,py,sql}` |
| Infrastructure | `infra/**/*.tf`, `k8s/**/*.yaml`, `docker-compose*.yml` |
| Documentation | `*.md`, `docs/**/*.md` |
| Secrets-touching | `*secret*`, `*vault*`, `*eso*` |

## Body

<2–3 paragraphs of the rule. Specific to the matched files.>

## Examples

```
TODO: concrete examples of the rule applied to matching files
```

## See also

- <related rule files>

---

## How to fill this template

1. Set `inclusion: fileMatch` in frontmatter.
2. Set `fileMatchPattern` to the glob the rule applies to.
3. Replace the title.
4. Write the body - specific to the matched file context.
5. Drop into `.kiro/steering/<name>.md` or mirror into the equivalent for your vendor (Cursor `.cursor/rules/<name>.mdc`, etc.).
