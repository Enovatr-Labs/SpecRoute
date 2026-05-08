# Hooks

Event-triggered automation. Hooks run automatically when something happens (file edit, session start, pre-tool invocation) — the user doesn't invoke them. This is what distinguishes hooks from skills, agents, and commands.

```
hooks/
├── claude/
│   ├── hooks.template.json              Claude Code hooks.json shape with examples
│   └── scripts/                         supporting shell scripts
└── kiro/
    └── examples/                        *.kiro.hook JSON files with file-pattern triggers
```

## Trigger taxonomy

Different vendors expose different trigger types. Match the trigger to the work:

### Claude Code

| Trigger | Fires when | Can block? |
|---|---|---|
| `SessionStart` | Once when a session begins | No (informational only) |
| `PreToolUse` | Before any tool invocation matching `matcher` | **Yes** (exit non-zero blocks) |
| `PostToolUse` | After any tool completes matching `matcher` | No (action already happened) |

Common matchers: `Bash`, `Write`, `Edit`, `Read`, `Write|Edit` (regex pipe), or empty (`""`) for all.

### Kiro

| Trigger | Fires when |
|---|---|
| `fileEdited` | A file matching `patterns` is edited |
| `fileSaved` | A file matching `patterns` is saved |
| `manual` | User explicitly invokes (e.g. via `pre-commit` trigger ID) |

Kiro hooks live in `*.kiro.hook` files (JSON), one per hook.

### Other vendors

Codex, Gemini CLI, Cursor, and Windsurf don't have first-class hook concepts. Equivalent automation goes via:

- **Codex**: scripts under `.codex/scripts/` invoked manually or via skills.
- **Gemini CLI**: shell wrappers around `gemini` invocations.
- **Cursor / Windsurf**: rules with `alwaysApply: true` change agent behavior, but don't fire on events.

## When to build a hook

Use a hook when:

- The work *must* run on a specific event — sanitization at commit time, lint at write time, status banner at session start.
- The work is fast (sub-second target).
- The work is idempotent (fires on every event, must not corrupt state).
- The user shouldn't have to remember to run it manually.

Don't use a hook when:

- The work takes more than a second or two — move to an agent or command.
- The work needs user input — that's a skill.
- The work is occasional, not always-on — that's a command.

See [`docs/automation-decision-framework.md`](../docs/automation-decision-framework.md) for the 4-row decision matrix.

## Hardening

Hook scripts run on every matching event. They must:

- **Quote variables**: `"$var"`, never `$var`.
- **Avoid `eval`** and unquoted command interpolation.
- **Use `set -u`** to catch unset variables.
- **Be idempotent** — fires repeatedly without side effects.
- **Fail closed for `PreToolUse`** — exit non-zero blocks the action.

See [`SECURITY.md`](../SECURITY.md) for the broader threat model. Malicious shell in hook scripts ships to every consumer who copies the runtime — review hook scripts as carefully as production code.

## Reference implementations

The three hooks in [`.claude/hooks/`](../.claude/hooks/) at the repo root are real, tracked examples:

- `session-start-status.sh` — SpecForge skeleton status banner.
- `pre-bash-sanitize.sh` — sanitization gate on `git commit` / `git push`.
- `post-edit-frontmatter.sh` — frontmatter validation on agent/skill/command writes.

Read these as worked examples of the hook protocol (stdin JSON, exit codes, stderr usage).

## Authoring agent

Designing and reviewing hooks is owned by the `hooks-author` agent. See `.claude/agents/hooks-author.md` for its operating principles.
