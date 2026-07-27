# Devin Desktop Rules

For Devin Local, the recommended project rules file is `AGENTS.md`. It is
loaded automatically and can be nested for directory-scoped context.
`AGENTS.local.md` is the personal, gitignored companion.

```text
project/
├── AGENTS.md
├── AGENTS.local.md                 personal; do not commit
└── src/
    └── AGENTS.md                   loaded when work enters src/
```

Keep always-on rules small. Prefer a skill when instructions are only useful
for a particular workflow.

## Cascade compatibility

Devin Desktop's Cascade agent also reads `.devin/rules/*.md` and accepts
`.windsurf/rules/*.md` as a fallback. Cascade rule frontmatter uses these
activation values:

| `trigger` | Behavior |
|---|---|
| `always_on` | Include the full rule on every message |
| `model_decision` | Load when the description appears relevant |
| `glob` | Load when a read or edit matches `globs` |
| `manual` | Load when the user mentions the rule |

```yaml
---
description: Test conventions for TypeScript files
trigger: glob
globs: "src/**/*.test.ts"
---
```

SpecRoute retains `runtimes/.devin/rules/` only for this Cascade-facing surface.
It does not ship a separate Windsurf rule guide or runtime.

## Other Devin Desktop artifacts

- Skills: `.devin/skills/<slug>/SKILL.md` or `.agents/skills/<slug>/SKILL.md`.
- Subagents: `.devin/agents/<name>/AGENT.md` (experimental).
- Hooks: `.devin/hooks.v1.json`.
- MCP: `.devin/config.json` under `mcpServers`.
- Commands: skills invoked as `/skill-name`.

Cascade's `.windsurf/workflows/`, `.windsurf/hooks.json`, and
`~/.codeium/windsurf/mcp_config.json` are compatibility paths during the
transition. Devin Local workflows should be migrated to skills.

## See also

- [`engineering-rules.md`](engineering-rules.md) — vendor-neutral engineering rules.
- [`runtimes/.devin/README.md`](../runtimes/.devin/README.md) — the Devin Desktop runtime.
- [`hooks/README.md`](../hooks/README.md) — cross-vendor hook taxonomy.
