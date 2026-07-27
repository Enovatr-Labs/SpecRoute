# Maintainers

SpecRoute is maintained by **[Enovatr Labs](https://github.com/Enovatr-Labs)** as an open-source contribution to the agentic-engineering ecosystem.

## Current maintainers

| Name | Role | GitHub | Contact |
|---|---|---|---|
| **Chika Ihejimba** | Lead maintainer / project author | [@cihejimba](https://github.com/cihejimba) | `chika@enovatr.com` |

## How to reach us

| You want to ... | Contact |
|---|---|
| Report a security vulnerability | `security@enovatr.com` (preferred) — see [`SECURITY.md`](SECURITY.md) for the full disclosure protocol |
| Discuss a contribution before opening a PR | Open a GitHub issue or `chika@enovatr.com` |
| Ask about commercial use, partnerships, or extended support | `chika@enovatr.com` |
| Report a bug or propose a feature | [GitHub issues](https://github.com/Enovatr-Labs/SpecRoute/issues) |
| Contribute | See [`CONTRIBUTING.md`](CONTRIBUTING.md) |

For non-security inquiries, prefer GitHub issues — they're public, searchable, and let the community participate.

## Sponsoring organization

[Enovatr Labs](https://github.com/Enovatr-Labs) sponsors SpecRoute as part of its work on agentic engineering tooling. The framework is intentionally vendor-neutral and not tied to any Enovatr product; it's a community-curated framework that Enovatr also uses internally.

## Becoming a maintainer

We grow the maintainer team based on demonstrated contribution and judgment. Typical path:

1. **Contribute consistently.** PRs, issue triage, doc improvements, worked examples, vendor-integration patterns. Quality and responsiveness matter more than volume.
2. **Demonstrate judgment.** Comment thoughtfully on others' PRs and issues; help shape architectural decisions; respect the project's hard constraints (vendor neutrality, sanitization, two-tier docs, frontmatter contracts).
3. **Take ownership of an area.** A new vendor's runtime template, a workflow, a doc category — a sustained area where you become the go-to reviewer.
4. **Receive an invitation.** Existing maintainers nominate; consensus among current maintainers confirms.

There's no fixed contribution count. We optimize for trust, not throughput.

## Decision-making

For most decisions: lazy consensus. A maintainer proposes; if no maintainer objects within a reasonable window, the change lands.

For architectural decisions: an ADR template ([`specs/templates/architecture-decision-record.md`](specs/templates/architecture-decision-record.md)). The proposing maintainer drafts; other maintainers review; once accepted, the ADR is immutable and superseding it requires a new ADR.

For breaking changes to the framework's contracts (vendor matrix, frontmatter, spec-driven flow): explicit review and sign-off from the lead maintainer.

## Releasing SpecRoute

SpecRoute is a content repository. There is no package build or registry
publication step; each GitHub release consists of the tagged repository state
and GitHub's generated source archives.

Releases are started manually from the [`Release`](.github/workflows/release.yml)
workflow on `main`, after the promotion PR has merged. Before the first
dispatch, repository owners must configure the `RELEASE_MANAGERS` repository
variable, configure the `release` environment with required review, enable
immutable releases, and install the dedicated Release GitHub App. The App needs
only Actions read, Administration read, and Contents write, and is installed
only on the SpecRoute repository. There is no personal-access-token or
`GITHUB_TOKEN` mutation fallback. Release immutability is currently off, so the
first run remains blocked until that prerequisite is enabled. The workflow pins
`actions/create-github-app-token` to the immutable commit for v3.2.0.
Configure `RELEASE_APP_CLIENT_ID` as a repository or `release`-environment
variable and `RELEASE_APP_PRIVATE_KEY` as a `release`-environment secret.

Release authorization has two layers:

1. `RELEASE_MANAGERS` is a required, comma-separated allowlist of GitHub logins.
   Every operation checks both the original `github.actor` and the
   `github.triggering_actor` who starts or reruns the current attempt against
   it, fail-closed, before checkout. GitHub cannot separately hide or ACL the
   **Run workflow** button from other users with write access; their
   unauthorized dispatches stop immediately without checkout or mutation.
2. Required reviewers on the protected `release` environment approve the
   mutation job after the public, read-only preflight passes.

| Input | Contract |
|---|---|
| `operation` | `publish` for a new release, `resume` for an interrupted annotated-tag publication with no release or a matching draft, or `realign-develop` for post-release branch recovery |
| `version` | Bare SemVer `X.Y.Z`; the workflow derives tag `vX.Y.Z` |
| `release_sha` | Full 40-character commit SHA; it must be the current `main` commit |
| `provenance_sha` | For `publish` and `resume`, the exact commit locally reviewed by the private-source provenance gate; it must equal `release_sha` |
| `confirm_provenance` | For `publish` and `resume`, the maintainer's recorded acknowledgement that the provenance gate passed for that SHA |
| `realign_develop` | After `publish`, optionally realign `develop` to the released `main` commit; disabled by default because the Release App additionally needs an `always` bypass on the develop ruleset |

Before dispatching `publish` or `resume`, run the release-only provenance audit
documented in [`tools/README.md`](tools/README.md) from a fresh
`git clone --single-branch --branch main --no-local ...`, detached at the exact
`release_sha` and confirmed clean. A worktree is not sufficient: worktrees share
refs, and `--history` audits them all. The working-tree pass also includes
untracked content. The hosted runner receives only the public commit SHA and
acknowledgement. Private repository identities, paths, excerpts, terms, reports,
and review decisions remain local and gitignored.

`publish` uses the Release App to verify repository settings, immutable tag
rules, and release metadata before mutation, creates an annotated tag and draft
release, verifies both, and only then publishes the release. `resume` uses the
same App and re-verifies an existing tag before publication; it accepts either
a matching draft or a tag-only partial failure and creates the missing draft
when needed. `realign-develop` is subject to the same actor allowlist and
environment approval.
`realign-develop` performs only the guarded post-release branch repair and does
not replace the provenance gate.

Failure recovery is intentionally narrow:

- A preflight failure has no publication side effects; fix the candidate and
  dispatch again.
- If an annotated tag exists with either no release or a matching draft, inspect
  it and use `resume`; the workflow creates a missing draft. Never move or
  recreate the release tag.
- If publication succeeded but `develop` realignment failed, the release is
  still valid; use `realign-develop` after fixing the repository permission.
- If a published immutable release is wrong, correct the repository and cut a
  new patch release. Do not mutate the published tag or release.

Wiki publication is independent. Release preflight verifies, read-only, that the
live wiki matches `wiki/`; it never republishes the wiki. A merge to `main` that
changes `wiki/**` triggers the existing `Sync wiki` workflow. Tag pushes and
GitHub-App branch updates do not recursively trigger other workflows, so verify
the main-driven sync separately and rerun it manually if it failed.

Repository-side environment, ruleset, and recovery configuration is maintained
in the local operations runbook. See [`CHANGELOG.md`](CHANGELOG.md) for release
notes and [`wiki/Sanitization.md`](wiki/Sanitization.md) for the public
sanitization contract.

## What this project is *not*

- **A SaaS or hosted service.** SpecRoute is markdown content. We don't run anything.
- **A vendor-specific framework.** We treat Claude Code, Codex, Gemini CLI / Antigravity, Kiro, Cursor, and Devin Desktop as parallel execution environments. The matrix is the contract.
- **A standards body.** We propose patterns we've found useful; consumers fork what they need and ignore the rest.

## Acknowledgments

SpecRoute generalizes patterns from internal Enovatr Labs codebases into a public framework. Specific design choices (the spec triplet, the phased master-prompt pattern, the per-vendor runtime layouts) draw on production usage across multiple projects. Sanitized for public release.

The agentic-engineering ecosystem moves quickly. We watch the upstream conventions of the agent CLIs we support and update SpecRoute in lock-step when they evolve (see commit history for examples — the 30-event Claude Code hook taxonomy and the cross-vendor hook coverage were added when those vendors shipped or expanded their hooks systems).

## License

SpecRoute is released under [Apache 2.0](LICENSE). Copyright (c) Enovatr Labs.
