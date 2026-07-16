#!/usr/bin/env python3
"""Regression guard: no benchmark prompt may contain a fixture's answer key
or inline planted-bug hint comments.

Added post-003 (2026-07-13) after finding that both runners fed raw fixtures —
including the '## Accessibility Issues (Planted Bugs)' sections — to every lane
that ever ran. Extended 2026-07-16 after finding that inline `// BUG: …` /
`{/* BUG: … */}` hint comments inside fixture code blocks survived answer-key
stripping and reached models in every prompt-based lane (24/33 critic and
20/25 perspective fixtures; fixtures de-hinted the same day — see the
hint-comment disclosure in ollama/BENCHMARK.md).

Builds real prompt content through BOTH runners for EVERY critic, perspective,
and planner fixture and fails if any answer-key marker or hint pattern
survives.

Run: python3 ollama/test_blind_prompts.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))

import run_benchmark as local_runner  # noqa: E402
import run_cloud_benchmark as cloud_runner  # noqa: E402

ANSWER_KEY_MARKERS = ("## Accessibility Issues", "Planted Bugs")

# Hint-comment leakage: the all-caps BUG token anywhere (comments, bare
# `BUG:` block-comment lines, prose `(BUG: …)` parentheticals), plus any-case
# `bug` immediately after a comment opener. Plain prose like "NOT a bug" or
# titles like "Focus Restoration Bug" intentionally do not match.
HINT_PATTERNS = (
    ("BUG token", re.compile(r"\bBUG\b")),
    ("comment-marker bug", re.compile(r"(?i)(?://|/\*|\{/\*|<!--)\s*bug\b")),
)


def fixture_ids(directory):
    return sorted(f[:-3] for f in os.listdir(directory) if f.endswith(".md"))


def leaks(label, fid, content, failures):
    for marker in ANSWER_KEY_MARKERS:
        if marker in content:
            failures.append(f"{label} {fid}: contains {marker!r}")
    for name, pattern in HINT_PATTERNS:
        match = pattern.search(content)
        if match:
            failures.append(f"{label} {fid}: hint leak ({name}): {match.group(0)!r}")


def main():
    failures = []
    checks = 0

    for runner, label in ((local_runner, "local"), (cloud_runner, "cloud")):
        # Critic suite: the fixture content each critic prompt embeds.
        for fid in fixture_ids(runner.FIXTURES_DIR):
            checks += 1
            leaks(f"{label} critic", fid, runner.load_fixture(fid), failures)
        # Perspective suite: the full composed user prompt.
        for fid in fixture_ids(runner.PERSPECTIVE_FIXTURES_DIR):
            checks += 1
            leaks(f"{label} perspective", fid, runner.build_escalation_prompt(fid), failures)
        # Planner suite: exempt from answer-key stripping (no answer sections),
        # checked anyway so a future fixture can't reintroduce either leak.
        for fid in fixture_ids(runner.PLANNER_FIXTURES_DIR):
            checks += 1
            leaks(f"{label} planner", fid, runner.load_fixture(fid, runner.PLANNER_FIXTURES_DIR), failures)

    if failures:
        print(f"FAIL — {len(failures)} leaked prompt(s) of {checks} checked:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    print(
        f"OK — {checks} prompts checked across both runners; "
        "no answer-key markers, no hint comments."
    )


if __name__ == "__main__":
    main()
