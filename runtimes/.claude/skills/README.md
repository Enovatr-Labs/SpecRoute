# `.claude/skills/` - Claude Code skill registry

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
argument-hint: "[arg1] [arg2?]"           # optional; "" if no args
user-invocable: true                      # optional; false hides it from the menu
allowed-tools: Read Write Edit Glob Bash  # optional; PRE-APPROVES these for the turn
disallowed-tools: Bash                    # optional; this is what actually restricts
---
```

See [`skills/skill-template/SKILL.md`](../../../skills/skill-template/SKILL.md) for the canonical template.

## When to build a skill

A skill is **interactive and parameterized**. The user invokes it; the skill walks them through decisions. If the workflow:

- Has zero user input → use an agent (autonomous) or command (one-shot).
- Runs on an event → use a hook.
- Asks one well-defined question and otherwise deterministic → use a command.

See [`agentic-docs/automation-decision-framework.md`](../../../agentic-docs/automation-decision-framework.md) for the full decision matrix.

## Mirroring across runtimes

All six supported runtimes consume folder-per-skill `SKILL.md` artifacts.
Mirror skills into each runtime's native directory and use
`tools/sync-skills.py` to compare or copy the portable body while preserving
vendor-specific frontmatter.

## Invoking a skill

Use your runtime's skill prefix. In Claude Code both work once the skill is registered:

```
/all-hands review the changes        # skill/command menu
@all-hands review the changes        # mention picker - lists files AND registered skills
```

A correctly registered skill appears in the `@` picker with type **Skill**. If you see only
directories and no `Skill` row, it did not register - and the cause is almost always
frontmatter:

- **`disable-model-invocation: true` hides it** from the model-facing registry the `@` picker
  completes against. Omit it unless you want the skill reachable *only* from the `/` menu.
- **`allowed-tools` is comma-separated** (`Read, Grep, Glob, Bash, Agent`). Space separation
  and stale tool names (`Task` was superseded by `Agent`) fail silently.
- **The folder name must equal the `name` field.**

Each skill's `SKILL.md` carries a per-runtime invocation table.
