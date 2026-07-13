#!/usr/bin/env python3
"""Score Ollama perspective-audit output against fixture rubrics.

Usage:
    python3 ollama/score_perspective.py <response_json> <metadata_yaml>

Checks:
- Did the model produce the correct verdict (PASS/REVISE/BLOCK)?
- Did it only audit escalated perspectives (not LOW ones)?
- Did it find must_find / should_find issues?
- Did it include WCAG citations?
- Did it include ARRM role routing?
- Did it avoid false positives on CLEAN fixtures?
"""

import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from score_common import strip_thinking, detect_verdict, fallback_keywords, normalize_quotes, MUST_FIND_ABORT_THRESHOLD  # noqa: E402


PERSPECTIVE_NAMES = {
    "magnification_reflow": "Magnification",
    "environmental_contrast": "Contrast",
    "vestibular_motion": "Vestibular",
    "auditory_access": "Auditory",
    "keyboard_motor": "Keyboard",
    "screen_reader_semantic": "Screen Reader",
    "cognitive_neurodivergent": "Cognitive",
}


def load_response(path: str) -> tuple[str, bool]:
    with open(path) as f:
        data = json.load(f)
    return strip_thinking(data.get("response", ""))


def load_rubric(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def get_alarm_levels(rubric: dict) -> dict:
    return rubric.get("expected_alarm_levels", {})


def get_escalated(alarm_levels: dict) -> list[str]:
    return [name for name, level in alarm_levels.items() if level in ("MEDIUM", "HIGH")]


def get_low(alarm_levels: dict) -> list[str]:
    return [name for name, level in alarm_levels.items() if level == "LOW"]


def check_verdict(text: str) -> str:
    return detect_verdict(text, ["BLOCK", "REVISE", "PASS"])


def check_perspective_coverage(text: str, escalated: list[str]) -> dict:
    """Check if the model ran checklists for each escalated perspective."""
    results = {}
    text_lower = text.lower()
    for name in escalated:
        readable = PERSPECTIVE_NAMES.get(name, name).lower()
        alt_names = [
            name.replace("_", " "),
            readable,
            name.replace("_", "-"),
        ]
        if name == "vestibular_motion":
            alt_names.extend(["motion", "vestibular", "reduced-motion", "prefers-reduced-motion"])
        elif name == "screen_reader_semantic":
            alt_names.extend(["screen reader", "semantic", "aria", "at user"])
        elif name == "keyboard_motor":
            alt_names.extend(["keyboard", "motor", "focus"])
        elif name == "cognitive_neurodivergent":
            alt_names.extend(["cognitive", "neurodivergent", "reading level", "jargon"])
        elif name == "environmental_contrast":
            alt_names.extend(["contrast", "color", "environmental"])
        elif name == "magnification_reflow":
            alt_names.extend(["magnification", "reflow", "zoom", "resize"])
        elif name == "auditory_access":
            alt_names.extend(["auditory", "captions", "audio"])

        results[name] = any(alt.lower() in text_lower for alt in alt_names)
    return results


def check_low_perspective_leakage(text: str, low_perspectives: list[str]) -> list[str]:
    """Check if the model incorrectly ran full checklists for LOW perspectives.

    Looks for structured checklist output or finding blocks mentioning LOW perspectives.
    Simple mentions (e.g. listing them as LOW) are fine — only structured findings count.
    """
    leaks = []
    for name in low_perspectives:
        readable = PERSPECTIVE_NAMES.get(name, name)
        finding_pattern = rf"(?:Finding|Checklist|CRITICAL|MAJOR).*{re.escape(readable)}"
        if re.search(finding_pattern, text, re.IGNORECASE):
            leaks.append(name)
    return leaks


def normalize_findings(rubric: dict) -> tuple[list[dict], list[dict], list[dict]]:
    """Extract must_find, should_find, nice_to_find from either metadata format."""
    must = []
    should = []
    nice = []

    findings = rubric.get("expected_findings", [])

    if isinstance(findings, list):
        for cat in findings:
            if isinstance(cat, dict) and "category" in cat:
                items = cat.get("items", [])
                if cat["category"] == "must_find":
                    must.extend(items)
                elif cat["category"] == "should_find":
                    should.extend(items)
                elif cat["category"] == "nice_to_find":
                    nice.extend(items)
    elif isinstance(findings, dict):
        for key in ["must_find", "should_find", "nice_to_find"]:
            section = findings.get(key, [])
            if isinstance(section, dict):
                items = section.get("items", [])
            elif isinstance(section, list):
                items = section
            else:
                items = []
            if key == "must_find":
                must.extend(items)
            elif key == "should_find":
                should.extend(items)
            elif key == "nice_to_find":
                nice.extend(items)

    return must, should, nice


def check_finding(text: str, finding: dict) -> dict:
    description = finding.get("description", "")
    wcag = finding.get("wcag", finding.get("criterion", ""))

    keywords = extract_keywords(description, wcag)
    norm_text = normalize_quotes(text.lower())
    found = any(normalize_quotes(kw.lower()) in norm_text for kw in keywords)

    wcag_cited = False
    if wcag:
        wcag_numbers = re.findall(r"(\d+\.\d+\.\d+)", str(wcag))
        wcag_cited = any(num in text for num in wcag_numbers)

    return {
        "description": description,
        "found": found,
        "wcag_cited": wcag_cited,
        "keywords_checked": keywords,
    }


def extract_keywords(description: str, wcag: str = "") -> list[str]:
    desc_lower = description.lower()

    if "color" in desc_lower and ("sole" in desc_lower or "alone" in desc_lower or "only" in desc_lower):
        return ["color alone", "color only", "1.4.1", "use of color", "sole differentiator", "non-color"]
    if "focus" in desc_lower and "trap" in desc_lower:
        return ["focus trap", "focus management", "tab escapes", "focus not contained"]
    if "focus" in desc_lower and ("move" in desc_lower or "modal" in desc_lower):
        return ["focus", "modal", "focus order", "focus management"]
    if "aria-describedby" in desc_lower:
        return ["aria-describedby", "describedby"]
    if "htmlfor" in desc_lower or "label" in desc_lower and "mismatch" in desc_lower:
        return ["htmlFor", "label", "mismatch", "association", "1.3.1"]
    if "reduced-motion" in desc_lower or "prefers-reduced-motion" in desc_lower:
        return ["prefers-reduced-motion", "reduced-motion", "2.3.1", "motion"]
    if "confetti" in desc_lower:
        return ["confetti", "particle", "animation", "canvas"]
    if "progress" in desc_lower and "animation" in desc_lower:
        return ["progress", "transition", "animation"]
    if "bounce" in desc_lower or "icon" in desc_lower and "animation" in desc_lower:
        return ["bounce", "icon", "animation", "scale"]
    if "hover" in desc_lower and ("tooltip" in desc_lower or "only" in desc_lower):
        return ["hover", "tooltip", "hover-only", ":hover", "keyboard"]
    if "target" in desc_lower and "size" in desc_lower:
        return ["target size", "touch target", "2.5.8", "24x24", "10px"]
    if "jargon" in desc_lower or "abbreviation" in desc_lower:
        return ["jargon", "abbreviation", "acronym", "plain language", "3.1"]
    if "9px" in desc_lower or "font" in desc_lower and "size" in desc_lower:
        return ["font-size", "9px", "resize", "1.4.4", "reflow"]
    if "role" in desc_lower and "dialog" in desc_lower:
        return ["role=\"dialog\"", "role='dialog'", "dialog", "aria-modal"]
    if "close" in desc_lower and "label" in desc_lower:
        return ["close", "aria-label", "accessible name", "×"]
    if "escape" in desc_lower:
        return ["Escape", "Esc", "close", "dismiss"]
    if "error" in desc_lower and "summary" in desc_lower and "link" in desc_lower:
        return ["error summary", "link", "navigate", "jump"]
    if "error" in desc_lower and "summary" in desc_lower:
        return ["error summary", "aria-live", "role=\"alert\"", "announcement"]
    if "step" in desc_lower and "color" in desc_lower:
        return ["step", "color", "indicator", "1.4.1"]
    if "density" in desc_lower:
        return ["density", "column", "hide", "simplified"]
    if "row" in desc_lower and "selection" in desc_lower:
        return ["row", "selection", "aria-selected", "background"]

    return fallback_keywords(description)


def check_arrm_routing(text: str) -> bool:
    """Check if findings include ARRM role routing."""
    arrm_patterns = [
        r"Route\s*to:",
        r"Front[\-\s]*End\s*Dev",
        r"Visual\s*Design",
        r"UX\s*Design",
        r"Content\s*Author",
        r"ARRM",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in arrm_patterns)


def check_false_positives(text: str, declared_verdict: str) -> dict:
    finding_patterns = [
        r"(?:Finding|Issue)\s*#?\d+\s*[:.]",
        r"^\s*\d+\.\s+\*\*(?:CRITICAL|SERIOUS|MAJOR|MODERATE)",
        r"Severity:\s*(?:CRITICAL|SERIOUS|MAJOR)",
        r"\|\s*(?:CRITICAL|SERIOUS|MAJOR)\s*\|",
    ]
    count = 0
    for pattern in finding_patterns:
        count += len(re.findall(pattern, text, re.MULTILINE | re.IGNORECASE))

    wrong_verdict = declared_verdict in ("BLOCK", "REVISE")
    return {"structured_findings": count, "wrong_verdict": wrong_verdict}


def score(response_path: str, rubric_path: str):
    text, truncated = load_response(response_path)
    if truncated:
        print("Response truncated mid-<think> block — not scoring")
        print("Status: INCOMPLETE — truncated response")
        return
    rubric = load_rubric(rubric_path)
    difficulty = rubric.get("difficulty", "unknown")
    fixture_id = rubric.get("fixture_id", "unknown")

    print(f"Response length: {len(text)} chars")
    print(f"Fixture: {fixture_id}")
    print(f"Difficulty: {difficulty}")
    print()

    alarm_levels = get_alarm_levels(rubric)
    escalated = get_escalated(alarm_levels)
    low = get_low(alarm_levels)

    print(f"Escalated perspectives: {', '.join(escalated) or 'none'}")
    print(f"LOW perspectives: {', '.join(low) or 'none'}")
    print()

    if difficulty == "CLEAN":
        verdict = check_verdict(text)
        acceptable_verdicts = ["PASS"]
        alt = rubric.get("alternate_verdicts", [])
        if alt:
            acceptable_verdicts.extend([v.upper() for v in alt])
        correct = verdict in acceptable_verdicts
        expected_str = "PASS" + (f" or {'/'.join(alt)}" if alt else "")
        print(f"Verdict: {verdict} (expected: {expected_str})")
        print(f"Verdict correct: {'YES' if correct else f'NO — should be {expected_str}'}")
        print()

        fp = check_false_positives(text, verdict)
        print(f"False positive signals:")
        print(f"  Structured findings: {fp['structured_findings']}")
        print(f"  Wrong verdict: {fp['wrong_verdict']}")
        print()

        passed = correct and (not fp["wrong_verdict"] or verdict in [v.upper() for v in alt])
        status = "PASS" if passed else "FAIL"
        if fp["structured_findings"] > 0 and passed:
            status = "WARN — correct verdict but raised findings"
        print(f"Status: {status}")
        return

    # HAS-BUGS / ADVERSARIAL
    coverage = check_perspective_coverage(text, escalated)
    covered = sum(1 for v in coverage.values() if v)
    print(f"Perspective coverage: {covered}/{len(escalated)}")
    for name, found in coverage.items():
        marker = "+" if found else "X"
        print(f"  {marker} {PERSPECTIVE_NAMES.get(name, name)}")
    print()

    leaks = check_low_perspective_leakage(text, low)
    if leaks:
        print(f"LOW perspective leakage: {', '.join(leaks)} (should not audit these)")
    else:
        print(f"LOW perspective leakage: none (correct)")
    print()

    must, should, nice = normalize_findings(rubric)

    if must:
        must_results = [check_finding(text, f) for f in must]
        found_count = sum(1 for r in must_results if r["found"])
        print(f"Must-find issues: {found_count}/{len(must)}")
        for r in must_results:
            marker = "+" if r["found"] else "X"
            wcag_marker = "W" if r["wcag_cited"] else "-"
            kw_suffix = f"  (keywords: {r['keywords_checked']})" if not r["found"] else ""
            print(f"  {marker} [{wcag_marker}] {r['description'][:80]}{kw_suffix}")
        print()
    else:
        must_results = []
        print("Must-find issues: 0 expected")
        print()

    if should:
        should_results = [check_finding(text, f) for f in should]
        found_count = sum(1 for r in should_results if r["found"])
        print(f"Should-find issues: {found_count}/{len(should)}")
        for r in should_results:
            marker = "+" if r["found"] else "X"
            wcag_marker = "W" if r["wcag_cited"] else "-"
            kw_suffix = f"  (keywords: {r['keywords_checked']})" if not r["found"] else ""
            print(f"  {marker} [{wcag_marker}] {r['description'][:80]}{kw_suffix}")
        print()
    else:
        should_results = []

    if nice:
        nice_results = [check_finding(text, f) for f in nice]
        found_count = sum(1 for r in nice_results if r["found"])
        print(f"Nice-to-find issues: {found_count}/{len(nice)}")
        for r in nice_results:
            marker = "+" if r["found"] else "-"
            print(f"  {marker} {r['description'][:80]}")
        print()

    has_arrm = check_arrm_routing(text)
    print(f"ARRM role routing: {'YES' if has_arrm else 'NO'}")

    verdict = check_verdict(text)
    expected = rubric.get("expected_verdict", "REVISE")
    # Perspective-audit uses PASS/REVISE/BLOCK ladder (different from critic's ACCEPT/REVISE/REJECT).
    # BLOCK is valid when CRITICAL findings are present, even if metadata says REVISE.
    verdict_ok = verdict == expected or (verdict == "BLOCK" and expected == "REVISE")
    print(f"Verdict: {verdict} (expected: {expected}{', BLOCK also valid' if verdict == 'BLOCK' and expected == 'REVISE' else ''})")
    print(f"Verdict acceptable: {'YES' if verdict_ok else 'NO'}")
    print()

    must_score = sum(1 for r in must_results if r["found"]) / max(len(must_results), 1)
    print(f"Must-find detection rate: {must_score:.0%}")
    print(f"Abort threshold: {MUST_FIND_ABORT_THRESHOLD:.0%} (escalation gate — see score_common.py)")
    print(f"Status: {'PASS' if must_score >= MUST_FIND_ABORT_THRESHOLD else 'FAIL'}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <response.json> <metadata.yaml>")
        sys.exit(1)
    score(sys.argv[1], sys.argv[2])
