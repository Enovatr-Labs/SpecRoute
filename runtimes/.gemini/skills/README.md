# `.gemini/skills/` - Gemini CLI skills

One folder per skill, each containing a `SKILL.md`. Gemini follows the Agent Skills open standard, so the layout matches `.claude/skills/`. Skills are enabled by default in current Gemini CLI builds.

```
.gemini/skills/
└── <slug>/
    └── SKILL.md
```

## Frontmatter contract

Gemini's SKILL.md frontmatter is just the two Agent Skills open-standard keys:

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Slug matching the folder name. |
| `description` | Yes | Include trigger phrases so the model knows when to invoke; this is what Gemini uses for discovery. |

Gemini does **not** use Claude's `argument-hint`, `user-invocable`, or `allowed-tools` skill fields - drop them when porting. Skills are activated via the `activate_skill` tool, not exposed as slash commands (use `.gemini/commands/*.toml` for those).

## Porting from `.claude/skills/`

The body is portable. Strip the Claude-only frontmatter (`argument-hint`, `user-invocable`, `allowed-tools`) down to `name` + `description`. Use `tools/sync-skills.py` to keep the body in sync across runtimes - it is body-aware and preserves each vendor's own frontmatter.

`audit-artifact/` ships here as a worked reference. Replace or extend it with your project's skills.
