#!/usr/bin/env python3
"""Render runtimes/mcp/servers.yaml into Kiro's .kiro/settings/mcp.json shape.

Usage:
    python3 runtimes/mcp/render/render_kiro.py > runtimes/.kiro/settings/mcp.template.json

Kiro uses the same `mcpServers` JSON shape as Claude and Gemini (workspace config
at .kiro/settings/mcp.json, user config at ~/.kiro/settings/mcp.json).

Reads YAML from runtimes/mcp/servers.yaml. Writes JSON to stdout. Does not modify any files.
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
    out = {
        "_comment": "Generated from runtimes/mcp/servers.yaml. Do not edit by hand. Re-run runtimes/mcp/render/render_kiro.py to regenerate. Install to .kiro/settings/mcp.json (workspace) or ~/.kiro/settings/mcp.json (user).",
        "mcpServers": {},
    }
    for s in servers:
        entry = {
            "command": s["command"],
            "args": list(s.get("args", [])),
        }
        if s.get("requires_env"):
            entry["env"] = {
                "_comment": f"Set the following in your shell or .env: {', '.join(s['requires_env'])}"
            }
        out["mcpServers"][s["name"]] = entry
    return out


def main() -> int:
    text = SERVERS_YAML.read_text(encoding="utf-8")
    parsed = parse_yaml_minimal(text)
    rendered = render(parsed["servers"])
    json.dump(rendered, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
