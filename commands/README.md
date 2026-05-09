# Commands

Slash-invoked operations. Simple, deterministic, no configuration. The user types `/<name>` and gets the same behavior every time.

```
commands/
├── command-template.claude.md           Claude Code: markdown body + description frontmatter
├── command-template.gemini.json         Gemini CLI: full command config template
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
.gemini/gemini_cli_config.json
```

JSON file with a top-level `commands` object:

```json
{
  "commands": {
    "<slug>": {
      "command": "<shell command to run>",
      "description": "<one-line description>",
      "directory": "<optional working directory>"
    }
  }
}
```

The `command` is a literal shell command, not a prompt. Different paradigm from Claude.

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

See [`docs/automation-decision-framework.md`](../docs/automation-decision-framework.md) for the 4-row decision matrix and anti-patterns.

## Reference implementations

The four commands under [`.claude/commands/`](../.claude/commands/) at the repository root are real, tracked examples:

- `/audit` - comprehensive pre-commit check
- `/parity` - cross-vendor runtime parity check
- `/sanitize` - sanitization wordlist scan
- `/status` - skeleton state report

Read `audit.md` and `sanitize.md` for the most substantive examples of the markdown shape.

## Authoring agent

Designing and reviewing slash commands is owned by the `command-author` agent. See `.claude/agents/command-author.md` for its operating principles.
