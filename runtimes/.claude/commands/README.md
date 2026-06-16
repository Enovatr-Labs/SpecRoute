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

See [`agentic-docs/automation-decision-framework.md`](../../../agentic-docs/automation-decision-framework.md) for the full matrix.

## Vendor support

As of mid-2026 all six vendors support custom commands, in their native shapes:

| Vendor | Command shape |
|---|---|
| Claude Code | `.claude/commands/<name>.md` (frontmatter + body) |
| Codex | a skill invoked via `/skills` or `$mention` |
| Gemini CLI | `.gemini/commands/<name>.toml` (`prompt` + `description`) |
| Kiro | a skill invoked via `/skill` (+ manual steering) |
| Cursor | `.cursor/commands/<name>.md` |
| Windsurf / Devin | `.windsurf/workflows/<name>.md` / `.devin/workflows/<name>.md` (invoked `/<name>`) |

When mirroring to Codex, convert to a skill folder under `.codex/skills/<slug>/SKILL.md`. See [`review-spec.md`](review-spec.md) for a worked example command.
