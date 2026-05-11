# MCP Integration

<!-- sources: runtimes/mcp/README.md, agentic-docs/cross-vendor-sync.md -->

Model Context Protocol (MCP) server inventory, with a single source of truth and per-vendor renderers. Three vendors (Claude Desktop, Codex, Gemini CLI) consume MCP configs — in three different shapes.

## The problem

| Vendor | Config shape | Config path |
|---|---|---|
| Claude Desktop | `mcpServers` JSON object | `.claude/claude_desktop_config.json` |
| Codex | `[mcp_servers.<name>]` TOML sections | `.codex/config.toml` |
| Gemini CLI | `mcpServers` JSON object | `.gemini/settings.json` |

Maintaining three files by hand is the failure mode. They drift; reviewers can't tell which is authoritative.

## The solution

Canonical inventory in **one YAML file**:

```
runtimes/mcp/servers.yaml          single source of truth
runtimes/mcp/render/
├── render_claude.py               renders to Claude Desktop JSON
├── render_codex.py                renders to Codex TOML
└── render_gemini.py               renders to Gemini JSON
```

## Workflow

When adding or modifying an MCP server:

```bash
# 1. Edit the canonical source
$EDITOR runtimes/mcp/servers.yaml

# 2. Re-render all three vendor configs
python3 runtimes/mcp/render/render_claude.py > runtimes/.claude/claude_desktop_config.template.json
python3 runtimes/mcp/render/render_codex.py  > runtimes/.codex/config.template.toml
python3 runtimes/mcp/render/render_gemini.py > runtimes/.gemini/settings.template.json

# 3. Commit all four files in one commit
git add runtimes/mcp/servers.yaml \
        runtimes/.claude/claude_desktop_config.template.json \
        runtimes/.codex/config.template.toml \
        runtimes/.gemini/settings.template.json
git commit -m "mcp: add <server-name>"
```

The commit shape — single YAML edit + three rendered outputs — makes the impact reviewable in one diff.

## `servers.yaml` shape

```yaml
servers:
  - name: <server-name>
    command: <executable>
    args:
      - <arg1>
      - <arg2>
    env:
      KEY: value
    enabled_for:
      - claude
      - codex
      - gemini
    notes: |
      <optional contextual notes>
```

Each renderer reads the same source and emits the vendor-specific shape. Renderers ignore servers whose `enabled_for` list excludes them.

## What MCP gives you

MCP servers expose tools and resources to agent CLIs over a JSON-RPC protocol. Common server categories:

- **`filesystem`** — file read/write/list within a scoped directory.
- **`git`** — repository operations.
- **`fetch`** — HTTP requests.
- **Vendor-specific or custom servers** — your project's bespoke tools, ranging from internal API access to specialized analyzers.

## Security defaults

Insecure defaults in MCP server configs are a security issue. See [[Security]]. Specifically:

- **Pin versions** in `runtimes/mcp/servers.yaml` — `@latest` invites supply-chain surprises.
- **Default to least privilege** — `filesystem` server scoped to the project root, not `/`.
- **Review what each server can do** before enabling.

## Cross-vendor parity

`/parity` checks that the three rendered files match what `servers.yaml` would produce. Drift means someone hand-edited a rendered file — the canonical file should be edited and re-rendered instead.

## Adding a new vendor that consumes MCP

When adding a new vendor with MCP support (see [[Adding a Vendor]]):

1. Document the vendor's MCP config shape and path.
2. Add a `render_<vendor>.py` renderer under `runtimes/mcp/render/`.
3. Update `servers.yaml` per-server `enabled_for` lists.
4. Document the new render command in `runtimes/mcp/README.md` and `agentic-docs/agent-cli-integrations.md`.

## Owner agent

MCP infrastructure is owned by the `runtime-architect` agent.

## See also

- [[Cross-Vendor Sync]] — `sync-skills.py` and the MCP renderers together
- [[Agent CLI Integrations]] — per-vendor wiring including MCP config paths
- [[Vendor Matrix]] — which vendors support MCP
- [[Security]] — hardening MCP configurations
