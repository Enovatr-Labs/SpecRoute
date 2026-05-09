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
  */skills/skill-template/SKILL.md|*/skills/examples/*/SKILL.md|*/runtimes/*/skills/*/SKILL.md) ARTIFACT="skill" ;;
  */commands/examples/*.claude.md|*/commands/command-template.claude.md|*/runtimes/.claude/commands/*.md) ARTIFACT="command" ;;
  *) exit 0 ;;
esac

# Skip the README files in those dirs.
case "$FILE_PATH" in *README.md) exit 0 ;; esac

python3 - "$FILE_PATH" "$ARTIFACT" <<'PY'
import sys, re
path, artifact = sys.argv[1], sys.argv[2]
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
    "agent":   ["name", "description", "model", "color"],
    "skill":   ["name", "description", "argument-hint", "user-invocable", "allowed-tools"],
    "command": ["description"],
}[artifact]

missing = [k for k in required if k not in fields or fields[k] == ""]
warnings = []

if missing:
    warnings.append(f"missing required field(s): {', '.join(missing)}")

if "name" in fields:
    name = fields["name"].strip('"').strip("'")
    expected = path.split("/")[-1].removesuffix(".md")
    if artifact == "skill":
        expected = path.split("/")[-2]
    if name != expected:
        warnings.append(f"name '{name}' does not match filename/dirname '{expected}'")

if artifact == "agent" and fields.get("model") not in ("opus", "sonnet", "haiku"):
    warnings.append(f"model '{fields.get('model')}' is not one of opus/sonnet/haiku")

if warnings:
    print(f"frontmatter-lint [{artifact}] {path}:", file=sys.stderr)
    for w in warnings:
        print(f"  - {w}", file=sys.stderr)
PY

exit 0
