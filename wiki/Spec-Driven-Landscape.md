# Spec-Driven Landscape

<!-- sources: agentic-docs/spec-driven-landscape.md -->

SpecRoute is neither the first nor the only framework for spec-driven agentic development. This page maps the field so you have what you need to decide what to adopt — including what you need to decide *against* SpecRoute.

Canonical source: [`agentic-docs/spec-driven-landscape.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/spec-driven-landscape.md).

## Scope and method

Four projects: the three most-adopted open-source SDD projects on GitHub, plus one vendor-native implementation that SpecRoute already supports as a runtime target.

Every claim is drawn from the project's own repository or from GitHub API metadata, and every number carries the command that regenerates it. Claims a project makes about itself that cannot be verified from its repository are attributed, not asserted.

This page does **not** benchmark the projects, score them on a feature matrix, or name a winner. A matrix built from SpecRoute's own taxonomy would score SpecRoute highest by construction — that is advocacy, not information.

## What the field is converging on

The interesting result is not that these projects differ. It is how much they independently agree.

1. **The artifact precedes the code, and the artifact is the review surface.** The diff becomes something you check *against* the spec rather than reason about from scratch.
2. **Explicit, named phases with gates between them.** `constitution → specify → plan → tasks → implement` · `propose → apply → archive` · requirements → design → tasks · PRD → spec triplet → tasks → implementation → validation. The counts differ; the conviction that phases must be named and separated does not.
3. **A durable project-level layer, held apart from per-change work.** spec-kit's constitution, OpenSpec's `openspec/specs/`, Kiro's `steering/`, SpecRoute's `rules/` and `AGENTS.md`. Four names, one idea: standing constraints must not be re-litigated inside every change.
4. **Settled work separated from in-flight work.** OpenSpec archives applied changes; SpecRoute has `prds/active|deprecated|archive`. Without it, a specs directory becomes an undated pile where current and abandoned intent look identical.
5. **Artifacts are plain Markdown in the repo, versioned with the code.** None of these projects put specs in an external tracker.
6. **Agent roles are first-class files.** BMAD's "Agent-as-Code", SpecRoute's [[Agents]], and every vendor's subagent format. A role in a file can be reviewed and versioned; one in a paste cannot.

**Not converged:** no shared file format (the artifacts are not interchangeable), no portability between frameworks (moving is a rewrite, not a migration), and hooks and commands remain vendor-shaped everywhere. The field agrees on the *shape* of spec-driven development and on almost none of the *format*.

## The comparison set

| Project | What it ships | Delivery | License | Artifacts live in | Phase model | Stars (verified 2026-08-31) |
|---|---|---|---|---|---|---|
| [github/spec-kit](https://github.com/github/spec-kit) | CLI + slash-command set | Python CLI | MIT | `.specify/` | `constitution` → `specify` → `plan` → `tasks` → `implement` | 132,508 |
| [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | CLI + slash-command set | TypeScript CLI (npm, Node >= 20.19.0) | MIT | `openspec/specs/`, `openspec/changes/` | `propose` → `apply` → `archive` | 66,821 |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Agent persona library + module system | CLI installer | Reported as `NOASSERTION`, displayed as "Other" | module-defined | full-lifecycle, module-defined | 52,514 |
| [Amazon Kiro](https://kiro.dev) | IDE with native SDD | Vendor product | Proprietary product | `.kiro/specs/` | requirements → design → tasks | n/a (not an OSS repo) |
| **SpecRoute** | Templates, rules, agent definitions, runtime layouts | Content only — copy directories | Apache-2.0 | per-vendor runtime dirs | PRD → spec triplet → tasks → implementation → validation | n/a (this project) |

Regenerate the Stars and License columns:

```bash
# Reproduces every Stars and License cell above. Last run: 2026-08-31.
for r in github/spec-kit Fission-AI/OpenSpec bmad-code-org/BMAD-METHOD; do
  gh api "repos/$r" --jq '"\(.full_name)\t\(.stargazers_count)\t\(.license.spdx_id // "NOASSERTION")"'
done
```

Star counts measure attention, not fitness. They are recorded because they are why *these four* are the comparison set rather than four arbitrary repositories — not as a ranking. The sections below are ordered by model-proximity to SpecRoute, which is more useful when you are choosing.

## What each project does well

### github/spec-kit

The most widely adopted of the set and the most complete end-to-end command sequence. `constitution` establishes durable principles at `.specify/memory/constitution.md`; `specify` captures intent; `plan` produces the approach; `tasks` decomposes it; `implement` executes. Each step writes real files into `.specify/`, so the flow is enforced by tooling rather than operator discipline, and the Python CLI scaffolds a new project in minutes.

**Pick it when:** you want the canonical five-phase flow, installed and scaffolded by a command, with the largest community and the most examples to learn from.

### Fission-AI/OpenSpec

The strictest state machine in the set, and the clearest thinking about *change* as the unit of work. `openspec/specs/` holds what is true; `openspec/changes/` holds what is proposed, each change carrying its own `proposal.md`, `design.md`, and `tasks.md`. `/opsx:propose`, `/opsx:apply`, and `/opsx:archive` move a change through, and applied changes land in `openspec/changes/archive/`. That settled-versus-delta distinction is the sharpest here — the spec never silently accumulates proposals nobody adopted. The project states that it works with 30+ AI coding assistants.

Install: `npm install -g @fission-ai/openspec@latest` (Node >= 20.19.0), then `openspec init`.

**Pick it when:** you want change proposals to be first-class and separately reviewable, and you want the tool to hold the line on phase ordering instead of relying on reviewers to notice.

### bmad-code-org/BMAD-METHOD

The deepest agent-persona library of the set. Its "Agent-as-Code" approach ships full-lifecycle roles as Markdown, so a team gets a working multi-role organization without designing one. The v6.0.0 stable release (February 2026) replaced the v5 monolith with a modular architecture — BMM for software development, BMB for building your own modules, CIS for creative work, BMVCS for version control — so you can adopt one module without the rest.

**A licensing note you must act on:** the GitHub API reports the license as `NOASSERTION`, displayed as "Other". That is not a recognized SPDX identifier, so scanners and procurement policies keyed to SPDX will not resolve it. Read the repository's terms directly and clear them before adopting. Do not infer permissiveness from the MIT-licensed projects in the same table.

**Pick it when:** you want a maintained, opinionated multi-role agent organization out of the box, and you have confirmed the license terms are acceptable to you.

### Amazon Kiro — a vendor that is also a peer

Kiro is a supported SpecRoute vendor column *and* a competing methodology. It ships SDD natively: `.kiro/specs/` holds a requirements/design/tasks progression built into the IDE, with `steering/` as its durable layer.

If Kiro is your only tool, its native path is shorter than any framework layered on top of it. SpecRoute supports Kiro because SpecRoute's contract is vendor neutrality — not because Kiro needs SpecRoute.

Kiro's runtime shape and hook taxonomy live in [[Agent CLI Integrations]] and [[Vendor Matrix]]; this page does not restate them.

## Where SpecRoute differs

Three real differences, each with what it costs.

**1. It is content, not a CLI.** No package to install, no `init`, no build step — you copy a runtime directory and edit it. Nothing to version-pin, nothing to upgrade, no tool between you and your files. The cost is equally real: nothing scaffolds the directories, and nothing enforces phase order except review and hooks you wire yourself. All three OSS peers ship a CLI, and for a team that wants the flow enforced by tooling that is a genuine advantage over SpecRoute.

This is the current design, not a permanent commitment. A `specroute` CLI or extension remains an open, uncommitted item on the [[Roadmap]].

**2. Vendor neutrality is a written contract, not a support list.** The unit of support is a complete runtime layout in each vendor's *native* format, with the matrix mirrored byte-identically and a new vendor added as a column rather than a fork.

This is a different axis from peer breadth claims, and the two should not be confused. OpenSpec states it works with 30+ AI coding assistants — a claim about how many assistants can consume its output, and a broader number than six. SpecRoute's six is a claim about depth: each has a maintained layout in its own idiom. Both are legitimate; neither number is evidence about the other.

**3. The framework is built by the pattern it documents.** SpecRoute's own `.claude/` directory is a working [[Implementation Team]] that authors and audits the framework. That makes the claim checkable rather than aspirational — the artifacts are in the repository.

## When to pick a peer instead

- **You want a command to scaffold the files for you.** Use spec-kit or OpenSpec. SpecRoute makes you copy directories by hand.
- **You want the tool to refuse out-of-order work.** Use OpenSpec. Its state machine is enforced; SpecRoute's ordering is convention upheld by review and hooks you configure.
- **You want a ready-made multi-role agent organization.** Use BMAD-METHOD, subject to the licensing check above. SpecRoute ships archetypes you are expected to adapt.
- **You are single-vendor on Kiro and content there.** Use `.kiro/specs/` natively. SpecRoute's vendor neutrality is overhead you would be paying for portability you are not using. Revisit if you add a second tool.
- **You want opinionated defaults you do not have to think about.** Use any of the three CLIs. SpecRoute assumes you will edit its templates; a team that will not edit them gets less from it.
- **Your policy requires a recognized SPDX license.** spec-kit and OpenSpec are MIT, SpecRoute is Apache-2.0; BMAD-METHOD needs a direct reading of its terms.
- **You are already succeeding with one of them.** None is a strict superset of another, and switching is a rewrite. A working spec-driven practice is worth more than a better-matched framework.

## Using SpecRoute alongside a peer

- **A peer CLI as the producer, SpecRoute as the review layer.** Let spec-kit or OpenSpec generate and sequence the artifacts; use SpecRoute's [[Rules]], agent roster, and [[Sanitization]] hooks as the standards those artifacts are reviewed against. The CLI enforces order; the rules enforce content.
- **Kiro's storage, SpecRoute's content.** Keep specs in `.kiro/specs/` where the IDE expects them, and use SpecRoute's [[Specs]] templates as what goes in them.
- **A peer for the flow, SpecRoute for the second vendor.** A team on spec-kit that adds a tool spec-kit does not target can cover it with a SpecRoute runtime layout without disturbing the existing flow.

## How these numbers stay honest

Every third-party number and license here is regenerable by the command above and stamped with the date it was last run — the same discipline [[Multi-Agent Orchestration]] applies to roster counts: ship the command that produces the number next to the number, and record when it was verified.

Two rules keep the page from rotting quietly:

- **Raw numbers appear in the table only, never in prose.** There is exactly one place to refresh.
- **Refreshing means re-running the command**, not editing digits from memory. A number without a reproduction is a rumor with a decimal point.

Third-party facts — star counts, SPDX identifiers, command names, phase vocabularies — are the fastest-rotting claims in the repository, because they change without anything in the repository changing.

## See also

- [[Philosophy]] — why SpecRoute is content rather than an application
- [[Spec-Driven Development]] — the SpecRoute flow this page situates
- [[Agent CLI Integrations]] · [[Vendor Matrix]] — per-vendor wiring, including Kiro
- [[Roadmap]] — non-goals, and the open question of a `specroute` CLI
