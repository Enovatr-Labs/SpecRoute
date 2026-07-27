#!/usr/bin/env python3
# /// script
# dependencies = []
# requires-python = ">=3.9"
# ///
"""Render runtimes/mcp/servers.yaml into Gemini CLI's settings.json mcpServers map.

Usage:
    python3 runtimes/mcp/render/render_gemini.py > runtimes/.gemini/settings.template.json
    uv run runtimes/mcp/render/render_gemini.py > runtimes/.gemini/settings.template.json

Output shape mirrors Claude Desktop's mcpServers (Gemini and Claude use the
same JSON contract for MCP), but produces a Gemini-flavored top-level wrapper.

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
        "_comment": "Gemini CLI MCP server config template. Drop into .gemini/settings.json in your repo. Generated from runtimes/mcp/servers.yaml. Do not edit by hand. Re-run runtimes/mcp/render/render_gemini.py to regenerate.",
        "mcpServers": {},
    }
    for s in servers:
        entry = {
            "command": s["command"],
            "args": list(s.get("args", [])),
        }
        # Gemini's settings.json takes an `env` map like every other JSON vendor,
        # so `requires_env` must not be dropped here. See env_note() in
        # render_claude.py for why it is emitted as a note rather than an `env` map.
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
