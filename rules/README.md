# Rules

Engineering standards and conventions. Vendor-neutral content lives in the top-level files; per-vendor format conventions live in `<vendor>-rules.md`; rule-loading semantics live in `steering/`.

```
rules/
├── engineering-rules.md             vendor-neutral engineering standards
├── code-review-rules.md             review process and bar
├── security-rules.md                security cross-cuts
├── documentation-rules.md           doc standards
├── codex-rules.md                   Codex-specific surfacing
├── claude-rules.md                  Claude Code-specific surfacing
├── gemini-rules.md                  Gemini-specific surfacing
├── cursor-rules.md                  Cursor MDC conventions
├── windsurf-rules.md                Windsurf rule conventions
└── steering/
    ├── README.md
    ├── always-on-template.md        inclusion: always
    └── file-match-template.md       inclusion: fileMatch
```

## How to use this directory

1. **Pick what to enforce.** Read the four shared rule files (`engineering`, `code-review`, `security`, `documentation`). These are SpecForge's defaults; adapt to your project.

2. **Pick how to enforce it per vendor.** Each `<vendor>-rules.md` file explains how that vendor surfaces rules. The shared content from the top-level files gets referenced (or copied) into the per-vendor format.

3. **Choose loading semantics.** `steering/` documents the two modes (always-on, file-pattern-matched). Apply per rule based on context.

## Why this split

The shared rule files are content; the per-vendor files are mechanism. Keeping them separate means:

- Updating a rule (content) is one edit.
- Adding a new vendor is one new file (`<new-vendor>-rules.md`) — the existing rules don't move.
- Vendors that don't natively load rules still surface the content via root context files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`).

## Authoring

Rules are owned by the `framework-docs-author` agent. Cross-cutting changes (e.g. updating `engineering-rules.md`) cascade to per-vendor files where vendors mirror content.

## See also

- [`docs/multi-vendor-context-files.md`](../docs/multi-vendor-context-files.md) — how the canonical `AGENTS.md` and per-vendor delegation shims work.
- [`docs/automation-decision-framework.md`](../docs/automation-decision-framework.md) — when to enforce via rule vs hook vs review.
