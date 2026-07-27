# Multi-Agent Orchestration

How one user-invoked entry point fans work across a roster of autonomous agents and
synthesizes the results. This is the **all-hands** pattern.

## It is a composition, not a fifth primitive

SpecRoute has four primitives - skill, agent, command, hook - and
[`automation-decision-framework.md`](automation-decision-framework.md) says that if two
answers in the decision tree come back "yes," the split is wrong.

All-hands looks like a violation: the user invokes it by name *and* it delegates
autonomously. It isn't. It is a **skill whose work product is delegation** - the
coordinator asks the user nothing about *how* to do the work, it asks the roster.
The primitives compose exactly as designed:

```
Skill (all-hands)              the user-invoked entry point and coordinator
  └── Agents (many)            the autonomous specialists doing the actual work
        └── Hooks              always-on enforcement, firing on every edit the agents make
  └── Commands (/audit, ...)   the deterministic validation gates it runs in Phase 4
```

Nothing new is introduced. What is new is the **coordination contract** between them.

## Why you need one

A roster of a dozen-plus agents has a discovery problem. Trigger phrases handle the single-agent
case well - "review this spec" finds `spec-reviewer`. They handle the *multi*-agent case
badly, because the user would have to know which six specialists a change implicates and
in what order. That knowledge lives in the roster, not in the user's head.

All-hands moves the routing decision from the user to a coordinator that can read the roster.

## The six mechanisms

A working orchestrator needs all six. Drop one and it degrades in a predictable way.

### 1. Roster-as-registry

The roster table's agent column is the **portable agent-slug registry**. The slug you write
in a markdown table identifies the specialist; each runtime maps that slug to its native
dispatch API and agent-file shape. That identity is what lets a document act as a dispatch
registry, and the orchestrator must state it explicitly - otherwise the coordinator invents
agent names that don't exist.

*Drop it and:* the coordinator hallucinates specialists.

### 2. A compressed routing index

The skill carries its own `Department → engage when → representative agents` table,
separate from the full roster. Three columns, one row per department, trigger keywords
in the middle column.

*Drop it and:* the coordinator must read the entire roster on every invocation, burning
context before any work starts.

### 3. An explicit anti-fan-out rule

"Engage the relevant subset, never all of them," stated with concrete counter-examples of
irrelevant pairings. Without a stated rule the default behavior is to convene everyone,
because that *looks* thorough.

*Drop it and:* every invocation costs the full roster and returns mostly noise.

### 4. Wave-based parallelism with a disjointness precondition

Batch independent calls into one message; work in waves of ~4-6; **only parallelize
agents whose file scopes do not overlap.** Each agent's `Owns` section is the proof
obligation - check it before launching, not after. Sequence anything sharing a file.
Where the runtime offers isolated worktrees, use them for heavy concurrent writers.

*Drop it and:* concurrent agents clobber each other's edits.

### 5. A veto class

A named set of concerns that halts the pipeline and outranks other specialists. For
SpecRoute: **sanitization**, **vendor neutrality**, **frontmatter contracts**. For a
product codebase, more typically security, compliance, and data integrity.

The point is that these are not opinions to be balanced against velocity - they are
blocking. Naming them in advance is what makes the coordinator stop instead of negotiate.

*Drop it and:* blocking findings get recorded as "follow-up TODOs" and ship.

### 6. A fixed pipeline with a mandated report schema

Five phases - intake/triage → parallel planning → synthesis → implementation squads →
review/validate/harden - closing with a report that must state **what was actually run,
with actual results, and which steps were skipped**.

The honesty clause is load-bearing. An orchestrator that summarizes optimistically is
worse than no orchestrator, because it launders unverified work as reviewed.

*Drop it and:* you get a confident summary of work nobody checked.

## Designing the departments

Departments are **routing buckets**, not an org chart. Rules that hold:

- Group by **the kind of work**, not seniority.
- Every agent belongs to exactly one department. Ambiguity means the boundary is wrong.
- Keep the middle column keyword-dense and lowercase - it's matched against a free-text
  work item, so it should read like the words a user would actually type.
- 4-9 representative agents per row. More than that and the department should split.

When two agents look interchangeable, record the distinction in the roster's
**Agent Complement Map** (`New Agent | Existing Complement | Distinction`) as an
"X vs Y" phrase - *strategy vs implementation*, *policy vs monitoring*,
*architecture vs measurement*. This is how rosters avoid accumulating near-duplicates.

## Keeping the roster honest

An orchestrator is only as good as the roster it routes over, and rosters rot: agents get
added, renamed, retired, and the table drifts from disk.

The defense is to make every count in the roster **regenerable** - ship the shell command
that produces it next to the number, and stamp the document with the date it was last
verified against disk. A roster whose claims can be re-derived in one command is a
testable artifact; one whose claims are hand-maintained is a rumor.

See [`agents/roster.md`](../agents/roster.md) for the template.

## Cross-vendor notes

The pattern needs one runtime capability: **an agent can spawn subagents.** All six
supported vendors ship subagents (see [`agent-cli-integrations.md`](agent-cli-integrations.md)),
so the pattern ports - but the details differ:

- The **skill body is portable**; `tools/sync-skills.py` keeps it in sync across runtimes.
- The **frontmatter is not** - each vendor has its own contract.
- The **spawn tool's name, argument names, and agent-file format vary** by vendor. Write the
  skill against the portable roster slug and include the role brief in the dispatch prompt.
- Vendors differ in whether subagents can themselves spawn subagents. Assume one level
  of nesting unless you have verified otherwise.

## When not to use it

- **One well-scoped task with an obvious owner.** Invoke that agent directly.
- **Answering a question.** Orchestrators implement; they don't explain.
- **Anything needing user judgment mid-flow.** That's an interactive skill.
- **Release and commit gates.** Keep those as their own deterministic workflow -
  see [`../workflows/release-readiness.md`](../workflows/release-readiness.md).

## Where to read next

- [`automation-decision-framework.md`](automation-decision-framework.md) - the four primitives.
- [`agentic-coding-model.md`](agentic-coding-model.md) - how they compose.
- [`agents/roster.md`](../agents/roster.md) - the roster template this pattern routes over.
- [`skills/examples/all-hands/SKILL.md`](../skills/examples/all-hands/SKILL.md) - the
  consumer-facing template.
- [`.claude/skills/all-hands/SKILL.md`](../.claude/skills/all-hands/SKILL.md) - this
  repository's own working instance.
