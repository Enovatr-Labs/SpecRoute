# Skills

<!-- sources: skills/README.md -->

Interactive, parameterized workflows. A skill guides the user through a multi-step task with prompts at decision points and validation checkpoints. Skills are **interactive by design** — that's what distinguishes them from agents (autonomous), commands (one-shot deterministic), and hooks (event-triggered).

For the canonical reference, see [`skills/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/skills/README.md).

## Folder-per-skill convention

Every skill is a **directory** containing `SKILL.md`. Never a flat file.

```
skills/examples/scaffold-artifact/
├── SKILL.md                             required
├── scripts/                             optional supporting scripts
│   └── helpers.sh
└── agents/                              optional skill-scoped sub-agents
    └── sub-agent.md
```

The directory name is the skill slug. The slug is what users invoke (e.g. `scaffold-artifact`). It **must match** the `name` field in `SKILL.md`'s frontmatter.

## Frontmatter contract

```yaml
---
name: <slug>                             # required; matches enclosing dir name
description: <triggers>                  # required; trigger phrases drive auto-selection
argument-hint: "[arg1] [arg2?]"          # required; "" if no args
user-invocable: true                     # required; true unless invoked by other skills/agents
allowed-tools: Read Write Edit Glob Bash # required; minimum tool set
---
```

Missing any required field and the skill won't register in Claude Code or Codex.

### `allowed-tools` should be the minimum set

Don't grant `Bash` by default. Common sets:

| Skill type | `allowed-tools` |
|---|---|
| Read-only audit / lint | `Read Glob Grep` |
| File-creating wizard | `Read Write Edit Glob` |
| Shell-driven workflow | `Read Write Edit Glob Grep Bash` |

## No topic-based directory taxonomy

Do **not** create `skills/coding/`, `skills/testing/`, `skills/security/`, etc. The folder is the skill, full stop.

If you need to categorize for discovery:

- Tag skills via filename prefix (`lint-*`, `audit-*`, `scaffold-*`).
- Maintain a topic index in the directory README.
- Add a `category` field to frontmatter if your runtime supports it.

## Quick comparison

| Primitive | Interactive? | Autonomous? | Deterministic? | Event-driven? |
|---|---|---|---|---|
| **Skill** | Yes | No | No | No |
| Agent | No | Yes | No | No |
| Command | Optional (one arg) | No | Yes | No |
| Hook | No | No | Yes (per event) | Yes |

A workflow that asks no questions is an agent or command, not a skill. A workflow that runs automatically on file edits is a hook, not a skill.

## Per-vendor mirrors

Skills are mirrored into:

- `runtimes/.claude/skills/<slug>/SKILL.md` — Claude Code reads from here.
- `runtimes/.codex/skills/<slug>/SKILL.md` — Codex reads from here.

Gemini CLI, Kiro, Cursor, and Windsurf do **not** consume `SKILL.md`-format skills. See [[Vendor Matrix]].

To check parity between the two runtimes: `tools/sync-skills.py --dry-run` or `/parity` command. See [[Cross-Vendor Sync]].

## Codex equivalent of Claude commands

Codex doesn't have a separate command primitive. Operations that would be Claude commands are Codex skills with `user-invocable: true` and a clear `argument-hint`. Don't pretend Codex has Claude-style commands — document the equivalence.

## Reference implementations

The four contributor skills in this repo's own `.claude/skills/` are real, tracked examples:

- [`scaffold-artifact`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/skills/scaffold-artifact/SKILL.md) — interactive scaffolding for any artifact type.
- [`add-vendor`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/skills/add-vendor/SKILL.md) — walks through adding a new agent CLI to the matrix.
- [`example-walkthrough`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/skills/example-walkthrough/SKILL.md) — guided build of `examples/sample-project/`.
- [`frontmatter-lint`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/skills/frontmatter-lint/SKILL.md) — interactive frontmatter validation with offered fixes.

## Owner agent

Designing and reviewing skills is owned by the `skill-author` agent.

## See also

- [[Agents]] · [[Commands]] · [[Hooks]] — the other three primitives
- [[Automation Decision Framework]] — when to build a skill vs agent vs command vs hook
- [[Implementation Team]] — the four contributor skills in `.claude/skills/`
- [[Frontmatter Contracts]] — full required-field reference
