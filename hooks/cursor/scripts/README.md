# Cursor Hook Scripts

Supporting shell scripts referenced by `hooks/cursor/hooks.template.json`.

## Hook protocol summary (Cursor)

- **Stdin**: JSON. Common base fields: `conversation_id`, `generation_id`, `model`, `hook_event_name`, `cursor_version`, `workspace_roots`, `user_email`, `transcript_path`.
- **Stdout**: JSON output (or empty for fire-and-forget hooks).
- **Stderr**: blocking message if exit code 2.
- **Exit codes**: `0` = success, `2` = block (= `permission: "deny"`), other = fail-open unless `failClosed: true` set.

## Permission decision schema

Control hooks (events starting with `before*` or `pre*`) return:

```json
{
  "permission": "allow|deny|ask",
  "user_message": "shown to the user",
  "agent_message": "sent back to the agent",
  "updated_input": { /* optional override of tool input */ }
}
```

For `beforeSubmitPrompt`:

```json
{
  "continue": true,
  "user_message": "string"
}
```

For `stop` / `subagentStop` (auto follow-up):

```json
{
  "followup_message": "auto-submitted as next prompt"
}
```

For `sessionStart` (env injection):

```json
{
  "env": { "MY_VAR": "value" },
  "additional_context": "string injected into context"
}
```

## Environment variables Cursor passes to hooks

```
CURSOR_PROJECT_DIR     # Workspace root
CURSOR_VERSION         # Cursor version
CURSOR_USER_EMAIL      # User email (if logged in)
CURSOR_TRANSCRIPT_PATH # Transcript file path (if enabled)
CURSOR_CODE_REMOTE     # "true" for remote workspaces
CLAUDE_PROJECT_DIR     # Alias for CURSOR_PROJECT_DIR (Claude-compatibility)
```

Session-scoped env vars set by `sessionStart` (via `env` output) flow to all subsequent hooks in that session.

## Canonical script structure

```bash
#!/usr/bin/env bash
set -u

INPUT="$(cat)"
EVENT="$(printf '%s' "$INPUT" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("hook_event_name", ""))')"

# Diagnostics on stderr.
echo "[cursor-hook] $EVENT in $CURSOR_PROJECT_DIR" >&2

# Make a decision.
if <unsafe condition>; then
  python3 -c 'import json; print(json.dumps({"permission": "deny", "user_message": "Reason"}))'
  exit 0
fi

python3 -c 'import json; print(json.dumps({"permission": "allow"}))'
exit 0
```

## Matchers

Tool-event matchers filter by tool type:

- `Shell`, `Read`, `Write`, `Task`
- `MCP:<server-name>` (e.g. `MCP:filesystem`)
- Subagent types: `generalPurpose`, `explore`, `shell`
- Regex on command text for `beforeShellExecution`
- File-tool types for `beforeReadFile` / `afterFileEdit`: `Read`, `Write`, `TabRead`, `TabWrite`

## failClosed semantics

By default, hook failures (anything other than exit 0 or 2) are **fail-open** — the action proceeds. Set `failClosed: true` per hook entry to flip this for security-critical gates.

## Hardening

Same as the other vendors:

- Quote variables (`"$var"`).
- `set -u`.
- No `eval` / unquoted interpolation.
- Use `python3` for JSON.
- Sub-second target.
- Idempotent.

## Adding a hook script

1. Drop the script under `<project>/.cursor/hooks/scripts/` (or `~/.cursor/hooks/`).
2. `chmod +x`.
3. Reference it in `<project>/.cursor/hooks.json` (project) or `~/.cursor/hooks.json` (user).
4. The path is relative to the hooks.json's parent directory.
