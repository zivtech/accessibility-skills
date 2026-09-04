#!/usr/bin/env python3
"""Aggregate all Phase 3 evidence-lane score reports into (a) per-(model,
condition) candidate totals via score_evidence_lane.aggregate_by_condition,
(b) per-item flip table via per_item_rows, (c) an adjudication worksheet:
per (model, arm-comparison, fixture, item) found/missed across draws.
Re-scores from the row JSONs (deterministic) rather than parsing txt files.
Output: aggregate.json + a printed summary table."""
import glob
import json
import os
import re
import sys
from collections import defaultdict

REPO = "/Users/AlexUA_1/claude/accessibility-skills"
LANE = os.path.join(REPO, "evals/results/context-utilization-phase3")
sys.path.insert(0, os.path.join(REPO, "ollama"))
from score_evidence_lane import (  # noqa: E402
    DEFAULT_MANIFEST, aggregate_by_condition, load_manifest, per_item_rows,
    resolve_fixture_config, resolve_repo_path, score_row, load_keyword_overrides,
)

CONDITIONS = {
    "curated-32k": "CURATED", "curated-40k": "CURATED", "dump-40k": "DUMP",
    "overflow-32k": "DUMP", "curated-hosted": "CURATED", "dump-hosted": "DUMP",
}
NAME_RE = re.compile(
    rf"^(?:ollama|claude)-evidence-lane-(?P<fixture>.+)-(?P<cond>{'|'.join(CONDITIONS)})"
    rf"-draw(?P<draw>\d+)-(?P<model>[A-Za-z0-9.-]+)-response\.json$"
)

manifest = load_manifest(DEFAULT_MANIFEST)
rows = []
for row_path in sorted(glob.glob(os.path.join(LANE, "rows", "*.json"))
                       + glob.glob(os.path.join(LANE, "rows-hosted", "*.json"))):
    m = NAME_RE.match(os.path.basename(row_path))
    if not m:
        continue
    fx = resolve_fixture_config(manifest, m["fixture"])
    result = score_row(
        row_path, resolve_repo_path(fx["metadata_path"]),
        m["cond"], CONDITIONS[m["cond"]],
        completeness_audit_path=resolve_repo_path(fx.get("completeness_audit_path")),
        keyword_overrides=load_keyword_overrides(fx), draw=int(m["draw"]),
    )
    rows.append(result)

agg = aggregate_by_condition(rows)
items = per_item_rows(rows)

# Adjudication worksheet: (model, condition, fixture, item) -> per-draw found
worksheet = defaultdict(list)
for row in rows:
    if row.get("invalid"):
        continue
    found_idx = {m["item_index"] for m in (row.get("must_find") or {}).get("matched", [])}
    all_items = ({m["item_index"] for m in (row.get("must_find") or {}).get("matched", [])}
                 | {ms["item_index"] for ms in row.get("misses") or []})
    for idx in sorted(all_items):
        worksheet[(row["model"], row["condition"], row["fixture_id"], idx)].append({
            "draw": row.get("draw"), "found": idx in found_idx,
            "miss_reason": next((ms.get("reason") for ms in row.get("misses") or []
                                 if ms["item_index"] == idx), None),
        })

out = {
    "aggregate_by_model_condition": {f"{k[0]}|{k[1]}": v for k, v in sorted(agg.items())},
    "per_item": [{"key": "|".join(map(str, r["key"])), "found": r["found"],
                   "reason": r["reason"]} for r in items],
    "adjudication_worksheet": {"|".join(map(str, k)): v for k, v in sorted(worksheet.items())},
    "row_count": len(rows),
}
out_path = os.path.join(LANE, "scores", "aggregate.json")
with open(out_path, "w") as f:
    json.dump(out, f, indent=1)

print(f"rows={len(rows)} -> {out_path}\n")
print(f"{'model':<14} {'condition':<16} {'matched':>7} {'possible':>8} {'fp':>3} {'rows':>4} {'invalid':>7}")
for (model, cond), v in sorted(agg.items()):
    print(f"{model:<14} {cond:<16} {v['matched']:>7} {v['possible']:>8} {v['fp']:>3} {v['rows']:>4} {v['invalid_rows']:>7}")
