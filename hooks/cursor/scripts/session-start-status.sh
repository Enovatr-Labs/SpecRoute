#!/usr/bin/env bash
# Cursor sessionStart hook: prints a compact SpecRoute orientation banner.
# Informational only - always exits 0.
#
# sessionStart accepts an additional_context key, which injects the banner into the
# conversation. Also repeated on stderr for the hook log.

set -u

# The script lives at <workspace>/.cursor/hooks/scripts/, so three levels up is
# the workspace root. Cursor also exports CURSOR_PROJECT_DIR, which is preferred when present.
REPO_ROOT="${CURSOR_PROJECT_DIR:-$(cd "$(dirname "$0")/../../.." && pwd)}"
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

printf '%s\n' "$BANNER" >&2
printf '%s' "$BANNER" | python3 -c 'import json, sys
print(json.dumps({"additional_context": sys.stdin.read()}))'
exit 0
