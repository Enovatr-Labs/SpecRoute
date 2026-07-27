---
description: Check the worked example's Claude and Codex runtime parity - agent roster, MCP inventory, and Claude hook/settings synchronization. Reports drift; read-only.
---

Check only the two live runtimes shipped by this worked example: `.claude/` and
`.codex/`. SpecRoute's six-vendor template matrix lives at the repository root;
this example does not duplicate those runtime layouts.

```bash
echo "── agent roster parity (.claude vs .codex) ──"
claude_agents=$(find .claude/agents -maxdepth 1 -type f -name '*.md' ! -name README.md -exec basename {} .md \; | sort)
codex_agents=$(find .codex/agents -maxdepth 1 -type f -name '*.toml' -exec basename {} .toml \; | sort)
if diff <(printf '%s\n' "$claude_agents") <(printf '%s\n' "$codex_agents"); then
  echo "  ✓ agent rosters match"
else
  echo "  ✗ agent roster drift"
fi

echo
echo "── MCP server-name parity ──"
python3 - <<'PY'
import json
import tomllib
from pathlib import Path

claude = json.loads(Path(".claude/mcp.template.json").read_text(encoding="utf-8"))
codex = tomllib.loads(Path(".codex/config.toml").read_text(encoding="utf-8"))
claude_names = set(claude.get("mcpServers", {}))
codex_names = set(codex.get("mcp_servers", {}))
print("  ✓ MCP server names match" if claude_names == codex_names else
      f"  ✗ MCP drift: Claude-only={sorted(claude_names - codex_names)}, "
      f"Codex-only={sorted(codex_names - claude_names)}")
PY

echo
echo "── Claude hook source vs live settings ──"
python3 - <<'PY'
import json
from pathlib import Path

source = json.loads(Path(".claude/hooks/hooks.json").read_text(encoding="utf-8"))
settings = json.loads(Path(".claude/settings.json").read_text(encoding="utf-8"))
print("  ✓ hooks are synchronized" if source.get("hooks") == settings.get("hooks")
      else "  ✗ hook drift: sync .claude/hooks/hooks.json into .claude/settings.json")
PY
```

After running:

- Agent roster drift means one vendor is missing a role; add the native-shaped
  file rather than copying Markdown into TOML or vice versa.
- MCP drift means the two configs expose different server names. Values may
  remain vendor-specific.
- Hook drift means the annotated source and Claude Code's live settings differ;
  update them together using the upstream SpecRoute sync workflow.

This command is read-only.
