# `.claude/hooks/scripts/`

Supporting shell scripts referenced by `hooks.json`. Each script must:

- Be executable (`chmod +x`).
- Read JSON from stdin (parse with `python3` or `jq`).
- Exit `0` to allow / proceed; non-zero to block (`PreToolUse` only).
- Write actionable messages to stderr.
- Run sub-second.
- Be idempotent.

## Reference implementations

See the SpecForge framework's own hooks at [`.claude/hooks/`](../../../../.claude/hooks/) (relative to repo root):

- `session-start-status.sh` — SpecForge skeleton status banner.
- `pre-bash-sanitize.sh` — sanitization gate on `git commit` / `git push`.
- `post-edit-frontmatter.sh` — frontmatter validation on agent/skill/command writes.

These are the canonical worked examples — copy and adapt them for your project rather than starting from scratch.

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
