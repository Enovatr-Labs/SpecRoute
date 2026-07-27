#!/usr/bin/env python3
# /// script
# dependencies = []
# requires-python = ">=3.9"
# ///
"""Render the canonical MCP inventory for Devin Desktop's Devin Local agent.

Usage:
    python3 runtimes/mcp/render/render_devin.py > runtimes/.devin/config.template.json

Devin Local reads project MCP servers from `.devin/config.json`. Cascade uses
the compatibility user path `~/.codeium/windsurf/mcp_config.json`; the same
`mcpServers` object can be merged there when a project still uses Cascade.

Reads YAML from runtimes/mcp/servers.yaml. Writes JSON to stdout. Does not
modify files.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_claude import parse_yaml_minimal  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[3]
SERVERS_YAML = REPO_ROOT / "runtimes" / "mcp" / "servers.yaml"


def render(servers: list[dict]) -> dict:
    out = {"mcpServers": {}}
    for server in servers:
        entry = {
            "command": server["command"],
            "args": list(server.get("args", [])),
        }
        required = server.get("requires_env", [])
        if required:
            entry["env"] = {name: f"${{env:{name}}}" for name in required}
        out["mcpServers"][server["name"]] = entry
    return out


def main() -> int:
    parsed = parse_yaml_minimal(SERVERS_YAML.read_text(encoding="utf-8"))
    json.dump(render(parsed["servers"]), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
