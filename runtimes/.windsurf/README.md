# `.windsurf/` - Windsurf runtime layout

Drop this directory into the root of your project. Windsurf reads from these paths.

## Layout

```
.windsurf/
├── rules/
│   └── <name>.md                    rule files
└── hooks.json                       (optional) Cascade hooks - 12 events
```

## What Windsurf consumes

- **Rule files** under `.windsurf/rules/`.
- **Cascade hooks** in `.windsurf/hooks.json` (workspace) or `~/.codeium/windsurf/hooks.json` (user). 12 events: `pre_user_prompt`, `pre_read_code` / `post_read_code`, `pre_write_code` / `post_write_code`, `pre_run_command` / `post_run_command`, `pre_mcp_tool_use` / `post_mcp_tool_use`, `post_cascade_response`, `post_cascade_response_with_transcript`, `post_setup_worktree`. Only pre-hooks block. See [`hooks/windsurf/`](../../hooks/windsurf/) for the template.

Windsurf does not have first-class skills, agents, or slash commands within the SpecRoute taxonomy. Rules carry ongoing context; Cascade hooks handle event-driven automation.

## Setup

1. Create `.windsurf/rules/` in your repo.
2. Add `*.md` files for each rule. See [`rules/README.md`](rules/README.md).
3. (Optional) Copy [`hooks/windsurf/hooks.template.json`](../../hooks/windsurf/hooks.template.json) to `.windsurf/hooks.json` and adapt the script paths. For Windows users, supply both `command` (bash) and `powershell` variants per hook.
4. Windsurf loads rules according to their trigger / glob configuration. Hooks fire on their lifecycle events.

## Cross-referencing project rules

Mirror or copy from the project's `rules/` directory.

## Hook integration

The Windsurf hook merge order is: cloud (Enterprise dashboard) → system (`/Library/Application Support/Windsurf/hooks.json` etc.) → user → workspace. Hooks at later layers run after earlier layers. Only **pre-hooks** are blockable - exit code 2 from a `pre_*` hook stops the action; the same exit code from a `post_*` hook is treated as a warning. See [`hooks/windsurf/scripts/README.md`](../../hooks/windsurf/scripts/README.md) for the protocol summary.
