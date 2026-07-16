#!/usr/bin/env python3
"""Lint SKILL.md files across both mirror surfaces.

Checks per SKILL.md:
1. YAML frontmatter parses and carries the required keys (name, description)
2. Frontmatter name matches the skill directory name
3. Code fences balance: no fence left open at EOF, and no 3-backtick fence
   with an info string nested inside an open 3-backtick block (breaks GitHub
   rendering — the inner block's bare closer terminates the outer block;
   wrap outer template blocks in 4-backtick fences instead)

Exit 1 on any failure; exit 0 if all pass.

Run from repo root:
    python3 scripts/lint_skills.py
"""

import glob
import os
import re
import sys

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SURFACES = [".claude/skills", ".agents/skills"]
REQUIRED_KEYS = ("name", "description")

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
# CommonMark: a code fence may be indented at most 3 spaces; 4+ means the
# backticks are ordinary content (e.g. examples nested inside an open block).
FENCE_RE = re.compile(r"^ {0,3}(`{3,})(.*)$")


def check_frontmatter(path, text):
    """Return list of problems with the YAML frontmatter."""
    problems = []
    m = FRONTMATTER_RE.match(text)
    if not m:
        return [f"{path}: no YAML frontmatter block"]
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception as e:
        return [f"{path}: frontmatter does not parse: {e}"]
    if not isinstance(fm, dict):
        return [f"{path}: frontmatter is not a mapping"]
    for key in REQUIRED_KEYS:
        if not fm.get(key):
            problems.append(f"{path}: frontmatter missing required key '{key}'")
    dir_name = os.path.basename(os.path.dirname(path))
    if fm.get("name") and fm["name"] != dir_name:
        problems.append(
            f"{path}: frontmatter name '{fm['name']}' != directory '{dir_name}'"
        )
    return problems


def check_fences(path, text):
    """Return list of fence-balance problems (CommonMark close rules)."""
    problems = []
    open_fence = None  # (line_no, tick_count)
    for i, line in enumerate(text.splitlines(), start=1):
        m = FENCE_RE.match(line)
        if not m:
            continue
        ticks, info = len(m.group(1)), m.group(2).strip()
        if open_fence is None:
            open_fence = (i, ticks)
        elif ticks >= open_fence[1] and not info:
            open_fence = None
        elif ticks == 3 and open_fence[1] == 3 and info:
            problems.append(
                f"{path}:{i}: 3-backtick '{info}' fence nested inside the "
                f"3-backtick block opened at line {open_fence[0]} — its bare "
                f"closer will terminate the outer block early; use a "
                f"4-backtick outer fence"
            )
    if open_fence is not None:
        problems.append(
            f"{path}:{open_fence[0]}: code fence never closed before EOF"
        )
    return problems


def main():
    paths = []
    for surface in SURFACES:
        paths.extend(
            sorted(glob.glob(os.path.join(REPO, surface, "*", "SKILL.md")))
        )
    if not paths:
        print("No SKILL.md files found — wrong working directory?")
        sys.exit(1)

    problems = []
    for path in paths:
        with open(path) as f:
            text = f.read()
        rel = os.path.relpath(path, REPO)
        problems.extend(check_frontmatter(rel, text))
        problems.extend(check_fences(rel, text))

    print(f"Linted {len(paths)} SKILL.md files across {len(SURFACES)} surfaces")
    if problems:
        for p in problems:
            print(f"  FAIL: {p}")
        sys.exit(1)
    print("All skill lint checks passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
