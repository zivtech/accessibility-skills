#!/usr/bin/env python3
"""Scan tracked files for client-engagement identifiers.

This repo is public. Client-engagement identifiers must never appear in
tracked file content or in tracked file paths. Four pattern groups are
checked (the first case-insensitively, as before; see PATTERNS):

  client codename   `nclc|nclcps|zenyth`                        (case-insensitive)
  product name      `airnow|comptox|dtxsid|ctx-api`             (case-insensitive)
                    — the agency name alone ("EPA") stays allowed; the
                    products, hosts, API paths, and identifier schemes of a
                    named engagement do not (ruling 2026-09-02: nothing
                    beyond the agency name, anywhere, including receipts).
  operation id      `\\bCTX-\\d+\\b|\\bAN\\d{2}\\b`                   (case-SENSITIVE:
                    engagement operation IDs are upper-case; word boundaries
                    keep base64/hex blobs and prose from false-firing)
  receipt profile   `siteimprove_detector|epa_post_capture`     (case-insensitive)

No allowlist, with exactly one exception: this file itself, which necessarily
spells the patterns it scans for and would otherwise fail its own check the
moment it became tracked. Every other tracked file is scanned unconditionally.
If a legitimate false positive shows up later, add an allowlist deliberately
rather than suppressing silently.

`--self-test` runs a positive and a negative control through every pattern
(a 0-hit scan is only meaningful if the patterns provably fire) and exits 1
if any control misbehaves. CI runs the self-test before the scan.

Exit 1 with a file:line listing on any hit; exit 0 if none found.

Run from repo root:
    python3 scripts/check_client_refs.py --self-test
    python3 scripts/check_client_refs.py
"""

import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATTERNS = [
    ("client codename", re.compile(r"nclc|nclcps|zenyth", re.IGNORECASE)),
    ("product name", re.compile(r"airnow|comptox|dtxsid|ctx-api", re.IGNORECASE)),
    ("operation id", re.compile(r"\bCTX-\d+\b|\bAN\d{2}\b")),
    ("receipt profile", re.compile(r"siteimprove_detector|epa_post_capture", re.IGNORECASE)),
]

# Positive / negative controls per pattern group. Every positive must fire;
# every negative must not. Negatives are chosen from the false-positive
# classes the word boundaries and case-sensitivity exist to exclude.
CONTROLS = {
    "client codename": (["nclc", "NCLCPS", "Zenyth"], ["uncle", "zenith"]),
    "product name": (["AirNow", "comptox.epa.gov", "DTXSID123", "ctx-api/v1"], ["EPA public site", "airflow", "context-api"]),
    "operation id": (["CTX-08-OP-RETURN", "AN19"], ["ctx-10", "an19", "xAN19y", "ANNEX12", "SPAN12"]),
    "receipt profile": (["siteimprove_detector_v1", "EPA_POST_CAPTURE"], ["siteimprove detector", "post_capture"]),
}

# The only self-exclusion. This file spells the patterns in its docstring and
# in PATTERNS above, so scanning itself would guarantee a false failure.
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


def matches(text):
    """Return the names of every pattern group that fires on `text`."""
    return [name for name, pattern in PATTERNS if pattern.search(text)]


def scan_path(rel_path):
    """Return hits for the path string itself (file and directory names)."""
    groups = matches(rel_path)
    return [f"{rel_path} (path): {', '.join(groups)}"] if groups else []


def scan_file(rel_path):
    """Return list of 'rel_path:lineno: line' hits for a single tracked file."""
    abs_path = os.path.join(REPO, rel_path)
    hits = []
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                groups = matches(line)
                if groups:
                    hits.append(f"{rel_path}:{lineno}: [{', '.join(groups)}] {line.strip()[:160]}")
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        # Binary files, dangling symlink targets, etc. — not text to scan.
        return []
    return hits


def self_test():
    """Positive and negative controls for every pattern group. Exit 1 on any miss."""
    failures = []
    for name, pattern in PATTERNS:
        positives, negatives = CONTROLS[name]
        for sample in positives:
            if not pattern.search(sample):
                failures.append(f"{name}: positive control did not fire: {sample!r}")
        for sample in negatives:
            if pattern.search(sample):
                failures.append(f"{name}: negative control fired: {sample!r}")
    if failures:
        print("Client-reference self-test FAILED:")
        for failure in failures:
            print(f"  {failure}")
        sys.exit(1)
    total = sum(len(p) + len(n) for p, n in CONTROLS.values())
    print(f"Client-reference self-test passed — {len(PATTERNS)} pattern groups, {total} controls.")
    sys.exit(0)


def main():
    if "--self-test" in sys.argv[1:]:
        self_test()

    all_hits = []
    for rel_path in tracked_files():
        if rel_path == SELF_PATH:
            continue
        all_hits.extend(scan_path(rel_path))
        all_hits.extend(scan_file(rel_path))

    if all_hits:
        print("Client-reference scan FAILED — hits found:")
        for hit in all_hits:
            print(f"  {hit}")
        print(f"\n{len(all_hits)} hit(s) across tracked files.")
        sys.exit(1)

    print("Client-reference scan passed — no hits in tracked files or paths.")
    sys.exit(0)


if __name__ == "__main__":
    main()
