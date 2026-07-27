# Sanitization Auditor - Working Notes

Verified against disk on 2026-07-27. This file is **tracked and public** - it must never contain a resolved home directory, a real memory filename, or any other value it is telling you to scan for. Verify with the section 3 check in `.claude/commands/sanitize.md`.

## Authoritative source

The canonical list of forbidden strings (private upstream project names, internal paths, domain-specific terms) lives in the **user-level** memory directory:

```
~/.claude/projects/<flattened-project-path>/memory/<sanitization-note>.md
```

`<flattened-project-path>` is the repo's absolute path with every `/` replaced by `-`. Resolve it at runtime rather than hard-coding it - a resolved path in a tracked file embeds a real home directory, which is itself a leak:

```bash
# Locate the user-level memory dir and list its notes.
MEM="$HOME/.claude/projects/$(git rev-parse --show-toplevel | tr '/' '-')/memory"
ls "$MEM"
```

The sanitization note is the one covering this repo's public-release rules; `MEMORY.md` in the same directory indexes them. Those files are **not** tracked in this repo (they live in the user's local Claude config). Read them at the start of every audit. If the directory is missing or unreadable, ask the user before proceeding - do not guess at the forbidden list.

## Standard audit sequence

1. Confirm gitignore has `initial.md` and `.claude/settings.local.json`.
2. Run the `/sanitize` command for the standard forbidden-strings sweep.
3. For deeper review:
   - Walk `git ls-files` and grep each tracked file against the user-level forbidden list.
   - Scan for absolute filesystem paths **and their flattened equivalents**. A home-dir path can hide as `/Users/<name>/...` or, in Claude project directory names, as the slash-flattened `-Users-<name>-...`. `/sanitize` section 3 covers both; do not narrow it back to the `LocalDev` form alone.
   - Scan for likely secrets with the regex in `.claude/commands/sanitize.md`.
4. For PR review: also walk the diff (`git diff --cached`) - new content is more likely to leak than existing.

## Known intentional placeholders

These are NOT leaks even though they pattern-match the absolute-path regex:

- `.claude/agents/sanitization-auditor.md` - contains `/Users/<user>/LocalDev/<private>/` as illustrative regex examples, with `<user>` and `<private>` as placeholders, not real values.
- `.claude/commands/sanitize.md` and `.claude/commands/audit.md` - same pattern.
- This file - same pattern.
- Any line quoting a regex rather than a path. `/sanitize` drops lines containing a `[^` character-class fragment for exactly this reason.

Angle-bracket placeholders are the convention: `<user>`, `<private>`, `<name>`, `<repo>`, `<flattened-project-path>`. If you need a new one, add it to `IGNORE_RE` in `.claude/commands/sanitize.md` at the same time.

## Block / warn distinction

- **Block** (exit non-zero in `pre-bash-sanitize.sh`): forbidden strings, real absolute paths (or their flattened `-Users-...` equivalents), real secrets.
- **Warn** (stderr only): drift, missing optional frontmatter, suspicious-but-uncertain content. The user decides.

## Update protocol

The forbidden-strings wordlist is **not** stored in tracked files (that would defeat the purpose). It lives at:

```
.claude/.forbidden-strings.txt   (gitignored, per-installation)
```

The hook scripts (`pre-bash-sanitize.sh`, `session-start-status.sh`) and `/sanitize` command read this file at runtime. If the file is missing, sanitization gates degrade gracefully (warn, don't block).

When the user adds a new private term to forbid:
1. Add the term to `.claude/.forbidden-strings.txt`.
2. Update the user-level sanitization note under `~/.claude/projects/<flattened-project-path>/memory/` (resolve the path with the snippet above) to record the term and rationale.
3. Run `/sanitize` to confirm no existing tracked file already contains the new term.
