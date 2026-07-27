#!/usr/bin/env python3
# /// script
# dependencies = []
# requires-python = ">=3.9"
# ///
"""Render runtimes/mcp/servers.yaml into the Claude Code CLI's .mcp.json shape.

Usage:
    python3 runtimes/mcp/render/render_claude.py > runtimes/.claude/mcp.template.json
    uv run runtimes/mcp/render/render_claude.py > runtimes/.claude/mcp.template.json

The Claude Code CLI reads MCP servers from `.mcp.json` (project scope, committed)
and `~/.claude.json` (user scope). This is NOT the Claude Desktop app's
`claude_desktop_config.json` - the two are different files for different products,
though they share the same `mcpServers` JSON shape.

This module is also the shared library for the sibling renderers: they import
`parse_yaml_minimal` and `env_note` from here rather than duplicating them.

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


def env_note(server: dict) -> str | None:
    """Return a note naming a server's required env vars, or None if it needs none.

    Every supported vendor's MCP config has an `env` map, but these are *tracked
    templates*: inlining values would commit secrets, and the `${VAR}` expansion
    syntax that would avoid that is not portable across all six runtimes; a
    placeholder may be handed to the server verbatim instead of expanded.

    So renderers without a documented expansion form surface `requires_env` as
    a comment rather than a synthetic `env` entry - a `_comment` key nested
    *inside* `env` (the previous shape) would reach the server process as an
    environment variable literally named `_comment`. Devin Local is the
    exception: its renderer emits the documented `${env:VAR}` substitution.
    No renderer may drop `requires_env` silently.
    """
    required = server.get("requires_env")
    if not required:
        return None
    return (
        "Requires these environment variables, exported in your shell or a "
        f"gitignored .env: {', '.join(required)}"
    )


def render(servers: list[dict]) -> dict:
    out = {
        "_comment": "Generated from runtimes/mcp/servers.yaml. Do not edit by hand. Re-run runtimes/mcp/render/render_claude.py to regenerate. Install to .mcp.json (project, committed) or ~/.claude.json (user) for the Claude Code CLI.",
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
