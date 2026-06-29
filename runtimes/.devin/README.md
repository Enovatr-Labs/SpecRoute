# `.devin/` - Devin runtime layout (preferred)

> **Successor to `.windsurf/`.** Windsurf was relaunched as Devin Desktop (2026-06-02). Devin reads **both** `.devin/` and the legacy `.windsurf/`, but `.devin/` is the current **read+write** layout and takes precedence. Cascade reaches end of life on **2026-07-01**; its successor is **Devin Local** (a Rust rewrite that supports subagents). Use this directory for new projects; [`../.windsurf/`](../.windsurf/) is a read-only fallback retained for Cascade installs during the transition.

Drop this directory into the root of your project. Devin reads from these paths.

## Layout

```
.devin/
├── rules/
│   └── <name>.md                    always-on instructions and context
├── skills/
│   └── <slug>/SKILL.md              reusable multi-step procedures
├── agents/
│   └── <name>/AGENT.md              subagent profiles (Devin Local)
├── workflows/
│   └── <name>.md                    slash commands, invoked /<name>
└── plans/                           (Devin-managed) saved execution plans
```

## What Devin consumes

- **Rules** under `.devin/rules/` - always-on context. See [`rules/README.md`](rules/README.md).
- **Skills** under `.devin/skills/<slug>/SKILL.md`. See [`skills/README.md`](skills/README.md).
- **Subagents** under `.devin/agents/<name>/AGENT.md` (Devin Local). Devin also imports Claude Code agents from `.claude/agents/*.md`. See [`agents/README.md`](agents/README.md).
- **Workflows** (slash commands) under `.devin/workflows/<name>.md`, invoked `/<name>`. See [`workflows/README.md`](workflows/README.md).
- **Hooks** in `hooks.json` (12 events; only pre-hooks block). See [`hooks/windsurf/`](../../hooks/windsurf/) for the shared Cascade/Devin hook template.

## MCP

Devin/Windsurf reads MCP servers from `~/.codeium/windsurf/mcp_config.json` (user-level, `mcpServers` JSON). Maintain [`../mcp/servers.yaml`](../mcp/servers.yaml) as the single source and render into that file.

## Setup

1. Create `.devin/rules/`, `.devin/skills/`, `.devin/agents/`, and `.devin/workflows/` in your repo.
2. Add rule, skill, agent, and workflow files. See each subdirectory's README.
3. (Optional) Add `hooks.json` from the shared Cascade/Devin hook template.
4. Devin loads rules as always-on context, registers workflows as `/<name>` slash commands, makes subagents available for delegation, and fires hooks on their lifecycle events.

## Migration from `.windsurf/`

The two layouts are structurally parallel. To migrate: copy `.windsurf/rules/`, `.windsurf/skills/`, and `.windsurf/workflows/` to the matching `.devin/` directories, then add `.devin/agents/<name>/AGENT.md` profiles for any subagents (Devin Local only - Cascade had no first-class subagents). When both exist, `.devin/` wins.
