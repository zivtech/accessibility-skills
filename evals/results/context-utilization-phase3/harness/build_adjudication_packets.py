#!/usr/bin/env python3
"""Build per-fixture adjudication packets for the Phase 3 evidence-lane opus
adjudication pass. One packet per fixture: ground-truth must-find items +
lane keywords + completeness audit summary, then every scored row (overflow
receipts excluded) with the scorer's candidate/miss/FP summary and the
model's full response text. Adjudicators ARE allowed ground truth (unlike
row-producing models)."""
import glob
import json
import os
import re
import sys

import yaml

REPO = "/Users/AlexUA_1/claude/accessibility-skills"
LANE = os.path.join(REPO, "evals/results/context-utilization-phase3")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adjudication")
sys.path.insert(0, os.path.join(REPO, "ollama"))
from score_evidence_lane import (  # noqa: E402
    DEFAULT_MANIFEST, load_manifest, resolve_repo_path,
)
from score_common import strip_thinking  # noqa: E402

CONDITIONS = ["curated-32k", "curated-40k", "dump-40k", "curated-hosted", "dump-hosted"]
NAME_RE = re.compile(
    rf"^(?:ollama|claude)-evidence-lane-(?P<fixture>.+)-(?P<cond>{'|'.join(CONDITIONS)})"
    rf"-draw(?P<draw>\d+)-(?P<model>[A-Za-z0-9.-]+)-response\.json$"
)

os.makedirs(OUT, exist_ok=True)
manifest = load_manifest(DEFAULT_MANIFEST)

rows_by_fixture = {}
for row_path in sorted(glob.glob(os.path.join(LANE, "rows", "*.json"))
                       + glob.glob(os.path.join(LANE, "rows-hosted", "*.json"))):
    m = NAME_RE.match(os.path.basename(row_path))
    if not m:
        continue  # overflow receipts and unrelated files
    rows_by_fixture.setdefault(m["fixture"], []).append((m, row_path))

for fx in manifest["fixtures"]:
    fid = fx["fixture_id"]
    meta = yaml.safe_load(open(resolve_repo_path(fx["metadata_path"])))
    score_dir = os.path.join(LANE, "scores")
    parts = [f"# Adjudication packet — fixture `{fid}` (tier: {fx.get('tier')})\n"]
    parts.append("## Ground truth (fixture metadata — authoritative)\n")
    parts.append("```yaml\n" + yaml.safe_dump(meta, sort_keys=False) + "```\n")
    parts.append("## Lane must-find keyword overrides (what the rule-based scorer matched on)\n")
    parts.append("```yaml\n" + yaml.safe_dump({"must_find_keywords": fx.get("must_find_keywords", [])}, sort_keys=False) + "```\n")
    audit_path = resolve_repo_path(fx.get("completeness_audit_path"))
    if audit_path and os.path.exists(audit_path):
        parts.append("## Pack completeness audit (evidence presence per payload — for miss partition)\n")
        parts.append("```yaml\n" + open(audit_path).read() + "```\n")
    for m, row_path in rows_by_fixture.get(fid, []):
        stem = os.path.basename(row_path)[:-len("-response.json")]
        row = json.load(open(row_path))
        score_txt_path = os.path.join(score_dir, f"score-{stem}.txt")
        score_json = {}
        if os.path.exists(score_txt_path):
            txt = open(score_txt_path).read()
            brace = txt.find("\n{")
            if brace != -1:
                score_json = json.loads(txt[brace:])
        summary = {
            "matched_candidates": [
                {"item_index": c["item_index"], "evidence_quote": c.get("evidence_quote")}
                for c in (score_json.get("must_find") or {}).get("matched", [])],
            "misses": score_json.get("misses"),
            "false_positive_candidates": score_json.get("false_positives"),
        }
        response, think_truncated = strip_thinking(row.get("response", ""))
        if think_truncated:
            response = "[WARNING: unclosed <think> block — response truncated mid-reasoning]\n\n" + response
        parts.append(f"\n---\n\n## ROW {stem}\n")
        parts.append(f"model={m['model']} condition={m['cond']} draw={m['draw']}\n")
        parts.append("### Scorer candidate summary (rule-based, to be adjudicated)\n")
        parts.append("```json\n" + json.dumps(summary, indent=1) + "\n```\n")
        parts.append("### Full model response\n")
        parts.append("````\n" + response + "\n````\n")
    out_path = os.path.join(OUT, f"packet-{fid}.md")
    with open(out_path, "w") as f:
        f.write("\n".join(parts))
    print(f"{out_path}: {os.path.getsize(out_path)}B, rows={len(rows_by_fixture.get(fid, []))}")
