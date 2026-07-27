# `.agents/` - the vendor-neutral runtime root

This directory makes SpecRoute's own implementation skills available to agent CLIs that are
**not** Claude Code. It is a live runtime, not a template.

```
.agents/
└── skills/<slug>/SKILL.md        mirrors .claude/skills/, minus Claude-only frontmatter
```

## Why it exists

`.agents/skills/` is the emerging vendor-neutral **repo-level skills root**. Codex reads it (the
0.145.0 binary carries it as a skills root alongside `.codex/skills` and `$CODEX_HOME/skills`), and
Gemini CLI, Cursor, Devin Desktop and Copilot are converging on the same location.

Before this existed, running Codex inside this repository found **no skills at all**. Everything
Codex-shaped lived under `runtimes/.codex/`, which is a copy-pasteable *template* for consumers -
no CLI reads that path. The symptom was a skill that looked correctly authored and simply never
appeared in Codex's picker.

**`runtimes/.<vendor>/` is what consumers copy. `.claude/` and `.agents/` are what this repository
actually runs.** Don't confuse the two.

## What is mirrored, and what is not

`.agents/skills/` mirrors [`.claude/skills/`](../.claude/skills/) - the six implementation skills
that build SpecRoute. It does **not** mirror `runtimes/.claude/skills/`, which holds the two
consumer-facing examples. Those are different sets on purpose, which is why
[`tools/sync-skills.py`](../tools/sync-skills.py) does not cover this directory: that tool syncs the
`runtimes/` layouts against each other.

The **body is identical**; only frontmatter differs. `.agents/` carries the Agent Skills
(`agentskills.io`) minimum - `name`, `description`, and `when_to_use` where useful - and drops
Claude-only fields such as `allowed-tools` and `argument-hint`, which other runtimes either ignore
or reject.

## Keeping it in sync

`/parity` reports drift between `.claude/skills/` and `.agents/skills/`. After editing a skill in
either place, re-run it. A skill present in one and missing from the other is a real defect: it
means the capability exists on one runtime and silently does not on the others.

## What is still missing for Codex

The `all-hands` skill routes over an agent roster. This repository's twelve agents are Claude
Markdown in `.claude/agents/`; **there is no `.codex/agents/<slug>.toml` equivalent yet**. Codex can
still run `all-hands`: it reads the selected `.claude/agents/<slug>.md` as a role brief and creates
a bounded collaboration task with `spawn_agent`. The collaboration `task_name` is a unique
lowercase-underscore workstream identifier, **not** a pre-registered roster slug or
`subagent_type`. Codex therefore preserves the role's instructions through the spawned prompt, but
it cannot dispatch to pre-registered named specialists the way Claude Code does. Porting the roster
to TOML is tracked as outstanding work, not something this directory solves.
