# Claude Code-specific Rules

How rules and standards are loaded into Claude Code. Rules content itself defers to the vendor-neutral rule files in this directory.

## Where Claude Code looks

- **`CLAUDE.md`** at the repo root - Claude Code's canonical context file. Reference shared rules from here.
- **`.claude/rules/*.md`** - modular instruction files loaded by the runtime itself. See below.
- **`AGENTS.md`** - also read; rules linked here are accessible.
- **`.claude/agents/<name>.md`** - agent-level operating principles (per-agent guidance, with `description` triggers).
- **`.claude/skills/<slug>/SKILL.md`** - skill-level operating principles.
- **`.claude/commands/<slug>.md`** - legacy-but-supported slash commands; the body is read on invocation.
- **`.claude/hooks/`** - automation rules enforced via hook scripts.

## `.claude/rules/*.md` - the native rule loader

Claude Code loads Markdown instruction files from `.claude/rules/`, discovered **recursively** (subdirectories are fine, so you can group by domain). There is exactly one optional frontmatter field:

```yaml
---
paths:
  - "src/**/*.ts"
  - "packages/*/src/**"
---
```

| Case | Loading behaviour |
|---|---|
| No frontmatter (or no `paths`) | Loaded at session launch, at the **same priority as `CLAUDE.md`**. |
| `paths:` present | Loaded only when a file matching one of the globs is touched. |

User-level rules in `~/.claude/rules/` load **before** project rules, so a project rule is read in the context of the user's standing preferences.

Practical consequences:

- Move always-on standards out of a ballooning `CLAUDE.md` into `.claude/rules/<topic>.md`; it costs the same context and reads better.
- Put per-language or per-area conventions behind `paths:` so they only cost context when relevant. This is the Claude Code analogue of Cursor's `globs` and Kiro's `inclusion: fileMatch`.
- There is no `alwaysApply` or `description` field. Presence or absence of `paths` is the whole contract.

### Do not confuse this with SpecRoute's `rules/` directory

SpecRoute's top-level `rules/` (the directory holding this file) is a **documentation** concept - vendor-neutral standards plus per-vendor explainers. Claude Code does not read it. `.claude/rules/` is a **runtime** feature that Claude Code reads automatically. To make SpecRoute rule content active in Claude Code, copy the body into `.claude/rules/<topic>.md` (adding `paths:` if it is scope-limited), or reference it from `CLAUDE.md`. See [`README.md`](README.md) for the full side-by-side.

## Recommended structure

In `CLAUDE.md` (which should be a slim delegation shim per the two-tier docs pattern), link to:

- [`AGENTS.md`](../AGENTS.md) - shared content.
- [`rules/engineering-rules.md`](engineering-rules.md)
- [`rules/code-review-rules.md`](code-review-rules.md)
- [`rules/security-rules.md`](security-rules.md)
- [`rules/documentation-rules.md`](documentation-rules.md)

Claude Code reads `CLAUDE.md` automatically; deep references resolve when the agent reads them.

For standards that must be in context every session without waiting for the agent to follow a link, put the body in `.claude/rules/<topic>.md` instead - it loads at launch at `CLAUDE.md` priority. Reserve the link-from-`CLAUDE.md` approach for reference material that is only occasionally needed.

## Vendor-specific behaviors

| Topic | Claude Code behavior |
|---|---|
| Permissions (`.claude/settings.json` `permissions`) | Allow/deny lists tighten or relax tool calls without prompting. |
| Per-user overrides (`.claude/settings.local.json`) | Gitignored; layers personal preferences on top of project settings. |
| Hooks (`.claude/settings.json hooks` or `~/.claude/settings.json`) | Most comprehensive of any vendor. 30 events spanning session/tool/permission/subagent/task/stop/config/cwd/file/worktree/compact/elicitation/notification lifecycles. 5 hook types: `command`, `http`, `mcp_tool`, `prompt`, `agent`. Blocking via exit 2 or `hookSpecificOutput.permissionDecision: "deny"`. Per-hook `if` filter (permission rule syntax), `timeout`, `async`, `asyncRewake`, `shell`, `once`. See [`hooks/claude/hooks.template.json`](../hooks/claude/hooks.template.json). |
| Sub-agents (`.claude/agents/`) | Invoked via the `Task` tool with `subagent_type: <agent-name>` - the runtime auto-loads agents from this dir. Author them by editing files directly; the interactive `/agents` wizard was removed in v2.1.198 and now only prints a reminder to edit `.claude/agents/`. |
| Skills and commands | **One contract, two locations.** `.claude/skills/<slug>/SKILL.md` is the current form; `.claude/commands/<name>.md` is legacy-but-supported and takes the *same* frontmatter as a skill. Don't maintain a separate "command frontmatter" mental model. |
| MCP servers (`.mcp.json` at project root, `~/.claude.json` for user servers, `claude_desktop_config.json` for Claude Desktop) | Multi-layered; `.mcp.json` configures project servers, `~/.claude.json` configures user-level servers. |

## Tool fields are not a sandbox

Skill and command frontmatter accepts `allowed-tools`, and it is routinely misread as a restriction. It is not:

- **`allowed-tools` pre-approves** the listed tools for the invoking turn so the user isn't prompted. The grant clears on the next message. It does not remove anything from the tool pool.
- **`disallowed-tools`** is the field that actually removes tools from the pool.

Write security rules accordingly: a short `allowed-tools` list is a convenience, not confinement. Real confinement comes from `disallowed-tools`, `permissions` deny rules in `.claude/settings.json`, and hooks.

## Sanitization gate

The PreToolUse hook (`pre-bash-sanitize.sh`) is recommended for any project using SpecRoute. It blocks `git commit` / `git push` if forbidden strings appear in tracked files. See [`security-rules.md`](security-rules.md) Rule 10.

## See also

- [`README.md`](README.md) - SpecRoute `rules/` vs Claude Code `.claude/rules/`.
- [`engineering-rules.md`](engineering-rules.md) - vendor-neutral engineering rules.
- [`runtimes/.claude/README.md`](../runtimes/.claude/README.md) - Claude Code runtime layout.
- [`agentic-docs/automation-decision-framework.md`](../agentic-docs/automation-decision-framework.md) - when to build a skill vs agent vs command vs hook.
- Claude Code documentation root: <https://code.claude.com/docs/en/>
