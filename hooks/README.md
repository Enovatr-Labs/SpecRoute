# Hooks

Event-triggered automation. Hooks run automatically when something happens (file edit, session start, pre-tool invocation) - the user doesn't invoke them. This is what distinguishes hooks from skills, agents, and commands.

**All six supported vendors ship a hooks system.** The underlying contract (script reads JSON on stdin, returns JSON on stdout, uses exit codes for blocking) is broadly compatible. The **event taxonomies and config shapes are not** - they remain the least portable part of the framework. See [Cross-vendor convergence](#cross-vendor-convergence) for what actually transfers.

```
hooks/
├── README.md                            (this file)
├── claude/
│   ├── hooks.template.json              Claude Code: 30 events, 5 hook types
│   └── scripts/                         supporting shell scripts
├── codex/
│   ├── hooks.template.json              Codex: 11 events; Claude-compatible JSON
│   └── scripts/                         supporting shell scripts
├── gemini/
│   ├── hooks-settings.template.json     Gemini CLI: 11 events; lives under `hooks` key in settings.json
│   └── scripts/                         supporting shell scripts
├── kiro/
│   ├── README.md                        Kiro hook format + 0.x → 1.0 migration checklist
│   └── examples/                        Kiro: 10 triggers, .kiro/hooks/<name>.json (v1)
├── cursor/
│   ├── hooks.template.json              Cursor: ~21 events with permission/decision schema
│   └── scripts/                         supporting shell scripts
├── devin/                               Devin Desktop (current)
│   ├── hooks.v1.template.json           Devin Local: 8 events, .devin/hooks.v1.json
│   └── scripts/                         supporting shell scripts
```

Working implementations of all six live under [`runtimes/`](../runtimes/), one
`runtimes/.<vendor>/hooks/` per vendor. The templates here are the reference tier; the runtimes are
the copy-and-run tier.

## Per-vendor event matrix

The full event lists. Bold events are the ones SpecRoute's reference implementations exercise.

### Claude Code (30 events)

Most comprehensive. Reference: <https://code.claude.com/docs/en/hooks>.

| Event | Fires when | Blockable |
|---|---|---|
| `Setup` | `--init-only` or `-p --init`/`--maintenance` | No |
| **`SessionStart`** | Session begins or resumes | No |
| `InstructionsLoaded` | `CLAUDE.md` / `.claude/rules/*.md` loaded | No |
| `UserPromptSubmit` | User submits a prompt | Yes |
| `UserPromptExpansion` | Slash command expands | Yes |
| **`PreToolUse`** | Before tool call executes | Yes |
| `PermissionRequest` | Permission dialog appears | Yes |
| `PermissionDenied` | Tool call denied by classifier | No (can `retry`) |
| **`PostToolUse`** | Tool call succeeds | Soft (exit 2 surfaces stderr to Claude) |
| `PostToolUseFailure` | Tool call fails | Soft |
| `PostToolBatch` | Full parallel batch resolves | Yes |
| `Notification` | Claude Code sends a notification | No |
| `MessageDisplay` | Claude Code displays a message to the user | No |
| `SubagentStart` | Subagent spawned | No |
| `SubagentStop` | Subagent finishes | Yes |
| `TaskCreated` | Task created via TaskCreate | Yes (rolls back) |
| `TaskCompleted` | Task marked completed | Yes |
| `Stop` | Claude finishes responding | Yes (continues turn) |
| `StopFailure` | Turn ends due to API error | No |
| `TeammateIdle` | Agent team teammate about to idle | Yes |
| `ConfigChange` | Configuration file changes | Yes |
| `CwdChanged` | Working directory changes | No |
| `FileChanged` | Watched file changes on disk | No |
| `WorktreeCreate` | Worktree being created | Yes (any non-zero exit fails creation) |
| `WorktreeRemove` | Worktree being removed | No |
| `PreCompact` | Before context compaction | Yes |
| `PostCompact` | After context compaction | No |
| `Elicitation` | MCP server requests user input | Yes |
| `ElicitationResult` | User responds to MCP elicitation | Yes |
| `SessionEnd` | Session terminates | No |

Hook types: `command`, `http`, `mcp_tool`, `prompt`, `agent`. Config in `.claude/settings.json` `hooks` key, or `~/.claude/settings.json` for user level. Matchers support exact strings, `|`-separated lists, and JavaScript regex.

### Codex (11 events)

Reference: <https://learn.chatgpt.com/docs/hooks>.

Codex has adopted Claude Code's hook event vocabulary almost verbatim - **the event names below are identical to Claude Code's**. This is the strongest cross-vendor convergence in the whole matrix.

| Event | Fires when | Blockable |
|---|---|---|
| `SessionStart` | Session begins or resumes | Yes (`continue: false`) |
| `SessionEnd` | Session ends | No |
| `UserPromptSubmit` | User submits a prompt | Yes |
| `PreToolUse` | Before tool call executes | Yes (`permissionDecision: "deny"`) |
| `PermissionRequest` | Before approval prompt | Yes |
| `PostToolUse` | After tool completion (success or fail) | Soft (replaces tool result) |
| `Stop` | Conversation turn ends | No (instead returns continuation prompt) |
| `PreCompact` | Before context compaction | No |
| `PostCompact` | After context compaction | No |
| `SubagentStart` | Subagent begins | No |
| `SubagentStop` | Subagent finishes | No |

Verified against an installed `codex-cli` 0.145.0 binary. Note Claude Code's `PostToolUseFailure` has **no** Codex counterpart - the convergence is close but not total.

Discovery order: `~/.codex/hooks.json`, `~/.codex/config.toml` `[hooks]`, `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml` `[hooks]`, and plugin-bundled `hooks/hooks.json`. Hooks are **enabled by default**. The canonical `[features]` key is `hooks`; `codex_hooks` is a deprecated alias that still works. Disable with `[features] hooks = false`.

Multiple matching hooks run **concurrently**. The JSON output schema is intentionally Claude-compatible (`hookSpecificOutput`, `permissionDecision`, `decision: "block"`). **Only `type: "command"` executes today** - `prompt` and `agent` handlers are parsed but skipped.

### Gemini CLI (11 events)

Reference: <https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/reference.md>.

| Event | Fires when | Blockable |
|---|---|---|
| `SessionStart` | App startup, session resume, or `/clear` | No |
| `SessionEnd` | CLI exits or session clears | No |
| `BeforeAgent` | After user prompt, before agent planning | Yes |
| `AfterAgent` | After model generates final response per turn | Yes (forces retry) |
| `BeforeModel` | Before LLM request | Yes |
| `BeforeToolSelection` | Before LLM tool-selection decision | No |
| `AfterModel` | After LLM response chunk | Yes (discards chunk) |
| `BeforeTool` | Before tool invocation | Yes |
| `AfterTool` | After tool executes | Yes (hides result) |
| `Notification` | System alert (e.g. tool permissions) | No |
| `PreCompress` | Before history summarization | No |

Config in `.gemini/settings.json` under `hooks` key (project) or `~/.gemini/settings.json` (user). Hook type `command` only. Each hook entry can set `sequential: true` to opt out of parallel execution. Stdout must be the final JSON only - no plain text.

### Kiro (10 triggers)

Reference: <https://kiro.dev/docs/hooks/types/>.

**Kiro IDE 1.0 (2026-06-25) replaced the hook format.** The old `*.kiro.hook` files and their
space-separated event names (`File Save`, `Pre Tool Use`, …) are gone. The table below is 1.0.
For the 0.x mapping and a migration checklist, see [`kiro/README.md`](kiro/README.md).

| Trigger | Fires when | Blockable |
|---|---|---|
| `SessionStart` | Session begins or resumes | No |
| `Stop` | Agent completes its turn | (advisory) |
| `PreToolUse` | Agent about to invoke a tool | Yes |
| `PostToolUse` | After agent invokes a tool | (advisory) |
| `PreTaskExec` | Before a spec task begins | Yes |
| `PostTaskExec` | After a spec task completes | (advisory) |
| `UserPromptSubmit` | User submits a prompt | (advisory) |
| `PostFileCreate` | New file matching `matcher` is created | (advisory) |
| `PostFileSave` | File matching `matcher` is saved | (advisory) |
| `PostFileDelete` | File matching `matcher` is deleted | (advisory) |
| ~~`Manual`~~ | **Retired in 1.0** - use a manual steering file instead | n/a |

Config in `.kiro/hooks/<name>.json` - a `"version": "v1"` root with a `hooks` array, so one file may
declare several hooks:

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

Hook types are `command` (shell, in an `action.command` field) and `agent` (prompt handed to the
Kiro agent, in `action.prompt`) - the 0.x `runCommand` / `askAgent` names under a different spelling.
`matcher` is a single string, where 0.x used a `patterns` array; `|`-separate multiple values. For
tool triggers it accepts specific tools, built-in categories (`read`, `write`, `shell`, `web`,
`spec`, `*`), prefix filters (`@mcp`, `@powers`, `@builtin`), and regex.

> **Consumers with existing hooks:** 1.0 flags legacy `*.kiro.hook` files with an upgrade badge but
> does not execute them. Run `ls .kiro/hooks/*.kiro.hook` - anything it prints is outside the v1
> runtime and needs migration.

### Cursor (~21 events)

Reference: <https://cursor.com/docs/agent/hooks>.

| Event | Fires when | Blockable |
|---|---|---|
| `sessionStart` | New composer conversation created | No |
| `sessionEnd` | Composer conversation ends | No |
| `preToolUse` | Before any tool executes | Yes (`permission: "deny"`) |
| `postToolUse` | After successful tool execution | No |
| `postToolUseFailure` | Tool fails, times out, or denied | No |
| `subagentStart` | Before spawning a subagent | No |
| `subagentStop` | Subagent completes / errors / aborts | Yes (auto follow-up) |
| `beforeShellExecution` | Before shell command | Yes |
| `afterShellExecution` | After shell command | No |
| `beforeMCPExecution` | Before MCP tool | Yes |
| `afterMCPExecution` | After MCP tool | No |
| `beforeReadFile` | Before agent reads a file | Yes |
| `afterFileEdit` | After agent edits a file | No |
| `beforeSubmitPrompt` | After user hits send, before backend request | Yes |
| `preCompact` | Before context window compaction | (advisory) |
| `afterAgentResponse` | After agent completes assistant message | No |
| `afterAgentThought` | After agent completes thinking block | No |
| `stop` | Agent loop ends | Yes (auto follow-up) |
| `beforeTabFileRead` / `afterTabFileEdit` | Inline-completion (Tab) flows | Hooks scoped to Tab feature |

Config: `<project>/.cursor/hooks.json` (project), `~/.cursor/hooks.json` (user), enterprise paths under `/Library/Application Support/Cursor/` or `/etc/cursor/`. Top-level `version: 1` + `hooks` map. Hook types: `command` (default) and `prompt` (LLM-evaluated). Per-hook `failClosed`, `loop_limit`, `timeout`, `matcher`.

### Devin Desktop / Devin Local (8 events)

Reference: <https://docs.devin.ai/cli/extensibility/hooks/overview>.

| Event | Fires when | Blockable |
|---|---|---|
| `PreToolUse` | Before a tool executes | Yes |
| `PostToolUse` | After a tool finishes | No |
| `PermissionRequest` | A permission decision is needed | Yes |
| `UserPromptSubmit` | User submits a message | Yes |
| `Stop` | Agent wants to stop | Yes |
| `PostCompaction` | Context compaction completes successfully | No |
| `SessionStart` | Session begins | No |
| `SessionEnd` | Session ends | No |

Config: `.devin/hooks.v1.json`, or the `hooks` key in `.devin/config.json`.
Handlers may be `command` or `prompt`; matchers are regular expressions over
`tool_name`.

Cascade compatibility uses a separate 12-event snake-case contract at
`.windsurf/hooks.json`. It is part of the transition inside Devin Desktop, not
a seventh SpecRoute hook vendor.

## Cross-vendor convergence

**Hooks are the least converged layer in the framework.** Skills are where convergence is
near-total - the Agent Skills `SKILL.md` shape is genuinely portable across all six vendors. Hooks
are not there, and it is worth being precise about what does and doesn't transfer.

What *has* converged:

- **Common base input**: `session_id`, `transcript_path`, `cwd`, `hook_event_name` appear in every vendor's payload.
- **Common output controls**: `continue`, `stopReason`, `systemMessage`, `suppressOutput` are accepted by Claude, Codex, and Gemini.
- **Decision schemas**: Claude, Codex, and Gemini all support `hookSpecificOutput` with `permissionDecision: "allow|deny|ask"` for tool-use events.
- **Exit codes**: `0` = success, `2` = blocking, anything else = warning is consistent across all six.
- **Event naming, in four of six**: Claude, Codex, Kiro, and Devin Local share `SessionStart`,
  `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`. Kiro's 1.0 rewrite (2026-06-25) moved it
  onto these names from its old `Pre Tool Use` / `File Save` spellings, so a Claude hook's event
  keys now port to Kiro with less translation than before.

What has *not* converged, and shows no sign of doing so:

- **Cursor** uses camelCase across ~21 events (`preToolUse`, `beforeShellExecution`, `afterFileEdit`)
  and adds Tab-scoped events no other vendor has.
- **Gemini CLI** uses its own verb-first vocabulary (`BeforeTool`, `AfterModel`,
  `BeforeToolSelection`, `PreCompress`) that maps only loosely onto pre/post tool-use.
- **Cascade compatibility inside Devin Desktop** retains snake_case operation
  names such as `pre_read_code` and `post_run_command`.

So: a hook script's *body* and its stdin/stdout discipline port well. Its *registration* - event
name, config path, config shape - does not, and each vendor still needs its own template under
`hooks/<vendor>/`. Budget for per-vendor hook wiring; do not budget for a single hooks file.

## Common matcher conventions

| Vendor | Matcher syntax | Notes |
|---|---|---|
| Claude Code | exact / `\|` list / regex | Auto-detected by content |
| Codex | regex string | Same conventions |
| Gemini CLI | regex string | Per hook entry |
| Kiro | glob / tool name / category / `@mcp` / regex | Single `matcher` string; `\|`-separate values |
| Cursor | tool type / pattern / regex | `matcher` field |
| Devin Desktop | regex on `tool_name` | Same matcher model as Devin CLI |

## When to build a hook

Use a hook when:

- The work *must* run on a specific event - sanitization at commit time, lint at write time, status banner at session start.
- The work is fast (sub-second target).
- The work is idempotent (fires on every event, must not corrupt state).
- The user shouldn't have to remember to run it manually.

Don't use a hook when:

- The work takes more than a second or two - move to an agent or command.
- The work needs user input - that's a skill.
- The work is occasional, not always-on - that's a command.

See [`agentic-docs/automation-decision-framework.md`](../agentic-docs/automation-decision-framework.md) for the full matrix.

## Hardening

Hook scripts run on every matching event. They must:

- **Quote variables**: `"$var"`, never `$var`.
- **Avoid `eval`** and unquoted command interpolation.
- **Use `set -u`** to catch unset variables.
- **Be idempotent** - fires repeatedly without side effects.
- **Fail closed** on `PreToolUse` / `pre_*` events - exit non-zero blocks the action.
- **Print only the final JSON to stdout** (Gemini is strict; others tolerate but don't depend on it).

Malicious shell in hook scripts ships to every consumer who copies the runtime - review hook scripts as carefully as production code. See [`SECURITY.md`](../SECURITY.md).

## Reference implementations

The three hooks in [`.claude/hooks/`](../.claude/hooks/) at the repo root are real, tracked examples:

- `session-start-status.sh` - SpecRoute skeleton status banner.
- `pre-bash-sanitize.sh` - sanitization gate on `git commit` / `git push`.
- `post-edit-frontmatter.sh` - frontmatter validation on agent/skill/command writes.

Read these as worked examples of the hook protocol (stdin JSON, exit codes, stderr usage). Each per-vendor template under `hooks/<vendor>/` adapts these patterns to that vendor's config shape.

## Authoring agent

Designing and reviewing hooks is owned by the `hooks-author` agent. See [`.claude/agents/hooks-author.md`](../.claude/agents/hooks-author.md).
