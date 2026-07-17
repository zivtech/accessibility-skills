#!/usr/bin/env python3
"""Regression guard: no benchmark prompt may contain a fixture's answer key,
inline planted-bug hint comments, or eval-authored reassurance/verdict text.

Added post-003 (2026-07-13) after finding that both runners fed raw fixtures —
including the '## Accessibility Issues (Planted Bugs)' sections — to every lane
that ever ran. Extended 2026-07-16 after finding that inline `// BUG: …` /
`{/* BUG: … */}` hint comments inside fixture code blocks survived answer-key
stripping and reached models in every prompt-based lane (24/33 critic and
20/25 perspective fixtures; fixtures de-hinted the same day — see the
hint-comment disclosure in ollama/BENCHMARK.md).

Extended again later on 2026-07-16 (reassurance follow-up): the mirror-image
leak — eval-authored reassurance ("NOT a bug", "Works:/Good:" annotations,
"should NOT be flagged") and, worse, verdict-revealing Difficulty Level/Notes
sections in the 7 critic fixtures that had no `## Accessibility Issues` cut
line at all (4 CLEAN + 3 ADVERSARIAL), whose expected verdict and grading
criteria therefore reached every prompt. Fixtures were fixed the same day
(reassurance comments removed; cut-line headings inserted); the REASSURANCE
patterns below keep both regressions out.

Builds real prompt content through BOTH runners for EVERY critic, perspective,
and planner fixture and fails if any answer-key marker, hint pattern, or
reassurance pattern survives.

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
# `bug` immediately after a comment opener. Title-case names like
# "Focus Restoration Bug" in fixture titles intentionally do not match —
# defect-naming titles are a known, disclosed residual (fixture ids double as
# filenames and result keys, so renaming is a separate decision).
HINT_PATTERNS = (
    ("BUG token", re.compile(r"\bBUG\b")),
    ("comment-marker bug", re.compile(r"(?i)(?://|/\*|\{/\*|<!--)\s*bug\b")),
)

# Reassurance/verdict leakage (2026-07-16 follow-up): eval-authored text that
# tells the model what NOT to flag or what verdict to reach. Each pattern is a
# machine-checkable invariant that holds corpus-wide above the blind cut line;
# realistic dev documentation (contrast ratios, "passes AA", rationale
# comments) deliberately does not match.
REASSURANCE_PATTERNS = (
    ("not-a-bug reassurance", re.compile(r"(?i)\bnot a bug\b")),
    ("flag-steering", re.compile(r"(?i)(?:should not|must not|won'?t|do(?:es)? not|don'?t|not\s+to)\s+(?:be\s+)?flag")),
    ("works/good annotation", re.compile(r"(?i)(?://|/\*|\{/\*|<!--)\s*(?:works|good)\b")),
    # Verdict-shaped phrasings only — mid-sentence mechanism rationale like
    # "recompute … so children … are handled correctly" is realistic and allowed.
    ("comment self-verdict", re.compile(r"(?i)(?://|/\*|\{/\*|<!--)[^\n]*(?:—\s*correct(?:ly)?\b|\bcorrectly implemented\b|\bworks correctly\b|\bis correct\b)")),
    ("comment color-only denial", re.compile(r"(?i)(?://|/\*|\{/\*|<!--)[^\n]*\bnot\s+color-?only\b")),
    ("difficulty verdict token", re.compile(r"\*\*(?:CLEAN|ADVERSARIAL|HAS-BUGS|FLAWED)\*\*")),
    ("tier suffix in title", re.compile(r"\((?:CLEAN|ADVERSARIAL|HAS-BUGS|FLAWED)\)")),
    ("fixture-class reveal", re.compile(r"(?i)\b(?:adversarial|clean)\s+fixture\b")),
    ("grading-notes voice", re.compile(r"(?i)a11y-critic should\b")),
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
    for name, pattern in REASSURANCE_PATTERNS:
        match = pattern.search(content)
        if match:
            failures.append(f"{label} {fid}: reassurance leak ({name}): {match.group(0)!r}")


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
        "no answer-key markers, no hint comments, no reassurance/verdict text."
    )


if __name__ == "__main__":
    main()
