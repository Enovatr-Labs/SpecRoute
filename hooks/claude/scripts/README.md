# Claude Code Hook Scripts

Supporting shell scripts referenced by `hooks/claude/hooks.template.json`. Each script is small, fast, idempotent, and follows the hook protocol.

## Hook protocol summary

- **Stdin**: Hook scripts receive a JSON object on stdin. Parse with `python3` (portable) or `jq` (if available).

  ```bash
  INPUT="$(cat)"
  COMMAND="$(printf '%s' "$INPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))')"
  ```

- **Exit codes**: `0` allows / proceeds. Non-zero **blocks** (PreToolUse only); `PostToolUse` and `SessionStart` cannot block - non-zero is informational.

- **Stderr**: Anything on stderr is shown to the user. Use for actionable messages.

- **Stdout**: Discarded by Claude Code. Don't rely on it for user-facing output.

## Reference implementations

See [`../../../.claude/hooks/`](../../../.claude/hooks/) at the repo root for working hooks:

- `session-start-status.sh` - prints a SpecForge skeleton status banner.
- `pre-bash-sanitize.sh` - blocks `git commit`/`git push` if forbidden strings appear in tracked files.
- `post-edit-frontmatter.sh` - validates frontmatter when agent/skill/command files are written or edited.

These are the canonical worked examples - copy and adapt them rather than starting from scratch.

## Common patterns

### Pre-commit gate

```bash
#!/usr/bin/env bash
# Block git commit/push on a custom check.
set -u
INPUT="$(cat)"
COMMAND="$(printf '%s' "$INPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))')"
case "$COMMAND" in
  *"git commit"*|*"git push"*) ;;
  *) exit 0 ;;
esac

# Run check. Exit 1 with stderr message to block.
if ! <your check command>; then
  echo "Pre-commit check failed: <reason>" >&2
  exit 1
fi
exit 0
```

### File-write validator

```bash
#!/usr/bin/env bash
# Validate frontmatter or content on Write/Edit.
set -u
INPUT="$(cat)"
FILE_PATH="$(printf '%s' "$INPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')"
[ -z "$FILE_PATH" ] && exit 0
[ ! -f "$FILE_PATH" ] && exit 0

# Only validate paths that fall under a contract.
case "$FILE_PATH" in
  */agents/*.md|*/.claude/agents/*.md) ;;
  *) exit 0 ;;
esac

<validation logic; warn on stderr if needed>
exit 0
```

### Session-start banner

```bash
#!/usr/bin/env bash
# Informational only - prints to user.
set -u
echo "── <project> status ──"
<status checks>
echo "──"
exit 0
```

## Hardening

- **Quote variables**: `"$var"` not `$var` - paths with spaces will break.
- **Avoid eval and unquoted command interpolation**.
- **Use `set -u`** to catch unset variables.
- **Sub-second execution target**. Slow hooks degrade the agent CLI.
- **Be idempotent**. Hooks fire on every matching event.
- **Don't write to tracked files** during PostToolUse - that creates infinite loops with PostToolUse hooks that match Write.

## Adding a hook script

1. Drop the script into this directory (or `runtimes/.claude/hooks/scripts/` for the consumer-facing template).
2. `chmod +x` so the runtime can execute it.
3. Reference it in `hooks.template.json`.
4. Test by triggering the matching event.
