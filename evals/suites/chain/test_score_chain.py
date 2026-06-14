#!/usr/bin/env python3
"""Unit tests for score_chain.py (plan 011 fixes I1-I9 + M1/M2).

Validates scorer functions against PRISTINE snippets (the agents' own output). These are
the FUNCTION-level guards; the INTEGRATION guard is re-scoring the 3 pristine pilot captures
(operator zones split out per I9) -- both are wired into scripts/smoke_chain.sh. Run free,
before any paid re-run:

    python3 evals/suites/chain/test_score_chain.py     # this file (function unit tests)
    bash scripts/smoke_chain.sh                         # units + the 3-capture integration

M2/I9/M1 cases below are the proposal-critic must-fixes (2026-06-13): prose never binds an
alarm, the operator zone is stripped before parsing while its peek flag still gates, and an
all-LOW over-escalation is observational rather than auto-failed.
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

# --- M2: parse_alarms reads structured table rows ONLY, never prose -------------------
check("M2 prose with a bare level is NOT bound ('SR experience is HIGH quality')",
      "screen_reader_semantic" in sc.parse_alarms("The screen reader experience is HIGH quality."),
      False)
check("M2 multi-perspective prose line does not bind first level to every lens",
      sc.parse_alarms("auditory_access: HIGH, screen_reader_semantic: MEDIUM, all others LOW"), {})
check("M2 a real table row IS parsed",
      sc.parse_alarms("| screen reader | HIGH |").get("screen_reader_semantic"), "HIGH")
check("M2 perspective read from cell[0]: keyboard row maps to keyboard_motor",
      sc.parse_alarms("| Keyboard-only | MEDIUM | screen reader users also affected |")
      .get("keyboard_motor"), "MEDIUM")
check("M2 rationale cross-talk does not leak screen_reader from a keyboard row",
      "screen_reader_semantic" in sc.parse_alarms(
          "| Keyboard-only | MEDIUM | screen reader users also affected |"), False)

# --- I9: operator zone stripped before parsing; peek flag read from the zone ----------
# The video case: agent PARAPHRASED the rubric, so the verbatim answer-key strings live only
# in the operator note. After stripping, detect_peek finds nothing -- the peek flag is the gate.
PEEK_CAPTURE = ("# Verdict: REVISE\n| auditory_access | HIGH |\n"
                "<!--OPERATOR\npeek: true\n"
                "reason: critic read expected_alarm_levels from the .chain.yaml rubric\n"
                "OPERATOR-->\n")
pristine_peek, flag_peek = sc.split_operator(PEEK_CAPTURE)
check("I9 operator zone (answer-key quote) stripped from pristine",
      "expected_alarm_levels" in pristine_peek, False)
check("I9 agent table survives stripping", "auditory_access" in pristine_peek, True)
check("I9 peek: true read from the zone", flag_peek, True)
check("I9 detect_peek on pristine finds nothing (paraphrased peek evades it)",
      sc.detect_peek(pristine_peek), [])
pristine_clean, flag_clean = sc.split_operator(
    "# Verdict: ACCEPT\n| cognitive | LOW |\n<!--OPERATOR\npeek: false\nreason: stayed blind\nOPERATOR-->\n")
check("I9 peek: false read from the zone", flag_clean, False)
check("I9 no-zone text passes through unchanged",
      sc.split_operator("just agent output, no zone")[0], "just agent output, no zone")

# --- M1: all-LOW S4 over-escalation is OBSERVATIONAL, not auto-fail -------------------
OBS_RUBRIC = {"expected_escalation": False, "s4_graded": True, "s4_observational": True,
              "expected_escalated_perspectives": [],
              "expected_alarm_levels": {k: "LOW" for k in LOGIN_RUBRIC["expected_alarm_levels"]}}
check("M1 observational: correct no-escalation still scores S4=1 (happy path probed)",
      sc.s4(OBS_RUBRIC, False, "every perspective LOW")[0], 1)
check("M1 observational: over-escalation -> None (human review), NOT auto-0",
      sc.s4(OBS_RUBRIC, True, "| cognitive | MEDIUM |")[0], None)
check("M1 non-observational all-LOW still auto-fails over-escalation (contrast)",
      sc.s4(ALLLOW_RUBRIC, True, "| cognitive | MEDIUM |")[0], 0)

# --- report ---------------------------------------------------------------------------
print("\n=== score_chain unit tests (plan 011) ===")
passed = 0
for name, ok, detail in CASES:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  ({detail})")
    passed += ok
print(f"\n{passed}/{len(CASES)} passed")
sys.exit(0 if passed == len(CASES) else 1)
