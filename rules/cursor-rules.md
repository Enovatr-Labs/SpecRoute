# Cursor-specific Rules

How rules are loaded into Cursor. Rule content itself defers to the vendor-neutral rule files in this directory.

## Where Cursor looks

- **`.cursor/rules/*.mdc`** - Cursor MDC (Markdown with frontmatter) rule files. The integration surface.
- **`AGENTS.md`** at the repo root - natively read for general project context.

> **`.cursorrules` is gone.** The single-file root format is absent from Cursor's documentation entirely and is reported non-functional in current versions. Treat it as **removed in practice**, not "legacy but working": do not author one, and if a repo still has one, migrate its content into `.cursor/rules/*.mdc` (or `AGENTS.md`) rather than assuming it is still read.

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
| `.cursorrules` | Removed in practice - undocumented and reported non-functional. Migrate to `.cursor/rules/*.mdc`. |
| Skills | Folder-per-skill `SKILL.md` under `.cursor/skills/<slug>/`, following the Agent Skills standard (`name` + `description`). Cursor does not use Claude's `argument-hint` / `user-invocable` / `allowed-tools` extensions. |
| Subagents | Flat agent files under `.cursor/agents/<name>.md`. All frontmatter fields are optional; `name` defaults to the filename. |
| Slash commands | Markdown files under `.cursor/commands/<slug>.md`. |
| Hooks via `.cursor/hooks.json` | 21 lifecycle events in **camelCase** (`sessionStart`/`sessionEnd`, `preToolUse`/`postToolUse`, `beforeShellExecution`, `beforeMCPExecution`, `beforeReadFile`, `afterFileEdit`, `beforeSubmitPrompt`, `stop`, plus Tab-flow events) with a `permission` / `decision` schema. Both `command` and `prompt` (LLM-evaluated) hook types. See [`hooks/cursor/`](../hooks/cursor/). |
| `failClosed` per hook | Default fail-open: hook errors don't block. Set `failClosed: true` per hook entry for security-critical gates. |
| Plugins / marketplace | Cursor packages rules, skills, subagents, commands, hooks, and MCP servers as installable plugins. A plugin is a distribution mechanism for the same artifacts described here - not a new artifact type. See [`agentic-docs/cross-vendor-sync.md`](../agentic-docs/cross-vendor-sync.md). |

Only `.cursor/rules/*.mdc` is a *rule* surface; the rest of that table exists because "where do my standards live in Cursor" now has more than one right answer. A standard that must gate an action belongs in a hook, not a rule.

## See also

- [`engineering-rules.md`](engineering-rules.md) - vendor-neutral engineering rules.
- [`runtimes/.cursor/README.md`](../runtimes/.cursor/README.md) - Cursor runtime layout.
- [`steering/file-match-template.md`](steering/file-match-template.md) - file-pattern-matched rule template (similar concept across Cursor / Kiro).
