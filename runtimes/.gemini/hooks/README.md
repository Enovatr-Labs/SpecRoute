# `.gemini/hooks/`

Working Gemini CLI hooks: a settings **snippet** plus the three shell scripts it references.

> **Gemini has no hooks file.** Hooks live under a top-level `hooks` key **inside
> `.gemini/settings.json`** (project) or `~/.gemini/settings.json` (user). There is no
> `.gemini/hooks.json`, and creating one gets you hooks that never fire.
>
> **Do not hand-edit `runtimes/.gemini/settings.template.json` to add them.** That file is generated
> from [`runtimes/mcp/servers.yaml`](../../mcp/servers.yaml) by
> [`render_gemini.py`](../../mcp/render/render_gemini.py); a hand edit is silently overwritten on the
> next render and breaks the single-source invariant. `hooks-settings.snippet.json` exists precisely
> so the hooks block stays outside the generated file until merge time.

## Layout

```
runtimes/.gemini/hooks/
├── README.md                        (this file)
├── hooks-settings.snippet.json      merge its "hooks" key into .gemini/settings.json
└── scripts/
    ├── session-start-status.sh      SessionStart - orientation banner
    ├── pre-shell-sanitize.sh        BeforeTool   - sanitization gate (blocks)
    └── post-edit-frontmatter.sh     AfterTool    - frontmatter check (warns)
```

## Setup

1. Render or copy the generated settings first, so MCP servers are in place:

   ```bash
   cp runtimes/.gemini/settings.template.json .gemini/settings.json
   ```

2. Install the scripts:

   ```bash
   mkdir -p .gemini/hooks/scripts
   cp runtimes/.gemini/hooks/scripts/*.sh .gemini/hooks/scripts/
   chmod +x .gemini/hooks/scripts/*.sh
   ```

3. Merge the `hooks` key into `.gemini/settings.json`:

   ```bash
   python3 - <<'PY'
   import json
   settings = json.load(open(".gemini/settings.json"))
   snippet = json.load(open("runtimes/.gemini/hooks/hooks-settings.snippet.json"))
   settings["hooks"] = snippet["hooks"]
   json.dump(settings, open(".gemini/settings.json", "w"), indent=2)
   PY
   ```

   Re-run this after any `render_gemini.py` regeneration - the renderer rewrites
   `settings.template.json` from `servers.yaml` and knows nothing about hooks.

4. Create the wordlist the sanitization gate reads (per-installation, gitignored):

   ```bash
   cat > .gemini/.forbidden-strings.txt <<'EOF'
   # Forbidden strings - one whitespace-free term per line. Lines starting with '#' are comments.
   EOF
   echo '.gemini/.forbidden-strings.txt' >> .gitignore
   ```

   The gate falls back to `.claude/.forbidden-strings.txt` when this file is absent.

5. Verify:

   ```bash
   python3 -c "import json; print('hooks' in json.load(open('.gemini/settings.json')))"
   ls -l .gemini/hooks/scripts/*.sh
   ```

Hooks are enabled by default from Gemini CLI 0.26.0 onward.

## Blocking semantics

Exit `0` succeeds, exit `2` is a **system block** with stderr as the reason, any other code is a
warning and the CLI continues. `BeforeAgent`, `AfterAgent`, `BeforeModel`, `AfterModel`,
`BeforeTool`, and `AfterTool` can block; `SessionStart`, `SessionEnd`, `BeforeToolSelection`,
`Notification`, and `PreCompress` cannot.

**Stdout discipline is stricter than any other vendor**: stdout must be the final JSON object and
nothing else. All three shipped scripts obey this and put diagnostics on stderr. If you add your
own, never `echo` plain text.

## The three defaults

| Default | Event | Status |
|---|---|---|
| Session-start orientation | `SessionStart` | Works. Emits `systemMessage` plus `hookSpecificOutput.additionalContext`, and repeats the banner on stderr so it is visible in the hook log either way. |
| Sanitization gate | `BeforeTool` | Works, and genuinely blocks (exit 2). |
| Post-edit frontmatter check | `AfterTool` | Works. Returns `systemMessage` and `continue: true` - warns, never hides the tool result. |

All three are expressible. Gemini's vocabulary shares no event names with the other five vendors,
so the *registration* had to be rewritten even though the script bodies port unchanged.

## Why the matchers are omitted

No entry in the snippet sets `matcher`, which Gemini reads as match-all. A matcher is a regex over
the tool name (`run_shell_command`, `write_file`, `edit_file`, `replace`, `mcp_<server>_<tool>`), and
a matcher that fails to match produces a hook that never fires - silently. Each script re-filters its
own payload instead:

```bash
printf '%s' '{"tool_name":"run_shell_command","tool_input":{"command":"git push"}}' \
  | bash .gemini/hooks/scripts/pre-shell-sanitize.sh; echo "exit=$?"
```

## Reference

Event-specific input fields, JSON output shapes, and hardening rules are in
[`hooks/gemini/scripts/README.md`](../../../hooks/gemini/scripts/README.md). The full 11-event table
is in [`hooks/README.md`](../../../hooks/README.md).

## Unverified

`hookSpecificOutput.additionalContext` is documented for `BeforeAgent`; whether `SessionStart`
honours it is not confirmed. The session-start script therefore emits `systemMessage` as well and
mirrors the banner to stderr, so the orientation text surfaces regardless of which key that build
reads.
