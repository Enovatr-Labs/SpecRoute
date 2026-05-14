# Contributing

<!-- sources: CONTRIBUTING.md -->

SpecRoute is a community-curated framework. Contributions are **markdown content** — templates, prompts, agent definitions, skills, hooks, workflows, rules — not application code.

Full guide: [CONTRIBUTING.md](https://github.com/Enovatr-Labs/SpecRoute/blob/main/CONTRIBUTING.md). Community standards: [CODE_OF_CONDUCT.md](https://github.com/Enovatr-Labs/SpecRoute/blob/main/CODE_OF_CONDUCT.md). Security reports: see [[Security]].

## Before you start

1. Read [[Home]] and [[Philosophy]] for project framing.
2. Skim the [[Worked Example]] for the artifact shapes end-to-end.
3. Search [issues](https://github.com/Enovatr-Labs/SpecRoute/issues) and [pull requests](https://github.com/Enovatr-Labs/SpecRoute/pulls) for related work in flight.

## What we accept

| Contribution type | Examples |
|---|---|
| **New template** | A spec template, PRD template, agent template, skill template |
| **New example** | A worked PRD, a real spec triplet, an agent roster for a domain |
| **New rule / workflow** | An engineering standard, a review-loop pattern |
| **New vendor support** | Runtime layout for a new agent CLI, a new column in the [[Vendor Matrix]] |
| **Documentation improvement** | Sharper explanations, missing decision frameworks |
| **Correction** | Typos, broken links, outdated frontmatter contracts |

## What we don't accept

- Domain-specific business logic (finance, healthcare, etc.) — keep examples generic.
- Vendor-favoring changes that break parity in the supported matrix.
- Build tooling, package configs, or test runners — SpecRoute is content, not an application.
- Templates that aren't immediately usable (no abstract checklists, no theory-only docs).
- Material extracted from a private codebase without [[Sanitization]].

## Contribution workflow

1. **Open an issue first** for non-trivial changes (new vendor, new top-level directory, new template category). Smaller changes (typo fix, single template improvement) can go straight to a PR.
2. **Fork and branch.** Branch names: `feat/<short-name>`, `fix/<short-name>`, `docs/<short-name>`.
3. **Follow the spec-driven flow** for substantial additions: PRD-style issue → spec/design comment → tasks checklist → PR.
4. **Match the existing shape.** Look at sibling files for the established frontmatter and structure. Skills must follow the folder-per-skill convention; agents must use flat-file frontmatter. See [[Frontmatter Contracts]].
5. **One concern per PR.** A new template, a doc improvement, and a runtime layout addition are three PRs.
6. **Respect TODO markers.** They mark places where real-world examples should be added later. Don't fill them with invented content.

## Quality bar

- **Practical, not theoretical.** Templates must be immediately usable — fill-in-the-blanks, not lectures.
- **Vendor-neutral by default.** Claude-specific content goes under `prompts/claude/` or `runtimes/.claude/`. Universal content goes under `prompts/shared/` or is documented as cross-vendor.
- **Sanitize.** No proprietary business logic, customer data, secrets, internal endpoints, or named private products. See [[Sanitization]].
- **Markdown quality.** Consistent heading levels, fenced code blocks with language tags, tables for matrices, no broken links.

## Pull request expectations

- A clear title and a short description that says **what** changed and **why**.
- Link the related issue.
- Note which vendors the change affects (or "vendor-neutral" if shared).
- Confirm sanitization in the PR description.
- Run `/audit` locally before opening the PR — fix anything flagged.

## License

By contributing, you agree your contributions are licensed under the [Apache 2.0 License](https://github.com/Enovatr-Labs/SpecRoute/blob/main/LICENSE).

## See also

- [[Quickstart]] — get a working setup
- [[Implementation Team]] — the `.claude/` agents that contributors invoke
- [[Roadmap]] — current priorities + open `☐` items
- [[Code of Conduct]]
