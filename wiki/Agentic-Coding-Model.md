# Agentic Coding Model

<!-- sources: agentic-docs/agentic-coding-model.md -->

How **agents, skills, commands, and hooks** compose to produce reviewable software. This is the conceptual model encoded by the templates and runtime layouts.

For the canonical version, see [`agentic-docs/agentic-coding-model.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/agentic-coding-model.md).

## The four primitives

| Primitive | Invocation | User input per call | Autonomy level |
|---|---|---|---|
| **Skill** | User invokes by name; skill guides through steps | Multiple (interactive) | Guided (asks for decisions) |
| **Agent** | User delegates a task; agent runs to completion | One (the task description) | High (decides on its own) |
| **Command** | User types `/<name>` | None or one argument | One-shot (deterministic) |
| **Hook** | Triggered by an event (file edit, session start, pre-tool) | None (event-driven) | Automatic |

These are not interchangeable. Picking the wrong primitive produces friction:

- A workflow that's actually interactive shoehorned into a command becomes a wall of arguments.
- A simple command shoehorned into a skill becomes annoyingly chatty.
- An autonomous agent shoehorned into a hook blocks the user mid-thought.
- A hook trying to do agent-level work times out or hangs.

## How they compose

A typical SpecRoute-driven feature uses all four:

```
Hook (PreToolUse on git commit)
  └── blocks if sanitization fails

Skill (scaffold-artifact)
  └── interactively bootstraps a new PRD with frontmatter

Agent (prd-author)
  └── drafts the PRD body autonomously

Command (/audit)
  └── one-shot pre-PR check
```

The user types `/scaffold-artifact prd notification-preferences`. The skill asks a few questions, copies the template. The user then says "draft section 5 with `prd-author`" — the agent produces the content. Before commit, the user runs `/audit`. On commit, the hook validates sanitization.

## Vendor differences

Not every vendor supports every primitive. See [[Vendor Matrix]] for the contract.

- **Claude Code** — all four primitives + the richest hook system (~27 events).
- **Codex** — skills + agents; commands subsumed into skills via `user-invocable: true`; hooks via 6 events.
- **Gemini CLI** — commands (JSON map), MCP, and hooks via 11 events.
- **Kiro** — hooks + steering rules; no standalone skills/agents/commands.
- **Cursor / Windsurf** — rules + hooks.

**Every supported vendor ships a hooks system.** Event taxonomies and config shapes differ; the underlying contract (script reads JSON on stdin, returns JSON on stdout, uses exit codes for blocking) is broadly compatible. See [[Hooks]].

## Composition rules (hold across vendors)

1. **Don't reimplement a primitive in another primitive's clothing.** A skill that runs without user input is an agent; rename it. A hook that asks a question is a skill; rename it.
2. **Hooks must be fast and idempotent.** Sub-second target.
3. **Agents declare their boundaries.** Every agent has a "Don't use for" section.
4. **Commands have no hidden parameters.** Multi-mode operations are skills.
5. **Skills don't run autonomously.** The user is in the loop — that's the point.

## Why this matters for spec-driven work

The four primitives map onto the spec-driven flow:

- **Skills** drive the early stages (PRD authoring, spec drafting, scaffolding).
- **Agents** drive implementation (drafting sections, refactoring, generating tests).
- **Commands** drive validation gates (`/audit`, `/parity`, `/sanitize`).
- **Hooks** drive always-on guardrails (sanitization, frontmatter, session-start status).

A team that uses only one primitive is missing the others' value.

## Pitfalls

- **Skill sprawl** — most "workflows" are commands or agents in disguise. Apply [[Automation Decision Framework]] before adding.
- **Hook overuse** — a repo with 30 hooks grinds the agent CLI.
- **Agent overlap** — two agents owning the same files is coordination tax. Make boundaries explicit in "Owns" and "Don't use for".
- **Command stuffing** — `/build` with 12 flags is a skill.

## See also

- [[Automation Decision Framework]] — the 4-row decision matrix
- [[Multi-Vendor Context Files]] — `AGENTS.md` + delegation shims
- [[Implementation Team]] — 11 worked agent examples in this repo's own `.claude/`
