---
description: Cross-vendor parity check - body-aware skill sync status across all runtime layouts, plus MCP single-source coverage. Reports drift; read-only.
---

Check parity between vendor runtime layouts. Skills share a portable body across all six vendors (each carries its own frontmatter); agents and commands are vendor-shaped and maintained per vendor. Drift is sometimes intentional but should be explicit, not accidental.

```bash
echo "── skills parity (body-aware, all vendors) ──"
if [ -f tools/sync-skills.py ]; then
  python3 tools/sync-skills.py        # read-only report; Claude is the default source of truth
else
  echo "  (tools/sync-skills.py missing - skipping)"
fi

echo
echo "── agents: not cross-synced ──"
echo "  Agent formats diverge by vendor (Claude/Gemini/Kiro/Cursor flat Markdown, Codex .toml,"
echo "  Devin per-profile AGENT.md). There is no cross-vendor agent parity - maintain each independently."

echo
echo "── MCP single-source coverage ──"
if [ -f "runtimes/mcp/servers.yaml" ]; then
  echo "Source of truth: runtimes/mcp/servers.yaml"
  for vendor_config in \
    runtimes/.claude/mcp.template.json \
    runtimes/.codex/config.template.toml \
    runtimes/.gemini/settings.template.json \
    runtimes/.kiro/settings/mcp.template.json \
    runtimes/.cursor/mcp.template.json; do
    if [ -f "$vendor_config" ]; then
      echo "  ✓ $vendor_config exists (re-run its renderer to verify drift vs servers.yaml)"
    else
      echo "  ✗ $vendor_config missing"
    fi
  done
  echo "  note: Windsurf/Devin MCP is user-level (~/.codeium/windsurf/mcp_config.json) - no committed template"
else
  echo "  (runtimes/mcp/servers.yaml missing - single source not yet established)"
fi
```

After running:

- **Skills:** if the report shows drift, re-run `tools/sync-skills.py --apply` to sync bodies (it preserves each vendor's frontmatter), or document intentional drift in the relevant `runtimes/README.md`.
- **MCP:** re-run the per-vendor renderer (`runtimes/mcp/render/render_<vendor>.py`) and diff against the committed template to confirm they match `servers.yaml`.

This command is read-only. To actually sync skills, use `tools/sync-skills.py`; for anything else, invoke `runtime-architect`.
