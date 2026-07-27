# Hooks

<!-- sources: hooks/README.md -->

Event-triggered automation. Hooks run automatically when something happens (file edit, session start, pre-tool invocation) — the user doesn't invoke them. This is what distinguishes hooks from skills, agents, and commands.

**All six supported vendors ship a hooks system.** The underlying contract (script reads JSON on stdin, returns JSON on stdout, uses exit codes for blocking) is broadly compatible. The **event taxonomies and config shapes are not** — hooks remain the least portable layer in the framework.

For the canonical reference (full event matrices), see [`hooks/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/hooks/README.md).

## Per-vendor depth

| Vendor | Event count | Blocking semantics | Hook types beyond shell |
|---|---|---|---|
| Claude Code | 30 | rich (per-event) | `http`, `mcp_tool`, `prompt`, `agent` |
| Codex | 11 | per-event JSON | `command` only |
| Gemini CLI | 11 | per-event | `command` only |
| Kiro | 10 | pre-hooks block | `agent` (built-in) |
| Cursor | 21 | `permission` schema | `command`, `prompt` |
| Devin Desktop (Devin Local) | 8 | exit 2 blocks | `command`, `prompt` |

Claude Code has the most comprehensive system. Cursor is second by event count. The other four cover the core "pre-tool, post-tool, session-start" patterns.

Devin Desktop's Cascade agent has a separate compatibility surface with 12
snake_case events and `command` / `powershell` handlers. That Cascade contract
does not change the primary Devin Local row above.

## Per-vendor config locations

```
hooks/
├── claude/    hooks.template.json     ~/.claude/settings.json or .claude/settings.json
├── codex/     hooks.template.json     .codex/hooks.json or [hooks] in config.toml
├── gemini/    hooks-settings template under `hooks` key in .gemini/settings.json
├── kiro/      examples/*.json         .kiro/hooks/<name>.json (v1 schema)
├── cursor/    hooks.template.json     .cursor/hooks.json (v1 schema)
└── devin/     hooks.v1.template.json  .devin/hooks.v1.json
```

The `hooks/` directory under the repo root ships one template for each of the
six vendors. Cascade still recognizes `.windsurf/hooks.json`, but that literal
compatibility path is not a separate SpecRoute vendor or runtime.

## Kiro 1.0 hook format (breaking change, 2026-06-25)

**Kiro IDE 1.0 replaced the `*.kiro.hook` format.** Hooks now live at `.kiro/hooks/<name>.json`:

```json
{
  "version": "v1",
  "hooks": [
    {
      "name": "Doc Sync Checker",
      "trigger": "PostFileSave",
      "matcher": "README.md|AGENTS.md|docs/**/*.md",
      "action": { "type": "agent", "prompt": "<what the agent should do>" },
      "timeout": 30,
      "enabled": true
    }
  ]
}
```

Ten triggers: `SessionStart`, `Stop`, `PreToolUse`, `PostToolUse`, `PreTaskExec`, `PostTaskExec`, `UserPromptSubmit`, `PostFileCreate`, `PostFileSave`, `PostFileDelete`. Actions are `agent` (prompt) or `command` (shell) — the 0.x `askAgent` / `runCommand` respelled.

Old → new mapping: `fileSaved` → `PostFileSave`; `fileEdited` → `PostFileSave` for user saves or `PostToolUse` for agent writes; `manual` → **no equivalent** (the `Manual` trigger was retired; use a manual steering file); the `when.patterns` array collapses into a single `|`-separated `matcher` string.

> ⚠️ Legacy `*.kiro.hook` files get an upgrade badge in the IDE but do not execute until migrated. Run `ls .kiro/hooks/*.kiro.hook`; anything it prints is not part of the v1 runtime. Full checklist in [`hooks/kiro/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/hooks/kiro/README.md).

## Cross-vendor convergence

Hooks are where cross-vendor convergence is weakest. **Skills** are the layer where it is near-total — the Agent Skills `SKILL.md` shape ports across all six vendors essentially unchanged. Hooks do not.

What *has* converged:

- **Common input concepts**: every vendor supplies event, session, and operation
  context, but field names and available values differ; do not assume one
  payload schema is portable.
- **Common output controls**: `continue`, `stopReason`, `systemMessage`, `suppressOutput` accepted by Claude, Codex, and Gemini.
- **Decision schemas**: Claude, Codex, and Gemini support `hookSpecificOutput` with `permissionDecision: "allow|deny|ask"`.
- **Exit codes**: `0` = success, `2` = blocking, anything else = warning, consistent across all six.
- **Event naming, in four of six**: Claude, Codex, Kiro, and Devin Local share
  core names such as `SessionStart`, `UserPromptSubmit`, `PreToolUse`,
  `PostToolUse`, and `Stop`.

What has *not*:

- **Cursor** — camelCase across ~21 events (`preToolUse`, `beforeShellExecution`, `afterFileEdit`), plus Tab-scoped events no other vendor has.
- **Gemini CLI** — its own verb-first vocabulary (`BeforeTool`, `AfterModel`, `BeforeToolSelection`, `PreCompress`).
- **Devin Desktop's Cascade compatibility surface** — snake_case operation
  names (`pre_read_code`, `post_run_command`, `post_cascade_response`) remain
  distinct from the primary Devin Local lifecycle.

A hook script's *body* and its stdin/stdout discipline port well. Its *registration* — event name, config path, config shape — does not. Budget for per-vendor hook wiring.

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
| Kiro | glob / tool name / category (`read`, `write`, `shell`, etc.) / `@mcp` prefix / regex — one `matcher` string, `\|`-separated |
| Cursor | tool type / pattern / regex (`matcher` field) |
| Devin Desktop | regex on Devin Local `tool_name`; Cascade compatibility hooks use script-side `tool_info` filtering |

## Owner agent

Designing and reviewing hooks is owned by the `hooks-author` agent.

## See also

- [[Automation Decision Framework]] — when to reach for a hook vs alternatives
- [[Sanitization]] — the canonical hook-driven enforcement example
- [[Security]] — hardening practices for shipped scripts
- [[Vendor Matrix]] — per-vendor event counts and capabilities
