#!/usr/bin/env python3
"""Fail-closed guard against silent edits to generated or frozen files.

A generated or frozen evidence file (a receipt, a freeze snapshot, a
hash-bound manifest, a rendered report) carries a hash or a signature that a
later hand-edit silently invalidates — the file still looks fine, but the
freeze/receipt chain it anchored is now a lie. This has happened to a human
and to more than one AI agent hitting the *same* repo with nothing warning
them. It is a repo trap, not a competence failure: three different actors
tripping one trap is a property of the repo.

The fix is deliberately small, structurally parallel to check_mirrors.py: a
manifest of frozen paths plus a one-line-equivalent check —
`git diff --name-only <range> | grep -Ff <manifest>` — wired into pre-commit
or CI so an edit to any listed path fails closed until a human re-freezes it
from stable sources and updates the manifest.

The manifest lists paths for ONE project and is project-specific; keep it out
of any shared skill bundle. This repo ships `frozen-files.manifest.example`
as the format template, never a real project's list.

Usage:
    python3 scripts/check_frozen_files.py [--manifest PATH] [--staged | --range REV]

    --manifest PATH   Manifest of frozen paths (default: frozen-files.manifest
                      at the repo root). One path per line; blank lines and
                      lines starting with '#' are ignored.
    --staged          Check staged changes only (default; pre-commit use).
    --range REV       Check the diff against REV instead (e.g. origin/main).

Exit status: 0 = no frozen path touched; 1 = a frozen path was modified, or
the manifest is missing/unreadable.
"""

import argparse
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MANIFEST = os.path.join(REPO, "frozen-files.manifest")


def load_manifest(path):
    """Return the set of frozen paths, or None if the manifest is unreadable."""
    if not os.path.isfile(path):
        return None
    frozen = set()
    with open(path) as f:
        for line in f:
            entry = line.strip()
            if entry and not entry.startswith("#"):
                frozen.add(entry)
    return frozen


def changed_files(staged, range_rev):
    """Return the set of changed repo-relative paths for the requested scope."""
    if range_rev:
        cmd = ["git", "-C", REPO, "diff", "--name-only", range_rev]
    else:
        cmd = ["git", "-C", REPO, "diff", "--cached", "--name-only"]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    return {line.strip() for line in out.splitlines() if line.strip()}


def main():
    parser = argparse.ArgumentParser(description="Guard frozen files against silent edits.")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--staged", action="store_true", default=True)
    parser.add_argument("--range", dest="range_rev", default=None)
    args = parser.parse_args()

    frozen = load_manifest(args.manifest)
    if frozen is None:
        print(f"MISSING manifest: {args.manifest}")
        print("Create it (see frozen-files.manifest.example) or pass --manifest.")
        return 1
    if not frozen:
        print(f"Manifest {args.manifest} lists no frozen paths — nothing to guard.")
        return 0

    touched = changed_files(args.staged, args.range_rev) & frozen
    if touched:
        print("FROZEN FILE EDIT DETECTED — fail closed. These paths are hash- or")
        print("freeze-bound; a hand-edit silently invalidates their receipt chain:")
        for path in sorted(touched):
            print(f"    {path}")
        print("Re-freeze from stable sources and update the manifest, or revert the edit.")
        print("This is a repo trap, not a competence failure — the guard is the warning")
        print("the repo previously lacked.")
        return 1

    print(f"No frozen path touched ({len(frozen)} guarded).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
