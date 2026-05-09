#!/usr/bin/env bash
# PreToolUse hook (matcher: Bash): blocks publish-style commands when tracked
# files contain a term listed in .claude/.forbidden-strings.txt.

set -u

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
WORDLIST="$REPO_ROOT/.claude/.forbidden-strings.txt"

INPUT="$(cat)"
COMMAND="$(printf '%s' "$INPUT" | python3 -c 'import json,sys
try:
    d = json.load(sys.stdin)
    print(d.get("tool_input", {}).get("command", ""))
except Exception:
    print("")
' 2>/dev/null)"

case "$COMMAND" in
  *"git commit"*|*"git push"*|*"gh pr create"*|*"gh release create"*) ;;
  *) exit 0 ;;
esac

[ -f "$WORDLIST" ] || exit 0

cd "$REPO_ROOT" || exit 0

HITS=()
while IFS= read -r line || [ -n "$line" ]; do
  case "$line" in '#'*|'') continue ;; esac
  term="$(printf '%s' "$line" | tr -d '[:space:]')"
  [ -z "$term" ] && continue
  if matched="$(git grep -l -i -- "$term" 2>/dev/null)"; then
    if [ -n "$matched" ]; then
      while IFS= read -r file_path; do
        [ -n "$file_path" ] && HITS+=("$term -> $file_path")
      done <<< "$matched"
    fi
  fi
done < "$WORDLIST"

if [ "${#HITS[@]}" -gt 0 ]; then
  {
    echo "Sanitization gate blocked the publish command."
    echo "Forbidden strings from .claude/.forbidden-strings.txt were found in tracked files:"
    printf '  - %s\n' "${HITS[@]}"
    echo
    echo "Generalize or remove these strings before publishing."
  } >&2
  exit 1
fi

exit 0
