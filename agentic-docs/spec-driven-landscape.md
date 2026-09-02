# The Spec-Driven Landscape

SpecRoute is neither the first nor the only framework for spec-driven agentic development. Several projects reached similar conclusions independently, and some have been adopted at a scale SpecRoute has not. This page maps that field so a reader deciding what to adopt has what they need to decide - including what they need to decide *against* SpecRoute.

## Scope and method

The comparison set is four projects: the three most-adopted open-source spec-driven-development projects on GitHub, plus one vendor-native implementation that SpecRoute already supports as a runtime target.

Every factual claim here is drawn from the project's own repository or from GitHub API metadata, and every number carries the command that regenerates it (see [The comparison set](#the-comparison-set)). Where a project makes a claim about itself that cannot be independently verified from its repository, it is attributed to that project rather than asserted.

This page deliberately does **not**:

- Benchmark the projects or rank them by quality. No such measurement exists that would survive scrutiny.
- Score them on a feature matrix. A matrix built from SpecRoute's own artifact taxonomy would score SpecRoute highest by construction, which makes it advocacy, not information.
- Recommend a single winner. The four are shaped by different constraints, and the right choice depends on constraints this page cannot see.

## What the field is converging on

The interesting result is not that these projects differ - it is how much they independently agree.

**1. A written artifact precedes code, and the artifact is the review surface.** All four treat the specification, not the diff, as the thing a human reads carefully. The diff becomes something you check *against* the spec rather than reason about from scratch. This is the shared premise; everything else is mechanism.

**2. Explicit, named phases with gates between them.** spec-kit runs `constitution -> specify -> plan -> tasks -> implement`. OpenSpec runs `propose -> apply -> archive`. Kiro runs requirements -> design -> tasks. SpecRoute runs PRD -> spec triplet -> tasks -> implementation -> validation. The phase counts differ; the conviction that phases must be *named and separated* rather than blurred into one prompt does not.

**3. A durable project-level layer, held apart from per-change work.** spec-kit keeps a constitution at `.specify/memory/constitution.md`. OpenSpec separates `openspec/specs/` (what is true) from `openspec/changes/` (what is being changed). Kiro has `steering/`. SpecRoute has `rules/` and `AGENTS.md`. Four projects, four names, one idea: standing constraints must not be re-litigated inside every change.

**4. Settled work is separated from in-flight work.** OpenSpec makes this most explicit - an applied change is moved to `openspec/changes/archive/`. SpecRoute's `prds/active/`, `prds/deprecated/`, and `prds/archive/` express the same lifecycle. Without it, a specs directory becomes an undated pile in which current intent and abandoned intent look identical.

**5. Artifacts live in the repository as plain Markdown, versioned with the code.** `.specify/`, `openspec/`, `.kiro/specs/`, and SpecRoute's runtime directories are all directories of Markdown committed beside the source. None of these projects put specs in an external tracker. The specification is expected to move with the branch, review with the PR, and be diffable.

**6. Agent roles are first-class files, not prompt fragments.** BMAD-METHOD calls this "Agent-as-Code" and ships Markdown personas. SpecRoute ships `agents/`. All six vendors in the [vendor matrix](agent-cli-integrations.md) now ship a subagent file format. A role that lives in a file can be reviewed, versioned, and reused; one that lives in a paste cannot.

### What the field has *not* converged on

- **No shared file format.** A spec-kit `spec.md`, an OpenSpec `proposal.md`, a Kiro `requirements.md`, and a SpecRoute requirements document are not interchangeable. There is no `AGENTS.md`-equivalent standard for the specification itself.
- **No portability between frameworks.** Adopting one is a commitment; moving between them is a rewrite, not a migration.
- **Automation surfaces remain vendor-shaped.** Hooks and commands differ per tool in event names, schema, and file location. Every project in this set inherits that fragmentation; none has solved it.

The honest summary of the state of the art: the field agrees on the *shape* of spec-driven development and agrees on almost none of the *format*.

## The comparison set

| Project | What it ships | Delivery | License | Artifacts live in | Phase model | Stars (verified 2026-08-31) |
|---|---|---|---|---|---|---|
| [github/spec-kit](https://github.com/github/spec-kit) | CLI + slash-command set | Python CLI | MIT | `.specify/` | `constitution` -> `specify` -> `plan` -> `tasks` -> `implement` | 132,508 |
| [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | CLI + slash-command set | TypeScript CLI (npm, Node >= 20.19.0) | MIT | `openspec/specs/`, `openspec/changes/` | `propose` -> `apply` -> `archive` | 66,821 |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Agent persona library + module system | CLI installer | Reported as `NOASSERTION`, displayed as "Other" | module-defined | full-lifecycle, module-defined | 52,514 |
| [Amazon Kiro](https://kiro.dev) | IDE with native SDD | Vendor product | Proprietary product | `.kiro/specs/` | requirements -> design -> tasks | n/a (not an OSS repo) |
| **SpecRoute** | Templates, rules, agent definitions, runtime layouts | Content only - copy directories | Apache-2.0 | per-vendor runtime dirs | PRD -> spec triplet -> tasks -> implementation -> validation | n/a (this project) |

Regenerate the Stars and License columns:

```bash
# Reproduces every Stars and License cell above. Last run: 2026-08-31.
for r in github/spec-kit Fission-AI/OpenSpec bmad-code-org/BMAD-METHOD; do
  gh api "repos/$r" --jq '"\(.full_name)\t\(.stargazers_count)\t\(.license.spdx_id // "NOASSERTION")"'
done
```

Star counts measure attention, not fitness. They are recorded here because they are the reason *these four* are the comparison set rather than four arbitrary repositories - not as a ranking. The sections below are ordered by how close each project's model is to SpecRoute's, which is a more useful ordering for a reader making a choice.

## What each project does well

### github/spec-kit

The most widely adopted of the set, and the most complete end-to-end command sequence. `constitution` establishes durable project principles at `.specify/memory/constitution.md`; `specify` captures intent; `plan` produces the technical approach; `tasks` decomposes it; `implement` executes. Each step is a real command that writes real files into `.specify/`, so the flow is enforced by the tooling rather than by the operator's discipline. The Python CLI installs and scaffolds for you, which means a new project is running the full flow in minutes rather than after a directory-copying session.

**Pick it when:** you want the canonical five-phase flow, installed and scaffolded by a command, with the largest community and the most examples to learn from.

### Fission-AI/OpenSpec

The strictest state machine in the set, and the clearest thinking about *change* as the unit of work. `openspec/specs/` holds what is currently true; `openspec/changes/` holds what is being proposed, each change carrying its own `proposal.md`, `design.md`, and `tasks.md`. `/opsx:propose`, `/opsx:apply`, and `/opsx:archive` move a change through the three phases, and applied changes land in `openspec/changes/archive/`. The distinction between the settled spec and the in-flight delta is the sharpest of any project here - it means the specification does not silently accumulate proposals that were never adopted. The project states that it works with 30+ AI coding assistants.

Installation is `npm install -g @fission-ai/openspec@latest` (Node >= 20.19.0) followed by `openspec init`.

**Pick it when:** you want change proposals to be first-class and separately reviewable, and you want the tool to hold the line on phase ordering rather than relying on reviewers to notice.

### bmad-code-org/BMAD-METHOD

The deepest agent-persona library of the set. Its "Agent-as-Code" approach ships roles as Markdown files spanning the full product lifecycle, so a team gets a working multi-role organization without designing one. The v6.0.0 stable release (February 2026) replaced the v5 monolith with a modular architecture: BMM for software development, BMB for building your own modules, CIS for creative work, and BMVCS for version control. That modularity means you can adopt the software-development module without taking the rest.

**A licensing note you must act on:** the GitHub API reports BMAD-METHOD's license as `NOASSERTION`, which GitHub displays as "Other". That is not a recognized SPDX identifier, so automated license scanners and procurement policies keyed to SPDX will not resolve it. If your organization has a license policy, read the repository's license terms directly and clear them before adopting. Do not infer permissiveness from the other MIT-licensed projects in this table.

**Pick it when:** you want a maintained, opinionated multi-role agent organization out of the box, and you have confirmed the license terms are acceptable to you.

### Amazon Kiro - a vendor that is also a peer

Kiro occupies an unusual position: it is a **supported SpecRoute vendor column** and *also* a competing methodology. It ships spec-driven development natively - `.kiro/specs/` holds a requirements/design/tasks progression built into the IDE, with `steering/` as its durable project layer.

If Kiro is your only tool, its native path is shorter than any framework layered on top of it. The specs are already where the IDE expects them, the flow is already wired, and there is nothing to copy. SpecRoute supports Kiro because SpecRoute's contract is vendor neutrality, not because Kiro needs SpecRoute.

Kiro's runtime shape, config surfaces, and hook taxonomy are documented in [`agent-cli-integrations.md`](agent-cli-integrations.md); this page does not restate the vendor matrix.

## Where SpecRoute differs

Three differences are real. Each is stated with what it costs.

**1. It is content, not a CLI.** SpecRoute has no package to install, no `init` command, and no build step - you copy a runtime directory into your repository and edit it. The upside is that there is nothing to version-pin, nothing to upgrade, and no tool between you and your own files; the templates are yours the moment you copy them, and diverging from them is editing, not forking. The cost is equally real: there is no `specroute init`, nothing scaffolds the directories for you, and nothing enforces the phase order except review and whatever hooks you wire yourself. All three OSS peers ship a CLI, and for a team that wants the flow enforced by tooling, that is a genuine advantage over SpecRoute.

This is the current design, not a permanent commitment. A `specroute` CLI or extension remains an open, uncommitted item on the [roadmap](../ROADMAP.md), conditioned on whether a tool would meaningfully exceed what `tools/sync-skills.py` already does.

**2. Vendor neutrality is a written contract, not a support list.** SpecRoute's unit of vendor support is a complete runtime layout in that vendor's *native* format - its own agent file shape, its own hook schema, its own MCP configuration - with the supported matrix mirrored byte-identically across several documents and a new vendor added as a new column rather than a fork.

This is a different axis from the breadth claims peers make, and the two should not be confused. OpenSpec states that it works with 30+ AI coding assistants; that is a claim about how many assistants can consume its output, and it is a broader number than six. SpecRoute's six is a claim about depth: each of the six has a maintained layout in its own idiom. Breadth and depth are both legitimate, and neither number is evidence about the other.

**3. The framework is built by the pattern it documents.** SpecRoute's own `.claude/` directory is a working implementation team - agents, skills, commands, and hooks that author and audit the framework itself. The documentation is an output of the process it describes, which makes the claim checkable rather than aspirational: the artifacts are in the repository.

## When to pick a peer instead

- **You want a command to scaffold the files for you.** Use spec-kit or OpenSpec. SpecRoute makes you copy directories by hand and edit them.
- **You want the tool to refuse out-of-order work.** Use OpenSpec. Its three-phase state machine is enforced; SpecRoute's ordering is a convention upheld by review and by hooks you configure yourself.
- **You want a ready-made multi-role agent organization.** Use BMAD-METHOD, subject to the licensing check above. SpecRoute ships archetypes you are expected to adapt, not a maintained persona library.
- **You are single-vendor on Kiro and content there.** Use `.kiro/specs/` natively. SpecRoute's vendor neutrality is overhead you would be paying for a portability you are not using. Revisit if you add a second tool.
- **You want opinionated defaults you do not have to think about.** Use any of the three CLIs. SpecRoute ships templates on the explicit assumption that you will edit them, and a team that will not edit them will get less value from it.
- **Your policy requires a recognized SPDX license.** spec-kit and OpenSpec are MIT and SpecRoute is Apache-2.0; BMAD-METHOD is reported as `NOASSERTION` / "Other" and needs a direct reading of its terms.
- **You are already succeeding with one of them.** None of these projects is a strict superset of another, and the switching cost is a rewrite. A working spec-driven practice is worth more than a better-matched framework.

## Using SpecRoute alongside a peer

These are not mutually exclusive, and the combinations are not hypothetical - the layers compose because they solve different halves of the problem.

- **A peer CLI as the producer, SpecRoute as the review layer.** Let spec-kit or OpenSpec generate and sequence the artifacts; use SpecRoute's `rules/`, agent roster, and sanitization hooks as the standards those artifacts are reviewed against. The CLI enforces order; the rules enforce content.
- **Kiro's storage, SpecRoute's content.** Keep specs in `.kiro/specs/` where the IDE expects them, and use SpecRoute's requirements, design, and tasks templates as what goes in them.
- **A peer for the flow, SpecRoute for the second vendor.** If a team on spec-kit adds a tool that spec-kit does not target, SpecRoute's runtime layouts cover the new vendor without disturbing the existing flow.

## How these numbers stay honest

Every third-party number and license on this page is regenerable by the command above and stamped with the date it was last run. This is the same discipline SpecRoute applies to its own roster counts: ship the command that produces the number next to the number, and record the date it was verified.

Two rules keep the page from rotting quietly:

- **Raw numbers appear in the table only, never in prose.** Body text says "the most widely adopted"; it never says a count. There is exactly one place to refresh.
- **Refreshing the numbers means re-running the command**, not editing digits from memory. A number without a reproduction is a rumor with a decimal point.

This page is on the `doc-currency-check` cycle. Third-party facts - star counts, SPDX identifiers, command names, and phase vocabularies - are the fastest-rotting claims in this repository, because they change without anything in this repository changing.

## See also

- [`philosophy.md`](philosophy.md) - why SpecRoute is content rather than an application.
- [`spec-driven-development.md`](spec-driven-development.md) - the SpecRoute flow this page situates.
- [`agent-cli-integrations.md`](agent-cli-integrations.md) - per-vendor wiring, including Kiro.
- [`../ROADMAP.md`](../ROADMAP.md) - non-goals, and the open question of a `specroute` CLI.
