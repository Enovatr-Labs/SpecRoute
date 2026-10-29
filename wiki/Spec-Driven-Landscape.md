# Spec-Driven Landscape

<!-- sources: agentic-docs/spec-driven-landscape.md -->

SpecRoute is neither the first nor the only framework for spec-driven agentic development. This page maps the field — including one framework that starts from research rather than a spec — so you have what you need to decide what to adopt, including what you need to decide *against* SpecRoute.

Canonical source: [`agentic-docs/spec-driven-landscape.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/spec-driven-landscape.md).

## Scope and method

Five projects, selected by three different rules:

- **By adoption:** the three most-adopted open-source SDD projects on GitHub — spec-kit, OpenSpec, BMAD-METHOD.
- **As a vendor-native implementation:** Amazon Kiro, which SpecRoute already supports as a runtime target.
- **As an adjacent method, for contrast:** microsoft/hve-core, an agentic framework maintained by a platform vendor (Microsoft) that describes itself as "a highly opinionated agentic software development lifecycle (SDLC) framework" and that is research-first rather than spec-first. It was **not** selected by adoption and is not spec-driven; it is here because a reader weighing spec-first against research-first needs to see both.

Every claim is drawn from the project's own repository or from GitHub API metadata, and every number carries the command that regenerates it. Claims a project makes about itself that cannot be verified from its repository are attributed, not asserted.

This page does **not** benchmark the projects, score them on a feature matrix, or name a winner. A matrix built from SpecRoute's own taxonomy would score SpecRoute highest by construction — that is advocacy, not information.

## What the field is converging on

The interesting result is not that these projects differ. It is how much they independently agree. Where hve-core, the research-first contrast, departs from a point, the point says so.

1. **The artifact precedes the code, and the artifact is the review surface.** In the spec-driven projects, the diff becomes something you check *against* the spec rather than reason about from scratch. hve-core has no spec artifact: a plan precedes implementation and, by default, an independent critique, and is compared against the changes at review, but those working artifacts are not meant to be committed (point 5), so none of them travels with the branch the way a committed spec does.
2. **Explicit, named phases.** `/speckit.constitution → specify → plan → tasks → implement → converge` (spec-kit's README instructs repeating implement/converge until converge reports Converged) · `propose → apply → archive` (actions rather than ordered phases, per OpenSpec's docs) · requirements → design → tasks · PRD → spec triplet → tasks → implementation → validation · hve-core's research (when needed) → plan → implement → review, where its docs state "The critique runs by default and records `Pass`, `Revise`, or `Blocked` before implementation readiness" — a default, skippable step rather than a hard gate. The counts differ; the conviction that phases must be named and separated does not.
3. **A durable project-level layer, held apart from per-change work.** spec-kit's constitution, OpenSpec's `openspec/specs/`, Kiro's `steering/`, SpecRoute's `rules/` and `AGENTS.md`, hve-core's always-loaded `.github/copilot-instructions.md` plus `.instructions.md` files scoped by `applyTo`. Different names in every project, one idea: standing constraints must not be re-litigated inside every change.
4. **Settled work separated from in-flight work.** OpenSpec archives applied changes; SpecRoute has `prds/active|deprecated|archive`. Without it, a specs directory becomes an undated pile where current and abandoned intent look identical.
5. **Artifacts are plain Markdown in the repo, versioned with the code.** No spec-driven project in this set puts specs in an external tracker — though OpenSpec's stores beta pilots an exception to the *beside* part, not the *tracker* part: planning can be externalized into a separate standalone OpenSpec repo, still versioned Markdown. hve-core is the exception on versioning: its dated working files under `.copilot-tracking/` are "durable working state" per its tracking instructions, but its install guide says they "should not be committed to your repository", and its own `.gitignore` lists the directory.
6. **Agent roles are first-class files.** BMAD's named agents, each a skill that loads a persona, hve-core's `.github/agents/**/*.agent.md` (including non-user-invocable subagents), SpecRoute's [[Agents]], and every vendor's subagent format. A role in a file can be reviewed and versioned; one in a paste cannot.

**Not converged:** no shared file format (the artifacts are not interchangeable, and hve-core adds `.agent.md`, `.prompt.md`, and `.instructions.md` — though its skills follow the same `SKILL.md` shape from agentskills.io), no portability between frameworks (moving is a rewrite, not a migration), no agreement on whether working artifacts are committed, and hooks and commands remain vendor-shaped for every multi-tool project (hve-core targets Copilot alone, so it does not face that). The field agrees on the *shape* of spec-driven development and on almost none of the *format*.

## The comparison set

| Project | What it ships | Delivery | License | Artifacts live in | Phase model | Stars (verified 2026-10-05) |
|---|---|---|---|---|---|---|
| [github/spec-kit](https://github.com/github/spec-kit) | CLI + slash-command set | Python CLI | MIT | `.specify/` | `/speckit.constitution` → `specify` → `plan` → `tasks` → `implement` → `converge` (implement/converge loop) | 140,250 |
| [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | CLI + slash-command set | TypeScript CLI (npm or Homebrew, Node >= 20.19.0) | MIT | `openspec/specs/`, `openspec/changes/` | `propose` → `apply` → `archive` (happy path; docs say "actions, not phases") | 71,088 |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Agent persona library + module system | npm installer (`npx bmad-method install`, stable line); Skills CLI (`npx skills add`) or plugin marketplace (preview line) | Reported as `NOASSERTION`, displayed as "Other" | module-defined | full-lifecycle, module-defined | 53,808 |
| [Amazon Kiro](https://kiro.dev) | IDE with native SDD | Vendor product | Proprietary product | `.kiro/specs/` | requirements → design → tasks | n/a (not an OSS repo) |
| [microsoft/hve-core](https://github.com/microsoft/hve-core) | Agents, prompts, instructions, and skills for GitHub Copilot (not SDD) | Copilot CLI plugin + VS Code extension; no CLI of its own | MIT; some bundled skills carry Creative Commons licenses | `.copilot-tracking/` (gitignored working files) | `research` (when needed) → `plan` → `implement` → `review` (RPI) | 1,498 |
| **SpecRoute** | Templates, rules, agent definitions, runtime layouts | Content only — copy directories | Apache-2.0 | per-vendor runtime dirs | PRD → spec triplet → tasks → implementation → validation | n/a (this project) |

Regenerate the Stars and License columns:

```bash
# Reproduces every Stars and License cell above. Last run: 2026-10-05.
for r in github/spec-kit Fission-AI/OpenSpec bmad-code-org/BMAD-METHOD microsoft/hve-core; do
  gh api "repos/$r" --jq '"\(.full_name)\t\(.stargazers_count)\t\(.license.spdx_id // "NOASSERTION")"'
done
```

The command returns only the repository-level SPDX identifier; hve-core's per-skill licenses are not visible to it (see its licensing note).

Star counts measure attention, not fitness. They are recorded because they are why spec-kit, OpenSpec, and BMAD-METHOD are in the set rather than arbitrary repositories — not as a ranking. They are not why hve-core is here: it was included for contrast of method, so do not read its count against the others. The sections below are ordered by model-proximity to SpecRoute, which is more useful when you are choosing.

## What each project does well

### github/spec-kit

The most widely adopted of the set and the most complete end-to-end command sequence among the spec-driven CLIs here. Its commands are namespaced: `/speckit.constitution` establishes durable principles at `.specify/memory/constitution.md`; `/speckit.specify` captures intent; `/speckit.plan` produces the approach; `/speckit.tasks` decomposes it; `/speckit.implement` executes; `/speckit.converge` closes the loop, and spec-kit's README instructs repeating implement/converge until converge reports Converged. `/speckit.clarify` (spec-kit describes it as the rename of `/quizme`) before `plan`, `/speckit.checklist` after `plan`, and `/speckit.analyze` after `tasks` are documented as optional quality gates. Each step writes real files into `.specify/`, so the sequence is carried by the commands rather than operator discipline alone. In skills-mode installs the same commands render as `speckit-<name>` behind a per-agent invocation prefix, which is why spec-kit's command reference shows both forms side by side while its README now shows only the skills form. The Python CLI scaffolds a new project in minutes.

**Pick it when:** you want the canonical constitution-to-converge loop, installed and scaffolded by a command, with the largest community and the most examples to learn from.

### Fission-AI/OpenSpec

The clearest thinking about *change* as the unit of work among the spec-driven projects here. `openspec/specs/` holds what is true; `openspec/changes/` holds what is proposed, each change carrying its own `proposal.md`, `design.md`, and `tasks.md`. `/opsx:propose`, `/opsx:apply`, and `/opsx:archive` move a change through, and applied changes land in `openspec/changes/archive/`. The project describes the workflow itself as "actions, not phases" — the default profile is `propose`, `explore`, `apply`, `update`, `sync`, and `archive`, invocable in any order. That settled-versus-delta distinction is the sharpest among the spec-driven projects here — the spec never silently accumulates proposals nobody adopted. The project states that it works with 30+ AI assistants.

Install: `npm install -g @fission-ai/openspec@latest`, or `brew install openspec` on macOS and Linux (official formula). Node >= 20.19.0 either way, then `openspec init`.

**Pick it when:** you want change proposals to be first-class and separately reviewable.

### bmad-code-org/BMAD-METHOD

Agent identity is the organizing unit here, more than the command or the artifact. Its docs state that the BMad Method module installs five named agents — analyst, product manager, architect, developer, UX designer — each invoked as a skill that loads that persona, each carrying a menu of short codes that start a workflow without leaving the conversation. A team gets a working multi-role organization without designing one. BMAD-METHOD currently ships on two lines. The stable line installs through the project's own npm installer, `npx bmad-method install`. The preview line delivers the modules as individually selectable `bmad-*` skills, and its README warns of breaking changes between updates. Install the preview with `npx skills add bmad-code-org/BMAD-METHOD` plus the module record for each module you draw from — `bmod-method` (delivery workflows), `bmod-core-tools` (standalone skills) — or add the Claude Code or Codex plugin marketplace, where those two records are named `bmad-method` and `bmad-core-tools` instead.

**A licensing note you must act on:** the GitHub API reports the license as `NOASSERTION`, displayed as "Other". That is not a recognized SPDX identifier, so scanners and procurement policies keyed to SPDX will not resolve it. Its `LICENSE` file is the verbatim MIT text with a TRADEMARK NOTICE appended — which is what stops GitHub resolving an SPDX identifier — and its README carries a `License: MIT` badge. Read the repository's terms directly and clear them before adopting, rather than relying on the API's answer or the badge.

**Pick it when:** you want a maintained, opinionated multi-role agent organization out of the box, and you have confirmed the license terms are acceptable to you.

### Amazon Kiro — a vendor that is also a peer

Kiro is a supported SpecRoute vendor column *and* a competing methodology. It ships SDD natively: `.kiro/specs/` holds a requirements/design/tasks progression built into the IDE, with `.kiro/steering/` as its durable layer. That progression is no longer the only shape — its docs describe a bug-fix spec whose first artifact is `bugfix.md` rather than `requirements.md`, alongside shorter quick-spec and quick-plan entry points.

If Kiro is your only tool, its native path is shorter than any framework layered on top of it. SpecRoute supports Kiro because SpecRoute's contract is vendor neutrality — not because Kiro needs SpecRoute.

Kiro's runtime shape and hook taxonomy live in [[Agent CLI Integrations]] and [[Vendor Matrix]]; this page does not restate them.

### microsoft/hve-core — a research-first contrast

hve-core is not a spec-driven framework, and that is why it is here. It is built for GitHub Copilot only; its transparency note states: "HVE Core targets GitHub Copilot Chat in Visual Studio Code and GitHub Copilot CLI. Clients do not load every type of customization in the same way." It ships as a Copilot CLI plugin and a VS Code extension, plus a clone-based installer skill for selective copying, with no CLI of its own. SpecRoute does not support GitHub Copilot as a vendor.

Its method is "The RPI (Research, Plan, Implement, Review) lifecycle": task context and evidence, research when needed, plan, implement, review, follow-up. Research is optional — use `/rpi-research` "only when available evidence is not adequate" — and "Research is read-only." Specs are optional input, not a gate: `prd-builder` and `brd-builder` agents exist, and plans cite PRD/BRD/ADR/requirement identifiers when they exist.

- **Evidence files over conversation memory.** Phases write dated Markdown under `.copilot-tracking/`; its tracking instructions state "This file-based tracking takes precedence over memory: persist durable working state to the dated tracking artifact rather than relying on session, conversation, or working memory." The rationale, per its context-engineering docs: "The model doesn't forget the instructions. It deprioritizes them because more recent tokens receive disproportionate attention weight." The files persist across sessions but are not meant to be committed.
- **A default critique step and a split review verdict.** A plan passes an independent critique before implementation by default, but the critique can be skipped and its verdict is advisory — "confirmed user direction outranks critique advice" — and review is optional too: "Review is optional; skip it when you do not need an acceptance record." Where it runs: "Review keeps execution status (`Complete`, `Partial`, or `Blocked`) separate from outcome (`Conformant`, `Conformant with justified divergence`, `Defects found`, `Residual work`, or `Not accepted`)."
- **Upkeep automated in its own repository.** Schema-validated frontmatter on `.agent.md`, `.prompt.md`, `.instructions.md`, and `SKILL.md` files; eval suites under `evals/` in PR validation; a date-based freshness threshold enforced in PR validation.

Its README: "It is best treated as a source of patterns and learning rather than a stable platform, foundation, or production dependency."

**A licensing note you must act on:** the GitHub API reports MIT, but the README states "Most content in this repository is covered by the MIT License. Certain skill content derived from OWASP Foundation publications is licensed under CC BY-SA 4.0. Each affected skill identifies its license in frontmatter". Skill frontmatter also shows `CC-BY-4.0`, alone or in combined expressions that also pull in `CC-BY-SA-3.0`, `OGL-UK-3.0`, or `Apache-2.0`, on many skills, and `CC-BY-NC-SA-4.0` — non-commercial — on one (`.github/skills/security/owasp-docker/`). Most skills declare `MIT`, a minority declare Creative Commons terms, and some declare no `license:` field at all, falling back to the repository default the README describes. If you have a license policy, read each skill's frontmatter rather than treating the repository-level MIT identifier as covering every file.

**Pick it when:** your team works in GitHub Copilot and wants a research-first, evidence-tracked workflow with a broad collection of agents, prompts, instructions, and skills — and you are using it as patterns to learn from, as its own README advises.

## Where SpecRoute differs

Three real differences, each with what it costs.

**1. It is content, not a CLI.** No package to install, no `init`, no build step — you copy a runtime directory and edit it. Nothing to version-pin, nothing to upgrade, no tool between you and your files. The cost is equally real: nothing scaffolds the directories, and nothing enforces phase order except review and hooks you wire yourself. spec-kit and OpenSpec each ship a CLI, and BMAD-METHOD's stable line ships its own npm installer; for a team that wants the flow carried by a tool — commands that scaffold the directories and write each stage's files in sequence — that is a genuine advantage over SpecRoute. None of them advertises refusing out-of-order work; OpenSpec's own docs describe its workflow as "actions, not phases". hve-core has no CLI of its own either; it installs through a Copilot CLI plugin or a VS Code extension.

This is the current design, not a permanent commitment. A `specroute` CLI or extension remains an open, uncommitted item on the [[Roadmap]].

**2. Vendor neutrality is a written contract, not a support list.** The unit of support is a complete runtime layout in each vendor's *native* format, with the matrix mirrored byte-identically and a new vendor added as a column rather than a fork.

This is a different axis from peer breadth claims, and the two should not be confused. OpenSpec states it works with 30+ AI assistants — a claim about how many assistants can consume its output, and a broader number than six. SpecRoute's six is a claim about depth: each has a maintained layout in its own idiom. hve-core's roadmap frames it as "optimized GitHub Copilot customizations" — depth on a single platform. Breadth and depth are both legitimate; neither kind of claim is evidence about the other.

**3. The framework is built by the pattern it documents.** SpecRoute's own `.claude/` directory is a working [[Implementation Team]] that authors and audits the framework. That makes the claim checkable rather than aspirational — the artifacts are in the repository.

## When to pick a peer instead

- **You want a command to scaffold the files for you.** Use spec-kit or OpenSpec. SpecRoute makes you copy directories by hand.
- **You want change proposals held apart from the settled spec.** Use OpenSpec. Its `openspec/specs/` vs `openspec/changes/` split is the sharpest among the spec-driven projects here — though its own docs describe the workflow as "actions, not phases" rather than an enforced order, and SpecRoute's ordering is likewise convention upheld by review and hooks you configure.
- **You want a ready-made multi-role agent organization.** Use BMAD-METHOD, subject to the licensing check above. SpecRoute ships archetypes you are expected to adapt.
- **You are single-vendor on Kiro and content there.** Use `.kiro/specs/` natively. SpecRoute's vendor neutrality is overhead you would be paying for portability you are not using. Revisit if you add a second tool.
- **You work only in GitHub Copilot.** Look at hve-core. SpecRoute has no Copilot runtime layout; hve-core is built for Copilot Chat and the Copilot CLI.
- **You want opinionated defaults you do not have to think about.** Use spec-kit, OpenSpec, or BMAD-METHOD. SpecRoute assumes you will edit its templates; a team that will not edit them gets less from it.
- **Your policy requires a recognized SPDX license.** spec-kit and OpenSpec are MIT, SpecRoute is Apache-2.0; BMAD-METHOD needs a direct reading of its terms; hve-core is reported as MIT, but some bundled skills carry Creative Commons licenses, one non-commercial, so check per-skill frontmatter.
- **You are already succeeding with one of them.** None is a strict superset of another, and switching is a rewrite. A working practice is worth more than a better-matched framework.

## Using SpecRoute alongside a peer

- **A peer CLI as the producer, SpecRoute as the review layer.** Let spec-kit or OpenSpec generate and sequence the artifacts; use SpecRoute's [[Rules]], agent roster, and [[Sanitization]] hooks as the standards those artifacts are reviewed against. The CLI sequences the artifacts; the rules govern their content.
- **Kiro's storage, SpecRoute's content.** Keep specs in `.kiro/specs/` where the IDE expects them, and use SpecRoute's [[Specs]] templates as what goes in them.
- **A peer for the flow, SpecRoute for the second vendor.** A team on spec-kit that adds a tool spec-kit does not target can cover it with a SpecRoute runtime layout without disturbing the existing flow.

## How these numbers stay honest

Every third-party number and license here is regenerable by the command above and stamped with the date it was last run — the same discipline [[Multi-Agent Orchestration]] applies to roster counts: ship the command that produces the number next to the number, and record when it was verified.

Two rules keep the page from rotting quietly:

- **Raw numbers appear in the table only, never in prose.** There is exactly one place to refresh.
- **Refreshing means re-running the command**, not editing digits from memory. A number without a reproduction is a rumor with a decimal point.

Third-party facts — star counts, SPDX identifiers, per-file licenses, command names, phase vocabularies — are the fastest-rotting claims in the repository, because they change without anything in the repository changing.

## See also

- [[Philosophy]] — why SpecRoute is content rather than an application
- [[Spec-Driven Development]] — the SpecRoute flow this page situates
- [[Agent CLI Integrations]] · [[Vendor Matrix]] — per-vendor wiring, including Kiro
- [[Roadmap]] — non-goals, and the open question of a `specroute` CLI
