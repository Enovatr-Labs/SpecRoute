---
description: Comprehensive pre-commit audit — sanitization, frontmatter validity, vendor matrix consistency, broken links, TODO health.
---

Run a comprehensive audit. This is the gate before any push or PR.

## 1. Sanitization

Run `/sanitize` first. If it fails, stop and report the failures — do not continue with later checks until sanitization is clean.

## 2. Frontmatter validation

Walk every agent / skill / command file and validate frontmatter:

```bash
echo "── frontmatter check (agents) ──"
for f in .claude/agents/*.md agents/agent-template.md agents/examples/*.md runtimes/.claude/agents/*.md runtimes/.codex/agents/*.md; do
  [ -f "$f" ] || continue
  case "$f" in *README.md) continue ;; esac
  for k in name description model color; do
    grep -q "^$k:" "$f" || echo "  $f: missing $k"
  done
done

echo
echo "── frontmatter check (skills) ──"
for f in skills/skill-template/SKILL.md skills/examples/*/SKILL.md runtimes/.claude/skills/*/SKILL.md runtimes/.codex/skills/*/SKILL.md; do
  [ -f "$f" ] || continue
  for k in name description argument-hint user-invocable allowed-tools; do
    grep -q "^$k:" "$f" || echo "  $f: missing $k"
  done
done

echo
echo "── frontmatter check (Claude commands) ──"
for f in commands/command-template.claude.md commands/examples/*.claude.md runtimes/.claude/commands/*.md .claude/commands/*.md; do
  [ -f "$f" ] || continue
  case "$f" in *README.md) continue ;; esac
  grep -q "^description:" "$f" || echo "  $f: missing description"
done
```

## 3. Vendor matrix consistency

The matrix table appears in three places. Confirm they are in sync:

```bash
echo "── vendor matrix references ──"
for f in README.md docs/agent-cli-integrations.md docs/multi-vendor-context-files.md; do
  if [ -f "$f" ]; then
    echo "$f: $(grep -c '^| ' "$f") matrix-row lines"
  else
    echo "$f: missing"
  fi
done
```

Flag any mismatch in the count of `| ...` rows across the three files.

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

TODOs are intentional placeholders. The audit doesn't fail on TODO count — it just reports.

## Final report

Summarize:

- Sanitization: PASS / FAIL
- Frontmatter: N issues across M files
- Vendor matrix: in sync / drift detected
- Links: N broken / clean
- TODOs: N total

Ready-to-publish iff: Sanitization PASS, Frontmatter 0 issues, Vendor matrix in sync, Links 0 broken.
