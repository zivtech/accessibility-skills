#!/usr/bin/env python3
"""Score every Phase 3 evidence-lane row (local rows/ + hosted rows-hosted/)
with ollama/score_evidence_lane.py, writing score-<stem>.txt next to a
scores/ dir under the lane results dir. Idempotent: skips stems whose score
file already exists unless --force. Filename is the routing source — the
same (fixture, condition, draw) the runner/wrapper encoded."""
import glob
import os
import re
import subprocess
import sys

REPO = "/Users/AlexUA_1/claude/accessibility-skills"
LANE = os.path.join(REPO, "evals/results/context-utilization-phase3")
SCORES = os.path.join(LANE, "scores")
CONDITIONS = {
    "curated-32k": "CURATED", "curated-40k": "CURATED", "dump-40k": "DUMP",
    "overflow-32k": "DUMP", "curated-hosted": "CURATED", "dump-hosted": "DUMP",
}
COND_ALT = "|".join(CONDITIONS)
NAME_RE = re.compile(
    rf"^(?:ollama|claude)-evidence-lane-(?P<fixture>.+)-(?P<cond>{COND_ALT})"
    rf"-draw(?P<draw>\d+)-(?P<model>[A-Za-z0-9.-]+)-response\.json$"
)

os.makedirs(SCORES, exist_ok=True)
force = "--force" in sys.argv
rows = sorted(glob.glob(os.path.join(LANE, "rows", "*.json"))
              + glob.glob(os.path.join(LANE, "rows-hosted", "*.json")))
ok = fail = skipped = 0
failures = []
for row_path in rows:
    base = os.path.basename(row_path)
    m = NAME_RE.match(base)
    if not m:
        print(f"UNRECOGNIZED name, skipping: {base}")
        continue
    stem = base[:-len("-response.json")]
    out_path = os.path.join(SCORES, f"score-{stem}.txt")
    if os.path.exists(out_path) and not force:
        skipped += 1
        continue
    cmd = [
        "python3", os.path.join(REPO, "ollama", "score_evidence_lane.py"), row_path,
        "--fixture-id", m["fixture"], "--condition", m["cond"],
        "--payload", CONDITIONS[m["cond"]], "--draw", m["draw"],
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    body = proc.stdout + (("\n[stderr]\n" + proc.stderr) if proc.stderr.strip() else "")
    with open(out_path + ".tmp", "w") as f:
        f.write(body)
    os.replace(out_path + ".tmp", out_path)
    if proc.returncode == 0:
        ok += 1
    else:
        fail += 1
        failures.append((base, proc.returncode))
print(f"scored={ok} failed={fail} skipped(existing)={skipped} of {len(rows)} rows")
for base, rc in failures:
    print(f"  FAIL rc={rc}: {base}")
