# `.codex/hooks/`

Working Codex hooks: an annotated config template plus the three shell scripts it references.

> **The config does not live here.** Codex reads `.codex/hooks.json` - one level *up* from this
> directory - or an inline `[hooks]` table in `.codex/config.toml`. A `hooks.json` left inside
> `.codex/hooks/` is never read, and the failure is silent. Copy `hooks.template.json` to
> `.codex/hooks.json`; keep the scripts under `.codex/hooks/scripts/`.

## Layout

```
runtimes/.codex/hooks/
├── README.md                       (this file)
├── hooks.template.json             copy to .codex/hooks.json
└── scripts/
    ├── session-start-status.sh     SessionStart  - orientation banner
    ├── pre-tool-sanitize.sh        PreToolUse    - sanitization gate (blocks)
    └── post-edit-frontmatter.sh    PostToolUse   - frontmatter check (warns)
```

## Setup

```bash
mkdir -p .codex/hooks/scripts
cp runtimes/.codex/hooks/hooks.template.json .codex/hooks.json
cp runtimes/.codex/hooks/scripts/*.sh        .codex/hooks/scripts/
chmod +x .codex/hooks/scripts/*.sh
```

Then create the wordlist the sanitization gate reads. It is per-installation and belongs in
`.gitignore`:

```bash
cat > .codex/.forbidden-strings.txt <<'EOF'
# Forbidden strings - one whitespace-free term per line. Lines starting with '#' are comments.
EOF
echo '.codex/.forbidden-strings.txt' >> .gitignore
```

The gate falls back to `.claude/.forbidden-strings.txt` if `.codex/.forbidden-strings.txt` is
absent, so a repo running both runtimes keeps a single list.

Confirm the config parses and the scripts are executable:

```bash
python3 -c "import json; json.load(open('.codex/hooks.json'))" && echo "config OK"
ls -l .codex/hooks/scripts/*.sh
```

Hooks are enabled by default. The canonical feature key is `hooks`; `codex_hooks` remains a
deprecated alias in 0.145.0. To disable hooks explicitly in `.codex/config.toml`:

```toml
[features]
hooks = false
```

## Blocking semantics

Exit `0` allows, exit `2` blocks with stderr as the rejection reason, any other code is a failure.
`PreToolUse` and `PermissionRequest` are the blocking events; `PostToolUse` can only replace the
tool result. Multiple hooks matching the same event run **concurrently**, so no script may depend on
another having run first.

## The three defaults

| Default | Event | Status |
|---|---|---|
| Session-start orientation | `SessionStart` | Works. Emits the banner as Claude-compatible `hookSpecificOutput.additionalContext`. |
| Sanitization gate | `PreToolUse` | Works, and genuinely blocks (exit 2). |
| Post-edit frontmatter check | `PostToolUse` | Works. Advisory - returns `additionalContext`, never blocks. |

All three of SpecRoute's defaults are expressible on Codex. Its event vocabulary is identical to
Claude Code's, which makes this the easiest cross-vendor port in the framework.

## Why every matcher is empty

Each entry in `hooks.template.json` uses `"matcher": ""` (universal). A Codex matcher is a regex
over the **tool name**, tool names differ between builds, and a matcher that fails to match produces
a hook that never fires - silently. Each script re-filters its own stdin payload instead, which you
can test from a shell:

```bash
printf '%s' '{"tool_input":{"command":"git commit -m x"}}' \
  | bash .codex/hooks/scripts/pre-tool-sanitize.sh; echo "exit=$?"
```

Narrow the matchers only after confirming what your Codex build actually emits - and never narrow a
*blocking* gate, because a missed match there is a hole rather than a warning.

## Reference

Protocol details, the Claude-compatible JSON output schemas, and hardening rules are in
[`hooks/codex/scripts/README.md`](../../../hooks/codex/scripts/README.md). The full 11-event table
is in [`hooks/README.md`](../../../hooks/README.md).
