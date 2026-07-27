#!/usr/bin/env python3
# /// script
# dependencies = []
# requires-python = ">=3.9"
# ///
"""Render runtimes/mcp/servers.yaml into Cursor's .cursor/mcp.json shape.

Usage:
    python3 runtimes/mcp/render/render_cursor.py > runtimes/.cursor/mcp.template.json
    uv run runtimes/mcp/render/render_cursor.py > runtimes/.cursor/mcp.template.json

Cursor uses the same `mcpServers` JSON shape as Claude Desktop, so this renderer
imports the Claude renderer's parsing helpers and only differs in the
regeneration comment.

Reads YAML from runtimes/mcp/servers.yaml. Writes JSON to stdout. Does not modify any files.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_claude import env_note, parse_yaml_minimal  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[3]
SERVERS_YAML = REPO_ROOT / "runtimes" / "mcp" / "servers.yaml"


def render(servers: list[dict]) -> dict:
    out = {
        "_comment": "Generated from runtimes/mcp/servers.yaml. Do not edit by hand. Re-run runtimes/mcp/render/render_cursor.py to regenerate.",
        "mcpServers": {},
    }
    for s in servers:
        entry = {
            "command": s["command"],
            "args": list(s.get("args", [])),
        }
        note = env_note(s)
        if note:
            entry["_comment"] = note
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
