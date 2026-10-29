#!/usr/bin/env bash
# Devin Desktop PreToolUse hook for the exec tool: blocks publish-style commands (git commit, git push,
# gh pr create, gh release create) while publishable content still contains a term
# from the per-installation forbidden-strings wordlist.
#
# Exit 2 blocks the command and stderr becomes the message shown to the user.

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
    print("__SPECROUTE_UNPARSEABLE_PAYLOAD__")
    sys.exit(0)

for found in walk(payload):
    print(found)
    break
' 2>/dev/null)"

MODE="$(printf '%s' "$COMMAND" | python3 -c '
import os, re, shlex, sys

RANK = {"none": 0, "commit": 1, "publish": 2}
SEPCHARS = set(";&|()\n")
SKIP = {"{", "}", "!", "if", "then", "else", "elif", "do", "while", "until", "fi", "done"}
SHELLS = {"bash", "sh", "zsh", "dash", "ksh"}
# wrapper -> option flags that consume a following value
WRAPPERS = {
    "command": set(), "builtin": set(), "nohup": set(), "exec": {"-a"},
    "time": {"-f", "-o"}, "env": {"-u", "-C", "-S"}, "sudo": {"-u", "-g", "-h", "-p", "-C", "-D", "-R", "-T", "-U"},
    "doas": {"-u", "-C"}, "nice": {"-n"}, "ionice": {"-c", "-n", "-p"}, "setsid": set(),
    "stdbuf": {"-i", "-o", "-e"}, "xargs": {"-I", "-n", "-P", "-L", "-s", "-d", "-E"},
    "timeout": {"-s", "-k"},
}
ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def lex(text):
    lexer = shlex.shlex(text, posix=True, punctuation_chars=";&|()\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    return list(lexer)


def split(words):
    commands, current = [], []
    for word in words:
        if set(word) <= SEPCHARS:
            if current:
                commands.append(current)
            current = []
        else:
            current.append(word)
    if current:
        commands.append(current)
    return commands


def classify_command(command, depth):
    while command:
        word = command[0]
        base = os.path.basename(word)
        if word in SKIP or ASSIGN.match(word):
            command = command[1:]
        elif base in WRAPPERS:
            valued = WRAPPERS[base]
            command = command[1:]
            while command and (command[0].startswith("-") or ASSIGN.match(command[0]) and base == "env"):
                flag = command[0]
                command = command[1:]
                if flag in valued and command:
                    command = command[1:]
            if base == "timeout" and command:
                command = command[1:]
        else:
            break
    if not command:
        return "none"
    base = os.path.basename(command[0])
    if base in SHELLS:
        for i, arg in enumerate(command[1:], 1):
            if arg.startswith("-") and not arg.startswith("--") and "c" in arg[1:]:
                return classify(command[i + 1], depth + 1) if i + 1 < len(command) else "none"
        return "none"
    if base == "eval":
        return classify(" ".join(command[1:]), depth + 1)
    mode = "none"
    if base == "git":
        index = 1
        while index < len(command):
            value = command[index]
            if value in {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}:
                index += 2
            elif value.startswith("-"):
                index += 1
            else:
                break
        sub = command[index] if index < len(command) else ""
        mode = "commit" if sub == "commit" else "publish" if sub == "push" else "none"
    elif base == "gh" and len(command) >= 3 and command[1:3] in (["pr", "create"], ["release", "create"]):
        mode = "publish"
    # Command substitution inside arguments still executes.
    for arg in command[1:]:
        if "$(" in arg or "`" in arg:
            sub = classify(arg.replace("`", "$("), depth + 1)
            if RANK[sub] > RANK[mode]:
                mode = sub
    return mode


def classify(text, depth=0):
    if depth > 5:
        return "publish"
    try:
        commands = split(lex(text))
    except Exception:
        return "publish"  # fail closed: unparseable input still gets the scan
    mode = "none"
    for command in commands:
        found = classify_command(command, depth)
        if RANK[found] > RANK[mode]:
            mode = found
    return mode


print(classify(sys.stdin.read()))
')"
# An unparseable payload fails closed: run the scan instead of allowing.
[ "$COMMAND" = "__SPECROUTE_UNPARSEABLE_PAYLOAD__" ] && MODE="publish"
[ "$MODE" != "none" ] || exit 0

# The wordlist is per-installation and gitignored. Prefer this runtime's copy,
# then fall back to the Claude location so a mixed-vendor repo keeps one list.
WORDLIST=""
for candidate in "$REPO_ROOT/.devin/.forbidden-strings.txt" "$REPO_ROOT/.claude/.forbidden-strings.txt"; do
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

FILES="$(mktemp)"; trap 'rm -f "$FILES"' EXIT
{ git ls-files -z; git ls-files -z --others --exclude-standard; } > "$FILES"
HITS=()
while IFS= read -r line || [ -n "$line" ]; do
  case "$line" in '#'*|'') continue ;; esac
  term="$(printf '%s' "$line" | tr -d '[:space:]')"
  [ -z "$term" ] && continue
  matched="$(xargs -0 grep -l -i -I -e "$term" < "$FILES" 2>/dev/null || true)"
  while IFS= read -r hit_path; do [ -n "$hit_path" ] && HITS+=("$term -> worktree:$hit_path"); done <<< "$matched"
  staged="$(git grep --cached -l -i -- "$term" 2>/dev/null || true)"
  while IFS= read -r hit_path; do [ -n "$hit_path" ] && HITS+=("$term -> index:$hit_path"); done <<< "$staged"
  if [ "$MODE" = "publish" ]; then
    upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
    [ -n "$upstream" ] && revisions="$(git rev-list "$upstream..HEAD" 2>/dev/null || true)" || revisions="$(git rev-list HEAD 2>/dev/null || true)"
    historical=""; [ -z "$revisions" ] || historical="$(git grep -l -i -- "$term" $revisions -- 2>/dev/null || true)"
    while IFS= read -r hit_path; do [ -n "$hit_path" ] && HITS+=("$term -> outgoing:$hit_path"); done <<< "$historical"
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
