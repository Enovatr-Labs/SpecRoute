---
name: <slug-lowercase-hyphenated>
description: <one-paragraph description that includes trigger phrases. Pattern - "Use when <situation>. Owns <files/dirs>. Triggers - 'literal user utterance 1', 'literal user utterance 2', 'literal user utterance 3'." Trigger phrases drive auto-selection - without them the agent will not be invoked.>
model: <vendor model id>                 # optional; e.g. Claude `opus` / `sonnet` / `haiku` / `inherit`. NOT a SpecRoute tier word.
tools: Read, Grep, Glob                  # optional; allowlist. Include WebFetch/WebSearch only if the agent should research the web.
disallowedTools: Write, Edit             # optional; denylist, applied before `tools`
skills: [<skill-slug>]                   # optional; preload skill content into this agent
memory: project | user | local           # optional; "project" stores per-conversation context in this repo's .claude/agent-memory/
effort: low | medium | high | xhigh | max  # optional; reasoning budget
isolation: worktree                      # optional; run in a dedicated git worktree
permissionMode: <mode>                   # optional; permission posture for this agent
color: blue | cyan | green | yellow | orange | red | pink | purple   # optional; UI tint only
---

You are the **<Role Title>** for <Project Name> - <one-sentence statement of the agent's authority and scope>.

## Owns

- `<path/to/files>` - <what's there and why this agent owns it>
- `<path/to/files>` - <…>
- `<path/to/files>` - <…>

List concrete file and directory ownership. Ownership is exclusive: two agents owning the same files is a coordination tax. Use the **Don't use for** section to hand off neighbors.

## Operating principles

- <Principle 1: a non-obvious rule the agent should follow. Be specific.>
- <Principle 2.>
- <Principle 3.>
- <Principle 4: usually a "shape" rule, e.g. "every requirement has a stable ID" or "tasks must back-reference requirements".>
- <Principle 5: usually a "scope" rule, e.g. "sample content uses generic domains only".>

These principles are the agent's brief. They override generic best-practice when in conflict.

## Don't use for

- <Adjacent concern 1> - <other agent that owns it>.
- <Adjacent concern 2> - <other agent>.
- <Adjacent concern 3> - <other agent>.

Crisp boundaries here are how rosters stay healthy. If you find yourself violating "Don't use for," stop and hand off.

---

## How to fill this template

1. **Pick a slug.** Lowercase, hyphen-separated. The filename matches the slug (e.g. `prd-author.md`).
2. **Write the description with triggers.** This is the most important field. Include 3–5 concrete trigger utterances in quotes - these drive automatic agent selection. Without triggers, the agent is invisible.
3. **Pick a model - or don't.** `name` and `description` are the only required fields; every other field below is optional. When `model` is absent, Claude Code subagents inherit the parent session's model, which is often the right answer. If you do set it, write a **value your runtime accepts** (Claude: `opus` / `sonnet` / `haiku` / `fable` / a full model id / `inherit`). SpecRoute's `flagship` / `balanced` / `fast` tiers are a documentation abstraction for rosters only - never write them into an agent file. Mapping table: [`wiki/Agents.md`](../wiki/Agents.md#semantic-model-tiers).
4. **Decide on web access via `tools`.** There is no `internet:` field - it is not read by any runtime. To let the agent research, include `WebFetch` / `WebSearch` in `tools`; to deny it, omit them from the allowlist or name them in `disallowedTools`.
5. **Pick a color, optionally.** Used by the runtime UI only. Nothing breaks if you omit it.
6. **List `Owns`.** Be specific about file paths and directories. The agent's claim to those files is exclusive.
7. **Write 4–6 operating principles.** Specific. Non-obvious. The kind of guidance you'd give a senior contributor on day one.
8. **Write 2–4 "Don't use for" lines.** These hand off the adjacent concerns to the right neighbor.
9. **Body length.** ~30–50 lines is the sweet spot. Longer agents tend to drift; shorter agents under-specify.

## Porting to another vendor

`name`, `description`, and the whole body are portable. The rest is not - each vendor has its own field set (Codex is TOML with `developer_instructions`; Gemini has `kind` / `temperature`; Kiro has no `color` or `memory`; Cursor has `readonly` / `is_background`). Translate the frontmatter, keep the body. See [`wiki/Frontmatter-Contracts.md`](../wiki/Frontmatter-Contracts.md) for the per-vendor field lists.
