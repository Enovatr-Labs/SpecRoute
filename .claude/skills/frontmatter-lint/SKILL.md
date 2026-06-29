---
name: frontmatter-lint
description: Validates YAML frontmatter across SpecRoute artifacts (agents, skills, commands) against the per-artifact contract. Reports missing required fields, malformed YAML, and drift between similar artifacts. Use proactively before commits, when reviewing PRs, or when an agent/skill/command isn't loading correctly.
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

Agent and skill frontmatter contracts are **vendor-specific** since the mid-2026 convergence - do not apply Claude's contract to every vendor's artifacts.

### Agent contract

**Claude** (`.claude/agents/`, `agents/examples/`, `runtimes/.claude/agents/*.md`):
- `name` - slug, lowercase-hyphenated, matches filename (without `.md`)
- `description` - non-empty string, must include trigger phrases
- `model` - one of `opus`, `sonnet`, `haiku`
- `color` - recognized color name
- Optional: `memory` (`project`|`user`), `internet` (`Yes`|`No`)

**Codex** (`runtimes/.codex/agents/*.toml`): TOML, not YAML - require `name`, `description`, `developer_instructions`.

**Other vendors** validate loosely - valid YAML frontmatter with a non-empty `name` and `description`; do **not** require Claude's `model`/`color`:
- Gemini `runtimes/.gemini/agents/*.md` - `name`, `description` (+ optional `kind`, `tools`, `model`, `temperature`)
- Cursor `runtimes/.cursor/agents/*.md` - `name`, `description` (+ optional `model`, `readonly`)
- Kiro `runtimes/.kiro/agents/*.md` - `name`, `description` (+ optional `tools`, `model`, `includeMcpJson`)
- Devin `runtimes/.devin/agents/<name>/AGENT.md` - `name`, `description` (+ optional `model`, `allowed-tools`)

### Skill contract

The Agent Skills open standard requires only `name` (matches enclosing directory) + `description` (non-empty) everywhere. Extra fields are vendor-specific:
- **Claude / Codex** (`runtimes/.claude/skills/`, `runtimes/.codex/skills/`, `skills/examples/<name>/SKILL.md`): also require `argument-hint`, `user-invocable` (boolean), `allowed-tools` (non-empty).
- **Gemini / Kiro / Cursor**: `name` + `description` only - flag Claude's `argument-hint`/`user-invocable`/`allowed-tools` as **invalid** if present.
- **Windsurf / Devin**: `name`, `description` (+ optional `argument-hint`, `allowed-tools`, `triggers`).

### Command contract (Claude `commands/examples/*.claude.md`, `runtimes/.claude/commands/*.md`)

Required:
- `description` - non-empty

### Command contract (Gemini `commands/examples/*.gemini.toml`, `runtimes/.gemini/commands/*.toml`)

Each TOML command file requires:
- `prompt` - non-empty string (the text the command expands to)
- `description` - optional one-line string

## Step 3: Run the checks

For each file:

1. Extract frontmatter (between `---` delimiters at file start).
2. Parse as YAML.
3. Validate required fields per contract.
4. Check `name`/filename consistency.
5. Check `description` for at least one trigger phrase pattern (e.g. quoted utterance, `Triggers - "..."`).
6. For agents: check `model` is in the allowed set.

For Gemini TOML: parse the file as TOML, check `prompt` is present and non-empty.

## Step 4: Report

Group findings by severity:

- **Errors** (would prevent loading): missing required field, malformed YAML/JSON/TOML, name/filename mismatch
- **Warnings** (degrades discoverability): description without triggers, missing optional fields on consumer-facing examples
- **Drift** (cross-runtime mismatch): a skill exists in `runtimes/.claude/skills/` but not `runtimes/.codex/skills/`, or has different frontmatter between the two

Output as a punch list: file path, field, issue, suggested fix.

## Step 5: Offer fixes

For trivial errors (missing required field, name/filename mismatch), offer to apply the fix automatically. Always ask before writing.

## Don't use for

- Linting body content (that's `template-quality-reviewer`).
- Sanitization checks (that's `sanitization-auditor` or the `/sanitize` command).
- Lint of arbitrary YAML files outside the agent/skill/command contracts.
