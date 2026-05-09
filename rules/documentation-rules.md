# Documentation Rules

Standards for documentation across the project. See also [`agentic-docs/documentation-structure.md`](../agentic-docs/documentation-structure.md) for where new docs go.

## 1. Two-tier docs

- **Root context files** (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) stay short. They're loaded into every agent conversation; long files crowd out the user's actual question.
- **Deep references** live in `agentic-docs/`. The root files link out; the deep docs hold the substance.

See [`agentic-docs/two-tier-docs-pattern.md`](../agentic-docs/two-tier-docs-pattern.md).

## 2. Docs are first-class artifacts

A PR that changes user-facing behavior includes the doc update. A PR that adds a new endpoint includes the API doc. A PR that retires a feature includes the deprecation note.

"Docs follow next sprint" is technical debt that compounds.

## 3. Concise, structured, scannable

- Headings hierarchy: `#` for the title only; `##` for top-level sections; `###` for subsections. Don't go deeper than `####` without a structural reason.
- Tables for matrices and reference content.
- Fenced code blocks with language tags.
- Bulleted or numbered lists for sequences.
- Short paragraphs (2–4 sentences).

## 4. Cross-references resolve

Every link in tracked documentation points to a tracked file (or an external URL). Broken links are bugs.

The `/audit` command flags broken local links. Run before merging doc changes.

## 5. Frontmatter where the format requires it

| File type | Required frontmatter |
|---|---|
| Agent (`agents/examples/*.md`, `runtimes/.<vendor>/agents/*.md`) | `name`, `description`, `model`, `color` |
| Skill (`skills/<slug>/SKILL.md`) | `name`, `description`, `argument-hint`, `user-invocable`, `allowed-tools` |
| Claude command (`commands/<slug>.md`) | `description` |
| Cursor rule (`*.mdc`) | `description`, optionally `globs` and `alwaysApply` |
| Kiro steering (`*.md` under `.kiro/steering/`) | `inclusion: always` or `inclusion: fileMatch` + `fileMatchPattern` |

Missing required frontmatter = the runtime won't load the file. The PostToolUse frontmatter hook validates on save.

## 6. Match docs to the audience

| Audience | Where they read |
|---|---|
| Agents (Claude, Codex, Gemini) | Root context files (`AGENTS.md`, etc.) |
| Contributors (humans starting fresh) | `README.md`, `CONTRIBUTING.md`, `agentic-docs/philosophy.md`, `agentic-docs/spec-driven-development.md` |
| Implementers (working on a feature) | The feature's PRD + spec triplet |
| Reviewers | `rules/`, `code-review-rules.md`, the PR template |
| Operators | Runbooks (project-specific) and `workflows/` |

A doc trying to address every audience addresses none.

## 7. PRDs, specs, and ADRs are versioned

- PRDs include `Version`, `Date`, `Author`, `Status`.
- Specs include `Version`, `Date`, `Author`, `Status`, source PRD link.
- ADRs include `Status`, `Date`, `Deciders`. ADRs are immutable once accepted; corrections come via new ADRs.

Status is the gate. Documents without an explicit status are not actionable.

## 8. Templates over theory

When SpecForge ships a "template," it must produce a valid artifact when filled in. Theoretical templates fail review.

The `template-quality-reviewer` agent enforces this bar; see [`.claude/agents/template-quality-reviewer.md`](../.claude/agents/template-quality-reviewer.md).

## 9. TODO markers are intentional

- TODO marks where a real value will be inserted later (e.g. `Architecture Reference: TODO`).
- TODO is **not** a placeholder for missing thinking ("TODO: figure out what goes here").
- TODOs in tracked content should have a known resolver and a target date or PR.

## 10. Generic, non-proprietary samples

Sample PRDs, specs, agents, skills, and commands use generic domains:

- ✓ user notification preferences, file upload, audit log export, paginated search.
- ✗ portfolio rebalancing, financial trade execution, healthcare claims, legal filings.

Domain-specific examples leak business intent and constrain who can adopt the framework.

## 11. Doc currency is the spec author's job

When a feature's design changes, the design doc updates first; code follows. When a PRD's scope expands, the PRD updates first; spec triplet follows. Stale docs that contradict the code are worse than missing docs.

## See also

- [`agentic-docs/documentation-structure.md`](../agentic-docs/documentation-structure.md) - where new docs go.
- [`agentic-docs/two-tier-docs-pattern.md`](../agentic-docs/two-tier-docs-pattern.md) - root context vs deep references.
- [`engineering-rules.md`](engineering-rules.md) Rule 11 - doc currency.
