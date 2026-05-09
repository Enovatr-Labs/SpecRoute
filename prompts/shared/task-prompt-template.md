# Task <NNN>: <Task Title>

> The production task-prompt shape. This is the format every numbered task prompt under `phase{N}_*/<NNN>_<task>.md` should follow.

---

## 1. Objective

<One paragraph stating what this task accomplishes. Be specific - what does the system look like after this task lands? What problem does it solve?>

## 2. Context

**PRD Reference**: `<path/to/prd.md>` - Section <N> (<section title>)
**Spec Reference**: `<path/to/specs/...>` - Requirements: R<N.M>, R<N.M>, NFR-<N.M>
**Architecture Reference**: `<path/to/architecture.md>` - Section <N> (<section title>)
**Phase Master**: `phase{N}_<name>/000_MASTER_<name>.md`
**Related Tasks**: <task IDs that produced state this depends on, or that consume this task's output>
**Current File(s)**: `<path/to/files/being/changed>`

<2–4 sentences placing this task in context. Why is it needed? Why now? What was the previous state?>

## 3. Agent Assignment

**Primary Agent**: `<agent-slug>` (see `.claude/agents/<agent>.md` for operating principles)
**Supporting Agents**:

- `<agent-slug>` - <what they help with in this task>
- `<agent-slug>` - <what they help with>

The primary agent owns the deliverable. Supporting agents are consulted for cross-cutting concerns.

## 4. Prerequisites

Before starting this task:

- [ ] Phase <N> prerequisites met (see phase master).
- [ ] Task <prior task ID> merged (or N/A if this is task 001 of the phase).
- [ ] <Specific prerequisite>.
- [ ] <Specific prerequisite>.

If any prerequisite is missing, surface it and pause - do not proceed with partial state.

## 5. Task Details

### 5.1 Goal

<Restate the objective in operational terms: "modify X so that Y is true.">

### 5.2 Current State

```<lang>
<paste the current state of the relevant code, config, or doc - make it concrete>
```

### 5.3 Target State

```<lang>
<paste the target state - what we want after this task>
```

### 5.4 Step-by-step

1. <Step 1: a single, reviewable action>
2. <Step 2>
3. <Step 3>
4. <Step 4>

### 5.5 Files to Modify

| File | Change |
|---|---|
| `<path>` | <what changes> |
| `<path>` | <what changes> |

### 5.6 Files to Create

| File | Purpose |
|---|---|
| `<path>` | <purpose> |

### 5.7 Files to Delete

| File | Reason |
|---|---|
| `<path>` | <why removed> |

## 6. Acceptance Criteria

Task <NNN> is complete when **all** of the following are true:

- [ ] <Concrete, testable criterion 1>.
- [ ] <Concrete, testable criterion 2>.
- [ ] <Concrete, testable criterion 3>.
- [ ] All requirements back-referenced (R<N.M>, R<N.M>) have at least one passing test.
- [ ] Performance budgets (NFR-<N.M>) met for changed code paths.
- [ ] Documentation updated where this task is referenced.
- [ ] PR opened with description linking back to this task.
- [ ] `/audit` returns clean.

## 7. Out of Scope

To prevent scope creep, explicitly out of scope:

- <Item 1>
- <Item 2>
- <Item 3>

These belong to other tasks (named) or are deliberate non-goals.

## 8. Validation

How we know this task worked:

- <Test 1>
- <Test 2>
- <Manual procedure if applicable>

## 9. Rollback

If this task ships and we need to revert:

1. <Step 1>
2. <Step 2>

(Most tasks have a trivial rollback - `git revert`. Tasks with data migrations or external system changes need an explicit rollback procedure.)

---

## How to fill this template

1. **Task number.** Three-digit, sortable. Filename `<NNN>_<task-slug>.md`. Number is sticky - don't renumber.
2. **Objective is one paragraph.** If it takes multiple paragraphs, the task is too big - split.
3. **Context cross-references are mandatory.** PRD, spec, architecture, phase master, related tasks. Without these, the agent works blind.
4. **Agent assignment is mandatory.** Primary + supporting. Without it, the runtime can't auto-select.
5. **Prerequisites checklist is non-negotiable.** Skipping prerequisites is the most common cause of failed task execution.
6. **Current → Target diff blocks** are the highest-leverage section. Showing both states side-by-side prevents misreads.
7. **Acceptance criteria are testable.** Vague criteria don't gate. Each criterion should map to a check, test, or attestation.
8. **Out of scope is first-class.** Without it, agents drift into adjacent work.
9. **Validation is concrete.** Every task has at least one way to confirm it worked.
10. **Body length** typically 80–150 lines. Longer prompts often hide unclear thinking; shorter prompts under-specify.
