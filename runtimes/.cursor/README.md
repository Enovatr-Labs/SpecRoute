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
├── hooks/scripts/*.sh               shell scripts the hook entries invoke
└── mcp.json                         MCP server configuration (mcpServers object)
```

Note the split: Cursor reads the hook **config** from `.cursor/hooks.json`, but the **scripts** it
references live under `.cursor/hooks/scripts/`. A `hooks.json` placed inside `.cursor/hooks/` is
never read.

Cursor also natively reads `AGENTS.md` at the project root for ongoing context. `.cursorrules` should be treated as **removed**: it is absent from Cursor's current documentation and is reported non-functional in recent versions - use `rules/*.mdc` instead.

## What Cursor consumes

- **Rule files** (`*.mdc`) under `.cursor/rules/`, plus the project-root `AGENTS.md`. See [`rules/README.md`](rules/README.md).
- **Subagents** in `.cursor/agents/<name>.md`. See [`agents/README.md`](agents/README.md).
- **Skills** in `.cursor/skills/<slug>/SKILL.md`. See [`skills/README.md`](skills/README.md).
- **Commands** in `.cursor/commands/<name>.md`, invoked with `/<name>`. See [`commands/README.md`](commands/README.md).
- **Hooks** in `.cursor/hooks.json` (project) or `~/.cursor/hooks.json` (user), with their scripts in `.cursor/hooks/scripts/`. Cursor v1 ships ~21 camelCase lifecycle events including `sessionStart`, `preToolUse`, `beforeShellExecution`, `beforeReadFile`, `afterFileEdit`, `beforeSubmitPrompt`, `stop`, and Tab-flow events. A working set ships in [`hooks/`](hooks/); [`hooks/cursor/`](../../hooks/cursor/) is the annotated reference template.
- **MCP servers** in `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (user). Same `mcpServers` JSON shape as Claude Desktop; rendered from [`runtimes/mcp/servers.yaml`](../mcp/servers.yaml).

Rules and `AGENTS.md` carry ongoing context; skills carry on-demand multi-step workflows; commands are deterministic prompt wrappers; subagents are delegated specialists; hooks handle event-driven automation.

## Setup

1. Create `.cursor/` in your repo with the subdirectories above.
2. Add `*.mdc` files under `rules/` for each rule. See [`rules/README.md`](rules/README.md) for the MDC frontmatter contract.
3. Add subagents, skills, and commands as needed, following the per-directory READMEs for the frontmatter contract.
4. Copy [`mcp.template.json`](mcp.template.json) to `.cursor/mcp.json` and adjust the filesystem root and any credentials (via env, not inline).
5. Install the working hook set from [`hooks/`](hooks/):

   ```bash
   mkdir -p .cursor/hooks/scripts
   cp runtimes/.cursor/hooks/hooks.template.json .cursor/hooks.json
   cp runtimes/.cursor/hooks/scripts/*.sh        .cursor/hooks/scripts/
   chmod +x .cursor/hooks/scripts/*.sh

   printf '# One whitespace-free term per line.\n' > .cursor/.forbidden-strings.txt
   echo '.cursor/.forbidden-strings.txt' >> .gitignore
   ```

   That wires three hooks: a `sessionStart` orientation banner, a `beforeShellExecution`
   sanitization gate that blocks `git commit` / `git push` / `gh pr create` / `gh release create`
   while forbidden strings remain in tracked files, and an `afterFileEdit` frontmatter check.
   Cursor chooses the hook command's working directory by scope: project hooks run from the
   project root, while user hooks run from `~/.cursor/`. That is why the shipped project commands
   use `.cursor/hooks/scripts/...`; a user installation must use `./hooks/scripts/...`.

   **Blocking semantics**: exit `0` succeeds, exit `2` denies, and **anything else fails open** -
   the action proceeds. That default is Cursor's key difference from every other vendor here, so
   the sanitization gate sets `failClosed: true`; copy that flag onto any gate of your own. See
   [`hooks/README.md`](hooks/README.md) for which of the three defaults Cursor can express fully
   (`afterFileEdit` is observational, so the frontmatter warning reaches the hook log rather than
   the chat).
6. Cursor loads matching rules automatically when you work with files matching the rule's `globs`. Skills and commands are invoked on demand; hooks fire on their lifecycle events.

## Cross-referencing project rules

The project's `rules/` directory holds the canonical content. Mirror or copy into Cursor MDC files; the MDC format is the integration shape. Likewise, the consumer agent roster (`agents/`) and skills are the source of truth - the files under `.cursor/agents/` and `.cursor/skills/` adapt those to Cursor's native frontmatter.

## Hook integration

The hook config supports `permission`/`decision` semantics, `failClosed` per hook entry, prompt-typed hooks (LLM-evaluated conditions), and a Cursor-specific `loop_limit` for `stop` and `subagentStop` follow-ups. See [`hooks/README.md`](hooks/README.md) for the shipped set and its blocking behaviour, and [`hooks/cursor/scripts/README.md`](../../hooks/cursor/scripts/README.md) for the protocol summary and canonical script structure.
