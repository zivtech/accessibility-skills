#!/usr/bin/env python3
"""Focused checks for the ICT baseline test-ID fidelity validator
(score_common.check_baseline_ids / load_baseline_manifest — adoption plan
Phase 3, step 11). Ground truth is the real committed manifest, so these
tests also pin the manifest's shape: 62 web IDs, 57 documents IDs, the
upstream stale-string ledger."""

from score_common import BASELINE_ID_RE, check_baseline_ids, load_baseline_manifest

MANIFEST = load_baseline_manifest()


def test_manifest_shape_pins():
    assert len(MANIFEST["web_ids"]) == 62
    assert len(MANIFEST["documents_lower"]) == 57
    assert "21.b-autoupdate" in MANIFEST["stale"]


def test_valid_web_citation_under_declared_scope():
    r = check_baseline_ids(
        "Baseline test: 5.A-ControlName — the button has no accessible name.",
        MANIFEST, declared=True, expected_ids=["5.A-ControlName"],
    )
    assert r["valid"] == ["5.A-ControlName"]
    assert not r["fabricated"] and not r["cross_baseline"]
    assert not r["undeclared"] and not r["expected_missing"]


def test_fabricated_id_is_caught():
    r = check_baseline_ids(
        "Filed under Baseline test 5.E-ControlLabel per the federal profile.",
        MANIFEST, declared=True,
    )
    assert [t for t, _ in r["fabricated"]] == ["5.E-ControlLabel"]


def test_upstream_stale_string_gets_the_ledger_hint():
    r = check_baseline_ids(
        "then Baseline Test 21.B-AutoUpdate fails",
        MANIFEST, declared=True,
    )
    (tok, hint), = r["fabricated"]
    assert tok == "21.B-AutoUpdate"
    assert "21.C-AutoUpdate" in hint


def test_documents_only_id_is_cross_baseline_not_fabricated():
    r = check_baseline_ids(
        "The PDF library maps to 11.A-DocumentTitled in the documents regime.",
        MANIFEST, declared=True,
    )
    assert r["cross_baseline"] == ["11.A-DocumentTitled"]
    assert not r["fabricated"]


def test_undeclared_scope_flags_any_citation_even_valid_ones():
    r = check_baseline_ids(
        "This maps to baseline test 1.A-KeyboardAccess.",
        MANIFEST, declared=False,
    )
    assert r["undeclared"] == ["1.A-KeyboardAccess"]
    assert r["valid"] == ["1.A-KeyboardAccess"]


def test_expected_missing_reported():
    r = check_baseline_ids(
        "No IDs cited here at all.", MANIFEST, declared=True,
        expected_ids=["5.A-ControlName"],
    )
    assert r["expected_missing"] == ["5.A-ControlName"]
    assert not r["cited"]


def test_case_insensitive_membership():
    r = check_baseline_ids(
        "baseline test 5.a-controlname applies.", MANIFEST, declared=True,
        expected_ids=["5.A-ControlName"],
    )
    assert r["valid"] == ["5.a-controlname"]
    assert not r["fabricated"] and not r["expected_missing"]


def test_grammar_never_matches_versions_scs_or_selectors():
    text = (
        "axe-core 4.9.1 flagged WCAG 4.1.2 on li:nth-child(3) at step-2; "
        "tags TT6.a and wcag412; contrast 4.5:1; v3.0.1 tag; E205.4 provision."
    )
    assert not BASELINE_ID_RE.findall(text)
    r = check_baseline_ids(text, MANIFEST, declared=False)
    assert not r["cited"] and not r["undeclared"]


def test_longer_token_wins_over_stale_prefix():
    # "5.A-ControlName" must not be double-read as the stale "5.A-Control".
    r = check_baseline_ids("5.A-ControlName", MANIFEST, declared=True)
    assert r["valid"] == ["5.A-ControlName"] and not r["fabricated"]


def test_filed_row_regex_accepts_plausible_label_formats():
    from score_bugreport import BASELINE_JSON_RE, BASELINE_ROW_RE
    filed_shapes = [
        "**Baseline test:** 5.A-ControlName",
        "- **Baseline test:** 5.A-ControlName",
        "**ICT Baseline test:** 5.A-ControlName",
        "**Baseline test (ICT Testing Baseline web):** 5.A-ControlName",
        "| Baseline test | 5.A-ControlName |",
        "Baseline Test ID: 5.A-ControlName",
    ]
    for line in filed_shapes:
        assert BASELINE_ROW_RE.search(line), f"row regex missed: {line}"
    assert BASELINE_JSON_RE.search('"baseline_test": "5.A-ControlName"')


def test_filed_row_regex_rejects_prose_mentions():
    from score_bugreport import BASELINE_ROW_RE
    prose = [
        "the baseline test 24.A-Parsing always passes upstream",
        "Candidate baseline tests considered were 5.A-ControlName and 5.B-ControlRole.",
    ]
    for line in prose:
        assert not BASELINE_ROW_RE.search(line), f"row regex over-matched prose: {line}"


if __name__ == "__main__":
    import sys
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as e:
                failures += 1
                print(f"FAIL {name}: {e}")
    sys.exit(1 if failures else 0)
