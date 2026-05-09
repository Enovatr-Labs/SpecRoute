# Cursor-specific Rules

How rules are loaded into Cursor. Rule content itself defers to the vendor-neutral rule files in this directory.

## Where Cursor looks

- **`.cursor/rules/*.mdc`** - Cursor MDC (Markdown with frontmatter) rule files. The integration surface.
- **`.cursorrules`** at the repo root - older Cursor rule format; still supported in many versions.

## MDC frontmatter

```yaml
---
description: <brief description>
globs:
  - "src/**/*.tsx"               # optional; rule applies to matching files only
alwaysApply: true                # optional; true = loaded into every conversation
---
```

| Field | Effect |
|---|---|
| `description` | Shown in Cursor's rule picker. |
| `globs` | When set without `alwaysApply: true`, the rule loads only when working with matching files. |
| `alwaysApply: true` | Always loaded, regardless of file context. Use sparingly - eats context budget. |

## Recommended file set

Mirror `rules/` content into `.cursor/rules/`:

| File | `alwaysApply` | `globs` |
|---|---|---|
| `coding-preferences.mdc` | true | (none) |
| `engineering-rules.mdc` | true | (none) |
| `security-rules.mdc` | true | (none) |
| `frontend.mdc` | false | `src/**/*.tsx`, `src/**/*.ts` |
| `backend.mdc` | false | `src/services/**/*.py` |
| `documentation.mdc` | false | `*.md`, `docs/**/*.md` |

## Source-of-truth strategy

The canonical rule content lives in `rules/`. For Cursor:

- **Option A**: copy the rule body into the MDC file with the appropriate frontmatter prepended. Re-sync on every change.
- **Option B**: keep MDC files thin, with `description: see ../../rules/<file>.md` and a one-line summary. Trade-off: less context loaded.

Option A is the recommended default - Cursor's loader reads what's in the MDC file, not what's referenced.

## Vendor-specific behaviors

| Topic | Cursor behavior |
|---|---|
| Rule precedence | When multiple rules match, Cursor merges them. Order is implementation-defined; don't rely on conflict resolution. |
| Glob patterns | `**` matches recursively; `*` matches one segment. Standard glob semantics. |
| `.cursorrules` (legacy) | Single file at repo root, no frontmatter. Use only for projects that haven't migrated to MDC. |
| Hooks via `.cursor/hooks.json` | ~19 lifecycle events (sessionStart/End, pre/postToolUse, beforeShell/MCP/Read, afterFileEdit, beforeSubmitPrompt, stop, plus Tab-flow events) with `permission` / `decision` schema. Both `command` and `prompt` (LLM-evaluated) hook types. See [`hooks/cursor/`](../hooks/cursor/). |
| `failClosed` per hook | Default fail-open: hook errors don't block. Set `failClosed: true` per hook entry for security-critical gates. |

## See also

- [`engineering-rules.md`](engineering-rules.md) - vendor-neutral engineering rules.
- [`runtimes/.cursor/README.md`](../runtimes/.cursor/README.md) - Cursor runtime layout.
- [`steering/file-match-template.md`](steering/file-match-template.md) - file-pattern-matched rule template (similar concept across Cursor / Kiro).
