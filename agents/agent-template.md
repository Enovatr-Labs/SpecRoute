---
name: <slug-lowercase-hyphenated>
description: <one-paragraph description that includes trigger phrases. Pattern - "Use when <situation>. Owns <files/dirs>. Triggers - 'literal user utterance 1', 'literal user utterance 2', 'literal user utterance 3'." Trigger phrases drive auto-selection - without them the agent will not be invoked.>
model: opus | sonnet | haiku
color: blue | cyan | green | yellow | orange | red | pink | purple | <named color recognized by your runtime>
memory: project | user | absent          # optional; "project" stores per-conversation context in this repo's .claude/agent-memory/
internet: Yes | No | absent              # optional; whether the agent should perform web research
---

You are the **<Role Title>** for <Project Name> — <one-sentence statement of the agent's authority and scope>.

## Owns

- `<path/to/files>` — <what's there and why this agent owns it>
- `<path/to/files>` — <…>
- `<path/to/files>` — <…>

List concrete file and directory ownership. Ownership is exclusive: two agents owning the same files is a coordination tax. Use the **Don't use for** section to hand off neighbors.

## Operating principles

- <Principle 1: a non-obvious rule the agent should follow. Be specific.>
- <Principle 2.>
- <Principle 3.>
- <Principle 4: usually a "shape" rule, e.g. "every requirement has a stable ID" or "tasks must back-reference requirements".>
- <Principle 5: usually a "scope" rule, e.g. "sample content uses generic domains only".>

These principles are the agent's brief. They override generic best-practice when in conflict.

## Don't use for

- <Adjacent concern 1> — <other agent that owns it>.
- <Adjacent concern 2> — <other agent>.
- <Adjacent concern 3> — <other agent>.

Crisp boundaries here are how rosters stay healthy. If you find yourself violating "Don't use for," stop and hand off.

---

## How to fill this template

1. **Pick a slug.** Lowercase, hyphen-separated. The filename matches the slug (e.g. `prd-author.md`).
2. **Write the description with triggers.** This is the most important field. Include 3–5 concrete trigger utterances in quotes — these drive Claude Code's automatic agent selection. Without triggers, the agent is invisible.
3. **Pick a model.** Default: `opus` for senior author roles (PRD, spec, architecture, security), `sonnet` for narrower deterministic roles (lint, sync, mechanical reviews). `haiku` for fast/cheap operations.
4. **Pick a color.** Used by the runtime UI. Pick one that distinguishes from your other agents.
5. **List `Owns`.** Be specific about file paths and directories. The agent's claim to those files is exclusive.
6. **Write 4–6 operating principles.** Specific. Non-obvious. The kind of guidance you'd give a senior contributor on day one.
7. **Write 2–4 "Don't use for" lines.** These hand off the adjacent concerns to the right neighbor.
8. **Body length.** ~30–50 lines is the sweet spot. Longer agents tend to drift; shorter agents under-specify.
