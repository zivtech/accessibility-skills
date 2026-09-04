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


# ---------------------------------------------------------------------------
# Structural leak checks (issue #51, 2026-09-03).
#
# The three checks above ask "does the prompt contain a known bad string?".
# These ask the structural questions that let the leak happen in the first
# place: is the cut line where we think it is, and is every heading above it
# one somebody deliberately decided to show the model?
# ---------------------------------------------------------------------------

CANONICAL_CUT = "## Accessibility Issues"
CUT_RE = re.compile(r"^## Accessibility Issues.*$", re.MULTILINE)
FENCE_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
HEADING_RE = re.compile(r"^## (.+?)[ \t]*$", re.MULTILINE)

TITLE_MANIFEST = os.path.join(
    os.path.dirname(__file__), "..", "evals", "fixture-title-manifest.yaml"
)
TITLE_CLASSES = ("neutral", "names-defect", "asserts-feature")

# Suites whose fixtures carry an in-file answer key below the blind cut line.
# Within one of these, EVERY fixture must have exactly one canonical cut line —
# all-or-none. The 2026-07-16 regression was 7 critic fixtures that had none,
# so their whole answer key (including the expected verdict) reached the model
# while their siblings' was withheld.
ANSWER_KEY_SUITES = ("a11y-critic", "perspectives", "a11y-test-recipe")

# What each answer-key suite deliberately shows the model, and what it keeps
# behind the cut. A heading in neither list fails CI: a new leak now requires
# ADDING a line here, which is a reviewable act, rather than an omission
# nobody sees. `Accessibility Features Present/Implemented` is listed as
# visible because it currently is — that is issue #51's open leak class 2
# (45 of 50 critic fixtures), disclosed here rather than silently tolerated.
VISIBLE_HEADINGS = {
    "a11y-critic": (
        r"Component Code", r"CSS", r"CSS Styles", r"Expected Behavior",
        r"Accessibility Features (?:Present|Implemented)",
        r"Design Rationale(?: \(.+\))?", r"Recent Changes(?: \(.+\))?",
    ),
    "perspectives": (
        # Harness-injected by build_escalation_prompt, not fixture-authored.
        r"Component Under Review", r"Escalated Perspectives \(from a11y-critic\)",
        r"Component Code", r"CSS", r"Expected Behavior",
        r"Accessibility Features Present", r"Context",
    ),
    "a11y-test-recipe": (
        r"Component Code", r"CSS", r"Expected Behavior",
        r"Frameworks & Environment", r"Keyboard Test Recipe", r"Run Output",
    ),
}
EVAL_SIDE_HEADINGS = {
    "a11y-critic": (
        r"Accessibility Issues", r"Difficulty Level", r"Difficulty Rating",
        r"Frameworks & Environment", r"Notes", r"The Ambiguity",
    ),
    "perspectives": (
        r"Accessibility Issues", r"Difficulty Level", r"Frameworks",
        r"What Should NOT Be Flagged",
    ),
    "a11y-test-recipe": (r"Accessibility Issues", r"Difficulty Level"),
}


def headings(text):
    """`## ` headings outside fenced code blocks."""
    return [h.strip() for h in HEADING_RE.findall(FENCE_RE.sub("", text))]


def allowed(name, patterns):
    return any(re.fullmatch(p, name) for p in patterns)


def check_cut_lines(suite, label, directory, failures):
    """Per suite: all fixtures carry exactly one canonical cut line, or none do."""
    seen = {}
    for fid in fixture_ids(directory):
        with open(os.path.join(directory, fid + ".md")) as f:
            raw = f.read()
        cuts = CUT_RE.findall(raw)
        seen[fid] = len(cuts)
        for cut in cuts:
            if cut.strip() != CANONICAL_CUT:
                failures.append(
                    f"{label} {fid}: non-canonical cut line {cut.strip()!r} "
                    f"(must be exactly {CANONICAL_CUT!r})"
                )
        if len(cuts) > 1:
            failures.append(f"{label} {fid}: {len(cuts)} cut lines, expected 1")
    expected = 1 if suite in ANSWER_KEY_SUITES else 0
    for fid, n in seen.items():
        if n != expected:
            failures.append(
                f"{label} {fid}: {n} cut line(s), but suite {suite!r} expects "
                f"{expected} for every fixture (all-or-none)"
            )


def check_headings(suite, fid, prompt, raw, failures):
    """Every heading is declared either visible-to-the-model or eval-side."""
    if suite not in VISIBLE_HEADINGS:
        return
    vis = set(headings(prompt))
    for h in sorted(vis):
        if not allowed(h, VISIBLE_HEADINGS[suite]):
            failures.append(
                f"{suite} {fid}: undeclared heading reaches the model: '## {h}' "
                f"(add it to VISIBLE_HEADINGS[{suite!r}] only if the model "
                f"should see it, else move it below the cut line)"
            )
    for h in sorted(set(headings(raw)) - vis):
        if not allowed(h, EVAL_SIDE_HEADINGS[suite]):
            failures.append(
                f"{suite} {fid}: undeclared eval-side heading '## {h}' "
                f"(add it to EVAL_SIDE_HEADINGS[{suite!r}])"
            )


def check_titles(failures, manifest_path=None, suites_root=None):
    """Line 1 of every fixture is above the cut, so it reaches the model.
    evals/fixture-title-manifest.yaml declares what each one gives away; this
    fails when a fixture has no row, or when its H1 has drifted from one."""
    import yaml

    with open(manifest_path or TITLE_MANIFEST) as f:
        manifest = yaml.safe_load(f)
    checked = 0
    for suite, block in manifest["suites"].items():
        root = suites_root or os.path.join(
            os.path.dirname(__file__), "..", "evals", "suites"
        )
        directory = os.path.join(root, suite, "fixtures")
        rows = block["fixtures"]
        on_disk = set(fixture_ids(directory))
        for fid in sorted(on_disk - set(rows)):
            failures.append(
                f"title-manifest {suite} {fid}: no row in "
                f"evals/fixture-title-manifest.yaml (classify its H1)"
            )
        for fid in sorted(set(rows) - on_disk):
            failures.append(f"title-manifest {suite} {fid}: row has no fixture file")
        for fid in sorted(on_disk & set(rows)):
            checked += 1
            row = rows[fid]
            with open(os.path.join(directory, fid + ".md")) as f:
                h1 = f.readline().rstrip("\n")
            if h1 != "# " + row["title"]:
                failures.append(
                    f"title-manifest {suite} {fid}: H1 {h1!r} does not match "
                    f"manifest title {row['title']!r}"
                )
            if row["class"] not in TITLE_CLASSES:
                failures.append(
                    f"title-manifest {suite} {fid}: class {row['class']!r} not in "
                    f"{TITLE_CLASSES}"
                )
            if row["class"] == "neutral" and "neutral_title" in row:
                failures.append(
                    f"title-manifest {suite} {fid}: neutral row must not carry a "
                    f"neutral_title"
                )
            if row["class"] != "neutral" and not row.get("neutral_title"):
                failures.append(
                    f"title-manifest {suite} {fid}: class {row['class']!r} needs a "
                    f"neutral_title (the measurement variant)"
                )
    return checked


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


def self_test():
    """Negative controls: each structural check must fail on the defect it
    exists to catch. A gate nobody has seen fail is a gate nobody can trust."""
    import tempfile, textwrap

    cases = []

    def case(name, fn):
        f = []
        fn(f)
        cases.append((name, bool(f), f[:1]))

    case("undeclared visible heading", lambda f: check_headings(
        "a11y-critic", "canary",
        "# Fixture: X\n\n## Planted Defect Summary\n\nbody\n",
        "# Fixture: X\n\n## Planted Defect Summary\n\nbody\n", f))
    case("undeclared eval-side heading", lambda f: check_headings(
        "a11y-critic", "canary",
        "# Fixture: X\n\n## Component Code\n",
        "# Fixture: X\n\n## Component Code\n\n## Grading Notes\n", f))
    case("heading inside a code fence is not a heading", lambda f: check_headings(
        "a11y-critic", "canary",
        "# Fixture: X\n\n## Component Code\n\n```md\n## Not A Real Heading\n```\n",
        "# Fixture: X\n\n## Component Code\n\n```md\n## Not A Real Heading\n```\n", f))

    with tempfile.TemporaryDirectory() as d:
        fx = os.path.join(d, "a11y-critic", "fixtures")
        os.makedirs(fx)
        def write(fid, body):
            with open(os.path.join(fx, fid + ".md"), "w") as fh:
                fh.write(textwrap.dedent(body).lstrip())
        write("good", "# Fixture: Good\n\n## Component Code\n\n## Accessibility Issues\n")
        write("noncanonical", "# Fixture: Bad\n\n## Accessibility Issues (Planted)\n")
        write("nocut", "# Fixture: None\n\n## Component Code\n")
        case("non-canonical cut line", lambda f: check_cut_lines(
            "a11y-critic", "canary", fx, f))

        man = os.path.join(d, "manifest.yaml")
        with open(man, "w") as fh:
            fh.write(textwrap.dedent("""
                version: 1
                suites:
                  a11y-critic:
                    fixtures:
                      good:
                        title: "Fixture: Drifted"
                        class: neutral
            """).lstrip())
        case("H1 drift + unlisted fixtures", lambda f: check_titles(f, man, d))

        with open(man, "w") as fh:
            fh.write(textwrap.dedent("""
                version: 1
                suites:
                  a11y-critic:
                    fixtures:
                      good:
                        title: "Fixture: Good"
                        class: names-defect
                      noncanonical:
                        title: "Fixture: Bad"
                        class: neutral
                        neutral_title: "Fixture: Bad"
                      nocut:
                        title: "Fixture: None"
                        class: neutral
            """).lstrip())
        case("non-neutral row without neutral_title / neutral row with one",
             lambda f: check_titles(f, man, d))

    ok = True
    for name, fired, sample in cases:
        expect_fire = "not a heading" not in name
        good = fired == expect_fire
        ok &= good
        verb = "fires" if fired else "silent"
        print(f"  {'PASS' if good else 'FAIL'}  {name}: {verb}"
              + (f"\n          -> {sample[0]}" if sample else ""))
    if not ok:
        sys.exit("self-test FAILED — a structural check does not catch its own defect")
    print(f"OK — {len(cases)} structural negative controls behave as specified.")


def main():
    failures = []
    checks = 0

    for runner, label in ((local_runner, "local"), (cloud_runner, "cloud")):
        # Every fixture directory the runner can build a prompt from, discovered
        # rather than listed: when a new eval lane lands, its prompts are covered
        # by this guard on day one. Before 2026-09-03 only three of nine were.
        suites = sorted(
            (os.path.basename(os.path.dirname(getattr(runner, name))), getattr(runner, name))
            for name in dir(runner)
            if name.endswith("FIXTURES_DIR")
        )
        for suite, directory in suites:
            check_cut_lines(suite, f"{label} {suite}", directory, failures)
            for fid in fixture_ids(directory):
                checks += 1
                if suite == "perspectives":
                    prompt = runner.build_escalation_prompt(fid)
                else:
                    prompt = runner.load_fixture(fid, directory)
                with open(os.path.join(directory, fid + ".md")) as f:
                    raw = f.read()
                leaks(f"{label} {suite}", fid, prompt, failures)
                check_headings(suite, f"{label} {fid}", prompt, raw, failures)

    titles = check_titles(failures)

    if failures:
        print(f"FAIL — {len(failures)} leaked prompt(s) of {checks} checked:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    print(
        f"OK — {checks} prompts checked across both runners; "
        "no answer-key markers, no hint comments, no reassurance/verdict text; "
        f"cut lines canonical and consistent; every heading declared; "
        f"{titles} fixture titles match the manifest."
    )


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        main()
