---
description: Cross-vendor parity check - body-aware skill sync status across all runtime layouts, plus MCP single-source coverage. Reports drift; read-only.
---

Check parity between the six vendor runtime layouts under `runtimes/` - `.claude`,
`.codex`, `.gemini`, `.kiro`, `.cursor`, and `.devin`. Devin Desktop is one
vendor identity; Cascade compatibility paths are not a seventh runtime. Skills
share a portable body while preserving vendor-native frontmatter. Agents and
commands are vendor-shaped and maintained per vendor. Drift is sometimes
intentional but should be explicit, not accidental.

```bash
echo "── skills parity (body-aware, all vendors) ──"
if [ -f tools/sync-skills.py ]; then
  python3 tools/sync-skills.py        # read-only report; Claude is the default source of truth
else
  echo "  (tools/sync-skills.py missing - skipping)"
fi

echo
echo "── agents: not cross-synced ──"
echo "  Agent formats diverge by vendor: flat Markdown + frontmatter for Claude/Gemini/Kiro/Cursor,"
echo "  TOML (agents/<name>.toml) for Codex, per-profile agents/<name>/AGENT.md for Devin Local."
echo "  Required fields also differ per vendor, so there is no cross-vendor agent parity"
echo "  to enforce - maintain each independently."
for d in claude codex gemini kiro cursor devin; do
  if [ -d "runtimes/.$d/agents" ]; then
    echo "    .$d/agents: $(find "runtimes/.$d/agents" -type f \( -name '*.md' -o -name '*.toml' \) ! -name 'README.md' | wc -l | tr -d ' ') agent file(s)"
  else
    echo "    .$d/agents: (none)"
  fi
done

echo
echo "── .agents/ vendor-neutral root vs .claude/skills ──"
# .agents/skills is a LIVE runtime directly verified here for Codex.
# It mirrors .claude/skills - the implementation skills - NOT runtimes/.claude/skills,
# which holds the consumer examples. sync-skills.py deliberately does not cover it.
if [ -d .agents/skills ]; then
  a=$(ls -d .claude/skills/*/ 2>/dev/null | xargs -n1 basename | sort)
  b=$(ls -d .agents/skills/*/ 2>/dev/null | xargs -n1 basename | sort)
  if [ "$a" = "$b" ]; then
    echo "  ✓ same skill set ($(echo "$a" | wc -l | tr -d ' ') skills)"
  else
    echo "  ✗ skill sets differ:"
    diff <(echo "$a") <(echo "$b") | sed 's/^/      /'
  fi
  # Bodies must match; frontmatter is expected to differ. Split only the first
  # frontmatter block - later `---` horizontal rules are body content.
  skill_body() {
    python3 - "$1" <<'PY'
from pathlib import Path
import sys
text = Path(sys.argv[1]).read_text(encoding="utf-8")
if text.startswith("---\n") and "\n---\n" in text[4:]:
    print(text.split("\n---\n", 1)[1], end="")
else:
    print(text, end="")
PY
  }
  drift=0
  for d in .claude/skills/*/; do
    s=$(basename "$d"); f1="$d/SKILL.md"; f2=".agents/skills/$s/SKILL.md"
    [ -f "$f1" ] && [ -f "$f2" ] || continue
    if ! diff -q <(skill_body "$f1") <(skill_body "$f2") >/dev/null; then
      echo "  ✗ body drift: $s"; drift=1
    fi
  done
  [ $drift -eq 0 ] && echo "  ✓ bodies identical (frontmatter differs by design)"
else
  echo "  ✗ .agents/skills missing - Codex and other non-Claude CLIs will find no skills in this repo"
fi

echo
echo "── MCP single-source coverage ──"
if [ -f "runtimes/mcp/servers.yaml" ]; then
  echo "Source of truth: runtimes/mcp/servers.yaml"
  for vendor_config in \
    runtimes/.claude/mcp.template.json \
    runtimes/.codex/config.template.toml \
    runtimes/.gemini/settings.template.json \
    runtimes/.kiro/settings/mcp.template.json \
    runtimes/.cursor/mcp.template.json \
    runtimes/.devin/config.template.json; do
    if [ -f "$vendor_config" ]; then
      echo "  ✓ $vendor_config exists (re-run its renderer to verify drift vs servers.yaml)"
    else
      echo "  ✗ $vendor_config missing"
    fi
  done
  echo
  echo "  renderers:"
  for v in claude codex gemini kiro cursor devin; do
    if [ -f "runtimes/mcp/render/render_$v.py" ]; then
      echo "    ✓ render_$v.py"
    else
      echo "    ✗ render_$v.py missing"
    fi
  done
  echo
  echo "  note: Devin Local installs the rendered project config at \`.devin/config.json\`."
  echo "  Cascade's user-level compatibility config is a separate product surface, not another renderer."
else
  echo "  (runtimes/mcp/servers.yaml missing - single source not yet established)"
fi
```

After running:

- **Skills:** if the report shows drift, re-run `tools/sync-skills.py --apply` to sync bodies (it preserves each vendor's frontmatter), or document intentional drift in the relevant `runtimes/README.md`.
- **MCP:** re-run the per-vendor renderer (`runtimes/mcp/render/render_<vendor>.py`) and diff against the committed template to confirm they match `servers.yaml`. Devin's template is `runtimes/.devin/config.template.json`, installed as `.devin/config.json`. A missing template or renderer is a coverage gap - hand it to `runtime-architect` rather than editing the rendered template by hand.

This command is read-only. To actually sync skills, use `tools/sync-skills.py`; for anything else, invoke `runtime-architect`.
