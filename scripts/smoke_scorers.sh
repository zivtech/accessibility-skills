#!/usr/bin/env bash
# Smoke tests for the three scorer scripts.
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
            break
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

# Case 2: critic CLEAN
run_case \
    "critic CLEAN (verdict correct, PASS)" \
    "ollama/score_output.py" \
    "critic-clean-response.json" \
    "critic-clean.metadata.yaml" \
    "Verdict correct: YES" \
    "Status: PASS"

# Case 3: perspective HAS-BUGS
run_case \
    "perspective HAS-BUGS (must-find 1/1, PASS)" \
    "ollama/score_perspective.py" \
    "perspective-hasbugs-response.json" \
    "perspective-hasbugs.metadata.yaml" \
    "Must-find issues: 1/1" \
    "Status: PASS"

# Case 4: perspective CLEAN
run_case \
    "perspective CLEAN (verdict PASS, status PASS)" \
    "ollama/score_perspective.py" \
    "perspective-clean-response.json" \
    "perspective-clean.metadata.yaml" \
    "Verdict: PASS" \
    "Status: PASS"

# Case 5: planner (SECTION_KEYWORDS path — existing criteria)
run_case \
    "planner (score 3/3, PASS)" \
    "ollama/score_planner.py" \
    "planner-response.json" \
    "planner.metadata.yaml" \
    "Score: 3/3" \
    "Status: PASS"

# Case 9: planner scoring_keywords path — third criterion resolves via scoring_keywords only
run_case \
    "planner scoring_keywords criterion (aria-current detected)" \
    "ollama/score_planner.py" \
    "planner-response.json" \
    "planner.metadata.yaml" \
    '+ aria-current="page" on breadcrumb current item'

# Case 6: critic truncated response (must NOT pass)
run_case \
    "critic truncated <think> (INCOMPLETE, not PASS)" \
    "ollama/score_output.py" \
    "critic-truncated-response.json" \
    "critic-hasbugs.metadata.yaml" \
    "Status: INCOMPLETE"

# Case 7: perspective truncated response (must NOT pass)
run_case \
    "perspective truncated <think> (INCOMPLETE, not PASS)" \
    "ollama/score_perspective.py" \
    "perspective-truncated-response.json" \
    "perspective-hasbugs.metadata.yaml" \
    "Status: INCOMPLETE"

# Case 8: perspective hedged-clean response (PASS despite mentioning revise)
run_case \
    "perspective hedged-clean (Verdict: PASS despite hedged language)" \
    "ollama/score_perspective.py" \
    "perspective-hedged-clean-response.json" \
    "perspective-clean.metadata.yaml" \
    "Verdict: PASS" \
    "Status: PASS"

echo
echo "Results: $pass_count passed, $fail_count failed"
if [ "$fail_count" -gt 0 ]; then
    exit 1
fi

echo "ALL SMOKE TESTS PASSED"
