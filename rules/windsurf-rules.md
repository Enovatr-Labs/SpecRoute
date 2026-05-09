# Windsurf-specific Rules

How rules are loaded into Windsurf. Rule content itself defers to the vendor-neutral rule files in this directory.

## Where Windsurf looks

- **`.windsurf/rules/*.md`** - Windsurf rule files. The integration surface.

## Frontmatter

Windsurf's rule frontmatter conventions are similar to Cursor's. Common fields:

```yaml
---
description: <brief description>
trigger: always | manual | model-decision
globs:
  - "src/**/*.tsx"
---
```

| Field | Effect |
|---|---|
| `trigger: always` | Loaded into every conversation (similar to Cursor's `alwaysApply: true`). |
| `trigger: model-decision` | The model decides whether to apply, typically based on file context. |
| `trigger: manual` | Loaded only when the user explicitly references the rule. |
| `globs` | Restricts rule applicability to matching files. |

Check your Windsurf version for the exact supported fields and triggers - they have evolved across releases.

## Recommended file set

Mirror `rules/` content into `.windsurf/rules/`:

| File | `trigger` | `globs` |
|---|---|---|
| `coding-preferences.md` | always | (none) |
| `engineering-rules.md` | always | (none) |
| `security-rules.md` | always | (none) |
| `frontend.md` | model-decision | `src/**/*.tsx` |
| `backend.md` | model-decision | `src/services/**` |

## Source-of-truth strategy

Same as Cursor - copy rule body into the Windsurf rule file (with appropriate frontmatter), or keep thin pointer files. Copying is the recommended default.

## Cascade Hooks

Windsurf supports event-triggered automation via Cascade hooks (`.windsurf/hooks.json`):

| Event | Blockable |
|---|---|
| `pre_user_prompt`, `pre_read_code`, `pre_write_code`, `pre_run_command`, `pre_mcp_tool_use` | Yes |
| `post_read_code`, `post_write_code`, `post_run_command`, `post_mcp_tool_use`, `post_cascade_response`, `post_cascade_response_with_transcript`, `post_setup_worktree` | No (observational) |

Each hook entry can specify both `command` (bash) and `powershell` (Windows fallback). The merge order is cloud (Enterprise dashboard) → system → user → workspace. See [`hooks/windsurf/`](../hooks/windsurf/) for the template.

## See also

- [`engineering-rules.md`](engineering-rules.md) - vendor-neutral engineering rules.
- [`runtimes/.windsurf/README.md`](../runtimes/.windsurf/README.md) - Windsurf runtime layout.
- [`cursor-rules.md`](cursor-rules.md) - analogous patterns for Cursor.
- [`hooks/README.md`](../hooks/README.md) - cross-vendor hook taxonomy.
