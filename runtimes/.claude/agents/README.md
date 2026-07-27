# `.claude/agents/` - Claude Code agent registry

Drop your project's agent definitions here. Each agent is a flat `<name>.md` file with YAML frontmatter that Claude Code reads automatically.

## Frontmatter contract

**Only `name` and `description` are required.** Everything else is optional with a runtime default.

```yaml
---
name: <slug>                              # required; matches filename
description: <triggers>                   # required; trigger phrases for auto-selection
model: opus                               # optional; opus | sonnet | haiku | fable | <full id> | inherit (default: inherit)
tools: Read, Grep, Glob                   # optional; allowlist
disallowedTools: Write, Edit              # optional; denylist, applied before `tools`
skills: [<skill-slug>]                    # optional; preload skill content
memory: project | user | local            # optional
effort: high                              # optional; low | medium | high | xhigh | max
isolation: worktree                       # optional; dedicated git worktree
permissionMode: <mode>                    # optional
color: <recognized color>                 # optional; UI tint only
---
```

**`description` must include trigger phrases** (literal user utterances in quotes). Without triggers, the agent won't be auto-selected.

Also available: `maxTurns`, `mcpServers`, `hooks`, `background`, `initialPrompt`.

Notes:

- When `model` is omitted the subagent **inherits the parent session's model**. That is usually what you want; pin a model only when the role genuinely needs a different one.
- `color` is cosmetic. Omitting it does not prevent the agent from loading.
- **There is no `internet:` field.** Grant web research by including `WebFetch` / `WebSearch` in `tools`; withhold it by omitting them or naming them in `disallowedTools`.
- SpecRoute's `flagship` / `balanced` / `fast` tiers are a documentation abstraction for roster tables - never write them into `model`. Mapping table: [`wiki/Agents.md`](../../../wiki/Agents.md#semantic-model-tiers).

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
2. Fill in frontmatter (`name` and `description` at minimum; add optional fields only where they earn their place).
3. Write the body (Owns / Operating principles / Don't use for).
4. The PostToolUse frontmatter hook (`hooks/scripts/post-edit-frontmatter.sh`) will validate on save.

## Mirroring to Codex

Codex agents are **standalone TOML files** at `.codex/agents/<name>.toml` (`name`, `description`, `developer_instructions`), not this Markdown shape. The body content is portable; the frontmatter is not. Because the shapes diverge, `tools/sync-skills.py` mirrors skills only - keep agents aligned by hand. See [`.codex/agents/README.md`](../../.codex/agents/README.md).
