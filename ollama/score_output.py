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
import os
import sys
import re
import yaml

sys.path.insert(0, os.path.dirname(__file__))
from score_common import strip_thinking, MUST_FIND_ABORT_THRESHOLD  # noqa: E402

REQUIRED_EVIDENCE_FIELDS = {
    "finding_id",
    "fingerprint",
    "source",
    "wcag_or_apg",
    "section_508_fpc_context",
    "severity",
    "perspective_alarms",
    "evidence",
    "reproduction_steps",
    "expected_behavior",
    "actual_behavior",
}
TREND_VALUES = {"new", "persistent", "worsening", "improving", "resolved"}

FIELD_ALIASES = {
    "wcag_apg": "wcag_or_apg",
    "wcag_apg_citation": "wcag_or_apg",
    "section_508_fpc": "section_508_fpc_context",
    "section_508_context": "section_508_fpc_context",
    "reproduction": "reproduction_steps",
    "steps_to_reproduce": "reproduction_steps",
    "expected": "expected_behavior",
    "actual": "actual_behavior",
    "perspective_alarm": "perspective_alarms",
}


def load_response(path: str) -> tuple[str, bool]:
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
        role_match = re.search(r"role[=\"'\s]+(\w+)", description.lower())
        if role_match:
            keywords = [role_match.group(1), "role"]
    elif "fieldset" in description.lower() or "group" in description.lower():
        keywords = ["fieldset", "group", "legend"]
    else:
        from score_common import fallback_keywords
        keywords = [kw.lower() for kw in fallback_keywords(description)]

    from score_common import normalize_quotes
    norm_text = normalize_quotes(text.lower())
    found = any(normalize_quotes(kw.lower()) in norm_text for kw in keywords)

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


def count_false_positives(text: str, declared_verdict: str) -> dict:
    """For CLEAN fixtures: check if the model raised actual accessibility findings.

    Uses structured signals (numbered findings, severity-tagged items) rather than
    keyword matching, which false-fires on section headers and positive statements.
    Accepts the already-computed verdict to avoid re-deriving it.
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

    reject_revise = declared_verdict in ("REJECT", "REVISE")

    return {
        "structured_findings": finding_count,
        "wrong_verdict": reject_revise,
    }


def normalize_contract_key(raw_key: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", raw_key.strip().lower()).strip("_")
    return FIELD_ALIASES.get(key, key)


def extract_evidence_contracts(text: str) -> list[dict]:
    """Extract optional A11y Evidence Finding Contract blocks.

    Contract blocks are markdown sections headed "A11y Evidence Finding" with
    key/value lines. The parser is intentionally simple and format-tolerant:
    it validates the data contract without becoming a second markdown engine.
    """
    contracts = []
    current = None
    for line in text.splitlines():
        if re.match(r"^\s{0,3}#{1,6}\s+A11y Evidence Finding\b", line, re.IGNORECASE):
            if current:
                contracts.append(current)
            current = {}
            continue
        if current is None:
            continue
        if re.match(r"^\s{0,3}#{1,6}\s+", line):
            contracts.append(current)
            current = None
            continue
        match = re.match(r"^\s*(?:[-*]\s*)?(?:\*\*)?([A-Za-z0-9 _/-]+)(?:\*\*)?\s*:\s*(.+?)\s*$", line)
        if match:
            key = normalize_contract_key(match.group(1))
            current[key] = match.group(2).strip()
    if current:
        contracts.append(current)
    return contracts


def check_evidence_contract(text: str) -> dict:
    contracts = extract_evidence_contracts(text)
    if not contracts:
        return {
            "total": 0,
            "complete": 0,
            "required_ok": True,
            "ids_ok": True,
            "trend_ok": True,
            "missing": [],
        }

    missing = []
    ids_ok = True
    trend_ok = True
    complete = 0
    for idx, contract in enumerate(contracts, start=1):
        missing_fields = sorted(REQUIRED_EVIDENCE_FIELDS - set(contract))
        if missing_fields:
            missing.append((idx, missing_fields))
        else:
            complete += 1

        finding_id = contract.get("finding_id", "")
        fingerprint = contract.get("fingerprint", "")
        if not re.match(r"^[a-z0-9][a-z0-9:_-]{7,}$", finding_id, re.IGNORECASE):
            ids_ok = False
        if not re.match(r"^[a-f0-9]{8,64}$", fingerprint, re.IGNORECASE):
            ids_ok = False

        trend = contract.get("trend")
        if trend and trend.lower() not in TREND_VALUES:
            trend_ok = False

    return {
        "total": len(contracts),
        "complete": complete,
        "required_ok": not missing,
        "ids_ok": ids_ok,
        "trend_ok": trend_ok,
        "missing": missing,
    }


def print_evidence_contract_summary(contract: dict) -> None:
    if contract["total"] == 0:
        print("Evidence contract: no findings declared")
        return

    print(f"Evidence contract: {contract['complete']} complete / {contract['total']} total")
    print(f"Required fields: {'PASS' if contract['required_ok'] else 'FAIL'}")
    print(f"Stable finding ids: {'PASS' if contract['ids_ok'] else 'FAIL'}")
    print(f"Trend values: {'PASS' if contract['trend_ok'] else 'FAIL'}")
    for idx, fields in contract["missing"]:
        print(f"  Missing fields in contract {idx}: {', '.join(fields)}")


def evidence_contract_gate_ok(contract: dict, required: bool) -> bool:
    if not required:
        return True
    return (
        contract["total"] > 0
        and contract["complete"] == contract["total"]
        and contract["required_ok"]
        and contract["ids_ok"]
        and contract["trend_ok"]
    )


def score(response_path: str, rubric_path: str):
    text, truncated = load_response(response_path)
    if truncated:
        print("Response truncated mid-<think> block — not scoring")
        print("Status: INCOMPLETE — truncated response")
        return
    rubric = load_rubric(rubric_path)
    difficulty = rubric.get("difficulty", "unknown")
    contract = check_evidence_contract(text)
    contract_required = bool(rubric.get("require_evidence_contract"))

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
    print_evidence_contract_summary(contract)
    if contract_required:
        print(f"Evidence contract required: YES")
        print(f"Evidence contract gate: {'PASS' if evidence_contract_gate_ok(contract, True) else 'FAIL'}")
    print()

    if difficulty == "CLEAN":
        expected_verdict = "ACCEPT"
        print(f"Verdict: {verdict} (expected: ACCEPT or ACCEPT-WITH-RESERVATIONS)")
        correct_verdict = verdict in ("ACCEPT", "ACCEPT-WITH-RESERVATIONS")
        print(f"Verdict correct: {'YES' if correct_verdict else 'NO — FALSE ALARM'}")
        print()

        fp = count_false_positives(text, verdict)
        print(f"False positive signals:")
        print(f"  Structured findings (numbered/tagged): {fp['structured_findings']}")
        print(f"  Wrong verdict (REJECT/REVISE): {fp['wrong_verdict']}")
        print()

        passed = correct_verdict and not fp["wrong_verdict"]
        passed = passed and evidence_contract_gate_ok(contract, contract_required)
        status = "PASS" if passed else "FAIL"
        if fp["structured_findings"] > 0 and passed:
            status = "WARN — correct verdict but raised findings (review manually)"
        print(f"Status: {status}")
    elif difficulty == "ADVERSARIAL":
        valid_verdicts = ("ACCEPT-WITH-RESERVATIONS", "REVISE")
        print(f"Verdict: {verdict} (valid for ADVERSARIAL: {', '.join(valid_verdicts)})")
        verdict_ok = verdict in valid_verdicts
        print(f"Verdict acceptable: {'YES' if verdict_ok else 'NO'}")
        print()

        must_articulate = []
        should_find = []
        for cat in rubric.get("expected_findings", []):
            category = cat.get("category", "")
            for item in cat.get("items", []):
                result = check_finding(text, item)
                result["category"] = category
                if category == "must_articulate":
                    must_articulate.append(result)
                elif category == "should_find":
                    should_find.append(result)

        if must_articulate:
            print(f"Must-articulate tradeoffs: {sum(1 for r in must_articulate if r['found'])}/{len(must_articulate)}")
            for r in must_articulate:
                marker = "+" if r["found"] else "X"
                kw_suffix = f"  (keywords: {r['keywords_checked']})" if not r["found"] else ""
                print(f"  {marker} {r['description'][:80]}{kw_suffix}")
            print()

        if should_find:
            print(f"Should-find issues: {sum(1 for r in should_find if r['found'])}/{len(should_find)}")
            for r in should_find:
                marker = "+" if r["found"] else "X"
                kw_suffix = f"  (keywords: {r['keywords_checked']})" if not r["found"] else ""
                print(f"  {marker} {r['description'][:80]}{kw_suffix}")
            print()

        articulate_score = sum(1 for r in must_articulate if r["found"]) / max(len(must_articulate), 1)
        passed = verdict_ok and articulate_score >= 0.5
        passed = passed and evidence_contract_gate_ok(contract, contract_required)
        print(f"Must-articulate rate: {articulate_score:.0%}")
        print(f"Status: {'PASS' if passed else 'FAIL'}")
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
            kw_suffix = f"  (keywords: {r['keywords_checked']})" if not r["found"] else ""
            print(f"  {marker} [{wcag_marker}] {r['description'][:80]}{kw_suffix}")
        print()

        print(f"Should-find issues: {sum(1 for r in should_find if r['found'])}/{len(should_find)}")
        for r in should_find:
            marker = "+" if r["found"] else "X"
            wcag_marker = "W" if r["wcag_cited"] else "-"
            kw_suffix = f"  (keywords: {r['keywords_checked']})" if not r["found"] else ""
            print(f"  {marker} [{wcag_marker}] {r['description'][:80]}{kw_suffix}")
        print()

        must_score = sum(1 for r in must_find if r["found"]) / max(len(must_find), 1)
        print(f"Must-find detection rate: {must_score:.0%}")
        print(f"Abort threshold: {MUST_FIND_ABORT_THRESHOLD:.0%} (escalation gate — see score_common.py)")
        passed = must_score >= MUST_FIND_ABORT_THRESHOLD
        passed = passed and evidence_contract_gate_ok(contract, contract_required)
        print(f"Status: {'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <response.json> <metadata.yaml>")
        sys.exit(1)
    score(sys.argv[1], sys.argv[2])
