# Kiro-specific Rules

How rules are loaded into Kiro. Rule content itself defers to the vendor-neutral rule files in this directory.

## Where Kiro looks

Kiro's equivalent of "rules" is **steering** - Markdown files under `.kiro/steering/` whose frontmatter declares when they load. Unlike Cursor/Windsurf rule files, steering files are Kiro's first-class always-on/contextual context mechanism.

- **`.kiro/steering/*.md`** - steering files. The integration surface.

## Frontmatter (inclusion modes)

```yaml
---
inclusion: always | fileMatch | manual | auto
fileMatchPattern: "src/**/*.tsx"      # required when inclusion: fileMatch
---
```

| `inclusion` | Effect |
|---|---|
| `always` | Loaded into every conversation. |
| `fileMatch` | Loaded only when the active file matches `fileMatchPattern`. |
| `manual` | Loaded only when referenced via `#name`. |
| `auto` | Kiro decides based on context. |

## Recommended file set

Mirror `rules/` content into `.kiro/steering/`:

| File | `inclusion` | `fileMatchPattern` |
|---|---|---|
| `coding-preferences.md` | always | (none) |
| `engineering-rules.md` | always | (none) |
| `security-rules.md` | always | (none) |
| `frontend.md` | fileMatch | `src/**/*.tsx` |
| `backend.md` | fileMatch | `src/services/**` |

## Source-of-truth strategy

The canonical rule content lives in `rules/`. Copy the rule body into the steering file with the appropriate `inclusion` frontmatter prepended. Kiro's loader reads what's in the steering file, not what's referenced.

## Skills, subagents, and MCP

As of Kiro 0.9 (2026-02-05) Kiro consumes more than steering:

- **Skills** follow the Agent Skills standard at `.kiro/skills/<slug>/SKILL.md` (progressive disclosure - only `name`/`description` load until invoked).
- **Subagents** live at `.kiro/agents/<name>.md` (frontmatter `name`, optional `description`, `tools`, `model`, `includeMcpJson`, `includePowers`).
- **Custom commands** are surfaced as skills invoked via `/skill` (plus `inclusion: manual` steering referenced with `#name`).
- **MCP servers** are configured at `.kiro/settings/mcp.json` (`mcpServers` JSON). Render it with `runtimes/mcp/render/render_kiro.py`.

## Hooks

Kiro hooks are `*.kiro.hook` JSON files (10 events: file create/save/delete, prompt submit, agent stop, pre/post tool, pre/post task, manual) with `askAgent` or `runCommand` actions. See [`hooks/kiro/examples/`](../hooks/kiro/examples/).

## See also

- [`engineering-rules.md`](engineering-rules.md) - vendor-neutral engineering rules.
- [`runtimes/.kiro/README.md`](../runtimes/.kiro/README.md) - Kiro runtime layout.
- [`steering/`](steering/) - file-pattern steering templates (shared concept with Cursor/Windsurf rules).
- [`hooks/README.md`](../hooks/README.md) - cross-vendor hook taxonomy.
