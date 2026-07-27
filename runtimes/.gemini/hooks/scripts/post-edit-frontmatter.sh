#!/usr/bin/env bash
# Gemini CLI AfterTool hook: validates SpecRoute frontmatter contracts after a
# file write. Warns and never blocks.
#
# AfterTool is advisory here. The warning is returned as systemMessage, which
# Gemini surfaces to the user, and repeated on stderr for the hook log.

set -u

INPUT="$(cat)"

# As with the sanitization gate, the written path is located by searching the
# whole payload rather than assuming one key name.
FILE_PATH="$(printf '%s' "$INPUT" | python3 -c '
import json, os, sys

KEYS = ("file_path", "filePath", "path", "absolute_path", "abs_path",
        "filename", "file", "target_file", "notebook_path")

def walk(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in KEYS and isinstance(value, str) and value.strip():
                yield value
            yield from walk(value)
        return
    if isinstance(node, list):
        for item in node:
            yield from walk(item)

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

for found in walk(payload):
    if found.endswith(".md") and os.path.isfile(found):
        print(found)
        break
' 2>/dev/null)"

[ -z "$FILE_PATH" ] && { python3 -c 'import json; print(json.dumps({"continue": True}))'; exit 0; }
[ ! -f "$FILE_PATH" ] && { python3 -c 'import json; print(json.dumps({"continue": True}))'; exit 0; }

case "$FILE_PATH" in
  */README.md) python3 -c 'import json; print(json.dumps({"continue": True}))'; exit 0 ;;
esac

case "$FILE_PATH" in
  */.claude/agents/*.md|*/.codex/agents/*.md|*/.cursor/agents/*.md|*/.gemini/agents/*.md|*/.kiro/agents/*.md|*/agents/examples/*.md|*/agents/agent-template.md)
    ARTIFACT="agent" ;;
  */.devin/agents/*/AGENT.md|*/.agents/agents/*/AGENT.md)
    ARTIFACT="agent" ;;
  */SKILL.md)
    ARTIFACT="skill" ;;
  */.claude/commands/*.md|*/.cursor/commands/*.md|*/commands/examples/*.claude.md|*/commands/command-template.claude.md)
    ARTIFACT="command" ;;
  *)
    python3 -c 'import json; print(json.dumps({"continue": True}))'; exit 0 ;;
esac

WARNINGS="$(python3 - "$FILE_PATH" "$ARTIFACT" <<'PY' 2>/dev/null
import os
import re
import sys

path, artifact = sys.argv[1], sys.argv[2]
is_claude = "/.claude/" in path

try:
    text = open(path, encoding="utf-8").read()
except Exception as exc:
    print(f"frontmatter-lint [{artifact}] {path}: cannot read file: {exc}")
    sys.exit(0)

match = re.match(r"^---\n(.*?)\n---\s*\n", text, re.DOTALL)
if not match:
    print(f"frontmatter-lint [{artifact}] {path}: missing YAML frontmatter")
    sys.exit(0)

fields = {}
for line in match.group(1).splitlines():
    field = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
    if field:
        fields[field.group(1)] = field.group(2).strip()

# Only `name` and `description` are genuinely required by any runtime: Claude
# Code requires that pair for agents, and the open Agent Skills standard
# (agentskills.io) requires the same pair for skills. A linter that flags valid
# artifacts trains people to ignore it.
required = {
    "agent":   [] if "/.kiro/agents/" in path or "/.cursor/agents/" in path else ["name", "description"],
    "skill":   ["name", "description"],
    "command": ["description"],
}[artifact]

# Conventional in SpecRoute but not required by any runtime - reported
# separately so a missing one reads as a nudge rather than a defect.
recommended = {
    "agent":   [],
    "skill":   [],
    "command": [],
}[artifact]

warnings = []

missing = [key for key in required if not fields.get(key)]
if missing:
    warnings.append("missing required field(s): " + ", ".join(missing))

absent = [key for key in recommended if not fields.get(key)]
if absent:
    warnings.append(
        "missing recommended field(s): " + ", ".join(absent)
        + " (optional for the runtime; conventional in SpecRoute)"
    )

if "name" in fields:
    name = fields["name"].strip("\"'")
    basename = os.path.basename(path)
    if basename in ("SKILL.md", "AGENT.md"):
        # Folder-per-artifact shapes take their identity from the directory.
        expected = os.path.basename(os.path.dirname(path))
    else:
        expected = basename[:-3] if basename.endswith(".md") else basename
        if expected.endswith(".claude"):
            expected = expected[:-len(".claude")]
    if name != expected:
        warnings.append(f"name '{name}' does not match filename/dirname '{expected}'")

# `flagship` / `balanced` / `fast` are SpecRoute tier abstractions for roster
# tables. No runtime accepts them, so an agent file carrying one is broken.
TIER_ALIASES = {"flagship": "opus", "balanced": "sonnet", "fast": "haiku"}
VALID_MODELS = {"opus", "sonnet", "haiku", "fable", "inherit"}

if artifact == "agent" and is_claude and "model" in fields:
    model = fields["model"].strip('"').strip("'").split("#")[0].strip()
    if model in TIER_ALIASES:
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
    print(f"frontmatter-lint [{artifact}] {path}:")
    for warning in warnings:
        print(f"  - {warning}")
PY
)"

if [ -z "$WARNINGS" ]; then
  python3 -c 'import json; print(json.dumps({"continue": True}))'; exit 0
fi

printf '%s\n' "$WARNINGS" >&2
printf '%s' "$WARNINGS" | python3 -c 'import json, sys
print(json.dumps({"systemMessage": sys.stdin.read(), "continue": True}))'
exit 0
