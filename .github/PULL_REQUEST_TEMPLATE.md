<!--
SpecRoute PR template. Replace this comment block as you fill in the sections.
For substantive changes, please open an issue first to discuss the approach.
-->

## Summary

<!-- 1-3 sentences. What does this PR change and why? -->

## Linked artifact

<!-- Pick whichever applies. -->

- [ ] Linked issue: #
- [ ] Linked task ID (if implementing against a spec triplet): _Requirements: ..._
- [ ] Linked ADR (if architectural change):
- [ ] N/A (typo / doc / sanitization fix)

## Type of change

- [ ] PATCH — doc fix, sanitization, link correction, typography, content refinement
- [ ] MINOR — new vendor support / new artifact type / new skill or command or hook category / substantive new template
- [ ] MAJOR — breaking change to artifact contracts (frontmatter, spec triplet shape, vendor matrix structure, spec-driven flow itself)

See [`ROADMAP.md`](../ROADMAP.md) Versioning section for the SemVer interpretation.

## Validation

- [ ] `/audit` returns clean (sanitization, frontmatter, vendor matrix consistency, broken links)
- [ ] Cross-references resolve (any new `[text](path)` links work)
- [ ] Frontmatter contracts intact (where applicable)
- [ ] No domain-specific business logic introduced (examples remain generic)
- [ ] Vendor neutrality preserved (the matrix is the contract; new vendors mean a new column, not a fork)

## Test plan

<!-- Bulleted list of what reviewers should verify, manually or via /audit. -->

## Notes

<!-- Anything reviewers should know that doesn't fit elsewhere. -->

---

By contributing, I agree that my contributions will be licensed under the project's [Apache 2.0 License](../LICENSE) and I have read [`CONTRIBUTING.md`](../CONTRIBUTING.md) and [`CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md).
