#!/usr/bin/env bash
# PreToolUse hook (matcher: Bash): blocks `git commit` and `git push` if
# tracked files contain any string from the gitignored wordlist at
# .claude/.forbidden-strings.txt.
#
# Hook protocol:
#   - Reads JSON from stdin: { "tool_input": { "command": "..." }, ... }
#   - Exit 0 = allow the Bash invocation
#   - Exit non-zero = block; the message on stderr is shown to the user
#
# If the wordlist file is missing, the hook does nothing (no false-positive blocks).
# Each clone of SpecRoute populates its own .claude/.forbidden-strings.txt.

set -u

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WORDLIST="$REPO_ROOT/.claude/.forbidden-strings.txt"

INPUT="$(cat)"
COMMAND="$(printf '%s' "$INPUT" | python3 -c 'import json,sys
try:
    d = json.load(sys.stdin)
    print(d.get("tool_input", {}).get("command", ""))
except Exception:
    print("")
' 2>/dev/null)"

# Only gate publish-style commands.
case "$COMMAND" in
  *"git commit"*|*"git push"*|*"gh pr create"*|*"gh release create"*) ;;
  *) exit 0 ;;
esac

# No wordlist = no scan. Don't fabricate a block.
[ -f "$WORDLIST" ] || exit 0

cd "$REPO_ROOT"

HITS=()
while IFS= read -r line || [ -n "$line" ]; do
  # Skip comments and blank lines.
  case "$line" in '#'*|'') continue ;; esac
  s="$(printf '%s' "$line" | tr -d '[:space:]')"
  [ -z "$s" ] && continue
  if matched="$(git grep -l -i -- "$s" 2>/dev/null)"; then
    if [ -n "$matched" ]; then
      while IFS= read -r f; do
        [ -n "$f" ] && HITS+=("$s -> $f")
      done <<< "$matched"
    fi
  fi
done < "$WORDLIST"

if [ "${#HITS[@]}" -gt 0 ]; then
  {
    echo "Sanitization gate blocked the publish command."
    echo "Forbidden strings (from .claude/.forbidden-strings.txt) found in tracked files:"
    printf '  - %s\n' "${HITS[@]}"
    echo
    echo "Resolve before committing/pushing. Run /sanitize for full details, or invoke the sanitization-auditor agent."
  } >&2
  exit 1
fi

exit 0
