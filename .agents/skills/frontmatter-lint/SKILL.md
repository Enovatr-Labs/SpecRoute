---
name: frontmatter-lint
description: Validates YAML frontmatter across SpecRoute artifacts (agents, skills, commands) against the per-artifact contract. Reports missing required fields, malformed YAML, and drift between similar artifacts. Use proactively before commits, when reviewing PRs, or when an agent/skill/command isn't loading correctly.
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
- `runtimes/.codex/agents/*.toml`, `runtimes/.codex/skills/*/SKILL.md`
- `runtimes/.gemini/agents/*.md`, `runtimes/.kiro/agents/*.md`, `runtimes/.cursor/agents/*.md`, `runtimes/.devin/agents/*/AGENT.md`
- `examples/sample-project/.claude/agents/*.md`, `examples/sample-project/.codex/agents/*.toml`

## Step 2: Apply contracts

Agent and skill frontmatter contracts are **vendor-specific** since the mid-2026 convergence - do not apply Claude's contract to every vendor's artifacts.

### Agent contract

**Claude** (`.claude/agents/`, `agents/examples/`, `runtimes/.claude/agents/*.md`) - **only `name` and `description` are required**:

- `name` - slug, lowercase-hyphenated, matches filename (without `.md`). Required.
- `description` - non-empty string, must include trigger phrases. Required.
- `model` - **optional**; default `inherit`. Valid: `opus`, `sonnet`, `haiku`, `fable`, a full model id matching `^claude-[a-z0-9.-]+$` (e.g. `claude-opus-5`), or `inherit`.
- `color` - **optional**; cosmetic only. Valid: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan`.
- Other optional fields, all valid: `tools`, `disallowedTools`, `skills`, `memory` (`user`|`project`|`local`), `effort` (`low`|`medium`|`high`|`xhigh`|`max`), `isolation` (`worktree`), `permissionMode`, `maxTurns`, `mcpServers`, `hooks`, `background`, `initialPrompt`.

Two **errors** specific to SpecRoute's history - flag these explicitly:

- `model: flagship | balanced | fast` - the semantic tiers are a SpecRoute documentation abstraction, **not** a Claude Code value. An agent file carrying one is broken. Suggest the mapped id: `flagship`→`opus`, `balanced`→`sonnet`, `fast`→`haiku` (canonical table: `wiki/Agents.md`).
- `internet: Yes | No` - not a field any runtime reads. Flag as an error in agent *files*; it is fine in roster *tables*, which are documentation. Suggested fix: delete the field, and if the intent was `Yes`, add `WebFetch` / `WebSearch` to `tools`.

Do **not** flag a missing `model` or a missing `color` as an error. At most, note a missing `color` as a style nit on consumer-facing examples.

**Codex** (`runtimes/.codex/agents/*.toml`): TOML, not YAML - require `name`, `description`, `developer_instructions`. Optional: `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`. Flag Claude's `color` / `memory` / `internet` as invalid if present.

**Other vendors** validate loosely - valid YAML frontmatter with a non-empty `name` and `description`; do **not** require Claude's `model`/`color`:
- Gemini `runtimes/.gemini/agents/*.md` - `name`, `description` (+ optional `kind`, `tools`, `model`, `temperature`)
- Cursor `runtimes/.cursor/agents/*.md` - `name`, `description` (+ optional `model`, `readonly`)
- Kiro `runtimes/.kiro/agents/*.md` - `name`, `description` (+ optional `tools`, `model`, `includeMcpJson`)
- Devin `runtimes/.devin/agents/<name>/AGENT.md` - `name`, `description` (+ optional `model`, `allowed-tools`)

### Skill contract

The Agent Skills open standard requires only `name` (matches enclosing directory, max 64 chars) + `description` (non-empty, max 1024 chars) everywhere. Extra fields are vendor-specific and **optional**:
- **Claude** (`runtimes/.claude/skills/`): `argument-hint`, `user-invocable` (boolean), and `allowed-tools` are optional vendor extensions - warn if absent on a consumer-facing example, but never report them as errors. `allowed-tools` *pre-approves* tools for the invoking turn; it does not restrict them. The restricting field is `disallowed-tools`.
- **Codex / Gemini / Kiro / Cursor**: SpecRoute templates carry `name` + `description` only. Flag Claude's `argument-hint` / `user-invocable` / `allowed-tools` as foreign to these shipped templates; do not claim that every vendor parser rejects them.
- **Devin Local**: `name`, `description` (+ optional `argument-hint`, `allowed-tools`, `triggers`).

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
6. For agents: if `model` is **present**, check it is a value that vendor accepts. A missing `model` is valid everywhere (inheritance is the default) - do not report it.
7. For agents: flag any field the vendor does not define (`internet` anywhere; `color`/`memory` outside Claude).

Canonical templates are an intentional exception to value and filename checks:

- `agents/agent-template.md` deliberately uses placeholders such as
  `name: <slug-lowercase-hyphenated>` and `model: <vendor model id>`.
- `skills/skill-template/SKILL.md` deliberately uses `name: <skill-slug>`.

Still parse their frontmatter and require the normal fields, but do not report
placeholder values, placeholder model ids, or template filename/name mismatches as
errors or warnings. Do not replace those markers with invented content; they are the
template's fill-in contract.

For Gemini TOML: parse the file as TOML, check `prompt` is present and non-empty.

## Step 4: Report

Group findings by severity:

- **Errors** (would prevent loading): missing required field, malformed YAML/JSON/TOML, name/filename mismatch
- **Warnings** (degrades discoverability): description without triggers, missing optional fields on consumer-facing examples
- **Drift** (cross-runtime mismatch): a skill is missing from one of the six declared runtime targets, or its body differs. Vendor-native frontmatter differences are expected and are not body drift.

Output as a punch list: file path, field, issue, suggested fix.

## Step 5: Offer fixes

For trivial errors (missing required field, name/filename mismatch), offer to apply the fix automatically. Always ask before writing.

## Don't use for

- Linting body content (that's `template-quality-reviewer`).
- Sanitization checks (that's `sanitization-auditor` or the `/sanitize` command).
- Lint of arbitrary YAML files outside the agent/skill/command contracts.
