# Spec Examples

Worked specifications demonstrating how the templates are used. The canonical end-to-end worked example lives in [`../../examples/sample-project/`](../../examples/sample-project/), which exercises the full spec triplet against a generic `user-search` feature.

Smaller examples in this directory may use any template. Generic domains only - no proprietary business logic.

When adding an example:

1. Create `<slug>/` for spec triplets (`requirements.md`, `design.md`, `tasks.md`) or a single file for lightweight feature specs / technical specs / ADRs.
2. Use stable requirement IDs (`R1.1`, `NFR-1.1`).
3. Confirm task back-refs cover every requirement.
4. Run `/audit` before committing.
