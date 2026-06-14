#!/usr/bin/env bash
# Smoke tests for the chain-eval scorer (plan 011).
# Run from repo root: bash scripts/smoke_chain.sh
# Two layers:
#   1. Function unit tests  (test_score_chain.py) — parse/score/peek logic in isolation.
#   2. Integration re-score  — runs score_chain.py against the 3 PRISTINE pilot captures
#      (operator zones split per I9) and asserts the proposal-critic's gate criteria:
#        login un-flagged · video flagged (paraphrased peek) · modal PASS.
#   The integration layer is the real instrument check; the unit layer guards the pieces.
# Exits 1 on any failed assertion.
set -euo pipefail

CHAIN="evals/suites/chain"
PILOT="$CHAIN/pilot"
pass=0
fail=0

# --- layer 1: function unit tests -----------------------------------------------------
echo "== chain scorer unit tests =="
if python3 "$CHAIN/test_score_chain.py" >/tmp/chain_units.out 2>&1; then
    echo "PASS: $(tail -1 /tmp/chain_units.out)"
    pass=$((pass + 1))
else
    echo "FAIL: unit tests"; cat /tmp/chain_units.out; fail=$((fail + 1))
fi

# --- layer 2: integration re-score of the 3 pristine pilot captures -------------------
# assert_has  <label> <fixture> <substring...>   : every substring MUST appear
# assert_lacks <label> <fixture> <substring>     : substring MUST NOT appear
score() { python3 "$CHAIN/score_chain.py" "$1" "$PILOT/$1" 2>&1; }

assert_has() {
    local label="$1" fixture="$2"; shift 2
    local out; out=$(score "$fixture")
    for s in "$@"; do
        if ! echo "$out" | grep -qF "$s"; then
            echo "FAIL: $label"; echo "  missing: $s"; echo "--- output ---"; echo "$out"
            fail=$((fail + 1)); return
        fi
    done
    echo "PASS: $label"; pass=$((pass + 1))
}

assert_lacks() {
    local label="$1" fixture="$2" s="$3"
    local out; out=$(score "$fixture")
    if echo "$out" | grep -qF "$s"; then
        echo "FAIL: $label"; echo "  unexpected: $s"; echo "--- output ---"; echo "$out"
        fail=$((fail + 1)); return
    fi
    echo "PASS: $label"; pass=$((pass + 1))
}

echo
echo "== chain integration: re-score 3 pristine captures (the real gate) =="
# login: the operator zone (which quotes the answer key) must be stripped -> NOT contaminated.
assert_lacks "login un-flagged (no false contamination)" "login-form-clean" "CONTAMINATED"
# video: agent paraphrased the rubric, so detect_peek is silent; the operator peek flag must fire.
assert_has  "video flagged via operator integrity flag" "video-tutorial-no-captions" \
    "CONTAMINATED" "operator integrity flag"
# modal: clean blind run -> passes on the mechanical sub-scores.
assert_has  "modal PASS (clean baseline)" "modal-broken-focus-trap" "PASS: True"

echo
echo "Results: $pass passed, $fail failed"
[ "$fail" -gt 0 ] && exit 1
echo "ALL CHAIN SMOKE TESTS PASSED"
