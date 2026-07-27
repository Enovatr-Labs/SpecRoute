# Multi-Agent Orchestration

<!-- sources: agentic-docs/multi-agent-orchestration.md, skills/examples/all-hands/SKILL.md -->

How one user-invoked entry point fans work across a roster of autonomous agents and synthesizes the results. SpecRoute ships this as the **all-hands** pattern.

## It is a composition, not a fifth primitive

SpecRoute has four primitives — skill, agent, command, hook — and [[Automation Decision Framework]] says that if two answers in the decision tree come back "yes," the split is wrong.

All-hands looks like a violation: the user invokes it by name *and* it delegates autonomously. It isn't. It is a **skill whose work product is delegation** — the coordinator asks the user nothing about *how* to do the work, it asks the roster.

```
Skill (all-hands)              the user-invoked entry point and coordinator
  └── Agents (many)            the autonomous specialists doing the work
        └── Hooks              always-on enforcement, firing on every edit they make
  └── Commands (/audit, ...)   the deterministic validation gates it runs
```

## Why you need one

Trigger phrases solve the single-agent case well — "review this spec" finds `spec-reviewer`. They solve the *multi*-agent case badly, because the user would have to know which six specialists a change implicates, and in what order. That knowledge lives in the roster, not in the user's head. All-hands moves the routing decision from the user to a coordinator that can read the roster.

## The six mechanisms

Drop any one and it degrades in a predictable way.

| # | Mechanism | Drop it and… |
|---|---|---|
| 1 | **Roster-as-registry** — the roster's agent column is the portable agent-slug registry | the coordinator hallucinates specialists |
| 2 | **A compressed routing index inside the skill** — department → trigger keywords → agents | it reads the whole roster before any work starts |
| 3 | **An explicit anti-fan-out rule** — "relevant subset, never all of them" | every run costs the full roster and returns noise |
| 4 | **Wave-based parallelism** — waves of ~4–6, file scopes proven disjoint first | concurrent agents clobber each other's edits |
| 5 | **A veto class** — named blocking concerns that outrank other specialists | blocking findings become "follow-up TODOs" and ship |
| 6 | **A fixed pipeline + mandated report schema** — including "state skipped steps honestly" | you get a confident summary of work nobody checked |

For SpecRoute the veto classes are **sanitization**, **vendor neutrality**, and **frontmatter contracts**. `sanitization-auditor` holds an absolute veto.

## Designing the departments

Departments are **routing buckets**, not an org chart:

- Group by the *kind of work*, not seniority.
- Every agent belongs to exactly one department. Ambiguity means the boundary is wrong.
- Keep the trigger column keyword-dense and lowercase — it is matched against free text.
- 4–9 agents per row; more means the department should split.

When two agents look interchangeable, record the distinction in the roster's **Agent Complement Map** as an "X vs Y" phrase — *strategy vs implementation*, *policy vs monitoring*. That is how rosters avoid accumulating near-duplicates.

## Keeping the roster honest

An orchestrator is only as good as the roster it routes over, and rosters rot.

The defense is to make every count **regenerable**: ship the shell command that produces it next to the number, and stamp the document with the date it was last verified against disk. A roster whose claims can be re-derived in one command is a testable artifact; one whose claims are hand-maintained is a rumor.

## Cross-vendor notes

The pattern needs one capability: **an agent can spawn subagents.** All supported vendors ship subagents, so it ports — but:

- The **skill body is portable**; `tools/sync-skills.py` keeps it in sync across all six runtime layouts.
- The **frontmatter is not** — each vendor has its own contract. See [[Frontmatter Contracts]].
- The **spawn tool, argument names, and agent-file shape vary**. Write against the portable roster slug and include the role brief in the dispatch prompt.
- Assume one level of nesting unless you have verified otherwise.

## When not to use it

- One well-scoped task with an obvious owner — invoke that agent directly.
- Answering a question — orchestrators implement, they don't explain.
- Anything needing user judgment mid-flow — that's an interactive skill.
- Release and commit gates — see [[Workflow Release Readiness]].

## See also

- [[Automation Decision Framework]] · [[Agentic Coding Model]] · [[Agents]] · [[Skills]]
- [[Cross-Vendor Sync]] — how the shared skill body stays in sync
