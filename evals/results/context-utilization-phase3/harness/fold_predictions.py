#!/usr/bin/env python3
"""Fold the opus adjudication verdicts into the lane's four registered
predictions (plan §6 / lane README §6, thresholds verbatim):

  P1  (local, dilution):  found(CURATED@40K) - found(DUMP@40K) >= +2 net
      adjudicated items across the local grid => real; |net| < 2 => null.
  P1b (local, fit):       |found(CURATED@32K) - found(CURATED@40K)| <= 1
      => holds (~=); a CURATED@32K deficit beyond 1 => num_ctx flag.
  P2  (hosted, harm-check): found(CURATED) >= found(DUMP) - 1 across all
      hosted cells => holds (CURATED loses <=1 net item).
  P3  (both, directional): REAL-FP on CLEAN under DUMP >= under CURATED.

Consumes verdicts-*.yaml (opus adjudicators) + the scorer's per-row miss
reasons (for the 4-bucket partition on adjudicated GENUINE-MISS items).
Emits adjudicated per-cell tables + prediction verdicts + draw-flip table.
"""
import glob
import json
import os
import re
from collections import defaultdict

import yaml

SCRATCH = os.path.dirname(os.path.abspath(__file__))
LANE = "/Users/AlexUA_1/claude/accessibility-skills/evals/results/context-utilization-phase3"

# ── load adjudications ───────────────────────────────────────────────────
found = defaultdict(int)          # (model, condition) -> adjudicated found items
per_draw = defaultdict(int)       # (model, condition, draw) -> found
items_flat = {}                   # (model, cond, fixture, item, draw) -> record
real_fp = defaultdict(int)        # (model, condition) -> REAL-FP count on CLEAN
misses = []                       # adjudicated GENUINE-MISS records
spurious = rephrased = 0
clean_verdict_wrong = defaultdict(int)

MODEL_NORM = {"qwen36-35b": "qwen3.6:35b", "qwen3-32b": "qwen3:32b",
              "qwen3.6:35b": "qwen3.6:35b", "qwen3:32b": "qwen3:32b",
              "opus": "opus", "sonnet": "sonnet"}

for path in sorted(glob.glob(os.path.join(SCRATCH, "adjudication", "verdicts-*.yaml"))):
    doc = yaml.safe_load(open(path))
    fid = doc["fixture_id"]
    for row in doc["rows"]:
        row["model"] = MODEL_NORM[row["model"]]
        key = (row["model"], row["condition"])
        for it in row.get("items") or []:
            rec = {"verdict": it["verdict"], "found": bool(it["adjudicated_found"])}
            items_flat[(row["model"], row["condition"], fid, it["item_index"], row["draw"])] = rec
            if rec["found"]:
                found[key] += 1
                per_draw[(row["model"], row["condition"], row["draw"])] += 1
            else:
                misses.append({"model": row["model"], "condition": row["condition"],
                                "fixture": fid, "item_index": it["item_index"],
                                "draw": row["draw"]})
            spurious += it["verdict"] == "SPURIOUS-MATCH"
            rephrased += it["verdict"] == "REPHRASED-FOUND"
        if doc.get("tier") == "CLEAN":
            real_fp[key] += row.get("real_fp_count") or 0
            if row.get("row_verdict_appropriate_for_clean") is False:
                clean_verdict_wrong[key] += 1

# ── miss partition (scorer reasons for adjudicated misses) ───────────────
CONDS = "curated-32k|curated-40k|dump-40k|curated-hosted|dump-hosted"
scorer_reason = {}
for txt_path in glob.glob(os.path.join(LANE, "scores", "score-*.txt")):
    txt = open(txt_path).read()
    brace = txt.find("\n{")
    if brace == -1:
        continue
    d = json.loads(txt[brace:])
    for ms in d.get("misses") or []:
        scorer_reason[(d["model"], d["condition"], d["fixture_id"],
                        ms["item_index"], d.get("draw"))] = ms.get("reason")
partition = defaultdict(lambda: defaultdict(int))
for ms in misses:
    reason = scorer_reason.get((ms["model"], ms["condition"], ms["fixture"],
                                 ms["item_index"], ms["draw"]), "model-miss")
    partition[(ms["model"], ms["condition"])][reason] += 1

# ── tables ───────────────────────────────────────────────────────────────
print("ADJUDICATED per-cell found totals (net items, both draws):")
print(f"{'model':<14} {'condition':<16} {'found':>5} {'d1':>3} {'d2':>3} {'REAL-FP':>8}  miss partition")
for key in sorted(set(list(found) + list(real_fp))):
    model, cond = key
    part = dict(partition.get(key, {}))
    print(f"{model:<14} {cond:<16} {found[key]:>5} {per_draw[(model, cond, 1)]:>3} "
          f"{per_draw[(model, cond, 2)]:>3} {real_fp.get(key, 0):>8}  {part or ''}")
print(f"\nscorer-vs-adjudication corrections: SPURIOUS-MATCH={spurious} REPHRASED-FOUND={rephrased}")
if clean_verdict_wrong:
    print(f"CLEAN rows with inappropriate verdicts: {dict(clean_verdict_wrong)}")

# ── draw-flip table (items that changed found-state between draws) ───────
flips = []
for (model, cond, fid, idx, draw), rec in items_flat.items():
    if draw != 1:
        continue
    other = items_flat.get((model, cond, fid, idx, 2))
    if other and other["found"] != rec["found"]:
        flips.append(f"{model}|{cond}|{fid}|item{idx}: d1={'F' if rec['found'] else 'miss'} d2={'F' if other['found'] else 'miss'}")
print(f"\ndraw flips ({len(flips)}):")
for f in flips:
    print(" ", f)

# ── predictions ──────────────────────────────────────────────────────────
local_models = ["qwen3.6:35b", "qwen3:32b"]
hosted_models = ["opus", "sonnet"]

p1_net = sum(found[(m, "curated-40k")] for m in local_models) - \
         sum(found[(m, "dump-40k")] for m in local_models)
p1 = "REAL (curation wins)" if p1_net >= 2 else ("NULL (variance band)" if p1_net > -2 else "REVERSED (dump wins by >=2)")

p1b_net = sum(found[(m, "curated-32k")] for m in local_models) - \
          sum(found[(m, "curated-40k")] for m in local_models)
p1b = "HOLDS (~=, |net|<=1)" if abs(p1b_net) <= 1 else f"VIOLATED (net {p1b_net:+d})"

p2_net = sum(found[(m, "curated-hosted")] for m in hosted_models) - \
         sum(found[(m, "dump-hosted")] for m in hosted_models)
p2 = "HOLDS (CURATED loses <=1)" if p2_net >= -1 else f"FAILS (CURATED loses {-p2_net})"

p3_local = (sum(real_fp[(m, "dump-40k")] for m in local_models),
            sum(real_fp[(m, "curated-40k")] for m in local_models))
p3_local_32k = sum(real_fp[(m, "curated-32k")] for m in local_models)
p3_hosted = (sum(real_fp[(m, "dump-hosted")] for m in hosted_models),
             sum(real_fp[(m, "curated-hosted")] for m in hosted_models))

print(f"""
=== REGISTERED PREDICTIONS (adjudicated) ===
P1  local dilution:   net(CURATED@40K - DUMP@40K) = {p1_net:+d}  -> {p1}
    per model: 35b {found[('qwen3.6:35b','curated-40k')]}-{found[('qwen3.6:35b','dump-40k')]}, 32b {found[('qwen3:32b','curated-40k')]}-{found[('qwen3:32b','dump-40k')]}
P1b local fit:        net(CURATED@32K - CURATED@40K) = {p1b_net:+d} -> {p1b}
    per model: 35b {found[('qwen3.6:35b','curated-32k')]}-{found[('qwen3.6:35b','curated-40k')]}, 32b {found[('qwen3:32b','curated-32k')]}-{found[('qwen3:32b','curated-40k')]}
P2  hosted harm-check: net(CURATED - DUMP) = {p2_net:+d} -> {p2}
    per model: opus {found[('opus','curated-hosted')]}-{found[('opus','dump-hosted')]}, sonnet {found[('sonnet','curated-hosted')]}-{found[('sonnet','dump-hosted')]}
P3  FP directional:   local DUMP@40K {p3_local[0]} vs CURATED@40K {p3_local[1]} -> {'consistent' if p3_local[0] >= p3_local[1] else 'AGAINST'} (CURATED@32K={p3_local_32k}, reported separately)
                      hosted DUMP {p3_hosted[0]} vs CURATED {p3_hosted[1]} -> {'consistent' if p3_hosted[0] >= p3_hosted[1] else 'AGAINST'}
""")

out = {"found": {f"{k[0]}|{k[1]}": v for k, v in found.items()},
       "per_draw": {f"{k[0]}|{k[1]}|d{k[2]}": v for k, v in per_draw.items()},
       "real_fp": {f"{k[0]}|{k[1]}": v for k, v in real_fp.items()},
       "miss_partition": {f"{k[0]}|{k[1]}": dict(v) for k, v in partition.items()},
       "corrections": {"spurious_match": spurious, "rephrased_found": rephrased},
       "flips": flips,
       "predictions": {"P1": {"net": p1_net, "verdict": p1},
                        "P1b": {"net": p1b_net, "verdict": p1b},
                        "P2": {"net": p2_net, "verdict": p2},
                        "P3": {"local_dump_vs_curated": p3_local, "hosted_dump_vs_curated": p3_hosted}}}
with open(os.path.join(LANE, "scores", "adjudicated-predictions.json"), "w") as f:
    json.dump(out, f, indent=1)
print(f"wrote {os.path.join(LANE, 'scores', 'adjudicated-predictions.json')}")
