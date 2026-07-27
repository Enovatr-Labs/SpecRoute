#!/usr/bin/env bash
# Gemini CLI SessionStart hook: prints a compact SpecRoute orientation banner.
# Informational only - always exits 0.
#
# Gemini is strict about stdout: it must be the final JSON and nothing else. The
# banner is therefore emitted as JSON, and repeated on stderr so it is visible in
# the hook log even if the CLI ignores the context key for this event.

set -u

# The script lives at <workspace>/.gemini/hooks/scripts/, so three levels up is
# the workspace root. Gemini runs hook commands from the workspace root.
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

# Repeat on stderr: guaranteed visible in the hook log.
printf '%s\n' "$BANNER" >&2
printf '%s' "$BANNER" | python3 -c 'import json, sys
text = sys.stdin.read()
print(json.dumps({"systemMessage": text, "hookSpecificOutput": {"additionalContext": text}}))'
exit 0
