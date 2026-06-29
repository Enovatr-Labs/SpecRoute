#!/usr/bin/env python3
"""Render runtimes/mcp/servers.yaml into Cursor's .cursor/mcp.json shape.

Usage:
    python3 runtimes/mcp/render/render_cursor.py > runtimes/.cursor/mcp.template.json

Cursor uses the same `mcpServers` JSON shape as Claude Desktop, so this renderer
reuses the Claude renderer's logic and only differs in the regeneration comment.

Reads YAML from runtimes/mcp/servers.yaml. Writes JSON to stdout. Does not modify any files.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SERVERS_YAML = REPO_ROOT / "runtimes" / "mcp" / "servers.yaml"


def parse_yaml_minimal(text: str) -> dict:
    """Parse the small subset of YAML used by servers.yaml.

    Avoids requiring PyYAML. The format here is intentionally simple:
    - top-level "servers:" list
    - each item has scalar fields (name, description, command) and list fields (args, requires_env)
    - one nested map (codex_tool_approvals) with scalar values
    """
    servers: list[dict] = []
    current: dict | None = None
    current_list_key: str | None = None
    current_map_key: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if indent == 0 and stripped == "servers:":
            continue

        if indent == 2 and stripped.startswith("- "):
            if current is not None:
                servers.append(current)
            current = {}
            current_list_key = None
            current_map_key = None
            kv = stripped[2:]
            if ":" in kv:
                k, v = kv.split(":", 1)
                current[k.strip()] = _scalar(v.strip())
            continue

        if current is None:
            continue

        if indent == 4 and ":" in stripped:
            key, _, value = stripped.partition(":")
            key, value = key.strip(), value.strip()
            if value == "":
                current_list_key = key
                current_map_key = key
                current[key] = []
            else:
                current[key] = _scalar(value)
                current_list_key = None
                current_map_key = None
            continue

        if indent == 6 and stripped.startswith("- "):
            if current_list_key:
                if isinstance(current[current_list_key], list):
                    current[current_list_key].append(_scalar(stripped[2:].strip()))
            continue

        if indent == 6 and ":" in stripped and current_map_key:
            k, _, v = stripped.partition(":")
            if not isinstance(current[current_map_key], dict):
                current[current_map_key] = {}
            current[current_map_key][k.strip()] = _scalar(v.strip())
            continue

    if current is not None:
        servers.append(current)

    return {"servers": servers}


def _scalar(s: str):
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    if s in {"true", "True"}:
        return True
    if s in {"false", "False"}:
        return False
    return s


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
