#!/usr/bin/env python3
"""Render runtimes/mcp/servers.yaml into Codex's config.toml [mcp_servers] sections.

Usage:
    python3 runtimes/mcp/render/render_codex.py > runtimes/.codex/config.template.toml

Emits a complete config.toml including the SpecForge-default approval policy
header followed by [mcp_servers.<name>] sections derived from servers.yaml.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Reuse the YAML parser from the Claude renderer.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_claude import parse_yaml_minimal  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[3]
SERVERS_YAML = REPO_ROOT / "runtimes" / "mcp" / "servers.yaml"


HEADER = """\
# Codex configuration. Generated from runtimes/mcp/servers.yaml.
# Do not edit by hand. Re-run runtimes/mcp/render/render_codex.py to regenerate.

approval_policy = "on-request"
sandbox_mode = "workspace-write"
"""


def render(servers: list[dict]) -> str:
    parts = [HEADER, ""]
    for s in servers:
        name = s["name"]
        parts.append(f"[mcp_servers.{name}]")
        parts.append(f'command = "{s["command"]}"')
        args = s.get("args", [])
        rendered_args = ", ".join(_quote(a) for a in args)
        parts.append(f"args = [{rendered_args}]")
        for tool, mode in (s.get("codex_tool_approvals") or {}).items():
            parts.append("")
            parts.append(f"[mcp_servers.{name}.tools.{tool}]")
            parts.append(f'approval_mode = "{mode}"')
        parts.append("")
    return "\n".join(parts)


def _quote(value) -> str:
    s = str(value).replace('"', '\\"')
    return f'"{s}"'


def main() -> int:
    text = SERVERS_YAML.read_text(encoding="utf-8")
    parsed = parse_yaml_minimal(text)
    sys.stdout.write(render(parsed["servers"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
