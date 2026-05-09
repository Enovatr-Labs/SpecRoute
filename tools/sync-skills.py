#!/usr/bin/env python3
"""Cross-runtime skill and agent sync.

Diff-and-copy `runtimes/.claude/` ↔ `runtimes/.codex/` for the artifact shapes
they share: skills (folder-per-skill `SKILL.md`) and agents (flat `<name>.md`).

Usage:
    python3 tools/sync-skills.py [--apply] [--source <claude|codex>]

  --apply              actually copy missing or drifted files (default is dry-run)
  --source <runtime>   which runtime is the source of truth (default: claude)

The default behavior is read-only: report what would change. Pass --apply to
actually copy files. Drift between two existing files is reported but never
auto-resolved without --apply (the `source` runtime's version wins on --apply).

This tool is a starting point - fork it for project-specific needs (e.g.
ignoring certain skills, applying transformations during copy).
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def runtime_dir(runtime: str) -> Path:
    return REPO_ROOT / "runtimes" / f".{runtime}"


def list_skills(runtime: str) -> set[str]:
    base = runtime_dir(runtime) / "skills"
    if not base.is_dir():
        return set()
    return {
        d.name
        for d in base.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    }


def list_agents(runtime: str) -> set[str]:
    base = runtime_dir(runtime) / "agents"
    if not base.is_dir():
        return set()
    return {
        f.stem
        for f in base.iterdir()
        if f.is_file() and f.suffix == ".md" and f.stem != "README"
    }


def skill_files(runtime: str, slug: str) -> list[Path]:
    """All files under a skill folder, recursively."""
    base = runtime_dir(runtime) / "skills" / slug
    if not base.is_dir():
        return []
    return [p for p in base.rglob("*") if p.is_file()]


def diff_skill(source: str, target: str, slug: str) -> list[str]:
    """Return a list of file-level differences between source and target skill folders."""
    src_base = runtime_dir(source) / "skills" / slug
    tgt_base = runtime_dir(target) / "skills" / slug
    diffs: list[str] = []

    src_files = {p.relative_to(src_base): p for p in src_base.rglob("*") if p.is_file()}
    tgt_files = {p.relative_to(tgt_base): p for p in tgt_base.rglob("*") if p.is_file()} if tgt_base.is_dir() else {}

    only_in_src = sorted(src_files.keys() - tgt_files.keys())
    only_in_tgt = sorted(tgt_files.keys() - src_files.keys())
    in_both = sorted(src_files.keys() & tgt_files.keys())

    for rel in only_in_src:
        diffs.append(f"  + {rel} (only in {source})")
    for rel in only_in_tgt:
        diffs.append(f"  - {rel} (only in {target})")
    for rel in in_both:
        if not filecmp.cmp(src_files[rel], tgt_files[rel], shallow=False):
            diffs.append(f"  ~ {rel} (drift)")
    return diffs


def diff_agent(source: str, target: str, slug: str) -> bool:
    """Return True if the source and target agent files differ."""
    src = runtime_dir(source) / "agents" / f"{slug}.md"
    tgt = runtime_dir(target) / "agents" / f"{slug}.md"
    if not src.is_file() or not tgt.is_file():
        return True
    return not filecmp.cmp(src, tgt, shallow=False)


def copy_skill(source: str, target: str, slug: str) -> None:
    src_base = runtime_dir(source) / "skills" / slug
    tgt_base = runtime_dir(target) / "skills" / slug
    if tgt_base.exists():
        shutil.rmtree(tgt_base)
    shutil.copytree(src_base, tgt_base)


def copy_agent(source: str, target: str, slug: str) -> None:
    src = runtime_dir(source) / "agents" / f"{slug}.md"
    tgt = runtime_dir(target) / "agents" / f"{slug}.md"
    tgt.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, tgt)


def report(source: str, target: str, apply: bool) -> int:
    """Returns 0 if everything is in sync, non-zero if drift was found."""
    src_skills = list_skills(source)
    tgt_skills = list_skills(target)
    src_agents = list_agents(source)
    tgt_agents = list_agents(target)

    only_src_skills = sorted(src_skills - tgt_skills)
    only_tgt_skills = sorted(tgt_skills - src_skills)
    shared_skills = sorted(src_skills & tgt_skills)
    only_src_agents = sorted(src_agents - tgt_agents)
    only_tgt_agents = sorted(tgt_agents - src_agents)
    shared_agents = sorted(src_agents & tgt_agents)

    drift_count = 0

    print(f"── skills: {source} (source) → {target} (target) ──")
    if only_src_skills:
        for slug in only_src_skills:
            print(f"  MISSING in {target}: skills/{slug}/")
            if apply:
                copy_skill(source, target, slug)
                print(f"    copied")
            drift_count += 1
    if only_tgt_skills:
        for slug in only_tgt_skills:
            print(f"  EXTRA in {target}: skills/{slug}/ (won't remove without explicit instruction)")
            drift_count += 1
    for slug in shared_skills:
        diffs = diff_skill(source, target, slug)
        if diffs:
            print(f"  DRIFT skills/{slug}/")
            for d in diffs:
                print(d)
            if apply:
                copy_skill(source, target, slug)
                print(f"    overwrote {target}/skills/{slug}/ with {source} version")
            drift_count += 1

    print(f"\n── agents: {source} (source) → {target} (target) ──")
    if only_src_agents:
        for slug in only_src_agents:
            print(f"  MISSING in {target}: agents/{slug}.md")
            if apply:
                copy_agent(source, target, slug)
                print(f"    copied")
            drift_count += 1
    if only_tgt_agents:
        for slug in only_tgt_agents:
            print(f"  EXTRA in {target}: agents/{slug}.md (won't remove without explicit instruction)")
            drift_count += 1
    for slug in shared_agents:
        if diff_agent(source, target, slug):
            print(f"  DRIFT agents/{slug}.md")
            if apply:
                copy_agent(source, target, slug)
                print(f"    overwrote {target}/agents/{slug}.md")
            drift_count += 1

    print(f"\n── summary ──")
    if drift_count == 0:
        print("  ✓ in sync")
        return 0
    if apply:
        print(f"  applied changes for {drift_count} drift item(s)")
        return 0
    print(f"  {drift_count} drift item(s); re-run with --apply to copy")
    return 1


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--apply", action="store_true", help="actually copy files (default: dry-run)")
    p.add_argument(
        "--source",
        default="claude",
        choices=["claude", "codex"],
        help="source of truth runtime (default: claude)",
    )
    args = p.parse_args()
    target = "codex" if args.source == "claude" else "claude"
    return report(args.source, target, args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
