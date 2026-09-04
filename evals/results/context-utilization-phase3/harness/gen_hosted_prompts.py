#!/usr/bin/env python3
"""Compose the hosted-arm prompts for the Phase 3 evidence-volume lane.

README §5.1 binds prompt composition identically across arms. This reuses
run_evidence_lane.py's own assemble_prompt / resolve_pack / load_fixture_content
so the hosted user-prompt text is byte-identical to what the local runner sends,
and run_benchmark.load_system_prompt() for the system-prompt-equivalent text.
Emits per (fixture, payload): a prompt file + a meta JSON (hashes, byte lengths,
pack meta) consumed later when wrapping subagent responses into row JSONs.
"""
import json
import os
import sys

REPO = "/Users/AlexUA_1/claude/accessibility-skills"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hosted")
sys.path.insert(0, os.path.join(REPO, "ollama"))

os.chdir(REPO)
import run_benchmark as rb  # noqa: E402
import run_evidence_lane as rel  # noqa: E402
from score_evidence_lane import load_manifest, DEFAULT_MANIFEST  # noqa: E402

os.makedirs(OUT, exist_ok=True)
manifest = load_manifest(DEFAULT_MANIFEST)
system_prompt = rb.load_system_prompt()

sys_path = os.path.join(OUT, "skill-system-prompt.md")
with open(sys_path, "w") as f:
    f.write(system_prompt)
print(f"system prompt: {sys_path} ({len(system_prompt.encode('utf-8'))}B, "
      f"sha256={rel.sha256_hex(system_prompt)[:16]}...)")

hosted_conditions = {c["payload"]: c["condition_id"] for c in manifest["conditions"]["hosted"]}

for fixture in manifest["fixtures"]:
    fid = fixture["fixture_id"]
    fixture_content = rel.load_fixture_content(fixture)
    for payload, condition_id in hosted_conditions.items():
        pack_text, pack_meta = rel.resolve_pack(fixture, payload, dry_run=False)
        prompt = rel.assemble_prompt(fixture_content, pack_text, payload)
        stem = f"{fid}.{payload.lower()}"
        prompt_path = os.path.join(OUT, f"{stem}.prompt.md")
        with open(prompt_path, "w") as f:
            f.write(prompt)
        meta = {
            "fixture_id": fid, "condition": condition_id, "payload": payload,
            "prompt_path": prompt_path,
            "prompt_sha256": rel.sha256_hex(system_prompt + prompt),
            "user_prompt_sha256": rel.sha256_hex(prompt),
            "prompt_byte_length": len((system_prompt + prompt).encode("utf-8")),
            **pack_meta,
        }
        with open(os.path.join(OUT, f"{stem}.meta.json"), "w") as f:
            json.dump(meta, f, indent=1)
        print(f"{stem}: prompt {len(prompt.encode('utf-8'))}B pack={pack_meta['pack_byte_length']}B")
