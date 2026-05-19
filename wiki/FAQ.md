# FAQ

## What is SpecRoute?

An open-source framework for **spec-driven agentic software engineering**, vendor-neutral across Claude Code, Codex, Gemini CLI, Kiro, Cursor, and Windsurf. It ships templates, prompts, agent definitions, runtime layouts, and engineering rules — **markdown content, not application code.**

See [[Home]] and [[Philosophy]].

## Is this a CLI? A package?

No. There's no `package.json`, no build step, no test suite, no lint config. SpecRoute is documentation and templates you drop into your own repository.

The only executables are sanitization-gate hooks and cross-vendor sync utilities under `tools/` — and those are intentionally minimal.

## Which agent CLIs are supported?

Six, in tiers (see [[Vendor Matrix]]):

- **Full**: Claude Code
- **Near-full**: Codex
- **Partial**: Gemini CLI
- **Specialized**: Kiro
- **Rules only**: Cursor, Windsurf

The framework's content (PRDs, specs, prompts, rules) works in any of them. Runtime-layer features (skills, agents, commands, hooks) only land where the vendor supports them.

## Can I use this with just one vendor?

Yes. You don't have to set up all six. Most teams start with one (often Claude Code or Codex), and the framework still pays off — the spec-driven flow, the templates, and the worked example don't depend on multi-vendor support.

When you add a second vendor later, the `runtimes/.<vendor>/` directory drops in and the multi-vendor context-file pattern (`AGENTS.md` + delegation shim) takes over. See [[Multi-Vendor Context Files]].

## How do I get started?

Three paths — see [[Quickstart]]:

- **Read the worked example** (5 min) — understand the artifact pipeline without touching anything.
- **Copy a template** (10 min) — bootstrap a new PRD or spec from the templates.
- **Drop the runtime in** (15 min) — copy `runtimes/.<vendor>/` into your repo and start using skills / agents / commands / hooks.

## What's the difference between an agent, a skill, a command, and a hook?

See [[Automation Decision Framework]]:

- **Skill** — interactive workflow with parameters and decision points. User invokes by name; skill walks them through.
- **Agent** — autonomous execution. User delegates a task; agent runs to completion.
- **Command** — deterministic slash operation. User types `/<name>` and gets the same result every time.
- **Hook** — event-triggered automation. Runs automatically on file edit, session start, pre-tool, etc.

Picking the wrong primitive produces friction. The decision tree in [[Automation Decision Framework]] is the load-bearing reference.

## What's the spec triplet?

`requirements.md` + `design.md` + `tasks.md`. The technical contract for a feature, with:

- **Stable IDs** (`R1.1`, `NFR-1.1`) that never get reused.
- **Back-references** — every task ends with `_Requirements: R1.1, R1.2_`.
- **Coverage table** mapping every requirement to the tasks that satisfy it.

The triplet exists because conflating *what* / *how* / *do this* is a known failure mode. See [[Specs]] and [[Spec-Driven Development]].

## Why does sanitization matter so much?

SpecRoute is open-source and is generalized from internal codebases. Private project names, customer data, and proprietary domain logic must not leak into tracked content.

Three enforcement layers (see [[Sanitization]]):

1. PreToolUse hook blocks `git commit` / `git push` / `gh pr create` if forbidden terms appear.
2. `/sanitize` for quick string-level scans during authoring.
3. `/audit` for comprehensive pre-commit sweep.

The wordlist (`.claude/.forbidden-strings.txt`) is **gitignored** on purpose — the framework should never carry a permanent record of what it was extracted from.

## Can I use SpecRoute for my closed-source project?

Yes — Apache 2.0 license. Copy what you need, adapt to your stack, ignore the rest. The sanitization gate only applies to *this* repo's tracked content; it doesn't follow your fork.

## What's the difference between `.claude/` and `runtimes/.claude/`?

- `.claude/` (at the repo root) is the **implementation team** that builds SpecRoute itself — 11 agents, 4 skills, 4 commands, 3 hooks for the SpecRoute contributors.
- `runtimes/.claude/` is the **consumer template** that you drop into your own repository.

Don't confuse them. See [[Implementation Team]].

## I found a typo / broken link / outdated reference

Open a PR. Small corrections go straight to PR; non-trivial changes should open an issue first. See [[Contributing]].

## How do I add a new vendor?

The `add-vendor` skill walks through it interactively. See [[Adding a Vendor]] for the manual steps.

## How do I report a security issue?

`security@enovatr.com` (preferred) or via [GitHub security advisory](https://github.com/Enovatr-Labs/SpecRoute/security/advisories/new). **Don't open a public issue.** See [[Security]].

## Is there a roadmap?

Yes — [[Roadmap]]. Current version is v0.2.4. Phases 1–3 are complete; Phase 4 (maturity) is in progress.

## What's a "phased master-prompt pattern"?

For multi-week initiatives, the prompt structure is:

```
000_GLOBAL_MASTER.md          single entry-point
phase0_<name>/
├── 000_MASTER_<phase>.md     phase summary
├── 001_<task>.md             production task prompt
├── 002_<task>.md
phase1_<name>/...
```

Numbered files, sorted phases, explicit agent assignments. Each task prompt instantiates a rich shape (Objective / Context / Agent Assignment / Prerequisites / Task Details with current→target diff blocks / Acceptance Criteria). See [[Prompts]] and [[Worked Example]].

## Why don't I see any code in the worked example?

Because **SpecRoute ships the inputs**, not the output. The worked example is the PRD + spec triplet + agent roster + 28 prompts + runtime layout. When you `cp -R examples/sample-project/. /path/to/new-repo/` and run `prompts/runtime/pickup-next-task.md` in Claude Code, the agents *generate* the code. See [[Worked Example]].

## How do I get help?

- General questions: [GitHub discussions or issues](https://github.com/Enovatr-Labs/SpecRoute/issues).
- Specific to a vendor: that vendor's docs + community.
- Commercial / partnership: `chika@enovatr.com`.

## See also

- [[Home]] · [[Quickstart]] · [[Glossary]]
- [[Philosophy]] — why this framework exists
