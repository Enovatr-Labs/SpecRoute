#!/usr/bin/env bash
# Codex SessionStart hook: prints a compact SpecRoute orientation banner.
# Informational only - always exits 0.
#
# Codex accepts either plain text on stdout (used as context) or Claude-compatible
# JSON. This emits the JSON form so the banner lands in the model's context.

set -u

# The script lives at <workspace>/.codex/hooks/scripts/, so three levels up is
# the workspace root. Codex runs hook commands from the workspace root, so the relative command
# path in hooks.json and this resolution agree.
REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$REPO_ROOT" || exit 0

# Drain stdin so the caller never blocks writing into an unread pipe.
INPUT="$(cat 2>/dev/null || true)"
: "${INPUT:-}"

EXPECTED_DIRS=(agentic-docs prds specs agents skills commands hooks prompts workflows rules runtimes examples tools assets scripts wiki)
PRESENT=()
MISSING=()

for d in "${EXPECTED_DIRS[@]}"; do
  if [ -d "$d" ]; then
    PRESENT+=("$d")
  else
    MISSING+=("$d")
  fi
done

BANNER="-- project status --------------------------------------------------
Present dirs (${#PRESENT[@]}/${#EXPECTED_DIRS[@]}): ${PRESENT[*]:-none}
Missing dirs (${#MISSING[@]}/${#EXPECTED_DIRS[@]}): ${MISSING[*]:-none}"

if [ -f "AGENTS.md" ]; then
  BANNER="$BANNER
Root context: AGENTS.md"
fi

BANNER="$BANNER
--------------------------------------------------------------------"

printf '%s' "$BANNER" | python3 -c 'import json, sys
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": sys.stdin.read()}}))'
exit 0
