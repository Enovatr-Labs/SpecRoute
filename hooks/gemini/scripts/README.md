# Gemini CLI Hook Scripts

Supporting shell scripts referenced by `hooks/gemini/hooks-settings.template.json`.

## Hook protocol summary (Gemini)

- **Stdin**: JSON. Common base fields: `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `timestamp`. Event-specific fields layered on top.
- **Stdout**: **MUST be the final JSON only**. Mix-in stderr for diagnostics. This is stricter than Claude / Codex.
- **Stderr**: blocking message if exit code 2.
- **Exit codes**: `0` = success, `2` = system block, other = warning.

## Key event-specific fields

| Event | Notable input fields |
|---|---|
| `BeforeTool` / `AfterTool` | `tool_name`, `tool_input`, `tool_response` (after only), `mcp_context`, `original_request_name` |
| `BeforeAgent` | `prompt` |
| `AfterAgent` | `prompt`, `prompt_response`, `stop_hook_active` |
| `BeforeModel` / `AfterModel` | `llm_request`, `llm_response` (after only) |
| `BeforeToolSelection` | `llm_request` |
| `SessionStart` | `source` (`startup`/`resume`/`clear`) |
| `SessionEnd` | `reason` |
| `Notification` | `notification_type`, `message`, `details` |
| `PreCompress` | `trigger` (`auto`/`manual`) |

## JSON output shapes

```json
// BeforeTool / AfterTool deny
{
  "decision": "deny",
  "reason": "string",
  "hookSpecificOutput": {
    "tool_input": { "field": "modified value" }
  }
}

// BeforeAgent context injection
{
  "hookSpecificOutput": {
    "additionalContext": "string added to context",
    "decision": "allow"
  }
}

// BeforeToolSelection - constrain tool config
{
  "hookSpecificOutput": {
    "toolConfig": {
      "mode": "AUTO|ANY|NONE",
      "allowedFunctionNames": ["read_file", "write_file"]
    }
  }
}

// Universal stop / system message
{
  "continue": false,
  "stopReason": "Why we stopped",
  "systemMessage": "Shown to user"
}
```

## Canonical script structure

```bash
#!/usr/bin/env bash
set -u

INPUT="$(cat)"
EVENT="$(printf '%s' "$INPUT" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("hook_event_name", ""))')"

# Diagnostics on stderr (allowed) - never on stdout for Gemini.
echo "[gemini-hook] firing for $EVENT" >&2

# Decide based on event-specific input.
TOOL="$(printf '%s' "$INPUT" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("tool_name", ""))')"
case "$TOOL" in
  run_shell_command) <validation logic> ;;
  *) ;;
esac

# Print the FINAL JSON only.
python3 -c 'import json; print(json.dumps({"continue": True}))'
exit 0
```

## Hardening

- Stdout discipline: nothing but the final JSON. Diagnostics go to stderr.
- Quote all variables (`"$var"`).
- `set -u`.
- Use `python3` (not `jq`) for JSON parsing - more portable, supports the strict-stdout requirement.
- Sub-second target.
- Idempotent.

## Adding a hook script

1. Drop the script under `.gemini/hooks/scripts/` (consumer side).
2. `chmod +x`.
3. Reference it in `.gemini/settings.json`'s `hooks` block (or merge from `hooks/gemini/hooks-settings.template.json`).
4. Confirm Gemini CLI version is 0.26.0+ (hooks enabled by default from that version onward).
