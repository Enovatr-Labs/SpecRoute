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

The body and `name`/`description` are portable. Claude's `color` and `memory` fields do not apply here, and Claude's `model` values are not Gemini model ids - map intent to Gemini's `model`, `tools`, `kind`, and `temperature`. Note that Gemini subagents do not inherit the parent's tools, so be explicit in `tools`.

If a SpecRoute roster row says `Internet: Yes`, express it here by listing Gemini's web tools in `tools`. There is no `internet:` frontmatter field in Gemini, Claude, or any other vendor - it is a roster column only. Tier words (`flagship` / `balanced` / `fast`) are likewise documentation; see [`wiki/Agents.md`](../../../wiki/Agents.md#semantic-model-tiers) for the mapping to concrete Gemini model ids.

`spec-reviewer.md` ships here as a worked reference. Replace or extend it with your project's roster.
