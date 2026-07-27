# `.codex/agents/`

Codex subagent registry. Codex agents are **standalone TOML files**, not the flat Markdown-plus-YAML shape Claude Code uses. Do not copy Claude's frontmatter here.

```
.codex/agents/
└── <name>.toml                       one subagent per file
```

## Field contract

```toml
name = "spec-reviewer"
description = """
When to delegate to this subagent, including trigger phrases.
"""

developer_instructions = """
The subagent's system prompt - the equivalent of the Markdown body in a Claude agent.
"""

# model = "gpt-5-codex"              # optional; inherits the parent session when omitted
# model_reasoning_effort = "high"    # optional
# sandbox_mode = "read-only"         # optional
```

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Subagent identifier. |
| `description` | Yes | When to delegate. Include trigger phrases so Codex routes to it. |
| `developer_instructions` | Yes | The system prompt. This is where the Owns / Operating Principles / Don't Use For body goes. |
| `model` | No | Codex model id. Inherits the parent session when omitted. |
| `model_reasoning_effort` | No | Reasoning budget for this subagent. |
| `sandbox_mode` | No | Filesystem / network posture for the subagent. |
| `mcp_servers` | No | MCP servers the subagent may use. |
| `skills.config` | No | Skill configuration for the subagent. |

Reference: <https://learn.chatgpt.com/docs/agent-configuration/subagents>

## Porting from `.claude/agents/`

The **body is portable; the frontmatter is not.**

| Claude field | Codex equivalent |
|---|---|
| Markdown body | `developer_instructions` (triple-quoted string) |
| `name`, `description` | `name`, `description` |
| `model: opus \| sonnet \| haiku` | `model` = a Codex model id, or omit to inherit. Reach for `model_reasoning_effort` before a bigger model. |
| `tools`, `disallowedTools` | `sandbox_mode` plus the MCP / skill config - not a direct one-to-one. |
| `color`, `memory` | No equivalent. Drop them. |

SpecRoute's `flagship` / `balanced` / `fast` tiers are a documentation abstraction used in roster tables; they are never valid in a real agent file, for Codex or any other vendor. See [`wiki/Agents.md`](../../../wiki/Agents.md#semantic-model-tiers) for the tier-to-vendor mapping.

Because the two shapes diverge, `tools/sync-skills.py` mirrors **skills only**. When an agent's substance changes, update both `.claude/agents/<name>.md` and `.codex/agents/<name>.toml` by hand.

See [`spec-reviewer.toml`](spec-reviewer.toml) for the worked reference and [`agents/agent-template.md`](../../../agents/agent-template.md) for body-level guidance.
