---
name: <skill-slug>
description: <one-paragraph description with use cases. Pattern - "Interactive workflow for <task>. Use when <situation>. Asks the user <key decision points>. Triggers - 'literal user utterance 1', 'literal user utterance 2'." The description drives auto-selection - include trigger phrases.>
argument-hint: "[arg1] [arg2?]"
user-invocable: true
allowed-tools: Read Write Edit Glob Grep Bash
---

# <Skill Title>

<2–4 sentence overview: what this skill does, what it produces, who uses it.>

## When to use

- <Situation 1>
- <Situation 2>
- <Situation 3>

## Step 1: <First step title>

<What this step does. If the skill takes an argument, parse it here. If a key decision is needed, ask the user.>

If the argument is missing or unclear, ask:

1. <Question 1>?
2. <Question 2>?

## Step 2: <Second step title>

<Concrete actions. Reference files to read. Use tables for mappings.>

| Input | Action | Output |
|---|---|---|
| <example> | <action> | <result> |

## Step 3: <Third step title>

<Continue the guided walkthrough. Validation checkpoints belong here — confirm before destructive actions.>

## Step 4: Report

<What the skill outputs at the end. Be specific:>

- Files created or modified (paths).
- Frontmatter fields the user must fill in.
- Suggested next agents or commands to invoke.
- Whether matching examples or runtime mirrors need updating.

## Don't use for

- <Adjacent operation 1> — use <other skill or agent>.
- <Adjacent operation 2> — use <other skill or agent>.

---

## How to fill this template

1. **Pick a slug.** Lowercase, hyphen-separated. The enclosing directory name is the slug; this file is always `SKILL.md`.

2. **Write the description with triggers.** Most important field. Concrete user utterances that should invoke the skill. Pattern: `"Triggers - 'do X', 'help me with Y', 'set up Z'."`

3. **`argument-hint`** — show the expected argument shape. Use `""` if no arguments. Use `[arg]` for required, `[arg?]` for optional.

4. **`user-invocable: true`** — almost always. Set to `false` only for skills meant to be invoked programmatically by other skills or agents.

5. **`allowed-tools`** — specify the **minimum** set the skill needs. Skills should not be granted Bash by default unless they shell out. Common sets:
   - Read-only audit: `Read Glob Grep`
   - File-creating wizard: `Read Write Edit Glob`
   - Shell-driven workflow: `Read Write Edit Glob Grep Bash`

6. **Number the steps.** "Step 1", "Step 2", … This is the format that makes skills feel guided. The user can interrupt and resume between steps.

7. **Validation checkpoints.** Before destructive actions (overwriting files, running git operations, deleting), pause and confirm.

8. **Final "Report" step.** Skills that produce artifacts must report what they created and what comes next. Skills that diagnose must produce a punch list.

9. **"Don't use for" section.** Hand off the adjacent concerns. This is how skill catalogs stay healthy.

## Optional sibling directories

Inside `<slug>/` alongside `SKILL.md`:

- `scripts/` — supporting shell or Python scripts the skill invokes.
- `agents/` — sub-agents scoped specifically to this skill (advanced use).

These are optional. Most skills are a single `SKILL.md`.
