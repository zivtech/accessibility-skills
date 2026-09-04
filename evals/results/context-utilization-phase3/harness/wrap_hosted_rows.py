#!/usr/bin/env python3
"""Wrap hosted-arm subagent .md responses into the lane's -response.json row
shape (same _benchmark conventions as acr-reporting-phase2's claude-subagent
rows + this lane's own additions: condition/payload/draw/prompt hashes/pack
meta from the composed-prompt meta JSONs). Idempotent: skips rows whose JSON
already exists unless --force. The .md files are kept (verbatim source)."""
import glob
import json
import os
import re
import sys
import time

REPO = "/Users/AlexUA_1/claude/accessibility-skills"
ROWS = os.path.join(REPO, "evals/results/context-utilization-phase3/rows-hosted")
META_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hosted")
NAME_RE = re.compile(
    r"^claude-evidence-lane-(?P<fixture>.+)-(?P<cond>curated-hosted|dump-hosted)"
    r"-draw(?P<draw>\d+)-(?P<model>opus|sonnet)-response\.md$"
)
METHOD = ("Phase 3 evidence-volume lane, hosted arm: Agent(subagent_type=general-purpose, "
          "model={model}) spawned depth-1 from the main session; subagent read exactly two "
          "staged files — the frontmatter-stripped a11y-critic SKILL.md (system-prompt "
          "equivalent) and the composed user prompt built by run_evidence_lane.assemble_prompt "
          "(PROMPT_PREFIX + blind fixture + labeled evidence-pack block, byte-identical to the "
          "local arm per README §5.1) — with all other reads barred (evals/ answer keys "
          "explicitly); response written by the subagent verbatim to this row's .md sibling, "
          "wrapped to JSON by wrap_hosted_rows.py without modification.")

force = "--force" in sys.argv
wrapped = skipped = 0
for md_path in sorted(glob.glob(os.path.join(ROWS, "*.md"))):
    m = NAME_RE.match(os.path.basename(md_path))
    if not m:
        print(f"SKIP (unrecognized name): {md_path}")
        continue
    fixture, cond, draw, model = m["fixture"], m["cond"], int(m["draw"]), m["model"]
    out_path = md_path[:-3] + ".json"
    if os.path.exists(out_path) and not force:
        skipped += 1
        continue
    payload = "CURATED" if cond == "curated-hosted" else "DUMP"
    meta_path = os.path.join(META_DIR, f"{fixture}.{payload.lower()}.meta.json")
    with open(meta_path) as f:
        meta = json.load(f)
    assert meta["condition"] == cond and meta["fixture_id"] == fixture
    with open(md_path) as f:
        response = f.read()
    bench = {
        "platform": "claude-subagent", "model": model, "tier": f"{model}-subagent-gp",
        "skill": "a11y-critic", "lane": "context-utilization-phase3",
        "fixture_id": fixture, "condition": cond, "payload": payload, "draw": draw,
        "num_ctx": None, "declared_context_length": None,
        "prompt_eval_count": None, "done_reason": None, "output_clipped": False,
        "context_pressure": None,
        "prompt_sha256": meta["prompt_sha256"],
        "user_prompt_sha256": meta["user_prompt_sha256"],
        "prompt_byte_length": meta["prompt_byte_length"],
        "pack_path": meta["pack_path"], "pack_sha256": meta["pack_sha256"],
        "pack_byte_length": meta["pack_byte_length"], "pack_available": True,
        "response_md_path": os.path.relpath(md_path, REPO),
        "method": METHOD.format(model=model),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    row = {"response": response, "done": True, "_benchmark": bench}
    tmp = out_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(row, f, indent=1)
    os.replace(tmp, out_path)
    wrapped += 1
    print(f"wrote {os.path.basename(out_path)} ({len(response)}B response)")
print(f"\nwrapped={wrapped} skipped(existing)={skipped}")
