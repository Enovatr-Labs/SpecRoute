# Tasks: <Feature Name>

**Version**: 0.1
**Date**: <YYYY-MM-DD>
**Author**: <Name>
**Status**: Draft | Approved | In Implementation | Complete
**Source PRD**: <link>
**Source Requirements**: [`requirements.md`](requirements.md)
**Source Design**: [`design.md`](design.md)

---

> **Spec triplet — part 3 of 3.** This document is the implementation work plan. Tasks are numbered for execution order and back-reference requirement IDs from `requirements.md`. Each task is small enough to land in one PR.

---

## Phase 1: <Phase Name>

Goal: <one-line phase outcome>.

### 1. <Task title>

- <Concrete sub-step 1>
- <Concrete sub-step 2>
- <Concrete sub-step 3>
- _Requirements: R1.1, R1.2_

### 2. <Task title>

- <Sub-step 1>
- <Sub-step 2>
- _Requirements: R1.3_

### 2.1 <Sub-task title>

For tasks that need finer breakdown:

- <Sub-step 1>
- _Requirements: R1.3_

## Phase 2: <Phase Name>

Goal: <one-line phase outcome>.

### 3. <Task title>

- <Sub-step 1>
- _Requirements: R2.1, NFR-1.1_

### 4. <Task title>

- <Sub-step 1>
- _Requirements: R2.2_

## Phase 3: <Phase Name>

Goal: <one-line phase outcome>.

### 5. <Task title>

- <Sub-step 1>
- _Requirements: R3.1_

---

## Coverage check

This map confirms every requirement has at least one task and every NFR is addressed:

| Requirement / NFR | Tasks |
|---|---|
| R1.1 | 1 |
| R1.2 | 1 |
| R1.3 | 2, 2.1 |
| R2.1 | 3 |
| R2.2 | 4 |
| R3.1 | 5 |
| NFR-1.1 | 3 |
| NFR-2.1 | TODO |
| NFR-2.2 | TODO |
| NFR-3.1 | TODO |
| NFR-3.2 | TODO |

Any requirement without a task is unimplemented. Any task without a requirement back-reference is unscoped — clarify before starting.

## Done checklist

The feature is complete when **all** of the following are true:

- [ ] All tasks have their checkbox checked.
- [ ] Coverage table is fully populated (no `TODO` rows).
- [ ] All requirements (R*) have at least one passing test.
- [ ] All NFRs have a measurement or attestation.
- [ ] PRD acceptance criteria are met (Section 23 of the source PRD).
- [ ] Design open questions (`design.md` Section 13) are resolved.
- [ ] Documentation updated per PRD Section 12.

---

## How to use this file

1. **Working a task**: change `### N. Title` to `### [x] N. Title` and check the sub-step boxes as you go. Reference the task number in your commit messages and PR titles (e.g. `feat: implement task #3 - <…>`).
2. **Adding a task**: append to the end of the relevant phase. Numbering is sticky — don't renumber to insert.
3. **Splitting a task**: keep the parent number and use sub-numbers (e.g. `2.1`, `2.2`). Sub-tasks inherit requirement back-refs unless otherwise stated.
4. **Removing a task**: mark it `~~strikethrough~~` with a note explaining why; don't delete (numbering is referenced in commits and PR descriptions).
