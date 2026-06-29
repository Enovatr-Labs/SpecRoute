#!/usr/bin/env python3
"""Cross-runtime skill sync.

Sync the SKILL.md *body* of folder-per-skill artifacts across the runtime layouts
under `runtimes/.<vendor>/skills/`. As of mid-2026 all six supported vendors carry
Agent Skills (`SKILL.md`), so a skill's instructions can be shared across every
runtime - but each vendor's skill **frontmatter contract differs** (Claude/Codex use
`argument-hint`/`user-invocable`/`allowed-tools`; Kiro and Cursor use just
`name`/`description`; Gemini rewrites `allowed-tools` to its own tool ids; etc.).

So this tool is deliberately **body-aware**: it syncs the Markdown body below the
frontmatter and **preserves each target's own frontmatter**. Auxiliary files inside a
skill folder (scripts, templates) are synced verbatim.

Agents are NOT synced. Their formats diverge across vendors (Claude flat Markdown,
Codex standalone TOML, Devin per-profile `AGENT.md` dirs), so there is no safe
file-level copy. Maintain agents per vendor.

Usage:
    python3 tools/sync-skills.py [--apply] [--source <vendor>] [--target <vendor>]

  --apply              actually write changes (default is dry-run)
  --source <vendor>    source of truth runtime (default: claude)
  --target <vendor>    single target; if omitted, syncs to every other vendor

The default behavior is read-only: report what would change. Drift is never
auto-resolved without --apply (the source runtime's skill body wins on --apply).

This tool is a starting point - fork it for project-specific needs.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

# Every vendor whose runtime layout carries folder-per-skill SKILL.md artifacts.
SKILL_VENDORS = ["claude", "codex", "gemini", "kiro", "cursor", "windsurf", "devin"]


def runtime_dir(runtime: str) -> Path:
    return REPO_ROOT / "runtimes" / f".{runtime}"


def list_skills(runtime: str) -> set[str]:
    base = runtime_dir(runtime) / "skills"
    if not base.is_dir():
        return set()
    return {d.name for d in base.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()}


def split_frontmatter(text: str) -> tuple[str, str]:
    """Split a Markdown file into (frontmatter_block, body).

    The frontmatter block includes the enclosing `---` fences and trailing newline.
    Returns ("", text) when there is no leading frontmatter.
    """
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    fence_end = end + len("\n---\n")
    return text[:fence_end], text[fence_end:]


def body_of(path: Path) -> str:
    return split_frontmatter(path.read_text(encoding="utf-8"))[1]


def aux_files(base: Path) -> dict[Path, Path]:
    """Map of relative-path → absolute-path for every file under a skill folder
    EXCEPT the top-level SKILL.md (which is body-synced separately)."""
    if not base.is_dir():
        return {}
    return {
        p.relative_to(base): p
        for p in base.rglob("*")
        if p.is_file() and p.relative_to(base) != Path("SKILL.md")
    }


def diff_skill(source: str, target: str, slug: str) -> list[str]:
    """File-level differences for a shared skill: SKILL.md body drift + aux files."""
    src_base = runtime_dir(source) / "skills" / slug
    tgt_base = runtime_dir(target) / "skills" / slug
    diffs: list[str] = []

    if body_of(src_base / "SKILL.md") != body_of(tgt_base / "SKILL.md"):
        diffs.append("  ~ SKILL.md (body drift; frontmatter preserved on --apply)")

    src_aux = aux_files(src_base)
    tgt_aux = aux_files(tgt_base)
    for rel in sorted(src_aux.keys() - tgt_aux.keys()):
        diffs.append(f"  + {rel} (only in {source})")
    for rel in sorted(tgt_aux.keys() - src_aux.keys()):
        diffs.append(f"  - {rel} (only in {target})")
    for rel in sorted(src_aux.keys() & tgt_aux.keys()):
        if not filecmp.cmp(src_aux[rel], tgt_aux[rel], shallow=False):
            diffs.append(f"  ~ {rel} (drift)")
    return diffs


def sync_skill_body(source: str, target: str, slug: str) -> None:
    """Rewrite the target SKILL.md as target-frontmatter + source-body, and copy
    aux files verbatim. Preserves the target's vendor-specific frontmatter."""
    src_base = runtime_dir(source) / "skills" / slug
    tgt_base = runtime_dir(target) / "skills" / slug
    tgt_skill = tgt_base / "SKILL.md"

    tgt_frontmatter, _ = split_frontmatter(tgt_skill.read_text(encoding="utf-8"))
    _, src_body = split_frontmatter((src_base / "SKILL.md").read_text(encoding="utf-8"))
    tgt_skill.write_text(tgt_frontmatter + src_body, encoding="utf-8")

    src_aux = aux_files(src_base)
    for rel, src_path in src_aux.items():
        dest = tgt_base / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest)


def copy_new_skill(source: str, target: str, slug: str) -> None:
    """Copy a whole skill folder that does not yet exist in the target."""
    src_base = runtime_dir(source) / "skills" / slug
    tgt_base = runtime_dir(target) / "skills" / slug
    shutil.copytree(src_base, tgt_base)


def report(source: str, target: str, apply: bool) -> int:
    src_skills = list_skills(source)
    tgt_skills = list_skills(target)

    only_src = sorted(src_skills - tgt_skills)
    only_tgt = sorted(tgt_skills - src_skills)
    shared = sorted(src_skills & tgt_skills)

    drift_count = 0
    print(f"── skills: {source} (source) → {target} (target) ──")
    for slug in only_src:
        print(f"  MISSING in {target}: skills/{slug}/")
        if apply:
            copy_new_skill(source, target, slug)
            print(f"    copied (review {target}/skills/{slug}/SKILL.md frontmatter for {target}'s contract)")
        drift_count += 1
    for slug in only_tgt:
        print(f"  EXTRA in {target}: skills/{slug}/ (won't remove without explicit instruction)")
        drift_count += 1
    for slug in shared:
        diffs = diff_skill(source, target, slug)
        if diffs:
            print(f"  DRIFT skills/{slug}/")
            for d in diffs:
                print(d)
            if apply:
                sync_skill_body(source, target, slug)
                print(f"    synced body of {target}/skills/{slug}/ from {source} (frontmatter kept)")
            drift_count += 1

    if drift_count == 0:
        print("  ✓ in sync")
    return drift_count


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--apply", action="store_true", help="actually write changes (default: dry-run)")
    p.add_argument("--source", default="claude", choices=SKILL_VENDORS,
                   help="source of truth runtime (default: claude)")
    p.add_argument("--target", default=None, choices=SKILL_VENDORS,
                   help="single target runtime; if omitted, sync to every other vendor")
    args = p.parse_args()

    if args.target == args.source:
        print("source and target are the same; nothing to do")
        return 0

    targets = [args.target] if args.target else [v for v in SKILL_VENDORS if v != args.source]
    # Only sync to targets that actually have a skills/ directory in this repo.
    targets = [t for t in targets if (runtime_dir(t) / "skills").is_dir()]

    print("Note: agents are not synced (formats diverge across vendors).\n")
    total_drift = 0
    for t in targets:
        total_drift += report(args.source, t, args.apply)
        print()

    print("── summary ──")
    if total_drift == 0:
        print("  ✓ all targets in sync")
        return 0
    if args.apply:
        print(f"  applied changes for {total_drift} drift item(s)")
        return 0
    print(f"  {total_drift} drift item(s); re-run with --apply to sync")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
