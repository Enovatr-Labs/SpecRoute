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
├── gemini-rules.md                  Gemini / Antigravity-specific surfacing
├── cursor-rules.md                  Cursor MDC conventions
├── kiro-rules.md                    Kiro steering conventions
├── devin-rules.md                   Devin Desktop rule conventions
└── steering/
    ├── README.md
    ├── always-on-template.md        inclusion: always
    └── file-match-template.md       inclusion: fileMatch
```

## `rules/` here is not Claude Code's `.claude/rules/`

Two different things share the word "rules". Keep them straight:

| | SpecRoute `rules/` (this directory) | Claude Code `.claude/rules/` |
|---|---|---|
| What it is | A SpecRoute documentation concept - the vendor-neutral standards plus a per-vendor explainer of how each CLI surfaces them | A Claude Code runtime feature - modular instruction files the CLI loads itself |
| Who reads it | Humans, and agents that follow a link from a root context file | The Claude Code runtime, automatically |
| Frontmatter | None | One optional field, `paths:` (glob list) |
| Location | Repo root `rules/` | `.claude/rules/` in a project, `~/.claude/rules/` for the user |

SpecRoute's directory predates the Claude Code feature and is deliberately **not** renamed - its content is vendor-neutral and several vendors mirror it. If you want Claude Code to auto-load some of this content, copy or link it into `.claude/rules/*.md`; putting a file in the top-level `rules/` directory does nothing on its own. See [`claude-rules.md`](claude-rules.md) for the mechanics.

## How to use this directory

1. **Pick what to enforce.** Read the four shared rule files (`engineering`, `code-review`, `security`, `documentation`). These are SpecRoute's defaults; adapt to your project.

2. **Pick how to enforce it per vendor.** Each `<vendor>-rules.md` file explains how that vendor surfaces rules. The shared content from the top-level files gets referenced (or copied) into the per-vendor format.

3. **Choose loading semantics.** `steering/` documents the two modes (always-on, file-pattern-matched). Apply per rule based on context.

## Why this split

The shared rule files are content; the per-vendor files are mechanism. Keeping them separate means:

- Updating a rule (content) is one edit.
- Adding a new vendor is one new file (`<new-vendor>-rules.md`) - the existing rules don't move.
- Vendors that don't natively load rules still surface the content via root context files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`).

## Authoring

Rules are owned by the `framework-docs-author` agent. Cross-cutting changes (e.g. updating `engineering-rules.md`) cascade to per-vendor files where vendors mirror content.

## See also

- [`agentic-docs/multi-vendor-context-files.md`](../agentic-docs/multi-vendor-context-files.md) - how the canonical `AGENTS.md` and per-vendor delegation shims work.
- [`agentic-docs/automation-decision-framework.md`](../agentic-docs/automation-decision-framework.md) - when to enforce via rule vs hook vs review.
