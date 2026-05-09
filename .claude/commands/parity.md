---
description: Cross-vendor parity check - diff skills, agents, commands, and hooks between runtimes/.claude/, runtimes/.codex/, and other runtime layouts. Reports drift.
---

Check parity between vendor runtime layouts. Drift is sometimes intentional (a Claude-only skill) but should be explicit, not accidental.

```bash
echo "── skills parity (claude vs codex) ──"
if [ -d "runtimes/.claude/skills" ] && [ -d "runtimes/.codex/skills" ]; then
  claude_skills=$(find runtimes/.claude/skills -maxdepth 1 -mindepth 1 -type d -exec basename {} \; | sort)
  codex_skills=$(find runtimes/.codex/skills -maxdepth 1 -mindepth 1 -type d -exec basename {} \; | sort)
  echo "Claude only:"
  comm -23 <(echo "$claude_skills") <(echo "$codex_skills") | sed 's/^/  /'
  echo "Codex only:"
  comm -13 <(echo "$claude_skills") <(echo "$codex_skills") | sed 's/^/  /'
  echo "Both:"
  comm -12 <(echo "$claude_skills") <(echo "$codex_skills") | wc -l | xargs echo "  shared count:"
else
  echo "  (one or both runtime skill dirs missing - skipping)"
fi

echo
echo "── agents parity (claude vs codex) ──"
if [ -d "runtimes/.claude/agents" ] && [ -d "runtimes/.codex/agents" ]; then
  claude_agents=$(find runtimes/.claude/agents -maxdepth 1 -name "*.md" -exec basename {} .md \; | grep -v "^README$" | sort)
  codex_agents=$(find runtimes/.codex/agents -maxdepth 1 -name "*.md" -exec basename {} .md \; | grep -v "^README$" | sort)
  echo "Claude only:"
  comm -23 <(echo "$claude_agents") <(echo "$codex_agents") | sed 's/^/  /'
  echo "Codex only:"
  comm -13 <(echo "$claude_agents") <(echo "$codex_agents") | sed 's/^/  /'
fi

echo
echo "── MCP servers parity ──"
if [ -f "runtimes/mcp/servers.yaml" ]; then
  echo "Source of truth: runtimes/mcp/servers.yaml"
  for vendor_config in runtimes/.claude/claude_desktop_config.template.json runtimes/.codex/config.template.toml runtimes/.gemini/settings.template.json; do
    if [ -f "$vendor_config" ]; then
      echo "  ✓ $vendor_config exists (run renderer to verify drift)"
    else
      echo "  ✗ $vendor_config missing"
    fi
  done
else
  echo "  (runtimes/mcp/servers.yaml missing - single source not yet established)"
fi

echo
echo "── frontmatter drift on shared skills ──"
if [ -d "runtimes/.claude/skills" ] && [ -d "runtimes/.codex/skills" ]; then
  for d in runtimes/.claude/skills/*/; do
    name=$(basename "$d")
    other="runtimes/.codex/skills/$name/SKILL.md"
    [ -f "$other" ] || continue
    if ! diff -q "$d/SKILL.md" "$other" >/dev/null 2>&1; then
      echo "  drift: $name"
    fi
  done
fi
```

After running:

- Report each section's findings.
- For "Claude only" / "Codex only" lists: ask whether each is intentional. If yes, document the rationale in the relevant `runtimes/README.md`. If no, invoke `runtime-architect` (or run `tools/sync-skills.py`) to mirror.
- For drift on shared skills: invoke `runtime-architect` to reconcile.

This command is read-only. To actually sync, use `tools/sync-skills.py` or invoke `runtime-architect`.
