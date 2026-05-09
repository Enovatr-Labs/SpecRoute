# Codex Hook Scripts

Supporting shell scripts referenced by `hooks/codex/hooks.template.json`.

## Hook protocol summary (Codex)

- **Stdin**: Hook scripts receive JSON. Common base fields: `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `turn_id` (for turn-scoped events).
- **Stdout**: success path — print JSON output (or plain text used as context) or nothing.
- **Stderr**: blocking message if exit code 2.
- **Exit codes**: `0` = success, `2` = blocking, other = failure.

## JSON output schemas (Claude-compatible)

```json
// PreToolUse blocking
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "string"
  }
}

// PostToolUse feedback
{
  "decision": "block",
  "reason": "string",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "string"
  }
}

// SessionStart context injection
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "string"
  }
}
```

## Reference implementations

The scripts under [`.claude/hooks/`](../../../.claude/hooks/) at the repo root are Claude Code hooks but the JSON protocol is broadly Codex-compatible. Adapt them by:

1. Renaming event keys where appropriate.
2. Removing references to Claude-specific fields like `permission_mode` (Codex doesn't expose this).
3. Wrapping in a parallel-safe pattern (Codex runs matching hooks concurrently).

## Common patterns

### Pre-tool sanitization

```bash
#!/usr/bin/env bash
set -u
INPUT="$(cat)"
TOOL_NAME="$(printf '%s' "$INPUT" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("tool_name", ""))')"

case "$TOOL_NAME" in
  Bash|apply_patch) ;;
  *) exit 0 ;;
esac

# Validate. Exit 2 with stderr reason to block; exit 0 to allow.
if <unsafe>; then
  echo "Blocked by sanitization gate." >&2
  exit 1  # or 2 for hard block
fi
exit 0
```

### Concurrency safety

Multiple matching hooks for the same event run in parallel. Don't write to shared state without locks. Don't depend on hook execution order.

## Hardening

Same as `hooks/claude/scripts/`:

- Quote variables (`"$var"`).
- `set -u` to catch unset variables.
- No `eval` or unquoted command interpolation.
- Use `python3` for JSON parsing (more portable than `jq`).
- Sub-second target.
- Idempotent.

## Adding a hook script

1. Drop the script under `.codex/hooks/scripts/` (consumer side).
2. `chmod +x`.
3. Reference in `.codex/hooks.json` or the inline `[[hooks.<EventName>.hooks]]` TOML block.
4. Confirm `[features] codex_hooks = true` is set in `.codex/config.toml`.
