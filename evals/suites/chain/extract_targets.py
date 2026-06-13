#!/usr/bin/env python3
"""Extract component files from fixture .md files for chain eval runs.

For each of the 8 chain fixtures, reads the source fixture .md, extracts fenced
code blocks, strips // BUG: and /* BUG: */ comments (exact patterns from
evals/suites/perspectives/strip_bug_comments.py), and writes real component files
to evals/suites/chain/targets/<fixture-id>/.

Also writes a README.md per target dir with the fixture's expected-behavior prose
(so the scout has context a real repo would have).

Deterministic: re-running overwrites identically. No network calls, no external
dependencies — stdlib only.

Usage:
    python3 evals/suites/chain/extract_targets.py
"""
import os
import re
import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))

FIXTURES = [
    # (fixture_id, source_suite_dir)
    ("modal-broken-focus-trap",      os.path.join(REPO_ROOT, "evals/suites/perspectives/fixtures")),
    ("product-carousel-autoplay",    os.path.join(REPO_ROOT, "evals/suites/perspectives/fixtures")),
    ("video-tutorial-no-captions",   os.path.join(REPO_ROOT, "evals/suites/perspectives/fixtures")),
    ("login-form-clean",             os.path.join(REPO_ROOT, "evals/suites/perspectives/fixtures")),
    ("article-page-clean",           os.path.join(REPO_ROOT, "evals/suites/perspectives/fixtures")),
    ("tabbed-nav-vs-tab-pattern",    os.path.join(REPO_ROOT, "evals/suites/a11y-critic/fixtures")),
    ("app-focus-order-illogical",    os.path.join(REPO_ROOT, "evals/suites/a11y-critic/fixtures")),
    ("toast-notification-no-role",   os.path.join(REPO_ROOT, "evals/suites/a11y-critic/fixtures")),
]
# NOTE: site-breadcrumb-nav (all-LOW never-escalate probe, plan 011) is CHAIN-NATIVE — it has
# no source fixture in another suite, so it is intentionally absent from FIXTURES above.
# Re-running this script regenerates only the 8 listed targets and leaves it untouched.

# Map fence language tag → output filename
LANG_TO_FILENAME = {
    "jsx":        "component.jsx",
    "tsx":        "component.tsx",
    "js":         "component.js",
    "ts":         "component.ts",
    "css":        "styles.css",
    "html":       "index.html",
    "scss":       "styles.scss",
}


# ---------------------------------------------------------------------------
# Bug comment stripping (mirrors strip_bug_comments.py:18-65 exactly)
# ---------------------------------------------------------------------------

def strip_bug_comments(content: str):
    """Remove // BUG: and /* BUG: comments from code blocks in markdown.

    Returns (cleaned_content, stripped_count).
    Extends strip_bug_comments.py:18-65 with multi-line /* ... */ block support.
    Handles both bare /* */ and JSX {/* */} forms, including blocks where the
    opening /* is on its own line and BUG: appears in the body (modal pattern).
    """
    lines = content.split("\n")
    result = []
    in_code_block = False
    in_block_comment = False   # inside any /* */ block comment
    block_has_bug = False      # current block comment contains BUG:
    block_buffer = []          # lines accumulated while scanning the block
    stripped = 0

    def flush_block(is_bug: bool):
        nonlocal stripped
        if is_bug:
            stripped += len(block_buffer)
            return []   # drop all lines in the block
        else:
            return list(block_buffer)  # keep them

    for line in lines:
        # Track markdown code block boundaries
        if line.strip().startswith("```"):
            # Flush any open block comment state
            if in_block_comment:
                result.extend(flush_block(block_has_bug))
                in_block_comment = False
                block_has_bug = False
                block_buffer = []
            in_code_block = not in_code_block
            result.append(line)
            continue

        if not in_code_block:
            result.append(line)
            continue

        # Inside a code block -----------------------------------------------

        # If we are accumulating a multi-line block comment
        if in_block_comment:
            block_buffer.append(line)
            # Check if this line contains BUG:
            if "BUG:" in line:
                block_has_bug = True
            # Check if this line closes the block comment
            if re.search(r"\*/", line):
                result.extend(flush_block(block_has_bug))
                block_buffer = []
                in_block_comment = False
                block_has_bug = False
            continue

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

        # Pattern 3: /* BUG: ... */ single-line block comment (bare or in JSX {})
        if re.match(r"^\s*\{?/\*\s*BUG:.*\*/\}?\s*$", line):
            stripped += 1
            continue

        # Pattern 4: Inline /* BUG: ... */ single-line within a larger line
        cleaned = re.sub(r"\s*/\*\s*BUG:.*?\*/", "", line)
        if cleaned != line:
            stripped += 1
            if cleaned.strip():
                result.append(cleaned)
            continue

        # Pattern 5: Opening of a multi-line block comment — /* or {/*
        # Capture opening line; scan forward for BUG: and closing */
        if re.match(r"^\s*\{?/\*", line) and not re.search(r"\*/", line):
            in_block_comment = True
            block_has_bug = "BUG:" in line
            block_buffer = [line]
            continue

        result.append(line)

    # Flush any unclosed block comment at end of input
    if in_block_comment and block_buffer:
        result.extend(flush_block(block_has_bug))

    return "\n".join(result), stripped


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

def extract_code_blocks(md_content: str):
    """Return list of (language, code_content) tuples from fenced code blocks.

    Only extracts blocks with a recognized language tag. Unlanguaged blocks
    and blocks with unknown tags are skipped.
    """
    blocks = []
    lines = md_content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^```(\w+)\s*$", line.strip())
        if m:
            lang = m.group(1).lower()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            # skip closing ```
            if lang in LANG_TO_FILENAME:
                blocks.append((lang, "\n".join(code_lines)))
        i += 1
    return blocks


def build_readme(fixture_id: str, metadata: dict, md_content: str) -> str:
    """Build a README.md for the target dir.

    Includes fixture name, description, and expected-behavior sections extracted
    from the .md prose. Deliberately omits difficulty, expected findings, and
    alarm levels — this is context a real repo would have, not evaluation hints.
    """
    name = metadata.get("name", fixture_id)
    description = metadata.get("description", "")
    if hasattr(description, "strip"):
        description = description.strip()

    # Extract "Expected Behavior" or "Accessibility Features Present" sections
    # from the fixture markdown prose (appear after the code blocks)
    behavior_lines = []
    in_behavior = False
    for line in md_content.split("\n"):
        if re.match(r"^#+\s*(Expected Behavior|Accessibility Features Present)", line, re.IGNORECASE):
            in_behavior = True
            behavior_lines.append(line)
            continue
        if in_behavior:
            # Stop at the next heading or planted-bug section
            if re.match(r"^#+\s*", line) and behavior_lines:
                if re.search(r"bug|issue|planted|accessibility issues", line, re.IGNORECASE):
                    break
                # Continue into the next behavior-level section heading
                behavior_lines.append(line)
            else:
                behavior_lines.append(line)

    behavior_section = "\n".join(behavior_lines).strip()

    parts = [
        f"# {name}",
        "",
        "## Description",
        "",
        description,
        "",
    ]
    if behavior_section:
        parts += [behavior_section, ""]

    parts += [
        "---",
        "",
        "_This directory contains component files extracted from the a11y eval suite for chain evaluation._",
        "_Run `/a11y-workflow full evals/suites/chain/targets/" + fixture_id + "/component.jsx` to start the chain._",
    ]
    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_fixture(fixture_id: str, src_dir: str, out_base: str) -> dict:
    """Extract one fixture into out_base/<fixture_id>/.

    Returns a stats dict: {fixture_id, files_written, bug_comments_stripped}.
    """
    md_path = os.path.join(src_dir, f"{fixture_id}.md")
    yaml_path = os.path.join(src_dir, f"{fixture_id}.metadata.yaml")

    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Fixture not found: {md_path}")
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"Metadata not found: {yaml_path}")

    with open(md_path, "r") as f:
        raw_md = f.read()
    with open(yaml_path, "r") as f:
        metadata = yaml.safe_load(f)

    # Strip BUG comments from the whole markdown document first
    cleaned_md, total_stripped = strip_bug_comments(raw_md)

    # Extract code blocks from the cleaned markdown
    blocks = extract_code_blocks(cleaned_md)

    # Create output directory
    out_dir = os.path.join(out_base, fixture_id)
    os.makedirs(out_dir, exist_ok=True)

    files_written = []

    # Write code blocks — if two blocks share the same language tag, append index
    lang_seen = {}
    for lang, code in blocks:
        base_name = LANG_TO_FILENAME[lang]
        count = lang_seen.get(lang, 0)
        if count == 0:
            filename = base_name
        else:
            stem, ext = os.path.splitext(base_name)
            filename = f"{stem}-{count}{ext}"
        lang_seen[lang] = count + 1

        out_path = os.path.join(out_dir, filename)
        with open(out_path, "w") as f:
            f.write(code.rstrip() + "\n")
        files_written.append(filename)

    # Write README.md (from original raw markdown, not the cleaned version —
    # behavior prose doesn't contain BUG hints so this is safe; and we want
    # the full human-readable description)
    readme_content = build_readme(fixture_id, metadata, raw_md)
    readme_path = os.path.join(out_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)
    files_written.append("README.md")

    return {
        "fixture_id": fixture_id,
        "files_written": files_written,
        "bug_comments_stripped": total_stripped,
    }


def main():
    out_base = os.path.join(BASE, "targets")
    os.makedirs(out_base, exist_ok=True)

    total_fixtures = 0
    total_files = 0
    total_stripped = 0

    for fixture_id, src_dir in FIXTURES:
        result = process_fixture(fixture_id, src_dir, out_base)
        n_files = len(result["files_written"])
        n_stripped = result["bug_comments_stripped"]
        total_fixtures += 1
        total_files += n_files
        total_stripped += n_stripped
        print(f"  {fixture_id}: {n_files} files ({', '.join(result['files_written'])}) — {n_stripped} BUG comments stripped")

    print(f"\nProcessed {total_fixtures} fixtures, {total_files} files total, {total_stripped} BUG comments stripped")
    print(f"Targets written to: {out_base}/")


if __name__ == "__main__":
    main()
