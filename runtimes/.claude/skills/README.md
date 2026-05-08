# `.claude/skills/` — Claude Code skill registry

Drop your project's skills here. Each skill is a directory containing `SKILL.md`. Optional sibling dirs (`scripts/`, `agents/`) hold supporting files.

## Folder-per-skill convention

```
.claude/skills/
└── <skill-slug>/
    ├── SKILL.md                     required
    ├── scripts/                     optional
    │   └── helpers.sh
    └── agents/                      optional
        └── sub-agent.md
```

The directory name is the slug. The slug must match the `name` field in `SKILL.md`'s frontmatter.

## Frontmatter contract

```yaml
---
name: <slug>                              # required; matches enclosing dir
description: <triggers>                   # required; trigger phrases drive auto-selection
argument-hint: "[arg1] [arg2?]"           # required; "" if no args
user-invocable: true                      # required; true unless invoked by other skills/agents
allowed-tools: Read Write Edit Glob Bash  # required; minimum tool set
---
```

See [`skills/skill-template/SKILL.md`](../../../skills/skill-template/SKILL.md) for the canonical template.

## When to build a skill

A skill is **interactive and parameterized**. The user invokes it; the skill walks them through decisions. If the workflow:

- Has zero user input → use an agent (autonomous) or command (one-shot).
- Runs on an event → use a hook.
- Asks one well-defined question and otherwise deterministic → use a command.

See [`docs/automation-decision-framework.md`](../../../docs/automation-decision-framework.md) for the full decision matrix.

## Mirroring to Codex

Codex consumes the same `SKILL.md` shape. Mirror skills into `.codex/skills/<slug>/SKILL.md`. Use `tools/sync-skills.py` to diff/copy.

Gemini, Kiro, Cursor, Windsurf do not consume `SKILL.md` skills.
