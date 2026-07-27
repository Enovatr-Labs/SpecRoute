# Framework Docs Author - Docs Status

Tracks which documentation files exist, which are still unwritten, and which need refresh after structural changes.

**Verified against disk on 2026-07-27.**

Two rounds of correction are baked into this file. An earlier version carried 21 phantom `TODO` markers for files that were already drafted, inflating the `/status` count. The version after that used `git ls-files`, which is **tracked-only** - so it silently missed every newly authored file until it was staged, which is precisely when a docs inventory is least useful. The commands below list tracked **and** untracked files. Re-run them before trusting any row.

## Regenerate the inventory

```bash
# Prose docs: top-level, agentic-docs/, workflows/. Includes untracked files.
git ls-files --cached --others --exclude-standard -- '*.md' \
  | grep -E '^[^/]+\.md$|^agentic-docs/|^workflows/' | sort

# Wiki pages (published separately; mirrors much of the above).
git ls-files --cached --others --exclude-standard -- 'wiki/*.md' | sort

# What is new since the last verification (authored but not yet staged).
git ls-files --others --exclude-standard -- '*.md' \
  | grep -E '^[^/]+\.md$|^agentic-docs/|^workflows/|^wiki/' | sort

# What has been deleted (tracked, but gone from the worktree).
git ls-files --deleted -- '*.md'

# Per-file size, to catch stubs masquerading as drafts.
for f in agentic-docs/*.md workflows/*.md; do
  printf '%-52s %5s lines\n' "$f" "$(wc -l < "$f" | tr -d ' ')"
done
```

Counts at verification: **10** top-level, **11** `agentic-docs/`, **6** `workflows/` (5 workflows + index), **46** `wiki/` pages. Nothing tracked has been deleted - `git ls-files --deleted` returned empty.

## Document inventory

### Top-level context files

| File | Status | Notes |
|---|---|---|
| `README.md` | drafted | Vendor matrix, artifact taxonomy, getting-started, repo structure. Refresh when matrix changes. |
| `AGENTS.md` | drafted | Canonical vendor-neutral context file. Single source of truth root. |
| `CLAUDE.md` | drafted | Short root shim; delegates intent to `AGENTS.md`. |
| `GEMINI.md` | drafted | Delegation shim → `AGENTS.md`. |
| `CONTRIBUTING.md` | drafted | Contribution workflow + quality bar. |
| `CODE_OF_CONDUCT.md` | drafted | Contributor Covenant. |
| `SECURITY.md` | drafted | Reporting channel + threat model (malicious shell in hook templates, supply-chain via `tools/`). |
| `ROADMAP.md` | drafted | Phased roadmap: skeleton → worked example + runtimes → community contributions. |
| `MAINTAINERS.md` | drafted | Maintainer list and review ownership. |
| `CHANGELOG.md` | drafted | Release history. Refresh on every release. |

### `agentic-docs/` deep references

All **eleven** are drafted - the count moved from ten on 2026-07-27. The directory is `agentic-docs/`, **not** `docs/`; anything still checking for a top-level `docs/` is stale.

| File | Status | Notes |
|---|---|---|
| `philosophy.md` | drafted | Why spec-driven. |
| `spec-driven-development.md` | drafted | PRD → triplet → tasks flow. |
| `agentic-coding-model.md` | drafted | How artifacts compose. |
| `automation-decision-framework.md` | drafted | Skill vs Agent vs Command vs Hook matrix. Most cross-referenced doc. |
| `documentation-structure.md` | drafted | Where new docs go. |
| `two-tier-docs-pattern.md` | drafted | Short root + namespaced reference. |
| `multi-vendor-context-files.md` | drafted | `AGENTS.md` + delegation shims. |
| `agent-cli-integrations.md` | drafted | How to wire SpecRoute into each vendor CLI. Carries a vendor-matrix mirror. |
| `cross-vendor-sync.md` | drafted | Owned jointly with `runtime-architect`. |
| `agent-memory.md` | drafted | Per-agent persistent context. |
| `multi-agent-orchestration.md` | drafted, **untracked** | New on 2026-07-27. Not yet staged, so tracked-only inventories miss it. |

### `workflows/`

All five workflows plus the index are drafted: `README.md`, `prd-to-production.md`, `spec-to-implementation.md`, `agent-review-loop.md`, `testing-and-validation.md`, `release-readiness.md`. No additions or deletions since the last verification.

### `wiki/`

46 pages. The wiki is a mirror layer, not a separate authorship surface - most pages restate an `agentic-docs/` or top-level file and link back to it. Only the pairing needs tracking here:

- `wiki/Multi-Agent-Orchestration.md` - **untracked**, new on 2026-07-27, the wiki counterpart of `agentic-docs/multi-agent-orchestration.md`. Already linked from `wiki/_Sidebar.md`.
- `wiki/Vendor-Matrix.md` - one of the four byte-identical vendor-matrix mirrors. `/audit` step 3 hashes the block; do not hand-edit one mirror.
- `wiki/Agent-CLI-Integrations.md` - a wiki stub that points at `[[Vendor Matrix]]` rather than restating the table. It is deliberately **not** a fifth mirror.

## Outstanding work

Drafting is complete; the remaining work is recurring currency verification, not authorship.

1. Keep the vendor matrix byte-identical across `README.md`, `AGENTS.md`, `wiki/Vendor-Matrix.md`, and `agentic-docs/agent-cli-integrations.md` - they drift first. `/audit` step 3 compares a `sha256` of the block (rows **and** footnotes) and names the offending file and cell. Note `agentic-docs/multi-vendor-context-files.md` is **not** a mirror.
2. Re-verify `agentic-docs/cross-vendor-sync.md` against `tools/sync-skills.py` whenever the tool changes.
3. Confirm capability claims against vendor documentation and inventory claims against `runtimes/.<vendor>/`; do not infer one from the other.

Resolved in the 2026-07-27 review:

- `multi-agent-orchestration.md` is linked from `README.md`, `agentic-docs/documentation-structure.md`, and the wiki sidebar.
- The docs now use one Devin Desktop vendor identity and one `render_devin.py`
  renderer for Devin Local's `.devin/config.json`; Cascade compatibility paths
  are labeled as product namespaces rather than a separate runtime.

## Refresh triggers

- **Matrix change** (new vendor or new column): refresh all four mirrors in lock-step, then `README.md` prose and `multi-vendor-context-files.md`.
- **New artifact type** (a new top-level dir under SpecRoute): refresh `agentic-coding-model.md`, `automation-decision-framework.md`, and the README's artifact taxonomy.
- **New deep reference under `agentic-docs/`**: add it to `documentation-structure.md`, the README, the wiki mirror, and `wiki/_Sidebar.md` in the same change. Item 1 above is what skipping this looks like.
- **Frontmatter contract change** (new required field on agent/skill/command): refresh the corresponding template README and any docs that quote the contract.
- **Any edit to this file**: re-run the commands above and update the "Verified against disk" date. A status written from memory is worse than no status.
