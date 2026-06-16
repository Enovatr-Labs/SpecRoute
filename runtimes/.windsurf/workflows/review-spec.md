---
description: Review a spec, PRD, or implementation plan for implementation-readiness. Invoke with /review-spec
---

# Review Spec

Run a readiness review of the planning artifact the user names before any code work starts. This is the deterministic, user-invokable wrapper around the spec-reviewer checklist.

## Steps

1. Ask for the artifact path if it was not supplied with the invocation.
2. Read the artifact and its nearest template or README for the applicable contract.
3. Apply the checklist below.
4. Report blocking gaps first, then non-blocking cleanups, then a one-line verdict.

## Checklist

- Goal, audience, and scope are stated in plain language; non-goals prevent scope creep.
- Success metrics and acceptance criteria are present, measurable, and testable.
- Requirements use stable IDs; every task back-references a requirement or states its rationale.
- Design covers interfaces, data flow, and failure modes.
- No unresolved placeholders or unowned decisions remain (placeholders are acceptable only in templates).
- Validation covers functional, security, performance, and rollout concerns where relevant.

## Output

```markdown
## Findings
- High: <blocking issue with path:line>
- Medium: <important non-blocking issue>
- Low: <cleanup>

## Ready?
<yes/no> for implementation, with one sentence explaining why.
```
