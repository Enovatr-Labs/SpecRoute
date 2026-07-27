# Agents

<!-- sources: agents/README.md, agents/roster.md -->

Agent definitions — defined roles with model, tools, and operating principles, invokable by an agent CLI runtime.

For the canonical reference, see [`agents/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agents/README.md).

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

## Frontmatter contract (Claude Code)

Only `name` and `description` are required. Everything else is optional and has a runtime default.

```yaml
---
name: <slug>                            # required; matches filename (without .md)
description: <triggers>                 # required; must include trigger phrases for auto-selection
model: opus                             # optional; default `inherit`
tools: Read, Grep, Glob                 # optional; allowlist
disallowedTools: Write, Edit            # optional; denylist, applied before `tools`
skills: [frontmatter-lint]              # optional; preload skill content
memory: project                         # optional; user | project | local
effort: high                            # optional; low | medium | high | xhigh | max
isolation: worktree                     # optional; run in a dedicated git worktree
permissionMode: <mode>                  # optional
color: yellow                           # optional; UI tint only
---
```

**`description` must include trigger phrases** in quotes (literal user utterances that should invoke the agent). Without triggers, Claude Code's automatic agent selection won't pick it up.

`model` accepts `opus` | `sonnet` | `haiku` | `fable`, a full model id (e.g. `claude-opus-5`), or `inherit`. It is **not** required, and the tier words `flagship` / `balanced` / `fast` are **not** valid values - see [Semantic model tiers](#semantic-model-tiers) below.

There is no `internet` field. Web access is expressed through `tools` (include or omit `WebFetch` / `WebSearch`), not through a declarative flag.

See [[Frontmatter Contracts]] for field-by-field guidance, including the remaining optional fields (`maxTurns`, `mcpServers`, `hooks`, `background`, `initialPrompt`).

## The "Don't use for" section is load-bearing

Every agent definition must have a "Don't use for" section that explicitly hands off to neighboring agents. This is how SpecRoute keeps agent rosters from becoming spaghetti — boundaries are crisp because they're written down.

## Per-vendor mirrors

All six vendors now consume subagents — they differ in **file format**, not capability:

- `runtimes/.claude/agents/<name>.md` — Claude Code (flat Markdown + frontmatter).
- `runtimes/.codex/agents/<name>.toml` — Codex (standalone TOML: `name`, `description`, `developer_instructions`).
- `runtimes/.gemini/agents/<name>.md`, `runtimes/.kiro/agents/<name>.md`, `runtimes/.cursor/agents/<name>.md` — Markdown subagents.
- Devin Desktop — experimental per-profile subagents under `.devin/agents/<name>/AGENT.md`.

See [[Vendor Matrix]].

Because Claude's flat Markdown and Codex's TOML are **different shapes**, `tools/sync-skills.py` mirrors skills only, not agents — keep agents aligned by invoking `runtime-architect`. See [[Cross-Vendor Sync]].

## Semantic model tiers

`flagship` / `balanced` / `fast` are a **SpecRoute abstraction**, not a value any vendor accepts. They exist so a roster can express intent once and stay readable across vendors. Every real agent file must carry a model id its own runtime accepts.

**This table is the canonical mapping.** Other SpecRoute docs point here rather than restating it.

| SpecRoute tier | Use for | Claude Code | Codex | Gemini CLI | Kiro | Cursor | Devin Desktop |
|---|---|---|---|---|---|---|---|
| `flagship` | Senior author roles - PRDs, spec triplets, roster design, complex reviews | `opus` | highest-capability Codex model id, optionally with `model_reasoning_effort = "high"` | `gemini-2.5-pro` | Anthropic model id (e.g. `claude-opus-4`) | omit / `inherit`, or a specific model ID | `opus` |
| `balanced` | Narrower deterministic roles - linting, scoped implementers | `sonnet` | `gpt-5-codex` | `gemini-2.5-flash` | `claude-sonnet-4` | omit / `inherit`, or a specific model ID | `sonnet` |
| `fast` | Fast / cheap operations - quick scans, mechanical checks | `haiku` | smallest Codex model id available | Gemini's lightest Flash id | Kiro's lightest available model id | omit / `inherit`, or a specific model ID | `haiku` |

Notes:

- Vendor model catalogues change. Treat the non-Claude columns as *nearest-tier* guidance and confirm the id against your vendor's current model list before shipping.
- Claude Code also accepts `fable` and full model ids (e.g. `claude-opus-5`). When `model` is absent the subagent **inherits the parent session's model** - which is often the right answer.
- Where a vendor's `model` field is optional and inheritance is the default (Cursor, Codex, Kiro), omitting it is preferable to pinning a stale id.

## Memory

- `memory: project` — agent has read/write access to `.claude/agent-memory/<agent-name>/`. See [[Agent Memory]].
- `memory: user` — uses user-level memory at `~/.claude/projects/<project>/memory/`.
- `memory: local` — machine-local memory that isn't shared with the project.

## Web access

There is no `internet:` frontmatter field. To let an agent research the web, grant `WebFetch` / `WebSearch` in `tools`; to deny it, either omit them from a `tools` allowlist or name them in `disallowedTools`. A roster table **may** keep an "Internet" column as human-readable documentation of intent - just don't mirror it into agent frontmatter, where it does nothing.

## The agent roster

A SpecRoute-driven project maintains an `agent-roster.md` (template at `agents/roster.md`) that:

- Groups agents by department (Specification, Implementation, Quality, Operations, Documentation, Strategic Advisors).
- Lists each agent's model tier, color, and memory, plus an optional documentation-only "Internet" column recording whether the agent is expected to do web research.
- Documents the per-task assignment when implementing a feature.

Roster tables are documentation, so they may use the semantic tiers. Agent **files** must not.

See the canonical roster template at [`agents/roster.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agents/roster.md).

## Owner agent

Designing and reviewing the agent roster is owned by the `agent-roster-architect` agent.

## See also

- [[Skills]] · [[Commands]] · [[Hooks]] — the other three automation primitives
- [[Automation Decision Framework]] — when to reach for an agent vs alternatives
- [[Implementation Team]] — 11 worked agent examples in this repo's own `.claude/`
- [[Frontmatter Contracts]] — full required-field reference
