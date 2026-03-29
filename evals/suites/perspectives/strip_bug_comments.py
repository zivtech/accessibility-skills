#!/usr/bin/env python3
"""Strip // BUG: and /* BUG: comments from fixture .md files for blind evaluation.

Reads fixtures/*.md, removes hint comments from code blocks only,
writes clean versions to fixtures-eval/. Original files preserved.

Usage:
    python3 strip_bug_comments.py
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE, "fixtures")
OUT_DIR = os.path.join(BASE, "fixtures-eval")


def strip_bug_comments(content: str) -> str:
    """Remove // BUG: and /* BUG: comments from code blocks in markdown."""
    lines = content.split("\n")
    result = []
    in_code_block = False
    stripped = 0

    for line in lines:
        # Track code block boundaries
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if not in_code_block:
            result.append(line)
            continue

        # Inside a code block — strip BUG hint comments
        # Pattern 1: Full-line // BUG: comment (possibly with leading whitespace)
        if re.match(r"^\s*//\s*BUG:", line):
            stripped += 1
            continue

        # Pattern 2: Inline // BUG: comment at end of code line
        cleaned = re.sub(r"\s*//\s*BUG:.*$", "", line)
        if cleaned != line:
            stripped += 1
            if cleaned.strip():  # Keep the code part if non-empty
                result.append(cleaned)
            continue

        # Pattern 3: /* BUG: ... */ single-line block comment
        if re.match(r"^\s*/\*\s*BUG:.*\*/\s*$", line):
            stripped += 1
            continue

        # Pattern 4: Inline /* BUG: ... */ within a line
        cleaned = re.sub(r"\s*/\*\s*BUG:.*?\*/", "", line)
        if cleaned != line:
            stripped += 1
            if cleaned.strip():
                result.append(cleaned)
            continue

        result.append(line)

    return "\n".join(result), stripped


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    total_files = 0
    total_stripped = 0

    for fname in sorted(os.listdir(SRC_DIR)):
        if not fname.endswith(".md"):
            continue

        src_path = os.path.join(SRC_DIR, fname)
        out_path = os.path.join(OUT_DIR, fname)

        with open(src_path, "r") as f:
            content = f.read()

        cleaned, count = strip_bug_comments(content)

        with open(out_path, "w") as f:
            f.write(cleaned)

        total_files += 1
        total_stripped += count
        if count > 0:
            print(f"  {fname}: stripped {count} BUG comments")
        else:
            print(f"  {fname}: clean (no BUG comments)")

    print(f"\nProcessed {total_files} files, stripped {total_stripped} BUG comments")
    print(f"Clean fixtures written to: {OUT_DIR}/")


if __name__ == "__main__":
    main()
