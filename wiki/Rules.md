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
├── gemini-rules.md                  Gemini / Antigravity-specific surfacing
├── cursor-rules.md                  Cursor MDC conventions
├── kiro-rules.md                    Kiro steering conventions
├── devin-rules.md                   Devin Desktop rule conventions, including Cascade compatibility
└── steering/
    ├── always-on-template.md        inclusion: always
    └── file-match-template.md       inclusion: fileMatch
```

## `rules/` is not `.claude/rules/`

Two different things share the word. Claude Code shipped a native `.claude/rules/` feature; SpecRoute's top-level `rules/` directory predates it and means something else.

| | SpecRoute `rules/` | Claude Code `.claude/rules/` |
|---|---|---|
| What it is | Documentation - vendor-neutral standards plus per-vendor explainers of how each CLI surfaces them | A runtime feature - modular instruction files the CLI loads itself |
| Who reads it | Humans, and agents following a link from a root context file | The Claude Code runtime, automatically |
| Frontmatter | None | One optional field, `paths:` (glob list) |
| Location | Repo root `rules/` | `.claude/rules/` per project, `~/.claude/rules/` per user |

SpecRoute's directory is deliberately **not** renamed - its content is vendor-neutral and several vendors mirror it. Putting a file in the top-level `rules/` directory does nothing on its own; to make it active in Claude Code, copy the body into `.claude/rules/<topic>.md`.

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
| Claude Code | `.claude/rules/*.md` or `CLAUDE.md` | `.claude/rules/` is auto-loaded and discovered recursively; optional `paths:` glob list scopes a file to matching edits, otherwise it loads at launch at `CLAUDE.md` priority. `~/.claude/rules/` loads first. |
| Codex | `AGENTS.md` body | Via the root context file. Codex has **no** Markdown rule loader - its own `.rules` files are Starlark command-approval policy, a different thing. |
| Gemini CLI / Antigravity | `GEMINI.md` body | Via the root context file. No rule-directory feature. `AGENTS.md` is **not** read unless `context.fileName` opts in. |
| Cursor | `.cursor/rules/*.mdc` | Frontmatter `alwaysApply` or `globs`. `.cursorrules` is removed in practice - undocumented and reported non-functional. |
| Kiro | `.kiro/steering/*.md` | Frontmatter `inclusion: always` or `fileMatch` |
| Devin Desktop | `.devin/rules/*.md` (preferred); Cascade also accepts `.windsurf/rules/*.md` | Frontmatter `trigger: always_on`, `model_decision`, `glob`, or `manual` |

Three vendors now offer file-scoped rule loading under different field names - Claude's `paths:`, Cursor's `globs`, Kiro's `inclusion: fileMatch` - and two (Codex, Gemini) offer none at all. Rule content ports across vendors; rule *loading semantics* do not.

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
