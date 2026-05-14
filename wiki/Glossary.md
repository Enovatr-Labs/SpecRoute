# Glossary

Quick definitions for terms used throughout the wiki. Linked to the pages that go deeper.

## A

**ADR (Architecture Decision Record)** — Immutable doc capturing a single architectural choice and its rationale. Superseding requires a new ADR. See [[Specs]].

**Agent** — A defined role with model, tools, and operating principles, invokable by an agent CLI runtime. Autonomous (runs to completion without user input). See [[Agents]].

**Agentic coding** — Software engineering with AI agents as collaborators that produce reviewable software when given a spec. See [[Agentic Coding Model]].

**`AGENTS.md`** — The canonical, vendor-neutral root context file. The single source of truth that every agent CLI working in a SpecRoute-driven repo should read first. See [[Multi-Vendor Context Files]].

**Archetype** — A role concept ("what does a security agent do?"), not a file the runtime loads. Used when designing your project's roster. See [[Agents]].

**Authoring agent** — The agent in the implementation team that owns a particular artifact type (e.g. `prd-author` owns PRDs, `spec-author` owns specs). See [[Implementation Team]].

## C

**Command** — A simple slash-invoked operation. No parameters (or one argument). Always does the same thing. See [[Commands]].

**Coverage table** — Mapping in `tasks.md` of every requirement and NFR to the tasks that satisfy it. Every cell populated; no `TODO` rows. See [[Specs]].

## D

**Delegation shim** — A short (~30–50 line) per-vendor root context file (`CLAUDE.md`, `GEMINI.md`) that points at the canonical `AGENTS.md` and adds vendor-specific overrides. See [[Multi-Vendor Context Files]].

## F

**Folder-per-skill convention** — Every skill is a directory containing `SKILL.md`. Never a flat file. See [[Skills]].

**Frontmatter** — YAML block at the top of a markdown file, fenced by `---`. Required fields vary by artifact type. See [[Frontmatter Contracts]].

## G

**Global master prompt** — `000_GLOBAL_MASTER.md`, the single entry-point for a phased initiative. Names the role, mission, source-of-truth table, and phase order. See [[Prompts]].

## H

**Hook** — Event-triggered automation. Runs automatically on file edit, session start, pre-tool, etc. Sub-second target. Fails closed. See [[Hooks]].

## I

**Implementation team** — The `.claude/` directory at the repo root. Eleven agents, four skills, four commands, three hooks that build SpecRoute itself. Not the consumer template. See [[Implementation Team]].

## M

**MCP (Model Context Protocol)** — A protocol for exposing tools and resources to agent CLIs. Three vendors (Claude Desktop, Codex, Gemini CLI) consume MCP server configs in different shapes. See [[MCP Integration]].

## N

**NFR (Non-Functional Requirement)** — A requirement that constrains *how* the system performs rather than *what* it does (performance, security, observability, etc.). Stable ID format: `NFR-<N.M>`. See [[Specs]].

## P

**Phase master prompt** — `000_MASTER_<phase>.md`, the second tier in the phased master-prompt pattern. Summarizes a phase, lists prerequisites, names agent assignments. See [[Prompts]].

**PRD (Product Requirements Document)** — The business-intent layer. Full 23-section template or lightweight single-page alternative. See [[PRDs]].

**Primitive (automation primitive)** — One of the four ways SpecRoute automates work: skill, agent, command, or hook. See [[Automation Decision Framework]].

**Prompt** — A reusable instruction. Three layers: global master, phase master, task prompt. See [[Prompts]].

## R

**Requirement ID** — Stable, unique identifier (`R1.1`, `R2.3`, `NFR-1.1`). Once published, never reused. Tasks, PRs, and tests back-reference these. See [[Specs]].

**Roster (agent roster)** — Cross-vendor inventory of a project's agents, grouped by department. See [[Agents]].

**Rule** — A standing engineering constraint that's always true. Lives in `rules/`. See [[Rules]].

**Runtime** — A copy-pasteable per-vendor layout consumers drop into their own repos. See [[Vendor Matrix]] and [[Agent CLI Integrations]].

## S

**Sanitization** — Keeping proprietary content (private project names, customer data, secrets, internal endpoints) out of tracked content. Enforced via wordlist + hook + commands + agent review. See [[Sanitization]].

**Skill** — An interactive, parameterized workflow. User invokes by name; skill guides through decisions and validation checkpoints. See [[Skills]].

**Spec triplet** — `requirements.md` + `design.md` + `tasks.md`. The technical contract for a feature with stable IDs and back-references. See [[Specs]].

**Stable ID** — See "Requirement ID."

**Steering** — Kiro's term for rule files loaded at session start (`.kiro/steering/*.md`). Two modes: `inclusion: always` and `inclusion: fileMatch`. See [[Rules]].

## T

**Task prompt** — A production-grade prompt instantiating the shape: Objective / Context / Agent Assignment / Prerequisites / Task Details with current→target diff blocks / Acceptance Criteria. See [[Prompts]].

**Trigger phrase** — A literal user utterance (in quotes within an agent's `description` frontmatter) that triggers automatic agent selection. See [[Agents]].

**Two-tier docs** — Short root context files (loaded into every conversation) + deep references in `agentic-docs/` (read on demand). See [[Two-Tier Docs Pattern]].

## V

**Vendor matrix** — The table of supported agent CLIs and what each consumes (runtime dir, root context file, skills, agents, commands, hooks, MCP). Adding a new tool means a new column. See [[Vendor Matrix]].

**Vendor neutrality** — A contract: don't fold one vendor into another, don't treat any as default, every artifact uses each vendor's native shape. See [[Philosophy]].

## W

**Workflow** — An end-to-end engineering execution model. A *verb* (procedure), not a *noun* (standard). See [[Workflows]].

**Worked example** — `examples/sample-project/`. Drop-in runnable demonstration that exercises every artifact shape. See [[Worked Example]].

## See also

- [[Home]] — start here
- [[Repository Structure]] — what lives where
- [[Frontmatter Contracts]] — the required-field reference
