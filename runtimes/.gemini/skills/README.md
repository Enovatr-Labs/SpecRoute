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
