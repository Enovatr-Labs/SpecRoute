# `.kiro/agents/` - Kiro custom subagents

Flat-file subagents Kiro can delegate to. Arrived in **Kiro 0.9** (2026-02-05); unchanged through **Kiro IDE 1.0** (2026-07-23), which reformatted hooks but left agents alone.

## Layout

```
.kiro/agents/<name>.md     one subagent per file - frontmatter + prompt body
```

Workspace subagents live under `<workspace>/.kiro/agents/`; user-global subagents live under `~/.kiro/agents/`. The body is the system prompt; the frontmatter declares the contract.

## Frontmatter contract

| Field | Required | Notes |
|---|---|---|
| `name` | yes | Agent identifier. Used to delegate to the subagent. |
| `description` | no | When to use the agent. Include trigger phrases so Kiro routes to it. |
| `tools` | no | Array of allowed tools. Supports wildcards and MCP references (e.g. `@figma/*`). Omit to inherit the default tool set. |
| `model` | no | Model id (e.g. `claude-sonnet-4`). Defaults to the model selected in chat. |
| `includeMcpJson` | no | Boolean. Include all MCP tools from `.kiro/settings/mcp.json`. |
| `includePowers` | no | Boolean. Include Powers MCP tools. |

> Note: Kiro subagents do NOT use the Claude agent fields `color` or `memory`. When syncing an agent from `.claude/agents/`, drop `color`/`memory`, map `model: sonnet` to a Kiro model id (e.g. `claude-sonnet-4`), and translate Claude's prose tool guidance into a `tools` array. Keep the prompt body and the Owns / Operating Principles / Don't Use For sections.

## See also

- [`spec-reviewer.md`](spec-reviewer.md) - canonical sample subagent body.
- The same agent in [`../../.claude/agents/spec-reviewer.md`](../../.claude/agents/spec-reviewer.md) - source for cross-vendor sync.
