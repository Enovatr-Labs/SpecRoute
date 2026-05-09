---
name: frontmatter-lint
description: Validates YAML frontmatter across SpecForge artifacts (agents, skills, commands) against the per-artifact contract. Reports missing required fields, malformed YAML, and drift between similar artifacts. Use proactively before commits, when reviewing PRs, or when an agent/skill/command isn't loading correctly.
argument-hint: "[path?]"
user-invocable: true
allowed-tools: Read Glob Grep Bash
---

# Frontmatter Lint

Validates the YAML frontmatter contract on every agent / skill / command file. Frontmatter is load-bearing - Claude Code, Codex, and Gemini won't register artifacts that fail the contract.

## When to use

- Before committing changes to `.claude/agents/`, `agents/examples/`, `skills/examples/`, `commands/examples/`, or any `runtimes/.<vendor>/` directory
- When an agent, skill, or command isn't auto-selected and the user expected it to be
- During PR review

## Step 1: Determine scope

If the argument is a path, lint that path. Otherwise lint all of:

- `.claude/agents/*.md`
- `agents/examples/*.md`, `agents/agent-template.md`
- `skills/skill-template/SKILL.md`, `skills/examples/*/SKILL.md`
- `commands/examples/*.claude.md`, `commands/command-template.claude.md`
- `runtimes/.claude/agents/*.md`, `runtimes/.claude/skills/*/SKILL.md`, `runtimes/.claude/commands/*.md`
- `runtimes/.codex/agents/*.md`, `runtimes/.codex/skills/*/SKILL.md`

## Step 2: Apply contracts

### Agent contract (`.claude/agents/`, `agents/examples/`, `runtimes/.<vendor>/agents/`)

Required:
- `name` - slug, lowercase-hyphenated, matches filename (without `.md`)
- `description` - non-empty string, must include trigger phrases
- `model` - one of `opus`, `sonnet`, `haiku`
- `color` - recognized color name

Optional (warn if missing on consumer-facing examples):
- `memory` - `project` | `user` | absent
- `internet` - `Yes` | `No` | absent

### Skill contract (`skills/examples/<name>/SKILL.md`, `runtimes/.<vendor>/skills/<name>/SKILL.md`)

Required:
- `name` - slug, must match enclosing directory name
- `description` - non-empty
- `argument-hint` - non-empty (use `""` if no argument expected)
- `user-invocable` - boolean
- `allowed-tools` - non-empty space-separated string

### Command contract (Claude `commands/examples/*.claude.md`, `runtimes/.claude/commands/*.md`)

Required:
- `description` - non-empty

### Command contract (Gemini `commands/examples/*.gemini.json`, `runtimes/.gemini/gemini_cli_config.json` entries)

Each command map entry requires:
- `command` - non-empty shell string
- `description` - non-empty
- `directory` - optional path

## Step 3: Run the checks

For each file:

1. Extract frontmatter (between `---` delimiters at file start).
2. Parse as YAML.
3. Validate required fields per contract.
4. Check `name`/filename consistency.
5. Check `description` for at least one trigger phrase pattern (e.g. quoted utterance, `Triggers - "..."`).
6. For agents: check `model` is in the allowed set.

For Gemini JSON: parse the file as JSON, walk the `commands` map.

## Step 4: Report

Group findings by severity:

- **Errors** (would prevent loading): missing required field, malformed YAML/JSON, name/filename mismatch
- **Warnings** (degrades discoverability): description without triggers, missing optional fields on consumer-facing examples
- **Drift** (cross-runtime mismatch): a skill exists in `runtimes/.claude/skills/` but not `runtimes/.codex/skills/`, or has different frontmatter between the two

Output as a punch list: file path, field, issue, suggested fix.

## Step 5: Offer fixes

For trivial errors (missing required field, name/filename mismatch), offer to apply the fix automatically. Always ask before writing.

## Don't use for

- Linting body content (that's `template-quality-reviewer`).
- Sanitization checks (that's `sanitization-auditor` or the `/sanitize` command).
- Lint of arbitrary YAML files outside the agent/skill/command contracts.
