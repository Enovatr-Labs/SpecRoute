# `.codex/skills/`

Codex skill registry. Same folder-per-skill `SKILL.md` convention as Claude Code's `.claude/skills/`.

```
.codex/skills/
└── <skill-slug>/
    ├── SKILL.md
    ├── scripts/                     optional
    └── agents/                      optional
```

SpecRoute's shipped Codex frontmatter uses the portable baseline:

```yaml
---
name: <slug>
description: <triggers>
---
```

Keep the argument contract and required capabilities in the body. Do not copy
Claude Code's `argument-hint`, `user-invocable`, or `allowed-tools` fields into
Codex unless current Codex documentation explicitly adds them.

## Codex skill invocation

Codex has no separate command file in this framework. Invoke a skill with `$name`
or select it from `/skills`. When mirroring a Claude command, convert it into a
skill and move any argument hint into the body:

| Claude side | Codex equivalent |
|---|---|
| `.claude/commands/audit.md` | `.codex/skills/audit/SKILL.md`, invoked as `$audit` |
| `.claude/commands/sanitize.md` | `.codex/skills/sanitize/SKILL.md`, invoked as `$sanitize` |

The `description` and body content map directly; the frontmatter changes shape.

## Mirroring with Claude

Use `tools/sync-skills.py` to detect drift between `.claude/skills/` and `.codex/skills/`.

## `all-hands` on Codex - read before using it

`all-hands` is the multi-agent orchestration skill: one user-invoked coordinator that fans work
across the agents in your roster. Its shared body is portable, but **the dispatch step is not**,
and Codex differs from Claude Code in a way that matters.

Claude Code dispatches with `subagent_type: <slug>`. Codex uses its collaboration spawning
facility instead: pass the portable roster slug and the role brief in the spawned task prompt,
then route follow-ups and synthesize the returned results. Registered TOML profiles remain
Codex-native; Claude's `subagent_type` argument does not carry over.

Two consequences for this layout:

- **Subagents live at `.codex/agents/<slug>.toml`**, not as Markdown with YAML frontmatter. The
  roster the coordinator routes over is that directory. See [`../agents/README.md`](../agents/README.md).
- **Do not copy Claude's `allowed-tools`.** `Task` and `Agent` are Claude Code tool names; the
  shipped [`all-hands/SKILL.md`](all-hands/SKILL.md) keeps Codex frontmatter to the portable
  `name` / `description` baseline.

Reference: <https://learn.chatgpt.com/docs/agent-configuration/subagents>

## Invoking a skill

Use `$name` or the `/skills` menu:

```
$all-hands review the changes
```

The folder name must equal the `name` field. Each skill's body carries its argument
contract and per-runtime dispatch notes.
