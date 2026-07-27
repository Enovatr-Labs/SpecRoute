# Agent Roster Template

Cross-vendor inventory of agents for a SpecRoute-driven project. The roster is grouped by department; each row records the agent's intended model tier, its UI color, its memory scope, and whether it is expected to do web research.

> **The roster is documentation, not frontmatter.** Its columns describe intent in vendor-neutral terms. Agent *files* carry different values - see [Frontmatter contract](#frontmatter-contract) at the bottom.

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
- **Model**: the semantic tier the agent runs on. SpecRoute uses `flagship` / `balanced` / `fast` in roster tables and vendor-neutral prose; these are a **SpecRoute abstraction**, not a value any vendor accepts. Each agent file must carry its own runtime's model id (Claude: `opus` / `sonnet` / `haiku`). The columns below spell out the concrete Claude values for clarity. Canonical tier-to-vendor mapping: [`../wiki/Agents.md`](../wiki/Agents.md#semantic-model-tiers).
- **Color**: visual distinction in the runtime UI. Optional in every runtime that supports it; pick something memorable and reuse colors only across departments, not within.
- **Memory**: `project` stores per-conversation context in this repo's `.claude/agent-memory/<agent-name>/`; `user` stores it in user-level memory; `local` is machine-local; absent = no persistent memory.
- **Internet**: **documentation only.** Records whether the agent is expected to perform web research. There is no `internet:` frontmatter field in any runtime - a `Yes` here means the agent file should grant `WebFetch` / `WebSearch` in its `tools`, and a `No` means it should not.

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

Agent files (in `agents/examples/` and per-vendor `runtimes/.<vendor>/agents/`) carry vendor-specific frontmatter. In Claude Code's shape, **only `name` and `description` are required**:

```yaml
---
name: <slug>                              # required; matches filename
description: <triggers>                   # required; must include trigger phrases for auto-selection
model: opus                               # optional; vendor model id, default `inherit`
tools: Read, Grep, Glob                   # optional; allowlist - this is where web access lives
memory: project | user | local            # optional
color: <recognized color>                 # optional; UI tint only
---
```

Two mappings from roster column to file field:

| Roster column | In the agent file |
|---|---|
| Model tier (`flagship` / `balanced` / `fast`) | A real vendor model id (`opus` / `sonnet` / `haiku`), or omitted to inherit. Never the tier word. |
| Internet (`Yes` / `No`) | Presence or absence of `WebFetch` / `WebSearch` in `tools`. There is no `internet:` field. |

See [`agent-template.md`](agent-template.md) for field-by-field guidance and [`../wiki/Frontmatter-Contracts.md`](../wiki/Frontmatter-Contracts.md) for the per-vendor field lists.
