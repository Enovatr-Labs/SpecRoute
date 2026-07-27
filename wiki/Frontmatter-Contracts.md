# Frontmatter Contracts

<!-- sources: agents/README.md, skills/README.md, commands/README.md, prds/README.md, specs/README.md -->

The frontmatter reference for every SpecRoute artifact that has a contract.

**Read the Required vs Conventional split below carefully.** SpecRoute requires `name` and `description` on published agents and skills as its portable baseline; some vendor parsers accept less. `model`, `color`, `argument-hint`, `user-invocable`, and `allowed-tools` are vendor-specific conventions, not universal requirements. PRD and spec frontmatter is different: those fields gate the lifecycle, not the runtime.

## Agent (Claude Code)

File: `agents/examples/<name>.md`, `runtimes/.claude/agents/<name>.md`, `.claude/agents/<name>.md`.

**Only `name` and `description` are required.** Every other field is optional with a runtime default.

```yaml
---
name: <slug>                            # required; matches filename (without .md)
description: <triggers>                 # required; must include trigger phrases for auto-selection
model: opus                             # optional; default `inherit`
tools: Read, Grep, Glob                 # optional; allowlist
disallowedTools: Write, Edit            # optional; denylist, applied before `tools`
skills: [frontmatter-lint]              # optional; skill content preloaded into the subagent
memory: project                         # optional; user | project | local
effort: high                            # optional; low | medium | high | xhigh | max
isolation: worktree                     # optional; run in a dedicated git worktree
permissionMode: <mode>                  # optional; permission posture for the subagent
color: yellow                           # optional; UI tint only
---
```

- `name` must match the filename (case-sensitive).
- `description` must include trigger phrases in quotes (literal user utterances). Without triggers, automatic agent selection won't pick the agent up.
- `model` accepts `opus` | `sonnet` | `haiku` | `fable`, a full model id (e.g. `claude-opus-5`), or `inherit`. **Default is `inherit`** - the subagent runs on the parent session's model. `flagship` / `balanced` / `fast` are SpecRoute's own tier vocabulary and are **not** valid values here; see the mapping table in [[Agents]].
- `color` is **optional** - it only tints the agent in the runtime UI. Valid: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan`.

### The optional fields worth knowing

| Field | What it does |
|---|---|
| `tools` | Allowlist of tools the subagent may use. Omit to inherit the parent's tool set. |
| `disallowedTools` | Denylist. Applied **before** `tools`, so it wins on conflict. This is how you actually take a tool away. |
| `skills` | Skill names whose content is preloaded into the subagent's context. |
| `memory` | `user` \| `project` \| `local` - which memory store the agent reads and writes. See [[Agent Memory]]. |
| `effort` | `low` \| `medium` \| `high` \| `xhigh` \| `max` - reasoning budget. Pair a `balanced` model with high effort instead of reaching for a bigger model. |
| `isolation` | `worktree` runs the subagent in its own git worktree - useful for agents that write code in parallel. |
| `permissionMode` | Permission posture for the subagent, independent of the parent session. |

Also available: `maxTurns`, `mcpServers`, `hooks` (subagent-scoped), `background`, `initialPrompt`.

**There is no `internet` field.** Web access is granted or withheld via `tools` / `disallowedTools` (`WebFetch`, `WebSearch`). Roster tables may keep an "Internet" column as documentation of intent, but it must not appear in agent frontmatter - the runtime ignores it.

### Agent (other vendors)

Each vendor has its own agent contract; do not apply Claude's fields elsewhere.

| Vendor | File | Fields |
|---|---|---|
| Codex | `.codex/agents/<name>.toml` | TOML, not YAML. Required `name`, `description`, `developer_instructions`; optional `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`. |
| Gemini CLI | `.gemini/agents/<name>.md` | Required `name`, `description`; optional `kind`, `tools`, `mcpServers`, `model`, `temperature`, `max_turns`, `timeout_mins`. |
| Kiro | `.kiro/agents/<name>.md` | Required `name`; optional `description`, `tools`, `model`, `includeMcpJson`, `includePowers`. No `color` / `memory`. |
| Cursor | `.cursor/agents/<name>.md` | All optional: `name` (defaults to filename), `description`, `model` (default `inherit`), `readonly`, `is_background`. |
| Devin Desktop | `.devin/agents/<name>/AGENT.md` | `name`, `description`; optional `model`, `allowed-tools`, `permissions`, `max-nesting`. |

## Skill

File: `skills/examples/<slug>/SKILL.md`, `runtimes/.claude/skills/<slug>/SKILL.md`, `runtimes/.codex/skills/<slug>/SKILL.md`.

Skill frontmatter follows the open [Agent Skills standard](https://agentskills.io), which requires only `name` and `description`. Claude Code's own reference is looser still - no field is strictly required, with `description` merely recommended. SpecRoute treats `name` + `description` as the practical floor, because without a description nothing can auto-select the skill.

```yaml
---
name: <slug>                             # required; matches enclosing directory name (max 64 chars)
description: <triggers>                  # required in practice; drives auto-selection (max 1024 chars)
license: MIT                             # optional; agentskills.io standard field
compatibility: "Requires bash, git"      # optional; agentskills.io environment requirements
metadata:                                # optional; agentskills.io metadata map
  author: "<author-or-team>"
  version: "1.0.0"
# Claude Code extensions:
allowed-tools: Read Write Edit Glob Bash # optional; pre-approves tools, does NOT restrict them
disallowed-tools: Bash                   # optional; removes tools from the pool
argument-hint: "[arg1] [arg2?]"          # optional
user-invocable: true                     # optional
---
```

- `name` must match the enclosing directory name.
- **`allowed-tools` does not confine the skill.** It *pre-approves* those tools for the invoking turn so the user isn't prompted; the grant clears on the next message. The field that removes a tool from the pool is `disallowed-tools`. Listing a short `allowed-tools` is a convenience, not a sandbox - don't rely on it for confinement.
- `argument-hint` and `user-invocable` are **Claude Code extensions**, not portable fields. The shipped Codex / Gemini / Kiro / Cursor templates omit them.

Other Claude Code optional fields worth knowing:

| Field | What it does |
|---|---|
| `arguments` | Structured argument declaration (beyond the free-text `argument-hint`). |
| `disable-model-invocation` | Skill can only be run by the user, never auto-selected by the model. |
| `disallowed-tools` | Tools removed from the pool for this skill. |
| `model` | Pin the skill to a specific model. |
| `effort` | Reasoning budget for the skill's run. |
| `context: fork` | Run the skill in a forked context so it doesn't consume the main thread. |
| `agent` | Run the skill inside a named subagent. |
| `background` | Run the skill as a background task. |
| `hooks` | Skill-scoped hooks. |
| `paths` | Scope the skill to matching paths. |

See [[Skills]] for the folder-per-skill convention.

## Command (Claude Code)

File: `commands/examples/<name>.claude.md`, `.claude/commands/<name>.md`, `runtimes/.claude/commands/<name>.md`.

```yaml
---
description: <one-line description shown in /help>
---
```

**Commands and skills have merged in Claude Code.** `.claude/commands/<name>.md` is legacy-but-supported and takes the *same* frontmatter as a skill — the full optional set above is available here too, and nothing is strictly required. `description` remains the one field worth always setting, since it is what `/help` shows. The body of the file is the prompt the command expands to.

For new work, prefer a skill: same invocation, same frontmatter, plus bundled resource files. Converting an existing command is a file move, not a header rewrite. See [[Commands]].

## Command (Gemini)

File: `commands/command-template.gemini.toml`, `.gemini/commands/<name>.toml`.

Not frontmatter — TOML keys (the old `gemini_cli_config.json` command map is gone):

```toml
prompt = "<the prompt the command expands to>"   # required
description = "<one-line description>"            # optional
```

Subdirectories namespace the command: `.gemini/commands/git/commit.toml` is invoked as `/git:commit`.

## PRD

File: `prds/active/<slug>.md`, `prds/archive/<year>-<slug>.md`.

```yaml
---
Version: 0.1
Date: YYYY-MM-DD
Author: <name>
Status: Draft | Under Review | Approved | In Implementation | Shipped | Deprecated
Architecture Reference: <link or "TODO">
Scope: <one-line scope statement>
---
```

A PRD without `Status` is not actionable. A PRD without `Architecture Reference` is missing context downstream stages need.

## Spec (requirements, design, tasks, feature-spec, technical-spec, ADR)

File: `specs/<feature>/{requirements,design,tasks}.md`, etc.

```yaml
---
Version: 0.1
Date: YYYY-MM-DD
Author: <name>
Status: Draft | Approved | In Implementation | Complete
Source PRD: <link>
Source Requirements: requirements.md   # design.md and tasks.md only
Source Design: design.md               # tasks.md only
---
```

ADRs additionally have:

```yaml
Status: Proposed | Accepted | Superseded
Supersedes: <link to prior ADR>        # only when superseding
```

## Cursor rule (MDC)

File: `.cursor/rules/<name>.mdc`.

```yaml
---
description: <one-line>
alwaysApply: true              # OR
globs: ["src/**/*.tsx"]        # for context-aware loading
---
```

## Kiro steering

File: `.kiro/steering/<name>.md`.

```yaml
---
inclusion: always              # OR
inclusion: fileMatch
globs: ["**/*.py"]             # required when inclusion: fileMatch
---
```

## Devin Desktop rule

File: `.devin/rules/<name>.md`. Cascade also accepts the compatibility path
`.windsurf/rules/<name>.md`.

```yaml
---
trigger: always_on             # OR
trigger: glob
globs: ["**/*.tsx"]            # required when trigger: glob
---
```

Use `trigger: model_decision` when Cascade should load the rule from its
description without a file pattern; `globs` belongs only to `trigger: glob`.

## Validation

The PostToolUse hook in this repo's `.claude/hooks/post-edit-frontmatter.sh` validates agent / skill / command frontmatter on write — surfaces violations on stderr but doesn't block (soft hook). The `frontmatter-lint` skill provides interactive validation.

For a comprehensive pre-commit sweep that includes frontmatter checks, run `/audit`.

## See also

- [[Agents]] · [[Skills]] · [[Commands]] · [[PRDs]] · [[Specs]]
- [[Sanitization]] — the other load-bearing pre-commit check
- [[Implementation Team]] — `frontmatter-lint` skill + PostToolUse hook
