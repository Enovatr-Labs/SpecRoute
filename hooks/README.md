# Hooks

Event-triggered automation. Hooks run automatically when something happens (file edit, session start, pre-tool invocation) - the user doesn't invoke them. This is what distinguishes hooks from skills, agents, and commands.

**All six supported vendors ship a hooks system.** The event taxonomies and config shapes differ; the underlying contract (script reads JSON on stdin, returns JSON on stdout, uses exit codes for blocking) is broadly compatible.

```
hooks/
├── README.md                            (this file)
├── claude/
│   ├── hooks.template.json              Claude Code: ~27 events, 5 hook types
│   └── scripts/                         supporting shell scripts
├── codex/
│   ├── hooks.template.json              Codex: 6 events; Claude-compatible JSON
│   └── scripts/                         supporting shell scripts
├── gemini/
│   ├── hooks-settings.template.json     Gemini CLI: 11 events; lives under `hooks` key in settings.json
│   └── scripts/                         supporting shell scripts
├── kiro/
│   └── examples/                        Kiro: 10 events, *.kiro.hook JSON files
├── cursor/
│   ├── hooks.template.json              Cursor: ~19 events with permission/decision schema
│   └── scripts/                         supporting shell scripts
└── windsurf/
    ├── hooks.template.json              Windsurf: 12 events, blocking pre-hooks only
    └── scripts/                         supporting shell scripts
```

## Per-vendor event matrix

The full event lists. Bold events are the ones SpecForge's reference implementations exercise.

### Claude Code (~27 events)

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

### Codex (6 events)

Reference: <https://developers.openai.com/codex/hooks>.

| Event | Fires when | Blockable |
|---|---|---|
| `SessionStart` | Session begins or resumes | Yes (`continue: false`) |
| `UserPromptSubmit` | User submits a prompt | Yes |
| `PreToolUse` | Before tool call executes | Yes (`permissionDecision: "deny"`) |
| `PermissionRequest` | Before approval prompt | Yes |
| `PostToolUse` | After tool completion (success or fail) | Soft (replaces tool result) |
| `Stop` | Conversation turn ends | No (instead returns continuation prompt) |

Config in `.codex/hooks.json` (preferred) or inline `[hooks]` table in `.codex/config.toml`. Requires `[features] codex_hooks = true`. Multiple matching hooks run **concurrently**. JSON output schema is intentionally Claude-compatible (`hookSpecificOutput`, `permissionDecision`, `decision: "block"`).

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

### Kiro (10 events)

Reference: <https://kiro.dev/docs/hooks/types/>.

| Event | Fires when | Blockable |
|---|---|---|
| `Prompt Submit` | User submits a prompt | (advisory) |
| `Agent Stop` | Agent completes its turn | (advisory) |
| `Pre Tool Use` | Agent about to invoke a tool | Yes |
| `Post Tool Use` | After agent invokes a tool | (advisory) |
| `File Create` | New files matching patterns are created | (advisory) |
| `File Save` | Files matching patterns are saved | (advisory) |
| `File Delete` | Files matching patterns are deleted | (advisory) |
| `Pre Task Execution` | Before a spec task begins | Yes |
| `Post Task Execution` | After a spec task completes | (advisory) |
| `Manual Trigger` | Manually invoked | n/a |

Config in `.kiro/hooks/<name>.kiro.hook` (one JSON file per hook). Tool-name field supports specific tools, built-in categories (`read`, `write`, `shell`, `web`, `spec`, `*`), prefix filters (`@mcp`, `@powers`, `@builtin`), and regex.

### Cursor (~19 events)

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

### Windsurf (12 events)

Reference: <https://docs.windsurf.com/windsurf/cascade/hooks>.

| Event | Fires when | Blockable |
|---|---|---|
| `pre_user_prompt` | Before prompt processing | Yes |
| `pre_read_code` | Before file read | Yes |
| `post_read_code` | After file read | No |
| `pre_write_code` | Before file modification | Yes |
| `post_write_code` | After file modification | No |
| `pre_run_command` | Before terminal execution | Yes |
| `post_run_command` | After terminal execution | No |
| `pre_mcp_tool_use` | Before MCP invocation | Yes |
| `post_mcp_tool_use` | After MCP invocation | No |
| `post_cascade_response` | After response completion | No |
| `post_cascade_response_with_transcript` | After response (async, full transcript) | No |
| `post_setup_worktree` | After worktree creation | No |

Config: `.windsurf/hooks.json` (workspace), `~/.codeium/windsurf/hooks.json` (user), `~/.codeium/hooks.json` (JetBrains), system paths for enterprise. Each hook entry has `command` (bash) and/or `powershell` (Windows fallback), plus `show_output` and `working_directory`. Only **pre-hooks** are blockable.

## Cross-vendor convergence

The schema is converging:

- **Common base input**: `session_id`, `transcript_path`, `cwd`, `hook_event_name` appear in every vendor's payload.
- **Common output controls**: `continue`, `stopReason`, `systemMessage`, `suppressOutput` are accepted by Claude, Codex, and Gemini.
- **Decision schemas**: Claude, Codex, and Gemini all support `hookSpecificOutput` with `permissionDecision: "allow|deny|ask"` for tool-use events.
- **Exit codes**: `0` = success, `2` = blocking, anything else = warning is consistent across all six.

This means hook scripts written for Claude Code can often run unchanged under Codex (with renamed event keys), and the JSON-output discipline transfers.

## Common matcher conventions

| Vendor | Matcher syntax | Notes |
|---|---|---|
| Claude Code | exact / `\|` list / regex | Auto-detected by content |
| Codex | regex string | Same conventions |
| Gemini CLI | regex string | Per hook entry |
| Kiro | tool name / category / `@mcp` / regex | Multiple modes |
| Cursor | tool type / pattern / regex | `matcher` field |
| Windsurf | per-event `tool_info` filter (script-side) | No declarative matcher |

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

- `session-start-status.sh` - SpecForge skeleton status banner.
- `pre-bash-sanitize.sh` - sanitization gate on `git commit` / `git push`.
- `post-edit-frontmatter.sh` - frontmatter validation on agent/skill/command writes.

Read these as worked examples of the hook protocol (stdin JSON, exit codes, stderr usage). Each per-vendor template under `hooks/<vendor>/` adapts these patterns to that vendor's config shape.

## Authoring agent

Designing and reviewing hooks is owned by the `hooks-author` agent. See [`.claude/agents/hooks-author.md`](../.claude/agents/hooks-author.md).
