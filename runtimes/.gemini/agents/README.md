# `.gemini/agents/` - Gemini CLI subagents

One Markdown file per subagent. The body after the frontmatter becomes the subagent's system prompt. Project-level agents live here; personal ones live at `~/.gemini/agents/`.

```
.gemini/agents/
└── <name>.md
```

## Frontmatter contract

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Subagent identifier. |
| `description` | Yes | Purpose plus trigger phrases for delegation. |
| `kind` | No | Agent type, e.g. `local`. |
| `tools` | No | Allowed Gemini tools. Parent permissions do NOT flow to subagents; list them explicitly. |
| `mcpServers` | No | MCP servers the subagent may use. |
| `model` | No | Model override, e.g. `gemini-2.5-pro`. |
| `temperature` | No | Sampling temperature. |
| `max_turns` | No | Per-invocation turn cap. |
| `timeout_mins` | No | Wall-clock cap. |

## Porting from `.claude/agents/`

The body and `name`/`description` are portable. Claude's `model`/`color`/`memory`/`internet` fields do not apply; map intent to Gemini's `model`, `tools`, `kind`, and `temperature`. Note that Gemini subagents do not inherit the parent's tools, so be explicit in `tools`.

`spec-reviewer.md` ships here as a worked reference. Replace or extend it with your project's roster.
