# `.cursor/` - Cursor runtime layout

Drop this directory into the root of your project. Cursor reads from these paths.

## Layout

```
.cursor/
├── rules/
│   └── <name>.mdc                   rule files with MDC frontmatter
└── hooks.json                       (optional) ~19 lifecycle hook events
```

## What Cursor consumes

- **Rule files** (`*.mdc`) under `.cursor/rules/`.
- **Hooks** in `.cursor/hooks.json` (project) or `~/.cursor/hooks.json` (user). Cursor v1.7+ ships ~19 lifecycle events including `sessionStart`, `preToolUse`, `beforeShellExecution`, `beforeReadFile`, `afterFileEdit`, `beforeSubmitPrompt`, `stop`, and Tab-flow events. See [`hooks/cursor/`](../../hooks/cursor/) for the template.

Cursor does not have first-class skills, agents, or slash commands within the SpecForge taxonomy. Rules carry ongoing context; hooks handle event-driven automation.

## Setup

1. Create `.cursor/rules/` in your repo.
2. Add `*.mdc` files for each rule. See [`rules/README.md`](rules/README.md) for the MDC frontmatter contract.
3. (Optional) Copy [`hooks/cursor/hooks.template.json`](../../hooks/cursor/hooks.template.json) to `.cursor/hooks.json` and adapt the script paths.
4. Cursor loads matching rules automatically when you work with files matching the rule's `globs`. Hooks fire on their lifecycle events.

## Cross-referencing project rules

The project's `rules/` directory holds the canonical content. Mirror or copy into Cursor MDC files; the MDC format is the integration shape.

## Hook integration

The hook config supports `permission`/`decision` semantics, `failClosed` per hook entry, prompt-typed hooks (LLM-evaluated conditions), and a Cursor-specific `loop_limit` for `stop` and `subagentStop` follow-ups. See [`hooks/cursor/scripts/README.md`](../../hooks/cursor/scripts/README.md) for the protocol summary and canonical script structure.
