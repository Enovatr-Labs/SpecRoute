# Command Examples

Concrete commands demonstrating per-vendor shapes. Reference implementations live in [`.claude/commands/`](../../.claude/commands/) at the repository root:

- `audit.md` — comprehensive pre-commit check
- `parity.md` — cross-vendor runtime parity check
- `sanitize.md` — sanitization wordlist scan
- `status.md` — skeleton state report

These are real, tracked commands you can read as worked examples of the Claude markdown shape.

## Per-vendor shape reminder

Commands are not a single format. Each vendor has its own contract:

| Vendor | Shape | Location |
|---|---|---|
| Claude Code | Markdown body + `description` frontmatter | `.claude/commands/<slug>.md` (or `runtimes/.claude/commands/<slug>.md` for the consumer template) |
| Gemini CLI | JSON entry: `{command, description, directory?}` | `.gemini/gemini_cli_config.json` under `commands` map |
| Codex | Skill with `user-invocable: true` and a clear `argument-hint` | `.codex/skills/<slug>/SKILL.md` |
| Kiro | Not a separate concept | (use hooks for automation) |
| Cursor / Windsurf | Not a separate concept | (use rules) |

When adding an example: ship the shape for every vendor where it makes sense.

## Adding an example command

1. Pick a generic operation (lint check, format, dependency report, log tail).
2. Use [`../command-template.claude.md`](../command-template.claude.md) for Claude.
3. Use [`../command-template.gemini.json`](../command-template.gemini.json) for Gemini.
4. For Codex: create the equivalent skill under `runtimes/.codex/skills/<slug>/SKILL.md` with `user-invocable: true`.
5. Run `/audit` to validate.
