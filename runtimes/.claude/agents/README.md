# `.claude/agents/` - Claude Code agent registry

Drop your project's agent definitions here. Each agent is a flat `<name>.md` file with YAML frontmatter that Claude Code reads automatically.

## Frontmatter contract

```yaml
---
name: <slug>                              # required; matches filename
description: <triggers>                   # required; trigger phrases for auto-selection
model: opus | sonnet | haiku              # required
color: <recognized color>                 # required
memory: project | user | absent           # optional
internet: Yes | No | absent               # optional
---
```

**`description` must include trigger phrases** (literal user utterances in quotes). Without triggers, the agent won't be auto-selected.

See [`agents/agent-template.md`](../../../agents/agent-template.md) for field-by-field guidance and [`agents/examples/`](../../../agents/examples/) for worked examples.

## File shape

Each `.md` file:

```markdown
---
name: <slug>
description: ...
model: opus
color: blue
---

You are the <Role> for <Project> - <one-sentence scope>.

## Owns

- `<file/dir>` - <why>

## Operating principles

- <Principle 1>

## Don't use for

- <Adjacent concern> - <other agent>.
```

Body length: ~30–50 lines is the sweet spot.

## Adding an agent

1. Choose a slug; create `<slug>.md`.
2. Fill in frontmatter (all four required fields).
3. Write the body (Owns / Operating principles / Don't use for).
4. The PostToolUse frontmatter hook (`hooks/scripts/post-edit-frontmatter.sh`) will validate on save.

## Mirroring to Codex

If your project also targets Codex, mirror the agent into `.codex/agents/<name>.md` (same shape). Use `tools/sync-skills.py` (which also handles agents) to keep them aligned.
