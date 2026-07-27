# Philosophy

<!-- sources: agentic-docs/philosophy.md -->

SpecRoute exists because **agent-assisted development drifts when there is no contract for what is being built.** This page captures the operating beliefs that shape every template, prompt, and convention.

For the canonical version with full prose, see [`agentic-docs/philosophy.md`](https://github.com/Enovatr-Labs/SpecRoute/blob/main/agentic-docs/philosophy.md).

## What we believe

### 1. Specs first, code second
A specification is cheaper to change than code. When humans and agents agree on what they're building *before* any line is written, implementation compresses from "exploratory negotiation" to "execution." Code generated without a spec is ungovernable: there's nothing to review against, nothing to validate, no acceptance criterion.

### 2. Agents are senior collaborators, not autocomplete
Modern agent CLIs are capable of architecture decisions, multi-file refactors, and end-to-end feature implementation. Treating them as autocomplete wastes that capacity. Given a real spec, they produce real software with the same review surface as a human contributor.

### 3. Vendor neutrality is a contract, not a wish
Tooling churns across Claude Code, Codex, Gemini CLI, Kiro, Cursor, and Devin Desktop. SpecRoute's value is **content** — PRDs, specs, prompts, agents, rules, skills, commands, hooks. The runtime layout is a thin shell adapting that content to each vendor. A consumer can switch vendors without rewriting their PRDs and specs; only the runtime shell changes. See [[Vendor Matrix]].

### 4. Templates that don't produce valid artifacts are theory
Every template must, when filled in by a competent contributor, produce a working artifact. Frontmatter contracts must be concrete; cross-references must resolve; worked examples must exist alongside templates. Abstract "checklist masquerading as deliverable" templates are rejected.

### 5. Sanitization is non-negotiable for shared frameworks
SpecRoute is open-source, derived from internal codebases. Patterns generalize freely; product names, customer data, and proprietary domain logic do not. See [[Sanitization]].

### 6. Maintainability over cleverness
Three obvious lines beat one clever abstraction. Folder-per-skill, flat-file agents, explicit per-vendor runtime dirs — deliberate choices favoring readability over elegance.

### 7. Two-tier docs
Root context files stay short (loaded into every agent conversation). Deep references live in `agentic-docs/`. See [[Two-Tier Docs Pattern]].

## What we reject

- **Implementation without specs.** "I'll figure it out as I go" is not a workflow.
- **Vendor-specific defaults that masquerade as universal.** Claude-specific content goes under `prompts/claude/` or `runtimes/.claude/`; universal goes under `prompts/shared/`.
- **Theory in template files.** A template is not the place to explain why spec-driven matters. That's what `agentic-docs/` is for.
- **Build tooling, test runners, app frameworks.** SpecRoute is markdown content. Scripts exist only when load-bearing (sanitization, cross-vendor sync, MCP rendering).

## What follows from these beliefs

- The PRD template is long because real PRDs are long. The lightweight PRD exists for genuinely small features, not as a way to skip the work.
- The spec triplet (requirements + design + tasks) uses stable IDs because tasks must back-reference requirements without ambiguity.
- The phased master-prompt pattern (`000_GLOBAL_MASTER` + `phase{N}/000_MASTER_<phase>` + numbered task prompts) exists because multi-week migrations need an execution structure, not a wall of text.
- Every agent definition has a "Don't use for" section — it keeps agent boundaries crisp.
- The PreToolUse sanitization gate is on by default because the cost of a one-time leak vastly exceeds the cost of a few false-positive blocks.

## What this is not

- Not a SaaS, CLI, or code generator.
- Not a claim that humans should not write code, or that agents should write all of it.
- Not a standards body. SpecRoute proposes patterns; consumers fork what they need and ignore the rest.

## See also

- [[Spec-Driven Development]] — the flow these beliefs produce
- [[Agentic Coding Model]] — how the four primitives compose
- [[Automation Decision Framework]] — the decision matrix
