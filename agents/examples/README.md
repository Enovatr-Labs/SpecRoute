# Agent Examples

Concrete agent definitions that demonstrate the flat-file frontmatter contract. These are **the canonical file shape** - not the archetypes in `../archetypes/`, which describe responsibilities.

```
agents/examples/
├── README.md                         (this file)
└── <agent-name>.md                   one flat file per agent
```

## File shape

Each agent is a single `<name>.md` file with YAML frontmatter and a body:

```yaml
---
name: <slug-matching-filename>           # required
description: <triggers>                  # required
model: sonnet                            # optional; vendor model id (Claude: opus | sonnet | haiku | fable | <full id> | inherit)
tools: Read, Grep, Glob                  # optional; allowlist. Web access = include WebFetch / WebSearch here.
memory: project | user | local           # optional
color: <recognized color>                # optional; UI tint only
---

You are the <Role Title> for <Project> - <one-sentence scope>.

## Owns

- `<file/dir>` - <why>

## Operating principles

- <Principle>

## Don't use for

- <Adjacent concern> - <other agent>.
```

Only `name` and `description` are required. `model` takes a **vendor model id** - SpecRoute's `flagship` / `balanced` / `fast` tiers belong in roster tables, not in files the runtime loads. There is no `internet:` field; grant or withhold `WebFetch` / `WebSearch` via `tools` instead.

See [`../agent-template.md`](../agent-template.md) for full guidance, [`../roster.md`](../roster.md) for the cross-vendor inventory, and [`../../wiki/Agents.md`](../../wiki/Agents.md#semantic-model-tiers) for the tier-to-vendor mapping table.

## Reference implementations

The 12 agents under [`.claude/agents/`](../../.claude/agents/) at the repository root are real, tracked implementations of this contract. Read them as worked examples:

- `prd-author.md`, `spec-author.md` - opus-tier author roles, `description` with explicit triggers
- `command-author.md`, `hooks-author.md` - sonnet-tier narrower-scope roles
- `sanitization-auditor.md`, `template-quality-reviewer.md` - quality-gate agents

## Adding an example

1. Pick a generic role (e.g. `release-coordinator`, `documentation-linker`). No domain-specific names.
2. Create `<name>.md` here using the template.
3. Mirror into `runtimes/.claude/agents/<name>.md` and `runtimes/.codex/agents/<name>.md` if it should ship as part of the runtime.
4. Update `../roster.md` to include the new agent.
5. Run `/audit` to validate frontmatter.
