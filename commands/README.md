# Commands

Slash-invoked operations. Simple, deterministic, no configuration. The user types `/<name>` and gets the same behavior every time.

```
commands/
├── command-template.claude.md           Claude Code: markdown body + description frontmatter
├── command-template.gemini.toml         Gemini CLI: TOML command template (prompt + description)
└── examples/                            worked examples
```

## The command primitive is being absorbed by skills

Before reaching for a command, know that "command" is increasingly a *role*, not a file format:

| Vendor | Is there a distinct command artifact? |
|---|---|
| Claude Code | **No longer really.** Commands and skills have merged - `.claude/commands/<name>.md` is legacy-but-supported and takes the **same frontmatter as a skill**. Two artifact contracts exist (agent, skill), not three. |
| Codex | No separate command file. Use a skill invoked with `$name` or from `/skills`. |
| Kiro | Never had one. A command is a skill invocation. |
| Cursor | Yes - `.cursor/commands/<slug>.md`, alongside its skills. |
| Gemini CLI / Antigravity | Yes - `.gemini/commands/<slug>.toml`, a genuinely different (TOML) shape. |
| Devin Desktop | No separate file. Devin Local skills are invoked as `/skill-name`. |

So SpecRoute keeps `commands/` as a design category (see the decision table below), but for Claude, Codex, and Kiro the thing you actually author is a skill. Don't maintain a separate "command frontmatter" mental model for those three.

## Per-vendor shape

For the vendors that do have a distinct artifact, the shapes differ. There is no single canonical format.

### Claude Code

```
.claude/commands/<slug>.md      # legacy-but-supported
.claude/skills/<slug>/SKILL.md  # current form
```

Both are read, and **both take skill frontmatter** - no field is strictly required, `description` is recommended, and the optional set (`argument-hint`, `arguments`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `disable-model-invocation`, `model`, `effort`, `context: fork`, `agent`, `background`, `hooks`, `paths`) is the same in both places. A minimal command is still just:

```yaml
---
description: <one-line description shown in the command list>
---
```

Body is the prompt that the slash command expands to. Body can include shell snippets in fenced code blocks; Claude executes them with explanation.

Note that `allowed-tools` here **pre-approves** tools for the invoking turn - it does not restrict what the command can reach for. See [`skills/README.md`](../skills/README.md#allowed-tools-is-not-a-sandbox).

For new work, prefer `.claude/skills/<slug>/SKILL.md`: same contract, the actively developed location, and it gets the folder for supporting scripts. Existing `.claude/commands/*.md` files do not need migrating.

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

Codex has no separate command file in this framework. The equivalent is a skill with portable `name` / `description` frontmatter, invoked with `$name` or from `/skills`.

```
.codex/skills/<slug>/SKILL.md
.agents/skills/<slug>/SKILL.md   # also read; vendor-neutral root
```

Use the shipped Codex skill frontmatter (`name` and `description`) and put the argument contract in the body. Codex's older *custom prompts* feature is deprecated in favour of skills - do not author new prompt files.

### Cursor

Cursor supports custom slash commands via Markdown files:

```
.cursor/commands/<slug>.md
```

These sit alongside Cursor's skills (`.cursor/skills/<slug>/SKILL.md`), subagents, and hooks.

### Devin Desktop

Devin Local uses skills as its command surface:

```text
.devin/skills/<slug>/SKILL.md
```

Invoke the skill as `/<slug>`. Cascade compatibility workflows still load from
`.windsurf/workflows/<slug>.md`, but new repeatable procedures should migrate
to skills.

### Kiro

Kiro has no command artifact. Operations that would be slash commands are skills (`.kiro/skills/<slug>/SKILL.md`), invoked via `/skill`; steering rules and hooks cover the automated cases.

## When to build a command vs alternative

| Question | Answer |
|---|---|
| Does the user type `/<name>` once and get the same result? | **Command** |
| Does the user need to make decisions mid-flow? | **Skill** (interactive) |
| Should it run autonomously without user input? | **Agent** |
| Should it run automatically on an event? | **Hook** |

This table still earns its keep - deciding whether something is one-shot or interactive shapes how you write it. It just no longer implies a different file format on Claude Code, Codex, or Kiro, where both answers produce a skill.

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
