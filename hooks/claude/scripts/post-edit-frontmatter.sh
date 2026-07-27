#!/usr/bin/env bash
# PostToolUse hook (matcher: Write|Edit): validates YAML frontmatter when an
# agent / skill / command file is written or edited. Warns (does not block).
#
# Hook protocol:
#   - Reads JSON from stdin: { "tool_input": { "file_path": "..." }, ... }
#   - Exit 0 = silent pass; messages on stderr are shown to the user

set -u

INPUT="$(cat)"
FILE_PATH="$(printf '%s' "$INPUT" | python3 -c 'import json,sys
try:
    d = json.load(sys.stdin)
    print(d.get("tool_input", {}).get("file_path", ""))
except Exception:
    print("")
' 2>/dev/null)"

[ -z "$FILE_PATH" ] && exit 0
[ ! -f "$FILE_PATH" ] && exit 0

# Only validate paths under the artifact directories that have a frontmatter contract.
case "$FILE_PATH" in
  */.claude/agents/*.md|*/agents/examples/*.md|*/agents/agent-template.md) ARTIFACT="agent" ;;
  */.claude/skills/*/SKILL.md|*/.agents/skills/*/SKILL.md|*/skills/skill-template/SKILL.md|*/skills/examples/*/SKILL.md|*/runtimes/*/skills/*/SKILL.md) ARTIFACT="skill" ;;
  */commands/examples/*.claude.md|*/commands/command-template.claude.md|*/runtimes/.claude/commands/*.md) ARTIFACT="command" ;;
  *) exit 0 ;;
esac

# Skip the README files in those dirs.
case "$FILE_PATH" in *README.md) exit 0 ;; esac

python3 - "$FILE_PATH" "$ARTIFACT" <<'PY'
import sys, re, json
path, artifact = sys.argv[1], sys.argv[2]
is_claude = "/.claude/" in path or "/agents/examples/" in path or path.endswith("/agents/agent-template.md")
is_agent_template = path.endswith("/agents/agent-template.md")
try:
    text = open(path, encoding="utf-8").read()
except Exception as e:
    print(f"frontmatter-lint: cannot read {path}: {e}", file=sys.stderr); sys.exit(0)

m = re.match(r'^---\n(.*?)\n---\s*\n', text, re.DOTALL)
if not m:
    print(f"frontmatter-lint [{artifact}] {path}: missing YAML frontmatter (--- ... ---)", file=sys.stderr)
    sys.exit(0)

body = m.group(1)
fields = {}
for line in body.splitlines():
    mm = re.match(r'^([A-Za-z_-]+):\s*(.*)$', line)
    if mm:
        fields[mm.group(1)] = mm.group(2).strip()

required = {
    # Only `name` and `description` are genuinely required by the runtime.
    # For agents, Claude Code requires just those two. For skills, the open
    # Agent Skills standard (agentskills.io) requires the same pair; everything
    # else is a vendor extension. Keeping `required` honest matters: a linter
    # that flags valid artifacts trains people to ignore it.
    "agent":   ["name", "description"],
    "skill":   ["name", "description"],
    "command": ["description"],
}[artifact]

# Fields that are conventional in SpecRoute but NOT required by any runtime.
# Reported separately so a missing one reads as a nudge, not a defect.
recommended = {
    "agent":   ["model", "color"] if is_claude else [],
    "skill":   ["argument-hint", "allowed-tools"] if is_claude else [],
    "command": [],
}[artifact]

missing = [k for k in required if k not in fields or fields[k] == ""]
absent_recommended = [k for k in recommended if k not in fields or fields[k] == ""]
warnings = []

if missing:
    warnings.append(f"missing required field(s): {', '.join(missing)}")

if absent_recommended:
    warnings.append(
        f"missing recommended field(s): {', '.join(absent_recommended)} "
        "(optional for the runtime; conventional in SpecRoute)"
    )

if "name" in fields:
    name = fields["name"].strip('"').strip("'")
    expected = path.split("/")[-1].removesuffix(".md")
    if artifact == "skill":
        expected = path.split("/")[-2]
    placeholder_ok = (
        path.endswith("/skills/skill-template/SKILL.md") and name == "<skill-slug>"
    ) or (
        is_agent_template and name == "<slug-lowercase-hyphenated>"
    )
    if name != expected and not placeholder_ok:
        warnings.append(f"name '{name}' does not match filename/dirname '{expected}'")

# Valid Claude Code `model` values. Note `flagship`/`balanced`/`fast` are SpecRoute's
# vendor-neutral tier ABSTRACTIONS for roster tables - they are NOT accepted by the
# runtime, so a real agent file carrying one is broken. Flag it explicitly rather
# than silently passing.
TIER_ALIASES = {"flagship": "opus", "balanced": "sonnet", "fast": "haiku"}
VALID_MODELS = {"opus", "sonnet", "haiku", "fable", "inherit"}

if artifact == "agent" and is_claude and "model" in fields:
    model = fields["model"].strip('"').strip("'").split("#")[0].strip()
    if is_agent_template and model == "<vendor model id>":
        pass
    elif model in TIER_ALIASES:
        warnings.append(
            f"model '{model}' is a SpecRoute tier abstraction, not a runtime value - "
            f"use '{TIER_ALIASES[model]}' here and keep tiers to roster tables"
        )
    elif model and model not in VALID_MODELS and not model.startswith("claude-"):
        warnings.append(
            f"model '{model}' is not one of {'/'.join(sorted(VALID_MODELS))} "
            "or a full model id (claude-*)"
        )

if warnings:
    # stderr is for the human running with --verbose. On exit 0 the model never
    # sees stderr, so also emit `systemMessage` on stdout - that is what actually
    # surfaces the warning in-session without blocking the write.
    print(f"frontmatter-lint [{artifact}] {path}:", file=sys.stderr)
    for w in warnings:
        print(f"  - {w}", file=sys.stderr)

    detail = "; ".join(warnings)
    print(json.dumps({
        "systemMessage": f"frontmatter-lint [{artifact}] {path}: {detail}"
    }))
PY

exit 0
