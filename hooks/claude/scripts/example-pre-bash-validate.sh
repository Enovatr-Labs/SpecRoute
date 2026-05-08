#!/usr/bin/env bash
# Example PreToolUse hook (matcher: Bash). Demonstrates the protocol:
# - read stdin JSON, extract command
# - decide whether to gate based on command pattern
# - exit 0 to allow, 1 to block (with stderr message)
#
# Adapt this script for project-specific gates (lint, format, security checks).

set -u

INPUT="$(cat)"
COMMAND="$(printf '%s' "$INPUT" | python3 -c 'import json, sys
try:
    print(json.load(sys.stdin).get("tool_input", {}).get("command", ""))
except Exception:
    print("")
' 2>/dev/null)"

# Pass through anything that is not a gated command.
case "$COMMAND" in
  *"rm -rf "*)
    echo "Blocked: rm -rf is a destructive operation. Use trash, mv, or scoped removal." >&2
    exit 1
    ;;
  *)
    exit 0
    ;;
esac
