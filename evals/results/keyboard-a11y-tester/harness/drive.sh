#!/bin/bash
# Drive one keyboard-a11y-tester serve session with a fixed keystroke plan.
# Usage: drive.sh <fixture-id> <port> <goal> <step...>
# where each step is "press:Tab", "press:Enter", "type:some text", or "observe"
set -u
KAT=/private/tmp/claude-501/-Users-AlexUA-1-claude-a11y-meta-skills/083549b3-a213-4de3-865a-02c09d7d8a7a/scratchpad/keyboard-a11y-tester
BASE=/private/tmp/claude-501/-Users-AlexUA-1-claude-a11y-meta-skills/083549b3-a213-4de3-865a-02c09d7d8a7a/scratchpad/kat-eval
FID="$1"; PORT="$2"; GOAL="$3"; shift 3
OUT="$BASE/driven/$FID"
rm -rf "$OUT"; mkdir -p "$OUT"

cd "$KAT"
nohup node scripts/runner.mjs serve --url "http://127.0.0.1:8777/$FID.html" \
  --goal "$GOAL" --viewport desktop --port "$PORT" --out "$OUT" > "$OUT/serve.log" 2>&1 &
SERVE_PID=$!
for i in $(seq 1 40); do grep -q READY "$OUT/serve.log" && break; sleep 0.5; done
SESSION=$(grep READY "$OUT/serve.log" | awk '{print $2}')
if [ -z "${SESSION:-}" ]; then echo "FAILED to start: $FID"; cat "$OUT/serve.log"; exit 1; fi
echo "### $FID session: $SESSION"

n=0
summarize() {
  python3 -c "
import json, sys
try:
    o = json.load(sys.stdin)
except Exception as e:
    print('   (unparseable observation)'); sys.exit(0)
f = o.get('focused') or {}
sr = o.get('sr_announcement') or {}
live = sr.get('live_announcements') or []
states = f.get('states') or {}
compact = {k: v for k, v in states.items() if k in ('expanded','pressed','selected','hidden','modal')}
print(f\"  [{sys.argv[1]}] focused={f.get('name')!r}/{f.get('role')} moved={o.get('focus_moved')} states={compact} url_frag={str(o.get('url',''))[-20:]}\")
for l in live: print(f'      LIVE: {l}')
" "$1"
}

node scripts/runner.mjs observe "$SESSION" | summarize "observe"
for step in "$@"; do
  n=$((n+1))
  kind="${step%%:*}"; val="${step#*:}"
  case "$kind" in
    press)   node scripts/runner.mjs step "$SESSION" --press "$val" | tee "$OUT/step_$n.json" | summarize "$val" ;;
    type)    node scripts/runner.mjs step "$SESSION" --type "$val" | tee "$OUT/step_$n.json" | summarize "type" ;;
    observe) node scripts/runner.mjs observe "$SESSION" | summarize "observe" ;;
    wait)    sleep "$val"; echo "  [wait ${val}s]" ;;
  esac
done
node scripts/runner.mjs finish "$SESSION" > "$OUT/finish.log" 2>&1
node scripts/runner.mjs stop "$SESSION" >> "$OUT/finish.log" 2>&1
wait $SERVE_PID 2>/dev/null
echo "  finished -> $OUT"
