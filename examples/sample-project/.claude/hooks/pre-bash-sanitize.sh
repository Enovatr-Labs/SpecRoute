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
MODE="$(printf '%s' "$COMMAND" | python3 -c '
import re, sys
text = sys.stdin.read()
prefix = r"(?:^|[;&|])\s*(?:[A-Za-z_]\w*=\S+\s+)*(?:command\s+)?"
git = re.search(prefix + r"git(?:\s+(?:(?:-C|-c|--git-dir|--work-tree)\s+\S+|--(?:git-dir|work-tree)=\S+))*\s+(commit|push)\b", text)
gh = re.search(prefix + r"gh\s+(?:pr|release)\s+create\b", text)
print("publish" if gh or git and git.group(1) == "push" else "commit" if git else "none")
')"
[ "$MODE" != "none" ] || exit 0

# No wordlist = no scan. Don't fabricate a block.
[ -f "$WORDLIST" ] || exit 0

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

# Scan scope: tracked files AND untracked-but-not-ignored files.
#
# `git grep` alone reads only TRACKED content. A commit that ADDS a leaking file
# would sail straight through this gate, because at hook time that file is still
# untracked - which is exactly the content most likely to leak. Ignored files are
# excluded on purpose (--exclude-standard): the wordlist itself lives in one.
FILES="$(mktemp)"
trap 'rm -f "$FILES"' EXIT
{ git ls-files -z; git ls-files -z --others --exclude-standard; } \
  | grep -zv '^\.claude/\.forbidden-strings\.txt$' > "$FILES" || true
# The wordlist is excluded from its own scan. It necessarily contains every
# forbidden term, so including it makes the gate match on every run and block
# forever - and a gate that always blocks gets switched off. It is gitignored in
# this repo, but a fresh consumer clone may not have added it yet, so exclude it
# explicitly rather than relying on --exclude-standard.

HITS=()
while IFS= read -r line || [ -n "$line" ]; do
  # Skip comments and blank lines.
  case "$line" in '#'*|'') continue ;; esac
  s="$(printf '%s' "$line" | tr -d '[:space:]')"
  [ -z "$s" ] && continue
  # -0 keeps paths with spaces intact; -I skips binary files.
  #
  # Do NOT gate on exit status here. xargs may split the file list across several
  # grep invocations, and grep exits 1 on "no match" - so xargs returns 123 whenever
  # ANY batch is clean, even if an earlier batch found a real hit. Capture the output
  # and test it for emptiness instead; `|| true` keeps `set -u`/pipefail-free shells
  # from tripping on the non-zero status.
  matched="$(xargs -0 grep -l -i -I -e "$s" < "$FILES" 2>/dev/null || true)"
  if [ -n "$matched" ]; then
    while IFS= read -r f; do
      [ -n "$f" ] && HITS+=("$s -> worktree:$f")
    done <<< "$matched"
  fi
  staged="$(git grep --cached -l -i -- "$s" 2>/dev/null || true)"
  while IFS= read -r f; do
    [ -n "$f" ] && HITS+=("$s -> index:$f")
  done <<< "$staged"
  if [ "$MODE" = "publish" ]; then
    upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
    [ -n "$upstream" ] && revisions="$(git rev-list "$upstream..HEAD" 2>/dev/null || true)" || revisions="$(git rev-list HEAD 2>/dev/null || true)"
    historical=""
    [ -z "$revisions" ] || historical="$(git grep -l -i -- "$s" $revisions -- 2>/dev/null || true)"
    while IFS= read -r f; do
      [ -n "$f" ] && HITS+=("$s -> outgoing:$f")
    done <<< "$historical"
  fi
done < "$WORDLIST"

if [ "${#HITS[@]}" -gt 0 ]; then
  {
    echo "Sanitization gate blocked the publish command."
    echo "Forbidden strings (from .claude/.forbidden-strings.txt) found in tracked or newly-added files:"
    printf '  - %s\n' "${HITS[@]}"
    echo
    echo "Resolve before committing/pushing. Run /sanitize for full details, or invoke the sanitization-auditor agent."
  } >&2
  exit 2
fi

exit 0
