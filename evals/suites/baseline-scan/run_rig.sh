#!/usr/bin/env bash
# Baseline-scan regression rig.
#
# Proves the committed scanner (references/baseline-url-scan.mjs --census)
# still catches its known machine-detectable defect classes on a fresh
# synthetic target, and stays silent on a clean sibling built the same way.
# See expected-rules.json for the defect-class -> detector-id map, and
# README.md for what this rig does and does NOT prove.
#
# Peer deps (playwright + @axe-core/playwright) are NOT vendored in this
# repo — install them in your own project first:
#   npm install -D playwright @axe-core/playwright && npx playwright install chromium
#
# Run from repo root:
#   bash evals/suites/baseline-scan/run_rig.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SCANNER="$REPO_ROOT/.claude/skills/a11y-test/references/baseline-url-scan.mjs"
FIXTURES_DIR="$SCRIPT_DIR/fixtures"
EXPECTED_JSON="$SCRIPT_DIR/expected-rules.json"
PORT="${BASELINE_SCAN_RIG_PORT:-8934}"
OUT_DIR="$(mktemp -d)"

cleanup() {
    if [ -n "${SERVER_PID:-}" ]; then
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
    rm -rf "$OUT_DIR"
}
trap cleanup EXIT

python3 -m http.server "$PORT" --directory "$FIXTURES_DIR" > /dev/null 2>&1 &
SERVER_PID=$!

ready=0
for _ in $(seq 1 20); do
    if curl -sf -o /dev/null "http://localhost:$PORT/synthetic-target.html"; then
        ready=1
        break
    fi
    sleep 0.25
done
if [ "$ready" -ne 1 ]; then
    echo "FAIL: local fixture server on port $PORT never came up"
    exit 1
fi

node "$SCANNER" --census --out "$OUT_DIR" --viewports 1280x800 \
    "http://localhost:$PORT/synthetic-target.html" \
    "http://localhost:$PORT/clean-sibling.html"

export OUT_DIR EXPECTED_JSON
python3 - <<'PYEOF'
import glob
import json
import os
import sys

out_dir = os.environ["OUT_DIR"]
with open(os.environ["EXPECTED_JSON"]) as f:
    expected = json.load(f)

viewport_key = expected["scan_viewport"]


def load_page(index):
    matches = sorted(glob.glob(os.path.join(out_dir, f"{index:03d}-*.json")))
    if not matches:
        print(f"FAIL: no scanner output file for page index {index}")
        sys.exit(1)
    with open(matches[0]) as f:
        return json.load(f)["viewports"][viewport_key]


target = load_page(0)  # synthetic-target.html
clean = load_page(1)   # clean-sibling.html

failures = []
target_rule_ids = {v["id"] for v in target["violations"]}

expected_axe_ids = [d["id"] for d in expected["defect_classes"] if d["detector"] == "axe"]
expected_axe_ids += [r["id"] for r in expected.get("incidental_axe_rules", [])]
for rule_id in expected_axe_ids:
    if rule_id in target_rule_ids:
        print(f'PASS: target fired axe rule "{rule_id}"')
    else:
        failures.append(f'target did NOT fire expected axe rule "{rule_id}"')

for d in expected["defect_classes"]:
    if d["detector"] != "census":
        continue
    count = target["census"][d["id"]]["count"]
    if count >= d["min_count"]:
        print(f'PASS: target census "{d["id"]}" count={count} (>= {d["min_count"]})')
    else:
        failures.append(f'target census "{d["id"]}" count={count} below required minimum {d["min_count"]}')

if clean["violations"]:
    ids = ", ".join(v["id"] for v in clean["violations"])
    failures.append(f"clean-sibling has {len(clean['violations'])} axe violation(s), expected zero: {ids}")
else:
    print("PASS: clean-sibling has zero axe violations")

clean_census_total = sum(c["count"] for c in clean["census"].values())
if clean_census_total:
    failures.append(f"clean-sibling has {clean_census_total} census finding(s), expected zero")
else:
    print("PASS: clean-sibling has zero census findings")

print()
if failures:
    print(f"{len(failures)} FAILURE(S):")
    for failure in failures:
        print(f"  - {failure}")
    print()
    print("RIG: FAIL")
    sys.exit(1)

print("RIG: PASS")
PYEOF
