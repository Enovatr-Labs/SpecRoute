# Runtime Architect - Vendor Matrix Progress

Tracks the build-out state of each supported vendor runtime. Update this note
whenever a `runtimes/.<vendor>/` layout, MCP renderer, or cross-runtime sync rule
changes.

**Verified against the working tree on 2026-07-27.**

Treat the commands below as truth. Snapshots age quickly, and untracked files are
part of the working implementation even though `git ls-files` cannot see them.

## Runtime identity

SpecRoute supports six vendor identities and six runtime layouts:

```text
claude  codex  gemini  kiro  cursor  devin
```

Devin Desktop is one product identity. The `.devin/` runtime is for Devin Local.
Cascade compatibility namespaces such as `.windsurf/workflows/`,
`.windsurf/hooks.json`, and `~/.codeium/windsurf/mcp_config.json` may still appear
in product documentation, but they are not a seventh SpecRoute vendor or runtime.
Do not recreate `runtimes/.windsurf/`.

The consumer-facing matrix is mirrored byte-identically in `README.md`,
`AGENTS.md`, `wiki/Vendor-Matrix.md`, and
`agentic-docs/agent-cli-integrations.md`. `/audit` hashes the table. Supporting
vendor notes live in the integration reference and dedicated wiki page.

## Regenerate capability inventory

```bash
for v in claude codex gemini kiro cursor devin; do
  printf '%-9s' "$v"
  for d in skills agents commands hooks rules steering workflows scripts settings; do
    [ -d "runtimes/.$v/$d" ] && printf ' %s' "$d"
  done
  echo
done
```

A directory in that output is a measured repository fact, not proof that the
vendor supports or lacks a capability. Verify vendor behavior independently.

Devin Local uses these project paths:

- `.devin/skills/<slug>/SKILL.md`
- `.devin/agents/<name>/AGENT.md` for experimental subagents
- `.devin/hooks.v1.json`
- `.devin/config.json` with `mcpServers`
- `.devin/rules/*.md` for rule content also consumed by Devin Desktop

Do not infer `.devin/workflows/`, `.devin/hooks.json`, or `.devin/mcp.json`.

## Regenerate artifact counts

```bash
for v in claude codex gemini kiro cursor devin; do
  printf '%-9s skills=%s\n' "$v" \
    "$(find "runtimes/.$v/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')"
done

find runtimes/.claude/agents runtimes/.gemini/agents \
     runtimes/.kiro/agents runtimes/.cursor/agents \
     -maxdepth 1 -type f -name '*.md' ! -name README.md -print 2>/dev/null
find runtimes/.codex/agents -maxdepth 1 -type f -name '*.toml' -print 2>/dev/null
find runtimes/.devin/agents -mindepth 2 -maxdepth 2 -type f -name AGENT.md -print 2>/dev/null
```

Uniform counts are not a goal by themselves. Missing artifacts are defects only
when the matrix or runtime README promises that SpecRoute ships them.

## MCP single source of truth

`runtimes/mcp/servers.yaml` is canonical. There should be one renderer per
supported vendor:

```bash
find runtimes/mcp/render -maxdepth 1 -type f -name 'render_*.py' -print | sort
git status --short runtimes/mcp/ runtimes/.devin/
```

Expected renderer/output mapping:

| Renderer | Output |
|---|---|
| `render_claude.py` | `runtimes/.claude/mcp.template.json` |
| `render_codex.py` | `runtimes/.codex/config.template.toml` |
| `render_gemini.py` | `runtimes/.gemini/settings.template.json` |
| `render_kiro.py` | `runtimes/.kiro/settings/mcp.template.json` |
| `render_cursor.py` | `runtimes/.cursor/mcp.template.json` |
| `render_devin.py` | `runtimes/.devin/config.template.json` |

Install the Devin output as `.devin/config.json`. Personal values belong in the
gitignored `.devin/config.local.json`.

## Cross-runtime skill sync

`tools/sync-skills.py` must target the same six runtime slugs:

```bash
rg -n 'SKILL_VENDORS' tools/sync-skills.py
python3 tools/sync-skills.py --dry-run
```

The tool synchronizes skill bodies while preserving vendor frontmatter. Agents
are intentionally not file-synced because their native formats diverge.

`.agents/skills/` is separate: it mirrors this repository's contributor skills
from `.claude/skills/`, not consumer runtime examples. `/parity` checks those
bodies independently.

## Historical context

An earlier implementation modeled the former product name as a separate
`runtimes/.windsurf/` compatibility layout and therefore reported seven layouts
and seven renderers. That model was removed on 2026-07-27 to keep one Devin
Desktop identity. Preserve compatibility path facts where the product still uses
them, but do not restore a separate vendor row, sync target, renderer, or runtime.

## Open checks

- Confirm the six runtime directories and six renderers after every structural
  change; do not copy a count from this note.
- Re-run `/audit`, `/parity`, `python3 tools/wiki-parity.py`, and the private
  provenance gate before release.
- Keep the Devin Local paths above aligned with its shipped CLI/runtime contract;
  keep Cascade compatibility claims explicitly labeled as Cascade.
