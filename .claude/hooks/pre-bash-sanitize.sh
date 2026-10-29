#!/usr/bin/env bash
# PreToolUse hook (matcher: Bash): blocks commit and publication commands if
# the working tree, staged index, or outgoing history contains a string from
# the gitignored wordlist at .claude/.forbidden-strings.txt.
#
# Hook protocol:
#   - Reads JSON from stdin: { "tool_input": { "command": "..." }, ... }
#   - Exit 0 = allow the Bash invocation
#   - Exit 2 = block; other non-zero exits are non-blocking hook errors
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
    print("__SPECROUTE_UNPARSEABLE_PAYLOAD__")
' 2>/dev/null)"

# Classify real publish commands rather than looking for a brittle substring.
# Handles newline/subshell/group separators, env/time/nohup/sudo/exec wrappers,
# `sh -c` / `eval` recursion, absolute paths, and Git global options, while
# ignoring quoted text such as `echo "git commit"`. A parse failure classifies
# as "publish" (fail closed): the wordlist scan is the gate, so it must run.
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
' 2>/dev/null)"
# An unparseable payload fails closed: run the scan instead of allowing.
[ "$COMMAND" = "__SPECROUTE_UNPARSEABLE_PAYLOAD__" ] && MODE="publish"
[ "$MODE" != "none" ] || exit 0

# No wordlist = no scan. Don't fabricate a block.
[ -f "$WORDLIST" ] || exit 0

cd "$REPO_ROOT" || {
  echo "Sanitization gate could not enter the repository; blocking publish." >&2
  exit 2
}

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

  # The index is the exact content `git commit` will publish. It may differ
  # from both HEAD and the working tree when a file is partially staged.
  staged="$(git grep --cached -l -i -- "$s" 2>/dev/null || true)"
  if [ -n "$staged" ]; then
    while IFS= read -r f; do
      [ -n "$f" ] && HITS+=("$s -> index:$f")
    done <<< "$staged"
  fi

  # PRs, releases, and pushes can publish commits that no longer appear in the
  # current tree. Scan the outgoing range; for a branch without an upstream,
  # scan all reachable commits rather than silently skipping history.
  if [ "$MODE" = "publish" ]; then
    upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
    if [ -n "$upstream" ]; then
      revisions="$(git rev-list "$upstream..HEAD" 2>/dev/null || true)"
    else
      revisions="$(git rev-list HEAD 2>/dev/null || true)"
    fi
    if [ -n "$revisions" ]; then
      historical="$(git grep -l -i -- "$s" $revisions -- 2>/dev/null || true)"
      if [ -n "$historical" ]; then
        while IFS= read -r f; do
          [ -n "$f" ] && HITS+=("$s -> outgoing:$f")
        done <<< "$historical"
      fi
    fi
  fi
done < "$WORDLIST"

if [ "${#HITS[@]}" -gt 0 ]; then
  {
    echo "Sanitization gate blocked the publish command."
    echo "Forbidden strings were found in the working tree, staged index, or outgoing commits:"
    printf '  - %s\n' "${HITS[@]}"
    echo
    echo "Resolve before committing/pushing. Run /sanitize for full details, or invoke the sanitization-auditor agent."
  } >&2
  exit 2
fi

exit 0
