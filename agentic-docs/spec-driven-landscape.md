# The Spec-Driven Landscape

SpecRoute is neither the first nor the only framework for spec-driven agentic development. Several projects reached similar conclusions independently, some have been adopted at a scale SpecRoute has not, and at least one agentic workflow framework starts from research rather than from a spec. This page maps that field so a reader deciding what to adopt has what they need to decide - including what they need to decide *against* SpecRoute.

## Scope and method

The comparison set is five projects, selected by three different rules:

- **By adoption:** the three most-adopted open-source spec-driven-development projects on GitHub - spec-kit, OpenSpec, and BMAD-METHOD.
- **As a vendor-native implementation:** Amazon Kiro, which SpecRoute already supports as a runtime target.
- **As an adjacent method, for contrast:** microsoft/hve-core, an agentic framework maintained by a platform vendor (Microsoft) that describes itself as "a highly opinionated agentic software development lifecycle (SDLC) framework" and that is research-first rather than spec-first. It was **not** selected by adoption and is not a spec-driven framework; it is here because a reader weighing spec-first against research-first needs to see both.

Every factual claim here is drawn from the project's own repository or from GitHub API metadata, and every number carries the command that regenerates it (see [The comparison set](#the-comparison-set)). Where a project makes a claim about itself that cannot be independently verified from its repository, it is attributed to that project rather than asserted.

This page deliberately does **not**:

- Benchmark the projects or rank them by quality. No such measurement exists that would survive scrutiny.
- Score them on a feature matrix. A matrix built from SpecRoute's own artifact taxonomy would score SpecRoute highest by construction, which makes it advocacy, not information.
- Recommend a single winner. The projects in this set are shaped by different constraints, and the right choice depends on constraints this page cannot see.

## What the field is converging on

The interesting result is not that these projects differ - it is how much they independently agree. Where hve-core, the research-first contrast, departs from a point, the point says so.

**1. A written artifact precedes code, and the artifact is the review surface.** The spec-driven projects in this set treat the specification, not the diff, as the thing a human reads carefully. The diff becomes something you check *against* the spec rather than reason about from scratch. This is the shared premise; everything else is mechanism. hve-core has no spec artifact: in its flow a plan precedes implementation and, by default, an independent critique, and its review compares the changes against that plan and the task's requirements. But those working artifacts, the review log included, are not meant to be committed (see point 5), so none of them travels with the branch the way a committed spec does.

**2. Explicit, named phases.** spec-kit runs `/speckit.constitution -> specify -> plan -> tasks -> implement -> converge`, and its README instructs repeating implement/converge until convergence reports Converged. OpenSpec runs `propose -> apply -> archive`, though its docs describe these as actions rather than ordered phases. Kiro runs requirements -> design -> tasks. SpecRoute runs PRD -> spec triplet -> tasks -> implementation -> validation. hve-core runs research (when needed) -> plan -> implement -> review, and its docs state that "The critique runs by default and records `Pass`, `Revise`, or `Blocked` before implementation readiness" - a default, skippable step rather than a hard gate. The phase counts differ; the conviction that phases must be *named and separated* rather than blurred into one prompt does not.

**3. A durable project-level layer, held apart from per-change work.** spec-kit keeps a constitution at `.specify/memory/constitution.md`. OpenSpec separates `openspec/specs/` (what is true) from `openspec/changes/` (what is being changed). Kiro has `steering/`. SpecRoute has `rules/` and `AGENTS.md`. hve-core relies on GitHub Copilot's `.github/copilot-instructions.md`, which is always loaded, and `.instructions.md` files that declare the file patterns they apply to with `applyTo` in frontmatter. Different names in every project, one idea: standing constraints must not be re-litigated inside every change.

**4. Settled work is separated from in-flight work.** OpenSpec makes this most explicit - an applied change is moved to `openspec/changes/archive/`. SpecRoute's `prds/active/`, `prds/deprecated/`, and `prds/archive/` express the same lifecycle. Without it, a specs directory becomes an undated pile in which current intent and abandoned intent look identical.

**5. Artifacts live in the repository as plain Markdown, versioned with the code.** `.specify/`, `openspec/`, `.kiro/specs/`, and SpecRoute's runtime directories are all directories of Markdown committed beside the source. No spec-driven project in this set puts specs in an external tracker. OpenSpec is piloting an exception to the *beside* part but not the *tracker* part: its stores beta lets a repo externalize planning into a separate standalone OpenSpec repo, which is still versioned Markdown rather than a tracker. The specification is expected to move with the branch, review with the PR, and be diffable.

hve-core is the exception on versioning. Its working artifacts are dated Markdown files under `.copilot-tracking/` - research, plan, plan critique, changes, and review log - and its tracking instructions call them "durable working state" that takes precedence over session memory. But its install guide says of these files that they "should not be committed to your repository", and its own `.gitignore` lists the directory. They are durable across sessions; they are not versioned with the code.

**6. Agent roles are first-class files, not prompt fragments.** BMAD-METHOD ships named agents as skills, each of which loads a persona. hve-core ships roles as `.github/agents/**/*.agent.md` files, including subagents that are not user-invocable. SpecRoute ships `agents/`. All six vendors in the [vendor matrix](agent-cli-integrations.md) now ship a subagent file format. A role that lives in a file can be reviewed, versioned, and reused; one that lives in a paste cannot.

### What the field has *not* converged on

- **No shared file format.** A spec-kit `spec.md`, an OpenSpec `proposal.md`, a Kiro `requirements.md`, and a SpecRoute requirements document are not interchangeable, and hve-core adds its own `.agent.md`, `.prompt.md`, and `.instructions.md` shapes. There is no `AGENTS.md`-equivalent standard for the specification itself. The one shape that does travel is `SKILL.md`: hve-core's skills follow agentskills.io, the same convergence SpecRoute records across its six vendors.
- **No portability between frameworks.** Adopting one is a commitment; moving between them is a rewrite, not a migration.
- **No agreement on whether working artifacts are committed.** The spec-driven projects named in point 5 commit them; hve-core's install guide says not to.
- **Automation surfaces remain vendor-shaped.** Hooks and commands differ per tool in event names, schema, and file location. The multi-tool projects in this set inherit that fragmentation and none has solved it; hve-core targets GitHub Copilot alone, so it does not face it.

The honest summary of the state of the art: the field agrees on the *shape* of spec-driven development and agrees on almost none of the *format*.

## The comparison set

| Project | What it ships | Delivery | License | Artifacts live in | Phase model | Stars (verified 2026-10-05) |
|---|---|---|---|---|---|---|
| [github/spec-kit](https://github.com/github/spec-kit) | CLI + slash-command set | Python CLI | MIT | `.specify/` | `/speckit.constitution` -> `specify` -> `plan` -> `tasks` -> `implement` -> `converge` (implement/converge loop) | 140,250 |
| [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | CLI + slash-command set | TypeScript CLI (npm or Homebrew, Node >= 20.19.0) | MIT | `openspec/specs/`, `openspec/changes/` | `propose` -> `apply` -> `archive` (happy path; docs say "actions, not phases") | 71,088 |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Agent persona library + module system | npm installer (`npx bmad-method install`, stable line); Skills CLI (`npx skills add`) or plugin marketplace (preview line) | Reported as `NOASSERTION`, displayed as "Other" | module-defined | full-lifecycle, module-defined | 53,808 |
| [Amazon Kiro](https://kiro.dev) | IDE with native SDD | Vendor product | Proprietary product | `.kiro/specs/` | requirements -> design -> tasks | n/a (not an OSS repo) |
| [microsoft/hve-core](https://github.com/microsoft/hve-core) | Agents, prompts, instructions, and skills for GitHub Copilot (not SDD) | Copilot CLI plugin + VS Code extension; no CLI of its own | MIT; some bundled skills carry Creative Commons licenses | `.copilot-tracking/` (gitignored working files) | `research` (when needed) -> `plan` -> `implement` -> `review` (RPI) | 1,498 |
| **SpecRoute** | Templates, rules, agent definitions, runtime layouts | Content only - copy directories | Apache-2.0 | per-vendor runtime dirs | PRD -> spec triplet -> tasks -> implementation -> validation | n/a (this project) |

Regenerate the Stars and License columns:

```bash
# Reproduces every Stars and License cell above. Last run: 2026-10-05.
for r in github/spec-kit Fission-AI/OpenSpec bmad-code-org/BMAD-METHOD microsoft/hve-core; do
  gh api "repos/$r" --jq '"\(.full_name)\t\(.stargazers_count)\t\(.license.spdx_id // "NOASSERTION")"'
done
```

The command returns only the repository-level SPDX identifier. hve-core's per-skill licenses are not visible to it; see the licensing note in its section.

Star counts measure attention, not fitness. They are recorded here because they are the reason spec-kit, OpenSpec, and BMAD-METHOD are in the comparison set rather than arbitrary repositories - not as a ranking. They are not the reason hve-core is here: it was included for contrast of method, and its count should not be read against the spec-driven projects' counts. The sections below are ordered by how close each project's model is to SpecRoute's, which is a more useful ordering for a reader making a choice.

## What each project does well

### github/spec-kit

The most widely adopted of the set, and the most complete end-to-end command sequence among the spec-driven CLIs here. Its commands are namespaced: `/speckit.constitution` establishes durable project principles at `.specify/memory/constitution.md`; `/speckit.specify` captures intent; `/speckit.plan` produces the technical approach; `/speckit.tasks` decomposes it; `/speckit.implement` executes; and `/speckit.converge` closes the loop - spec-kit's README instructs repeating implement/converge until converge reports Converged. Three commands are documented as optional quality gates and sit in the gaps: `/speckit.clarify` (spec-kit describes it as the rename of `/quizme`) before `plan`, `/speckit.checklist` after `plan`, and `/speckit.analyze` after `tasks`. Each step is a real command that writes real files into `.specify/`, so the sequence is carried by the commands rather than by the operator's discipline alone - in skills-mode installs the same commands render as `speckit-<name>` behind a per-agent invocation prefix, which is why spec-kit's command reference carries both forms side by side while its README now shows only the skills form. The Python CLI installs and scaffolds for you, which means a new project is running the full flow in minutes rather than after a directory-copying session.

**Pick it when:** you want the canonical constitution-to-converge loop, installed and scaffolded by a command, with the largest community and the most examples to learn from.

### Fission-AI/OpenSpec

The clearest thinking about *change* as the unit of work among the spec-driven projects here. `openspec/specs/` holds what is currently true; `openspec/changes/` holds what is being proposed, each change carrying its own `proposal.md`, `design.md`, and `tasks.md`. `/opsx:propose`, `/opsx:apply`, and `/opsx:archive` move a change through its lifecycle, and applied changes land in `openspec/changes/archive/`. The project describes the workflow itself as "actions, not phases" - the default profile is `propose`, `explore`, `apply`, `update`, `sync`, and `archive`, invocable in any order. The distinction between the settled spec and the in-flight delta is the sharpest among the spec-driven projects here - it means the specification does not silently accumulate proposals that were never adopted. The project states that it works with 30+ AI assistants.

Installation is `npm install -g @fission-ai/openspec@latest` or, on macOS and Linux, the official Homebrew formula (`brew install openspec`); either way Node >= 20.19.0 is required, and `openspec init` follows.

**Pick it when:** you want change proposals to be first-class and separately reviewable.

### bmad-code-org/BMAD-METHOD

Agent identity is the organizing unit here, more than the command or the artifact. Its documentation states that the BMad Method module installs five named agents - analyst, product manager, architect, developer, and UX designer - each invoked as a skill that loads that persona, and each carrying a menu of short codes that start a workflow without leaving the conversation. A team gets a working multi-role organization without designing one. BMAD-METHOD currently ships on two lines. The stable line installs through the project's own npm installer, `npx bmad-method install`. The preview line delivers the modules as individually selectable `bmad-*` skills; its README warns of breaking changes between updates. Install the preview with `npx skills add bmad-code-org/BMAD-METHOD`, adding the module record for each module you draw from - `bmod-method` for the delivery workflows, `bmod-core-tools` for the standalone skills - or add the Claude Code or Codex plugin marketplace, where those two records are named `bmad-method` and `bmad-core-tools` instead.

**A licensing note you must act on:** the GitHub API reports BMAD-METHOD's license as `NOASSERTION`, which GitHub displays as "Other". That is not a recognized SPDX identifier, so automated license scanners and procurement policies keyed to SPDX will not resolve it. The repository's `LICENSE` file is the verbatim MIT text with a TRADEMARK NOTICE appended, which is what stops GitHub resolving an SPDX identifier, and its README carries a `License: MIT` badge. If your organization has a license policy, read the repository's license terms directly and clear them before adopting rather than relying on the API's answer or the badge.

**Pick it when:** you want a maintained, opinionated multi-role agent organization out of the box, and you have confirmed the license terms are acceptable to you.

### Amazon Kiro - a vendor that is also a peer

Kiro occupies an unusual position: it is a **supported SpecRoute vendor column** and *also* a competing methodology. It ships spec-driven development natively - `.kiro/specs/` holds a requirements/design/tasks progression built into the IDE, with `.kiro/steering/` as its durable project layer. That progression is no longer the only shape: its docs describe a bug-fix spec whose first artifact is `bugfix.md` rather than `requirements.md`, alongside shorter quick-spec and quick-plan entry points.

If Kiro is your only tool, its native path is shorter than any framework layered on top of it. The specs are already where the IDE expects them, the flow is already wired, and there is nothing to copy. SpecRoute supports Kiro because SpecRoute's contract is vendor neutrality, not because Kiro needs SpecRoute.

Kiro's runtime shape, config surfaces, and hook taxonomy are documented in [`agent-cli-integrations.md`](agent-cli-integrations.md); this page does not restate the vendor matrix.

### microsoft/hve-core - a research-first contrast

hve-core is not a spec-driven framework, and that is why it is on this page. It is built for GitHub Copilot only; its transparency note states: "HVE Core targets GitHub Copilot Chat in Visual Studio Code and GitHub Copilot CLI. Clients do not load every type of customization in the same way." It ships as a Copilot CLI plugin and a VS Code extension, plus a clone-based installer skill for copying selected components. It has no CLI of its own. SpecRoute does not support GitHub Copilot as a vendor, so the two do not share a runtime target.

Its method is what its docs call "The RPI (Research, Plan, Implement, Review) lifecycle": task context and evidence, research when needed, plan, implement, review, follow-up. Research is optional - the docs say to use `/rpi-research` "only when available evidence is not adequate" - and "Research is read-only." A spec is an optional input rather than a gate: separate `prd-builder` and `brd-builder` agents exist, and RPI plans cite PRD, BRD, ADR, and requirement identifiers when they exist.

What it does distinctively:

- **Evidence files over conversation memory.** Its phases write dated Markdown files under `.copilot-tracking/`. Its tracking instructions state: "This file-based tracking takes precedence over memory: persist durable working state to the dated tracking artifact rather than relying on session, conversation, or working memory." Its context-engineering docs give the rationale: "The model doesn't forget the instructions. It deprioritizes them because more recent tokens receive disproportionate attention weight." Those files are not meant to be committed (see [convergence point 5](#what-the-field-is-converging-on)), so the evidence trail persists across sessions but not with the branch.
- **A default critique step and a split review verdict.** A plan passes an independent critique before implementation by default, though the critique can be skipped and its verdict is advisory - its docs state that "A `Pass`, `Revise`, or `Blocked` verdict is advisory: confirmed user direction outranks critique advice" - and review is optional too: "Review is optional; skip it when you do not need an acceptance record." Where review does run, its docs state: "Review keeps execution status (`Complete`, `Partial`, or `Blocked`) separate from outcome (`Conformant`, `Conformant with justified divergence`, `Defects found`, `Residual work`, or `Not accepted`)." Work that finished and work that was accepted are recorded as different facts.
- **Upkeep automated in its own repository.** Frontmatter on its `.agent.md`, `.prompt.md`, `.instructions.md`, and `SKILL.md` files is validated against JSON schemas; eval suites under `evals/` run in PR validation; and a date-based freshness threshold is enforced in PR validation.

Its README is direct about how to use it: "It is best treated as a source of patterns and learning rather than a stable platform, foundation, or production dependency."

**A licensing note you must act on:** the GitHub API reports hve-core as MIT, but its README states: "Most content in this repository is covered by the MIT License. Certain skill content derived from OWASP Foundation publications is licensed under CC BY-SA 4.0. Each affected skill identifies its license in frontmatter". Skill frontmatter in the repository shows `CC-BY-SA-4.0` on several security skills, `CC-BY-4.0` - alone or in combined expressions that also pull in `CC-BY-SA-3.0`, `OGL-UK-3.0`, or `Apache-2.0` - on many others, and `CC-BY-NC-SA-4.0`, a non-commercial license, on one (`.github/skills/security/owasp-docker/`). Most skills declare `MIT` and a minority declare Creative Commons terms, while some declare no `license:` field at all and fall back to the repository default the README describes. If your organization has a license policy, read each skill's frontmatter before adopting the whole collection rather than treating the repository-level MIT identifier as covering every file.

**Pick it when:** your team works in GitHub Copilot and wants a research-first, evidence-tracked workflow with a broad collection of agents, prompts, instructions, and skills - and you are using it as patterns to learn from, as its own README advises.

## Where SpecRoute differs

Three differences are real. Each is stated with what it costs.

**1. It is content, not a CLI.** SpecRoute has no package to install, no `init` command, and no build step - you copy a runtime directory into your repository and edit it. The upside is that there is nothing to version-pin, nothing to upgrade, and no tool between you and your own files; the templates are yours the moment you copy them, and diverging from them is editing, not forking. The cost is equally real: there is no `specroute init`, nothing scaffolds the directories for you, and nothing enforces the phase order except review and whatever hooks you wire yourself. spec-kit and OpenSpec each ship a CLI, and BMAD-METHOD's stable line ships its own npm installer; for a team that wants the flow carried by a tool - commands that scaffold the directories and write each stage's files in sequence - that is a genuine advantage over SpecRoute. What none of them advertises is refusing out-of-order work: OpenSpec's own docs describe its workflow as "actions, not phases". hve-core has no CLI of its own either; it installs through a Copilot CLI plugin or a VS Code extension.

This is the current design, not a permanent commitment. A `specroute` CLI or extension remains an open, uncommitted item on the [roadmap](../ROADMAP.md), conditioned on whether a tool would meaningfully exceed what `tools/sync-skills.py` already does.

**2. Vendor neutrality is a written contract, not a support list.** SpecRoute's unit of vendor support is a complete runtime layout in that vendor's *native* format - its own agent file shape, its own hook schema, its own MCP configuration - with the supported matrix mirrored byte-identically across several documents and a new vendor added as a new column rather than a fork.

This is a different axis from the breadth claims peers make, and the two should not be confused. OpenSpec states that it works with 30+ AI assistants; that is a claim about how many assistants can consume its output, and it is a broader number than six. SpecRoute's six is a claim about depth: each of the six has a maintained layout in its own idiom. hve-core sits at the other end of the same axis: its roadmap frames the project as "optimized GitHub Copilot customizations" - depth on a single platform. Breadth and depth are both legitimate, and neither kind of claim is evidence about the other.

**3. The framework is built by the pattern it documents.** SpecRoute's own `.claude/` directory is a working implementation team - agents, skills, commands, and hooks that author and audit the framework itself. The documentation is an output of the process it describes, which makes the claim checkable rather than aspirational: the artifacts are in the repository.

## When to pick a peer instead

- **You want a command to scaffold the files for you.** Use spec-kit or OpenSpec. SpecRoute makes you copy directories by hand and edit them.
- **You want change proposals held apart from the settled spec.** Use OpenSpec. Its `openspec/specs/` vs `openspec/changes/` split is the sharpest among the spec-driven projects here, though its own docs describe the workflow as "actions, not phases" rather than an enforced order; SpecRoute's ordering is likewise a convention upheld by review and by hooks you configure yourself.
- **You want a ready-made multi-role agent organization.** Use BMAD-METHOD, subject to the licensing check above. SpecRoute ships archetypes you are expected to adapt, not a maintained persona library.
- **You are single-vendor on Kiro and content there.** Use `.kiro/specs/` natively. SpecRoute's vendor neutrality is overhead you would be paying for a portability you are not using. Revisit if you add a second tool.
- **You work only in GitHub Copilot.** Look at hve-core. SpecRoute has no Copilot runtime layout; hve-core is built for Copilot Chat and the Copilot CLI.
- **You want opinionated defaults you do not have to think about.** Use spec-kit, OpenSpec, or BMAD-METHOD. SpecRoute ships templates on the explicit assumption that you will edit them, and a team that will not edit them will get less value from it.
- **Your policy requires a recognized SPDX license.** spec-kit and OpenSpec are MIT and SpecRoute is Apache-2.0; BMAD-METHOD is reported as `NOASSERTION` / "Other" and needs a direct reading of its terms. hve-core is reported as MIT, but some bundled skills carry Creative Commons licenses, one of them non-commercial, so check each skill's frontmatter license before adopting the whole collection.
- **You are already succeeding with one of them.** None of these projects is a strict superset of another, and the switching cost is a rewrite. A working practice is worth more than a better-matched framework.

## Using SpecRoute alongside a peer

These are not mutually exclusive, and the combinations are not hypothetical - the layers compose because they solve different halves of the problem.

- **A peer CLI as the producer, SpecRoute as the review layer.** Let spec-kit or OpenSpec generate and sequence the artifacts; use SpecRoute's `rules/`, agent roster, and sanitization hooks as the standards those artifacts are reviewed against. The CLI sequences the artifacts; the rules govern their content.
- **Kiro's storage, SpecRoute's content.** Keep specs in `.kiro/specs/` where the IDE expects them, and use SpecRoute's requirements, design, and tasks templates as what goes in them.
- **A peer for the flow, SpecRoute for the second vendor.** If a team on spec-kit adds a tool that spec-kit does not target, SpecRoute's runtime layouts cover the new vendor without disturbing the existing flow.

## How these numbers stay honest

Every third-party number and license on this page is regenerable by the command above and stamped with the date it was last run. This is the same discipline SpecRoute applies to its own roster counts: ship the command that produces the number next to the number, and record the date it was verified.

Two rules keep the page from rotting quietly:

- **Raw numbers appear in the table only, never in prose.** Body text says "the most widely adopted"; it never says a count. There is exactly one place to refresh.
- **Refreshing the numbers means re-running the command**, not editing digits from memory. A number without a reproduction is a rumor with a decimal point.

This page is on the `doc-currency-check` cycle. Third-party facts - star counts, SPDX identifiers, per-file licenses, command names, and phase vocabularies - are the fastest-rotting claims in this repository, because they change without anything in this repository changing.

## See also

- [`philosophy.md`](philosophy.md) - why SpecRoute is content rather than an application.
- [`spec-driven-development.md`](spec-driven-development.md) - the SpecRoute flow this page situates.
- [`agent-cli-integrations.md`](agent-cli-integrations.md) - per-vendor wiring, including Kiro.
- [`../ROADMAP.md`](../ROADMAP.md) - non-goals, and the open question of a `specroute` CLI.
