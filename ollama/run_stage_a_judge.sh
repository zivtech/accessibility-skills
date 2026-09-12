#!/usr/bin/env bash
# Stage-A hosted-judge runner — SUBSCRIPTION ONLY (claude -p), NO metered API spend.
#
# Runs the a11y-critic protocol on each fixture in TWO arms:
#   blind          — fixture only (full protocol, no candidate list)
#   with-cands     — fixture + the qwen pre-sort candidate leads as an appendix
# and writes each arm's JSON (model result + token usage) to files, so M0
# (qwen value-add) and M1 (token/cost delta) can be scored afterward.
#
# WHY A SCRIPT YOU RUN ON YOUR DESKTOP: nested `claude -p` inside a Claude Code
# session hangs, and this repo's shell env has ANTHROPIC_API_KEY set (that path
# is metered $). This script `env -u ANTHROPIC_API_KEY`s each call so claude -p
# uses your claude.ai SUBSCRIPTION login instead. Run it from a normal terminal.
#
# Usage:
#   bash ollama/run_stage_a_judge.sh [fixture-id ...]      # defaults to the pilot set
#   DRY_RUN=1 bash ollama/run_stage_a_judge.sh             # print plan, write inputs, no claude calls
#   MODEL=opus QWEN_TAG=qwen3.6-35b bash ollama/run_stage_a_judge.sh
#
# Requires: qwen candidates already generated (ollama/presort_candidates.py) at
#   evals/results/qwen-presort/<fixture>-<QWEN_TAG>.json for each fixture.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$REPO_ROOT/.claude/skills/a11y-critic/SKILL.md"
FIXDIR="$REPO_ROOT/evals/suites/a11y-critic/fixtures"
CANDIR="$REPO_ROOT/evals/results/qwen-presort"
OUTDIR="$REPO_ROOT/evals/results/qwen-presort/stage-a"
MODEL="${MODEL:-opus}"
QWEN_TAG="${QWEN_TAG:-qwen3.6-35b}"
DRY_RUN="${DRY_RUN:-0}"
mkdir -p "$OUTDIR"

# Default pilot: spans name-role-state / focus-order / live-region + 2 CLEAN.
DEFAULT_PILOT=(accordion-no-region-role app-focus-order-illogical \
  async-retry-error-unannounced async-retry-recovery-clean \
  button-skip-link-clean trail-conditions-filter)
FIXTURES=("$@"); [ ${#FIXTURES[@]} -eq 0 ] && FIXTURES=("${DEFAULT_PILOT[@]}")

run_arm () {
  local fix="$1" arm="$2" infile="$3"
  local out="$OUTDIR/${fix}--${arm}--${MODEL}.json"
  echo "[$(date +%H:%M:%S)] $fix / $arm -> ${out#$REPO_ROOT/}"
  if [ "$DRY_RUN" = "1" ]; then
    echo "  DRY_RUN: would run: env -u ANTHROPIC_API_KEY claude -p (stdin=${infile#$REPO_ROOT/}) \\"
    echo "    --system-prompt-file <a11y-critic SKILL.md> --exclude-dynamic-system-prompt-sections \\"
    echo "    --disallowed-tools '*' --model $MODEL --output-format json"
    return 0
  fi
  env -u ANTHROPIC_API_KEY claude -p \
    --system-prompt-file "$SKILL" \
    --exclude-dynamic-system-prompt-sections \
    --disallowed-tools "Bash" "Read" "Edit" "Write" "Glob" "Grep" "WebFetch" "WebSearch" "Agent" \
    --model "$MODEL" \
    --output-format json < "$infile" > "$out" 2>"${out}.err" \
    && echo "  ok ($(wc -c <"$out") bytes)" \
    || { echo "  FAILED — see ${out}.err"; return 1; }
}

TMPD="$(mktemp -d)"; trap 'rm -rf "$TMPD"' EXIT
for fix in "${FIXTURES[@]}"; do
  comp="$FIXDIR/${fix}.md"
  cand="$CANDIR/${fix}-${QWEN_TAG}.json"
  [ -f "$comp" ] || { echo "SKIP $fix: no fixture at ${comp#$REPO_ROOT/}"; continue; }

  # Arm A — blind
  blind_in="$TMPD/${fix}.blind.txt"
  { printf 'Review this component using your full protocol. Output your findings.\n\n'; cat "$comp"; } > "$blind_in"
  run_arm "$fix" blind "$blind_in" || true

  # Arm B — with candidates (appendix, cross-check only)
  if [ -f "$cand" ]; then
    wc_in="$TMPD/${fix}.withcands.txt"
    { printf 'Review this component using your full protocol. Output your findings.\n\n';
      cat "$comp";
      printf '\n\n---\n## External candidate leads (from a local pre-sort detector — leads only, unverified; confirm or reject each with your own evidence, and note any real issue they missed)\n\n';
      cat "$cand"; } > "$wc_in"
    run_arm "$fix" with-cands "$wc_in" || true
  else
    echo "  NOTE $fix: no candidates at ${cand#$REPO_ROOT/} — run ollama/presort_candidates.py first; skipping with-cands arm"
  fi
done
echo "Done. Outputs in ${OUTDIR#$REPO_ROOT/}/  (one *.json per fixture-arm, with model result + token usage)."
