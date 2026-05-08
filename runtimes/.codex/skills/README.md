# `.codex/skills/`

Codex skill registry. Same folder-per-skill `SKILL.md` convention as Claude Code's `.claude/skills/`.

```
.codex/skills/
└── <skill-slug>/
    ├── SKILL.md
    ├── scripts/                     optional
    └── agents/                      optional
```

Frontmatter contract identical to Claude:

```yaml
---
name: <slug>
description: <triggers>
argument-hint: "[arg1] [arg2?]"
user-invocable: true
allowed-tools: Read Write Edit Glob Bash
---
```

## Codex-specific use of `user-invocable`

Codex doesn't have a separate slash-command primitive. Skills with `user-invocable: true` and a clear `argument-hint` play the role Claude commands play.

When mirroring a Claude command into Codex, convert it into a skill:

| Claude side | Codex equivalent |
|---|---|
| `.claude/commands/audit.md` | `.codex/skills/audit/SKILL.md` with `user-invocable: true` |
| `.claude/commands/sanitize.md` | `.codex/skills/sanitize/SKILL.md` with `user-invocable: true` |

The `description` and body content map directly; the frontmatter changes shape.

## Mirroring with Claude

Use `tools/sync-skills.py` to detect drift between `.claude/skills/` and `.codex/skills/`.
