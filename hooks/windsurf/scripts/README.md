# Windsurf Cascade Hook Scripts

Supporting shell scripts referenced by `hooks/windsurf/hooks.template.json`.

## Hook protocol summary (Windsurf)

- **Stdin**: JSON. Common fields: `agent_action_name`, `trajectory_id`, `execution_id`, `timestamp`, `model_name`, `tool_info` (event-specific).
- **Stdout**: free-form text or JSON; `show_output: true` displays it in the IDE.
- **Stderr**: blocking message if exit code 2 (pre-hooks only).
- **Exit codes**: `0` = success, `2` = block (pre-hooks only), other = warning.

## Blockable events

Only `pre_*` events are blockable:

- `pre_user_prompt`
- `pre_read_code`
- `pre_write_code`
- `pre_run_command`
- `pre_mcp_tool_use`

`post_*` events are observational. Returning exit 2 from a post-hook is treated as a warning, not a block.

## Cross-platform: `command` vs `powershell`

Each hook entry can specify both:

```json
{
  "command": "bash .windsurf/hooks/scripts/check.sh",
  "powershell": "powershell -File .windsurf/hooks/scripts/check.ps1"
}
```

- macOS / Linux always use `command` via bash.
- Windows uses `powershell` if set; otherwise tries `command` via PowerShell.

## Canonical script structure

```bash
#!/usr/bin/env bash
set -u

INPUT="$(cat)"
EVENT="$(printf '%s' "$INPUT" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("agent_action_name", ""))')"

case "$EVENT" in
  pre_run_command)
    CMD="$(printf '%s' "$INPUT" | python3 -c 'import json, sys; d = json.load(sys.stdin); print(d.get("tool_info", {}).get("command_line", ""))')"
    case "$CMD" in
      *"rm -rf /"*)
        echo "Blocked: destructive command detected." >&2
        exit 2
        ;;
    esac
    ;;
esac

exit 0
```

## post_setup_worktree special

The `post_setup_worktree` event sets a `$ROOT_WORKSPACE_PATH` env var pointing to the original repo. Useful for copying configs from the original workspace into the new worktree.

## Hardening

- Quote variables (`"$var"`).
- `set -u`.
- Idempotent.
- Sub-second target.
- Use `python3` for JSON parsing (more portable than `jq` and works on Windows via WSL or native Python).

## Adding a hook script

1. Drop the script under `<project>/.windsurf/hooks/scripts/` (workspace) or `~/.codeium/windsurf/hooks/scripts/` (user).
2. `chmod +x` (macOS/Linux) or save as `.ps1` (Windows).
3. Reference it in the corresponding `hooks.json`.
4. If supporting Windows users: add the `powershell` variant alongside `command`.

## Enterprise distribution

Enterprise admins can deploy hooks via:

- **Cloud dashboard**: Team Settings → Cascade Hooks (requires Enterprise plan).
- **System paths**: place `hooks.json` at the system path (cannot be disabled by users without root).

System hooks merge with user and workspace hooks; execution order: cloud → system → user → workspace.
