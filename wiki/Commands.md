# Commands

<!-- sources: commands/README.md -->

Slash-invoked operations. Simple, deterministic, no configuration. The user types `/<name>` and gets the same behavior every time.

For the canonical reference, see [`commands/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/commands/README.md).

## The command primitive is being absorbed by skills

"Command" is increasingly a *role*, not a file format:

| Vendor | Distinct command artifact? |
|---|---|
| Claude Code | **No longer really.** Commands and skills have merged - `.claude/commands/<name>.md` is legacy-but-supported and takes the **same frontmatter as a skill**. Two artifact contracts (agent, skill), not three. |
| Codex | No separate command file. Use a skill invoked with `$name` or from `/skills`. |
| Kiro | Never had one. A command is a skill invoked via `/skill`. |
| Cursor | Yes - `.cursor/commands/<slug>.md`. |
| Gemini CLI / Antigravity | Yes - `.gemini/commands/<slug>.toml`, a genuinely different shape. |
| Devin Desktop | No separate Devin Local command file. Use a skill invoked as `/skill-name`; Cascade compatibility workflows remain at `.windsurf/workflows/<slug>.md`. |

SpecRoute keeps `commands/` as a design category, but on Claude, Codex, Kiro,
and Devin Local the artifact you actually author is a skill.

## Per-vendor shape

For the vendors that do have a distinct artifact, the shapes differ.

### Claude Code

```
.claude/commands/<slug>.md      # legacy-but-supported
.claude/skills/<slug>/SKILL.md  # current form
```

Both are read and **both take skill frontmatter** - nothing is strictly required, `description` is recommended, and the same optional set applies in either location (`argument-hint`, `arguments`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `disable-model-invocation`, `model`, `effort`, `context: fork`, `agent`, `background`, `hooks`, `paths`). A minimal command is still:

```yaml
---
description: <one-line description shown in the command list>
---
```

Body is the prompt that the slash command expands to. Body can include shell snippets in fenced code blocks; Claude executes them with explanation.

`allowed-tools` here **pre-approves** tools for the invoking turn - it does not restrict what the command can reach for. See [[Skills]].

Prefer `.claude/skills/<slug>/SKILL.md` for new work: same contract, actively developed location, and you get a folder for supporting scripts. Existing command files need no migration.

### Gemini CLI

```
.gemini/commands/<name>.toml
```

TOML file per command (the old `gemini_cli_config.json` JSON command map is gone):

```toml
prompt = "<the prompt the command expands to>"
description = "<one-line description>"   # optional
```

`prompt` is required; `description` is optional. Subdirectories namespace the command — `.gemini/commands/git/commit.toml` is invoked as `/git:commit`.

### Codex

Codex has no separate command file in this framework. The equivalent is a skill with portable `name` / `description` frontmatter, invoked with `$name` or from `/skills`:

```
.codex/skills/<slug>/SKILL.md
.agents/skills/<slug>/SKILL.md   # also read; vendor-neutral root
```

Codex's older custom-prompts feature is deprecated in favour of skills - don't author new prompt files.

### Cursor

```
.cursor/commands/<slug>.md
```

Markdown custom slash commands, alongside Cursor's `.cursor/skills/` skills, `.cursor/agents/` subagents, and `.cursor/hooks.json` hooks.

### Kiro / Devin Desktop

Kiro has no command artifact - operations that would be slash commands are skills (`.kiro/skills/<slug>/SKILL.md`) invoked via `/skill`, with steering rules and hooks for the automated cases.

Devin Local uses `.devin/skills/<slug>/SKILL.md` (or the recommended
`.agents/skills/` location), invoked as `/skill-name`. Devin Desktop's Cascade
agent still supports workflows at `.windsurf/workflows/<slug>.md`; that literal
path is a compatibility surface, not a separate runtime. Devin Local does not
support Cascade workflows, so migrate reusable procedures to skills.

## When to build a command vs alternative

| Question | Answer |
|---|---|
| Does the user type `/<name>` once and get the same result? | **Command** |
| Does the user need to make decisions mid-flow? | **Skill** (interactive) |
| Should it run autonomously without user input? | **Agent** |
| Should it run automatically on an event? | **Hook** |

This table still earns its keep - one-shot versus interactive shapes how you write the thing. It just no longer implies a different file format on Claude Code, Codex, or Kiro, where both answers produce a skill.

See [[Automation Decision Framework]] for the full matrix.

## Reference implementations

The four commands under this repo's own `.claude/commands/` are real, tracked examples:

- [`/audit`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/commands/audit.md) — comprehensive pre-commit check.
- [`/parity`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/commands/parity.md) — cross-vendor runtime parity check.
- [`/sanitize`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/commands/sanitize.md) — sanitization wordlist scan.
- [`/status`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/commands/status.md) — skeleton state report.

Read `audit.md` and `sanitize.md` for the most substantive examples of the markdown shape.

## Templates

- Claude: [`commands/command-template.claude.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/commands/command-template.claude.md)
- Gemini: [`commands/command-template.gemini.toml`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/commands/command-template.gemini.toml)

## Owner agent

Designing and reviewing slash commands is owned by the `command-author` agent.

## See also

- [[Skills]] · [[Agents]] · [[Hooks]] — the other three primitives
- [[Automation Decision Framework]] — when to reach for a command vs alternatives
- [[Vendor Matrix]] — which vendors consume commands and in what shape
