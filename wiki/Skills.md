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

`SKILL.md` frontmatter adheres to the open [Agent Skills standard](https://agentskills.io) ([specification](https://agentskills.io/specification)) - a genuine cross-vendor standard supported by all six vendors SpecRoute targets.

```yaml
---
name: <slug>                             # required by the standard; matches enclosing dir (max 64 chars)
description: <triggers>                  # required by the standard; drives auto-selection (max 1024 chars)
license: MIT                             # optional agentskills.io standard field
compatibility: "Requires bash, git"      # optional agentskills.io standard environment requirements
metadata:                                # optional agentskills.io standard metadata map
  author: "<author-or-team>"
  version: "1.0.0"
# Claude Code extensions - not part of the standard:
allowed-tools: Read Write Edit Glob Bash # optional; PRE-APPROVES these tools, does not restrict
disallowed-tools: Bash                   # optional; the field that actually removes tools
argument-hint: "[arg1] [arg2?]"          # optional argument hint
user-invocable: true                     # optional; menu visibility only
---
```

The standard requires `name` and `description`. Claude Code itself is looser - **no field is strictly required**, and `description` is only "Recommended". SpecRoute treats `name` + `description` as the practical floor, because without a description nothing can auto-select the skill.

The standard caps `description` at 1024 characters. Front-load trigger phrases.

### `allowed-tools` is not a sandbox

The most common misreading of the contract:

- **`allowed-tools` pre-approves.** Listed tools run without a permission prompt for the invoking turn, and the grant clears on the next message. It does **not** remove anything from the tool pool - the skill can still reach for tools you left off the list, they just prompt.
- **`disallowed-tools` restricts.** This is the field that removes tools from the pool for the skill's run.

"Keep `allowed-tools` minimal" is therefore advice about prompt noise and the blast radius of unattended approval, not about confinement. For real confinement use `disallowed-tools`, deny rules in the runtime's permission settings, and a hook for anything security-critical.

Reasonable pre-approval sets:

| Skill type | `allowed-tools` |
|---|---|
| Read-only audit / lint | `Read Glob Grep` |
| File-creating wizard | `Read Write Edit Glob` |
| Shell-driven workflow | `Read Write Edit Glob Grep Bash` |

### Other real optional fields (Claude Code)

`arguments` (structured argument declaration), `disable-model-invocation` (user-only, never auto-selected), `model`, `effort`, `context: fork`, `agent` (run inside a named subagent), `background`, `hooks` (skill-scoped), `paths` (scope the skill to matching paths).

`user-invocable` controls **menu visibility only** - it does not block access via the Skill tool, so it is a discoverability control rather than an access control.

All of these are vendor extensions. Gemini, Kiro, and Cursor consume only `name` + `description`. See [[Frontmatter Contracts]].

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

The table is SpecRoute's design vocabulary, not four file formats. See "Skills have absorbed commands" below.

## Per-vendor mirrors

As of mid-2026 **all six** supported vendors consume folder-per-skill `SKILL.md`:

```
runtimes/.claude/skills/<slug>/SKILL.md
runtimes/.codex/skills/<slug>/SKILL.md
runtimes/.gemini/skills/<slug>/SKILL.md
runtimes/.kiro/skills/<slug>/SKILL.md
runtimes/.cursor/skills/<slug>/SKILL.md
runtimes/.devin/skills/<slug>/SKILL.md
```

Only the frontmatter dialect differs - the body is shared, which is why `tools/sync-skills.py` is body-aware. See [[Vendor Matrix]].

A vendor-neutral **`.agents/skills/`** root is also emerging. It has been
verified directly in Codex and is the recommended repository location in
Devin's documentation. It does not replace every per-vendor directory yet;
re-check other runtime support against current vendor documentation. See
[[Cross-Vendor Sync]].

To check parity across runtimes: `tools/sync-skills.py --dry-run` or the `/parity` command.

## Skills have absorbed commands

In **Claude Code**, skills and commands have merged. `.claude/commands/<name>.md` is legacy-but-supported and takes the **same frontmatter as a skill** - there are effectively two artifact contracts (agent, skill), not three. New work belongs in `.claude/skills/<slug>/SKILL.md`; existing command files need no migration.

In **Codex**, **Kiro**, and **Devin Local** there is no separate command file
in these runtimes: the equivalent is a skill invoked through the runtime's
skill UI (`$name` or `/skills` in Codex, `/skill <name>` in Kiro,
`/skill-name` in Devin Local). Codex's older custom-prompts feature is
deprecated in favour of skills.

**Cursor** and **Gemini CLI** do still have distinct command artifacts.
Devin Desktop's Cascade agent retains compatibility workflows under
`.windsurf/workflows/`. See [[Commands]].

## Plugins

Claude Code, Codex, Cursor, and Gemini CLI all support **plugins** installed from a marketplace. A plugin bundles artifacts - typically some mix of skills, subagents, commands, hooks, and MCP server definitions - behind a manifest so they install and update as one unit.

For authors this changes distribution, not authoring: the `SKILL.md` inside a plugin is the same `SKILL.md` documented above. SpecRoute's `runtimes/` layouts are deliberately copy-paste templates rather than plugins, because they are meant to be edited by the consuming project. Packaging is the better option once a skill set has stabilised and you want other teams to consume it unchanged. Manifest formats differ per vendor and are still moving.

## Reference implementations

The six contributor skills in this repo's own `.claude/skills/` are real, tracked examples:

- [`scaffold-artifact`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/skills/scaffold-artifact/SKILL.md) — interactive scaffolding for any artifact type.
- [`add-vendor`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/skills/add-vendor/SKILL.md) — walks through adding a new agent CLI to the matrix.
- [`example-walkthrough`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/skills/example-walkthrough/SKILL.md) — guided build of `examples/sample-project/`.
- [`frontmatter-lint`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/skills/frontmatter-lint/SKILL.md) — interactive frontmatter validation with offered fixes.
- [`all-hands`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/skills/all-hands/SKILL.md) — routes multi-specialist work across the implementation roster.
- [`doc-currency-check`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/skills/doc-currency-check/SKILL.md) — checks version anchors, vendor facts, counts, tense, and matrix mirrors.

## Owner agent

Designing and reviewing skills is owned by the `skill-author` agent.

## Invoking a skill

In Claude Code both prefixes work once the skill is registered:

```
/all-hands review the changes        # skill / command menu
@all-hands review the changes        # mention picker — lists files AND registered skills
```

A correctly registered skill appears in the `@` picker with type **Skill**. If you see only
directories and no `Skill` row, it did not register — and the cause is almost always frontmatter
or location, not the body:

| Symptom | Cause |
|---|---|
| No `Skill` row in the `@` picker | `disable-model-invocation: true` removes the skill from the model-facing registry the picker completes against. Omit it unless you want the skill reachable *only* from `/`. |
| Skill silently absent in Codex | The skill lives somewhere no CLI reads. `runtimes/.<vendor>/` is a **template**; Codex reads `.codex/skills/`, `.agents/skills/`, or `$CODEX_HOME/skills`. |
| Tools unavailable at runtime | In Claude Code, `allowed-tools` is a space-separated scalar (`Read Grep Glob Bash Agent`) or a YAML list. Stale names such as `Task` fail silently. Other runtimes keep their native frontmatter. |
| Skill never matches | The folder name must equal the `name` field. |

A newly created skill may not appear in the interactive picker until the session restarts — the
autocomplete registry is built at startup.

Per-runtime prefixes differ: Codex uses `$name` or the `/skills` menu, Kiro uses `/skill <name>`.
Each skill's own `SKILL.md` carries the full table.

## See also

- [[Agents]] · [[Commands]] · [[Hooks]] — the other three primitives
- [[Automation Decision Framework]] — when to build a skill vs agent vs command vs hook
- [[Implementation Team]] — the six contributor skills in `.claude/skills/`
- [[Frontmatter Contracts]] — full required-field reference
