#!/bin/bash
# Issue #51 leak class 2: does the features section hold up the CLEAN verdicts?
# Waits for the title-hint run to finish, then draws:
#   11 CLEAN fixtures  x {withfeatures,nofeatures} x 5 = 110  (measurement)
#    9 max-leak BUG    x {withfeatures,nofeatures} x 3 =  54  (must-find control)
set -u
S=/private/tmp/claude-501/-Users-AlexUA-1-claude-accessibility-skills/da5005d3-32a1-4f08-9e8b-02ac3d2761e6/scratchpad
cd /Users/AlexUA_1/claude/accessibility-skills-fixture-leak
export BENCHMARK_RESULTS_DIR=$S/featurehint
mkdir -p "$BENCHMARK_RESULTS_DIR"
export OLLAMA_URL=http://127.0.0.1:11435/api/generate   # dedicated server — claude-smart shares :11434
MODEL=qwen3.6:35b

echo "waiting for the title-hint run to finish..."
while ! grep -q "ALL DRAWS COMPLETE" "$S/titlehint.log" 2>/dev/null; do sleep 30; done
echo "title-hint done at $(date +%H:%M:%S); starting features lane"

CLEAN=(button-skip-link-clean interactive-dropdown-clean modal-complete-clean
       search-results-dynamic-clean trail-conditions-filter pool-lesson-registration
       composite-descendant-clean async-retry-recovery-clean map-controls-clean
       paired-id-name-columns-clean spa-route-change-clean)
BUGS=(combobox-autocomplete-no-listbox-role expandable-section-no-button
      image-carousel-no-region infinite-scroll-no-announcement toast-notification-no-role
      pagination-no-nav-landmark video-player-missing-captions
      breadcrumb-navigation-no-nav-landmark checkbox-group-no-fieldset)

draw_set () {  # $1 = draws, then fixture ids
  local draws=$1; shift
  for d in $(seq 1 "$draws"); do
    for f in "$@"; do
      for c in withfeatures nofeatures; do
        out="$BENCHMARK_RESULTS_DIR/ollama-featurehint-$c-$f-qwen36-35b-d$d-response.json"
        [ -f "$out" ] && { echo "skip $c $f d$d"; continue; }
        echo "$(date +%H:%M:%S) $c $f d$d"
        python3 ollama/run_benchmark.py featurehint "$MODEL" "$f" "$c" "$d" >/dev/null 2>>"$BENCHMARK_RESULTS_DIR/errors.log" \
          || echo "  DRAW FAILED: $c $f d$d"
      done
    done
  done
}

echo "--- CLEAN arm (110 draws) ---"
draw_set 5 "${CLEAN[@]}"
echo "--- BUG control arm (54 draws) ---"
draw_set 3 "${BUGS[@]}"
echo "ALL FEATURE DRAWS COMPLETE"
