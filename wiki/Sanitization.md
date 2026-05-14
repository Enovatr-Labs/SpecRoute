# Sanitization

<!-- sources: CLAUDE.md, hooks/README.md -->

SpecRoute is open-source and is generalized from internal codebases. **Patterns generalize freely; product names, customer data, and proprietary domain logic do not.** Sanitization is the framework's hard contract.

## What sanitization covers

Forbidden in any tracked file:

- Private project / product / company names that aren't the public consumer-facing brand.
- Customer data — names, emails, IDs, account numbers.
- Internal absolute paths (`/Users/<name>/...`, `/srv/internal/...`).
- Proprietary domain logic (specific financial / medical / legal business rules that aren't generalized).
- Credentials, API keys, tokens, secrets.
- Internal endpoints and infra URLs.
- Names of private internal products or services.

Allowed (generalize first):

- Generic patterns and architectures (e.g. "a job that reads a queue and writes to Postgres").
- Generic data models (e.g. `users`, `orders`, `products`).
- Open-source library names and public infrastructure (Postgres, Redis, AWS, Kubernetes — these are fine).
- The public name of the project itself (SpecRoute, Enovatr Labs).

## How sanitization is enforced

Three layers:

### 1. Wordlist + PreToolUse hook

`.claude/.forbidden-strings.txt` (**gitignored**) holds one forbidden term per line. The PreToolUse hook `.claude/hooks/pre-bash-sanitize.sh` runs `git grep` against this list before allowing:

- `git commit`
- `git push`
- `gh pr create`
- `gh release create`

If any forbidden term matches in tracked content, the hook **exits non-zero** and the action is blocked. Treat this as a hard stop — generalize the source content; do not bypass.

### 2. `/sanitize` slash command

Quick string-level scan. Reports findings as a punch list without blocking. Use during authoring, not just at commit time.

### 3. `/audit` slash command

Comprehensive pre-commit sweep including sanitization plus frontmatter, vendor-matrix consistency, broken links, and TODO health. Run before any commit.

For a deeper logic-level review (catches things string-matching misses, like generalized patterns that still leak intent), invoke the `sanitization-auditor` agent.

## Per-installation wordlist (gitignored on purpose)

`.claude/.forbidden-strings.txt` is **gitignored**. The framework should never carry a permanent record of what it was extracted from. Each installation maintains its own wordlist locally.

For SpecRoute maintainers, the wordlist is repopulated from user-level memory at `~/.claude/projects/-Users-chika-LocalDev-SpecRoute/memory/specroute_public_release.md` when needed.

## When sanitization fires

The hook blocks at `PreToolUse` for the four commit/publish operations. It does **not** fire on:

- `Write` / `Edit` (those use the PostToolUse frontmatter hook instead).
- Local commands that don't publish (`git status`, `git diff`).
- Test runs.

This keeps the inner loop fast while still gating the moment when content leaves the local machine.

## What to do when blocked

1. Read the hook's stderr output — it names the forbidden term(s).
2. Find the offending line(s) with `git grep "<term>"`.
3. **Generalize the content.** Replace specific names with placeholders, paths with relative ones, business logic with generic patterns.
4. Stage the fix; retry the commit.

**Do not** add the forbidden term to an ignore list to bypass the check. The check is the contract.

## Cross-vendor note

The sanitization infrastructure currently lives in `.claude/` (the implementation team's runtime). It applies to **all tracked content**, regardless of which vendor authored the content. A `runtimes/.codex/hooks/pre-bash-sanitize.json` template ships under `hooks/codex/` for consumers who run Codex as their primary CLI.

## Owner agent

Sanitization is owned by the `sanitization-auditor` agent. See [[Implementation Team]].

## See also

- [[Hooks]] — the hook mechanism in detail
- [[Security]] — the broader threat model (sanitization is one slice)
- [[Implementation Team]] — `/sanitize`, `/audit`, `sanitization-auditor` agent
- [[Contributing]] — what contributors must run before opening a PR
