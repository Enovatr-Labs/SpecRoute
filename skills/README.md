# Skills

Interactive, parameterized workflows. A skill guides the user through a multi-step task with prompts at decision points and validation checkpoints. Skills are **interactive by design** - that's what distinguishes them from agents (autonomous), commands (one-shot deterministic), and hooks (event-triggered).

```
skills/
├── skill-template/
│   └── SKILL.md                         canonical template with full frontmatter
└── examples/
    └── <skill-name>/
        ├── SKILL.md                     required
        ├── scripts/                     optional supporting scripts
        └── agents/                      optional skill-scoped sub-agents
```

## Folder-per-skill convention

Every skill is a directory containing `SKILL.md`. Never a single flat file.

```
skills/examples/scaffold-artifact/
├── SKILL.md                             required
├── scripts/                             optional
│   └── helpers.sh
└── agents/                              optional
    └── sub-agent.md
```

The directory name is the skill slug. The slug is what users invoke (e.g. `scaffold-artifact`). It must match the `name` field in `SKILL.md`'s frontmatter.

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

**`allowed-tools` should be the minimum set.** Don't grant Bash by default. Common sets:

| Skill type | `allowed-tools` |
|---|---|
| Read-only audit / lint | `Read Glob Grep` |
| File-creating wizard | `Read Write Edit Glob` |
| Shell-driven workflow | `Read Write Edit Glob Grep Bash` |

## Topic categorization

Do **not** use a topic-based directory taxonomy (`skills/coding/`, `skills/testing/`, `skills/security/`, etc.). The folder is the skill, full stop.

If you need to categorize for discovery:

- Tag skills via filename prefix or naming convention (e.g. `lint-*`, `audit-*`, `scaffold-*`).
- Maintain a topic index in this README.
- Add a "category" field to frontmatter if your runtime supports it.

## Skills vs agents vs commands vs hooks

Picking the wrong primitive produces friction. See [`docs/automation-decision-framework.md`](../docs/automation-decision-framework.md) for the 4-row matrix.

Quick distinctions:

| Primitive | Interactive? | Autonomous? | Deterministic? | Event-driven? |
|---|---|---|---|---|
| **Skill** | Yes | No | No | No |
| Agent | No | Yes | No | No |
| Command | Optional (one arg) | No | Yes | No |
| Hook | No | No | Yes (per event) | Yes |

A workflow that asks no questions is an agent or command, not a skill. A workflow that runs automatically on file edits is a hook, not a skill.

## Per-vendor mirrors

Skills are mirrored into:

- `runtimes/.claude/skills/<slug>/SKILL.md` - Claude Code reads from here.
- `runtimes/.codex/skills/<slug>/SKILL.md` - Codex reads from here.

Gemini CLI does not consume `SKILL.md`-format skills. Kiro, Cursor, and Windsurf do not either. To check that the two runtimes that *do* support skills stay aligned, run `tools/sync-skills.py --dry-run` or invoke `/parity`.

## Authoring agent

Designing and reviewing skills is owned by the `skill-author` agent. See `.claude/agents/skill-author.md` for its operating principles.

## Related documents

- [`skills/skill-template/SKILL.md`](skill-template/SKILL.md) - fill-in-the-blanks template
- [`skills/examples/README.md`](examples/README.md) - adding an example skill
- [`docs/automation-decision-framework.md`](../docs/automation-decision-framework.md) - when to build a skill vs agent vs command vs hook
