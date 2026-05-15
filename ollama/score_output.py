#!/usr/bin/env python3
"""Score Ollama a11y-critic output against fixture rubrics.

Usage:
    python3 ollama/score_output.py <response_json> <metadata_yaml>

Checks:
- Did the model find each must_find issue?
- Did the model find each should_find issue?
- Did the model follow phase structure?
- What verdict did it produce?
"""

import json
import sys
import re
import yaml


def strip_thinking(text: str) -> str:
    """Strip <think>...</think> blocks emitted by reasoning models (e.g., DeepSeek-R1).

    Scoring should only evaluate the final output, not internal chain-of-thought.
    """
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def load_response(path: str) -> str:
    with open(path) as f:
        data = json.load(f)
    return strip_thinking(data.get("response", ""))


def load_rubric(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def check_phases(text: str) -> dict:
    phases = {}
    for i in range(11):
        pattern = rf"Phase\s+{i}\b"
        phases[f"phase_{i}"] = bool(re.search(pattern, text, re.IGNORECASE))
    return phases


def check_verdict(text: str) -> str:
    # First check for explicit verdict declarations (most reliable)
    verdict_pattern = re.search(
        r"(?:#\s*)?(?:\*\*)?Verdict(?:\*\*)?[:\s]+\*?\*?(REJECT|REVISE|ACCEPT-WITH-RESERVATIONS|ACCEPT)\b",
        text,
        re.IGNORECASE,
    )
    if verdict_pattern:
        return verdict_pattern.group(1).upper()
    # Fallback: look for verdict keywords, checking most specific first
    for verdict in ["ACCEPT-WITH-RESERVATIONS", "REJECT", "REVISE", "ACCEPT"]:
        if verdict in text.upper():
            return verdict
    return "NONE"


def check_finding(text: str, finding: dict) -> dict:
    description = finding.get("description", "")
    wcag = finding.get("wcag", "")

    keywords = []
    if "aria-describedby" in description.lower():
        keywords = ["aria-describedby", "describedby"]
    elif "live region" in description.lower() or "announced" in description.lower():
        keywords = ["aria-live", "role=\"alert\"", "role='alert'", "live region", "status message", "4.1.3"]
    elif "link" in description.lower() and "field" in description.lower():
        keywords = ["link", "jump", "anchor", "summary"]
    elif "arrow" in description.lower() and "nav" in description.lower():
        keywords = ["arrow", "roving", "tabindex", "keyboard navigation"]
    elif "role" in description.lower():
        role_match = re.search(r'role[="\s]+(\w+)', description.lower())
        if role_match:
            keywords = [role_match.group(1), "role"]
    elif "fieldset" in description.lower() or "group" in description.lower():
        keywords = ["fieldset", "group", "legend"]
    else:
        keywords = description.lower().split()[:3]

    found = any(kw.lower() in text.lower() for kw in keywords)

    wcag_cited = False
    if wcag:
        wcag_number = re.search(r"(\d+\.\d+\.\d+)", wcag)
        if wcag_number:
            wcag_cited = wcag_number.group(1) in text

    return {
        "description": description,
        "found": found,
        "wcag_cited": wcag_cited,
        "keywords_checked": keywords,
    }


def count_false_positives(text: str) -> dict:
    """For CLEAN fixtures: check if the model raised actual accessibility findings.

    Uses structured signals (numbered findings, severity-tagged items) rather than
    keyword matching, which false-fires on section headers and positive statements.
    """
    finding_patterns = [
        r"(?:Finding|Issue)\s*#?\d+\s*[:.]",
        r"^\s*\d+\.\s+\*\*(?:CRITICAL|SERIOUS|MAJOR|MODERATE)",
        r"Severity:\s*(?:CRITICAL|SERIOUS|MAJOR)",
        r"\|\s*(?:CRITICAL|SERIOUS|MAJOR)\s*\|",
    ]
    finding_count = 0
    for pattern in finding_patterns:
        finding_count += len(re.findall(pattern, text, re.MULTILINE | re.IGNORECASE))

    # Check if the declared verdict (not mentions in hypothetical sections) is REJECT/REVISE
    declared = check_verdict(text)
    reject_revise = declared in ("REJECT", "REVISE")

    return {
        "structured_findings": finding_count,
        "wrong_verdict": reject_revise,
    }


def score(response_path: str, rubric_path: str):
    text = load_response(response_path)
    rubric = load_rubric(rubric_path)
    difficulty = rubric.get("difficulty", "unknown")

    print(f"Response length: {len(text)} chars")
    print(f"Fixture: {rubric.get('fixture_id', 'unknown')}")
    print(f"Difficulty: {difficulty}")
    print()

    phases = check_phases(text)
    phase_count = sum(1 for v in phases.values() if v)
    print(f"Phases found: {phase_count}/11")
    for phase, found in phases.items():
        marker = "+" if found else "-"
        print(f"  {marker} {phase}")
    print()

    verdict = check_verdict(text)

    if difficulty == "CLEAN":
        expected_verdict = "ACCEPT"
        print(f"Verdict: {verdict} (expected: ACCEPT or ACCEPT-WITH-RESERVATIONS)")
        correct_verdict = verdict in ("ACCEPT", "ACCEPT-WITH-RESERVATIONS")
        print(f"Verdict correct: {'YES' if correct_verdict else 'NO — FALSE ALARM'}")
        print()

        fp = count_false_positives(text)
        print(f"False positive signals:")
        print(f"  Structured findings (numbered/tagged): {fp['structured_findings']}")
        print(f"  Wrong verdict (REJECT/REVISE): {fp['wrong_verdict']}")
        print()

        passed = correct_verdict and not fp["wrong_verdict"]
        status = "PASS" if passed else "FAIL"
        if fp["structured_findings"] > 0 and passed:
            status = "WARN — correct verdict but raised findings (review manually)"
        print(f"Status: {status}")
    else:
        expected = rubric.get("notes", "")
        expected_verdict = "REVISE" if "REVISE" in expected else "unknown"
        print(f"Verdict: {verdict} (expected: {expected_verdict})")
        print()

        must_find = []
        should_find = []
        for cat in rubric.get("expected_findings", []):
            category = cat.get("category", "")
            for item in cat.get("items", []):
                result = check_finding(text, item)
                result["category"] = category
                if category == "must_find":
                    must_find.append(result)
                elif category == "should_find":
                    should_find.append(result)

        print(f"Must-find issues: {sum(1 for r in must_find if r['found'])}/{len(must_find)}")
        for r in must_find:
            marker = "+" if r["found"] else "X"
            wcag_marker = "W" if r["wcag_cited"] else "-"
            print(f"  {marker} [{wcag_marker}] {r['description'][:80]}")
        print()

        print(f"Should-find issues: {sum(1 for r in should_find if r['found'])}/{len(should_find)}")
        for r in should_find:
            marker = "+" if r["found"] else "X"
            wcag_marker = "W" if r["wcag_cited"] else "-"
            print(f"  {marker} [{wcag_marker}] {r['description'][:80]}")
        print()

        must_score = sum(1 for r in must_find if r["found"]) / max(len(must_find), 1)
        print(f"Must-find detection rate: {must_score:.0%}")
        print(f"Abort threshold: 40%")
        print(f"Status: {'PASS' if must_score >= 0.4 else 'FAIL'}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <response.json> <metadata.yaml>")
        sys.exit(1)
    score(sys.argv[1], sys.argv[2])
