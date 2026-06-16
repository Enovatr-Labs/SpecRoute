# Commands

<!-- sources: commands/README.md -->

Slash-invoked operations. Simple, deterministic, no configuration. The user types `/<name>` and gets the same behavior every time.

For the canonical reference, see [`commands/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/commands/README.md).

## Per-vendor shape

Commands are **vendor-specific in shape**. There is no single canonical format — each vendor consumes a different file structure.

### Claude Code

```
.claude/commands/<slug>.md
```

Markdown file. Frontmatter:

```yaml
---
description: <one-line description shown in /help>
---
```

Body is the prompt that the slash command expands to. Body can include shell snippets in fenced code blocks; Claude executes them with explanation.

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

Codex has no separate command primitive. The equivalent is a skill with `user-invocable: true` and a clear `argument-hint`:

```
.codex/skills/<slug>/SKILL.md
```

### Cursor

```
.cursor/commands/*.md
```

Markdown custom slash commands, alongside `.cursor/skills/` `SKILL.md` skills.

### Kiro / Windsurf

Kiro invokes skills via `/skill` plus manual steering. Windsurf uses `.windsurf/workflows/*.md` (invoked as `/workflow-name`) and Cascade `SKILL.md` skills.

## When to build a command vs alternative

| Question | Answer |
|---|---|
| Does the user type `/<name>` once and get the same result? | **Command** |
| Does the user need to make decisions mid-flow? | **Skill** (interactive) |
| Should it run autonomously without user input? | **Agent** |
| Should it run automatically on an event? | **Hook** |

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
