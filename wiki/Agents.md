# Agents

<!-- sources: agents/README.md, agents/roster.md -->

Agent definitions — defined roles with model, tools, and operating principles, invokable by an agent CLI runtime.

For the canonical reference, see [`agents/README.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/agents/README.md).

## Directory layout

```
agents/
├── agent-template.md         canonical template with frontmatter contract
├── roster.md                 cross-vendor agent inventory template
├── archetypes/               role concepts — NOT files the runtime loads
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

### Archetypes — *role concepts*
`archetypes/` describes **responsibilities**: "what does a security agent do?" Use when designing your project's roster, onboarding a new contributor, or deciding whether a role you have in mind already has a recognized archetype. These are conceptual references, not files the runtime loads.

### Examples — *file shape*
`examples/` shows **how the file is laid out**: flat `<name>.md` files with YAML frontmatter that the runtime actually loads. Use when creating a new concrete agent, validating frontmatter, or mirroring agents into `runtimes/.claude/agents/` and `runtimes/.codex/agents/`.

These are not redundant — they answer different questions.

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

See [[Frontmatter Contracts]] for field-by-field guidance.

## The "Don't use for" section is load-bearing

Every agent definition must have a "Don't use for" section that explicitly hands off to neighboring agents. This is how SpecForge keeps agent rosters from becoming spaghetti — boundaries are crisp because they're written down.

## Per-vendor mirrors

Concrete agent files are mirrored into:

- `runtimes/.claude/agents/<name>.md` — Claude Code reads from here.
- `runtimes/.codex/agents/<name>.md` — Codex reads from here.

Gemini CLI, Kiro, Cursor, and Windsurf do **not** consume agent files in this shape — they have other concepts (commands, steering, rules). See [[Vendor Matrix]].

To keep the two runtime mirrors aligned: invoke `runtime-architect` or run `tools/sync-skills.py` (which also handles agents). See [[Cross-Vendor Sync]].

## Model choice

| Model | Use for |
|---|---|
| `opus` | Senior author roles — PRDs, spec triplets, agent roster design, complex reviews |
| `sonnet` | Narrower deterministic roles — frontmatter linting, specific implementers |
| `haiku` | Fast / cheap operations — quick scans, sanitization checks |

## Memory and internet flags

- `memory: project` — agent has read/write access to `.claude/agent-memory/<agent-name>/`. See [[Agent Memory]].
- `memory: user` — uses user-level memory at `~/.claude/projects/<project>/memory/`.
- `internet: Yes` — agent should perform web research. Default `No` for code-touching agents.

## The agent roster

A SpecForge-driven project maintains an `agent-roster.md` (template at `agents/roster.md`) that:

- Groups agents by department (Specification, Implementation, Quality, Operations, Documentation, Strategic Advisors).
- Lists each agent's model, color, memory, internet flags.
- Documents the per-task assignment when implementing a feature.

See the canonical roster template at [`agents/roster.md`](https://github.com/Enovatr-Labs/SpecForge/blob/main/agents/roster.md).

## Owner agent

Designing and reviewing the agent roster is owned by the `agent-roster-architect` agent.

## See also

- [[Skills]] · [[Commands]] · [[Hooks]] — the other three automation primitives
- [[Automation Decision Framework]] — when to reach for an agent vs alternatives
- [[Implementation Team]] — 11 worked agent examples in this repo's own `.claude/`
- [[Frontmatter Contracts]] — full required-field reference
