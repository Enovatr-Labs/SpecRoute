# CLAUDE.md

@AGENTS.md

Claude Code delegation shim for SpecRoute. `AGENTS.md` is the canonical,
vendor-neutral source of truth; do not duplicate its contracts here.

Repository implementation assets live in `.claude/`. Consumer-facing Claude
Code templates live in `runtimes/.claude/`.

Project hook wiring executes from `.claude/settings.json`; after editing the
annotated `.claude/hooks/hooks.json`, run
`tools/sync-hooks-to-settings.sh --check` to verify parity.
