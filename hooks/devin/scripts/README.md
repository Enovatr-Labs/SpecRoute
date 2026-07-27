# Devin Desktop hook scripts

These scripts implement the three defaults in
[`../hooks.v1.template.json`](../hooks.v1.template.json). The matching consumer
copies live under
[`runtimes/.devin/hooks/scripts/`](../../../runtimes/.devin/hooks/scripts/).

## Devin Local hook contract

- Project file: `.devin/hooks.v1.json`.
- Events: `PreToolUse`, `PostToolUse`, `PermissionRequest`,
  `UserPromptSubmit`, `Stop`, `SessionStart`, and `SessionEnd`.
- Hook types: `command` and `prompt`.
- Matcher: a regular expression over `tool_name` for tool events.
- Input: JSON on stdin, including `hook_event_name`, `session_id`, and
  event-specific fields.
- Exit codes: `0` succeeds, `2` blocks, other non-zero codes are logged.

The scripts use these payload fields:

| Event | Fields |
|---|---|
| `SessionStart` | `source` |
| `PreToolUse` | `tool_name`, `tool_input` |
| `PostToolUse` | `tool_name`, `tool_input`, `tool_response` |

The runtime template matches the publication gate only to `^exec$` and the
frontmatter adviser only to `^edit$`.

## Output

Command hooks may return a top-level `decision` and `reason`. Context injection
uses:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Project orientation"
  }
}
```

## Hardening

- Quote shell variables.
- Use `set -u`.
- Avoid `eval` and unquoted interpolation.
- Keep hooks fast and deterministic.
- Never inline credentials.
- Test both matching and non-matching payloads.

Use `/hooks` in Devin Local to verify which files were loaded.
