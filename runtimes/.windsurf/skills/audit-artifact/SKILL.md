---
name: audit-artifact
description: Interactive workflow for auditing a SpecRoute artifact before it is treated as implementation-ready. Use when checking a PRD, spec triplet, prompt set, agent file, skill, command, hook, rule, or runtime layout. Asks which artifact path to inspect and which contract to apply. Triggers - "audit this artifact", "check this template", "is this spec ready", "review this prompt set".
argument-hint: "[path] [artifact-type?]"
allowed-tools:
  - read
  - grep
  - glob
  - exec
---

# Audit Artifact

Use this skill when a user wants a guided readiness review of one SpecRoute artifact or a small related set of artifacts.

## Inputs

Ask for any missing input before reviewing:

1. **Path** - file or directory to audit.
2. **Artifact type** - one of `prd`, `spec`, `agent`, `skill`, `command`, `hook`, `prompt`, `rule`, `runtime`, or `unknown`.
3. **Readiness target** - `draft`, `review-ready`, or `implementation-ready`.

If the artifact type is omitted, infer it from the path and confirm the inference in the audit summary.

## Workflow

1. Read the artifact and its nearest README or template reference.
2. Identify the applicable contract:
   - PRDs need goals, non-goals, metrics, rollout, risks, dependencies, and acceptance criteria.
   - Specs need stable requirement IDs, design coverage, task back-references, and validation steps.
   - Agents and skills need valid frontmatter and clear boundaries.
   - Commands, hooks, rules, and runtime layouts need vendor-native shape.
3. Check for unresolved placeholders that are inappropriate for the readiness target.
4. Check sanitization risk: private names, credentials, internal endpoints, customer data, or proprietary domain logic.
5. Report findings in severity order with file references and concrete recommended fixes.

## Output Shape

```markdown
## Findings

- High: <blocking issue with path>
- Medium: <important non-blocking issue>
- Low: <cleanup>

## Ready?

<yes/no> for <readiness target>, with one sentence explaining why.

## Recommended Changes

- <smallest concrete edit>
```

## Guardrails

- Do not rewrite the artifact unless the user explicitly asks for implementation.
- Do not invent missing business facts. Mark missing facts as required decisions.
- Treat placeholders as acceptable in templates and suspicious in approved examples.
