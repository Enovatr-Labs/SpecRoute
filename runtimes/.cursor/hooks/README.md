# `.cursor/hooks/`

Working Cursor hooks: an annotated config template plus the three shell scripts it references.

> **The config does not live here.** Cursor reads `.cursor/hooks.json` - one level *up* from this
> directory - or `~/.cursor/hooks.json` for user scope. A `hooks.json` left inside `.cursor/hooks/`
> is never read. Copy `hooks.template.json` to `.cursor/hooks.json`; keep the scripts under
> `.cursor/hooks/scripts/`.

## Layout

```
runtimes/.cursor/hooks/
├── README.md                        (this file)
├── hooks.template.json              copy to .cursor/hooks.json
└── scripts/
    ├── session-start-status.sh      sessionStart          - orientation banner
    ├── pre-shell-sanitize.sh        beforeShellExecution  - sanitization gate (blocks)
    └── post-edit-frontmatter.sh     afterFileEdit         - frontmatter check (warns)
```

## Setup

```bash
mkdir -p .cursor/hooks/scripts
cp runtimes/.cursor/hooks/hooks.template.json .cursor/hooks.json
cp runtimes/.cursor/hooks/scripts/*.sh        .cursor/hooks/scripts/
chmod +x .cursor/hooks/scripts/*.sh
```

Cursor chooses the hook command's working directory by scope, not by the directory containing
`hooks.json`. **Project** hooks run from the project root, so `.cursor/hooks/scripts/x.sh` is
correct. **User** hooks run from `~/.cursor/`, so the same entry must use
`./hooks/scripts/x.sh`.

Create the wordlist the sanitization gate reads (per-installation, gitignored):

```bash
cat > .cursor/.forbidden-strings.txt <<'EOF'
# Forbidden strings - one whitespace-free term per line. Lines starting with '#' are comments.
EOF
echo '.cursor/.forbidden-strings.txt' >> .gitignore
```

The gate falls back to `.claude/.forbidden-strings.txt` when this file is absent.

Verify:

```bash
python3 -c "import json; json.load(open('.cursor/hooks.json'))" && echo "config OK"
ls -l .cursor/hooks/scripts/*.sh
```

## Blocking semantics

Exit `0` succeeds, exit `2` blocks (equivalent to `permission: "deny"`), and **anything else
fails open** - the action proceeds. That default is the important difference from every other
vendor in the matrix: a Cursor hook that crashes or times out does not protect you.

Set `failClosed: true` per hook entry to invert it. `beforeShellExecution` in the shipped template
does exactly that, because a sanitization gate that fails open is not a gate. Copy the flag onto any
hook of your own that must not be bypassed by its own failure.

Control events (`before*` / `pre*`) return a decision object:

```json
{ "permission": "allow|deny|ask", "user_message": "...", "agent_message": "..." }
```

Observational events (`after*`, `postToolUse`, `afterAgentResponse`) have their output ignored.

## The three defaults

| Default | Event | Status |
|---|---|---|
| Session-start orientation | `sessionStart` | Works. Returns `additional_context`, which Cursor injects into the conversation. |
| Sanitization gate | `beforeShellExecution` | Works, and genuinely blocks. Denies via **both** the JSON decision and exit 2, with `failClosed: true` so a crash also blocks. |
| Post-edit frontmatter check | `afterFileEdit` | Fires and lints correctly, but **the warning does not reach the chat**. `afterFileEdit` is observational and Cursor ignores hook output, so the message lands on stderr in the hook log only. |

All three are expressible; the third is degraded rather than absent. If you need frontmatter
warnings in front of the agent, move the check to `beforeShellExecution` on a lint command, or run
it as a `preToolUse` control hook where output is honoured - at the cost of firing before the write
rather than after it.

## The Tab events

Cursor's ~21 events include Tab-scoped ones (`beforeTabFileRead`, `afterTabFileEdit`) that fire in
the inline-completion flow rather than the agent loop. Nothing here wires them; add them only if
your project uses Cursor Tab, and expect them to fire far more often than the agent events.

## Reference

The permission schema, the environment variables Cursor exports (`CURSOR_PROJECT_DIR` and the
`CLAUDE_PROJECT_DIR` compatibility alias), matcher syntax, and hardening rules are in
[`hooks/cursor/scripts/README.md`](../../../hooks/cursor/scripts/README.md). The full event table is
in [`hooks/README.md`](../../../hooks/README.md).
