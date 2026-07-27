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

`SKILL.md` frontmatter adheres to the open [Agent Skills standard](https://agentskills.io) ([specification](https://agentskills.io/specification)) - a genuine cross-vendor standard supported by all six vendors SpecRoute targets:

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

The standard requires `name` and `description`. Claude Code itself is looser - **no field is strictly required**, and `description` is only "Recommended". SpecRoute treats `name` + `description` as the practical floor anyway, because without a description nothing can auto-select the skill and the slug is the only thing left to match on.

The standard caps `description` at 1024 characters. Front-load the trigger phrases.

### `allowed-tools` is not a sandbox

This is the single most common misreading of the skill contract:

- **`allowed-tools` pre-approves.** The listed tools run without a permission prompt for the invoking turn, and the grant clears on the next message. It does **not** remove anything from the tool pool - the skill can still use tools you left off the list, they just prompt.
- **`disallowed-tools` restricts.** This is the field that removes tools from the pool for the skill's run.

So "keep `allowed-tools` minimal" is advice about *prompt noise and blast radius of unattended approval*, not about confinement. A read-only lint skill that lists only `Read Glob Grep` is well-scoped in intent; it is not prevented from asking to run Bash. If a skill genuinely must not touch something, use `disallowed-tools`, plus deny rules in the runtime's permission settings and a hook for anything security-critical.

Reasonable starting points for the pre-approval list:

| Skill type | `allowed-tools` |
|---|---|
| Read-only audit / lint | `Read Glob Grep` |
| File-creating wizard | `Read Write Edit Glob` |
| Shell-driven workflow | `Read Write Edit Glob Grep Bash` |

### Other real optional fields (Claude Code)

Beyond the above, Claude Code accepts: `arguments` (structured argument declaration), `disable-model-invocation` (user-only, never auto-selected), `model`, `effort`, `context: fork` (run in a forked context), `agent` (run inside a named subagent), `background`, `hooks` (skill-scoped hooks), and `paths` (scope the skill to matching paths).

Note that `user-invocable` controls **menu visibility only**. Setting it to `false` hides the skill from the invocation menu but does not block access via the Skill tool - it is a discoverability control, not an access control.

All of these are Claude Code extensions. The shipped Codex, Gemini, Kiro, and Cursor templates keep the portable `name` + `description` baseline; `tools/sync-skills.py` preserves each target's own frontmatter for exactly this reason.

## Topic categorization

Do **not** use a topic-based directory taxonomy (`skills/coding/`, `skills/testing/`, `skills/security/`, etc.). The folder is the skill, full stop.

If you need to categorize for discovery:

- Tag skills via filename prefix or naming convention (e.g. `lint-*`, `audit-*`, `scaffold-*`).
- Maintain a topic index in this README.
- Add a "category" field to frontmatter if your runtime supports it.

## Skills vs agents vs commands vs hooks

Picking the wrong primitive produces friction. See [`agentic-docs/automation-decision-framework.md`](../agentic-docs/automation-decision-framework.md) for the 4-row matrix.

Quick distinctions:

| Primitive | Interactive? | Autonomous? | Deterministic? | Event-driven? |
|---|---|---|---|---|
| **Skill** | Yes | No | No | No |
| Agent | No | Yes | No | No |
| Command | Optional (one arg) | No | Yes | No |
| Hook | No | No | Yes (per event) | Yes |

A workflow that asks no questions is an agent or command, not a skill. A workflow that runs automatically on file edits is a hook, not a skill.

The table describes SpecRoute's design vocabulary, not four separate file formats. In Claude Code the skill and command *artifacts have merged*: `.claude/commands/<name>.md` is legacy-but-supported and takes the same frontmatter as a skill. Codex and Kiro have no separate command file here; the user invokes the equivalent skill through the runtime's skill UI (`$name` or `/skills` in Codex, `/skill <name>` in Kiro). See [`commands/README.md`](../commands/README.md).

## Per-vendor mirrors

As of mid-2026, all six supported vendors (Claude Code, Codex, Gemini/Antigravity, Kiro, Cursor, Devin Desktop) consume folder-per-skill `SKILL.md` artifacts under `runtimes/.<vendor>/skills/<slug>/SKILL.md`.

A vendor-neutral `.agents/skills/` root is also emerging and has been verified directly in Codex. It does not replace the per-vendor directories yet; re-check other runtime support against current vendor documentation. See [`agentic-docs/cross-vendor-sync.md`](../agentic-docs/cross-vendor-sync.md).

To check that skill Markdown bodies stay in sync across all runtime layouts, run `tools/sync-skills.py --dry-run` or invoke `/parity`.

## Skills as plugins

Claude Code, Codex, Cursor, and Gemini CLI now support **plugins** installed from a marketplace. A plugin is a *packaging and distribution* format: it bundles artifacts - typically some combination of skills, subagents, commands, hooks, and MCP server definitions - so they install as a unit instead of being copied file by file.

For skill authors this changes distribution, not authoring: the `SKILL.md` inside a plugin is the same `SKILL.md` documented above. SpecRoute's runtime layouts under `runtimes/.<vendor>/` remain copy-paste layouts rather than plugins, because they are meant to be read and edited as a starting point. If you want to hand a finished skill set to other teams, packaging it as a plugin is the better delivery mechanism - check your vendor's current plugin manifest format, which is still moving.

## Authoring agent

Designing and reviewing skills is owned by the `skill-author` agent. See `.claude/agents/skill-author.md` for its operating principles.

## Related documents

- [`skills/skill-template/SKILL.md`](skill-template/SKILL.md) - fill-in-the-blanks template
- [`skills/examples/README.md`](examples/README.md) - adding an example skill
- [`agentic-docs/automation-decision-framework.md`](../agentic-docs/automation-decision-framework.md) - when to build a skill vs agent vs command vs hook

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
- **Claude Code `allowed-tools` is a space-separated scalar** (`Read Grep Glob Bash Agent`) or a YAML list. Comma separation
  and stale tool names (`Task` was superseded by `Agent`) fail silently.
- **The folder name must equal the `name` field.**

Each skill's `SKILL.md` carries a per-runtime invocation table.
