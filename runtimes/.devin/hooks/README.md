# Devin Desktop hook assets

Devin Local reads the standalone project hook file at
`.devin/hooks.v1.json`. This directory holds the annotated source template and
the three scripts it invokes.

## Install

```bash
cp runtimes/.devin/hooks/hooks.v1.template.json .devin/hooks.v1.json
mkdir -p .devin/hooks/scripts
cp runtimes/.devin/hooks/scripts/*.sh .devin/hooks/scripts/
chmod +x .devin/hooks/scripts/*.sh
```

## Defaults

| Script | Event | Matcher | Behavior |
|---|---|---|---|
| `session-start-status.sh` | `SessionStart` | none | Injects a compact project orientation |
| `pre-shell-sanitize.sh` | `PreToolUse` | `^exec$` | Blocks publication when forbidden strings remain |
| `post-edit-frontmatter.sh` | `PostToolUse` | `^edit$` | Advises on frontmatter after file edits |

The documented event set is `PreToolUse`, `PostToolUse`, `PermissionRequest`,
`UserPromptSubmit`, `Stop`, `PostCompaction`, `SessionStart`, and `SessionEnd`.
Hooks may be `command` or `prompt`; these templates use command hooks so their
behavior is deterministic and testable.

Exit `0` succeeds, exit `2` blocks, and other non-zero exits are logged without
blocking. Matchers are regular expressions over `tool_name`.

Create a gitignored wordlist before relying on the publication gate:

```bash
printf '# One whitespace-free term per line.\n' > .devin/.forbidden-strings.txt
echo '.devin/.forbidden-strings.txt' >> .gitignore
```

Use `/hooks` in Devin Local to inspect loaded hooks and their source files.
