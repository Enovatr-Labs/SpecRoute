# Frontmatter Contracts

<!-- sources: agents/README.md, skills/README.md, commands/README.md, prds/README.md, specs/README.md -->

The required-field reference for every SpecRoute artifact with a frontmatter contract. Missing fields = the artifact won't register in the runtime (for agents/skills/commands) or won't satisfy the lifecycle gates (for PRDs/specs).

## Agent

File: `agents/examples/<name>.md`, `runtimes/.claude/agents/<name>.md`, `runtimes/.codex/agents/<name>.md`.

```yaml
---
name: <slug>                            # required; matches filename (without .md)
description: <triggers>                 # required; must include trigger phrases for auto-selection
model: opus | sonnet | haiku            # required
color: <recognized color>               # required
memory: project | user | absent         # optional
internet: Yes | No | absent             # optional
---
```

- `name` must match the filename (case-sensitive).
- `description` must include trigger phrases in quotes (literal user utterances). Without triggers, automatic agent selection won't pick the agent up.
- `model` choice: see [[Agents]].
- `color` distinguishes the agent in the runtime UI. Pick something memorable.

## Skill

File: `skills/examples/<slug>/SKILL.md`, `runtimes/.claude/skills/<slug>/SKILL.md`, `runtimes/.codex/skills/<slug>/SKILL.md`.

```yaml
---
name: <slug>                             # required; matches enclosing directory name
description: <triggers>                  # required; trigger phrases drive auto-selection
argument-hint: "[arg1] [arg2?]"          # required; "" if no args
user-invocable: true                     # required; true unless invoked by other skills/agents
allowed-tools: Read Write Edit Glob Bash # required; minimum tool set
---
```

- `name` must match the enclosing directory name.
- `allowed-tools` must be the **minimum** set the skill needs. Don't grant `Bash` by default. See [[Skills]] for common combinations.

## Command (Claude Code)

File: `commands/examples/<name>.claude.md`, `.claude/commands/<name>.md`, `runtimes/.claude/commands/<name>.md`.

```yaml
---
description: <one-line description shown in /help>
---
```

The Claude command frontmatter is minimal — only `description` is required. The body of the file is the prompt the command expands to.

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

## Windsurf rule

File: `.windsurf/rules/<name>.md`.

```yaml
---
trigger: always                # OR
trigger: model-decision
globs: ["**/*.tsx"]            # required when trigger: model-decision
---
```

## Validation

The PostToolUse hook in this repo's `.claude/hooks/post-edit-frontmatter.sh` validates agent / skill / command frontmatter on write — surfaces violations on stderr but doesn't block (soft hook). The `frontmatter-lint` skill provides interactive validation.

For a comprehensive pre-commit sweep that includes frontmatter checks, run `/audit`.

## See also

- [[Agents]] · [[Skills]] · [[Commands]] · [[PRDs]] · [[Specs]]
- [[Sanitization]] — the other load-bearing pre-commit check
- [[Implementation Team]] — `frontmatter-lint` skill + PostToolUse hook
