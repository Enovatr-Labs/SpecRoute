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
- `runtimes/.codex/agents/*.toml`, `runtimes/.codex/skills/*/SKILL.md`
- `runtimes/.gemini/agents/*.md`, `runtimes/.kiro/agents/*.md`, `runtimes/.cursor/agents/*.md`, `runtimes/.devin/agents/*/AGENT.md`
- `examples/sample-project/.claude/agents/*.md`, `examples/sample-project/.codex/agents/*.toml`

## Step 2: Apply contracts

Agent frontmatter contracts are **vendor-specific** since the 2026 capability convergence - do not apply Claude's contract to every vendor's artifacts. Skill frontmatter is the exception: its core is the vendor-neutral [Agent Skills standard](https://agentskills.io/specification), identical everywhere, with a thin per-vendor layer on top.

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

The [Agent Skills open standard](https://agentskills.io/specification) requires exactly two fields, `name` and `description`, in every runtime. Validate them by the standard's own rules, not by eye:

| Field | Required | Rule |
|---|---|---|
| `name` | yes | 1-64 chars. Lowercase alphanumerics (`a`-`z`, `0`-`9`) and hyphens only. Must not start or end with a hyphen. Must not contain consecutive hyphens (`pdf--processing` is invalid). **Must match the enclosing directory name exactly** - the standard's one hard structural rule. |
| `description` | yes | 1-1024 chars, non-empty. |
| `license` | no | License name or a reference to a bundled license file. |
| `compatibility` | no | Environment requirements. Max 500 chars. |
| `metadata` | no | Map of string keys to string values. |
| `allowed-tools` | no | **Standard field, marked (Experimental)** - a space-separated string of pre-approved tools whose support varies between implementations. |

Two classification traps to get right when reporting:

- **`allowed-tools` is part of the standard, not a Claude Code extension.** Never label it one. Because the standard marks it Experimental, its **absence is never a finding** - not an error, not a warning. Only flag it when it is present and malformed (comma-separated instead of space-separated, or a stale tool name such as `Task`, superseded by `Agent`).
- **`argument-hint` and `user-invocable` genuinely are Claude Code extensions.** Their absence is also not an error; at most a style nit on a consumer-facing Claude example.

Behaviour worth restating in any finding that touches it: `allowed-tools` *pre-approves* tools for the invoking turn and does **not** remove anything from the tool pool. The field that actually restricts is `disallowed-tools`. Do not describe a short `allowed-tools` list as a sandbox.

Per-vendor layer on top of the standard:

- **Claude** (`.claude/skills/`, `runtimes/.claude/skills/`): may additionally carry `argument-hint`, `user-invocable` (boolean), `disallowed-tools`, `arguments`, `disable-model-invocation`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`. All optional.
- **Codex / Gemini / Kiro / Cursor** (`runtimes/.<vendor>/skills/`, `.agents/skills/`): SpecRoute templates carry `name` + `description` only. If `argument-hint` or `user-invocable` appears, note it as a Claude Code extension foreign to the shipped template. If `allowed-tools` appears, note only that the shipped template omits it - it is a standard field, so do not call it a Claude extension, and do not claim that every vendor parser rejects it.
- **Devin Local**: `name`, `description` (+ optional `argument-hint`, `allowed-tools`, `triggers`).

The standard also sets progressive-disclosure budgets: frontmatter metadata is always loaded (~100 tokens), the body loads on activation and should stay under 5000 tokens, and the main `SKILL.md` should stay under 500 lines. Report a `SKILL.md` over 500 lines as a **warning** with the suggestion to move detail into `references/` or `scripts/`.

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

### Skill-specific checks (every `SKILL.md`, every vendor)

The standard's rules are mechanical, so check them mechanically rather than reading the value:

1. **`name` matches the enclosing directory.** `basename(dirname(path))` must equal `name` exactly. This is the standard's one hard structural rule and the most common real defect - report a mismatch as an **error**.
2. **`name` length** is 1-64 characters.
3. **`name` charset** is `a`-`z`, `0`-`9`, and `-` only. Uppercase, underscores, dots, and spaces are errors.
4. **`name` has no leading or trailing hyphen.** `-audit` and `audit-` are errors.
5. **`name` has no consecutive hyphens.** `pdf--processing` is an error; `pdf-processing` is fine.
6. **`description` is non-empty and at most 1024 characters.**
7. **`compatibility`, if present, is at most 500 characters.**
8. **`metadata`, if present, is a flat map of string keys to string values** - nested maps and non-string values are errors.
9. **`allowed-tools`, if present, is a space-separated string** (or, in Claude Code only, a YAML list). Comma separation is an error. Its **absence is never reported**.
10. **Body length**: warn if `SKILL.md` exceeds 500 lines (progressive-disclosure budget).

Checks 2-5 collapse to one regex on the whole value: `^[a-z0-9]+(-[a-z0-9]+)*$` with a length of 1-64. That single pattern rejects uppercase, underscores, edge hyphens, and consecutive hyphens at once - use it, and only fall back to explaining which specific rule failed when reporting the finding.

```bash
# Quick sweep: name-vs-directory, name charset/hyphen/length, body budget.
# The canonical template is skipped for name-value checks - its `name: <skill-slug>`
# placeholder is the template's fill-in contract, not a defect.
find . -name SKILL.md -not -path './.git/*' | while read -r f; do
  dir=$(basename "$(dirname "$f")")
  name=$(sed -n '/^name:/{s/^name:[[:space:]]*//;s/[[:space:]]*#.*$//;s/[[:space:]]*$//;p;q;}' "$f")
  if [ "$f" != "./skills/skill-template/SKILL.md" ]; then
    [ "$dir" = "$name" ] || echo "  ERROR $f: name '$name' != directory '$dir'"
    printf '%s' "$name" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$' \
      || echo "  ERROR $f: name '$name' violates the standard's charset/hyphen rules"
    [ "${#name}" -le 64 ] || echo "  ERROR $f: name exceeds 64 characters"
  fi
  [ "$(wc -l < "$f")" -le 500 ] || echo "  WARN  $f: over 500 lines (progressive-disclosure budget)"
done
```

Optionally, cross-check a single skill against the published standard with the Agent Skills reference validator from the `skills-ref` library (`skills-ref validate ./my-skill`). It is an **external, optional** tool - this repository has no toolchain and does not require it, so never treat its absence as a failure or wire it into a gate.

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

- **Errors** (would prevent loading or violate the standard): missing required field, malformed YAML/JSON/TOML, name/filename or name/directory mismatch, `name` violating the standard's length / charset / hyphen rules, `description` over 1024 chars, `compatibility` over 500 chars
- **Warnings** (degrades discoverability or blows a budget): description without triggers, a `SKILL.md` over 500 lines, a missing optional *Claude* field on a consumer-facing Claude example. Never warn on a missing `allowed-tools` - the standard marks it Experimental, and warning on its absence pushes contributors toward a field no runtime is obliged to honour.
- **Drift** (cross-runtime mismatch): a skill is missing from one of the six declared runtime targets, or its body differs. Vendor-native frontmatter differences are expected and are not body drift.

Output as a punch list: file path, field, issue, suggested fix.

## Step 5: Offer fixes

For trivial errors (missing required field, name/filename mismatch), offer to apply the fix automatically. Always ask before writing.

## Don't use for

- Linting body content (that's `template-quality-reviewer`).
- Sanitization checks (that's `sanitization-auditor` or the `/sanitize` command).
- Lint of arbitrary YAML files outside the agent/skill/command contracts.
