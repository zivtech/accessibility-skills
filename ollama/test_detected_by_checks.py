#!/usr/bin/env python3
"""Focused checks for the cross-detector corroboration canary (issue #85)
— score_common.check_detected_by / check_corroboration_sentences /
ENGINE_ID_VOCAB / ENGINE_MENTION_RE. Ground truth is the fixed 4-term
detector vocabulary (axe-core, html_codesniffer, alfa, wave); anything else
mentioned as a detecting engine is a fabrication."""

from score_common import (
    ENGINE_ID_VOCAB,
    ENGINE_MENTION_RE,
    check_corroboration_sentences,
    check_detected_by,
)


def test_vocab_pins():
    assert ENGINE_ID_VOCAB == {"axe-core", "html_codesniffer", "alfa", "wave"}


def test_valid_mentions_pass_clean():
    r = check_detected_by(
        "Detected by axe-core and WAVE (cross-detector agreement).",
        source_detected_by={"1.4.3": ["axe-core", "wave"]},
    )
    assert set(t.lower() for t in r["valid"]) == {"axe-core", "wave"}
    assert not r["fabricated"]


def test_near_miss_lighthouse_caught():
    r = check_detected_by("Lighthouse also flagged it.")
    assert any(tok == "Lighthouse" for tok, _ in r["fabricated"])


def test_near_miss_bare_axe_caught():
    r = check_detected_by("Rule: axe — color-contrast.")
    assert any(tok == "axe" for tok, _ in r["fabricated"])


def test_other_near_misses_caught():
    for phrase, expect in [
        ("Confirmed via pa11y as well.", "pa11y"),
        ("Axe DevTools also surfaced this.", "Axe DevTools"),
        ("Accessibility Insights flagged the same node.", "Accessibility Insights"),
        ("IBM Equal Access reported it too.", "IBM Equal Access"),
    ]:
        r = check_detected_by(phrase)
        assert any(tok == expect for tok, _ in r["fabricated"]), phrase


def test_unattributed_valid_id_caught_as_invented_corroboration():
    # wave is real vocabulary, but 1.4.3's source only lists axe-core —
    # attributing wave to 1.4.3 in the same sentence is invented
    # corroboration, not a clean valid mention.
    r = check_detected_by(
        "For 1.4.3, wave also corroborated the finding.",
        source_detected_by={"1.4.3": ["axe-core"]},
    )
    hints = [hint for tok, hint in r["fabricated"] if tok.lower() == "wave"]
    assert hints and "invented corroboration" in hints[0]


def test_attributed_valid_id_within_source_is_clean():
    r = check_detected_by(
        "For 1.4.3, axe-core and wave both flagged the low-contrast header.",
        source_detected_by={"1.4.3": ["axe-core", "wave"]},
    )
    assert not r["fabricated"]


def test_case_insensitive_vocab_membership():
    r = check_detected_by("Detected by AXE-CORE and Wave.")
    assert set(t.lower() for t in r["valid"]) == {"axe-core", "wave"}
    assert not r["fabricated"]


def test_word_boundary_safety_axe_core_runner_and_wavelength():
    text = ("Captured via axe-core-runner-1.2 in CI; the header's wavelength "
            "of light was not the cause of the contrast failure.")
    r = check_detected_by(text)
    assert not r["fabricated"], r["fabricated"]
    # bare "axe" and bare "wave" must not have tripped inside these tokens
    assert not any(t.lower() == "axe" for t in r["cited"])
    assert not any(t.lower() == "wave" for t in r["cited"])


def test_no_source_detected_by_is_vocab_only_mode():
    r = check_detected_by("Lighthouse flagged 1.4.3.")
    assert any(tok == "Lighthouse" for tok, _ in r["fabricated"])


def test_corroboration_sentence_confirmation_collision():
    tokens_ctx = ["corroborated", "both engines", "two scanners",
                  "cross-detector", "both scanners", "scanner agreement",
                  "both tools", "two tools"]
    tokens_forbidden = ["confirmed", "verified", "proven"]
    text = ("This defect was corroborated by axe-core and WAVE and has "
            "been confirmed. Severity remains MAJOR.")
    offending = check_corroboration_sentences(text, tokens_ctx, tokens_forbidden)
    assert len(offending) == 1
    assert "corroborated" in offending[0].lower()
    assert "confirmed" in offending[0].lower()


def test_corroboration_sentence_unrelated_clauses_do_not_collide():
    tokens_ctx = ["corroborated"]
    tokens_forbidden = ["verified"]
    text = ("This defect was corroborated by the team. The fix was "
            "verified separately in a later release.")
    # Both tokens appear in the text, but in SEPARATE (period-delimited)
    # sentences — the sentence-scoped helper must not flag a document-wide
    # co-occurrence across unrelated clauses.
    offending = check_corroboration_sentences(text, tokens_ctx, tokens_forbidden)
    assert offending == []


def test_corroboration_sentence_known_instrument_limit_semicolon_clause():
    # Documented known limit (fixture notes, riverbend-permits-corroboration
    # metadata): a semicolon joins two clauses into one sentence for this
    # heuristic splitter, so "corroborated by the team; the fix was
    # verified separately" DOES collide even though the clauses are
    # unrelated. This is an intentional, documented false-positive
    # direction — detector output, not a verdict; a human adjudicates
    # before counting it as a real miss. Pinning the behavior here so a
    # future change to the splitter is a deliberate decision, not a
    # regression nobody noticed.
    tokens_ctx = ["corroborated"]
    tokens_forbidden = ["verified"]
    text = ("This defect was corroborated by the team; the fix was "
            "verified separately in a later release.")
    offending = check_corroboration_sentences(text, tokens_ctx, tokens_forbidden)
    assert len(offending) == 1


def test_corroboration_sentence_clean_mention_passes():
    tokens_ctx = ["corroborated", "cross-detector"]
    tokens_forbidden = ["confirmed", "verified", "proven"]
    text = "This defect was corroborated by axe-core and wave (cross-detector agreement); severity remains MAJOR."
    offending = check_corroboration_sentences(text, tokens_ctx, tokens_forbidden)
    assert offending == []


def test_engine_mention_re_direct_ordering():
    # axe-core must win over the bare "axe" alternative at the same position.
    m = ENGINE_MENTION_RE.search("axe-core-runner-1.2")
    assert m and m.group(0).lower() == "axe-core"


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
