# `.codex/` - Codex runtime layout

Drop this directory into the root of your project. Codex reads from these paths automatically.

## Layout

```
.codex/
├── config.toml                      MCP servers + approval policy
├── agents/<name>.toml               standalone TOML subagents (NOT Claude's Markdown shape)
├── skills/<slug>/SKILL.md           folder-per-skill (portable body, Codex frontmatter)
├── hooks.json                       lifecycle hooks (11 events; enabled by default)
├── hooks/scripts/*.sh               shell scripts the hook entries invoke
└── scripts/                         project-internal scripts
```

Note the split: Codex reads the hook **config** from `.codex/hooks.json`, but the **scripts** it
references live under `.codex/hooks/scripts/`. A `hooks.json` placed inside `.codex/hooks/` is never
read, and the failure is silent.

## Setup

1. Copy `config.template.toml` → `.codex/config.toml`. Adjust `approval_policy` and `sandbox_mode` for your team's risk posture.

2. **MCP servers** - `config.toml` carries the MCP server inventory under `[mcp_servers.<name>]` blocks. Maintain `runtimes/mcp/servers.yaml` as the canonical source and run `runtimes/mcp/render/render_codex.py` to regenerate.

3. **Agents** - author standalone TOML files under `.codex/agents/<name>.toml` with required fields `name`, `description`, `developer_instructions` (see [`agents/spec-reviewer.toml`](agents/spec-reviewer.toml)). This is a **different shape** from Claude's flat Markdown agents, so agents do not cross-mirror automatically.

4. **Skills** - copy from `runtimes/.codex/skills/` (or body-sync from `.claude/skills/`). The `SKILL.md` body is portable; preserve Codex's own frontmatter.

5. **Hooks** - enabled by default. The canonical `[features]` key is `hooks` (`codex_hooks` is a deprecated alias); disable with `[features] hooks = false`. Install the working set from [`hooks/`](hooks/):

   ```bash
   mkdir -p .codex/hooks/scripts
   cp runtimes/.codex/hooks/hooks.template.json .codex/hooks.json
   cp runtimes/.codex/hooks/scripts/*.sh        .codex/hooks/scripts/
   chmod +x .codex/hooks/scripts/*.sh
   ```

   That wires three hooks: a `SessionStart` orientation banner, a `PreToolUse` sanitization gate that
   blocks `git commit` / `git push` / `gh pr create` / `gh release create` while forbidden strings
   remain in the working tree, staged index, or outgoing commits, and a `PostToolUse` frontmatter check. Create the gate's wordlist and
   gitignore it:

   ```bash
   printf '# One whitespace-free term per line.\n' > .codex/.forbidden-strings.txt
   echo '.codex/.forbidden-strings.txt' >> .gitignore
   ```

   **Blocking semantics**: exit `0` allows, exit `2` blocks with stderr as the rejection reason,
   anything else is a failure. `PreToolUse` and `PermissionRequest` are the blocking events;
   `PostToolUse` can only replace the tool result. Matching hooks run concurrently, so no script may
   depend on another. Only `type: "command"` executes today - `prompt` and `agent` handlers are
   parsed then skipped.

   11 lifecycle events, Claude-compatible JSON schema. Alternatively merge the inline `[hooks]` table
   into `config.toml`. See [`hooks/README.md`](hooks/README.md) for the full contract and
   [`hooks/codex/`](../../hooks/codex/) for the annotated reference template.

6. **Cross-vendor sync** - run `tools/sync-skills.py --dry-run` to verify Claude / Codex **skill** parity. Agents are excluded (formats differ).

## What's tracked vs gitignored

| Path | Tracked? |
|---|---|
| `.codex/config.toml` | Yes (sans secrets) |
| `.codex/agents/*.toml` | Yes |
| `.codex/skills/<slug>/SKILL.md` | Yes |
| `.codex/hooks.json` | Yes |
| `.codex/hooks/scripts/*.sh` | Yes |
| `.codex/.forbidden-strings.txt` | **No** (per-installation) |
| `.codex/scripts/*` | Yes |

Secrets (e.g. `GITHUB_PERSONAL_ACCESS_TOKEN`) belong in environment variables or a gitignored `.env`, never inline in `config.toml`.

## Mirroring with Claude Code

Codex shares **one** file shape with Claude Code outright - skills (`<slug>/SKILL.md`). Agents, commands, and hooks each map differently:

| Concept | Claude path | Codex path |
|---|---|---|
| Agent | `.claude/agents/<name>.md` (Markdown + frontmatter) | `.codex/agents/<name>.toml` (TOML: `name`, `description`, `developer_instructions`) - **format differs** |
| Skill | `.claude/skills/<slug>/SKILL.md` | `.codex/skills/<slug>/SKILL.md` (body shared; frontmatter preserved per runtime) |
| Slash command | `.claude/commands/<name>.md` | a skill invoked via `/skills` or `$mention` |
| Hook | `.claude/settings.json` (`hooks` key) + scripts | `.codex/hooks.json` or `[hooks]` in `config.toml` (11 events, names identical to Claude Code; only `type: "command"` executes today) |

To keep Claude and Codex **skills** in sync: `tools/sync-skills.py`. Agents are not synced - the TOML/Markdown formats diverge.
