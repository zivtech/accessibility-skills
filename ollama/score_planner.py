#!/usr/bin/env python3
"""Score Ollama a11y-planner output against fixture rubrics.

Usage:
    python3 ollama/score_planner.py <response_json> <metadata_yaml>

Checks key sections and content quality per the planner evaluation criteria.
"""

import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from score_common import (  # noqa: E402
    PLANNER_SECTION_PASS_THRESHOLD,
    check_baseline_ids,
    fallback_keywords,
    load_baseline_manifest,
    strip_thinking,
)


def load_response(path: str) -> tuple[str, bool]:
    with open(path) as f:
        data = json.load(f)
    return strip_thinking(data.get("response", ""))


def load_rubric(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


SECTION_KEYWORDS = {
    "APG Dialog pattern reference with URL": [
        "w3.org/WAI/ARIA/apg", "apg/patterns/dialog", "APG", "Dialog pattern"
    ],
    "Focus trap plan (Tab, Shift+Tab behavior)": [
        "focus trap", "Tab", "Shift+Tab", "trap focus", "focus management"
    ],
    "Focus restoration plan": [
        "focus restoration", "return focus", "restore focus", "trigger button"
    ],
    "aria-modal=\"true\" and aria-labelledby": [
        "aria-modal", "aria-labelledby"
    ],
    "Form structure with fieldset/legend": [
        "fieldset", "legend"
    ],
    "aria-invalid for error states": [
        "aria-invalid"
    ],
    "aria-describedby linking input to error message": [
        "aria-describedby"
    ],
    "Keyboard interaction (Tab, Escape, Shift+Tab)": [
        "Escape", "keyboard", "Tab"
    ],
    "HTML structure stub": [
        "<dialog", "role=\"dialog\"", "role='dialog'", "<form", "html", "```"
    ],
    "Validation approach decision (real-time vs submit)": [
        "validation", "submit", "real-time", "on-submit", "onSubmit"
    ],
    "WCAG citations": [
        "WCAG", "2.1.1", "4.1.2", "4.1.3", "1.3.1"
    ],
    "Live region for validation messages": [
        "aria-live", "live region", "polite", "assertive"
    ],
    "Roving tabindex plan": [
        "roving tabindex", "roving", "tabindex"
    ],
    "Arrow key navigation": [
        "arrow key", "ArrowDown", "ArrowUp", "ArrowLeft", "ArrowRight"
    ],
    "APG pattern reference": [
        "APG", "w3.org/WAI/ARIA/apg", "ARIA Authoring Practices"
    ],
    "Grid/menu structure": [
        "grid", "menu", "toolbar", "listbox"
    ],
}


def score_planner(text: str, rubric: dict):
    fixture_id = rubric.get("fixture_id", "unknown")
    print(f"Fixture: {fixture_id}")
    print(f"Response length: {len(text)} chars")
    print()

    must_have = []
    expected = rubric.get("expected_findings", {})
    if isinstance(expected, dict):
        must_have = expected.get("must_have", [])
    elif isinstance(expected, list):
        for cat in expected:
            if isinstance(cat, dict) and cat.get("category") == "must_have":
                must_have = cat.get("items", [])

    if not must_have:
        criteria = rubric.get("key_evaluation_criteria", [])
        must_have = criteria if criteria else []

    text_lower = text.lower()
    found = 0
    total = 0

    print("Key sections:")
    for item in must_have:
        desc = item if isinstance(item, str) else item.get("description", str(item))
        total += 1

        rubric_keywords = rubric.get("scoring_keywords", {})
        keywords = rubric_keywords.get(desc) or SECTION_KEYWORDS.get(desc, [])
        if not keywords:
            keywords = fallback_keywords(desc)
            print(f"  WARN: fallback keywords for criterion: {desc[:60]}")

        hit = any(kw.lower() in text_lower for kw in keywords)
        marker = "+" if hit else "X"
        if hit:
            found += 1
        if not hit:
            print(f"  {marker} {desc[:80]}  (keywords: {keywords[:3]})")
        else:
            print(f"  {marker} {desc[:80]}")

    print()
    print(f"Score: {found}/{total}")

    wcag_count = len(re.findall(r"\d+\.\d+\.\d+", text))
    print(f"WCAG criterion numbers cited: {wcag_count}")

    has_html = bool(re.search(r"```(?:html|jsx|tsx)?[\s\S]*?```", text))
    print(f"HTML/JSX code stubs: {'YES' if has_html else 'NO'}")

    # ICT baseline test-ID fidelity (adoption plan Phase 3 step 11). Scans
    # every plan: fabricated IDs and out-of-scope citations force NEEDS
    # REVIEW regardless of gate score. Cross-baseline (documents) IDs in plan
    # prose are flagged for reading, not auto-failed — a plan may legitimately
    # name a documents ID while declaring the documents boundary.
    b508 = rubric.get("baseline_508") or {}
    declared = bool(b508.get("declared", False))
    bl = check_baseline_ids(
        text,
        load_baseline_manifest(),
        declared=declared,
        expected_ids=b508.get("expected_ids") or [],
    )
    baseline_violation = False
    if bl["cited"]:
        print(f"Baseline IDs cited: {len(bl['cited'])} "
              f"(valid web: {len(bl['valid'])})")
    for tok, hint in bl["fabricated"]:
        baseline_violation = True
        print(f"FABRICATION: baseline ID '{tok}' — {hint}")
    for tok in bl["cross_baseline"]:
        print(f"  ! cross-baseline ID '{tok}' (documents-only) — verify context by reading")
    if bl["undeclared"]:
        baseline_violation = True
        print("VIOLATION: baseline citation(s) outside declared 508 scope: "
              + ", ".join(bl["undeclared"]))
    for missing in bl["expected_missing"]:
        baseline_violation = True
        print(f"MUST MISS: expected baseline ID {missing} not cited")

    # Trap markers (fixture-declared, read-verified detectors): regexes that
    # match trap-TAKING language. The keyword gate is polarity-blind — a plan
    # can hit federal vocabulary while taking the bait — so any marker hit
    # forces NEEDS REVIEW regardless of gate score. Markers are detectors:
    # a human reads the hit before the row is used anywhere.
    trap_hits = []
    for marker in rubric.get("trap_markers") or []:
        if re.search(marker["pattern"], text, re.IGNORECASE):
            trap_hits.append(marker["name"])
            print(f"TRAP MARKER: {marker['name']} — read-verify before using this row")

    status = (
        "PASS"
        if found / max(total, 1) >= PLANNER_SECTION_PASS_THRESHOLD
        else "NEEDS REVIEW"
    )
    if baseline_violation or trap_hits:
        status = "NEEDS REVIEW"
    print(f"\nStatus: {status}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <response.json> <metadata.yaml>")
        sys.exit(1)

    text, truncated = load_response(sys.argv[1])
    if truncated:
        print("Response truncated mid-<think> block — not scoring")
        print("Status: INCOMPLETE — truncated response")
        sys.exit(0)
    rubric = load_rubric(sys.argv[2])
    score_planner(text, rubric)
