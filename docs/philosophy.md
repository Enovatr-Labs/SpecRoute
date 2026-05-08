# Philosophy

SpecForge exists because agent-assisted development drifts when there is no contract for *what* is being built. This document captures the operating beliefs that shape every template, prompt, and convention in the repository.

## What we believe

### 1. Specs first, code second

A specification is cheaper to change than code. When humans and agents agree on what they're building before any line is written, the implementation step compresses from "exploratory negotiation" to "execution." Code generated without a spec is ungovernable: there's nothing to review against, nothing to validate, no acceptance criterion. SpecForge treats `PRD → spec triplet → tasks → implementation` as the canonical flow, not a recommendation.

### 2. Agents are senior collaborators, not autocomplete

Modern agent CLIs are capable of architecture decisions, multi-file refactors, and end-to-end feature implementation. Treating them as autocomplete wastes that capacity. SpecForge's templates and prompts assume agents are participating in design — given a real spec, they produce real software, with the same review surface as a human contributor.

### 3. Vendor neutrality is a contract, not a wish

Tooling churns. Claude Code, Codex, Gemini CLI, Kiro, Cursor, Windsurf — and whatever ships next — each have their own runtime conventions. SpecForge's value is the **content** (PRDs, specs, prompts, agent definitions, rules, skills, commands, hooks). The runtime layout is a thin shell that adapts the same content to each vendor's expectations. A SpecForge consumer can switch vendors without rewriting their PRDs and specs; only the runtime shell changes.

### 4. Templates that don't produce valid artifacts are theory

Every template in SpecForge must, when filled in by a competent contributor, produce a working artifact. Frontmatter contracts must be concrete. Cross-references must resolve. Worked examples must exist alongside templates. We reject "abstract" templates — checklists masquerading as deliverables.

### 5. Sanitization is non-negotiable for shared frameworks

SpecForge is open-source, derived from internal codebases. Patterns generalize freely; product names, customer data, and proprietary domain logic do not. The sanitization wordlist (`.claude/.forbidden-strings.txt`) is gitignored on purpose: the framework should never carry a permanent record of what it was extracted from.

### 6. Maintainability over cleverness

Three obvious lines beat one clever abstraction. Repeated patterns beat premature reuse. SpecForge prefers contributors reading existing files and copying the shape over teaching them a meta-language. The folder-per-skill convention, the flat-file agent layout, the explicit per-vendor runtime dirs — these are deliberate choices to favor readability over elegance.

### 7. Two-tier docs

Root context files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) stay short — they're loaded into every agent conversation. Deep references live in `docs/`. Long context files crowd out the user's actual question; short ones force discipline about what's actually load-bearing.

## What we reject

- **Implementation without specs.** "I'll figure it out as I go" is not a workflow; it's a bug report waiting to happen.
- **Vendor-specific defaults that masquerade as universal.** If a pattern is Claude-specific, it goes under `prompts/claude/` or `runtimes/.claude/`. If it's universal, it goes under `prompts/shared/`.
- **Theory in template files.** A template is not a place to explain why spec-driven coding matters. That's what `docs/` is for.
- **Build tooling, test runners, app frameworks.** SpecForge is markdown content. We add scripts only when they're load-bearing for the framework's correctness (sanitization, cross-vendor sync, MCP rendering).

## What follows from these beliefs

- The PRD template is long because real PRDs are long. The lightweight PRD exists for genuinely small features, not as a way to skip the work.
- The spec triplet (requirements + design + tasks) has stable IDs because tasks must back-reference requirements without ambiguity.
- The phased master-prompt pattern (`000_GLOBAL_MASTER` + `phase{N}/000_MASTER_<phase>` + numbered task prompts) exists because multi-week migrations need an execution structure, not a wall of text.
- The "Don't use for" section in every agent definition is load-bearing — it's how we keep agent boundaries crisp.
- The PreToolUse sanitization gate is on by default because the cost of a one-time leak vastly exceeds the cost of a few false-positive blocks.

## What this is not

SpecForge is not:

- A SaaS, a CLI, a code generator, or an opinionated framework on top of any single vendor.
- A claim that humans should not write code, or that agents should write all of it.
- A standards body. We propose patterns that we've found useful; consumers fork what they need and ignore the rest.

It is, simply, a set of templates and conventions that make agent-assisted engineering legible and reviewable across the vendors that exist today and the ones that will exist tomorrow.
