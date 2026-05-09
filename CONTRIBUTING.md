# Contributing to SpecForge

Thanks for considering a contribution. SpecForge is a community-curated framework for spec-driven agentic software engineering. Contributions are markdown content - templates, prompts, agent definitions, skills, hooks, workflows, rules - not application code.

## Before you start

1. Read the [README](README.md) to understand the artifact taxonomy and the supported vendor matrix.
2. Read [`docs/philosophy.md`](docs/philosophy.md) and [`docs/spec-driven-development.md`](docs/spec-driven-development.md).
3. Skim the worked example in [`examples/sample-feature/`](examples/sample-feature/) to see the artifact shapes end-to-end.
4. Search [issues](../../issues) and [pull requests](../../pulls) for related work in flight.

## What we accept

| Contribution type | Examples |
|---|---|
| **New template** | A spec template, PRD template, agent template, skill template |
| **New example** | A worked PRD, a real spec triplet, an agent roster for a domain |
| **New rule / workflow** | An engineering standard, a review-loop pattern |
| **New vendor support** | Runtime layout for a new agent CLI, a new column in the vendor matrix |
| **Documentation improvement** | Sharper explanations, missing decision frameworks |
| **Correction** | Typos, broken links, outdated frontmatter contracts |

## What we don't accept

- Domain-specific business logic (finance, healthcare, etc.) - keep examples generic
- Vendor-favoring changes that break parity in the supported matrix
- Build tooling, package configs, or test runners - SpecForge is content, not an application
- Templates that aren't immediately usable (no abstract checklists, no theory-only docs)
- Material extracted from a private codebase without sanitization

## Contribution workflow

1. **Open an issue first** for non-trivial changes (new vendor, new top-level directory, new template category). Smaller changes (typo fix, single template improvement) can go straight to a PR.
2. **Fork and branch.** Branch names: `feat/<short-name>`, `fix/<short-name>`, `docs/<short-name>`.
3. **Follow the spec-driven flow** for substantial additions: PRD-style issue → spec/design comment → tasks checklist → PR.
4. **Match the existing shape.** Before adding a new file, look at sibling files for the established frontmatter and structure. Skills must follow the folder-per-skill `SKILL.md` convention; agents must use the flat-file frontmatter contract. The README's vendor matrix is the contract - don't drift from it.
5. **One concern per PR.** A new template, a doc improvement, and a runtime layout addition are three PRs.
6. **Respect TODO markers.** They mark places where real-world examples should be added later. Don't fill them with invented content; if you have a real example, contribute that.

## Quality bar

- **Practical, not theoretical.** Templates must be immediately usable - fill-in-the-blanks, not lectures.
- **Vendor-neutral by default.** If a pattern is Claude-specific, put it under `prompts/claude/` or `runtimes/.claude/`. If a pattern is universal, put it under `prompts/shared/` or document it as cross-vendor.
- **Sanitize.** No proprietary business logic, customer data, secrets, internal endpoints, or named private products in any tracked file.
- **Markdown quality.** Consistent heading levels, fenced code blocks with language tags, tables for matrices, no broken links.

## Pull request expectations

- A clear title and a short description that says **what** changed and **why**.
- Link the related issue.
- Note which vendors the change affects (or "vendor-neutral" if shared).
- Confirm sanitization in the PR description.

## License

By contributing, you agree your contributions are licensed under the [Apache 2.0 License](LICENSE).

## Code of conduct

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
