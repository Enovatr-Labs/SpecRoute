# Gemini / Antigravity-specific Rules

How rules and standards are loaded into Gemini CLI and Google Antigravity CLI (which superseded standalone Gemini CLI starting June 2026). Rules content itself defers to the vendor-neutral rule files in this directory.

## Where Gemini / Antigravity looks

- **`GEMINI.md`** at the repo root - the canonical context file, and the **only** root file loaded out of the box.
- **`.gemini/settings.json`** - MCP server configuration, hook definitions, and the `context.fileName` setting.
- **`.gemini/commands/*.toml`** - slash commands.
- **`.gemini/skills/<slug>/SKILL.md`**, **`.gemini/agents/<name>.md`** - skills and subagents.

> **Gemini CLI does not read `AGENTS.md` by default.** It reads `GEMINI.md`. Support for `AGENTS.md` requires opting in via the `context.fileName` setting; the upstream request to read it by default was closed as not planned. Do not assume the cross-vendor `AGENTS.md` convention reaches Gemini for free.

## Reading `AGENTS.md` in Gemini

Two workable options, in order of preference:

**Option A - opt in via settings.** Point Gemini's context loader at both files in `.gemini/settings.json`:

```json
{
  "context": {
    "fileName": ["GEMINI.md", "AGENTS.md"]
  }
}
```

This keeps `GEMINI.md` as the vendor shim and lets the canonical `AGENTS.md` load alongside it. It is a per-project setting and must be committed for teammates to get the same behaviour.

**Option B - make `GEMINI.md` self-sufficient.** If you cannot rely on the setting being present, `GEMINI.md` has to carry (not merely link to) the standards that must always be in context. This trades duplication for reliability - the trade-off the delegation-shim pattern normally avoids, so take it only when Option A is unavailable.

A shim that merely says "read `AGENTS.md`" is a third, weaker option: the model can still follow the link once it is working in the repo, but nothing is loaded at launch.

## Recommended structure

In `GEMINI.md`:

```markdown
# GEMINI.md

For project context, conventions, and rules, read [`AGENTS.md`](AGENTS.md).

## Gemini-specific overrides

<vendor-specific bits only - keep this short>
```

From whichever root file is actually loaded, link to:

- [`rules/engineering-rules.md`](engineering-rules.md)
- [`rules/code-review-rules.md`](code-review-rules.md)
- [`rules/security-rules.md`](security-rules.md)
- [`rules/documentation-rules.md`](documentation-rules.md)

## Vendor mapping notes

- Skills: Gemini supports folder-per-skill `SKILL.md` under `.gemini/skills/`, and also reads the vendor-neutral `.agents/skills/` root. Frontmatter is the Agent Skills standard `name` + `description`; Claude's `argument-hint` / `user-invocable` / `allowed-tools` are not consumed.
- Subagents: flat agent files under `.gemini/agents/`.
- Slash commands: TOML files under `.gemini/commands/*.toml` (a `prompt`, not a markdown body or a shell string).

For SpecRoute artifacts that don't have a one-to-one Gemini equivalent:

- Use `prompts/shared/` and `prompts/codex|claude/` as reference prompts that humans copy into a Gemini conversation.

## Vendor-specific behaviors

| Topic | Gemini behavior |
|---|---|
| Root context file | `GEMINI.md` only, unless `context.fileName` is set. `AGENTS.md` is **not** read by default. |
| MCP servers | Configured in `.gemini/settings.json` `mcpServers`. |
| Slash commands | TOML files under `.gemini/commands/*.toml` (required `prompt`, optional `description`; subdirs namespace as `/parent:child`; `{{args}}` is the argument placeholder). |
| Skills | Folder-per-skill `SKILL.md` under `.gemini/skills/`; `.agents/skills/` is also read. |
| Subagents | Flat agent files under `.gemini/agents/`. |
| Hooks | Top-level `hooks` key in `.gemini/settings.json`. **11 events with a vocabulary distinct from every other vendor**: `BeforeTool`, `AfterTool`, `BeforeModel`, `AfterModel`, `BeforeToolSelection`, `BeforeAgent`, `AfterAgent`, `SessionStart`, `SessionEnd`, `PreCompress`, `Notification`. Do not port Claude's `PreToolUse` / `PostToolUse` names - they will not fire. `type: "command"` is the only hook type. Exit code 2 blocks. See [`hooks/gemini/`](../hooks/gemini/). |
| Stdout discipline (hooks) | Gemini is **strict** - hook scripts must print **only the final JSON to stdout**. Send diagnostics to stderr. Plain-text-mixed-with-JSON breaks the parser. |
| Rule loading | None native - no `.gemini/rules/` equivalent of Claude's `.claude/rules/` or Cursor's `.cursor/rules/`. Rules surface only through the loaded root context file. |

## See also

- [`README.md`](README.md) - what SpecRoute's `rules/` directory is and is not.
- [`engineering-rules.md`](engineering-rules.md) - vendor-neutral engineering rules.
- [`runtimes/.gemini/README.md`](../runtimes/.gemini/README.md) - Gemini runtime layout.
- [`agentic-docs/multi-vendor-context-files.md`](../agentic-docs/multi-vendor-context-files.md) - the delegation-shim pattern, and why Gemini is its awkward case.
