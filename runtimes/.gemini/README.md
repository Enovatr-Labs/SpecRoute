# `.gemini/` - Gemini CLI runtime layout

Drop this directory into the root of your project. Gemini reads from these paths. Current Gemini CLI builds back the full SpecRoute capability matrix: skills, subagents, commands, hooks, and MCP servers.

## Layout

```
.gemini/
├── settings.json                MCP servers (mcpServers) + hooks block
├── skills/
│   └── <slug>/SKILL.md          Agent Skills open standard (enabled by default)
├── agents/
│   └── <name>.md                subagents (Markdown + YAML frontmatter)
├── commands/
│   └── <name>.toml              custom commands (prompt + optional description)
└── hooks/scripts/*.sh           shell scripts the settings.json hooks block invokes
```

There is **no `.gemini/hooks.json`**. Gemini reads hooks from a top-level `hooks` key inside
`settings.json`; a separate hooks file is never read. `.gemini/hooks/` holds only the scripts.

## Setup

1. Copy the settings template:

   ```bash
   cp runtimes/.gemini/settings.template.json .gemini/settings.json
   ```

2. **MCP servers** - `settings.json`'s `mcpServers` map mirrors the canonical `runtimes/mcp/servers.yaml`. Run `runtimes/mcp/render/render_gemini.py` to regenerate it.

3. **Hooks** - install the scripts, then merge the `hooks` key into `settings.json`:

   ```bash
   mkdir -p .gemini/hooks/scripts
   cp runtimes/.gemini/hooks/scripts/*.sh .gemini/hooks/scripts/
   chmod +x .gemini/hooks/scripts/*.sh

   python3 - <<'PY'
   import json
   settings = json.load(open(".gemini/settings.json"))
   snippet = json.load(open("runtimes/.gemini/hooks/hooks-settings.snippet.json"))
   settings["hooks"] = snippet["hooks"]
   json.dump(settings, open(".gemini/settings.json", "w"), indent=2)
   PY

   printf '# One whitespace-free term per line.\n' > .gemini/.forbidden-strings.txt
   echo '.gemini/.forbidden-strings.txt' >> .gitignore
   ```

   That wires three hooks: a `SessionStart` orientation banner, a `BeforeTool` sanitization gate that
   blocks `git commit` / `git push` / `gh pr create` / `gh release create` while forbidden strings
   remain in tracked files, and an `AfterTool` frontmatter check.

   **The hooks block ships as a separate snippet on purpose.** `runtimes/.gemini/settings.template.json`
   is *generated* from [`../mcp/servers.yaml`](../mcp/servers.yaml) by
   [`../mcp/render/render_gemini.py`](../mcp/render/render_gemini.py). Hand-editing it to add hooks is
   silently overwritten on the next render and breaks the single-source invariant, so the hooks live in
   [`hooks/hooks-settings.snippet.json`](hooks/hooks-settings.snippet.json) and are merged at install
   time. Re-run the merge after any regeneration.

   **Blocking semantics**: exit `0` succeeds, exit `2` is a system block with stderr as the reason,
   anything else is a warning and the CLI continues. Stdout must be the final JSON and nothing else -
   stricter than any other vendor. Only `type: "command"` is supported.

   See [`hooks/README.md`](hooks/README.md) for the full contract and the 11-event vocabulary
   (SessionStart, SessionEnd, BeforeAgent, AfterAgent, BeforeModel, AfterModel, BeforeToolSelection,
   BeforeTool, AfterTool, PreCompress, Notification), which is shared with no other vendor.

4. **Skills** - copy `runtimes/.gemini/skills/` to `.gemini/skills/`. One folder per skill with a `SKILL.md`; see [`skills/README.md`](skills/README.md) for the frontmatter contract.

5. **Subagents** - copy `runtimes/.gemini/agents/` to `.gemini/agents/`. One Markdown file per subagent; see [`agents/README.md`](agents/README.md).

6. **Commands** - copy `runtimes/.gemini/commands/` to `.gemini/commands/`. One TOML file per command; subdirectories namespace as `/parent:child`. See [`commands/README.md`](commands/README.md).

## Capability matrix

| Concept | Available in Gemini? | Where |
|---|---|---|
| Skills | Yes | `.gemini/skills/<slug>/SKILL.md` |
| Subagents | Yes | `.gemini/agents/<name>.md` |
| Slash commands | Yes | `.gemini/commands/<name>.toml` (TOML, not the old JSON map) |
| Hooks | Yes | `settings.json` `hooks` block (11 events); scripts in `.gemini/hooks/scripts/` |
| MCP servers | Yes | `settings.json` `mcpServers` |
| Engineering rules | Indirect | root `GEMINI.md` and rules referenced from there |
| Prompts | Yes | `prompts/` works in any agent CLI that reads markdown |

## Root context file

Gemini reads `GEMINI.md` at repo root. It should be a short delegation shim pointing to `AGENTS.md`. See [`../../GEMINI.md`](../../GEMINI.md) for an example.

## What's tracked vs gitignored

| Path | Tracked? |
|---|---|
| `.gemini/settings.json` | Yes (sans secrets) |
| `.gemini/skills/`, `.gemini/agents/`, `.gemini/commands/` | Yes |
| `.gemini/hooks/scripts/*.sh` | Yes |
| `.gemini/.forbidden-strings.txt` | **No** (per-installation) |

Secrets and personal preferences belong in environment variables or `.env` (gitignored).

## Transition note

Google began superseding the standalone Gemini CLI with the Antigravity CLI on 2026-06-18 for free and Google One tiers; paid tiers retain Gemini CLI access. The `.gemini/` layout described here remains valid for current installs, and the skills/agents/commands artifacts are portable to whatever runtime ships next.
