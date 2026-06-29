# Devin-specific Rules

How rules are loaded into Devin Desktop (the relaunched Windsurf). Rule content itself defers to the vendor-neutral rule files in this directory.

## Where Devin looks

- **`.devin/rules/*.md`** - the current, preferred rule location (read + write).
- **`.windsurf/rules/*.md`** - legacy, read-only fallback. Devin reads both, with `.devin/` taking precedence. New rules should go in `.devin/rules/`.

Devin Desktop (June 2026 relaunch of Windsurf by Cognition) reads the same workspace shapes Windsurf did - `rules/`, `workflows/`, `skills/` - now rooted at `.devin/`. The Cascade local agent reaches end-of-life on 2026-07-01 and is succeeded by Devin Local (a Rust rewrite with subagent support).

## Frontmatter

Devin's rule frontmatter mirrors the legacy Windsurf conventions:

```yaml
---
description: <brief description>
trigger: always_on | manual | model-decision
globs:
  - "src/**/*.tsx"
---
```

| Field | Effect |
|---|---|
| `trigger: always_on` | Loaded into every conversation. |
| `trigger: model-decision` | The model decides whether to apply, typically based on file context. |
| `trigger: manual` | Loaded only when the user explicitly references the rule. |
| `globs` | Restricts rule applicability to matching files. |

Check your Devin version for the exact supported fields - they inherit from Windsurf and continue to evolve.

## Recommended file set

Mirror `rules/` content into `.devin/rules/`:

| File | `trigger` | `globs` |
|---|---|---|
| `coding-preferences.md` | always_on | (none) |
| `engineering-rules.md` | always_on | (none) |
| `security-rules.md` | always_on | (none) |
| `frontend.md` | model-decision | `src/**/*.tsx` |
| `backend.md` | model-decision | `src/services/**` |

## Source-of-truth strategy

Same as Cursor / Windsurf - copy the rule body into the Devin rule file (with appropriate frontmatter), or keep thin pointer files. Copying is the recommended default.

## Subagents, skills, and workflows

Devin Local goes beyond rules:

- **Subagents** live at `.devin/agents/<name>/AGENT.md` (per-profile directories). Devin also auto-imports Claude Code agents from `.claude/agents/*.md`.
- **Skills** follow the Agent Skills standard at `.devin/skills/<slug>/SKILL.md`.
- **Workflows** (`.devin/workflows/<name>.md`, invoked `/<name>`) are Devin's custom-command equivalent.

## Hooks and MCP

- Cascade/Devin hooks (`hooks.json`, 12 events; only `pre_*` hooks block) carry over from Windsurf. See [`hooks/windsurf/`](../hooks/windsurf/) for the template.
- MCP servers are configured at the user-level path `~/.codeium/windsurf/mcp_config.json` (`mcpServers` JSON). Render it from the canonical inventory with `runtimes/mcp/render/render_windsurf.py`.

## See also

- [`engineering-rules.md`](engineering-rules.md) - vendor-neutral engineering rules.
- [`runtimes/.devin/README.md`](../runtimes/.devin/README.md) - Devin runtime layout.
- [`windsurf-rules.md`](windsurf-rules.md) - the legacy Windsurf conventions Devin inherits.
- [`hooks/README.md`](../hooks/README.md) - cross-vendor hook taxonomy.
