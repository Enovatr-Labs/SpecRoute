#!/usr/bin/env bash
# Manually publish wiki/ to the GitHub wiki repo.
#
# Mirrors what .github/workflows/sync-wiki.yml does on every push to main,
# but runs locally. Use this for:
#   - The very first publish (before the wiki repo exists, see prerequisite below).
#   - Pushing wiki changes from a branch you don't intend to merge yet.
#   - Recovering from a failed CI run.
#
# Prerequisite: the wiki must already exist on GitHub. If you've never created
# a wiki page, visit https://github.com/<owner>/<repo>/wiki and create the Home
# page once via the UI. Only after that does <repo>.wiki.git exist to clone.
#
# Usage:
#   ./scripts/sync-wiki.sh                          # uses default remote
#   REMOTE_OVERRIDE=git@github.com:owner/repo.wiki.git ./scripts/sync-wiki.sh
#
# Requires: git, rsync, write access to the wiki repo.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WIKI_SRC="${REPO_ROOT}/wiki"

if [[ ! -d "${WIKI_SRC}" ]]; then
  echo "error: ${WIKI_SRC} does not exist" >&2
  exit 1
fi

# Derive the wiki remote from the current `origin` if not overridden.
if [[ -n "${REMOTE_OVERRIDE:-}" ]]; then
  WIKI_REMOTE="${REMOTE_OVERRIDE}"
else
  ORIGIN="$(git -C "${REPO_ROOT}" remote get-url origin)"
  # Convert e.g. git@github.com:Enovatr-Labs/SpecForge.git → ...SpecForge.wiki.git
  # or       https://github.com/Enovatr-Labs/SpecForge.git → ...SpecForge.wiki.git
  WIKI_REMOTE="${ORIGIN%.git}.wiki.git"
fi

CLONE_DIR="$(mktemp -d -t specforge-wiki.XXXXXX)"
trap 'rm -rf "${CLONE_DIR}"' EXIT

echo "→ Cloning ${WIKI_REMOTE}"
git clone "${WIKI_REMOTE}" "${CLONE_DIR}"

echo "→ Syncing wiki/ → wiki repo"
rsync -av --delete \
  --exclude='.git' \
  --exclude='README.md' \
  "${WIKI_SRC}/" "${CLONE_DIR}/"

cd "${CLONE_DIR}"
git add -A

if git diff --cached --quiet; then
  echo "→ No changes to push."
  exit 0
fi

SHA="$(git -C "${REPO_ROOT}" rev-parse HEAD)"
git commit -m "Sync wiki from $(basename "${REPO_ROOT}")@${SHA}"

echo "→ Pushing"
git push origin HEAD

echo "✓ Wiki published."
