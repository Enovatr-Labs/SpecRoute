#!/usr/bin/env bash
#
# sync-hooks-to-settings.sh - merge a hooks.json source of truth into the
# settings.json file that the Claude Code CLI actually reads.
#
# WHY THIS EXISTS
# ---------------
# Claude Code loads hooks from exactly these sources:
#
#   ~/.claude/settings.json          user settings
#   .claude/settings.json            project settings   (tracked)
#   .claude/settings.local.json      local settings     (gitignored)
#   managed policy settings
#   <plugin>/hooks/hooks.json        plugin hooks only
#   skill / agent frontmatter
#
# A bare project-level `.claude/hooks/hooks.json` is NOT on that list - the
# `hooks/hooks.json` filename is only a hook source inside a *plugin*. A repo
# that keeps its hook configuration there and nowhere else ships hooks that
# never fire.
#
# SpecRoute still keeps `hooks.json` as the authoring artifact: it is the
# vendor-neutral shape documented under hooks/, it can carry `_comment`
# annotations that would be noise inside settings.json, and it is what other
# vendors' runtimes mirror. This script closes the gap by copying its `.hooks`
# key into the settings.json the CLI reads. settings.json is the file that
# executes; hooks.json is the file humans edit.
#
# USAGE
# -----
#   tools/sync-hooks-to-settings.sh                 sync every known pair
#   tools/sync-hooks-to-settings.sh --check         report drift, write nothing
#   tools/sync-hooks-to-settings.sh SRC DEST        sync one explicit pair
#   tools/sync-hooks-to-settings.sh --check SRC DEST
#
# Exit codes: 0 = in sync / synced, 1 = failure, 2 = drift found under --check.
#
# The script is idempotent: running it twice produces no second diff.

set -uo pipefail

CHECK_ONLY=0
if [ "${1:-}" = "--check" ]; then
  CHECK_ONLY=1
  shift
fi

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  sed -n '2,40p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is required but was not found on PATH." >&2
  echo "       Install it (macOS: brew install jq / Debian: apt-get install jq)" >&2
  echo "       and re-run, or hand-copy the .hooks key from hooks.json into settings.json." >&2
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)" || exit 1

# Known source -> destination pairs, relative to the repo root.
PAIRS=(
  ".claude/hooks/hooks.json::.claude/settings.json"
  "runtimes/.claude/hooks/hooks.template.json::runtimes/.claude/settings.template.json"
  "examples/sample-project/.claude/hooks/hooks.json::examples/sample-project/.claude/settings.json"
)

if [ "$#" -eq 2 ]; then
  PAIRS=("$1::$2")
elif [ "$#" -ne 0 ]; then
  echo "error: expected 0 or 2 path arguments, got $#. Run with --help." >&2
  exit 1
fi

FAILED=0
DRIFTED=0
CHANGED=0

sync_pair() {
  local src="$1" dest="$2"
  local src_abs dest_abs tmp mode

  case "$src" in /*) src_abs="$src" ;; *) src_abs="$REPO_ROOT/$src" ;; esac
  case "$dest" in /*) dest_abs="$dest" ;; *) dest_abs="$REPO_ROOT/$dest" ;; esac

  echo "── $src -> $dest"

  if [ ! -f "$src_abs" ]; then
    echo "   FAIL: source not found: $src_abs" >&2
    FAILED=1
    return
  fi
  if [ ! -f "$dest_abs" ]; then
    echo "   FAIL: destination not found: $dest_abs" >&2
    echo "         Create it first - this script merges into an existing settings file," >&2
    echo "         it does not invent permissions/model/env for you." >&2
    FAILED=1
    return
  fi

  # Validate BOTH ends before touching anything. A malformed settings.json
  # silently disables every setting in it, so refuse to overwrite one we
  # cannot parse - the user may have a half-finished edit in flight.
  if ! jq empty "$src_abs" 2>/dev/null; then
    echo "   FAIL: source is not valid JSON: $src" >&2
    jq empty "$src_abs" 2>&1 | sed 's/^/         /' >&2
    FAILED=1
    return
  fi
  if ! jq empty "$dest_abs" 2>/dev/null; then
    echo "   FAIL: destination is not valid JSON - refusing to overwrite: $dest" >&2
    jq empty "$dest_abs" 2>&1 | sed 's/^/         /' >&2
    FAILED=1
    return
  fi

  if [ "$(jq -r 'has("hooks")' "$src_abs")" != "true" ]; then
    echo "   FAIL: source has no top-level \"hooks\" key: $src" >&2
    FAILED=1
    return
  fi

  if ! jq -e '
    (.hooks | type == "object")
    and all(.hooks[];
      type == "array"
      and all(.[];
        type == "object"
        and (.hooks | type == "array")
        and all(.hooks[]; type == "object")
      )
    )
  ' "$src_abs" >/dev/null 2>&1; then
    echo "   FAIL: source hooks do not match the event/matcher/handler schema: $src" >&2
    FAILED=1
    return
  fi

  # Same-directory temporary output makes the final rename atomic.
  tmp="$(mktemp "$dest_abs.tmp.XXXXXX")" || { FAILED=1; return; }

  if ! jq --slurpfile hooksrc "$src_abs" '.hooks = $hooksrc[0].hooks' "$dest_abs" >"$tmp" 2>/dev/null; then
    echo "   FAIL: merge failed for $dest" >&2
    rm -f "$tmp"
    FAILED=1
    return
  fi

  # Never publish output we have not re-validated.
  if ! jq empty "$tmp" 2>/dev/null; then
    echo "   FAIL: merged output is not valid JSON - destination left untouched." >&2
    rm -f "$tmp"
    FAILED=1
    return
  fi

  # Summary: one line per event with its handler count.
  if ! jq -r '
    .hooks
    | to_entries[]
    | "   \(.key): \([.value[].hooks[]] | length) handler(s) across \(.value | length) matcher(s)"
  ' "$tmp"; then
    echo "   FAIL: could not summarize merged hooks; destination left untouched." >&2
    rm -f "$tmp"
    FAILED=1
    return
  fi

  if cmp -s "$tmp" "$dest_abs"; then
    echo "   already in sync"
    rm -f "$tmp"
    return
  fi

  if [ "$CHECK_ONLY" -eq 1 ]; then
    echo "   DRIFT: $dest does not match $src (run without --check to fix)"
    rm -f "$tmp"
    DRIFTED=1
    return
  fi

  mode="$(stat -f '%Lp' "$dest_abs" 2>/dev/null || stat -c '%a' "$dest_abs" 2>/dev/null || true)"
  if [ -n "$mode" ] && ! chmod "$mode" "$tmp"; then
    echo "   FAIL: could not preserve permissions for $dest" >&2
    rm -f "$tmp"
    FAILED=1
    return
  fi
  if ! mv -f "$tmp" "$dest_abs"; then
    echo "   FAIL: atomic replacement failed for $dest" >&2
    rm -f "$tmp"
    FAILED=1
    return
  fi
  echo "   updated"
  CHANGED=$((CHANGED + 1))
}

for pair in "${PAIRS[@]}"; do
  sync_pair "${pair%%::*}" "${pair##*::}"
done

echo
if [ "$FAILED" -ne 0 ]; then
  echo "sync-hooks-to-settings: FAILED - see errors above." >&2
  exit 1
fi
if [ "$DRIFTED" -ne 0 ]; then
  echo "sync-hooks-to-settings: drift found. Run without --check to write." >&2
  exit 2
fi
if [ "$CHANGED" -eq 0 ]; then
  echo "sync-hooks-to-settings: OK - everything already in sync."
else
  echo "sync-hooks-to-settings: OK - $CHANGED file(s) updated."
fi
exit 0
