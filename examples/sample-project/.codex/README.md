# `.codex/` - Codex runtime for the user-search sample project

This is the **Codex drop-in** for the same user-search worked example that ships under [`.claude/`](../.claude/). It demonstrates the mid-2026 vendor convergence end-to-end: the identical implementation team and project artifacts, expressed in a second vendor's native shape. The spec triplet, PRDs, ADRs, prompts, and roster are vendor-neutral and shared - only the runtime layer differs.

Drop this directory into the root of your project alongside (or instead of) `.claude/`. Codex reads from these paths automatically.

## Layout

```
.codex/
├── config.toml              MCP servers + approval policy
└── agents/<name>.toml        9 standalone TOML subagents (the user-search team)
```

The 9 agents mirror the `.claude/agents/` roster one-for-one:
`prd-author`, `spec-author`, `backend-engineer`, `frontend-engineer`, `database-engineer`,
`security-auditor`, `unit-test-writer`, `integration-test-generator`, `deployment-validator`.

## TOML agent shape

Codex agents are standalone TOML files, **not** the flat Markdown shape Claude uses. Required fields:

| Field | Purpose |
|---|---|
| `name` | Stable agent id (matches the Claude agent name). |
| `description` | One-line role summary plus trigger phrases (carried verbatim from the Claude agent). |
| `developer_instructions` | Triple-quoted string holding the agent's full body: owns, operating principles, checklists, "Don't use for". |

Claude-only fields are dropped: there is no `color`, and the Claude `model: opus | sonnet` does not carry across (Codex uses different model ids). Each file leaves `model` out, with a commented `# model = "gpt-5-codex"` line you can uncomment to pin a model; otherwise the agent inherits the parent session.

Codex has **no per-agent memory directory**, so where the Claude agents declared `memory: project` each TOML body has a short "Persistent state" note: surface persistent context through the agent definition and the tracked project artifacts (spec triplet, task checkboxes, PR notes) rather than a separate memory store.

## MCP in config.toml

`config.toml` carries the MCP server inventory under `[mcp_servers.<name>]` blocks - the same five servers as this project's [`.claude/mcp.template.json`](../.claude/mcp.template.json): `filesystem`, `github`, `memory`, `sequential-thinking`, `playwright`. Keep the two in sync. In the SpecRoute framework these render from `runtimes/mcp/servers.yaml` via `runtimes/mcp/render/render_codex.py`. Secrets (e.g. `GITHUB_PERSONAL_ACCESS_TOKEN`) belong in environment variables or a gitignored `.env`, never inline.

`approval_policy` and `sandbox_mode` set the team's risk posture; adjust for your environment.

## Hooks and skills

Hooks and skills remain vendor-shaped. This sample deliberately uses **no skills**
(the work is task-driven; see [`../agentic-docs/agentic-coding-model.md`](../agentic-docs/agentic-coding-model.md)).
Codex exposes 11 hook events and command handlers. For skills, keep the portable
`name` and `description` baseline and scaffold any additional fields from current
Codex documentation before syncing bodies with `tools/sync-skills.py`.

## No agent cross-sync with `.claude/`

Agents do **not** cross-sync between `.claude/` and `.codex/`. The formats diverge - Claude agents are Markdown with YAML frontmatter, Codex agents are TOML with `developer_instructions`. When you change an agent's substance, update both shapes by hand. `tools/sync-skills.py` keeps **skills** in parity across vendors but excludes agents for this reason.

## See also

- [`../README.md`](../README.md) - the example's drop-in instructions (now covers both runtimes)
- [`../AGENTS.md`](../AGENTS.md) - the vendor-neutral canonical context all CLIs read first
- The SpecRoute framework's `runtimes/.codex/README.md` - the canonical Codex layout this is modeled on
