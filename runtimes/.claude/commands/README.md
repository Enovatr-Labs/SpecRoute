# `.claude/commands/` - Claude Code slash commands

Drop your project's slash commands here. Each command is a flat `<name>.md` file with YAML frontmatter and a body. Users invoke as `/<name>`.

## File shape

```markdown
---
description: <one-line description shown in /help>
---

<2–3 sentence overview of what this command does.>

## What this command does

- <Action 1>
- <Action 2>

## Implementation

```bash
# Inline shell commands. Deterministic - same input, same output.
echo "Running <command>..."
<your shell or python here>
```

## Output

<What the user sees. Tables, status indicators, punch lists.>
```

See [`commands/command-template.claude.md`](../../../commands/command-template.claude.md) for the canonical template.

## When to build a command vs alternative

- Command: deterministic, no parameters or one well-defined arg, every invocation behaves the same.
- Skill: interactive, asks the user questions.
- Agent: autonomous, runs to completion.
- Hook: triggered by an event, not user-invoked.

See [`docs/automation-decision-framework.md`](../../../docs/automation-decision-framework.md) for the full matrix.

## Vendor support

Slash commands are a Claude Code primitive. Codex's equivalent is a skill with `user-invocable: true`. Gemini's equivalent is a JSON entry in `gemini_cli_config.json`. Kiro / Cursor / Windsurf don't have slash commands.

When mirroring to Codex, convert to a skill folder under `.codex/skills/<slug>/SKILL.md` with `user-invocable: true`.
