# Hooks

<!-- sources: hooks/README.md -->

Event-triggered automation. Hooks run automatically when something happens (file edit, session start, pre-tool invocation) — the user doesn't invoke them. This is what distinguishes hooks from skills, agents, and commands.

**All six supported vendors ship a hooks system.** The event taxonomies and config shapes differ; the underlying contract (script reads JSON on stdin, returns JSON on stdout, uses exit codes for blocking) is broadly compatible.

For the canonical reference (full event matrices), see [`hooks/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/hooks/README.md).

## Per-vendor depth

| Vendor | Event count | Blocking semantics | Hook types beyond shell |
|---|---|---|---|
| Claude Code | ~27 | rich (per-event) | `http`, `mcp_tool`, `prompt`, `agent` |
| Codex | 6 | per-event JSON | `command` only |
| Gemini CLI | 11 | per-event | `command` only |
| Kiro | 10 | pre-hooks block | `askAgent` (built-in) |
| Cursor | ~19 | `permission` schema | `command`, `prompt` |
| Windsurf | 12 | pre-hooks only | `command`, `powershell` |

Claude Code has the most comprehensive system. Cursor is second by event count. The other four cover the core "pre-tool, post-tool, session-start" patterns.

## Per-vendor config locations

```
hooks/
├── claude/    hooks.template.json     ~/.claude/settings.json or .claude/settings.json
├── codex/     hooks.template.json     .codex/hooks.json or [hooks] in config.toml
├── gemini/    hooks-settings template under `hooks` key in .gemini/settings.json
├── kiro/      *.kiro.hook             .kiro/hooks/<name>.kiro.hook
├── cursor/    hooks.template.json     .cursor/hooks.json (v1 schema)
└── windsurf/  hooks.template.json     .windsurf/hooks.json
```

The `hooks/` directory under the repo root ships templates for **all six vendors**. Drop the per-vendor template into your runtime layout and customize.

## Cross-vendor convergence

The schema is converging:

- **Common base input**: `session_id`, `transcript_path`, `cwd`, `hook_event_name` appear in every vendor's payload.
- **Common output controls**: `continue`, `stopReason`, `systemMessage`, `suppressOutput` accepted by Claude, Codex, and Gemini.
- **Decision schemas**: Claude, Codex, and Gemini support `hookSpecificOutput` with `permissionDecision: "allow|deny|ask"`.
- **Exit codes**: `0` = success, `2` = blocking, anything else = warning, consistent across all six.

This means hook scripts written for Claude Code can often run unchanged under Codex (with renamed event keys).

## When to build a hook

**Use** a hook when:

- Work *must* run on a specific event (sanitization at commit time, lint at write time, status banner at session start).
- Work is fast (sub-second target).
- Work is idempotent (fires on every event, must not corrupt state).
- The user shouldn't have to remember to run it manually.

**Don't** use a hook when:

- Work takes more than a second or two — move to an agent or command.
- Work needs user input — that's a skill.
- Work is occasional, not always-on — that's a command.

See [[Automation Decision Framework]].

## Hardening

Hook scripts run on **every matching event**. Malicious shell in hook scripts ships to every consumer who copies the runtime. Treat them like production code.

Requirements:

- **Quote variables**: `"$var"`, never `$var`.
- **Avoid `eval`** and unquoted command interpolation.
- **Use `set -u`** to catch unset variables.
- **Be idempotent** — fires repeatedly without side effects.
- **Fail closed** on `PreToolUse` / `pre_*` events — exit non-zero blocks the action.
- **Print only the final JSON to stdout** (Gemini is strict; others tolerate it).

See [[Security]] for the full hardening checklist.

## Reference implementations

This repo's own `.claude/hooks/` ships three real, tracked hook scripts:

- [`session-start-status.sh`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/hooks/session-start-status.sh) — SpecRoute skeleton status banner.
- [`pre-bash-sanitize.sh`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/hooks/pre-bash-sanitize.sh) — sanitization gate on `git commit` / `git push` / `gh pr create` / `gh release create`.
- [`post-edit-frontmatter.sh`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.claude/hooks/post-edit-frontmatter.sh) — frontmatter validation on agent/skill/command writes.

Read these as worked examples of the hook protocol (stdin JSON, exit codes, stderr usage). Each per-vendor template under `hooks/<vendor>/` adapts these patterns to that vendor's config shape.

## Common matcher conventions

| Vendor | Matcher syntax |
|---|---|
| Claude Code | exact / `|`-list / regex (auto-detected) |
| Codex | regex string |
| Gemini CLI | regex string (per hook entry) |
| Kiro | tool name / category (`read`, `write`, `shell`, etc.) / `@mcp` prefix / regex |
| Cursor | tool type / pattern / regex (`matcher` field) |
| Windsurf | per-event `tool_info` filter (script-side; no declarative matcher) |

## Owner agent

Designing and reviewing hooks is owned by the `hooks-author` agent.

## See also

- [[Automation Decision Framework]] — when to reach for a hook vs alternatives
- [[Sanitization]] — the canonical hook-driven enforcement example
- [[Security]] — hardening practices for shipped scripts
- [[Vendor Matrix]] — per-vendor event counts and capabilities
