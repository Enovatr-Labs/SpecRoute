# `.cursor/` - Cursor runtime layout

Drop this directory into the root of your project. Cursor reads from these paths.

## Layout

```
.cursor/
├── rules/
│   └── <name>.mdc                   rule files with MDC frontmatter
├── agents/
│   └── <name>.md                    subagents (Markdown + frontmatter; since Cursor 2.4)
├── skills/
│   └── <slug>/SKILL.md              Agent Skills (open standard)
├── commands/
│   └── <name>.md                    custom commands (since Cursor 1.6)
├── hooks.json                       (optional) ~21 lifecycle hook events
└── mcp.json                         MCP server configuration (mcpServers object)
```

Cursor also natively reads `AGENTS.md` at the project root for ongoing context; `.cursorrules` is legacy/deprecated - use `rules/*.mdc` instead.

## What Cursor consumes

- **Rule files** (`*.mdc`) under `.cursor/rules/`, plus the project-root `AGENTS.md`. See [`rules/README.md`](rules/README.md).
- **Subagents** in `.cursor/agents/<name>.md`. See [`agents/README.md`](agents/README.md).
- **Skills** in `.cursor/skills/<slug>/SKILL.md`. See [`skills/README.md`](skills/README.md).
- **Commands** in `.cursor/commands/<name>.md`, invoked with `/<name>`. See [`commands/README.md`](commands/README.md).
- **Hooks** in `.cursor/hooks.json` (project) or `~/.cursor/hooks.json` (user). Cursor v1 ships ~21 lifecycle events including `sessionStart`, `preToolUse`, `beforeShellExecution`, `beforeReadFile`, `afterFileEdit`, `beforeSubmitPrompt`, `stop`, and Tab-flow events. See [`hooks/cursor/`](../../hooks/cursor/) for the template.
- **MCP servers** in `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (user). Same `mcpServers` JSON shape as Claude Desktop; rendered from [`runtimes/mcp/servers.yaml`](../mcp/servers.yaml).

Rules and `AGENTS.md` carry ongoing context; skills carry on-demand multi-step workflows; commands are deterministic prompt wrappers; subagents are delegated specialists; hooks handle event-driven automation.

## Setup

1. Create `.cursor/` in your repo with the subdirectories above.
2. Add `*.mdc` files under `rules/` for each rule. See [`rules/README.md`](rules/README.md) for the MDC frontmatter contract.
3. Add subagents, skills, and commands as needed, following the per-directory READMEs for the frontmatter contract.
4. Copy [`mcp.template.json`](mcp.template.json) to `.cursor/mcp.json` and adjust the filesystem root and any credentials (via env, not inline).
5. (Optional) Copy [`hooks/cursor/hooks.template.json`](../../hooks/cursor/hooks.template.json) to `.cursor/hooks.json` and adapt the script paths.
6. Cursor loads matching rules automatically when you work with files matching the rule's `globs`. Skills and commands are invoked on demand; hooks fire on their lifecycle events.

## Cross-referencing project rules

The project's `rules/` directory holds the canonical content. Mirror or copy into Cursor MDC files; the MDC format is the integration shape. Likewise, the consumer agent roster (`agents/`) and skills are the source of truth - the files under `.cursor/agents/` and `.cursor/skills/` adapt those to Cursor's native frontmatter.

## Hook integration

The hook config supports `permission`/`decision` semantics, `failClosed` per hook entry, prompt-typed hooks (LLM-evaluated conditions), and a Cursor-specific `loop_limit` for `stop` and `subagentStop` follow-ups. See [`hooks/cursor/scripts/README.md`](../../hooks/cursor/scripts/README.md) for the protocol summary and canonical script structure.
