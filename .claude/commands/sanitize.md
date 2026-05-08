---
description: Scan tracked files for private-project leaks (forbidden strings, absolute paths, likely secrets) and report findings as a punch list.
---

Run a sanitization sweep over the SpecForge repository. SpecForge is a public open-source repo; private upstream codebases must never leak into tracked files.

Execute these checks in order, using only `git`-tracked files (so gitignored files like `initial.md` and `.claude/settings.local.json` are excluded):

```bash
# 1. Confirm gitignore is in place
echo "── gitignore status ──"
grep -E "settings\.local|initial\.md" .gitignore || echo "WARN: expected gitignore entries missing"

# 2. Forbidden upstream-project strings (case-insensitive, tracked files only).
#    Wordlist lives in .claude/.forbidden-strings.txt (gitignored, per-installation).
echo
echo "── forbidden strings ──"
WORDLIST=".claude/.forbidden-strings.txt"
if [ ! -f "$WORDLIST" ]; then
  echo "WARN  $WORDLIST missing — no terms to scan. Populate it with any private upstream names."
else
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in '#'*|'') continue ;; esac
    s="$(printf '%s' "$line" | tr -d '[:space:]')"
    [ -z "$s" ] && continue
    hits=$(git grep -l -i -- "$s" 2>/dev/null)
    if [ -n "$hits" ]; then
      echo "FAIL  '$s' found in:"
      echo "$hits" | sed 's/^/    /'
    fi
  done < "$WORDLIST"
fi

# 3. Absolute filesystem paths into private repos
echo
echo "── absolute path leaks ──"
git grep -nE "/Users/[^/]+/LocalDev/" -- '*.md' '*.json' '*.toml' '*.yaml' '*.yml' 2>/dev/null \
  | grep -v "<user>" | grep -v "<private>" \
  || echo "OK    no absolute paths into private repos"

# 4. Likely secrets in tracked files
echo
echo "── likely secrets ──"
git grep -nE "(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9_-]{16,}" \
  -- '*.md' '*.json' '*.toml' '*.yaml' '*.yml' '*.sh' 2>/dev/null \
  || echo "OK    no obvious secrets"

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
- If any "FAIL" appears, treat it as a blocker — do not proceed with `git commit` or `git push` until resolved.
- If everything is "OK", say so plainly — don't pad the response.

For a deeper review (logic-level audit, not just string match), invoke the `sanitization-auditor` agent.
