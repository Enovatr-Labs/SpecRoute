---
description: Report the current state of the SpecRoute skeleton - which top-level dirs exist, which artifacts have been drafted, what's outstanding.
---

Report the SpecRoute skeleton state at a glance. Run these checks and summarize the output as a status table.

```bash
echo "── top-level directory status ──"
for d in docs prds specs agents skills commands hooks prompts workflows rules runtimes examples tools assets; do
  if [ -d "$d" ]; then
    n=$(find "$d" -type f \( -name "*.md" -o -name "*.json" -o -name "*.toml" -o -name "*.yaml" -o -name "*.yml" -o -name "*.sh" -o -name "*.py" \) 2>/dev/null | wc -l | tr -d ' ')
    echo "  ✓  $d/ ($n files)"
  else
    echo "  ✗  $d/ (missing)"
  fi
done

echo
echo "── runtime layouts ──"
for v in claude codex gemini kiro cursor windsurf; do
  if [ -d "runtimes/.$v" ]; then
    echo "  ✓  runtimes/.$v/"
  else
    echo "  ✗  runtimes/.$v/ (not yet wired)"
  fi
done

echo
echo "── implementation agents ──"
if [ -d ".claude/agents" ]; then
  find .claude/agents -maxdepth 1 -name "*.md" -not -name "README.md" -exec basename {} .md \; | sort
fi

echo
echo "── outstanding TODOs in tracked files ──"
git grep -n "TODO" 2>/dev/null | wc -l | xargs echo "TODO count:"
echo "(top 10):"
git grep -n "TODO" 2>/dev/null | head -10

echo
echo "── git state ──"
git status --short
git log --oneline -5
```

Summarize as:

1. Overall completion: `<built>/<expected>` top-level dirs, `<built>/6` runtime layouts.
2. The 11 implementation agents (note any missing).
3. TODO count and the top items.
4. Git: branch, uncommitted changes, recent commits.

Keep the report under ~30 lines of output. The point is orientation, not exhaustive listing.
