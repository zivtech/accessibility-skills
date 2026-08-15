#!/usr/bin/env python3
"""Scan tracked files for client-engagement identifiers.

This repo is public. Client-engagement project codenames must never appear
in tracked file content, paths, or comments. Checks the case-insensitive
pattern `nclc|nclcps|zenyth` against every git-tracked file's text content.

No allowlist, with exactly one exception: this file itself, which necessarily
spells the pattern it scans for and would otherwise fail its own check the
moment it became tracked. Every other tracked file is scanned unconditionally.
If a legitimate false positive shows up later, add an allowlist deliberately
rather than suppressing silently.

Exit 1 with a file:line listing on any hit; exit 0 if none found.

Run from repo root:
    python3 scripts/check_client_refs.py
"""

import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERN = re.compile(r"nclc|nclcps|zenyth", re.IGNORECASE)
# The only self-exclusion. This file spells the pattern in its docstring and
# in PATTERN above, so scanning itself would guarantee a false failure.
SELF_PATH = "scripts/check_client_refs.py"


def tracked_files():
    """Return list of git-tracked file paths, relative to REPO."""
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def scan_file(rel_path):
    """Return list of 'rel_path:lineno: line' hits for a single tracked file."""
    abs_path = os.path.join(REPO, rel_path)
    hits = []
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                if PATTERN.search(line):
                    hits.append(f"{rel_path}:{lineno}: {line.strip()}")
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        # Binary files, dangling symlink targets, etc. — not text to scan.
        return []
    return hits


def main():
    all_hits = []
    for rel_path in tracked_files():
        if rel_path == SELF_PATH:
            continue
        all_hits.extend(scan_file(rel_path))

    if all_hits:
        print("Client-reference scan FAILED — hits found:")
        for hit in all_hits:
            print(f"  {hit}")
        print(f"\n{len(all_hits)} hit(s) across tracked files.")
        sys.exit(1)

    print("Client-reference scan passed — no hits in tracked files.")
    sys.exit(0)


if __name__ == "__main__":
    main()
