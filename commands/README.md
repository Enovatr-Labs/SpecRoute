# Commands

Slash-invoked operations. Simple, deterministic, no configuration. The user types `/<name>` and gets the same behavior every time.

```
commands/
├── command-template.claude.md           Claude Code: markdown body + description frontmatter
├── command-template.gemini.toml         Gemini CLI: TOML command template (prompt + description)
└── examples/                            worked examples
```

## Per-vendor shape

Commands are **vendor-specific in shape**. There is no single canonical format. Each vendor consumes a different file structure.

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
.gemini/commands/<slug>.toml
```

One TOML file per command. The file name (minus `.toml`) is the command name; subdirectories namespace it (`.gemini/commands/git/commit.toml` -> `/git:commit`):

```toml
description = "<one-line description>"
prompt = """
<the prompt the slash command expands to; use {{args}} for arguments>
"""
```

`prompt` is required; `description` is optional. The `prompt` is the text the command expands to, same paradigm as Claude (not a shell command).

### Codex

Codex has no separate command primitive. The Codex equivalent is a skill with `user-invocable: true` and a clear `argument-hint`.

```
.codex/skills/<slug>/SKILL.md
```

Frontmatter sets `user-invocable: true` and `argument-hint: ""` (or the expected arg shape).

### Kiro / Cursor / Windsurf

These vendors do not have a slash-command concept. For Kiro use hooks for automation. For Cursor and Windsurf, the equivalent is a rule that the agent reads and acts on.

## When to build a command vs alternative

| Question | Answer |
|---|---|
| Does the user type `/<name>` once and get the same result? | **Command** |
| Does the user need to make decisions mid-flow? | **Skill** (interactive) |
| Should it run autonomously without user input? | **Agent** |
| Should it run automatically on an event? | **Hook** |

See [`agentic-docs/automation-decision-framework.md`](../agentic-docs/automation-decision-framework.md) for the 4-row decision matrix and anti-patterns.

## Reference implementations

The four commands under [`.claude/commands/`](../.claude/commands/) at the repository root are real, tracked examples:

- `/audit` - comprehensive pre-commit check
- `/parity` - cross-vendor runtime parity check
- `/sanitize` - sanitization wordlist scan
- `/status` - skeleton state report

Read `audit.md` and `sanitize.md` for the most substantive examples of the markdown shape.

## Authoring agent

Designing and reviewing slash commands is owned by the `command-author` agent. See `.claude/agents/command-author.md` for its operating principles.
