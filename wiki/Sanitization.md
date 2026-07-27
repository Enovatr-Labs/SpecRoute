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

Four layers:

### 1. Wordlist + PreToolUse hook

`.claude/.forbidden-strings.txt` (**gitignored**) holds one forbidden term per line. The PreToolUse hook `.claude/hooks/pre-bash-sanitize.sh` runs `git grep` against this list before allowing:

- `git commit`
- `git push`
- `gh pr create`
- `gh release create`

The gate scans the working tree plus untracked-not-ignored files, the staged index, and the outgoing commit range for publish operations. This closes the three common bypasses: a new untracked file, a staged version that differs from the working tree, and an older local commit being pushed later. If any forbidden term matches, the hook **exits 2** and the action is blocked. Treat this as a hard stop — generalize the source content; do not bypass.

**Where the gate is wired.** The script lives in `.claude/hooks/`, but Claude Code executes hooks from the `hooks` key of `.claude/settings.json` — *not* from a project-level `.claude/hooks/hooks.json`. That filename is a hook source only inside a **plugin**; in a plain project it is inert. SpecRoute keeps `.claude/hooks/hooks.json` as the annotated authoring artifact (JSON can't carry comments, so the `_comment_*` keys live there) and merges its `hooks` key into `settings.json` with `tools/sync-hooks-to-settings.sh`; `--check` reports drift without writing. A sanitization gate parked in `hooks.json` alone never fires, and nothing warns you.

The gate matches the whole `Bash` tool rather than being narrowed with a per-hook `"if"` condition. Narrowing a *publish gate* trades a loud failure for a silent hole — a pattern that stops matching disables the gate with no signal. The script's own `case` statement exits 0 immediately for non-publish commands, so the wide matcher costs one short-lived subprocess.

### 2. Private-source provenance audit

`tools/provenance-audit.py` compares the public working tree — and, with `--history`, every reachable public Git blob — against locally configured private source repositories. It detects forbidden identifiers, normalized exact fragments, high-overlap prose/code blocks, and matching 40-token runs. Reports name only the public target location and a hash; they never print private source paths or excerpts.

The source list and reviewed-hash allowlist are gitignored. Configure them locally in `.claude/.provenance-sources.txt` and `.claude/.provenance-allowlist.txt`, then run the documented `--history` release gate. A finding requires human review; renaming identifiers is not sufficient if distinctive business rules, schemas, prose, prompts, or workflow structure remain.

### 3. `/sanitize` slash command

Quick string-level scan. Reports findings as a punch list without blocking. Use during authoring, not just at commit time.

### 4. `/audit` slash command

Comprehensive pre-commit sweep including sanitization plus frontmatter, vendor-matrix consistency, broken links, and TODO health. Run before any commit.

For a deeper logic-level review (catches things string-matching misses, like generalized patterns that still leak intent), invoke the `sanitization-auditor` agent.

## Per-installation wordlist (gitignored on purpose)

`.claude/.forbidden-strings.txt` is **gitignored**. The framework should never carry a permanent record of what it was extracted from. Each installation maintains its own wordlist locally.

The publish gate verifies both conditions: the wordlist must match `.gitignore`, and it must not already be tracked in the index. This prevents a combined `git add && git commit` command from publishing the private identifiers the gate itself relies on.

Maintainers repopulate the wordlist from their own user-level memory directory. Derive the path rather than hard-coding it — Claude Code flattens the project path by replacing `/` with `-`, giving `~/.claude/projects/<flattened-project-path>/memory/`:

```bash
echo "$HOME/.claude/projects/$(git rev-parse --show-toplevel | tr '/' '-')/memory"
```

Never commit that path, its contents, or the filenames inside it. A tracked file naming a maintainer's home directory is itself a small leak — and so is a tracked file naming a *file* inside that directory, since the filename discloses what the repo was extracted from. The `/sanitize` path check flags both the `/Users/<name>/` and the flattened `-Users-<name>-` forms; use `<flattened-project-path>` style placeholders in prose.

## When sanitization fires

The hook blocks at `PreToolUse` for the four commit/publish operations. It does **not** fire on:

- `Write` / `Edit` (those use the PostToolUse frontmatter hook instead).
- Local commands that don't publish (`git status`, `git diff`).
- Test runs.

This keeps the inner loop fast while still gating the moment when content leaves the local machine.

## What to do when blocked

1. Read the hook's stderr output — it names the forbidden term(s).
2. Find the offending line(s) in the public target named by the report. Do not paste private-source excerpts into an issue or PR.
3. **Generalize the content.** Replace specific names with placeholders, paths with relative ones, business logic with generic patterns.
4. Stage the fix; retry the commit.

**Do not** add the forbidden term to an ignore list to bypass the check. The check is the contract.

## Cross-vendor note

The sanitization infrastructure currently lives in `.claude/` (the implementation team's runtime). It applies to **all tracked content**, regardless of which vendor authored the content.

Consumers running another CLI as their primary get the same gate from the per-vendor templates under `hooks/<vendor>/`. For Codex, `hooks/codex/hooks.template.json` wires a `PreToolUse` matcher on `Bash|^apply_patch$` to a `pre-tool-sanitize.sh` script; drop it in as `.codex/hooks.json` or merge it as an inline `[hooks]` table in `.codex/config.toml`. Every vendor needs its own registration — hook *bodies* port across vendors, hook *wiring* does not. See [[Hooks]].

## Owner agent

Sanitization is owned by the `sanitization-auditor` agent. See [[Implementation Team]].

## See also

- [[Hooks]] — the hook mechanism in detail
- [[Security]] — the broader threat model (sanitization is one slice)
- [[Implementation Team]] — `/sanitize`, `/audit`, `sanitization-auditor` agent
- [[Contributing]] — what contributors must run before opening a PR
