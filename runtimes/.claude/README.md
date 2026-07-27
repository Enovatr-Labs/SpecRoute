# `.claude/` - Claude Code runtime layout

Drop this directory into the root of your project (rename or merge with any existing `.claude/`). Claude Code reads from these paths automatically.

## Layout

```
.claude/
├── settings.json                       project-wide settings + hooks (tracked)
├── settings.local.json                 per-user overrides (gitignored)
├── (repo root) .mcp.json               MCP server config for the Claude Code CLI
├── agents/<name>.md                    flat-file agents
├── skills/<slug>/SKILL.md              folder-per-skill
├── commands/<name>.md                  slash commands
├── hooks/
│   ├── hooks.json                      annotated hook source of truth (NOT read by the CLI)
│   └── scripts/                        supporting shell scripts
└── agent-memory/<agent-name>/          per-agent persistent context
```

## Where hooks actually live

Read this before copying anything. Claude Code loads hooks from exactly these sources:

| Source | Read for a project? |
|---|---|
| `~/.claude/settings.json` | Yes (user scope) |
| `.claude/settings.json` | **Yes - tracked project scope** |
| `.claude/settings.local.json` | Yes (per-user, gitignored) |
| Managed policy settings | Yes (admin scope) |
| `<plugin>/hooks/hooks.json` | Only inside an installed **plugin** |
| Skill / agent frontmatter | Yes |

A bare project-level `.claude/hooks/hooks.json` is **not** on that list. Dropping hook configuration there and stopping gets you hooks that never fire - silently, with no error. `hooks/hooks.json` is kept in this layout as the *authoring* artifact: it can carry `_comment` annotations that would be noise inside `settings.json`, and it is the shape mirrored across the other vendor runtimes. `settings.template.json` already ships the same hook block inline, so a straight copy works; [`tools/sync-hooks-to-settings.sh`](../../tools/sync-hooks-to-settings.sh) keeps the two aligned when you edit `hooks.json`.

## Setup

1. **Copy templates into place** (rename `.template` suffix off):

   ```bash
   mkdir -p .claude/hooks/scripts
   cp runtimes/.claude/settings.template.json .claude/settings.json    # carries a working "hooks" key
   cp runtimes/.claude/settings.local.template.json .claude/settings.local.json
   cp runtimes/.claude/mcp.template.json .mcp.json    # Claude Code reads .mcp.json at the repo root
   cp runtimes/.claude/hooks/hooks.template.json .claude/hooks/hooks.json    # optional: the annotated original
   ```

2. **Add to `.gitignore`**:

   ```
   .claude/settings.local.json
   .claude/.forbidden-strings.txt
   ```

3. **Install hook scripts** (starter scripts are included under `hooks/scripts/`):

   ```bash
   mkdir -p .claude/hooks/scripts
   cp runtimes/.claude/hooks/scripts/*.sh .claude/hooks/scripts/
   chmod +x .claude/hooks/scripts/*.sh
   ```

   The hook commands resolve their script paths through `"${CLAUDE_PROJECT_DIR:-.}"`, so they fire correctly no matter which directory a tool call ran from.

   Verify. Note that checking `settings.json` alone is **not** enough - it confirms the hook is *wired*, not that the script it points at exists. A registered hook whose script is missing exits 127, which for the `PreToolUse` sanitization gate means it **fails open**: the publish command is allowed through with no scan. Assert both:

   ```bash
   jq -e '.hooks.PostToolUse[].hooks[].command' .claude/settings.json   # wired?
   for s in .claude/hooks/scripts/*.sh; do test -x "$s" || echo "MISSING/NOT EXECUTABLE: $s"; done
   ```

   If you keep `hooks.json` around and edit it, re-sync afterwards - otherwise your edits change nothing:

   ```bash
   tools/sync-hooks-to-settings.sh .claude/hooks/hooks.json .claude/settings.json
   ```

4. **Populate the wordlist** (gitignored):

   ```bash
   cat > .claude/.forbidden-strings.txt <<'EOF'
   # Forbidden strings - one per line. Lines starting with '#' are comments.
   # Add upstream private project names, internal identifiers, etc.
   EOF
   ```

5. **Add agents, skills, commands as your project requires.** See per-subdir READMEs.

## What's tracked vs gitignored

| Path | Tracked? |
|---|---|
| `.claude/settings.json` | Yes (this is where hooks execute from) |
| `.claude/settings.local.json` | **No** (per-user) |
| `.claude/.forbidden-strings.txt` | **No** (per-installation) |
| `.mcp.json` (repo root) | Project decision; usually yes (sans secrets) |
| `.claude/agents/*.md` | Yes |
| `.claude/skills/<slug>/SKILL.md` | Yes |
| `.claude/commands/*.md` | Yes |
| `.claude/hooks/hooks.json` | Yes (authoring source; the CLI reads `settings.json`) |
| `.claude/hooks/scripts/*.sh` | Yes |
| `.claude/agent-memory/**/*.md` | Yes (treat content as published) |

## Cross-vendor notes

- **Codex** consumes the same agent and skill shapes. Mirror agents and skills into `.codex/` and use `tools/sync-skills.py` to keep them aligned.
- **Gemini, Kiro, Cursor, and Devin Desktop** do not consume Claude's runtime layout. See their respective runtime dirs.

## Reference implementation

This repo's own `.claude/` directory at the repo root is a working example of every concept here. Read those files as worked examples.
