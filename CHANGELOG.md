# Changelog

All notable changes to SpecRoute are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

For a content-only framework, versions are interpreted as:

- **MAJOR** - breaking change to artifact contracts (frontmatter, spec triplet shape, vendor matrix structure, the spec-driven flow itself).
- **MINOR** - new vendor support, new artifact type, new skill/command/hook category, substantive new templates.
- **PATCH** - doc fixes, sanitization, link corrections, typography, content refinements.

---

## [Unreleased]

(Changes accumulating since v0.2.1 will be listed here.)

---

## [0.2.1] - 2026-05-14

### Changed

- Project renamed from SpecForge to SpecRoute. The original name collided with another existing GitHub project; the repo now lives at [`Enovatr-Labs/SpecRoute`](https://github.com/Enovatr-Labs/SpecRoute). GitHub maintains an automatic redirect from the old `Enovatr-Labs/SpecForge` URL, so existing clones and links continue to resolve.

---

## [0.2.0] - 2026-05-11

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

[Unreleased]: https://github.com/Enovatr-Labs/SpecRoute/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/Enovatr-Labs/SpecRoute/releases/tag/v0.2.1
[0.2.0]: https://github.com/Enovatr-Labs/SpecRoute/releases/tag/v0.2.0

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
- Hooks: comprehensive coverage across all six vendors (Claude Code ~27 events with 5 hook types; Codex 6 events; Gemini 11 events; Kiro 10 events; Cursor ~19 events; Windsurf 12 events).
- Prompts: master/phase/task production-grade trio + per-vendor sets for Claude and Codex + shared utility prompts (prd-to-spec, spec-to-tasks, code-review).

#### Runtime layouts

- Per-vendor `runtimes/.claude/`, `runtimes/.codex/`, `runtimes/.gemini/`, `runtimes/.kiro/`, `runtimes/.cursor/`, `runtimes/.windsurf/` — copy-pasteable into consumer repos.
- MCP single-source-of-truth: `runtimes/mcp/servers.yaml` + working Python renderers for Claude, Codex, Gemini.
- `tools/sync-skills.py` — cross-runtime skill / agent diff and copy.

#### Workflows and rules

- 5 workflow playbooks: `prd-to-production.md`, `spec-to-implementation.md`, `agent-review-loop.md`, `testing-and-validation.md`, `release-readiness.md`.
- Vendor-neutral rules: engineering, code-review, security, documentation.
- Per-vendor rule surfacing: codex, claude, gemini, cursor, windsurf.
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
