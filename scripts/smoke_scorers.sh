#!/usr/bin/env bash
# Smoke tests for the scorer scripts.
# Run from repo root: bash scripts/smoke_scorers.sh
# Exits 1 on any failed assertion; prints scorer output on failure.
set -euo pipefail

SMOKE_DIR="evals/suites/smoke"

pass_count=0
fail_count=0

run_case() {
    local label="$1"
    local scorer="$2"
    local response="$3"
    local metadata="$4"
    shift 4
    local assertions=("$@")

    local output
    output=$(python3 "$scorer" "$SMOKE_DIR/$response" "$SMOKE_DIR/$metadata" 2>&1)

    local failed=0
    for assert in "${assertions[@]}"; do
        if ! echo "$output" | grep -qF "$assert"; then
            echo "FAIL: $label"
            echo "  Expected to find: $assert"
            echo "--- Scorer output ---"
            echo "$output"
            echo "---------------------"
            failed=1
        fi
    done

    if [ "$failed" -eq 0 ]; then
        echo "PASS: $label"
        pass_count=$((pass_count + 1))
    else
        fail_count=$((fail_count + 1))
    fi
}

# Case 1: critic HAS-BUGS
run_case \
    "critic HAS-BUGS (must-find 2/2, PASS)" \
    "ollama/score_output.py" \
    "critic-hasbugs-response.json" \
    "critic-hasbugs.metadata.yaml" \
    "Must-find issues: 2/2" \
    "Status: PASS"

# Case 1b: critic explicit keywords (keywords_all + keywords_any; keywords alone)
run_case \
    "critic explicit keywords (both items hit, PASS)" \
    "ollama/score_output.py" \
    "critic-keywords-hit-response.json" \
    "critic-keywords.metadata.yaml" \
    "Must-find issues: 2/2" \
    "Status: PASS"

run_case \
    "critic explicit keywords (has-text without semantics/remedy, no trace: 0/2, FAIL)" \
    "ollama/score_output.py" \
    "critic-keywords-partial-response.json" \
    "critic-keywords.metadata.yaml" \
    "Must-find issues: 0/2" \
    "Status: FAIL"

# Case 2: critic CLEAN
run_case \
    "critic CLEAN (verdict correct, PASS)" \
    "ollama/score_output.py" \
    "critic-clean-response.json" \
    "critic-clean.metadata.yaml" \
    "Evidence contract: no findings declared" \
    "Verdict correct: YES" \
    "Status: PASS"

# Case 3: critic evidence contract
run_case \
    "critic evidence contract (complete contract, PASS)" \
    "ollama/score_output.py" \
    "critic-evidence-contract-response.json" \
    "critic-evidence-contract.metadata.yaml" \
    "Evidence contract: 1 complete / 1 total" \
    "Required fields: PASS" \
    "Stable finding ids: PASS" \
    "Trend values: PASS" \
    "Evidence contract required: YES" \
    "Evidence contract gate: PASS" \
    "Status: PASS"

# Case 4: critic CLEAN prose bait
run_case \
    "critic CLEAN prose bait (explicit ACCEPT wins, PASS)" \
    "ollama/score_output.py" \
    "critic-clean-bait-response.json" \
    "critic-clean-bait.metadata.yaml" \
    "Evidence contract: no findings declared" \
    "Verdict correct: YES" \
    "Status: PASS"

# Case 5: perspective HAS-BUGS
run_case \
    "perspective HAS-BUGS (must-find 1/1, PASS)" \
    "ollama/score_perspective.py" \
    "perspective-hasbugs-response.json" \
    "perspective-hasbugs.metadata.yaml" \
    "Must-find issues: 1/1" \
    "Status: PASS"

# Case 6: perspective CLEAN
run_case \
    "perspective CLEAN (verdict PASS, status PASS)" \
    "ollama/score_perspective.py" \
    "perspective-clean-response.json" \
    "perspective-clean.metadata.yaml" \
    "Verdict: PASS" \
    "Status: PASS"

# Case 7: planner (SECTION_KEYWORDS path — existing criteria)
run_case \
    "planner (score 3/3, PASS)" \
    "ollama/score_planner.py" \
    "planner-response.json" \
    "planner.metadata.yaml" \
    "Score: 3/3" \
    "Status: PASS"

# Case 8: planner scoring_keywords path — third criterion resolves via scoring_keywords only
run_case \
    "planner scoring_keywords criterion (aria-current detected)" \
    "ollama/score_planner.py" \
    "planner-response.json" \
    "planner.metadata.yaml" \
    '+ aria-current="page" on breadcrumb current item'

# Case 9: critic truncated response (must NOT pass)
run_case \
    "critic truncated <think> (INCOMPLETE, not PASS)" \
    "ollama/score_output.py" \
    "critic-truncated-response.json" \
    "critic-hasbugs.metadata.yaml" \
    "Status: INCOMPLETE"

# Case 10: perspective truncated response (must NOT pass)
run_case \
    "perspective truncated <think> (INCOMPLETE, not PASS)" \
    "ollama/score_perspective.py" \
    "perspective-truncated-response.json" \
    "perspective-hasbugs.metadata.yaml" \
    "Status: INCOMPLETE"

# Case 11: perspective hedged-clean response (PASS despite mentioning revise)
run_case \
    "perspective hedged-clean (Verdict: PASS despite hedged language)" \
    "ollama/score_perspective.py" \
    "perspective-hedged-clean-response.json" \
    "perspective-clean.metadata.yaml" \
    "Verdict: PASS" \
    "Status: PASS"

# Case 12: bug-report complete report (PASS incl. stable-ID verification)
run_case \
    "bugreport complete report (PASS, stable IDs verified)" \
    "ollama/score_bugreport.py" \
    "bugreport-good-response.json" \
    "bugreport-meta.yaml" \
    "Stable IDs: 2/2 verified" \
    "Status: PASS"

# Case 13: bug-report missing required field (FAIL, names the label)
run_case \
    "bugreport missing Severity row (FAIL)" \
    "ollama/score_bugreport.py" \
    "bugreport-missing-field-response.json" \
    "bugreport-meta.yaml" \
    "missing labels: Severity" \
    "Status: FAIL"

# Case 14: bug-report fabricated environment value (FAIL as fabrication)
run_case \
    "bugreport invented screen reader value (FABRICATION -> FAIL)" \
    "ollama/score_bugreport.py" \
    "bugreport-fabricated-response.json" \
    "bugreport-meta.yaml" \
    "FABRICATION: 'Screen reader'" \
    "Status: FAIL"

# Case 15: bug-report duplicate filing instead of dedup (count FAIL)
run_case \
    "bugreport two reports where dedup demands one (FAIL)" \
    "ollama/score_bugreport.py" \
    "bugreport-overreported-response.json" \
    "bugreport-meta.yaml" \
    "report count 2 != 1" \
    "Status: FAIL"

# Case 16: evaluation-report honest aggregation (PASS)
run_case \
    "evalreport honest aggregation (PASS)" \
    "ollama/score_evalreport.py" \
    "evalreport-good-response.json" \
    "evalreport-meta.yaml" \
    "Finding ids: 3/3 present, 0 invented" \
    "withholding language present" \
    "Status: PASS"

# Case 17: evaluation-report severity re-ranked while the NEXT finding line
# legitimately carries the expected token — regression guard for the
# truncated severity span (2026-08-01: untruncated window masked re-ranks)
run_case \
    "evalreport severity re-rank beside MINOR neighbor (FAIL)" \
    "ollama/score_evalreport.py" \
    "evalreport-severity-rerank-response.json" \
    "evalreport-meta.yaml" \
    "severity: a11y_icon_button_name not reported MINOR" \
    "Status: FAIL"

# Case 18: evaluation-report fabrications — never-evaluated criterion passed,
# invented finding id, environment token from no input stream
run_case \
    "evalreport fabrications: untested->passed, invented id, JAWS (FAIL)" \
    "ollama/score_evalreport.py" \
    "evalreport-fabricated-response.json" \
    "evalreport-meta.yaml" \
    "invented finding_id: a11y_ghost_finding" \
    "3.1.2 marked passed but nothing evaluated it" \
    "environment token never in input: JAWS" \
    "Status: FAIL"

# Case 19: evaluation-report assertive product-wide conformance claim (FAIL)
run_case \
    "evalreport assertive conformance claim (FAIL)" \
    "ollama/score_evalreport.py" \
    "evalreport-claim-response.json" \
    "evalreport-meta.yaml" \
    "assertive conformance claim: 'is WCAG 2.2 AA conformant'" \
    "Status: FAIL"

FIX="evals/suites/a11y-test-operation-evidence/fixtures"
OD_META="../a11y-test-operation-evidence/fixtures/op-dialog-escape-overreach.metadata.yaml"
OE_META="../a11y-test-operation-evidence/fixtures/op-empty-state-coverage-shortcuts.metadata.yaml"
OC_META="../a11y-test-operation-evidence/fixtures/op-retest-clean.metadata.yaml"
OM_META="../a11y-test-operation-evidence/fixtures/op-mixed-package-partial.metadata.yaml"
OH_META="../a11y-test-operation-evidence/fixtures/op-human-walkthrough-clean.metadata.yaml"
OS_META="../a11y-test-operation-evidence/fixtures/op-human-signature-only.metadata.yaml"
OP_SCORER="ollama/score_operation_evidence.py"

# Case 20: opevidence opdialog gold (PASS)
run_case "opevidence opdialog gold (PASS)" "$OP_SCORER" \
    "opevidence-opdialog-gold-response.json" "$OD_META" \
    "+ bounded_diagnostic_not_promoted under OP-CLOSE" \
    "+ setup_action_continuity under OP-CLOSE" "Status: PASS"

# Case 21: opevidence opdialog flip-admissibility (FAIL, wrong admissibility)
run_case "opevidence opdialog flip-admissibility (FAIL)" "$OP_SCORER" \
    "opevidence-opdialog-flip-admissibility-response.json" "$OD_META" \
    "admissibility: got 'ACCEPT', expected 'REJECT'" "Status: FAIL"

# Case 22: opevidence opdialog drop-diagnostic-rule (FAIL, missing rule under OP-CLOSE)
run_case "opevidence opdialog drop-diagnostic-rule (FAIL)" "$OP_SCORER" \
    "opevidence-opdialog-drop-diagnostic-rule-response.json" "$OD_META" \
    "rules_violated missing: bounded_diagnostic_not_promoted under OP-CLOSE" "Status: FAIL"

# Case 23: opevidence opdialog drop-continuity-rule (FAIL, missing rule under OP-CLOSE)
run_case "opevidence opdialog drop-continuity-rule (FAIL)" "$OP_SCORER" \
    "opevidence-opdialog-drop-continuity-rule-response.json" "$OD_META" \
    "rules_violated missing: setup_action_continuity under OP-CLOSE" "Status: FAIL"

# Case 24: opevidence opdialog ratify-phrase (FAIL, forbidden verdict phrase)
run_case "opevidence opdialog ratify-phrase (FAIL)" "$OP_SCORER" \
    "opevidence-opdialog-ratify-phrase-response.json" "$OD_META" \
    "forbidden verdict phrase: '2.1.2 FAIL confirmed'" "Status: FAIL"

# Case 25: opevidence opdialog close-blocked (FAIL, wrong disposition)
run_case "opevidence opdialog close-blocked (FAIL)" "$OP_SCORER" \
    "opevidence-opdialog-close-blocked-response.json" "$OD_META" \
    "disposition OP-CLOSE: got 'BLOCKED', expected 'UNTESTED'" "Status: FAIL"

# Case 26: opevidence opdialog reject-empty-rules (FAIL, REJECT with empty rules_violated)
run_case "opevidence opdialog reject-empty-rules (FAIL)" "$OP_SCORER" \
    "opevidence-opdialog-reject-empty-rules-response.json" "$OD_META" \
    "admissibility REJECT but rules_violated is empty" "Status: FAIL"

# Case 27: opevidence opdialog no-block (FAIL, no structured disposition block)
run_case "opevidence opdialog no-block (FAIL)" "$OP_SCORER" \
    "opevidence-opdialog-no-block-response.json" "$OD_META" \
    "no structured disposition block found" "Status: FAIL"

# Case 28: opevidence opempty gold (PASS)
run_case "opevidence opempty gold (PASS)" "$OP_SCORER" \
    "opevidence-opempty-gold-response.json" "$OE_META" \
    "+ natural_only_conditional_state under OP-EMPTY" \
    "+ passive_observation_binding under OP-OPTION" \
    "+ ancestor_remapping_review under OP-OPTION" "Status: PASS"

# Case 29: opevidence opempty flip-admissibility (FAIL)
run_case "opevidence opempty flip-admissibility (FAIL)" "$OP_SCORER" \
    "opevidence-opempty-flip-admissibility-response.json" "$OE_META" \
    "admissibility: got 'ACCEPT', expected 'REJECT'" "Status: FAIL"

# Case 30: opevidence opempty drop-natural-rule (FAIL, missing rule under OP-EMPTY)
run_case "opevidence opempty drop-natural-rule (FAIL)" "$OP_SCORER" \
    "opevidence-opempty-drop-natural-rule-response.json" "$OE_META" \
    "rules_violated missing: natural_only_conditional_state under OP-EMPTY" "Status: FAIL"

# Case 31: opevidence opempty drop-passive-rule (FAIL, missing rule under OP-OPTION)
run_case "opevidence opempty drop-passive-rule (FAIL)" "$OP_SCORER" \
    "opevidence-opempty-drop-passive-rule-response.json" "$OE_META" \
    "rules_violated missing: passive_observation_binding under OP-OPTION" "Status: FAIL"

# Case 32: opevidence opempty drop-ancestor-rule (FAIL, missing rule under OP-OPTION)
run_case "opevidence opempty drop-ancestor-rule (FAIL)" "$OP_SCORER" \
    "opevidence-opempty-drop-ancestor-rule-response.json" "$OE_META" \
    "rules_violated missing: ancestor_remapping_review under OP-OPTION" "Status: FAIL"

# Case 33: opevidence opempty op-empty-pass (FAIL, wrong disposition)
run_case "opevidence opempty op-empty-pass (FAIL)" "$OP_SCORER" \
    "opevidence-opempty-op-empty-pass-response.json" "$OE_META" \
    "disposition OP-EMPTY: got 'PASS', expected 'UNTESTED'" "Status: FAIL"

# Case 34: opevidence opempty forbidden-phrase (FAIL, forbidden verdict phrase)
run_case "opevidence opempty forbidden-phrase (FAIL)" "$OP_SCORER" \
    "opevidence-opempty-forbidden-phrase-response.json" "$OE_META" \
    "forbidden verdict phrase: 'OP-EMPTY COVERED'" "Status: FAIL"

# Case 35: opevidence opempty misattributed-rule (FAIL, rule under wrong operation)
run_case "opevidence opempty misattributed-rule (FAIL)" "$OP_SCORER" \
    "opevidence-opempty-misattributed-rule-response.json" "$OE_META" \
    "rules_violated missing: natural_only_conditional_state under OP-EMPTY" \
    "unexpected rule fired on OP-OPTION: natural_only_conditional_state" "Status: FAIL"

# Case 36: opevidence opclean gold (PASS, false-alarm control)
run_case "opevidence opclean gold (PASS)" "$OP_SCORER" \
    "opevidence-opclean-gold-response.json" "$OC_META" \
    "Rules violated: {}" "Status: PASS"

# Case 37: opevidence opclean invented-rule (FAIL, fabricated rule id)
run_case "opevidence opclean invented-rule (FAIL)" "$OP_SCORER" \
    "opevidence-opclean-invented-rule-response.json" "$OC_META" \
    "unknown rule id in rules_violated: evidence_staleness_check" "Status: FAIL"

# Case 38: opevidence opclean downgrade-close (FAIL, wrong disposition)
run_case "opevidence opclean downgrade-close (FAIL)" "$OP_SCORER" \
    "opevidence-opclean-downgrade-close-response.json" "$OC_META" \
    "disposition OP-CLOSE: got 'FAIL', expected 'PASS'" "Status: FAIL"

# Case 39: opevidence opclean downgrade-option (FAIL, wrong disposition)
run_case "opevidence opclean downgrade-option (FAIL)" "$OP_SCORER" \
    "opevidence-opclean-downgrade-option-response.json" "$OC_META" \
    "disposition OP-OPTION: got 'UNTESTED', expected 'PASS'" "Status: FAIL"

# Case 40: opevidence opclean op-empty-pass (FAIL, wrong disposition)
run_case "opevidence opclean op-empty-pass (FAIL)" "$OP_SCORER" \
    "opevidence-opclean-op-empty-pass-response.json" "$OC_META" \
    "disposition OP-EMPTY: got 'PASS', expected 'UNTESTED'" "Status: FAIL"

# Case 41: opevidence opclean false-fire-phrase (FAIL, forbidden verdict phrase)
run_case "opevidence opclean false-fire-phrase (FAIL)" "$OP_SCORER" \
    "opevidence-opclean-false-fire-phrase-response.json" "$OC_META" \
    "forbidden verdict phrase: 'promoted diagnostic'" "Status: FAIL"

# Case 42: opevidence opclean accept-with-rules (FAIL, ACCEPT with non-empty rules_violated)
run_case "opevidence opclean accept-with-rules (FAIL)" "$OP_SCORER" \
    "opevidence-opclean-accept-with-rules-response.json" "$OC_META" \
    "admissibility ACCEPT but rules_violated is not empty" "Status: FAIL"

# Case 43: opevidence opmixed gold (PASS, per-operation attribution)
run_case "opevidence opmixed gold (PASS)" "$OP_SCORER" \
    "opevidence-opmixed-gold-response.json" "$OM_META" \
    "+ passive_observation_binding under OP-OPTION" "Status: PASS"

# Case 44: opevidence opmixed rollback-close (FAIL, wrong disposition)
run_case "opevidence opmixed rollback-close (FAIL)" "$OP_SCORER" \
    "opevidence-opmixed-rollback-close-response.json" "$OM_META" \
    "disposition OP-CLOSE: got 'UNTESTED', expected 'PASS'" "Status: FAIL"

# Case 45: opevidence opmixed accept (FAIL, wrong admissibility)
run_case "opevidence opmixed accept (FAIL)" "$OP_SCORER" \
    "opevidence-opmixed-accept-response.json" "$OM_META" \
    "admissibility: got 'ACCEPT', expected 'REJECT'" "Status: FAIL"

# Case 46: opevidence opmixed option-pass (FAIL, wrong disposition)
run_case "opevidence opmixed option-pass (FAIL)" "$OP_SCORER" \
    "opevidence-opmixed-option-pass-response.json" "$OM_META" \
    "disposition OP-OPTION: got 'PASS', expected 'UNTESTED'" "Status: FAIL"

# Case 47: opevidence opmixed rule-on-close (FAIL, rule false-fired on admissible operation)
run_case "opevidence opmixed rule-on-close (FAIL)" "$OP_SCORER" \
    "opevidence-opmixed-rule-on-close-response.json" "$OM_META" \
    "rule fired on admissible operation OP-CLOSE: setup_action_continuity" "Status: FAIL"

# Case 48: opevidence opmixed boundary-omits-option (WARN, claim_boundary should-miss)
run_case "opevidence opmixed boundary-omits-option (WARN)" "$OP_SCORER" \
    "opevidence-opmixed-boundary-omits-option-response.json" "$OM_META" \
    "claim_boundary does not mention OP-OPTION" "Status: WARN"

# Case 49: opevidence truncated response (unclosed <think>) -> INCOMPLETE, not scored
run_case \
    "opevidence truncated response (INCOMPLETE)" \
    "ollama/score_operation_evidence.py" \
    "opevidence-opclean-truncated-response.json" \
    "../a11y-test-operation-evidence/fixtures/op-retest-clean.metadata.yaml" \
    "Status: INCOMPLETE"

# Case 50: opevidence over-flag — every rule fired on OP-CLOSE must FAIL (flag-everything is dead)
run_case "opevidence opdialog overflag (FAIL)" "$OP_SCORER" \
    "opevidence-opdialog-overflag-response.json" "$OD_META" \
    "unexpected rule fired on OP-CLOSE: natural_only_conditional_state" \
    "unexpected rule fired on OP-CLOSE: passive_observation_binding" \
    "unexpected rule fired on OP-CLOSE: ancestor_remapping_review" "Status: FAIL"

# Case 51: opevidence over-flag — every rule on both operations must FAIL
run_case "opevidence opempty overflag (FAIL)" "$OP_SCORER" \
    "opevidence-opempty-overflag-response.json" "$OE_META" \
    "unexpected rule fired on OP-EMPTY: bounded_diagnostic_not_promoted" \
    "unexpected rule fired on OP-OPTION: natural_only_conditional_state" "Status: FAIL"

# Case 52: opevidence unparseable block (unquoted claim_boundary with colons) -> distinct line, not "no block"
run_case "opevidence opclean unparseable block (FAIL, distinct line)" "$OP_SCORER" \
    "opevidence-opclean-unparseable-response.json" "$OC_META" \
    "disposition block present but not parseable YAML" "Status: FAIL"

# Case 53: opevidence should-tier hook_present path -> WARN, never FAIL
run_case "opevidence opdialog gold block, hookless prose (WARN)" "$OP_SCORER" \
    "opevidence-opdialog-no-hooks-response.json" "$OD_META" \
    "hook not mentioned for bounded_diagnostic_not_promoted" "Status: WARN"

# ── human-sourced walk-through packages (issue #57 Phase 2) ────────────────

# Case 65: opevidence ophumanclean gold (PASS, human-sourced false-alarm control)
run_case "opevidence ophumanclean gold (PASS)" "$OP_SCORER" \
    "opevidence-ophumanclean-gold-response.json" "$OH_META" \
    "Rules violated: {}" "Status: PASS"

# Case 66: opevidence ophumanclean trap — promoted diagnostic on OP-RETURN,
# OP-FLASH collapsed to UNTESTED instead of BLOCKED (FAIL)
run_case "opevidence ophumanclean trap (FAIL)" "$OP_SCORER" \
    "opevidence-ophumanclean-trap-response.json" "$OH_META" \
    "admissibility: got 'REJECT', expected 'ACCEPT'" \
    "disposition OP-FLASH: got 'UNTESTED', expected 'BLOCKED'" \
    "unexpected rule fired on OP-RETURN: bounded_diagnostic_not_promoted" "Status: FAIL"

# Case 67: opevidence ophumansig gold (PASS, per-operation attribution across
# one admissible operation and three under-specified signatures)
run_case "opevidence ophumansig gold (PASS)" "$OP_SCORER" \
    "opevidence-ophumansig-gold-response.json" "$OS_META" \
    "+ setup_action_continuity under OP-RETURN" \
    "+ passive_observation_binding under OP-AD" \
    "+ setup_action_continuity under OP-OPTION" \
    "+ passive_observation_binding under OP-OPTION" \
    "+ ancestor_remapping_review under OP-OPTION" \
    "+ passive_observation_binding under OP-LABEL" "Status: PASS"

# Case 68: opevidence ophumansig trap — accepts the whole signature-only
# package (FAIL)
run_case "opevidence ophumansig trap (FAIL)" "$OP_SCORER" \
    "opevidence-ophumansig-trap-response.json" "$OS_META" \
    "admissibility: got 'ACCEPT', expected 'REJECT'" \
    "disposition OP-RETURN: got 'PASS', expected 'UNTESTED'" "Status: FAIL"

# ── a11y-content-judgment scorer (wave-2 item #1, 2026-09-02) ──────────────
CJ_SCORER="ollama/score_content_judgment.py"
CJ_META="cj-meta.yaml"

# Case 54: cj gold (PASS)
run_case "cj gold (PASS)" "$CJ_SCORER" "cj-gold-response.json" "$CJ_META" \
    "Must-no rows (R1): 2/2 found" "false alarms: 0" "Status: PASS"

# Case 55: cj expected-no judged yes (FAIL, R1)
run_case "cj missed-no (FAIL)" "$CJ_SCORER" "cj-missed-no-response.json" "$CJ_META" \
    "R1 expected-no row TITLE-SM-0000000001 judged yes" "Status: FAIL"

# Case 56: cj expected-yes judged no (FAIL, R2 false alarm)
run_case "cj false-alarm (FAIL)" "$CJ_SCORER" "cj-false-alarm-response.json" "$CJ_META" \
    "R2 false alarm: expected-yes row LINK-SM-0000000003 judged no" "Status: FAIL"

# Case 57: cj metadata-listed fabricated token (FAIL, R4)
run_case "cj fabricated token (FAIL)" "$CJ_SCORER" "cj-fabricated-token-response.json" "$CJ_META" \
    "R4 fabricated token(s) in rationale/fix: LINK-SM-0000000002:Downtown Branch" "Status: FAIL"

# Case 58: cj one input id unanswered (FAIL, C1)
run_case "cj missing line (FAIL)" "$CJ_SCORER" "cj-missing-line-response.json" "$CJ_META" \
    "C1 missing output for 1 id(s): IDENT-SM-0000000004" "Status: FAIL"

# Case 59: cj judgment outside the enum (FAIL, C2)
run_case "cj bad enum (FAIL)" "$CJ_SCORER" "cj-bad-enum-response.json" "$CJ_META" \
    "C2 judgment outside {yes,no,unsure}" "Status: FAIL"

# Case 60: cj expected-yes judged unsure -> over-hedge is should-tier (WARN)
run_case "cj over-hedge (WARN)" "$CJ_SCORER" "cj-over-hedge-response.json" "$CJ_META" \
    "R2 over-hedge: expected-yes row(s) judged unsure (1)" "Status: WARN"

# Case 61: cj no-rationale without a loses phrase (WARN, R6)
run_case "cj loses miss (WARN)" "$CJ_SCORER" "cj-loses-miss-response.json" "$CJ_META" \
    "R6 no-rationale names none of the row's loses phrases" "Status: WARN"

# Case 62: cj quoted span absent from the row -> should-tier by calibration (WARN, R5)
run_case "cj quoted span (WARN)" "$CJ_SCORER" "cj-quoted-span-response.json" "$CJ_META" \
    "R5 quoted span(s) absent from the row (1)" "Status: WARN"

# Case 64: cj pattern group not unanimous (WARN, R7) — the gold's two clean rows form one group
run_case "cj split pattern group (WARN)" "$CJ_SCORER" "cj-split-group-response.json" "$CJ_META" \
    "R7 pattern_group 'clean-pair' not unanimous" "Status: WARN"

# Case 63: cj truncated response (INCOMPLETE, never PASS)
run_case "cj truncated (INCOMPLETE)" "$CJ_SCORER" "cj-truncated-response.json" "$CJ_META" \
    "Status: INCOMPLETE"

echo
echo "Results: $pass_count passed, $fail_count failed"
if [ "$fail_count" -gt 0 ]; then
    exit 1
fi

echo "ALL SMOKE TESTS PASSED"
