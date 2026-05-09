#!/usr/bin/env bash
# PostToolUse hook (matcher: Write|Edit): validates common SpecForge
# frontmatter contracts. Warns on stderr and never blocks.

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

case "$FILE_PATH" in
  */.claude/agents/*.md|*/.codex/agents/*.md|*/agents/examples/*.md|*/agents/agent-template.md) ARTIFACT="agent" ;;
  */.claude/skills/*/SKILL.md|*/.codex/skills/*/SKILL.md|*/skills/examples/*/SKILL.md|*/skills/skill-template/SKILL.md) ARTIFACT="skill" ;;
  */.claude/commands/*.md|*/commands/examples/*.claude.md|*/commands/command-template.claude.md) ARTIFACT="command" ;;
  *) exit 0 ;;
esac

case "$FILE_PATH" in *README.md) exit 0 ;; esac

python3 - "$FILE_PATH" "$ARTIFACT" <<'PY'
import re
import sys

path, artifact = sys.argv[1], sys.argv[2]

try:
    text = open(path, encoding="utf-8").read()
except Exception as exc:
    print(f"frontmatter-lint: cannot read {path}: {exc}", file=sys.stderr)
    sys.exit(0)

match = re.match(r"^---\n(.*?)\n---\s*\n", text, re.DOTALL)
if not match:
    print(f"frontmatter-lint [{artifact}] {path}: missing YAML frontmatter", file=sys.stderr)
    sys.exit(0)

fields = {}
for line in match.group(1).splitlines():
    field = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
    if field:
        fields[field.group(1)] = field.group(2).strip()

required = {
    "agent": ["name", "description", "model", "color"],
    "skill": ["name", "description", "argument-hint", "user-invocable", "allowed-tools"],
    "command": ["description"],
}[artifact]

warnings = []
missing = [key for key in required if not fields.get(key)]
if missing:
    warnings.append("missing required field(s): " + ", ".join(missing))

if "name" in fields:
    name = fields["name"].strip("\"'")
    expected = path.split("/")[-1].removesuffix(".md")
    if artifact == "skill":
        expected = path.split("/")[-2]
    if name != expected:
        warnings.append(f"name '{name}' does not match filename/dirname '{expected}'")

if artifact == "agent" and fields.get("model") not in ("opus", "sonnet", "haiku"):
    warnings.append(f"model '{fields.get('model')}' is not one of opus/sonnet/haiku")

if warnings:
    print(f"frontmatter-lint [{artifact}] {path}:", file=sys.stderr)
    for warning in warnings:
        print(f"  - {warning}", file=sys.stderr)
PY

exit 0
