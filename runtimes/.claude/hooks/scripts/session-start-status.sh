#!/usr/bin/env bash
# SessionStart hook: prints a compact project status banner.
# Exit 0 always; this hook is informational.

set -u

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$REPO_ROOT" || exit 0

echo "-- project status --------------------------------------------------"

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

echo "Present dirs (${#PRESENT[@]}/${#EXPECTED_DIRS[@]}): ${PRESENT[*]:-none}"
echo "Missing dirs (${#MISSING[@]}/${#EXPECTED_DIRS[@]}): ${MISSING[*]:-none}"

if [ -f "AGENTS.md" ]; then
  echo "Root context: AGENTS.md"
fi

echo "--------------------------------------------------------------------"
exit 0
