# MCP Integration

<!-- sources: runtimes/mcp/README.md, agentic-docs/cross-vendor-sync.md -->

Model Context Protocol (MCP) server inventory, with a single source of truth and per-vendor renderers. **All six vendors consume MCP configs** — in two emit shapes: a `mcpServers` JSON object for everyone except Codex, which uses `[mcp_servers]` TOML sections.

## The problem

| Vendor | Config shape | Config path |
|---|---|---|
| Claude Code | `mcpServers` JSON object | `.mcp.json` (project) / `~/.claude.json` (user) |
| Codex | `[mcp_servers.<name>]` TOML sections | `.codex/config.toml` |
| Gemini CLI | `mcpServers` JSON object | `.gemini/settings.json` |
| Kiro | `mcpServers` JSON object | `.kiro/settings/mcp.json` |
| Cursor | `mcpServers` JSON object | `.cursor/mcp.json` |
| Devin Desktop | `mcpServers` JSON object | `.devin/config.json` |

> **Note:** `claude_desktop_config.json` is the **Claude Desktop app's** MCP file, not the Claude Code CLI's. The CLI reads `.mcp.json` (project, committed) and `~/.claude.json` (user). Earlier SpecRoute releases pointed at the Desktop file in error.

Maintaining six emitted configurations by hand is the failure mode. They drift; reviewers can't tell which is authoritative.

## The solution

Canonical inventory in **one YAML file**, with six renderers:

```
runtimes/mcp/servers.yaml          single source of truth
runtimes/mcp/render/
├── render_claude.py               renders the Claude Code CLI .mcp.json shape
├── render_codex.py                renders to Codex TOML
├── render_gemini.py               renders to Gemini JSON
├── render_kiro.py                 renders to Kiro JSON
├── render_cursor.py               renders to Cursor JSON
└── render_devin.py                renders Devin Desktop's `.devin/config.json`
```

## Workflow

When adding or modifying an MCP server:

```bash
# 1. Edit the canonical source
$EDITOR runtimes/mcp/servers.yaml

# 2. Re-render the vendor configs you target
python3 runtimes/mcp/render/render_claude.py  > runtimes/.claude/mcp.template.json
python3 runtimes/mcp/render/render_codex.py   > runtimes/.codex/config.template.toml
python3 runtimes/mcp/render/render_gemini.py  > runtimes/.gemini/settings.template.json
python3 runtimes/mcp/render/render_kiro.py    > runtimes/.kiro/settings/mcp.template.json
python3 runtimes/mcp/render/render_cursor.py  > runtimes/.cursor/mcp.template.json
python3 runtimes/mcp/render/render_devin.py   > runtimes/.devin/config.template.json

# 3. Commit the canonical source + rendered outputs in one commit
git add runtimes/mcp/servers.yaml runtimes/.*/mcp*.json runtimes/.codex/config.template.toml \
        runtimes/.gemini/settings.template.json runtimes/.devin/config.template.json
git commit -m "mcp: add <server-name>"
```

The commit shape — single YAML edit + rendered outputs — makes the impact reviewable in one diff. Apart from Codex's TOML, every vendor uses the same `mcpServers` JSON object.

## `servers.yaml` shape

```yaml
servers:
  - name: <server-name>
    description: <what this server exposes>
    command: <executable>
    args:
      - <arg1>
      - <arg2>
    requires_env:
      - <CREDENTIAL_ENV_VAR>
    codex_tool_approvals:
      <tool_name>: approve
```

Those six keys are the whole schema — `name`, `description`, `command`, `args`,
`requires_env`, and `codex_tool_approvals`. There is no `env`, `enabled_for`, or
`notes` key; the renderers do not read them.

| Field | Meaning |
|---|---|
| `name` | Key used in the rendered config. |
| `description` | Documentation only; never emitted as behaviour. |
| `command` / `args` | The server launch command. |
| `requires_env` | Credential **names** a consumer must supply. Never a value. |
| `codex_tool_approvals` | Codex-only per-tool approval metadata; other renderers ignore it. |

Each renderer reads the same source and emits the vendor-specific shape. **Every
renderer emits every server** — there is no per-vendor filtering in `servers.yaml`.
If a vendor should not receive a server, leave it out of the inventory or remove it
from that vendor's installed config by hand after rendering.

Renderers never inline credential values. Most turn `requires_env` into a comment so
the requirement stays visible without committing a secret; the Devin renderer uses
Devin Local's `${env:VAR}` substitution in the server's `env` map, so its output
contains only references to shell environment variables.

Devin Desktop's Cascade agent still reads the user-level compatibility path
`~/.codeium/windsurf/mcp_config.json`. It accepts the same `mcpServers` object
as the Devin renderer, so this compatibility destination does not create a
separate vendor or renderer.

## What MCP gives you

MCP servers expose tools and resources to agent CLIs over a JSON-RPC protocol. Common server categories:

- **`filesystem`** — file read/write/list within a scoped directory.
- **`git`** — repository operations.
- **`fetch`** — HTTP requests.
- **Vendor-specific or custom servers** — your project's bespoke tools, ranging from internal API access to specialized analyzers.

## Protocol revisions and transports

MCP revision **2026-07-28** made the protocol core stateless (the
`initialize` / `initialized` exchange and the `Mcp-Session-Id` header were removed)
and deprecated the HTTP+SSE transport in favour of streamable HTTP, under a formal
deprecation policy with a **12-month minimum** removal window. See the
[release announcement](https://blog.modelcontextprotocol.io/posts/2026-07-28/) and the
[specification](https://modelcontextprotocol.io/specification/2026-07-28).

**This changes nothing SpecRoute renders.** `servers.yaml` and all six renderers emit
**stdio** servers only — a `command` plus `args`, with no transport, URL, session, or
header field anywhere in the schema or in any rendered template. Transport and session
changes in the protocol therefore affect no rendered config.

It matters the moment you add a **remote** server: use streamable HTTP, not HTTP+SSE.
The per-vendor config key for a remote server is the vendor's own, not MCP's — check
that vendor's documentation rather than assuming the stdio shape extends to it.

The same revision also introduced an **extensions** framework, under which optional
capabilities such as Tasks, MCP Apps, and Skills over MCP are negotiated per
connection rather than being part of the core protocol.

## Security defaults

Insecure defaults in MCP server configs are a security issue. See [[Security]]. Specifically:

- **Pin versions** in `runtimes/mcp/servers.yaml` — `@latest` invites supply-chain surprises.
- **Default to least privilege** — `filesystem` server scoped to the project root, not `/`.
- **Review what each server can do** before enabling.

## Cross-vendor parity

`/parity` checks that the rendered per-vendor files match what `servers.yaml` would produce. Drift means someone hand-edited a rendered file — the canonical file should be edited and re-rendered instead.

## Adding a new vendor that consumes MCP

When adding a new vendor with MCP support (see [[Adding a Vendor]]):

1. Document the vendor's MCP config shape and path.
2. Add a `render_<vendor>.py` renderer under `runtimes/mcp/render/`.
3. Confirm the renderer preserves `requires_env` — no renderer may drop a credential requirement silently.
4. Document the new render command in `runtimes/mcp/README.md` and `agentic-docs/agent-cli-integrations.md`.

## Owner agent

MCP infrastructure is owned by the `runtime-architect` agent.

## See also

- [[Cross-Vendor Sync]] — `sync-skills.py` and the MCP renderers together
- [[Agent CLI Integrations]] — per-vendor wiring including MCP config paths
- [[Vendor Matrix]] — which vendors support MCP
- [[Security]] — hardening MCP configurations
