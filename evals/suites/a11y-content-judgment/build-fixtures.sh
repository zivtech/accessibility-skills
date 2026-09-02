#!/usr/bin/env bash
# Regenerate the a11y-content-judgment fixtures from their HTML sources by
# running the skill's OWN deterministic pipeline (content-inventory.mjs +
# build-judgment-rows.mjs) — the rows a judge is graded on are the rows the
# skill actually emits, flags and dedupe included. Reproduce-from-scratch
# (the `verify` skill pattern): playwright is a scratch install, never a repo
# dependency.
#
#   mkdir -p /tmp/cj-pw && cd /tmp/cj-pw && npm init -y && npm i playwright@1.57.0 \
#       && npx playwright install chromium
#   PW_DIR=/tmp/cj-pw bash evals/suites/a11y-content-judgment/build-fixtures.sh [fixture-id ...]
#
# Per fixture, sources/<id>/ holds: views.txt (view_id,product,/path.html per
# line), the *.html views, origin.txt (the fictional origin the rows are
# rewritten to), scenario.md (the blind author's product/audience note).
# The site is served on a FIXED origin (127.0.0.1:8765) because unit ids are
# content hashes over product|type|key where key includes the resolved URL —
# a different port would change every id. After the build the origin is
# rewritten to origin.txt for readability; ids are computed before the
# rewrite and are unchanged by it.
#
# Exit 1 if any fixture's deterministic block (metadata `deterministic:`)
# disagrees with what the pipeline emitted — that is the freeze guard: a
# changed source changes counts, and a changed count is a recorded event.
set -euo pipefail

SUITE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$SUITE/../../.." && pwd)"
REF="$REPO/.claude/skills/a11y-content-judgment/references"
PW_DIR="${PW_DIR:-/tmp/cj-pw}"
PORT=8765
ORIGIN_SERVED="http://127.0.0.1:$PORT"
test -d "$PW_DIR/node_modules/playwright" || { echo "playwright not found in $PW_DIR (see header)"; exit 2; }
# unit ids hash the served host:port — a taken port would silently re-id every
# row, and a stale server from the previous fixture would serve the WRONG
# directory (404 pages inventory as "Error response"; caught 2026-09-02).
port_free() { ! lsof -nP -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; }
wait_port_free() { for _ in $(seq 1 30); do port_free && return 0; sleep 0.2; done; return 1; }
port_free || { echo "port $PORT is in use; ids would change — stop that process first"; exit 2; }

ids=("$@")
if [ ${#ids[@]} -eq 0 ]; then
  ids=($(ls "$SUITE/sources"))
fi

fail=0
for id in "${ids[@]}"; do
  src="$SUITE/sources/$id"
  test -f "$src/views.txt" || { echo "$id: no sources/$id/views.txt"; fail=1; continue; }
  origin="$(tr -d '[:space:]' < "$src/origin.txt")"
  work="$(mktemp -d)"
  # absolute view list for the served site
  awk -F, -v o="$ORIGIN_SERVED" '/^#/||NF<3{next}{printf "%s,%s,%s%s%s\n",$1,$2,o,$3,(NF>3?","$4:"")}' "$src/views.txt" > "$work/views.txt"
  wait_port_free || { echo "$id: port $PORT still busy"; fail=1; continue; }
  ( cd "$src" && exec python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 ) &
  echo $! > "$work/server.pid"
  sleep 0.7
  # every view must come back 200 from THIS fixture's directory
  bad_views=0
  while IFS=, read -r vid prod url rest; do
    code=$(curl -s -o /dev/null -w '%{http_code}' "$url"); [ "$code" = "200" ] || { echo "$id: $vid -> HTTP $code for $url"; bad_views=1; }
  done < "$work/views.txt"
  [ "$bad_views" = 0 ] || { kill "$(cat "$work/server.pid")" 2>/dev/null; wait_port_free; fail=1; continue; }
  ( cd "$PW_DIR" \
    && node "$REF/content-inventory.mjs" --urls-file "$work/views.txt" --out "$work/inv" --settle 300 --no-screenshots >"$work/inventory.log" 2>&1 \
    && node "$REF/build-judgment-rows.mjs" --build --inventory "$work/inv" >"$work/build.log" 2>&1 \
    && node "$REF/build-judgment-rows.mjs" --merge --inventory "$work/inv" >"$work/merge.log" 2>&1 ) || { echo "$id: pipeline failed"; cat "$work"/*.log; kill "$(cat "$work/server.pid")"; fail=1; continue; }
  kill "$(cat "$work/server.pid")" 2>/dev/null || true
  wait_port_free || { echo "$id: server did not release port $PORT"; fail=1; continue; }
  grep -q '"title": "Error response"' "$work/inv/inventory-run.json" && { echo "$id: a view inventoried as an HTTP error page"; fail=1; continue; }
  mkdir -p "$src/build"
  host="${origin#*://}"
  sed -e "s#$ORIGIN_SERVED#$origin#g" -e "s#127\.0\.0\.1:$PORT#$host#g" "$work/inv/nav-consistency.csv" > "$src/build/nav-consistency.csv"
  cat "$work"/inv/batches/*.jsonl | sed -e "s#$ORIGIN_SERVED#$origin#g" -e "s#127\.0\.0\.1:$PORT#$host#g" > "$src/build/rows.jsonl"
  sed -e "s#$ORIGIN_SERVED#$origin#g" -e "s#127\.0\.0\.1:$PORT#$host#g" "$work/inv/judgment-units.json" > "$src/build/judgment-units.json"
  grep -h '"nav_error"' "$work/inv/inventory-run.json" | grep -v '"nav_error": null' && { echo "$id: navigation error in inventory (environment, not product)"; fail=1; }
  python3 "$SUITE/assemble_fixture.py" "$id" || fail=1
done
exit $fail
