---
description: Comprehensive pre-commit audit - sanitization, frontmatter validity, vendor matrix consistency, broken links, TODO health.
---

Run a comprehensive audit. This is the gate before any push or PR.

## 1. Sanitization

Run `/sanitize` first. If it fails, stop and report the failures - do not continue with later checks until sanitization is clean.

## 2. Frontmatter validation

Walk every agent / skill / command file and validate frontmatter:

Contracts are vendor-scoped since the mid-2026 convergence - see [`wiki/Frontmatter-Contracts.md`](../../wiki/Frontmatter-Contracts.md) and the `frontmatter-lint` skill. Do not hold non-Claude vendors to Claude's contract.

```bash
echo "── frontmatter check (agents: Claude contract) ──"
# Claude requires name + description; model and color are optional.
for f in .claude/agents/*.md agents/agent-template.md agents/examples/*.md runtimes/.claude/agents/*.md; do
  [ -f "$f" ] || continue
  case "$f" in *README.md) continue ;; esac
  for k in name description; do
    grep -q "^$k:" "$f" || echo "  ERROR $f: missing $k"
  done
done

echo
echo "── frontmatter check (agents: Codex contract) ──"
# Codex agents are TOML, not Markdown - keys are `name = "..."`, not `name:`.
for f in runtimes/.codex/agents/*.toml; do
  [ -f "$f" ] || continue
  for k in name description developer_instructions; do
    grep -qE "^$k *=" "$f" || echo "  ERROR $f: missing $k"
  done
done

echo
echo "── frontmatter check (agents: other vendors) ──"
# SpecRoute's portable publication baseline is name + description. Some vendor
# parsers accept less; the audit intentionally holds shipped templates to the
# stronger portable baseline. model/color remain Claude-specific.
# Devin Local subagent profiles use per-profile `AGENT.md` directories under
# `runtimes/.devin/agents/`. Cascade compatibility paths are not a second runtime.
for f in runtimes/.gemini/agents/*.md runtimes/.kiro/agents/*.md runtimes/.cursor/agents/*.md runtimes/.devin/agents/*/AGENT.md; do
  [ -f "$f" ] || continue
  case "$f" in *README.md) continue ;; esac
  for k in name description; do
    grep -q "^$k:" "$f" || echo "  ERROR $f: missing $k"
  done
done

echo
echo "── frontmatter check (skills) ──"
# Contract lives in wiki/Frontmatter-Contracts.md. The Agent Skills open standard
# uses name + description as the portable baseline. argument-hint /
# user-invocable / allowed-tools are optional Claude Code extensions, so they
# are warnings only in Claude-shaped templates.
for f in .claude/skills/*/SKILL.md .agents/skills/*/SKILL.md \
         skills/skill-template/SKILL.md skills/examples/*/SKILL.md \
         runtimes/.claude/skills/*/SKILL.md runtimes/.codex/skills/*/SKILL.md \
         runtimes/.gemini/skills/*/SKILL.md runtimes/.kiro/skills/*/SKILL.md \
         runtimes/.cursor/skills/*/SKILL.md runtimes/.devin/skills/*/SKILL.md; do
  [ -f "$f" ] || continue
  for k in name description; do
    grep -q "^$k:" "$f" || echo "  ERROR $f: missing $k"
  done
  case "$f" in
    .claude/*|skills/*|runtimes/.claude/*)
      for k in argument-hint user-invocable allowed-tools; do
        grep -q "^$k:" "$f" || echo "  WARN  $f: missing $k (optional Claude extension)"
      done ;;
  esac
done

echo
echo "── frontmatter check (Claude commands) ──"
for f in commands/command-template.claude.md commands/examples/*.claude.md runtimes/.claude/commands/*.md .claude/commands/*.md; do
  [ -f "$f" ] || continue
  case "$f" in *README.md) continue ;; esac
  grep -q "^description:" "$f" || echo "  ERROR $f: missing description"
done
```

## 3. Vendor matrix consistency

The vendor matrix table is mirrored in four files. All four tables are maintained byte-identically, so the check is a digest comparison, not a shape comparison. Supporting notes are centralized in the integration reference and dedicated wiki page.

Why a digest and not just counts: row count and the set of runtime-dir tokens only detect a vendor being **added or dropped**. They cannot see a hook event count edited in one mirror or a config path renamed in a single cell - which is the drift this repo actually produces. Both signals are kept, but they play different roles: the digest decides pass/fail, and the row-count / vendor-set lines are the cheap human-readable summary printed for every mirror plus the first thing reported when a block does differ (a dropped row makes every subsequent row "differ", so the count line is what tells you it was one deletion rather than five edits).

Counting every `| ...` line would be useless here - all four files carry unrelated tables - so vendor rows are matched by a second cell holding a backticked runtime directory (`` `.claude/` ``, `` `.codex/` ``, ...). The trailing backtick in that regex is load-bearing: without it, cells that merely mention a path like `` `.claude/agents/README.md` `` match too.

```bash
echo "── vendor matrix consistency ──"

mirrors="README.md AGENTS.md wiki/Vendor-Matrix.md agentic-docs/agent-cli-integrations.md"
row_re='^\|[^|]+\|[^|]*`\.[a-z]+/`'

# Digest helper - macOS ships `shasum`, most Linux images ship `sha256sum`.
# `cksum` is the POSIX-guaranteed last resort: weaker, but still detects edits.
if command -v shasum >/dev/null 2>&1;      then blockhash() { shasum -a 256 | cut -d' ' -f1; }
elif command -v sha256sum >/dev/null 2>&1; then blockhash() { sha256sum    | cut -d' ' -f1; }
else                                            blockhash() { cksum        | cut -d' ' -f1; }
fi

# The comparable block = the contiguous pipe-table containing at least one vendor
# row (so: header + separator + every row). Supporting vendor notes are centralized
# in the integration reference and wiki rather than duplicated into every mirror.
# Surrounding prose is excluded on purpose - each mirror frames the table
# differently, and that framing is not drift.
extract_matrix() {
  awk '
    /^\|/ { buf = buf $0 "\n"; if ($0 ~ /^\|[^|]+\|[^|]*`\.[a-z]+\/`/) hit = 1; next }
          { if (hit) printf "%s", buf; hit = 0; buf = "" }
    END   { if (hit) printf "%s", buf }
  ' "$1"
}

work=$(mktemp -d) && drift=0 && : > "$work/index"

# Pass 1 - extract every mirror's block and record its digest.
for f in $mirrors; do
  if [ ! -f "$f" ]; then echo "  $f: MISSING MIRROR"; drift=1; continue; fi
  out="$work/$(printf '%s' "$f" | tr '/' '_')"
  extract_matrix "$f" > "$out"
  if [ ! -s "$out" ]; then echo "  $f: NO MATRIX BLOCK FOUND"; drift=1; continue; fi
  # Mirror paths are fixed and space-free, so space-separated fields are safe.
  printf '%s %s %s\n' "$(blockhash < "$out")" "$f" "$out" >> "$work/index"
done

# Pass 2 - the majority digest is the reference, so a single bad mirror gets
# named instead of the whole set being blamed on whichever file was listed first.
ref_h=$(cut -d' ' -f1 "$work/index" | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')
ref_f=$(awk -v h="$ref_h" '$1==h {print $2; exit}' "$work/index")
ref_o=$(awk -v h="$ref_h" '$1==h {print $3; exit}' "$work/index")

while read -r h f out; do
  n=$(grep -cE "$row_re" "$out" || true)
  t=$(grep -E "$row_re" "$out" | grep -oE '`\.[a-z]+/`' | sort -u | tr '\n' ' ')
  printf '  %-40s %s rows  sha %s  %s\n' "$f" "$n" "$(printf '%.8s' "$h")" "$t"
  [ "$h" = "$ref_h" ] && continue
  drift=1
  echo "    DRIFT in $f - matrix block differs from the majority ($ref_f)"
  n_ref=$(grep -cE "$row_re" "$ref_o" || true)
  t_ref=$(grep -E "$row_re" "$ref_o" | grep -oE '`\.[a-z]+/`' | sort -u | tr '\n' ' ')
  [ "$n" = "$n_ref" ] || echo "      row count:  $n vs $n_ref"
  [ "$t" = "$t_ref" ] || echo "      vendor set: $t vs $t_ref"
  # Cell-precise diff. A whole-line diff is useless here - the rows are ~400
  # characters wide, so a one-word change scrolls off the right edge. Split both
  # blocks on `|` and name the row and column that moved. `-` is $ref_f, `+` is $f.
  awk '
    NR==FNR { ref[FNR] = $0; nref = FNR; next }
    { if ($0 == ref[FNR]) next
      if (FNR > nref) { print "      line " FNR " only in +: " $0; next }
      if ($0 !~ /^\|/) { print "      line " FNR " differs:";
                         print "        - " ref[FNR]; print "        + " $0; next }
      na = split(ref[FNR], A, "|"); nb = split($0, B, "|")
      if (na != nb) { print "      line " FNR ": column count " nb-2 " vs " na-2; next }
      for (i = 2; i < na; i++) if (A[i] != B[i])
        printf "      line %d, column %d:\n        -%s\n        +%s\n", FNR, i-1, A[i], B[i]
    }
    END { for (i = FNR + 1; i <= nref; i++) print "      line " i " only in -: " ref[i] }
  ' "$ref_o" "$out" | head -20
done < "$work/index"

rm -rf "$work"
[ "$drift" -eq 0 ] && echo "  OK: all four mirrors byte-identical (sha256 $ref_h)"
```

Any `DRIFT`, `MISSING MIRROR`, or `NO MATRIX BLOCK FOUND` line fails this check. A clean run prints one line per mirror plus a single `OK:` line carrying the shared digest.

Fixing drift means making the blocks byte-identical again - copy the correct block over the wrong one rather than hand-patching the reported cell, since a hand-patch that differs by whitespace will still fail. The majority is a heuristic, not an authority: when the count splits two-two, or when the majority is what's actually stale, decide from the source of truth and not from the vote.

Note `agentic-docs/multi-vendor-context-files.md` is **not** a matrix mirror - it documents the context-file convention only, and `wiki/Agent-CLI-Integrations.md` is a wiki stub that points at `wiki/Vendor-Matrix.md` rather than restating the table.

## 4. Broken markdown links

```bash
echo "── broken local links ──"
python3 - <<'PY'
import re, os, subprocess
broken = 0
raw = subprocess.check_output(
    ["git", "ls-files", "-co", "--exclude-standard", "-z"]
)
for item in raw.split(b"\0"):
    if not item:
        continue
    fp = item.decode("utf-8", errors="surrogateescape")
    if not fp.endswith(".md") or not os.path.isfile(fp):
        continue
    text = open(fp, encoding="utf-8", errors="ignore").read()
    text = re.sub(r"(?ms)^```.*?^```", "", text)
    text = re.sub(r"`[^`\n]*`", "", text)
    for m in re.finditer(r"\]\(([^)]+)\)", text):
        target = m.group(1).split("#", 1)[0].strip().strip("<>")
        if (not target or target.startswith(("http://", "https://", "mailto:"))
                or "<" in target or target in {"path", "TODO"}):
            continue
        candidate = os.path.normpath(os.path.join(os.path.dirname(fp), target))
        if not os.path.exists(candidate):
            print(f"  {fp}: {target}")
            broken += 1
print(f"Total broken links: {broken}")
PY
```

## 5. TODO health

```bash
echo "── TODO health ──"
python3 - <<'PY'
import os, subprocess
raw = subprocess.check_output(["git", "ls-files", "-co", "--exclude-standard", "-z"])
findings = []
for item in raw.split(b"\0"):
    if not item:
        continue
    path = item.decode("utf-8", errors="surrogateescape")
    if not os.path.isfile(path):
        continue
    text = open(path, encoding="utf-8", errors="ignore").read()
    count = text.count("TODO")
    if count:
        findings.append((path, count))
print(f"Total TODOs: {sum(count for _, count in findings)}")
print("Files with TODOs:")
for path, count in findings[:20]:
    print(f"  {path}: {count}")
PY
```

TODOs are intentional placeholders. The audit doesn't fail on TODO count - it just reports.

## Final report

Summarize:

- Sanitization: PASS / FAIL
- Frontmatter: N `ERROR` / M `WARN` across K files
- Vendor matrix: in sync / drift detected
- Links: N broken / clean
- TODOs: N total

Ready-to-publish iff: Sanitization and local provenance PASS, Frontmatter
0 `ERROR`, Vendor matrix in sync, Links 0 broken, and Wiki parity has no
unexplained warning. `WARN` lines are advisory and must name the vendor whose
optional convention they describe.
