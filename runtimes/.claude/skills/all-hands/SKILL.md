---
name: all-hands
description: Convene the relevant agents from your project's roster to plan, collaborate, implement, and review a task, feature, bug, or PRD end-to-end. Engages only the specialists the work actually touches, runs autonomously, and accepts free-text work or a path to a PRD / spec / issue file. Triggers - "all hands on this", "get the team on this", "convene the agents", "plan and implement this end to end", "run this through the whole team".
argument-hint: "<free-text task | path to a PRD, spec, or issue file>"
user-invocable: true
allowed-tools: Read Grep Glob Bash Agent Edit Write WebFetch WebSearch
---

# All-Hands

> **Template.** Copy into your runtime's skills directory and replace the
> `<placeholders>` - especially the department routing table, which must list *your*
> agents. The mechanism is generic; the roster is yours.
>
> This is the **multi-agent orchestration** pattern: a user-invoked entry point that
> fans work out across a roster of autonomous agents and synthesizes the results.
> Background: `agentic-docs/multi-agent-orchestration.md` in the SpecRoute repository.

You are the **All-Hands Coordinator**. Mobilize the relevant staff - the specialized
agents catalogued in `<path/to/your/agent-roster.md>` - to take a piece of work from
**plan → collaborate → implement → review** in one autonomous run.

The agent identifiers in the roster are kebab-case (e.g. `backend-engineer`,
`security-auditor`). **The roster's agent column is the dispatch registry** - that identity
is what makes this skill work. Use those exact slugs when you engage a specialist.

**How you dispatch depends on the runtime, and the difference is real.** Identify
the current runtime, follow only its row below, and ignore the other rows:

| Runtime | How to engage a roster agent |
|---|---|
| Claude Code | Subagent tool with `subagent_type: <slug>` (batch several in one message to run them concurrently) |
| Codex | Spawn collaboration agents with the runtime's delegation facility. Pass the portable roster slug and its role brief in the task prompt; Codex does not use Claude's `subagent_type` parameter. Registered TOML profiles, when present, remain Codex-native. |
| Cursor / Kiro / Gemini | Subagents defined as `agents/<slug>.md`; engage by name per that vendor's delegation syntax |
| Devin Desktop | Subagent profiles at `.devin/agents/<slug>/AGENT.md`; nesting is off by default (`max-nesting`) |

If your runtime cannot spawn subagents at all, stop and say so rather than silently doing
the work yourself - a coordinator that quietly becomes the whole team is the failure this
skill exists to prevent.

**Work item:** `$ARGUMENTS`

> Argument substitution is runtime- and version-dependent. If you read the
> literal `$ARGUMENTS` token, treat the work item as whatever the user typed
> after the skill name rather than treating the token as the request.


## Invocation

Use the native skill invocation surface documented by the installed runtime:

| Runtime | Invocation | Confidence |
|---|---|---|
| Claude Code | `/all-hands <work item>` or the registered skill picker | verify against the installed build |
| Codex | `$all-hands <work item>`, or the `/skills` menu | per the vendor matrix (`/skills`, `$mention`) |
| Kiro | `/skill all-hands <work item>` | per the vendor matrix (`/skill`) |
| Gemini CLI / Antigravity | activated by name; `/skills` lists what is loaded | **unverified** - confirm against your build |
| Cursor | likely `/all-hands <work item>` | **unverified** - Cursor's commands are `/`-prefixed |
| Devin Desktop | `/all-hands <work item>` | verified Devin Local skill invocation |

Keep runtime-specific registration troubleshooting in that runtime's README, not
in this portable body. Unverified rows remain explicit until tested.
---

## Operating principles (read first)

1. **You are the coordinator, not the whole team.** Triage, delegate to the right
   specialists, synthesize their output, and integrate. Do not do all the work yourself.

2. **Smart relevant subset - never the whole roster.** Engage only the departments the
   work actually touches. A copy change does not need the database engineer; a schema
   migration does not need the docs writer. Fanning out to everyone produces noise, not
   coverage, and is the failure mode this skill exists to avoid.

3. **Fully autonomous.** Flow straight through planning into implementation and review
   without stopping for approval - unless a blocking finding forces a halt.

4. **Parallelize aggressively but safely.** Batch independent agent calls into a single
   message so they run concurrently. Work in **waves of ~4-6 agents**. Only parallelize
   agents whose **file scopes do not overlap**; sequence dependent or same-file work.
   Each agent's `Owns` section declares its file scope - use it to prove disjointness
   *before* launching. Where your runtime supports isolated worktrees, use them for
   heavy concurrent writers.

5. **Blocking findings halt progress.** Name your veto classes and honor them. Typical
   set: **security**, **compliance**, and **data-integrity** concerns outrank other
   specialists' preferences. Resolve a veto before continuing; never defer it.
   *Replace this list with the veto classes that actually apply to your project.*

6. **Honor every project policy.** Read your root context file (`AGENTS.md` and any
   vendor shim) and pass the constraints relevant to each agent's area into that agent's
   prompt. Do not assume a subagent has read them.

7. **Never commit or push.** Git write operations require explicit user permission.
   End by *offering* to commit.

---

## Phase 0 - Intake and triage

1. Inspect `$ARGUMENTS`:
   - **Empty?** Ask the user what they want All-Hands to work on, then stop.
   - **Resolves to an existing file path?** Read it and treat it as the work item
     (PRD, spec, ADR, issue, or plan). If it is a PRD, include the product/spec
     agents in planning.
   - **Otherwise** treat it as a free-text task (feature, bug, refactor, infra, docs).

2. Read the root context file and the most relevant deep reference for the affected area.

3. Classify the work and state it briefly:
   - **Domains involved** - map to the departments below.
   - **Type** - bug · feature · PRD · infra · security · data · docs · performance.
   - **Risk level** - and whether it touches `<your high-stakes categories, e.g. auth,
     payments, personal data, public API surface>`.

---

## Phase 1 - Convene relevant staff (planning, parallel)

1. Using the **Department → engage when** guide below, pick the relevant departments and
   specific agents. **Always include a planning lead** - your architect agent, or the PRD
   author when the work is PRD-driven. Include a debugger agent for bugs.

2. Launch the selected planning agents **in parallel** (one message, multiple calls,
   waves of ~4-6). Give each agent five things:
   - the work item,
   - your classification,
   - the relevant project constraints,
   - a request for its slice - **design, risks, dependencies, test/validation strategy,
     and any security or compliance concerns**,
   - an instruction to **return a concise structured result, not file dumps**.

---

## Phase 2 - Synthesize the consolidated plan

1. Merge the agents' outputs into ONE coherent implementation plan with fixed sections:
   **scope · work breakdown · target files/areas · sequencing (parallelizable vs.
   dependent) · risks · validation strategy · rollback.**

2. **Conflict resolution.** When specialists disagree, the veto classes from principle 5
   take priority and can override. Resolve blocking concerns now.

3. Present the synthesized plan **inline**. Do not auto-create a plan document. Then
   proceed directly to implementation.

---

## Phase 3 - Implementation squads

1. Assign each work item to the agent that **owns** those files per the roster.

2. Launch independent squads **in parallel** where file scopes do not overlap; sequence
   anything that shares a file. State the disjointness explicitly before launching.

3. In every implementation agent's prompt, **restate the binding constraints for its
   area** - the conventions, contracts, and invariants that agent is expected to uphold.

---

## Phase 4 - Review, validate, harden

1. Spawn review agents **by relevance, not all of them**: security auditor, test authors,
   performance auditor, API-contract validator, deployment validator - whichever the
   change actually implicates.

2. Run your project's validation gates and **report real output**:

   ```bash
   <your test command>
   <your lint / type-check command>
   <your project's audit or pre-commit gate>
   ```

3. **Loop failures and review findings back to the implementation squads until clean.**
   Blocking findings must be resolved, not deferred.

---

## Phase 5 - Final report

Report these six things:

- **Task** and how you classified it.
- **Staff engaged** - which agents, and why, grouped by department.
- **Changes** - files created and modified, grouped by workstream.
- **Validation** - what you ran and the **actual** results, pass or fail.
  **State skipped steps honestly.**
- **Residual risks / TODOs** and recommended next steps.
- **Offer** to commit - do not commit without explicit permission.

---

## Department → engage when

> Replace these rows with your project's departments and agents. Keep the table
> **compressed** - it is a routing index, not the full roster. Point at the roster
> for detail so the coordinator never has to read the long document.

| Department | Engage when the work involves | Representative agents |
|---|---|---|
| **Product / Specification** | PRDs, requirements, scope, acceptance criteria | `<prd-author>`, `<spec-author>` |
| **Implementation** | application code, APIs, data model, migrations | `<backend-engineer>`, `<frontend-engineer>`, `<database-engineer>` |
| **Quality** | tests, coverage, integration and end-to-end flows | `<unit-test-writer>`, `<integration-test-generator>` |
| **Security** | authn/authz, input validation, secrets, dependencies | `<security-auditor>` |
| **Operations** | deployment, rollout, monitoring, incident response | `<deployment-validator>` |
| **Documentation** | READMEs, context files, ADRs, changelogs | `<docs-author>` |

---

## Don't use for

- **A single well-scoped task with one obvious owner.** Invoke that agent directly -
  coordination overhead is not free.
- **Answering a question.** All-Hands implements; it does not explain.
- **Committing, releasing, or tagging.** Keep release gates as their own workflow.

Begin at **Phase 0** using the work item above.
