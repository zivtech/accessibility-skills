#!/usr/bin/env python3
"""Unit tests for score_chain.py (plan 011 fixes I1-I6).

Validates the scorer functions against PRISTINE snippets extracted from the 2026-06-13
pilot outputs -- NOT by re-scoring the captured .txt files, which interleave operator
annotations that quote the answer key (finding I9). Run free, before any paid re-run:

    python3 evals/suites/chain/test_score_chain.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_chain as sc

CASES = []


def check(name, got, want, tol=None):
    ok = (abs(got - want) <= tol) if tol is not None else (got == want)
    CASES.append((name, ok, f"got={got} want={want}" + (f" (tol {tol})" if tol else "")))


# --- I2: crosswalk + absent-as-LOW + max-collapse -------------------------------------
# Pristine perspective tables (the agents' own output, no annotations).
MODAL_TABLE = """
| Screen reader | MEDIUM | Major 2 double-announce |
| Keyboard-only | MEDIUM | Enter-submit path |
| Low vision    | MEDIUM | Headline focus-ring fix on blue buttons |
| Voice control | LOW    | programmatic spoken name present |
| Switch access | LOW    | focus order + trap well-designed |
| Cognitive     | LOW    | specific error messages, no timeouts |
"""
LOGIN_TABLE = """
| screen reader        | MEDIUM |
| keyboard             | MEDIUM |
| low vision           | LOW    |
| cognitive            | MEDIUM |
| motor                | LOW    |
| speech / voice       | LOW    |
| seizure / vestibular | LOW    |
"""
MODAL_RUBRIC = {"expected_alarm_levels": {
    "magnification_reflow": "LOW", "environmental_contrast": "LOW",
    "vestibular_motion": "LOW", "auditory_access": "LOW",
    "keyboard_motor": "HIGH", "screen_reader_semantic": "HIGH",
    "cognitive_neurodivergent": "MEDIUM"}}
LOGIN_RUBRIC = {"expected_alarm_levels": {
    "magnification_reflow": "LOW", "environmental_contrast": "LOW",
    "vestibular_motion": "LOW", "auditory_access": "LOW",
    "keyboard_motor": "LOW", "screen_reader_semantic": "LOW",
    "cognitive_neurodivergent": "MEDIUM"}}

# max-collapse: keyboard MEDIUM + voice/switch/motor LOW all map to keyboard_motor -> MEDIUM
alarms = sc.parse_alarms(MODAL_TABLE)
check("I2 crosswalk: low vision -> magnification_reflow", alarms.get("magnification_reflow"), "MEDIUM")
check("I2 max-collapse: keyboard_motor is MEDIUM not LOW", alarms.get("keyboard_motor"), "MEDIUM")

s3_modal, _ = sc.s3_alarm(MODAL_RUBRIC, MODAL_TABLE)
s3_login, _ = sc.s3_alarm(LOGIN_RUBRIC, LOGIN_TABLE)
# Broken scorer produced modal 0.214 / login 0.429. Manual ground truth ~0.6 / ~0.86.
check("I2 modal S3 in healthy band (~0.71, manual ~0.6)", s3_modal, 0.714, tol=0.02)
check("I2 login S3 matches manual ~0.86", s3_login, 0.857, tol=0.02)
check("I2 modal S3 well above broken-floor 0.214", float(s3_modal > 0.5), 1.0)

# --- I3: concept-based tracer match (real pilot phrasings, synonym-shifted) ------------
MODAL_AUDIT = ("# Perspective Audit -- modal-broken-focus-trap\n"
               "MAJOR -- No focus movement INTO the dialog on open. Focus stays on the "
               "trigger; next Tab lands on background nav.")
VIDEO_AUDIT = ("CRITICAL 1 -- Video with instructor speech has NO captions. <video> "
               "self-closing, no <track> child. 1.2.2 Level A.")
check("I3 modal tracer survives synonym shift (moved->movement, modal->dialog)",
      sc.tracer({"tracer_finding": "Focus not moved to modal on open -- stays on trigger button"},
                MODAL_AUDIT)[0], 1)
check("I3 video tracer survives (track/captions present)",
      sc.tracer({"tracer_finding": 'Missing <track kind="captions"> element on <video>'},
                VIDEO_AUDIT)[0], 1)
check("I3 tracer correctly MISSES unrelated text",
      sc.tracer({"tracer_finding": "Focus not moved to modal on open -- stays on trigger button"},
                "The button has a nice color and good contrast.")[0], 0)

# --- I4: verdict line + finding counts, not a bare PASS token --------------------------
PASS_RUBRIC = {"expected_audit_verdict": "PASS"}
check("I4 REVISE + MAJOR:3 -> NON-PASS (was false-positive on 'PASS' token)",
      sc.audit_verdict(PASS_RUBRIC, "## Summary\nCRITICAL: 0. MAJOR: 3\n"
                       "Overall recommendation: REVISE (not a block; no CRITICAL).")[0], 0)
check("I4 ACCEPT + 0/0 -> PASS",
      sc.audit_verdict(PASS_RUBRIC, "Perspectives audited: 1. CRITICAL: 0. MAJOR: 0.\n"
                       "Overall recommendation: ACCEPT -- no blocking issues.")[0], 1)
check("I4 'Many PASS items recorded' with no verdict line -> NOT a false PASS",
      sc.audit_verdict(PASS_RUBRIC, "Many PASS items recorded honestly (landmarks, labels).")[0], 0)

# --- I1: peek detection ---------------------------------------------------------------
check("I1 flags the video critic's actual rubric quote",
      len(sc.detect_peek("opened: \"Expected alarm levels are pre-defined: "
                         "auditory_access: HIGH, screen_reader_semantic: MEDIUM\"")) > 0, True)
check("I1 clean critic output is not flagged",
      sc.detect_peek("MAJOR 1 -- Stale aria-invalid persists on a corrected field. WCAG 4.1.2."), [])

# --- I5: S5a scoped to critic-escalated set, per-section ------------------------------
# critic escalates SR+keyboard+cognitive (the login critic's actual flags).
CLEAN_AUDIT = ("## Screen Reader & Semantic (MEDIUM)\nMAJOR -- stale aria-invalid.\n"
               "## Keyboard & Motor (MEDIUM)\nFalse positive; CLEAN today.\n"
               "## Cognitive & Neurodivergent (MEDIUM)\nMAJOR -- stale red border.\n")
LEAK_AUDIT = CLEAN_AUDIT + "## Magnification & Reflow (LOW)\nMAJOR -- zoom breaks layout.\n"
s5_clean, _ = sc.s5(LOGIN_RUBRIC, CLEAN_AUDIT, LOGIN_TABLE)
s5_leak, _ = sc.s5(LOGIN_RUBRIC, LEAK_AUDIT, LOGIN_TABLE)
check("I5 audit reviewing only critic-escalated perspectives -> S5a ok (S5=2)", s5_clean, 2)
check("I5 audit opening a non-escalated LOW section -> leak (S5=1)", s5_leak, 1)

# --- S4: all-LOW never-escalate probe + CLEAN narrow-escalation scope (plan 011) ------
ALLLOW_RUBRIC = {"expected_escalation": False, "s4_graded": True,
                 "expected_escalated_perspectives": [],
                 "expected_alarm_levels": {k: "LOW" for k in LOGIN_RUBRIC["expected_alarm_levels"]}}
check("S4 all-LOW: no escalation is correct (1)",
      sc.s4(ALLLOW_RUBRIC, False, "every perspective LOW")[0], 1)
check("S4 all-LOW: any escalation is an over-escalation (0)",
      sc.s4(ALLLOW_RUBRIC, True, "every perspective LOW")[0], 0)

NARROW_RUBRIC = {"expected_escalation": True, "s4_graded": True,
                 "expected_escalated_perspectives": ["cognitive_neurodivergent"],
                 "expected_alarm_levels": LOGIN_RUBRIC["expected_alarm_levels"]}
check("S4 narrow (login post-fix): critic escalates cognitive ONLY -> 1",
      sc.s4(NARROW_RUBRIC, True, "| cognitive | MEDIUM |")[0], 1)
check("S4 narrow: scope-inflated (cognitive + keyboard) -> 0",
      sc.s4(NARROW_RUBRIC, True, "| cognitive | MEDIUM |\n| keyboard | MEDIUM |")[0], 0)

# --- report ---------------------------------------------------------------------------
print("\n=== score_chain unit tests (plan 011) ===")
passed = 0
for name, ok, detail in CASES:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  ({detail})")
    passed += ok
print(f"\n{passed}/{len(CASES)} passed")
sys.exit(0 if passed == len(CASES) else 1)
