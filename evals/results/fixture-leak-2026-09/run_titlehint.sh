#!/bin/bash
# Issue #51 step 2: does the defect-naming H1 move must-find detection?
# 9 maximum-leak fixtures (every content word the title drops appears verbatim
# in a must_find description) x {titled, neutral} x 5 draws = 90 draws.
set -u
cd /Users/AlexUA_1/claude/accessibility-skills-fixture-leak
export BENCHMARK_RESULTS_DIR=/private/tmp/claude-501/-Users-AlexUA-1-claude-accessibility-skills/da5005d3-32a1-4f08-9e8b-02ac3d2761e6/scratchpad/titlehint
mkdir -p "$BENCHMARK_RESULTS_DIR"
export OLLAMA_URL=http://127.0.0.1:11435/api/generate   # dedicated server — claude-smart shares :11434
MODEL=qwen3.6:35b
FIXTURES=(
  combobox-autocomplete-no-listbox-role
  expandable-section-no-button
  image-carousel-no-region
  infinite-scroll-no-announcement
  toast-notification-no-role
  pagination-no-nav-landmark
  video-player-missing-captions
  breadcrumb-navigation-no-nav-landmark
  checkbox-group-no-fieldset
)
n=0
for draw in 1 2 3 4 5; do
  for f in "${FIXTURES[@]}"; do
    for cond in titled neutral; do
      out="$BENCHMARK_RESULTS_DIR/ollama-titlehint-$cond-$f-qwen36-35b-d$draw-response.json"
      n=$((n+1))
      if [ -f "$out" ]; then echo "[$n/90] skip $cond $f d$draw"; continue; fi
      echo "[$n/90] $cond $f d$draw"
      python3 ollama/run_benchmark.py titlehint "$MODEL" "$f" "$cond" "$draw" >/dev/null 2>>"$BENCHMARK_RESULTS_DIR/errors.log" \
        || echo "  DRAW FAILED: $cond $f d$draw"
    done
  done
done
echo "ALL DRAWS COMPLETE"
