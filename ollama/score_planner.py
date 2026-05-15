#!/usr/bin/env python3
"""Score Ollama a11y-planner output against fixture rubrics.

Usage:
    python3 ollama/score_planner.py <response_json> <metadata_yaml>

Checks key sections and content quality per the planner evaluation criteria.
"""

import json
import re
import sys

import yaml


def strip_thinking(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def load_response(path: str) -> str:
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

        keywords = SECTION_KEYWORDS.get(desc, [])
        if not keywords:
            words = desc.lower().split()[:4]
            keywords = [w.strip(".,;:()") for w in words if len(w) > 3]

        hit = any(kw.lower() in text_lower for kw in keywords)
        marker = "+" if hit else "X"
        if hit:
            found += 1
        print(f"  {marker} {desc[:80]}")

    print()
    print(f"Score: {found}/{total}")

    wcag_count = len(re.findall(r"\d+\.\d+\.\d+", text))
    print(f"WCAG criterion numbers cited: {wcag_count}")

    has_html = bool(re.search(r"```(?:html|jsx|tsx)?[\s\S]*?```", text))
    print(f"HTML/JSX code stubs: {'YES' if has_html else 'NO'}")

    print(f"\nStatus: {'PASS' if found / max(total, 1) >= 0.7 else 'NEEDS REVIEW'}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <response.json> <metadata.yaml>")
        sys.exit(1)

    text = load_response(sys.argv[1])
    rubric = load_rubric(sys.argv[2])
    score_planner(text, rubric)
