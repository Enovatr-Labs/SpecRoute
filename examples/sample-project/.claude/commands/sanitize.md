---
description: Scan tracked files for private-project leaks (forbidden strings, absolute paths, likely secrets) and report findings as a punch list.
---

Run a sanitization sweep over the SpecRoute repository. SpecRoute is a public open-source repo; private upstream codebases must never leak into tracked files.

Execute these checks in order, over tracked **and** newly-added files (gitignored files like `initial.md` and `.claude/settings.local.json` stay excluded):

```bash
# 1. Confirm gitignore is in place
echo "── gitignore status ──"
grep -E "settings\.local|initial\.md" .gitignore || echo "WARN: expected gitignore entries missing"

# 2. Forbidden upstream-project strings (case-insensitive; working tree,
#    untracked additions, and the staged index).
#    Wordlist lives in .claude/.forbidden-strings.txt (gitignored, per-installation).
echo
echo "── forbidden strings ──"
SCAN="$(mktemp)"; trap 'rm -f "$SCAN"' EXIT
{ git ls-files -z; git ls-files -z --others --exclude-standard; } > "$SCAN"
# git grep reads TRACKED files only, so a commit that ADDS a leaking file is
# invisible to it. Scan tracked + untracked-but-not-ignored instead.
WORDLIST=".claude/.forbidden-strings.txt"
if [ ! -f "$WORDLIST" ]; then
  echo "WARN  $WORDLIST missing - no terms to scan. Populate it with any private upstream names."
else
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in '#'*|'') continue ;; esac
    s="$(printf '%s' "$line" | tr -d '[:space:]')"
    [ -z "$s" ] && continue
    hits=$(xargs -0 grep -l -i -I -e "$s" < "$SCAN" 2>/dev/null || true)
    if [ -n "$hits" ]; then
      echo "FAIL  '$s' found in:"
      echo "$hits" | sed 's/^/    /'
    fi
    staged=$(git grep --cached -l -i -- "$s" 2>/dev/null || true)
    if [ -n "$staged" ]; then
      echo "FAIL  '$s' found in staged index:"
      echo "$staged" | sed 's/^/    /'
    fi
  done < "$WORDLIST"
fi

# 3. Absolute filesystem paths and their flattened equivalents.
#    Two shapes, because a leak can hide in either:
#      a) /Users/<name>/   - any bare home-directory absolute path
#      b) -Users-<name>-   - the FLATTENED form Claude uses for project dirs,
#                            e.g. ~/.claude/projects/-Users-<name>-<repo>/
#    Known-benign lines are dropped by IGNORE_RE - documented placeholders and
#    regex-source lines (a `[^` character-class fragment means it is a pattern,
#    not a path). Extend IGNORE_RE rather than deleting a check.
#    `U` is interpolated so this command's own source does not self-match.
echo
echo "── absolute / flattened path leaks ──"
U="Users"
IGNORE_RE='<user>|<private>|<name>|<repo>|<flattened-project-path>|yourname|youruser|\[\^'
xargs -0 grep -nHE -I -e "/$U/[^/[:space:]]+/" -e "-$U-[A-Za-z0-9]+-" < "$SCAN" 2>/dev/null \
  | grep -Ev "$IGNORE_RE" \
  || echo "OK    no absolute or flattened path leaks"
git grep --cached -nE "/$U/[^/[:space:]]+/|-$U-[A-Za-z0-9]+-" \
  -- '*.md' '*.json' '*.toml' '*.yaml' '*.yml' '*.sh' '*.py' 2>/dev/null \
  | grep -Ev "$IGNORE_RE" || true

# 4. Likely secrets in tracked files
echo
echo "── likely secrets ──"
xargs -0 grep -nHE -I -e "(api[_-]?key|secret|token|password)[[:space:]]*[:=][[:space:]]*['\"][A-Za-z0-9_-]{16,}" < "$SCAN" 2>/dev/null \
  || echo "OK    no obvious secrets"
git grep --cached -nE "(api[_-]?key|secret|token|password)[[:space:]]*[:=][[:space:]]*['\"][A-Za-z0-9_-]{16,}" \
  -- '*.md' '*.json' '*.toml' '*.yaml' '*.yml' '*.sh' 2>/dev/null || true

# 5. What would actually be committed
echo
echo "── tracked file inventory ──"
git ls-files | wc -l | xargs echo "Tracked files:"
echo
echo "── current diff status ──"
git status --short
```

After running:

- Report findings as a clear punch list: file, line, the specific string, suggested replacement.
- If any "FAIL" appears, treat it as a blocker - do not proceed with `git commit` or `git push` until resolved.
- If everything is "OK", say so plainly - don't pad the response.

For a deeper review (logic-level audit, not just string match), invoke the `sanitization-auditor` agent.
