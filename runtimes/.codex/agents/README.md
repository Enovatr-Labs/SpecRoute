# `.codex/agents/`

Codex agent registry. Same flat-file frontmatter shape as Claude Code's `.claude/agents/`.

```yaml
---
name: <slug>
description: <triggers>
model: opus | sonnet | haiku
color: <recognized color>
memory: project | user | absent     # optional
internet: Yes | No | absent         # optional
---
```

See [`agents/agent-template.md`](../../../agents/agent-template.md) for full guidance.

## Mirroring with Claude

Codex consumes the **same agent file shape** as Claude Code. Mirror agents 1:1 between `.claude/agents/` and `.codex/agents/`. Use `tools/sync-skills.py` (which also handles agents) to detect drift.
