#!/usr/bin/env python3
"""Report drift between .claude/skills/ and .agents/skills/ mirror surfaces.

Checks per skill directory:
1. Heading set diff (## headings present in one surface but not the other)
2. .Codex/ path hits in the .agents/ file (broken paths)
3. Diff stat (count of differing lines)
4. References files: byte-for-byte match

Always exits 0 in report-only mode (default).
Use --strict to exit 1 on any .Codex/ hit or heading-set difference.
Plan 004 will wire --strict into CI after syncing the mirrors.

Run from repo root:
    python3 scripts/check_mirrors.py
    python3 scripts/check_mirrors.py --strict
"""

import difflib
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAUDE_SKILLS = os.path.join(REPO, ".claude", "skills")
AGENTS_SKILLS = os.path.join(REPO, ".agents", "skills")

SKILL_NAMES = ["a11y-critic", "a11y-planner", "a11y-test", "perspective-audit"]


def extract_headings(text):
    """Return list of ## headings (stripped) from markdown text."""
    return [
        line.strip()
        for line in text.splitlines()
        if re.match(r"^## ", line)
    ]


def count_codex_hits(text, path):
    """Return list of (line_number, line) for lines containing .Codex/ in text."""
    hits = []
    for i, line in enumerate(text.splitlines(), start=1):
        if ".Codex/" in line:
            hits.append((i, line.strip()))
    return hits


def diff_stat(text_a, text_b, label_a, label_b):
    """Return count of differing lines via unified_diff."""
    lines_a = text_a.splitlines(keepends=True)
    lines_b = text_b.splitlines(keepends=True)
    diff = list(difflib.unified_diff(lines_a, lines_b, fromfile=label_a, tofile=label_b))
    # Count changed lines (lines starting with + or - but not the header lines +++ / ---)
    changed = sum(
        1 for line in diff
        if (line.startswith("+") and not line.startswith("+++"))
        or (line.startswith("-") and not line.startswith("---"))
    )
    return changed


def check_skill(skill_name, strict_mode):
    """Check mirrors for one skill. Returns has_drift (bool)."""
    claude_skill_file = os.path.join(CLAUDE_SKILLS, skill_name, "SKILL.md")
    agents_skill_file = os.path.join(AGENTS_SKILLS, skill_name, "SKILL.md")

    print(f"\n=== {skill_name} ===")

    has_drift = False

    if not os.path.isfile(claude_skill_file):
        print(f"  MISSING: {claude_skill_file}")
        return True
    if not os.path.isfile(agents_skill_file):
        print(f"  MISSING: {agents_skill_file}")
        return True

    with open(claude_skill_file) as f:
        claude_text = f.read()
    with open(agents_skill_file) as f:
        agents_text = f.read()

    # 1. Heading drift
    claude_headings = set(extract_headings(claude_text))
    agents_headings = set(extract_headings(agents_text))

    only_in_claude = claude_headings - agents_headings
    only_in_agents = agents_headings - claude_headings

    if only_in_claude or only_in_agents:
        has_drift = True
        print(f"  Heading drift detected:")
        for h in sorted(only_in_claude):
            print(f"    - only in .claude/: {h}")
        for h in sorted(only_in_agents):
            print(f"    + only in .agents/: {h}")
    else:
        print(f"  Headings: identical ({len(claude_headings)} headings)")

    # 2. .Codex/ hits in .agents/ file
    codex_hits = count_codex_hits(agents_text, agents_skill_file)
    if codex_hits:
        has_drift = True
        print(f"  .Codex/ hits in .agents/ file: {len(codex_hits)}")
        for lineno, line in codex_hits:
            print(f"    line {lineno}: {line[:100]}")
    else:
        print(f"  .Codex/ hits: none")

    # 3. Diff stat
    changed = diff_stat(claude_text, agents_text, f".claude/{skill_name}", f".agents/{skill_name}")
    print(f"  Diff stat: {changed} differing lines")

    # 4. References files
    claude_refs_dir = os.path.join(CLAUDE_SKILLS, skill_name, "references")
    agents_refs_dir = os.path.join(AGENTS_SKILLS, skill_name, "references")

    if os.path.isdir(claude_refs_dir) or os.path.isdir(agents_refs_dir):
        claude_refs = set(os.listdir(claude_refs_dir)) if os.path.isdir(claude_refs_dir) else set()
        agents_refs = set(os.listdir(agents_refs_dir)) if os.path.isdir(agents_refs_dir) else set()
        all_refs = claude_refs | agents_refs

        if not all_refs:
            print(f"  References: no files")
        else:
            for fname in sorted(all_refs):
                claude_ref_path = os.path.join(claude_refs_dir, fname)
                agents_ref_path = os.path.join(agents_refs_dir, fname)
                if fname not in claude_refs:
                    print(f"  References: {fname} — only in .agents/ (MISSING from .claude/)")
                    has_drift = True
                elif fname not in agents_refs:
                    print(f"  References: {fname} — only in .claude/ (MISSING from .agents/)")
                    has_drift = True
                else:
                    with open(claude_ref_path, "rb") as f:
                        claude_bytes = f.read()
                    with open(agents_ref_path, "rb") as f:
                        agents_bytes = f.read()
                    if claude_bytes == agents_bytes:
                        print(f"  References: {fname} — MATCH")
                    else:
                        print(f"  References: {fname} — DIFFER")
                        has_drift = True
    else:
        print(f"  References: no references dir in either surface")

    return has_drift


def main():
    strict_mode = "--strict" in sys.argv

    if strict_mode:
        print("Running in STRICT mode — will exit 1 on any drift")
    else:
        print("Running in report-only mode (use --strict to exit 1 on drift)")

    any_drift = False
    for skill_name in SKILL_NAMES:
        drift = check_skill(skill_name, strict_mode)
        if drift:
            any_drift = True

    print()
    if any_drift:
        print("Drift detected across mirror surfaces (see above)")
    else:
        print("No drift detected — mirrors are in sync")

    print("MODE: report-only (strict mode enabled by plan 004)")

    if strict_mode and any_drift:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
