# `.windsurf/` - Windsurf runtime layout (legacy)

> **Now Devin Desktop.** Windsurf was acquired by Cognition and relaunched as Devin Desktop (2026-06-02). Cascade reaches end of life on **2026-07-01**; its successor is **Devin Local** (a Rust rewrite that supports subagents). Devin reads **both** locations, but `.devin/` is the current read+write layout and takes precedence; `.windsurf/` is a legacy read-only fallback. **For new projects, use [`../.devin/`](../.devin/).** This directory is retained for Cascade installs during the transition.

Drop this directory into the root of your project. Windsurf/Cascade reads from these paths.

## Layout

```
.windsurf/
├── rules/
│   └── <name>.md                    rule files
├── skills/
│   └── <slug>/SKILL.md              reusable multi-step procedures
├── workflows/
│   └── <name>.md                    slash commands, invoked /<name>
└── hooks.json                       (optional) Cascade hooks - 12 events
```

## What Windsurf consumes

- **Rule files** under `.windsurf/rules/`. See [`rules/README.md`](rules/README.md).
- **Skills** under `.windsurf/skills/<slug>/SKILL.md`. See [`skills/README.md`](skills/README.md).
- **Workflows** (slash commands) under `.windsurf/workflows/<name>.md`, invoked `/<name>`. See [`workflows/README.md`](workflows/README.md).
- **Cascade hooks** in `.windsurf/hooks.json` (workspace) or `~/.codeium/windsurf/hooks.json` (user). 12 events: `pre_user_prompt`, `pre_read_code` / `post_read_code`, `pre_write_code` / `post_write_code`, `pre_run_command` / `post_run_command`, `pre_mcp_tool_use` / `post_mcp_tool_use`, `post_cascade_response`, `post_cascade_response_with_transcript`, `post_setup_worktree`. Only pre-hooks block. See [`hooks/windsurf/`](../../hooks/windsurf/) for the template.

Rules carry ongoing context; workflows are user-invokable slash commands; skills are reusable multi-step procedures; Cascade hooks handle event-driven automation.

## MCP

Windsurf reads MCP servers from `~/.codeium/windsurf/mcp_config.json` (user-level, `mcpServers` JSON). Maintain [`../mcp/servers.yaml`](../mcp/servers.yaml) as the single source and render into that file.

## Setup

1. Create `.windsurf/rules/`, `.windsurf/skills/`, and `.windsurf/workflows/` in your repo.
2. Add rule, skill, and workflow files. See each subdirectory's README.
3. (Optional) Copy [`hooks/windsurf/hooks.template.json`](../../hooks/windsurf/hooks.template.json) to `.windsurf/hooks.json` and adapt the script paths. For Windows users, supply both `command` (bash) and `powershell` variants per hook.
4. Windsurf loads rules according to their trigger / glob configuration, registers workflows as `/<name>` slash commands, and fires hooks on their lifecycle events.

## Cross-referencing project rules

Mirror or copy from the project's `rules/` directory.

## Hook integration

The Windsurf hook merge order is: cloud (Enterprise dashboard) → system (`/Library/Application Support/Windsurf/hooks.json` etc.) → user → workspace. Hooks at later layers run after earlier layers. Only **pre-hooks** are blockable - exit code 2 from a `pre_*` hook stops the action; the same exit code from a `post_*` hook is treated as a warning. See [`hooks/windsurf/scripts/README.md`](../../hooks/windsurf/scripts/README.md) for the protocol summary.
