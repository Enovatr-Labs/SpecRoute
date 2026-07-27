---
description: <one-line description of what this command does. Pattern - "Run X and report Y." Used by Claude Code to display the command in /help and to inform when auto-selection is appropriate.>
---

<2–3 sentence overview of what this command does. Commands are simple, non-parameterized operations - if your idea has multiple modes or asks the user questions, it's a skill, not a command.>

## What this command does

<Bullet list of concrete actions, in order:>

- <Action 1>
- <Action 2>
- <Action 3>

## Implementation

```bash
# Inline shell commands the slash command runs.
# Keep this section deterministic - same input, same output, every time.

echo "── Running <command> ──"

<your shell or python here>

echo "── Done ──"
```

## Output

<What the user sees. Make it scannable - tables, status indicators (✓ / ✗), or punch lists.>

## When to use

- <Situation 1>
- <Situation 2>

## Don't use for

- Operations with multiple modes - those are skills.
- Operations that require user input mid-flow - those are skills.
- Operations that should run automatically - those are hooks.

---

## How to fill this template

1. **Pick a slug.** Lowercase, hyphen-separated. Filename is `<slug>.md`. The slash command users type is `/<slug>`.

2. **Write the description.** One concise line. This shows up in `/help`.

3. **Write the body.** Markdown explaining what the command does, followed by the actual implementation in a fenced code block. The body is the prompt that the slash command expands to - Claude Code interprets it.

4. **Output is structured.** Tables, status markers, punch lists. Don't make the user parse paragraphs.

5. **Keep the frontmatter to `description`** unless you need more. Claude Code's commands and skills have merged, so this file accepts the **full skill frontmatter** (`argument-hint`, `allowed-tools`, `disallowed-tools`, `model`, `context: fork`, and the rest - see [`skills/skill-template/SKILL.md`](../skills/skill-template/SKILL.md)). Nothing is strictly required; `description` is recommended because it is what the command list shows. Reach for the extra fields only when the command genuinely needs them - a command whose header grows a decision surface is a skill.

6. **Mirror to the runtime.** Place the production version under `runtimes/.claude/commands/<slug>.md`.

7. **Consider writing it as a skill instead.** `.claude/commands/<slug>.md` is legacy-but-supported and there is no need to migrate existing files, but new work is better placed at `.claude/skills/<slug>/SKILL.md`: identical contract, actively developed location, and you get a folder for supporting scripts.
