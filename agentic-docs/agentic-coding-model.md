# Agentic Coding Model

How agents, skills, commands, and hooks compose to produce reviewable software. This is the conceptual model that the templates and runtime layouts encode.

## The four primitives

SpecRoute recognizes four distinct automation primitives. Each has a different invocation pattern, a different cognitive load, and a different "right time to use." [`automation-decision-framework.md`](automation-decision-framework.md) is the decision matrix; this doc explains why we have four primitives and how they compose.

| Primitive | Invocation | User input per call | Autonomy level |
|---|---|---|---|
| **Skill** | User invokes by name; agent guides through steps | Multiple (interactive) | Guided (asks for decisions) |
| **Agent** | User delegates a task; agent runs to completion | One (the task description) | High (decides on its own) |
| **Command** | User types `/<name>` | None or argument | One-shot (deterministic) |
| **Hook** | Triggered by an event (file edit, session start, pre-tool) | None (event-driven) | Automatic |

These are not interchangeable. Picking the wrong primitive produces friction:

- A workflow that's actually interactive shoehorned into a command becomes a wall of arguments.
- A simple command shoehorned into a skill becomes annoyingly chatty.
- An autonomous agent shoehorned into a hook blocks the user mid-thought.
- A hook trying to do agent-level work timeouts or hangs.

## How they compose

A typical SpecRoute-driven feature implementation uses all four:

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│   Hook (PreToolUse on git commit)                                    │
│     └── blocks if sanitization fails                                 │
│                                                                      │
│   Skill (scaffold-artifact)                                          │
│     └── interactively bootstraps a new PRD with frontmatter          │
│                                                                      │
│   Agent (prd-author)                                                 │
│     └── drafts the PRD body autonomously, given the bootstrap        │
│                                                                      │
│   Command (/audit)                                                   │
│     └── one-shot pre-PR check                                        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

The user types `/scaffold-artifact prd notification-preferences`. The skill asks a few questions, copies the template. The user then says "draft section 5 with `prd-author`" - the agent produces the content. Before commit, the user runs `/audit`, which surfaces issues. On commit, the hook validates sanitization. Each primitive does what it's best at.

## Vendor differences

Not every vendor supports every primitive. The matrix in [`AGENTS.md`](../AGENTS.md) documents this:

- **Claude Code** supports all four primitives plus the richest hook system (~30 events, 5 hook types).
- **Codex** supports skills and agents; commands are subsumed into skills via `user-invocable: true`; hooks via `.codex/hooks.json` (6 events, Claude-compatible JSON).
- **Gemini CLI** supports commands (JSON map), MCP, and hooks via `.gemini/settings.json` (11 events; v0.26.0+).
- **Kiro** supports hooks (`*.kiro.hook` files, 10 events including file create/save/delete) and steering rules; no skills, agents, or commands as standalone concepts.
- **Cursor** supports rules and hooks via `.cursor/hooks.json` (~21 events with `permission` decision schema).
- **Windsurf** supports rules and hooks via `.windsurf/hooks.json` (12 events; pre-hooks block, post-hooks observe).

**Every supported vendor ships a hooks system.** The event taxonomies and config shapes differ; the underlying contract (script reads JSON on stdin, returns JSON on stdout, uses exit codes for blocking) is broadly compatible. See [`hooks/README.md`](../hooks/README.md) for the full per-vendor event matrix.

A SpecRoute consumer chooses primitives based on which vendors they target. A team on Claude Code uses all four. A team on Cursor uses rules and shared prompts. A team on multiple vendors uses the shared `prompts/` and `rules/` plus per-vendor implementations of each primitive where supported.

## Composition rules

These hold across vendors:

1. **Don't reimplement a primitive in another primitive's clothing.** A skill that runs autonomously without user input is an agent; rename it. A hook that asks the user a question is a skill; rename it.
2. **Hooks should be fast and idempotent.** Sub-second target. Hooks that take seconds degrade the agent CLI and frustrate users.
3. **Agents should declare their boundaries.** Every agent has a "Don't use for" section that hands off to the right neighbor. This is how we keep agent rosters from becoming spaghetti.
4. **Commands should not have hidden parameters.** If the operation has more than one mode, it's a skill.
5. **Skills should not run autonomously.** The user is in the loop; that's the entire point.

## Why this matters for spec-driven work

The four primitives map cleanly onto the spec-driven flow:

- **Skills** drive the early stages where decisions are made (PRD authoring, spec drafting, scaffolding).
- **Agents** drive the implementation stages where work runs to completion (drafting sections, refactoring, generating tests).
- **Commands** drive the validation gates where checks must be deterministic (`/audit`, `/parity`, `/sanitize`).
- **Hooks** drive the always-on guardrails (sanitization gate, frontmatter check, session-start status).

A team that uses only one primitive is missing the others' value. SpecRoute's templates make all four readily available so consumers pick the right tool for each step.

## Pitfalls

- **Skill sprawl.** Every contributor wants a skill for their workflow. Most workflows are commands or agents in disguise. Apply the decision matrix before adding.
- **Hook overuse.** Every reasonable validation can be a hook, but a repository with 30 hooks is unusable - the agent CLI grinds. Reserve hooks for things that *must* be enforced, not things that should be reminded.
- **Agent overlap.** Two agents owning the same files is a coordination tax. Make boundaries explicit in the "Owns" and "Don't use for" sections.
- **Command stuffing.** `/build` that takes 12 flags is a skill. `/run-tests` is a command.

## Where to read next

- [`automation-decision-framework.md`](automation-decision-framework.md) - the 4-row decision matrix and when to reach for each primitive.
- [`multi-vendor-context-files.md`](multi-vendor-context-files.md) - how the canonical `AGENTS.md` and per-vendor delegation shims work.
- [`agent-cli-integrations.md`](agent-cli-integrations.md) - concrete wiring per vendor.
- The `.claude/agents/` directory of this repo - 11 worked examples of agent definitions.
