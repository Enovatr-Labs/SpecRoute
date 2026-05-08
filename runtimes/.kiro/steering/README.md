# `.kiro/steering/`

Steering rules — markdown files Kiro loads as context, either always or matching a file pattern.

## Inclusion modes

### Always-on

Frontmatter:

```yaml
---
inclusion: always
---
```

Loaded into every Kiro conversation. Use sparingly — these eat context budget. Reserve for true cross-cutting rules (engineering standards, security baseline, project structure).

See [`rules/steering/always-on-template.md`](../../../rules/steering/always-on-template.md) for the canonical template.

### File-pattern-matched

Frontmatter:

```yaml
---
inclusion: fileMatch
fileMatchPattern: "src/**/*.tsx"
---
```

Loaded only when the user is working with a file matching the pattern. Use for vertical-slice rules (frontend conventions, database conventions, secrets handling).

See [`rules/steering/file-match-template.md`](../../../rules/steering/file-match-template.md) for the template.

## Suggested files

Map your project's rules into steering files:

| Steering file | Inclusion | Loaded for |
|---|---|---|
| `engineering-rules.md` | always | every conversation |
| `code-review-rules.md` | always | every conversation |
| `security-rules.md` | always | every conversation |
| `documentation-rules.md` | fileMatch (`*.md`) | doc edits |
| `frontend-rules.md` | fileMatch (`src/components/**`, `src/pages/**`) | frontend edits |
| `backend-rules.md` | fileMatch (`src/services/**`) | backend edits |
| `secrets-management.md` | fileMatch (`*secret*`, `*vault*`, `*eso*`) | secrets-touching edits |

## Source content

The actual rule content can be sourced from `../../rules/`. Either copy the file content directly into a steering file (with the inclusion frontmatter prepended) or symlink. Copying is simpler; symlinks risk Kiro / cross-vendor weirdness.
