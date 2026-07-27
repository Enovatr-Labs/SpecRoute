# Maintainers

<!-- sources: MAINTAINERS.md, .github/workflows/release.yml, tools/README.md -->

SpecRoute is maintained by **[Enovatr Labs](https://github.com/Enovatr-Labs)** as an open-source contribution to the agentic-engineering ecosystem.

Full governance: [MAINTAINERS.md](https://github.com/Enovatr-Labs/SpecRoute/blob/main/MAINTAINERS.md).

## Current maintainers

| Name | Role | GitHub | Contact |
|---|---|---|---|
| **Chika Ihejimba** | Lead maintainer / project author | [@cihejimba](https://github.com/cihejimba) | `chika@enovatr.com` |

## How to reach us

| You want to ... | Contact |
|---|---|
| Report a security vulnerability | `security@enovatr.com` — see [[Security]] |
| Discuss a contribution before opening a PR | [Open a GitHub issue](https://github.com/Enovatr-Labs/SpecRoute/issues) or `chika@enovatr.com` |
| Ask about commercial use, partnerships, or extended support | `chika@enovatr.com` |
| Report a bug or propose a feature | [GitHub issues](https://github.com/Enovatr-Labs/SpecRoute/issues) |
| Contribute | See [[Contributing]] |

For non-security inquiries, **prefer GitHub issues** — they're public, searchable, and let the community participate.

## Sponsoring organization

[Enovatr Labs](https://github.com/Enovatr-Labs) sponsors SpecRoute as part of its work on agentic engineering tooling. The framework is intentionally vendor-neutral and not tied to any Enovatr product — it's a community-curated framework that Enovatr also uses internally.

## Becoming a maintainer

We grow the maintainer team based on demonstrated contribution and judgment. Typical path:

1. **Contribute consistently.** PRs, issue triage, doc improvements, worked examples, vendor-integration patterns. Quality and responsiveness matter more than volume.
2. **Demonstrate judgment.** Comment thoughtfully on others' PRs and issues; help shape architectural decisions; respect the project's hard constraints (vendor neutrality, sanitization, two-tier docs, frontmatter contracts).
3. **Take ownership of an area.** A new vendor's runtime template, a workflow, a doc category — a sustained area where you become the go-to reviewer.
4. **Receive an invitation.** Existing maintainers nominate; consensus among current maintainers confirms.

There's no fixed contribution count. We optimize for trust, not throughput.

## Decision-making

For most decisions: **lazy consensus**. A maintainer proposes; if no maintainer objects within a reasonable window, the change lands.

For architectural decisions: an ADR ([template](https://github.com/Enovatr-Labs/SpecRoute/blob/main/specs/templates/architecture-decision-record.md)). Once accepted, the ADR is immutable; superseding requires a new ADR.

For breaking changes to the framework's contracts (vendor matrix, frontmatter, spec-driven flow): explicit review and sign-off from the lead maintainer.

## Releasing SpecRoute

SpecRoute is content, so there is no package build or registry publication
step. A release contains the tagged repository state and GitHub's generated
source archives.

After the promotion PR reaches `main`, a maintainer starts the
[`Release` workflow](https://github.com/Enovatr-Labs/SpecRoute/blob/main/.github/workflows/release.yml)
manually from `main`. Before the first dispatch, repository owners must
configure the `RELEASE_MANAGERS` repository variable, required review on the
`release` environment, and immutable releases, then install the dedicated
Release GitHub App only on SpecRoute, with Actions read, Administration read,
and Contents write. There is no personal-access-token or `GITHUB_TOKEN`
mutation fallback. Release immutability is currently off, so the first run
remains blocked until it is enabled. The workflow pins
`actions/create-github-app-token` to the immutable commit for v3.2.0.
Configure `RELEASE_APP_CLIENT_ID` as a repository or `release`-environment
variable and `RELEASE_APP_PRIVATE_KEY` as a `release`-environment secret.

Authorization has two layers. `RELEASE_MANAGERS` is a required comma-separated
allowlist of GitHub logins. Both the original dispatcher and the user who starts
or reruns the current attempt are checked fail-closed before checkout for every
operation. GitHub cannot separately hide or ACL the **Run workflow** button
from other write users, but their unauthorized dispatches stop immediately
without checkout or mutation. After public, read-only preflight passes,
required reviewers on the protected `release` environment approve the mutation
job.

| Input | Contract |
|---|---|
| `operation` | `publish` for a new release, `resume` for an interrupted annotated-tag publication with no release or a matching draft, or `realign-develop` for post-release branch recovery |
| `version` | Bare SemVer `X.Y.Z`; the workflow derives tag `vX.Y.Z` |
| `release_sha` | Full 40-character SHA of the current `main` commit |
| `provenance_sha` | For `publish` and `resume`, the exact locally audited commit; it must equal `release_sha` |
| `confirm_provenance` | For `publish` and `resume`, acknowledgement that the private-source provenance gate passed for that SHA |
| `realign_develop` | After `publish`, optionally realign `develop` to the release commit; disabled by default because the Release App additionally needs an `always` bypass on the develop ruleset |

Run the local provenance gate from a fresh
`git clone --single-branch --branch main --no-local ...`, detached at the exact
`release_sha` and confirmed clean. A worktree is not sufficient because
worktrees share refs and `--history` audits them all; the working-tree pass also
includes untracked content. The hosted runner receives only a public commit SHA
and acknowledgement. The private audit's source identities, paths, excerpts,
terms, reports, and reviewed findings remain local and gitignored. See
[`tools/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/tools/README.md)
and [[Sanitization]].

`publish` creates and verifies an annotated tag and draft before publishing.
Use `resume` only after inspecting an exact annotated tag and any matching
draft; the workflow creates the draft when the tag exists without one.
If publication succeeded but branch realignment failed, the release is still
valid; use `realign-develop` after repairing its permission. Never repoint a
release tag. Correct a bad immutable release with a new patch release.

Wiki publication remains separate. Release preflight verifies, read-only, that
the live wiki matches `wiki/`; it never republishes it. A merge to `main` that
changes `wiki/**` triggers `Sync wiki`, while tag pushes and GitHub-App branch
updates do not recursively start other workflows. Verify or manually rerun the
main-driven wiki sync if it failed.

## What this project is *not*

- **A SaaS or hosted service.** SpecRoute is markdown content. We don't run anything.
- **A vendor-specific framework.** Claude Code, Codex, Gemini CLI / Antigravity, Kiro, Cursor, and Devin Desktop are parallel execution environments. The [[Vendor Matrix]] is the contract.
- **A standards body.** We propose patterns we've found useful; consumers fork what they need and ignore the rest.

## Acknowledgments

SpecRoute generalizes patterns from internal Enovatr Labs codebases into a public framework. Specific design choices (the spec triplet, the phased master-prompt pattern, the per-vendor runtime layouts) draw on production usage across multiple projects. Sanitized for public release.

The agentic-engineering ecosystem moves quickly. We watch the upstream conventions of the agent CLIs we support and update SpecRoute in lock-step when they evolve — the 30-event Claude Code hook taxonomy and the cross-vendor hook coverage were both added when those vendors shipped or expanded their hooks systems. Currency is itself an owned job: see the `docs-currency-auditor` agent in [[Implementation Team]].

## License

Apache 2.0. Copyright © Enovatr Labs. See [LICENSE](https://github.com/Enovatr-Labs/SpecRoute/blob/main/LICENSE).

## See also

- [[Roadmap]] — current trajectory
- [[Contributing]] — contributor workflow
- [[Code of Conduct]] — community standards
