# Agent Roster Template

Cross-vendor inventory of agents for a SpecRoute-driven project. The roster is grouped by department; each row captures the runtime metadata that vendors consume (model, color) plus optional fields (`memory`, `internet`).

> This is a **template**. Copy it into your repo, then populate with your project's actual agents. Sample content below uses generic placeholders.

```yaml
---
Project: <Project Name>
Date: <YYYY-MM-DD>
Total Agents: <N>
---
```

## How to use this roster

- **Departments** group agents by responsibility area. Add departments as your team grows.
- **Model**: which LLM tier the agent runs on (`opus`, `sonnet`, `haiku`). Senior author roles → `opus`. Narrower deterministic roles → `sonnet`. Fast / cheap operations → `haiku`.
- **Color**: visual distinction in the runtime UI. Pick something memorable; reuse colors only across departments, not within.
- **Memory**: `project` stores per-conversation context in this repo's `.claude/agent-memory/<agent-name>/`; `user` stores it in user-level memory; absent = no persistent memory.
- **Internet**: whether the agent should perform web research. Default: `No` for code-touching agents, `Yes` for research-heavy ones.

## Department 1: Specification

| Agent | Role | Model | Color | Memory | Internet |
|---|---|---|---|---|---|
| `prd-author` | PRD author | opus | blue | project | No |
| `spec-author` | Spec triplet author | opus | cyan | project | No |
| `agent-roster-architect` | Agent roster designer | opus | purple | project | No |

**Purpose:** Defines what's being built - PRDs, spec triplets, agent assignments.

## Department 2: Implementation

| Agent | Role | Model | Color | Memory | Internet |
|---|---|---|---|---|---|
| `<implementer-1>` | <role> | opus | <color> | project | No |
| `<implementer-2>` | <role> | sonnet | <color> | project | No |

**Purpose:** Translates specs into code. Add domain-specific implementers as your stack requires (frontend-engineer, backend-engineer, database-engineer, etc.).

## Department 3: Quality

| Agent | Role | Model | Color | Memory | Internet |
|---|---|---|---|---|---|
| `<reviewer-1>` | <role> | sonnet | yellow | project | No |
| `<reviewer-2>` | <role> | opus | red | user | No |

**Purpose:** Code review, security review, sanitization, template quality, test coverage.

## Department 4: Operations

| Agent | Role | Model | Color | Memory | Internet |
|---|---|---|---|---|---|
| `<ops-1>` | <role> | sonnet | <color> | project | Yes |

**Purpose:** Deployment, monitoring, incident response, infrastructure changes.

## Department 5: Documentation

| Agent | Role | Model | Color | Memory | Internet |
|---|---|---|---|---|---|
| `<docs-1>` | <role> | opus | blue | project | No |

**Purpose:** Maintains framework documentation, READMEs, workflow descriptions, ADRs.

## Department 6: Strategic Advisors

| Agent | Role | Model | Color | Memory | Internet |
|---|---|---|---|---|---|
| `<advisor-1>` | <role> | opus | <color> | project | Yes |

**Purpose:** Higher-level guidance - architecture, build-vs-buy, governance. Optional.

## Roster maintenance

- **Adding an agent**: invoke the `agent-roster-architect` agent (or follow `agents/agent-template.md`). Update this roster in the same PR.
- **Renaming an agent**: stable name = stable trigger surface. Renaming requires updating every prompt that names the agent. Avoid unless the rename is a real correction.
- **Retiring an agent**: don't delete the file. Move to a `retired/` subdirectory and note `Status: Retired` in its frontmatter.

## Frontmatter contract

All agent files (in `agents/examples/` and per-vendor `runtimes/.<vendor>/agents/`) include this frontmatter block:

```yaml
---
name: <slug>                              # required; matches filename
description: <triggers>                   # required; must include trigger phrases for auto-selection
model: opus | sonnet | haiku              # required
color: <recognized color>                 # required
memory: project | user | absent           # optional
internet: Yes | No | absent               # optional
---
```

See [`agent-template.md`](agent-template.md) for field-by-field guidance.
