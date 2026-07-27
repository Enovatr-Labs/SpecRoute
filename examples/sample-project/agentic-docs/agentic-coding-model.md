# Agentic Coding Model in This Project

How the four primitives (skills, agents, commands, hooks) compose for user-search. This project ships two runtimes over one shared spec layer: the Claude Code runtime (`.claude/`) and a Codex runtime (`.codex/`) that demonstrates the same team in a second vendor's native shape.

## What we use

| Primitive | What it's used for | Claude (`.claude/`) | Codex (`.codex/`) |
|---|---|---|---|
| **Agents** | 9 implementation-team roles, named per task in `agent-roster.md` | [`.claude/agents/`](../.claude/agents/) (Markdown + frontmatter) | [`.codex/agents/`](../.codex/agents/) (TOML, `developer_instructions`) |
| **Commands** | Pre-commit and pre-PR validation | [`.claude/commands/`](../.claude/commands/) | a skill invoked via `/skills` or `$mention` |
| **Hooks** | Always-on enforcement (sanitization gate, frontmatter check, session status) | [`.claude/hooks/`](../.claude/hooks/) | `.codex/hooks.json` or inline `[hooks]` in `config.toml` (none shipped here) |
| **MCP servers** | filesystem, github, memory, sequential-thinking, playwright | [`.claude/mcp.template.json`](../.claude/mcp.template.json) | [`.codex/config.toml`](../.codex/config.toml) `[mcp_servers.*]` |
| **Skills** | Not used in this project | n/a | n/a |

The two runtimes are vendor shapes over the **same** project: identical agents, identical MCP set, identical spec triplet and prompts. Only the file format differs (Markdown vs TOML; `mcp.template.json` vs `config.toml`). Agents do not cross-sync automatically because the formats diverge - see [`.codex/README.md`](../.codex/README.md).

We don't use skills here because the work is task-driven. Each task in `tasks.md` is well-scoped enough to delegate to an agent without interactive prompting. If we found ourselves writing prompts that asked the user a series of questions, we'd build a skill.

## How they compose for a typical task

Concrete example: implementing task 10 (wire `/api/users/search` endpoint).

```
1. User runs prompts/runtime/pickup-next-task.md
   └── Agent reads tasks.md, identifies task 10 as next, names backend-engineer
       └── Agent invokes backend-engineer subagent
           └── backend-engineer reads task prompt at
               prompts/phase1_backend/010_wire_endpoint.md
           └── backend-engineer reads requirements R1.1...R5.3, NFR-*
           └── backend-engineer composes the validator + RBAC + cache + query
               + cursor + observability components into the request handler
           └── backend-engineer runs the test suite
           └── backend-engineer writes a commit message; runs git commit
               └── PreToolUse hook fires (pre-bash-sanitize.sh)
                   └── Hook reads .claude/.forbidden-strings.txt
                   └── Hook runs git grep for forbidden terms
                   └── If clean: exit 0 -> commit proceeds
                   └── If hits: exit 1 -> commit blocked, agent must fix
2. Before opening the PR, user runs /audit
   └── Command runs comprehensive checks: sanitization, frontmatter,
       broken links, vendor-matrix consistency
   └── If clean: PR-ready signal
```

Every stage involves multiple primitives. The hooks are invisible until they fire. The command is one-shot deterministic. The agents do the substantive work. No skills needed.

## When we'd add a skill

If a task involved interactive scaffolding ("scaffold a new ADR with the right frontmatter and number") we'd build a skill. Currently the team handles this manually because the cadence is low (5 ADRs total in the project history).

If we shipped a tool that's invoked from outside the implementation loop (say, a "weekly metrics report" generator that prompts the user for a date range), that'd be a skill.

## When we'd add a hook

We added three hooks because each enforces something the team cannot afford to forget:

- `session-start-status.sh` - shows where we are when starting a session (orientation).
- `pre-bash-sanitize.sh` - blocks commits if forbidden strings appear (compliance / privacy).
- `post-edit-frontmatter.sh` - validates agent / skill / command frontmatter on save (catches the contract violation early).

We'd add a fourth hook if we found ourselves repeatedly missing some validation. Hooks should be 1-second operations; if it's slower, it's a command instead.

## When we'd add an agent

We add an agent when:

- A task type recurs and benefits from a stable role.
- Boundaries between adjacent agents are clear (the "Don't use for" section is non-empty).
- Trigger phrases naturally point at the role.

Adding a 9th agent for this project would require a new role we don't currently have. Possible candidates if scope grew:

- `mobile-engineer` (not currently relevant; sample is web-only)
- `incident-responder` (for production rollout monitoring; currently absorbed into deployment-validator)
- `compliance-engineer` (for regulatory frameworks; not currently in scope)

## See also

- The framework's [`agentic-docs/agentic-coding-model.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/agentic-coding-model.md) for the broader composition theory.
- [`automation-decision-framework.md`](automation-decision-framework.md) - when to choose which primitive.
- [`.claude/agents/README.md`](../.claude/agents/README.md) - this project's agent roster.
