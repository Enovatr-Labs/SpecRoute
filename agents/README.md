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

Only `name` and `description` are required. Shown here in Claude Code's shape; other vendors differ (see [`../wiki/Frontmatter-Contracts.md`](../wiki/Frontmatter-Contracts.md)).

```yaml
---
name: <slug>                            # required; matches filename (without .md)
description: <triggers>                 # required; must include trigger phrases for auto-selection
model: opus                             # optional; default `inherit`
tools: Read, Grep, Glob                 # optional; allowlist
disallowedTools: Write, Edit            # optional; denylist, applied before `tools`
skills: [<skill-slug>]                  # optional; preload skill content
memory: project | user | local          # optional
effort: high                            # optional; low | medium | high | xhigh | max
isolation: worktree                     # optional; dedicated git worktree
permissionMode: <mode>                  # optional
color: <recognized color>               # optional; UI tint only
---
```

**`description` must include trigger phrases** in quotes (literal user utterances that should invoke the agent). Without triggers, Claude Code's automatic agent selection won't pick it up.

Two things SpecRoute used to get wrong, corrected here:

- **`model` takes a vendor model id, not a tier word.** `flagship` / `balanced` / `fast` are a SpecRoute documentation abstraction for roster tables. Writing one into an agent file produces an invalid value. Canonical tier-to-vendor mapping: [`../wiki/Agents.md`](../wiki/Agents.md#semantic-model-tiers).
- **There is no `internet:` field.** It restricts nothing. Express web access through `tools` (include or omit `WebFetch` / `WebSearch`). A roster table may keep an "Internet" column as documentation of intent.

See [`agent-template.md`](agent-template.md) for field-by-field guidance and [`roster.md`](roster.md) for the cross-vendor roster template.

## Per-vendor mirrors

Concrete agent files are mirrored into:

- `runtimes/.claude/agents/<name>.md` - Claude Code (Markdown + frontmatter)
- `runtimes/.codex/agents/<name>.toml` - Codex (standalone TOML with `developer_instructions`)
- `runtimes/.gemini/agents/<name>.md`, `runtimes/.kiro/agents/<name>.md`, `runtimes/.cursor/agents/<name>.md` - Markdown subagents with vendor-specific frontmatter
- `runtimes/.devin/agents/<name>/AGENT.md` - Devin Desktop subagent profiles

The **body** is portable across all of them; the frontmatter is not. Don't copy Claude's fields into another vendor's file. See the vendor matrix in [`../README.md`](../README.md) and the per-vendor field lists in [`../wiki/Frontmatter-Contracts.md`](../wiki/Frontmatter-Contracts.md).

Use `tools/sync-skills.py` to keep skill bodies aligned. Agent formats diverge across vendors, so maintain agent mirrors through `runtime-architect`.

## Authoring agent

Designing and reviewing the agent roster is owned by the `agent-roster-architect` agent. See `.claude/agents/agent-roster-architect.md` for its operating principles.

## Related documents

- [`agentic-docs/agentic-coding-model.md`](../agentic-docs/agentic-coding-model.md) - when to choose agent vs skill vs command vs hook
- [`agentic-docs/automation-decision-framework.md`](../agentic-docs/automation-decision-framework.md) - the 4-row decision matrix
