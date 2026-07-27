#!/usr/bin/env bash
# SessionStart hook: prints a project status banner so Claude knows what's
# built vs. missing without re-grepping every session.
#
# Exit 0 always - informational only.

set -u

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

echo "── user-search project status ─────────────────────────────────────"

# Top-level dirs in this project's layout. Keep in sync with the same list in
# .claude/commands/status.md. Regenerate the ground truth with: ls -d */
EXPECTED_DIRS=(prds specs adrs prompts agentic-docs)
MISSING=()
PRESENT=()
for d in "${EXPECTED_DIRS[@]}"; do
  if [ -d "$d" ]; then PRESENT+=("$d"); else MISSING+=("$d"); fi
done

echo "Built  (${#PRESENT[@]}/${#EXPECTED_DIRS[@]}): ${PRESENT[*]:-none}"
echo "TODO   (${#MISSING[@]}/${#EXPECTED_DIRS[@]}): ${MISSING[*]:-none}"

# Implementation agents loaded
AGENT_COUNT=0
if [ -d ".claude/agents" ]; then
  AGENT_COUNT=$(find .claude/agents -maxdepth 1 -name "*.md" -not -name "README.md" | wc -l | tr -d ' ')
fi
echo "Agents loaded: $AGENT_COUNT in .claude/agents/"

# Sanitization quick check (won't block the session, just warn).
# Reads forbidden strings from the gitignored wordlist if present.
WORDLIST=".claude/.forbidden-strings.txt"
if [ -f "$WORDLIST" ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in '#'*|'') continue ;; esac
    s="$(printf '%s' "$line" | tr -d '[:space:]')"
    [ -z "$s" ] && continue
    if git grep -l -i -- "$s" >/dev/null 2>&1; then
      echo "⚠  Sanitization: forbidden term in tracked file(s) - run /sanitize"
      break
    fi
  done < "$WORDLIST"
fi

echo "───────────────────────────────────────────────────────────────────"
exit 0
