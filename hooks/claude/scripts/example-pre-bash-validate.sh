#!/usr/bin/env bash
# Example PreToolUse hook (matcher: Bash). Demonstrates the protocol:
# - read stdin JSON, extract command
# - decide whether to gate based on the command's tokens
# - exit 0 to allow, exit 2 to block (stderr is shown to Claude as the reason)
#   Any other non-zero exit is a NON-blocking error: the tool call still runs.
#
# ILLUSTRATIVE ONLY - this is not a security boundary. A shell command can be
# reshaped in endless ways (variables, eval, wrappers, scripts), so a token
# check here catches the obvious spelling of the mistake, not a determined
# bypass. Use permissions/sandboxing for real enforcement.
#
# Adapt this script for project-specific gates (lint, format, security checks).

set -u

INPUT="$(cat)"
# Prints "block" when any command in the line is `rm` with both a recursive and
# a force flag, in any spelling (-rf, -fr, -r -f, --recursive --force).
VERDICT="$(printf '%s' "$INPUT" | python3 -c 'import json, shlex, sys
try:
    command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    words = list(lexer)
except Exception:
    print("block")  # unparseable input: fail closed
    raise SystemExit
commands, current = [], []
for word in words + [";"]:
    if set(word) <= set(";&|()\n"):
        if current:
            commands.append(current)
        current = []
    else:
        current.append(word)
for cmd in commands:
    if cmd[0].rsplit("/", 1)[-1] != "rm":
        continue
    flags = [w for w in cmd[1:] if w.startswith("-")]
    short = "".join(w[1:] for w in flags if not w.startswith("--"))
    recursive = "r" in short or "R" in short or "--recursive" in flags
    force = "f" in short or "--force" in flags
    if recursive and force:
        print("block")
        break
' 2>/dev/null)"

if [ "$VERDICT" = "block" ]; then
  echo "Blocked: rm -rf is a destructive operation. Use trash, mv, or scoped removal." >&2
  exit 2
fi
exit 0
