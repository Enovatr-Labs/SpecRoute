# Command Examples

Concrete commands demonstrating per-vendor shapes. Reference implementations live in [`.claude/commands/`](../../.claude/commands/) at the repository root:

- `audit.md` - comprehensive pre-commit check
- `parity.md` - cross-vendor runtime parity check
- `sanitize.md` - sanitization wordlist scan
- `status.md` - skeleton state report

These are real, tracked commands you can read as worked examples of the Claude markdown shape.

## Per-vendor shape reminder

Commands are not a single format. Each vendor has its own contract:

| Vendor | Shape | Location |
|---|---|---|
| Claude Code | Markdown body + **skill frontmatter** (`description` recommended, nothing strictly required) | `.claude/commands/<slug>.md` - legacy-but-supported; `.claude/skills/<slug>/SKILL.md` is the current form |
| Cursor | Markdown command file | `.cursor/commands/<slug>.md` |
| Devin Desktop | Skill invoked as `/skill-name` | `.devin/skills/<slug>/SKILL.md` (also `.agents/skills/<slug>/SKILL.md`) |
| Gemini CLI / Antigravity | TOML file with `prompt` (+ optional `description`) | `.gemini/commands/<slug>.toml` |
| Codex | Skill invoked with `$name` or from `/skills` | `.codex/skills/<slug>/SKILL.md` (also `.agents/skills/<slug>/SKILL.md`) |
| Kiro | No command artifact - a skill invoked via `/skill` | `.kiro/skills/<slug>/SKILL.md` |

Claude Code's commands and skills have merged: the two Claude locations take the **same** frontmatter, so an example written as a command ports to a skill by moving the file, not by rewriting the header. See [`../README.md`](../README.md).

When adding an example: ship the shape for every vendor where it makes sense.

## Adding an example command

1. Pick a generic operation (lint check, format, dependency report, log tail).
2. Use [`../command-template.claude.md`](../command-template.claude.md) for Claude.
3. Use [`../command-template.gemini.toml`](../command-template.gemini.toml) for Gemini, or mirror the shape in `check-docs.gemini.toml`.
4. For Codex, Kiro, and Devin Desktop: create the equivalent skill under `runtimes/.<vendor>/skills/<slug>/SKILL.md`, preserving that runtime's native frontmatter.
5. Run `/audit` to validate.
