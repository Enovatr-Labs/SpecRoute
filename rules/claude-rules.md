# Claude Code-specific Rules

How rules and standards are loaded into Claude Code. Rules content itself defers to the vendor-neutral rule files in this directory.

## Where Claude Code looks

- **`CLAUDE.md`** at the repo root - Claude Code's canonical context file. Reference shared rules from here.
- **`AGENTS.md`** - also read; rules linked here are accessible.
- **`.claude/agents/<name>.md`** - agent-level operating principles (per-agent guidance, with `description` triggers).
- **`.claude/skills/<slug>/SKILL.md`** - skill-level operating principles.
- **`.claude/commands/<slug>.md`** - command-level guidance (the body of a slash command is read on invocation).
- **`.claude/hooks/`** - automation rules enforced via hook scripts.

## Recommended structure

In `CLAUDE.md` (which should be a slim delegation shim per the two-tier docs pattern), link to:

- [`AGENTS.md`](../AGENTS.md) - shared content.
- [`rules/engineering-rules.md`](engineering-rules.md)
- [`rules/code-review-rules.md`](code-review-rules.md)
- [`rules/security-rules.md`](security-rules.md)
- [`rules/documentation-rules.md`](documentation-rules.md)

Claude Code reads `CLAUDE.md` automatically; deep references resolve when the agent reads them.

## Vendor-specific behaviors

| Topic | Claude Code behavior |
|---|---|
| Permissions (`.claude/settings.json` `permissions`) | Allow/deny lists tighten or relax tool calls without prompting. |
| Per-user overrides (`.claude/settings.local.json`) | Gitignored; layers personal preferences on top of project settings. |
| Hooks (`.claude/settings.json hooks` or `~/.claude/settings.json`) | Most comprehensive of any vendor. ~30 events spanning session/tool/permission/subagent/task/stop/config/cwd/file/worktree/compact/elicitation/notification lifecycles. 5 hook types: `command`, `http`, `mcp_tool`, `prompt`, `agent`. Blocking via exit 2 or `hookSpecificOutput.permissionDecision: "deny"`. Per-hook `if` filter (permission rule syntax), `timeout`, `async`, `asyncRewake`, `shell`, `once`. See [`hooks/claude/hooks.template.json`](../hooks/claude/hooks.template.json). |
| Sub-agents (`.claude/agents/`) | Invoked via the `Task` tool with `subagent_type: <agent-name>` - the runtime auto-loads agents from this dir. |
| MCP servers (`.claude/claude_desktop_config.json` for Desktop, project-scoped `.claude/settings.json` for project servers) | Two layers; the desktop config is global, the project config is per-project. |

## Rule frontmatter (Claude-irrelevant)

Claude Code doesn't consume rule-loading frontmatter like Cursor's `alwaysApply` or Kiro's `inclusion: fileMatch`. Rules in `rules/` are surfaced through `CLAUDE.md` / `AGENTS.md` references.

## Sanitization gate

The PreToolUse hook (`pre-bash-sanitize.sh`) is recommended for any project using SpecRoute. It blocks `git commit` / `git push` if forbidden strings appear in tracked files. See [`security-rules.md`](security-rules.md) Rule 10.

## See also

- [`engineering-rules.md`](engineering-rules.md) - vendor-neutral engineering rules.
- [`runtimes/.claude/README.md`](../runtimes/.claude/README.md) - Claude Code runtime layout.
- [`agentic-docs/automation-decision-framework.md`](../agentic-docs/automation-decision-framework.md) - when to build a skill vs agent vs command vs hook.
