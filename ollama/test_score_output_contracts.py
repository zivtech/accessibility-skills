#!/usr/bin/env python3
"""Focused checks for score_output evidence-contract parsing."""

from score_output import (
    check_evidence_contract,
    check_verdict,
    count_false_positives,
    evidence_contract_gate_ok,
)


COMPLETE_CONTRACT = """### A11y Evidence Finding
finding_id: a11y_form_error_describedby
fingerprint: a1b2c3d4
source: a11y-test Playwright keyboard evidence
wcag_or_apg: WCAG 1.3.1 Info and Relationships
section_508_fpc_context: Revised Section 508 web context maps to WCAG 2.0 Level A/AA
severity: MAJOR
perspective_alarms: screen_reader_semantic=HIGH
evidence: LoginForm.tsx:72 input lacks aria-describedby for visible error
reproduction_steps: Submit the form empty and focus the email field
expected_behavior: Screen reader announces the associated error
actual_behavior: Screen reader announces invalid state without the error text
trend: persistent
"""


def test_complete_contract_passes():
    contract = check_evidence_contract(COMPLETE_CONTRACT)
    assert contract["total"] == 1
    assert contract["complete"] == 1
    assert contract["required_ok"]
    assert contract["ids_ok"]
    assert contract["trend_ok"]
    assert evidence_contract_gate_ok(contract, required=True)


def test_missing_required_field_fails():
    contract = check_evidence_contract(
        COMPLETE_CONTRACT.replace(
            "actual_behavior: Screen reader announces invalid state without the error text\n",
            "",
        )
    )
    assert contract["total"] == 1
    assert not contract["required_ok"]
    assert not evidence_contract_gate_ok(contract, required=True)


def test_bad_ids_fail():
    contract = check_evidence_contract(
        COMPLETE_CONTRACT.replace("a11y_form_error_describedby", "mf-1").replace(
            "a1b2c3d4",
            "nothex",
        )
    )
    assert not contract["ids_ok"]
    assert not evidence_contract_gate_ok(contract, required=True)


def test_invalid_trend_fails():
    contract = check_evidence_contract(COMPLETE_CONTRACT.replace("persistent", "recurring"))
    assert not contract["trend_ok"]
    assert not evidence_contract_gate_ok(contract, required=True)


def test_required_contract_must_exist():
    contract = check_evidence_contract("Verdict: REVISE\nFinding text without a contract.")
    assert contract["total"] == 0
    assert not evidence_contract_gate_ok(contract, required=True)
    assert evidence_contract_gate_ok(contract, required=False)


def test_explicit_verdict_wins_over_prose_bait():
    text = "I considered whether to REVISE this review.\n\nVerdict: ACCEPT\n"
    assert check_verdict(text) == "ACCEPT"


def test_false_positive_counter_ignores_prose_bait():
    text = "This clean component mentions CRITICAL risk only as a hypothetical example.\nVerdict: ACCEPT"
    verdict = check_verdict(text)
    false_positives = count_false_positives(text, verdict)
    assert false_positives["structured_findings"] == 0
    assert not false_positives["wrong_verdict"]


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"PASS: {name}")
