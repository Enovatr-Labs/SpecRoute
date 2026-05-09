# Agents

Agent definitions - defined roles with model, tools, and operating principles, invokable by an agent CLI runtime.

```
agents/
├── agent-template.md         canonical template with frontmatter contract
├── roster.md                 cross-vendor agent inventory template
├── archetypes/               role concepts (NOT file layout - these describe responsibilities)
│   ├── product-agent.md
│   ├── architect-agent.md
│   ├── backend-agent.md
│   ├── frontend-agent.md
│   ├── security-agent.md
│   ├── qa-agent.md
│   └── devops-agent.md
└── examples/                 concrete <name>.md files showing the actual frontmatter shape
```

## Two distinct concepts

### Archetypes (role concepts)

`archetypes/` describes *responsibilities* - "what does a security agent do?" These are conceptual references, not files the runtime loads. Use them when:

- Designing your project's roster.
- Onboarding a new contributor to the agent model.
- Deciding whether a role you have in mind already has a recognized archetype.

### Examples (file shape)

`examples/` shows *how the file is laid out* - flat `<name>.md` files with YAML frontmatter that the runtime actually loads. Use them when:

- Creating a new concrete agent.
- Validating frontmatter on an existing one.
- Mirroring agents into `runtimes/.claude/agents/` and `runtimes/.codex/agents/`.

These are not redundant - they answer different questions. An archetype is "what is a backend agent?"; an example is "what does a backend-agent file look like?"

## Frontmatter contract

```yaml
---
name: <slug>                            # required; matches filename (without .md)
description: <triggers>                 # required; must include trigger phrases for auto-selection
model: opus | sonnet | haiku            # required
color: <recognized color>               # required
memory: project | user | absent         # optional
internet: Yes | No | absent             # optional
---
```

**`description` must include trigger phrases** in quotes (literal user utterances that should invoke the agent). Without triggers, Claude Code's automatic agent selection won't pick it up.

See [`agent-template.md`](agent-template.md) for field-by-field guidance and [`roster.md`](roster.md) for the cross-vendor roster template.

## Per-vendor mirrors

Concrete agent files are mirrored into:

- `runtimes/.claude/agents/<name>.md` - Claude Code reads from here
- `runtimes/.codex/agents/<name>.md` - Codex reads from here

Gemini CLI, Kiro, Cursor, and Windsurf do not consume agent files in this shape - they have other concepts (commands, steering, rules). See the vendor matrix in [`../README.md`](../README.md).

To keep the two runtime mirrors aligned: invoke `runtime-architect` or run `tools/sync-skills.py` (which also handles agents).

## Authoring agent

Designing and reviewing the agent roster is owned by the `agent-roster-architect` agent. See `.claude/agents/agent-roster-architect.md` for its operating principles.

## Related documents

- [`agentic-docs/agentic-coding-model.md`](../agentic-docs/agentic-coding-model.md) - when to choose agent vs skill vs command vs hook
- [`agentic-docs/automation-decision-framework.md`](../agentic-docs/automation-decision-framework.md) - the 4-row decision matrix
