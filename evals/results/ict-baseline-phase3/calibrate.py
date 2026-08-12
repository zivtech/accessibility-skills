#!/usr/bin/env python3
"""Synthetic calibration for the ICT baseline Phase 3 instruments (steps 10+11)
— run BEFORE any model rows, per house practice.

Generates deterministic synthetic responses, scores them with the real
scorers (ollama/score_planner.py, ollama/score_bugreport.py), asserts the
expected verdicts, and regression-checks the extended scorers against every
committed response file of the two touched lanes (statuses must not change).

Reproduce:  python3 evals/results/ict-baseline-phase3/calibrate.py
Outputs:    synthetic-*.json + score-*.txt in this directory, summary on stdout.
"""

import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PLANNER_META = os.path.join(
    REPO, "evals", "suites", "a11y-planner", "fixtures",
    "test-federal-agency-audit.metadata.yaml",
)
BUGREPORT_META = os.path.join(
    REPO, "evals", "suites", "bug-reporting", "fixtures",
    "axe-button-name-federal.metadata.yaml",
)
IMAGE_ALT_META = os.path.join(
    REPO, "evals", "suites", "bug-reporting", "fixtures",
    "axe-image-alt-single.metadata.yaml",
)

sys.path.insert(0, os.path.join(REPO, "ollama"))
from score_bugreport import expected_id_hexes  # noqa: E402

# ── Synthetic planner responses ──────────────────────────────────────────────

PLANNER_PROTOCOL_SHAPED = """# Federal Grant Program Accessibility Evaluation Plan

## Scope & Context
This is a declared Revised Section 508 engagement. The conformance floor
declaration is a named artifact of this plan: the evaluation's conformance
target is Revised Section 508, which incorporates WCAG 2.0 Level A/AA, plus
the applicable non-WCAG provisions — E205.2/E205.3 scope provisions deciding
which intranet content must conform (public-facing content and the nine
agency official communication categories, resolved with legal by category),
503.4/503.4.1/503.4.2 caption and audio-description user-control placement,
and Chapter 3 functional performance criteria via E204. The vendor's claim
that WCAG 2.2 replaced the older standard is incorrect: Section 508 does not
incorporate WCAG 2.2. We report conformance against the floor and keep
WCAG 2.2 AA as a separately-reported recommendation layer — the
magnification/reflow complaints (WCAG 1.4.10 Reflow, a 2.1-era criterion)
are filed there as recommendations, never as Section 508 violations.

## Testing Strategy
The required-tests question: our process is designed to cover 22 of the 62
web baseline tests with decisive machine evidence, 26 partially (machine
substrate, human decision), and 13 not at all — the ICT Testing Baseline is
the federal test-completeness standard behind that list, and the not-covered
tests (for example 9.A-Flashes and 17.E-ADPrerecorded) are assigned to
manual/AT sessions in the schedule. 24.A-Parsing always passes per the
WCAG 2.0 errata: 4.1.1 is formally in the Section 508 basis, but no testing
is planned for it — the web lead's HTML-checker output is triaged into the
criteria markup errors actually break (name/role/state under 5.A-ControlName,
5.B-ControlRole, 5.C-ControlState). The 20-minute timeout is evaluated under
WCAG 2.2.1 Timing Adjustable at the floor. Player control placement is
checked for caption and description controls at the same menu level as
volume (503.4.1, 503.4.2).

## Content Accessibility
The 200 PDFs sit outside the automated web pass — that boundary is stated
plainly in the report. They get a documents-appropriate method: tagged PDF /
PDF/UA checking on a sample, with the scanned files called out as image-only.
The shared login is third-party: best-effort testing with documented limits.

## Visual Accessibility
Contrast (WCAG 1.4.3) at the floor across site, portal, and PDFs.

## Semantic Structure / Interaction Pattern Design / Focus Management / State Communication
Portal form steps: error identification (WCAG 3.3.1, 3.3.3), name/role/value
(WCAG 4.1.2) on the upload widget and player controls, focus order
(WCAG 2.4.3) across route changes.

## Implementation Tasks
Procurement's approval question, answered directly: no — our approach carries
no certification and no official stamp. Alignment recognition is an external
review of a test process; Trusted Tester certification is a DHS credential
held by people, and we claim neither. The written report is evidence that
feeds an Accessibility Conformance Report (VPAT) authored downstream; the
report itself is not one, and that is what procurement can attach.

```html
<button aria-label="Remove document">…</button>
```
"""

PLANNER_BASELINE_SHAPED = """# Accessibility Test Plan

We will test the website, portal, videos, PDFs, and intranet against
WCAG 2.2 AA, the current standard, as your vendor advised. Our automated
scanner will crawl all five surfaces including the 200 PDFs and the intranet
in one pass. Every markup error the HTML checker flags will be listed in the
final report as a violation for the contractor to fix. Our testing process is
government-approved, and on completion we will provide a compliance
certificate you can attach to the contract file, confirming the program
passes the required test 7.D-ColorContrast and the rest of the official
checklist. Timeline: two weeks of scanning, report in week three.
"""

PLANNER_MIXED_FABRICATING = PLANNER_PROTOCOL_SHAPED.replace(
    "for example 9.A-Flashes and 17.E-ADPrerecorded",
    "for example 9.A-Flashes, 17.E-ADPrerecorded, and 5.E-ControlLabel",
)

# Fluent all-four-baits plan (adapted from the 2026-08-12 critic gate's
# reproduction, which measured 8/11 PASS on the keyword gate before trap
# markers existed). No fabricated IDs, so the fidelity override never fires —
# only the trap_markers can catch it. Its measured gate score is the honest
# ceiling for trap-taking plans and is recorded in the README.
PLANNER_TRAP_TAKER = """# Accessibility Evaluation Plan — Office of Rural Grants Administration

## Scope & Context
The engagement is a Section 508 evaluation of five surfaces. Your vendor is
correct that the standards landscape moved on: WCAG 2.0 is the version the
original rule referenced, but WCAG 2.2 AA is the current standard and it
supersedes the earlier versions, so we will evaluate and report conformance
against WCAG 2.2 AA throughout. That keeps the agency ahead of the next
refresh and gives the contracting officer a single number.

Our practice follows the ICT Testing Baseline, the federal test list
procurement is asking about, and our process is certified against it — we can
supply the certificate for the contract file.

## Semantic Structure
We will review landmark structure, heading hierarchy, and list semantics on
the public-facing website and the intranet in the same crawl; both run on the
same templates, so one pass covers the boundary between them.

## Interaction Pattern Design
Custom player controls, multi-step forms, and the upload widget get pattern
review against the ARIA Authoring Practices.

## Focus Management
Tab order, focus visibility, and focus restoration across route changes.

## State Communication
Error identification and status messaging on the application steps. Lower-
impact items will be listed as advisory notes.

## Visual Accessibility
Contrast, reflow at 400%, and text spacing across all five surfaces.

## Content Accessibility
Alt text, link purpose, and plain-language review of eligibility content.

## Testing Strategy
Automated scanning covers the whole estate in one pass: the 120-page website,
the 25 portal screens, the 200 PDFs, and the intranet. We run the same
crawler over the PDF library so the documents come back in the same
spreadsheet as the web results. The web lead's HTML checker output is welcome
— every markup error it reports will be carried into the final report as a
WCAG 4.1.1 Parsing violation for the contractor to remediate.

## Implementation Tasks
The deliverable is a completed VPAT the agency can attach to the contract
file, plus a remediation backlog for the contractor.
"""

PLANNER_CROSS_BASELINE_PROSE = PLANNER_PROTOCOL_SHAPED.replace(
    "The shared login is third-party: best-effort testing with documented limits.",
    "The shared login is third-party: best-effort testing with documented limits. "
    "For orientation: document-side IDs such as 11.A-DocumentTitled belong to the "
    "Electronic Documents baseline, which is out of this engagement's measured scope.",
)

UNDECLARED_PLANNER_META = """fixture_id: synthetic-undeclared-control
dehinted: false
expected_findings:
  must_have:
    - Mentions a focus trap
scoring_keywords:
  "Mentions a focus trap":
    - "focus trap"
"""

PLANNER_UNDECLARED_CREEP = """# Modal Plan
The dialog needs a focus trap (WCAG 2.1.2). This also maps to baseline test
1.A-KeyboardAccess for the federal checklist.
"""

# ── Synthetic bug reports ────────────────────────────────────────────────────


def federal_report(baseline_rows, include_expected_labels=True):
    spec = {
        "prefix": "A11Y",
        "screen_type": "desktop",
        "page_path": "/application/step-2",
        "rule_id": "button-name",
        "instances": [{"selector": "ul.uploaded-docs > li:nth-child(3) button.doc-remove"}],
    }
    (_, _, inst_hex), (_, _, pat_hex) = expected_id_hexes(spec)
    rows = "\n".join(baseline_rows)
    return f"""## Accessibility Issue: Remove-document button missing accessible name (WCAG 4.1.2)

**URL:** https://apply.ruralgrants.example.gov/application/step-2
**XPath:** //ul[@class="uploaded-docs"]/li[3]//button[@class="doc-remove"]
**Full DOM path:** /html/body/main/form/section[2]/ul[@class="uploaded-docs"]/li[3]/button[@class="doc-remove"]
**WCAG SC:** 4.1.2 Name, Role, Value (Level A)
**Rule:** button-name (axe-core 4.9.1)
**Severity:** Critical
**Frequency:** 1 instance on this page (selector ul.uploaded-docs > li:nth-child(3) button.doc-remove)
{rows}
**Instance ID:** A11Y-{inst_hex}
**Pattern ID:** A11Y-{pat_hex}
**Screen reader:** N/A — automated scan, no assistive technology in the run

### HTML Snippet
```html
<button class="doc-remove"><svg aria-hidden="true" viewBox="0 0 16 16"><path d="M4 4l8 8m0-8l-8 8"/></svg></button>
```

### Steps to Reproduce
1. Sign in and open https://apply.ruralgrants.example.gov/application/step-2
2. Upload three documents and inspect the third row's remove control

### Expected Behaviour
The remove button exposes an accessible name such as "Remove document".

### Actual Behaviour
The button contains only an aria-hidden SVG; screen readers announce "button"
with no name.

### Suggested Fix
Add `aria-label="Remove document"` to the button.
"""


IMAGE_ALT_CREEP_REPORT = None  # built in main() (needs that fixture's hexes)


def build_image_alt_report(extra_rows=""):
    spec = {
        "prefix": "A11Y",
        "screen_type": "desktop",
        "page_path": "/articles/spring-garden-guide",
        "rule_id": "image-alt",
        "instances": [{"selector": "article.feature-story > img.hero"}],
    }
    (_, _, inst_hex), (_, _, pat_hex) = expected_id_hexes(spec)
    return f"""## Accessibility Issue: Feature image missing alt text (WCAG 1.1.1)

**URL:** https://news.example.com/articles/spring-garden-guide
**XPath:** //article[contains(@class,"feature-story")]/img[@class="hero"]
**Full DOM path:** /html/body/main/article[@class="feature-story"]/img[@class="hero"]
**WCAG SC:** 1.1.1 Non-text Content (Level A)
**Rule:** image-alt (axe-core 4.9.1)
**Severity:** Critical
**Frequency:** 1 instance on this page (selector article.feature-story > img.hero)
**Testing Environment:** Chrome 126, macOS 14, viewport 1280 × 800
{extra_rows}**Instance ID:** A11Y-{inst_hex}
**Pattern ID:** A11Y-{pat_hex}
**Screen reader:** N/A — automated scan

### HTML Snippet
```html
<img src="/img/hero-2481.jpg" class="hero">
```

### Steps to Reproduce
1. Open https://news.example.com/articles/spring-garden-guide

### Expected Behaviour
The hero image has a text alternative.

### Actual Behaviour
No alt attribute; screen readers announce the filename hero-2481.jpg.
"""


# ── Harness ──────────────────────────────────────────────────────────────────


def write_response(name, text):
    path = os.path.join(HERE, f"synthetic-{name}.json")
    with open(path, "w") as f:
        json.dump({"response": text, "_synthetic": True}, f, indent=1)
    return path


def score(scorer, response_path, meta_path, name):
    proc = subprocess.run(
        [sys.executable, os.path.join(REPO, "ollama", scorer), response_path, meta_path],
        capture_output=True, text=True,
    )
    out = proc.stdout + proc.stderr
    with open(os.path.join(HERE, f"score-{name}.txt"), "w") as f:
        f.write(out)
    m = re.search(r"^Status: (.+)$", out, re.MULTILINE)
    return (m.group(1).strip() if m else "NO STATUS"), out


def main():
    results, failures = [], []

    def expect(name, got, want_prefix, detail=""):
        ok = got.startswith(want_prefix)
        results.append((name, got, want_prefix, ok, detail))
        if not ok:
            failures.append(name)

    # ── planner instrument ──
    undeclared_meta = os.path.join(HERE, "synthetic-undeclared-control.metadata.yaml")
    with open(undeclared_meta, "w") as f:
        f.write(UNDECLARED_PLANNER_META)

    cases = [
        ("planner-protocol-shaped", PLANNER_PROTOCOL_SHAPED, PLANNER_META,
         "PASS", "all 11 musts + valid IDs only"),
        ("planner-baseline-shaped", PLANNER_BASELINE_SHAPED, PLANNER_META,
         "NEEDS REVIEW", "vendor-agreeing plan, fabricated 7.D-ColorContrast"),
        ("planner-mixed-fabricating", PLANNER_MIXED_FABRICATING, PLANNER_META,
         "NEEDS REVIEW", "gate-saturating text + fabricated 5.E-ControlLabel — override proof"),
        ("planner-undeclared-creep", PLANNER_UNDECLARED_CREEP, undeclared_meta,
         "NEEDS REVIEW", "valid ID cited on a non-508 fixture — creep tripwire"),
        ("planner-trap-taker", PLANNER_TRAP_TAKER, PLANNER_META,
         "NEEDS REVIEW", "fluent all-four-baits plan — trap markers must catch what the polarity-blind gate cannot"),
        ("planner-cross-baseline-prose", PLANNER_CROSS_BASELINE_PROSE, PLANNER_META,
         "PASS", "documents ID in boundary-declaring prose — flagged for reading, never auto-failed"),
    ]
    for name, text, meta, want, detail in cases:
        path = write_response(name, text)
        got, out = score("score_planner.py", path, meta, name)
        gate = re.search(r"^Score: \d+/\d+$", out, re.MULTILINE)
        if name == "planner-protocol-shaped":
            detail += f" (gate {gate.group(0)[7:] if gate else '?'})"
            if not re.search(r"^Score: 11/11$", out, re.MULTILINE):
                failures.append(name + ":gate")
            if "TRAP MARKER" in out:
                failures.append(name + ":false-trap-marker")
        if name == "planner-baseline-shaped" and "FABRICATION: baseline ID '7.D-ColorContrast'" not in out:
            failures.append(name + ":fabrication-line")
        if name == "planner-mixed-fabricating" and "FABRICATION: baseline ID '5.E-ControlLabel'" not in out:
            failures.append(name + ":fabrication-line")
        if name == "planner-undeclared-creep" and "VIOLATION: baseline citation(s) outside declared 508 scope" not in out:
            failures.append(name + ":violation-line")
        if name == "planner-trap-taker":
            markers = re.findall(r"^TRAP MARKER: (\S+)", out, re.MULTILINE)
            detail += f" (gate {gate.group(0)[7:] if gate else '?'}, markers: {len(markers)})"
            if len(markers) < 3:
                failures.append(name + ":too-few-markers")
        if name == "planner-cross-baseline-prose":
            if "cross-baseline ID '11.A-DocumentTitled'" not in out:
                failures.append(name + ":missing-cross-baseline-line")
            if "TRAP MARKER" in out:
                failures.append(name + ":false-trap-marker")
        expect(name, got, want, detail)

    # ── bugreport instrument ──
    br_cases = [
        ("bugreport-correct-federal",
         federal_report(["**Baseline test:** 5.A-ControlName"]),
         BUGREPORT_META, "PASS", "correct filing"),
        ("bugreport-fabricated-id",
         federal_report(["**Baseline test:** 5.E-ControlLabel"]),
         BUGREPORT_META, "FAIL", "grammar-shaped invention"),
        ("bugreport-missing-row",
         federal_report([]),
         BUGREPORT_META, "FAIL", "declared scope, no Baseline test row"),
        ("bugreport-24a-filed",
         federal_report(["**Baseline test:** 5.A-ControlName", "**Baseline test:** 24.A-Parsing"]),
         BUGREPORT_META, "FAIL", "24.A filed as a finding"),
        ("bugreport-documents-id",
         federal_report(["**Baseline test:** 11.A-DocumentTitled"]),
         BUGREPORT_META, "FAIL", "documents-baseline ID on a web finding"),
        ("bugreport-undeclared-creep",
         build_image_alt_report("**Baseline test:** 6.A-MeaningfulImage\n"),
         IMAGE_ALT_META, "FAIL", "baseline citation on a non-508 fixture"),
        ("bugreport-clean-non508",
         build_image_alt_report(),
         IMAGE_ALT_META, "PASS", "extension inert on undeclared fixture with no citations"),
        ("bugreport-wrong-but-valid-neighbor",
         federal_report(["**Baseline test:** 10.A-FormName"])
         + "\nCandidate tests considered: 5.A-ControlName, 5.B-ControlRole.\n",
         BUGREPORT_META, "FAIL", "wrong filing with the right ID quoted in prose — the FILED value is compared, not mere mention"),
        ("bugreport-json-filing",
         federal_report([])
         + '\n```json\n{"baseline_test": "5.A-ControlName"}\n```\n',
         BUGREPORT_META, "PASS", "JSON-shaped filing recognized as a filed row"),
        ("bugreport-stale-ledger-id",
         federal_report(["**Baseline test:** 21.B-AutoUpdate"]),
         BUGREPORT_META, "FAIL", "upstream stale string filed — ledger hint expected"),
    ]
    for name, text, meta, want, detail in br_cases:
        path = write_response(name, text)
        got, out = score("score_bugreport.py", path, meta, name)
        if name == "bugreport-wrong-but-valid-neighbor" and "not FILED" not in out:
            failures.append(name + ":missing-filed-check")
        if name == "bugreport-json-filing" and "filed rows 1" not in out:
            failures.append(name + ":json-row-not-detected")
        if name == "bugreport-stale-ledger-id" and "21.C-AutoUpdate" not in out:
            failures.append(name + ":missing-ledger-hint")
        expect(name, got, want, detail)

    # ── regression: the extension must be INERT on every committed response
    # of the two touched lanes. Pre-federal outputs contain no baseline
    # citations, so the new checks must emit zero baseline findings on all of
    # them — a property that holds at any HEAD (committed score files use
    # per-lane naming conventions, so status-diffing against them is not
    # reproducible; the one-time old-vs-new status diff for the landing
    # commit is recorded in this directory's README instead).
    print("\n== Regression (committed responses: baseline checks must be inert) ==")
    regressions = 0
    scanned = 0
    baseline_line = re.compile(
        r"FABRICATION: baseline|VIOLATION: baseline|baseline citation\(s\) outside|baseline ID '"
    )
    for resp in sorted(
        glob.glob(os.path.join(REPO, "evals", "results", "**", "ollama-bugreport-*-response.json"), recursive=True)
        + glob.glob(os.path.join(REPO, "evals", "results", "**", "ollama-planner-*-response.json"), recursive=True)
    ):
        base = os.path.basename(resp).replace("-response.json", "")
        if base.startswith("synthetic-"):
            continue
        scorer = "score_bugreport.py" if "bugreport" in base else "score_planner.py"
        fixture = re.sub(r"^ollama-(bugreport|planner(-federal)?)-", "", base)
        fixture = re.sub(r"-(qwen[\w.:-]+|laguna[\w.:-]+|gemma[\w.:-]+|gpt[\w.:-]+|ornith[\w.:-]+)$", "", fixture)
        suite_dir = "bug-reporting" if "bugreport" in base else "a11y-planner"
        meta = os.path.join(REPO, "evals", "suites", suite_dir, "fixtures", f"{fixture}.metadata.yaml")
        if not os.path.exists(meta):
            print(f"  SKIP (no metadata resolved): {base}")
            continue
        proc = subprocess.run(
            [sys.executable, os.path.join(REPO, "ollama", scorer), resp, meta],
            capture_output=True, text=True,
        )
        scanned += 1
        hits = [l for l in proc.stdout.splitlines() if baseline_line.search(l)]
        if hits:
            regressions += 1
            print(f"  NOT INERT {base}: {hits[0]}")
    print(f"  {scanned} committed responses rescored; baseline checks inert on {scanned - regressions}")
    if regressions:
        failures.append("regression-inertness")

    # ── summary ──
    print("\n== Calibration summary ==")
    for name, got, want, ok, detail in results:
        print(f"  {'OK ' if ok else 'FAIL'} {name}: {got} (expected {want}) — {detail}")
    print(f"\n{'CALIBRATION CLEAN' if not failures else 'CALIBRATION FAILURES: ' + ', '.join(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
