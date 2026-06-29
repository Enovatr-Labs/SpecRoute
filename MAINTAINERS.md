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

## What this project is *not*

- **A SaaS or hosted service.** SpecRoute is markdown content. We don't run anything.
- **A vendor-specific framework.** We treat Claude Code, Codex, Gemini CLI, Kiro, Cursor, and Windsurf as parallel execution environments. The matrix is the contract.
- **A standards body.** We propose patterns we've found useful; consumers fork what they need and ignore the rest.

## Acknowledgments

SpecRoute generalizes patterns from internal Enovatr Labs codebases into a public framework. Specific design choices (the spec triplet, the phased master-prompt pattern, the per-vendor runtime layouts) draw on production usage across multiple projects. Sanitized for public release.

The agentic-engineering ecosystem moves quickly. We watch the upstream conventions of the agent CLIs we support and update SpecRoute in lock-step when they evolve (see commit history for examples — the ~30-event Claude Code hook taxonomy and the cross-vendor hook coverage were added when those vendors shipped or expanded their hooks systems).

## License

SpecRoute is released under [Apache 2.0](LICENSE). Copyright (c) Enovatr Labs.
