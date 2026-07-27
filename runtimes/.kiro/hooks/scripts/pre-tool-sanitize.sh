#!/usr/bin/env bash
# Kiro PreToolUse hook: blocks publish-style commands (git commit, git push,
# gh pr create, gh release create) while publishable content still contains a term
# from the per-installation forbidden-strings wordlist.
#
# Registered with an empty matcher on purpose. Kiro matches PreToolUse on the tool
# name, and a matcher that fails to match is a silent hole rather than a loud
# failure - so the filtering happens here, where it is testable. Exit 2 blocks and
# stderr becomes the rejection reason.

set -u

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

INPUT="$(cat)"

# Payload shapes differ across vendors and across releases of the same vendor,
# so the command is located by searching the whole payload for any key that has
# been used to carry it. A narrower reader that misses the key would fail open,
# which is the exact failure this gate exists to prevent.
COMMAND="$(printf '%s' "$INPUT" | python3 -c '
import json, sys

KEYS = ("command", "command_line", "commandLine", "cmd", "shell_command", "script")

def walk(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in KEYS and isinstance(value, str) and value.strip():
                yield value
            yield from walk(value)
        return
    if isinstance(node, list):
        for item in node:
            yield from walk(item)

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

for found in walk(payload):
    print(found)
    break
' 2>/dev/null)"

MODE="$(printf '%s' "$COMMAND" | python3 -c '
import re, sys
text = sys.stdin.read()
prefix = r"(?:^|[;&|])\s*(?:[A-Za-z_]\w*=\S+\s+)*(?:command\s+)?"
git = re.search(prefix + r"git(?:\s+(?:(?:-C|-c|--git-dir|--work-tree)\s+\S+|--(?:git-dir|work-tree)=\S+))*\s+(commit|push)\b", text)
gh = re.search(prefix + r"gh\s+(?:pr|release)\s+create\b", text)
print("publish" if gh or git and git.group(1) == "push" else "commit" if git else "none")
')"
[ "$MODE" != "none" ] || exit 0

# The wordlist is per-installation and gitignored. Prefer this runtime's copy,
# then fall back to the Claude location so a mixed-vendor repo keeps one list.
WORDLIST=""
for candidate in "$REPO_ROOT/.kiro/.forbidden-strings.txt" "$REPO_ROOT/.claude/.forbidden-strings.txt"; do
  if [ -f "$candidate" ]; then
    WORDLIST="$candidate"
    break
  fi
done

if [ -z "$WORDLIST" ]; then
  exit 0
fi

cd "$REPO_ROOT" || { echo "Sanitization gate could not enter the repository." >&2; exit 2; }

WORDLIST_REL="${WORDLIST#$REPO_ROOT/}"
if ! git check-ignore --no-index -q -- "$WORDLIST_REL"; then
  echo "Sanitization gate blocked: $WORDLIST_REL must be listed in .gitignore." >&2
  exit 2
fi
if git ls-files --error-unmatch -- "$WORDLIST_REL" >/dev/null 2>&1; then
  echo "Sanitization gate blocked: $WORDLIST_REL is tracked; remove it from the index." >&2
  exit 2
fi

FILES="$(mktemp)"
trap 'rm -f "$FILES"' EXIT
{ git ls-files -z; git ls-files -z --others --exclude-standard; } > "$FILES"
HITS=()
while IFS= read -r line || [ -n "$line" ]; do
  case "$line" in '#'*|'') continue ;; esac
  term="$(printf '%s' "$line" | tr -d '[:space:]')"
  [ -z "$term" ] && continue
  matched="$(xargs -0 grep -l -i -I -e "$term" < "$FILES" 2>/dev/null || true)"
  while IFS= read -r hit_path; do
    [ -n "$hit_path" ] && HITS+=("$term -> worktree:$hit_path")
  done <<< "$matched"
  staged="$(git grep --cached -l -i -- "$term" 2>/dev/null || true)"
  while IFS= read -r hit_path; do
    [ -n "$hit_path" ] && HITS+=("$term -> index:$hit_path")
  done <<< "$staged"
  if [ "$MODE" = "publish" ]; then
    upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
    [ -n "$upstream" ] && revisions="$(git rev-list "$upstream..HEAD" 2>/dev/null || true)" || revisions="$(git rev-list HEAD 2>/dev/null || true)"
    historical=""
    [ -z "$revisions" ] || historical="$(git grep -l -i -- "$term" $revisions -- 2>/dev/null || true)"
    while IFS= read -r hit_path; do
      [ -n "$hit_path" ] && HITS+=("$term -> outgoing:$hit_path")
    done <<< "$historical"
  fi
done < "$WORDLIST"

if [ "${#HITS[@]}" -gt 0 ]; then
  REASON="Sanitization gate blocked the publish command. Forbidden strings are present in the worktree, index, or outgoing commits:
$(printf '  - %s\n' "${HITS[@]}")
Generalize or remove these strings before publishing."
  printf '%s\n' "$REASON" >&2
  exit 2
fi

exit 0
