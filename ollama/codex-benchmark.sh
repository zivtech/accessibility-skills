#!/usr/bin/env bash
# Run the a11y-critic benchmark from Codex.
#
# Usage (from inside Codex):
#   bash ollama/codex-benchmark.sh                    # Escalation: cheapest GPT tier first
#   bash ollama/codex-benchmark.sh single 5.2 <fixture-id>  # Single fixture, specific tier
#   bash ollama/codex-benchmark.sh all 5.2            # All 33 fixtures, one tier
#   bash ollama/codex-benchmark.sh score              # Score all Codex results
#
# Tiers: 5.2, 5.2-low, 5.5, 5.5-low

set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo "$(dirname "$0")/..")"

CMD="${1:-escalate}"

case "$CMD" in
  escalate)
    echo "Running Codex escalation benchmark (33 critic fixtures, bottom-up)..."
    python3 ollama/run_cloud_benchmark.py codex-escalate
    ;;
  single)
    TIER="${2:?Usage: codex-benchmark.sh single <tier> <fixture-id>}"
    FIXTURE="${3:?Usage: codex-benchmark.sh single <tier> <fixture-id>}"
    python3 ollama/run_cloud_benchmark.py codex "$TIER" "$FIXTURE"
    ;;
  all)
    TIER="${2:?Usage: codex-benchmark.sh all <tier>}"
    python3 ollama/run_cloud_benchmark.py codex-all "$TIER"
    ;;
  score)
    python3 ollama/run_cloud_benchmark.py score-codex
    ;;
  perspective)
    echo "Running Codex perspective-audit escalation..."
    python3 ollama/run_cloud_benchmark.py codex-escalate --skill perspective
    ;;
  summary)
    python3 ollama/run_cloud_benchmark.py summary
    ;;
  *)
    echo "Unknown command: $CMD"
    echo "Usage: codex-benchmark.sh [escalate|single|all|score|perspective|summary]"
    exit 1
    ;;
esac
