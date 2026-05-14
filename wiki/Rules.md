# Rules

<!-- sources: rules/README.md -->

Engineering standards and conventions. Vendor-neutral content lives in the top-level files; per-vendor format conventions live in `<vendor>-rules.md`; rule-loading semantics live in `steering/`.

For the canonical reference, see [`rules/README.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/rules/README.md).

## Directory layout

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
    ├── always-on-template.md        inclusion: always
    └── file-match-template.md       inclusion: fileMatch
```

## How to use this directory

1. **Pick what to enforce.** Read the four shared rule files (`engineering`, `code-review`, `security`, `documentation`). These are SpecRoute's defaults; adapt to your project.
2. **Pick how to enforce it per vendor.** Each `<vendor>-rules.md` file explains how that vendor surfaces rules.
3. **Choose loading semantics.** `steering/` documents the two modes (always-on, file-pattern-matched).

## Why this split

The shared rule files are **content**; the per-vendor files are **mechanism**. Keeping them separate means:

- Updating a rule (content) is one edit.
- Adding a new vendor is one new file — existing rules don't move.
- Vendors that don't natively load rules still surface the content via root context files.

## Loading semantics: always-on vs file-pattern-matched

Two modes:

| Mode | Loaded when | Use for |
|---|---|---|
| **Always-on** | Loaded into every agent conversation | Cross-cutting standards (sanitization, security baselines, code-review bar) |
| **File-pattern-matched** | Loaded only when the agent is operating on files matching a glob | Per-language conventions (`.py` rules, `.tsx` rules, infra rules) |

File-pattern matching saves context budget — agents don't load Kotlin conventions when reviewing TypeScript.

## Per-vendor surfacing

| Vendor | Where rules live | Loading mechanism |
|---|---|---|
| Claude Code | `.claude/rules/` or `CLAUDE.md` | Auto-loaded via context file |
| Codex | `AGENTS.md` body or `.codex/` rules dir | Via root context file |
| Gemini CLI | `GEMINI.md` body | Via root context file |
| Cursor | `.cursor/rules/*.mdc` | Frontmatter `alwaysApply` or `globs` |
| Kiro | `.kiro/steering/*.md` | Frontmatter `inclusion: always` or `fileMatch` |
| Windsurf | `.windsurf/rules/*.md` | Frontmatter `trigger: always` or `model-decision` |

See [[Vendor Matrix]] for the full contract.

## Owner agent

Rules are owned by the `framework-docs-author` agent. Cross-cutting changes to `engineering-rules.md` cascade to per-vendor files where vendors mirror content.

## When to add a rule vs hook vs review

- **Rule** — standing constraint that should be true always. Documented in markdown; surfaces via the agent's context file.
- **Hook** — enforced automatically on a specific event (commit, write). See [[Hooks]].
- **Review item** — checked by a human or code-reviewer agent during PR review. See [[Workflow Agent Review Loop]].

A rule is a *noun* (a standard); a hook is a *trigger*; a review is a *checkpoint*. The most reliable enforcement combines all three: write the rule, add a hook for what's mechanical, train the reviewer (human or agent) to check the judgmental parts.

## See also

- [[Multi-Vendor Context Files]] — how rules surface across vendors
- [[Hooks]] — automatic enforcement
- [[Workflow Agent Review Loop]] — review-time enforcement
- [[Documentation Structure]] — `rules/` vs `workflows/` vs `agentic-docs/`
