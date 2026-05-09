# Sanitization Auditor - Working Notes

## Authoritative source

The canonical list of forbidden strings (private upstream project names, internal paths, domain-specific terms) lives in the **user-level** memory directory:

```
~/.claude/projects/-Users-chika-LocalDev-SpecForge/memory/specforge_public_release.md
```

That file is **not** tracked in this repo (it lives in the user's local Claude config). Read it at the start of every audit. If the user-level memory file is missing or unreadable, ask the user before proceeding - do not guess at the forbidden list.

## Standard audit sequence

1. Confirm gitignore has `initial.md` and `.claude/settings.local.json`.
2. Run the `/sanitize` command for the standard forbidden-strings sweep.
3. For deeper review:
   - Walk `git ls-files` and grep each tracked file against the user-level forbidden list.
   - Scan for absolute filesystem paths with `git grep -nE "/Users/[^/]+/LocalDev/"` (excluding intentional `<user>/<private>` placeholders in this auditor's own files).
   - Scan for likely secrets with the regex in `.claude/commands/sanitize.md`.
4. For PR review: also walk the diff (`git diff --cached`) - new content is more likely to leak than existing.

## Known intentional placeholders

These are NOT leaks even though they pattern-match the absolute-path regex:

- `.claude/agents/sanitization-auditor.md` - contains `/Users/<user>/LocalDev/<private>/` as illustrative regex examples, with `<user>` and `<private>` as placeholders, not real values.
- `.claude/commands/sanitize.md` and `.claude/commands/audit.md` - same pattern.
- This file - same pattern.

## Block / warn distinction

- **Block** (exit non-zero in `pre-bash-sanitize.sh`): forbidden strings, real absolute paths into private repos, real secrets.
- **Warn** (stderr only): drift, missing optional frontmatter, suspicious-but-uncertain content. The user decides.

## Update protocol

The forbidden-strings wordlist is **not** stored in tracked files (that would defeat the purpose). It lives at:

```
.claude/.forbidden-strings.txt   (gitignored, per-installation)
```

The hook scripts (`pre-bash-sanitize.sh`, `session-start-status.sh`) and `/sanitize` command read this file at runtime. If the file is missing, sanitization gates degrade gracefully (warn, don't block).

When the user adds a new private term to forbid:
1. Add the term to `.claude/.forbidden-strings.txt`.
2. Update the user-level memory file at `~/.claude/projects/-Users-chika-LocalDev-SpecForge/memory/specforge_public_release.md` to record the term and rationale.
3. Run `/sanitize` to confirm no existing tracked file already contains the new term.
