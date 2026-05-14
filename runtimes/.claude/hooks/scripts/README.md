# `.claude/hooks/scripts/`

Supporting shell scripts referenced by `hooks.json`. Each script must:

- Be executable (`chmod +x`).
- Read JSON from stdin (parse with `python3` or `jq`).
- Exit `0` to allow / proceed; non-zero to block (`PreToolUse` only).
- Write actionable messages to stderr.
- Run sub-second.
- Be idempotent.

## Included starter scripts

This runtime includes starter scripts that match `../hooks.template.json`:

- `session-start-status.sh` - SpecRoute skeleton status banner.
- `pre-bash-sanitize.sh` - sanitization gate on `git commit` / `git push`.
- `post-edit-frontmatter.sh` - frontmatter validation on agent/skill/command writes.

The SpecRoute framework's own active hook installation lives at [`.claude/hooks/`](../../../../.claude/hooks/) and uses the same behavior.

## Canonical script structure

```bash
#!/usr/bin/env bash
set -u

INPUT="$(cat)"

# Extract relevant field from stdin JSON.
FIELD="$(printf '%s' "$INPUT" | python3 -c 'import json, sys
try:
    print(json.load(sys.stdin).get("tool_input", {}).get("<field>", ""))
except Exception:
    print("")
' 2>/dev/null)"

# Decide what to do based on field.
# ...

exit 0
```

See [`hooks/claude/scripts/README.md`](../../../../hooks/claude/scripts/README.md) for hardening guidance.
