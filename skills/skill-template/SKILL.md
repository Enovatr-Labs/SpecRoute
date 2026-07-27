---
name: <skill-slug>
description: <one-paragraph description with use cases. Pattern - "Interactive workflow for <task>. Use when <situation>. Asks the user <key decision points>. Triggers - 'literal user utterance 1', 'literal user utterance 2'." The description drives auto-selection - include trigger phrases.>
license: MIT                                    # optional agentskills.io standard field
compatibility: "Requires bash, git, python3"    # optional agentskills.io standard environment constraints
metadata:                                       # optional agentskills.io standard metadata map
  author: "<author-name-or-team>"
  version: "1.0.0"
# Claude Code extensions - not part of the standard:
allowed-tools: Read Write Edit Glob Grep Bash   # optional; PRE-APPROVES these tools, does not restrict
disallowed-tools: Bash                          # optional; the field that actually removes tools
argument-hint: "[arg1] [arg2?]"                 # optional argument hint
user-invocable: true                            # optional; menu visibility only
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

<Continue the guided walkthrough. Validation checkpoints belong here - confirm before destructive actions.>

## Step 4: Report

<What the skill outputs at the end. Be specific:>

- Files created or modified (paths).
- Frontmatter fields the user must fill in.
- Suggested next agents or commands to invoke.
- Whether matching examples or runtime mirrors need updating.

## Don't use for

- <Adjacent operation 1> - use <other skill or agent>.
- <Adjacent operation 2> - use <other skill or agent>.

---

## How to fill this template

1. **Pick a slug.** Lowercase, hyphen-separated. The enclosing directory name is the slug; this file is always `SKILL.md`.

2. **Write the description with triggers.** Most important field. Concrete user utterances that should invoke the skill. Pattern: `"Triggers - 'do X', 'help me with Y', 'set up Z'."` Cap it at 1024 characters per the standard and front-load the triggers.

3. **For a Claude Code target, `argument-hint`** shows the expected argument shape. Use `""` if no arguments. Use `[arg]` for required, `[arg?]` for optional.

4. **For a Claude Code target, `user-invocable: true`** is usually appropriate. Setting it to `false` hides the skill from the invocation menu; it does **not** block access via the Skill tool, so it is a discoverability control, not an access control. Use `disable-model-invocation: true` for the opposite case (user-only, never auto-selected).

5. **In Claude Code, `allowed-tools` pre-approves; it does not restrict.** The listed tools run without prompting for the invoking turn, and the grant clears on the next message - the skill can still reach for tools you omitted, it just prompts first. Keep the list to what the skill routinely needs so that unattended approval stays narrow, but never treat it as a sandbox. The field that removes tools from the pool is `disallowed-tools`. Common pre-approval sets:
   - Read-only audit: `Read Glob Grep`
   - File-creating wizard: `Read Write Edit Glob`
   - Shell-driven workflow: `Read Write Edit Glob Grep Bash`

6. **Number the steps.** "Step 1", "Step 2", … This is the format that makes skills feel guided. The user can interrupt and resume between steps.

7. **Validation checkpoints.** Before destructive actions (overwriting files, running git operations, deleting), pause and confirm.

8. **Final "Report" step.** Skills that produce artifacts must report what they created and what comes next. Skills that diagnose must produce a punch list.

9. **"Don't use for" section.** Hand off the adjacent concerns. This is how skill catalogs stay healthy.

10. **Keep the body portable.** SpecRoute uses `name` and `description` as its portable publication contract. Everything else above is Claude Code-oriented convention; other runtime templates keep only fields verified for that vendor. Put nothing load-bearing in the frontmatter that the body does not also state. `tools/sync-skills.py` syncs bodies and preserves each target's own frontmatter.

## Optional sibling directories

Inside `<slug>/` alongside `SKILL.md`:

- `scripts/` - supporting shell or Python scripts the skill invokes.
- `agents/` - sub-agents scoped specifically to this skill (advanced use).

These are optional. Most skills are a single `SKILL.md`.
