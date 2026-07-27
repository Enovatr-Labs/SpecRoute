# Changelog

All notable changes to SpecRoute are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

For a content-only framework, versions are interpreted as:

- **MAJOR** - breaking change to artifact contracts (frontmatter, spec triplet shape, vendor matrix structure, the spec-driven flow itself).
- **MINOR** - new vendor support, new artifact type, new skill/command/hook category, substantive new templates.
- **PATCH** - doc fixes, sanitization, link corrections, typography, content refinements.

---

## [Unreleased]

(Changes accumulating since v0.4.0 will be listed here.)

---

## [0.4.0] - 2026-07-27

**Multi-agent orchestration, and a currency cycle that found real defects.** This release adds the `all-hands` orchestration pattern across every runtime, and corrects a set of claims that had drifted from - or never matched - what the vendors actually do. Several were functional, not cosmetic: the sanitization gate this framework advertises was not firing, and one shipped template carried a model value no runtime accepts.

Vendor facts in this release were verified against official documentation and, where docs were inconsistent, against installed vendor binaries. That method is now written down as a repeatable cycle.

### Added

- **`all-hands` multi-agent orchestration.** A coordinator skill that triages a work item, fans it out across the relevant agents in parallel waves, synthesizes their output, runs the validation gates, and reports. Shipped in all six runtime layouts (`runtimes/.<vendor>/skills/all-hands/`), each with its own vendor-correct frontmatter and a shared body kept in sync by `tools/sync-skills.py`. Consumer template at `skills/examples/all-hands/`.
- `agentic-docs/multi-agent-orchestration.md` and `wiki/Multi-Agent-Orchestration.md` - the six mechanisms a working orchestrator needs, and what breaks when each is missing. Framed as a **composition** of the existing four primitives, not a fifth primitive.
- `docs-currency-auditor` agent - owns vendor facts, version anchors, transition dates, and cross-mirror consistency. Produces evidence-backed findings; does not write the prose.
- `doc-currency-check` skill - the currency cycle in executable form, encoding the specific rot classes that have bitten this repo.
- `tools/sync-hooks-to-settings.sh` - merges the annotated `hooks.json` source of truth into `settings.json`, with JSON validation, refusal to overwrite an invalid destination, and idempotency.
- Tracked `.claude/settings.json`, which `CLAUDE.md` had documented but which did not exist.
- `runtimes/mcp/render/render_devin.py` and `runtimes/.devin/config.template.json` - six renderers now emit from `runtimes/mcp/servers.yaml`.
- **Hook layouts in every runtime.** `runtimes/.codex/`, `.gemini/`, `.cursor/`, and `.devin/` now ship hooks in their vendor's native shape, plus a new top-level `hooks/devin/` reference. All six layouts now deliver the hook support they advertise. Gemini is the shape exception: its hooks live inside the generated `.gemini/settings.json`, so the layout ships a documented merge-in snippet rather than a standalone config.

### Fixed

- **Hooks never fired.** Claude Code executes hooks from `settings.json`; a project-level `.claude/hooks/hooks.json` is read only for plugins. This repo's own sanitization gate, the consumer template, and the worked example all shipped inert hooks while `CLAUDE.md` described a hook block as "a hard stop". All three are now wired through `settings.json` and the fix was verified by observing the hook actually run.
- **`model: flagship` was written into live agent files.** `flagship`/`balanced`/`fast` are SpecRoute's vendor-neutral tier abstractions; no runtime accepts them. Nine shipped agent files carried one. Real files now carry real values; tiers are confined to roster tables, with a per-vendor mapping in `wiki/Agents.md`. The frontmatter hook now flags a tier name used as a model value.
- **Kiro's hook format was retired.** Kiro IDE 1.0 (2026-06-25) replaced `*.kiro.hook` with `.kiro/hooks/<name>.json` v1; 0.x hooks do not execute until migrated. Examples migrated, trigger vocabulary updated, migration guidance added.
- **Agent and skill frontmatter contracts were wrong in both directions.** Only `name` and `description` are required; `model` and `color` are optional. `internet: Yes|No` was documented as a contract field but is not one - removed, with web access now expressed through `tools`. Roughly eleven real optional fields were undocumented.
- **`allowed-tools` was described as a restriction.** It *pre-approves* tools for the invoking turn; `disallowed-tools` is what removes them. The previous framing gave a false sense of confinement.
- **A fabricated standard was cited.** A claimed "150-line instruction budget" from the Agentic AI Foundation does not exist - the `AGENTS.md` standard specifies no schema and no length limit. The Linux Foundation stewardship is real and is now stated accurately; the length target is labelled as SpecRoute's own convention.
- **The capability table over-claimed.** It conflated "the vendor supports this" with "SpecRoute ships a runtime layout for this". Those are now distinct claims.
- `agentic-docs/agentic-coding-model.md`'s vendor section predated the v0.3.0 convergence and contradicted the matrix in four places.
- **Codex hook facts.** v0.3.0 recorded 10 events; there are **11** (`SessionEnd` was missing), confirmed against both `codex-cli` 0.145.0 and the official docs. Codex reuses Claude Code's event names verbatim, but the overlap is close rather than total: no `PostToolUseFailure`, and only `type: "command"` handlers execute. Hooks are **enabled by default**, and the canonical `[features]` key is `hooks` with `codex_hooks` as a deprecated alias - an intermediate draft of this release wrongly retracted that as unverifiable, on the strength of a grep that could not prove the negative. Corrected against the vendor documentation.
- **Kiro hook templates would not have loaded.** The root `version` field is the string `"v1"`, not the integer `1` - all four shipped example hooks carried the integer, and two migration tables instructed readers to convert *toward* it. Kiro IDE 1.0 also has **10** triggers, not 11: `Manual` was retired in favour of manual steering files, and one shipped example used it. Both fixed and verified against `kiro.dev/docs/hooks/`.
- MCP renderers declared a `pyyaml` dependency they never used, and the Gemini and Codex renderers silently dropped `requires_env`, omitting required environment wiring from the generated configs. All six now round-trip byte-identically against their committed templates.
- `/audit` checked the wrong files for matrix consistency and used a glob that matched nothing for Codex agents; `/sanitize` could not detect flattened project paths, which was the one path leak actually present.
- Maintainer home-directory paths removed from tracked files; `.claude/agent-memory/` notes regenerated against disk after marking 21 existing files as "TODO".
- The SessionStart banner and `/status` reported a phantom missing `docs/` directory, renamed to `agentic-docs/` long ago.
- **The sanitization gate could not see the files most likely to leak.** `/sanitize` and `pre-bash-sanitize.sh` both scanned via `git grep`, which reads **tracked content only** - so a commit that *adds* a leaking file passed cleanly, and new content is exactly what leaks. 49 of this release's own files were invisible to it. Both now scan tracked plus untracked-but-not-ignored paths, verified by planting a canary in a new file and confirming the gate blocks. (The first attempt at this fix was itself broken: `xargs` returns 123 when any `grep` batch finds nothing, so an exit-status guard swallowed real hits.)
- Three inconsistencies caught by a post-implementation audit pass: `hooks/cursor/hooks.template.json` claimed 19 lifecycle events while wiring 18 against a documented 21 (now states the count and why the Tab/workspace hooks are omitted); `wiki/Frontmatter-Contracts.md`'s intro still asserted the pre-correction "missing fields = won't register" rule that its own corrected body contradicts; and `.claude/agent-memory/runtime-architect/vendor-matrix-progress.md` still carried an in-flight banner and a pre-hooks capability snapshot.
- **`all-hands` did not register as a skill at all.** Its frontmatter carried `disable-model-invocation: true`, which removes a skill from the model-facing registry that Claude Code's `@` mention picker completes against - so `@all-hands` returned only directories and no `Skill` row, and the skill looked broken while being structurally valid. Its tool list also named `Task`, which was superseded by `Agent`. The Claude copy now uses the documented space-separated `allowed-tools` scalar, while every runtime keeps only its native frontmatter. The portable body documents each runtime's dispatch mechanism without claiming Claude's `subagent_type` is universal.
- **Cursor hook path resolution was documented two contradictory ways.** `hooks/cursor/scripts/README.md` said paths resolve relative to `hooks.json`'s parent; the runtime README said project root. Cursor's docs settle it: **project** hooks resolve from the project root (`.cursor/hooks/scripts/x.sh`), **user** hooks from `~/.cursor/` (`./hooks/scripts/x.sh`). The shipped configs were already correct - only the reference doc was wrong. This mattered because the `beforeShellExecution` gate sets `failClosed: true`, so an unresolvable path exits 127 and blocks every shell command rather than failing quietly.
- **`$ARGUMENTS` now degrades gracefully.** All six `all-hands` bodies are byte-identical by design, so a per-vendor substitution token cannot be expressed - but only Claude Code and Codex expand `$ARGUMENTS`. The body now tells the coordinator what to do when it reads the literal token instead of a work item.
- **Kiro shipped one hook where every sibling ships three**, with no stated reason, and its hooks README was the only one without a Setup section. It now ships the same session-start / sanitization-gate / frontmatter-check trio, plus setup steps that assert the scripts exist rather than only that the config parses.
- **The `wiki-parity` CI gate was inert.** It captured `$?` after a pipeline, which is `tee`'s status, not the script's - so `exit_code` was pinned to 0 and both the staleness-annotation and hard-break-failure steps were unreachable. Now uses `PIPESTATUS[0]`.
- **`/audit`'s vendor-matrix check could not detect cell-level drift** - it compared only row count and the set of runtime-dir tokens, so a changed cell passed silently. It now hashes the extracted matrix block (table plus footnotes) across all four mirrors and reports the differing file, line and column. The four blocks are byte-identical.
- `agentic-docs/agent-memory.md` named a real file inside a maintainer's private user-level memory directory. Replaced with a derivation command; the elided path form had slipped past the string-level scan.
- `runtimes/.claude/settings.local.template.json` was **invalid JSON** - an object entry inside an array - so any consumer copying it got settings that silently failed to load.
- Five wiki mirrors reconciled against their sources, including a claim that a `runtimes/.codex/hooks/pre-bash-sanitize.json` template shipped when no such file existed in either location.
- Three agents with populated memory directories never declared `memory: project` (four agents now declare it, including the new `docs-currency-auditor`).

### Changed

- Counts and version anchors reconciled across the repo: 12 implementation agents, 6 contributor skills, 6 runtime layouts, 6 MCP renderers.
- `.cursorrules` downgraded from "legacy, still supported" to removed in practice.
- The product is documented under its current **Devin Desktop** name. The `.devin/` runtime now targets Devin Local; Cascade's remaining `.windsurf` paths are documented only as compatibility paths within the same product.
- Hook documentation states plainly that hook taxonomies have **not** converged. Claude Code, Codex, Kiro, and Devin Local share several event names, but payload and decision schemas still differ. Skills, not hooks, are the near-total convergence point.

### Known gaps

- `.agents/skills/` is emerging as a vendor-neutral skills location (confirmed present in an installed Codex 0.145.0 binary as a repo-level skills root, alongside a still-working `.codex/skills`). Documented, but SpecRoute has not migrated to it, and the ecosystem has not settled.
- Codex hooks are documented as enabled by default; `[features] hooks` is canonical and `codex_hooks` is a deprecated alias.
- Cascade remains available inside Devin Desktop, but SpecRoute no longer ships it as a separate runtime. Projects still using Cascade may retain its documented `.windsurf/workflows/`, `.windsurf/hooks.json`, and user-level MCP compatibility paths while migrating reusable procedures to skills.

---

## [0.3.0] - 2026-06-29

**Vendor capability convergence.** All six supported tools now back the full capability set (skills, agents, commands, hooks, MCP) with real runtime templates - previously several vendors were rules/steering-only. The vendor docs and tooling were re-verified current against each vendor's mid-2026 releases (the vendor-doc currency cycle from the Phase 4 roadmap).

### Added

- An early `runtimes/.devin/` layout for **Devin Desktop**. Its agents and skills remain; v0.4.0 later replaced the unsupported workflow, hook, and MCP path assumptions with Devin Local's documented `.devin/` contracts.
- Skills, subagents, and command templates for Gemini CLI, Kiro, Cursor, and the then-Windsurf-branded Desktop product - each in the vendor's native shape as understood at that release.
- Codex hooks wiring and a standalone `.codex/agents/<name>.toml` subagent example.
- MCP renderers `render_kiro.py`, `render_cursor.py`, and the historical `render_windsurf.py` - six renderers emitted from the single source `runtimes/mcp/servers.yaml`. v0.4.0 replaced the latter with `render_devin.py`.
- Per-vendor rule files `rules/kiro-rules.md` and `rules/devin-rules.md`.
- A `review-spec` worked-example command, mirrored across vendors in each native shape.

### Changed

- `tools/sync-skills.py` rewritten to be **body-aware**: it syncs the `SKILL.md` body across all six vendors while preserving each vendor's distinct frontmatter contract. Agents are no longer synced - their formats diverge (Codex TOML, Devin `AGENT.md` directories).
- Codex agents are standalone TOML (`name` / `description` / `developer_instructions`), not Claude's flat Markdown - the matrix and `sync-skills.py` reflect this.
- Gemini commands migrated from the obsolete `gemini_cli_config.json` shell-command map to `.gemini/commands/*.toml` prompt templates.
- Claude MCP template renamed `claude_desktop_config.template.json` → `mcp.template.json`; it renders to the Claude Code CLI's `.mcp.json` (project) / `~/.claude.json` (user), which is distinct from the Claude **Desktop app's** `claude_desktop_config.json`. Earlier docs conflated the two.
- Vendor matrix and supporting docs reconciled to the convergence model: capability tiers (Full / Near-full / Partial / Rules-only) retired; "three vendors consume MCP" corrected to all six (two emit shapes - JSON for everyone except Codex's TOML).

### Fixed

- Hook event counts re-verified against official vendor docs and corrected repo-wide: Claude Code **~30** (was ~27/~31), Codex **10** and enabled by default (`hooks` feature; `codex_hooks` is a deprecated alias), Cursor **~21** (was ~19).
- Gemini `SKILL.md` frontmatter corrected to the Agent Skills open-standard `name` / `description` only (Claude-specific `user-invocable` / `argument-hint` / `allowed-tools` removed).
- Removed a hardcoded local filesystem path from `wiki/README.md` (sanitization).
- Fixed a broken cross-reference link in `runtimes/.cursor/agents/README.md`.

---

## [0.2.4] - 2026-05-19

### Fixed

- `CITATION.cff` `version` and `date-released` fields advanced from `0.2.1` / `2026-05-14` to the current release. The field had been left stale during the v0.2.3 cut and was caught in the post-flip pre-publication review.
- `ROADMAP.md` and `wiki/Home.md` / `wiki/Roadmap.md` "Current version" lines synchronized to the current release. Phase 4 release-history bullets in both `ROADMAP.md` and `wiki/Roadmap.md` updated to reflect the v0.2.0 / v0.2.1 retraction and the v0.2.3 → v0.2.4 path.

---

## [0.2.3] - 2026-05-19

First publicly available release. Supersedes the withdrawn v0.2.0 (2026-05-11) and v0.2.1 (2026-05-14) entries below; the shipping content is unchanged from v0.2.1.

### Security

- Repository history sanitized end-to-end prior to public flip. A second-pass commit-message rewrite scrubbed a residual reference to the upstream private codebase that was reintroduced (while *describing* the prior sanitization) in the release-promotion commits behind v0.2.0 and v0.2.1. File content, authorship, and authorship timestamps are unchanged; only message bodies in the rewritten chain differ.
- The repository was additionally recreated from the clean local state to drop GitHub-preserved `refs/pull/*/head` refs that retained the tainted commits out-of-band of the rewrite. The pre-recreate repository is retained privately as `Enovatr-Labs/SpecRoute-archive`.
- The v0.2.0, v0.2.1, and v0.2.2 tag names were consumed during this process and are permanently reserved org-wide by the immutable-releases feature; v0.2.3 is therefore the equivalent shipping artifact for what would have been v0.2.1.

---

## 0.2.1 — 2026-05-14 *(withdrawn during pre-public sanitization; superseded by v0.2.3)*

### Changed

- Project renamed from SpecForge to SpecRoute. The original name collided with another existing GitHub project; the repo now lives at [`Enovatr-Labs/SpecRoute`](https://github.com/Enovatr-Labs/SpecRoute). GitHub maintains an automatic redirect from the old `Enovatr-Labs/SpecForge` URL, so existing clones and links continue to resolve.

---

## 0.2.0 — 2026-05-11 *(withdrawn during pre-public sanitization; superseded by v0.2.3)*

First public release. v0.1.0 was tagged privately as the launch milestone; v0.2.0 is what appears on the public landing page on day one of public visibility, with the wiki and GitHub-side hygiene infrastructure in place.

### Added

#### Documentation surface

- `wiki/` directory: 42 GitHub Wiki pages (Home, Quickstart, Vendor-Matrix, Repository-Structure, all artifact types - PRDs/Specs/Agents/Skills/Commands/Hooks/Prompts/Rules - all five workflows, all conceptual docs - Philosophy/Spec-Driven-Development/Agentic-Coding-Model/Automation-Decision-Framework/Documentation-Structure/Two-Tier-Docs-Pattern/Multi-Vendor-Context-Files/Agent-CLI-Integrations/Cross-Vendor-Sync/Agent-Memory - plus FAQ, Glossary, Maintainers, Security, Code-of-Conduct, Roadmap, Worked-Example, Contributing, Frontmatter-Contracts, Implementation-Team, MCP-Integration, Sanitization, Adding-a-Vendor) plus `_Sidebar.md` and `_Footer.md` navigation.
- `scripts/sync-wiki.sh` - local-run wrapper for manual wiki publishing.
- `tools/wiki-parity.py` - PR-time check for missing source files referenced by `<!-- sources: ... -->` manifests, broken gollum `[[wiki-links]]`, and staleness (wiki page summary older than its declared source).

#### GitHub-side repository hygiene

- `CODEOWNERS` - default owner plus explicit ownership for sanitization infrastructure, hooks, vendor-matrix sources, release infrastructure, `agentic-docs/`, `examples/`, `.github/`.
- `.github/PULL_REQUEST_TEMPLATE.md` - enforces SemVer change-type declaration, spec/ADR/issue link, validation checklist, vendor-neutrality gate.
- `.github/ISSUE_TEMPLATE/bug_report.yml` - content-bug-shaped form (file path, expected behavior, version/commit).
- `.github/ISSUE_TEMPLATE/feature_request.yml` - categorized form (new vendor / artifact / skill / etc.) with vendor-neutrality dropdown.
- `.github/ISSUE_TEMPLATE/config.yml` - routes security issues to private advisories, questions to Discussions; disables blank issues.
- `.github/dependabot.yml` - weekly GitHub Actions update PRs targeting develop.
- `.github/workflows/links.yml` - lychee link-check on every PR, scheduled weekly cron, auto-issue on scheduled failures.
- `.github/workflows/sync-wiki.yml` - mirrors `wiki/` → `<repo>.wiki.git` on push to main touching `wiki/**`.
- `.github/workflows/wiki-parity.yml` - read-only PR check via `tools/wiki-parity.py`.
- `.lycheeignore` - link-check exclusion patterns (placeholder hosts, local-only hosts, anchor links).

### Changed

- Branch model: dropped `staging` tier. develop → main is now the only flow; nothing deploys from SpecRoute, so the previous develop → staging → main chain added friction without signal.
- Action versions (Node24 runtime bumps for GitHub-org maintained actions): `actions/cache@v4` → `v5`, `actions/checkout@v4` → `v6`, `peter-evans/create-issue-from-file@v5` → `v6`. No API/behavior changes affect our workflows.
- `.github/workflows/links.yml` - lychee runs on every PR regardless of which files changed (was filtered to markdown only). Prevents non-markdown PRs from deadlocking against the required-status-check gate.

### Fixed

- 10 pre-existing broken markdown links surfaced by the first lychee CI run on a PR:
  - `agentic-docs/two-tier-docs-pattern.md` - `docs/<topic>.md` placeholder converted from a markdown link to inline code (was being resolved as a real path).
  - `examples/sample-project/prompts/phase3_validation/019_feature_flag.md` - `/users` placeholder converted to inline code.
  - `CONTRIBUTING.md` - `../../issues` and `../../pulls` (only resolve on github.com, not in lychee's local-file scan) replaced with full URLs.
  - `specs/templates/{design,requirements,tasks}-template.md` - triplet self-references that referenced `requirements.md` / `design.md` / `tasks.md` (the post-rename target names users adopt after copying the templates) converted from markdown links to inline code.
- `agentic-docs/multi-vendor-context-files.md` - one occurrence of `[AGENTS.md](AGENTS.md)` on line 48 used a sibling-relative path from inside `agentic-docs/`; corrected to `[AGENTS.md](../AGENTS.md)` (line 88 already had this right).
- `.github/ISSUE_TEMPLATE/bug_report.yml` - version/commit placeholder updated from a stale SHA reference to a generic version string after the history rewrite (see Security).
- `CHANGELOG.md` v0.1.0 entry - prompt-file count corrected from "28" to "29" (the math: 1 global master + 4 phase masters + 22 numbered task prompts + 2 runtime operational prompts).

### Security

- Three repository rulesets configured (`main-ruleset`, `develop-ruleset`, `release-tags-ruleset`):
  - `main-ruleset` - require PR + 1 Code Owner approval + linear history + squash-only merges + lychee status check; force-push and deletion blocked; `bypass_actors` carries the maintainer with `bypass_mode: pull_request` to resolve the solo-maintainer self-approval deadlock.
  - `develop-ruleset` - same shape with 0 approvals required and no Code Owner requirement.
  - `release-tags-ruleset` - locks `v*` tags from update and deletion once created.
- Repository history sanitized: one commit message body containing a reference to the upstream private codebase from which SpecRoute was extracted was rewritten before public flip. The rewrite preserves all file content and authorship; only the message paragraph in that one commit changed. The `v0.1.0` tag and release object were retargeted to the rewritten commit chain.
- Sanitization infrastructure validated end-to-end on real-world push attempts: PreToolUse `pre-bash-sanitize.sh` hook + gitignored `.claude/.forbidden-strings.txt` wordlist + `/sanitize` command + `sanitization-auditor` agent.

[Unreleased]: https://github.com/Enovatr-Labs/SpecRoute/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/Enovatr-Labs/SpecRoute/releases/tag/v0.4.0
[0.3.0]: https://github.com/Enovatr-Labs/SpecRoute/releases/tag/v0.3.0
[0.2.4]: https://github.com/Enovatr-Labs/SpecRoute/releases/tag/v0.2.4
[0.2.3]: https://github.com/Enovatr-Labs/SpecRoute/releases/tag/v0.2.3

---

## [0.1.0] - 2026-05-09

Initial public release. Phases 1-3 of the roadmap complete; Phase 4 (maturity) in progress.

### Added

#### Framework foundation

- Repository skeleton, root files (`README.md`, `LICENSE`, `.gitignore`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ROADMAP.md`).
- Canonical vendor-neutral context: `AGENTS.md`. Per-vendor delegation shims: `CLAUDE.md`, `GEMINI.md`.
- Two-tier docs pattern: short root context + deep references in `agentic-docs/` (10 conceptual docs).
- Implementation team in `.claude/`: 11 author agents, 4 contributor skills, 4 slash commands, 3 hooks, agent-memory directories.
- Sanitization infrastructure: `.claude/.forbidden-strings.txt` (gitignored, per-installation); PreToolUse hook gates `git commit` / `git push` / `gh pr create` / `gh release create`.

#### Artifact templates

- PRDs: full 23-section enterprise template, lightweight alternative, platform SRS.
- Specs: triplet (`requirements-template.md` + `design-template.md` + `tasks-template.md`) with stable IDs and back-reference contract; lightweight feature-spec template; technical-spec template; ADR template.
- Agents: `agent-template.md` with frontmatter contract; 7 archetypes (product, architect, backend, frontend, security, qa, devops); `roster.md` for cross-vendor inventory.
- Skills: `skill-template/SKILL.md` (folder-per-skill convention).
- Commands: per-vendor templates (Claude markdown + Gemini JSON).
- Hooks: comprehensive coverage across all six vendors as understood at that release (Claude Code 30 events with 5 hook types; Codex 10 events; Gemini 11 events; Kiro 10 events; Cursor ~21 events; the then-Windsurf-branded Desktop product's Cascade agent with 12 events). Devin Local's v1 hook contract replaced the last integration in v0.4.0.
- Prompts: master/phase/task production-grade trio + per-vendor sets for Claude and Codex + shared utility prompts (prd-to-spec, spec-to-tasks, code-review).

#### Runtime layouts

- Six per-vendor runtime layouts. The initial Desktop integration used a `.windsurf/` compatibility layout; v0.4.0 removed it in favor of the single current `.devin/` runtime.
- MCP single-source-of-truth: `runtimes/mcp/servers.yaml` + working Python renderers for Claude, Codex, Gemini.
- `tools/sync-skills.py` — cross-runtime skill / agent diff and copy.

#### Workflows and rules

- 5 workflow playbooks: `prd-to-production.md`, `spec-to-implementation.md`, `agent-review-loop.md`, `testing-and-validation.md`, `release-readiness.md`.
- Vendor-neutral rules: engineering, code-review, security, documentation.
- Per-vendor rule surfacing for Codex, Claude, Gemini, Cursor, and the then-current Desktop branding; the latter moved to `rules/devin-rules.md` in v0.3.0.
- Steering templates (always-on vs file-pattern-matched).

#### Worked example

- `examples/sample-project/` - drop-in runnable, Claude-Code-only.
  - PRD (full 23-section, `prds/active/user-search.md`).
  - Spec triplet (`specs/user-search/{requirements,design,tasks}.md`) with 11 stable-ID requirements + 11 NFRs + full coverage table.
  - 5 ADRs (`adrs/`): Postgres indexed scans, cursor pagination, Redis cache TTL, HMAC-signed cursors, filter-set hash logging.
  - 7 project-specific deep references (`agentic-docs/`).
  - 29 prompt files: 1 global master + 4 phase masters + 22 numbered task prompts + 2 runtime operational prompts.
  - 8 implementation-team agents in `.claude/agents/`.
  - 4 slash commands, 3 hooks, agent-memory directory.
  - Self-contained: copy folder, rename `.template` files, open Claude Code, run `prompts/runtime/pickup-next-task.md`.

#### Documentation and attribution

- 10-file `agentic-docs/` framework reference (philosophy, spec-driven-development, agentic-coding-model, automation-decision-framework, documentation-structure, two-tier-docs-pattern, multi-vendor-context-files, agent-cli-integrations, cross-vendor-sync, agent-memory).
- `MAINTAINERS.md` with current-maintainer table, how-to-reach-us decision matrix, sponsoring-org context, becoming-a-maintainer process, decision-making conventions.
- README sections for Maintainers and Citation.
- `CITATION.cff` (CFF v1.2.0) - GitHub renders a "Cite this repository" button.

### Conventions established

- Vendor-neutrality matrix as the contract: adding a new vendor is a new column, not a fork.
- Sanitization-by-design: gitignored wordlist + runtime hook gate + `/sanitize` command + `sanitization-auditor` agent.
- Two-tier docs pattern: `AGENTS.md` (~100 lines max) + per-vendor delegation shims (~30-50 lines) + `agentic-docs/` deep references.
- Frontmatter contracts as load-bearing: agents, skills, commands all have required-field contracts; the PostToolUse hook validates on save.
- Spec-driven flow: PRD → spec triplet (with stable IDs) → numbered tasks (with back-refs) → phased prompts (with current/target diff blocks) → implementation → validation → review.

[0.1.0]: https://github.com/Enovatr-Labs/SpecRoute/releases/tag/v0.1.0
