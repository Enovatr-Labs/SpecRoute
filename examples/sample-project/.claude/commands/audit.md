---
description: Comprehensive pre-commit audit - sanitization, frontmatter validity, vendor matrix consistency, broken links, TODO health.
---

Run a comprehensive audit. This is the gate before any push or PR.

## 1. Sanitization

Run `/sanitize` first. If it fails, stop and report the failures - do not continue with later checks until sanitization is clean.

## 2. Frontmatter validation

This project ships two runtimes - `.claude/` (Markdown) and `.codex/` (TOML) - and their frontmatter contracts differ. Validate each against its own contract; do not hold Codex agents to Claude's `model` / `color` fields.

```bash
echo "── frontmatter check (Claude agents) ──"
for f in .claude/agents/*.md; do
  [ -f "$f" ] || continue
  case "$f" in *README.md) continue ;; esac
  for k in name description model color; do
    grep -q "^$k:" "$f" || echo "  ERROR $f: missing $k"
  done
done

echo
echo "── frontmatter check (Codex agents) ──"
# Codex agents are TOML, not Markdown - keys are `name = "..."`, not `name:`.
for f in .codex/agents/*.toml; do
  [ -f "$f" ] || continue
  for k in name description developer_instructions; do
    grep -qE "^$k *=" "$f" || echo "  ERROR $f: missing $k"
  done
done

echo
echo "── frontmatter check (skills) ──"
# name + description are the Agent Skills open-standard required pair.
# argument-hint / user-invocable / allowed-tools are Claude/Codex vendor
# extensions - warnings only. Contract: SpecRoute wiki, "Frontmatter Contracts".
# This project ships no skills today - use find so the check stays quiet
# instead of erroring on an unmatched glob.
skill_files=$(find .claude/skills .codex/skills -name SKILL.md 2>/dev/null)
if [ -z "$skill_files" ]; then
  echo "  (no skills in this project - nothing to check)"
else
  for f in $skill_files; do
    for k in name description; do
      grep -q "^$k:" "$f" || echo "  ERROR $f: missing $k"
    done
    for k in argument-hint user-invocable allowed-tools; do
      grep -q "^$k:" "$f" || echo "  WARN  $f: missing $k (Claude/Codex vendor extension)"
    done
  done
fi

echo
echo "── frontmatter check (Claude commands) ──"
for f in .claude/commands/*.md; do
  [ -f "$f" ] || continue
  case "$f" in *README.md) continue ;; esac
  grep -q "^description:" "$f" || echo "  ERROR $f: missing description"
done
```

## 3. Cross-runtime agent parity

This project has no vendor matrix table (that lives upstream in SpecRoute). The equivalent consistency check here is that the `.claude/` and `.codex/` runtimes carry the same agent roster, and that `agent-roster.md` documents it:

```bash
echo "── agent roster parity (.claude vs .codex) ──"
claude_agents=$(find .claude/agents -name '*.md' ! -name 'README.md' -exec basename {} .md \; | sort)
codex_agents=$(find .codex/agents -name '*.toml' -exec basename {} .toml \; | sort)
echo "  .claude/agents: $(echo "$claude_agents" | wc -l | tr -d ' ') agents"
echo "  .codex/agents:  $(echo "$codex_agents" | wc -l | tr -d ' ') agents"
diff <(echo "$claude_agents") <(echo "$codex_agents") \
  && echo "  ✓ rosters match" \
  || echo "  ✗ DRIFT: '<' = Claude-only, '>' = Codex-only"

echo
echo "── roster documentation ──"
for a in $claude_agents; do
  grep -q "\`$a\`" agent-roster.md || echo "  ✗ $a not listed in agent-roster.md"
done
```

Note the two runtimes intentionally do **not** cross-sync file bodies (Markdown vs TOML) - only the roster of agent names must match.

## 4. Broken markdown links

```bash
echo "── broken local links ──"
git grep -nE "\]\(([^)]+)\)" -- '*.md' 2>/dev/null \
  | python3 -c '
import sys, re, os
broken = 0
for line in sys.stdin:
    fp, _, rest = line.partition(":")
    for m in re.finditer(r"\]\(([^)]+)\)", rest):
        target = m.group(1).split("#")[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        candidate = os.path.normpath(os.path.join(os.path.dirname(fp), target))
        if not (os.path.exists(candidate) or os.path.exists(target)):
            print(f"  {fp}: {target}")
            broken += 1
print(f"Total broken links: {broken}")
'
```

## 5. TODO health

```bash
echo "── TODO health ──"
total=$(git grep -c "TODO" 2>/dev/null | awk -F: '{s+=$2} END{print s+0}')
echo "Total TODOs: $total"
echo "Files with TODOs:"
git grep -l "TODO" 2>/dev/null | head -20
```

TODOs are intentional placeholders. The audit doesn't fail on TODO count - it just reports.

## Final report

Summarize:

- Sanitization: PASS / FAIL
- Frontmatter: N `ERROR` / M `WARN` across K files
- Agent roster parity: in sync / drift detected
- Links: N broken / clean
- TODOs: N total

Ready-to-publish iff: Sanitization PASS, Frontmatter 0 `ERROR`, agent rosters in sync, Links 0 broken. `WARN` lines are advisory - they flag missing Claude/Codex vendor extensions, not contract violations.
