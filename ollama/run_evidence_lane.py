#!/usr/bin/env python3
"""Run Phase 3 evidence-volume-lane model rows against local Ollama models
(context-utilization plan, docs/plans/2026-08-24-context-utilization-plan.md
§6 Phase 3; lane design: evals/results/context-utilization-phase3/README.md;
built to close gate review finding F6:
docs/plans/2026-08-25-context-utilization-phase3-gate-review.md).

Critic-suite only, local models only (qwen3.6:35b / qwen3:32b per the
manifest's models.local — hosted opus/sonnet rows are Claude Code subagent
runs, not this script). lane_manifest.yaml is the ONLY config source: no
fixture list, condition/cell shape, or num_ctx value is hardcoded here.

Rows are scored by ollama/score_evidence_lane.py — this file's job stops at
producing a row in the shape that scorer consumes (see its docstring): a
`_benchmark` dict carrying `prompt_eval_count` / `done_reason` /
`context_pressure` / `fixture_id` / `model`, plus this lane's own additions
(condition / payload / draw / num_ctx / prompt+pack hashes / output_clipped).

SCHEMA NOTE (open at write time — see the runner-builder's report to the
team lead): the brief specifies pack content goes "between fixture source
and the critic ask," which is ambiguous against run_benchmark.py's
PROMPT_PREFIX (ask BEFORE the fixture, nothing after it). assemble_prompt()
below implements a best-effort default — ask, then fixture, then a labeled
"## Evidence Pack (CURATED|DUMP)" block — pending confirmation from
phase3-lane-designer (coordinated via SendMessage before this file was
finalized). It is the single function to change if README §5 lands on a
different order/heading; nothing else in this file depends on the exact
splice point. Likewise resolve_pack_path() is schema-tolerant (tries a
fixture-level `packs: {CURATED: path, DUMP: path}` dict, falling back to
flat `curated_pack_path` / `dump_pack_path` keys) pending the manifest's
actual pack_path field name/shape.

Usage:
    # One cell, real run (requires a committed pack; fails loud if TBD/missing):
    python3 ollama/run_evidence_lane.py --fixture-id heading-hierarchy-skipped \\
        --condition curated-32k --draw 1 --model qwen3.6:35b

    # Preview a cell's assembled-prompt stats without calling Ollama — works
    # today even though no packs exist yet (prints a PLACEHOLDER note):
    python3 ollama/run_evidence_lane.py --fixture-id heading-hierarchy-skipped \\
        --condition curated-32k --draw 1 --model qwen3.6:35b --dry-run

    # Every scored local cell in the manifest (6 fixtures x 3 scored
    # conditions x 2 models x 2 draws = 72), optionally filtered:
    python3 ollama/run_evidence_lane.py --all --dry-run
    python3 ollama/run_evidence_lane.py --all --dry-run --model qwen3.6:35b

    # The OVERFLOW mechanism receipt (README §4 "OVERFLOW" row / gate F6):
    # sends the DUMP-sized prompt at the cell's num_ctx ANYWAY, bypassing the
    # client-side guard, to record what Ollama actually does. Capped at one
    # recorded row per model+condition (glob-checked); --force to re-record.
    python3 ollama/run_evidence_lane.py --fixture-id tabs-missing-arrow-nav \\
        --condition overflow-32k --draw 1 --model qwen3:32b --allow-overflow-receipt

    # Prove the num_ctx-per-cell resolver and the overflow-guard arithmetic
    # with synthetic data only — no live model calls, no scored rows:
    python3 ollama/run_evidence_lane.py --selftest

Conventions reused UNCHANGED from ollama/run_benchmark.py (the critic lane):
PROMPT_PREFIX, strip_answer_key's blind protocol, context_overflow +
write_overflow_row (the Phase 0.2/0.3 guard), flag_context_pressure,
write_json_atomic, temperature=0.3 + stream=True + a 300s timeout (the
critic lane's own settings — the same 300s applies here even though DUMP@40K
prompts run larger than a plain critic row; flagging for the gate re-review
rather than silently widening it [2026-08-25: condition IDs were curated-49k/
dump-49k when this note was first written; the lane standardized on @40K the
same day, DUMP-cell ruling — corrected here]). Also imports resolve_repo_path
/ load_manifest / resolve_fixture_config from ollama/score_evidence_lane.py
so the two scripts can never resolve a fixture's paths differently.

`--all` never wraps individual cells in try/except: a RunnerError from any
cell (e.g. a missing pack) aborts the whole batch immediately rather than
scrolling past 72 loud-but-swallowed errors — a missing pack is a setup
precondition, not a one-off.

F13 fast-follow (bench-reviewer gate re-review, same day): the overflow
guard used to check the estimate against the REQUESTED num_ctx only —
proven live to miss a real failure mode (qwen3:32b requested at 49,152 was
silently clamped server-side to its declared 40,960, truncating 54.7% of a
45,176-token prompt). Every cell here now fetches the model's real ceiling
(rb.fetch_declared_context_length, cached, fails loud if unreachable) and
threads it into rb.context_overflow as the ceiling to clamp against —
resolve_declared_context_length() below mirrors resolve_pack()'s
dry-run-degrades / real-run-fails-loud shape. Recorded on every row as
`declared_context_length`.
"""

import argparse
import glob
import hashlib
import json
import os
import sys
import tempfile
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_benchmark as rb  # noqa: E402
from score_evidence_lane import (  # noqa: E402
    DEFAULT_MANIFEST,
    ScorerError,
    load_manifest,
    resolve_fixture_config,
    resolve_repo_path,
)

LANE_ID = "context-utilization-phase3"
OUTPUT_PREFIX = "ollama-evidence-lane"
PACK_HEADING = {
    "CURATED": "## Evidence Pack (CURATED)",
    "DUMP": "## Evidence Pack (DUMP)",
}


class RunnerError(Exception):
    """Lane-runner precondition failure (bad manifest reference, missing
    pack, schema mismatch, quota/validation violation) — caught in main()
    and reported cleanly, never a raw traceback."""


# ── small pure helpers ──────────────────────────────────────────────────

def sha256_hex(data):
    """data: str or bytes. Repo receipts convention: a large blob is never
    embedded raw in a row — length + sha256 stand in for it."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


# ── manifest resolution ─────────────────────────────────────────────────

def resolve_overflow_receipt_fixture(manifest):
    """The manifest's pinned OVERFLOW-receipt fixture (added 2026-08-25,
    phase3-lane-designer, top-level `overflow_receipt_fixture` key — was
    unpinned/operator's-choice when this runner was first built). None if
    the manifest predates this key: fixture choice for
    --allow-overflow-receipt then stays fully operator's judgment,
    unvalidated (this runner's original, still-supported behavior)."""
    return manifest.get("overflow_receipt_fixture")


def resolve_condition(manifest, condition_id):
    for c in manifest.get("conditions", {}).get("local", []):
        if c.get("condition_id") == condition_id:
            return c
    available = [c.get("condition_id") for c in manifest.get("conditions", {}).get("local", [])]
    raise RunnerError(f"{condition_id!r} not found in lane_manifest.yaml conditions.local "
                       f"(available: {available})")


def resolve_num_ctx(condition, model):
    """Per-CELL num_ctx (the reason run_benchmark.py's per-MODEL CRITIC_CTX
    can't serve this lane — gate F6). Checks a per-model override first
    (num_ctx_by_model — not in the manifest as of this writing, but the
    qwen3:32b DUMP@49K ceiling risk in README §4.1 may add one) and falls
    back to the condition's flat num_ctx either way."""
    overrides = condition.get("num_ctx_by_model") or {}
    if model in overrides:
        return overrides[model]
    if "num_ctx" not in condition:
        raise RunnerError(f"condition {condition.get('condition_id')!r} has no num_ctx "
                           f"(and no num_ctx_by_model override for model {model!r}) in the manifest.")
    return condition["num_ctx"]


def resolve_declared_context_length(model, *, dry_run, fetch=None):
    """F13 fast-follow (gate re-review, 2026-08-25): num_ctx alone is the
    REQUESTED window, not what Ollama will actually allocate — proven live
    the same day (qwen3:32b requested at 49,152 was silently clamped
    server-side to its declared 40,960; a 45,176-token prompt lost 54.7% of
    itself to truncation underneath a guard checking only the requested
    value). rb.fetch_declared_context_length (the default `fetch`,
    injectable here for selftest determinism without a network call) is the
    model's real ceiling from /api/tags, threaded into rb.context_overflow
    so the guard compares against min(num_ctx, declared) instead of num_ctx
    alone. In --dry-run, a fetch failure (no local Ollama, model not
    pulled) degrades to an explicitly-labeled unknown rather than blocking
    the preview — mirrors resolve_pack()'s dry-run degradation. A REAL run
    never degrades: the fetch's own fail-loud GuardConfigError becomes a
    RunnerError. Returns (declared_context_length_or_None, known: bool)."""
    fetch = fetch or rb.fetch_declared_context_length
    try:
        return fetch(model), True
    except rb.GuardConfigError as e:
        if dry_run:
            return None, False
        raise RunnerError(str(e)) from e


def resolve_pack_path(fixture, payload):
    """Manifest's authoritative shape (lane_manifest.yaml, 2026-08-25 REVISE
    fixes: 'Runner interface contract' section): fixture['pack_paths'] =
    {curated: path, dump: path}, lowercase payload keys. Also tolerates two
    alternate shapes in case of further schema drift: fixture['packs']
    (uppercase CURATED/DUMP keys) and a flat f'{payload.lower()}_pack_path'
    key. None if nothing matches, or the value is an empty/'TBD' placeholder."""
    pack_paths = fixture.get("pack_paths") or {}
    candidate = pack_paths.get(payload.lower())
    if candidate is None:
        packs = fixture.get("packs") or {}
        candidate = packs.get(payload)
    if candidate is None:
        candidate = fixture.get(f"{payload.lower()}_pack_path")
    if candidate is None:
        return None
    if not isinstance(candidate, str):
        raise RunnerError(f"fixture {fixture.get('fixture_id')!r} pack path for payload={payload} "
                           f"is a {type(candidate).__name__}, expected one string path (one frozen "
                           "pack file per fixture-payload, per README §9 'packs are frozen').")
    if not candidate.strip() or candidate.strip().upper() == "TBD":
        return None
    return candidate


def resolve_pack(fixture, payload, *, dry_run):
    """Read the frozen pack file for (fixture, payload). dry_run=True
    degrades a missing/TBD/not-yet-written pack to a labeled placeholder
    (packs are gated — this must work before any pack exists); dry_run=False
    fails loud instead (README §10: no scored row without a committed pack)."""
    rel_path = resolve_pack_path(fixture, payload)
    abs_path = resolve_repo_path(rel_path) if rel_path else None
    if abs_path and os.path.exists(abs_path):
        with open(abs_path, "rb") as f:
            raw = f.read()
        meta = {"pack_path": rel_path, "pack_sha256": sha256_hex(raw),
                 "pack_byte_length": len(raw), "pack_available": True}
        return raw.decode("utf-8"), meta
    if dry_run:
        placeholder = (f"[PACK NOT YET AVAILABLE for payload={payload} — declared path: "
                        f"{rel_path or 'TBD (no path in manifest yet)'}]")
        meta = {"pack_path": rel_path, "pack_sha256": None,
                 "pack_byte_length": 0, "pack_available": False}
        return placeholder, meta
    reason = "does not exist on disk" if rel_path else "is TBD/missing in the manifest"
    raise RunnerError(f"Pack unavailable for fixture={fixture.get('fixture_id')!r} payload={payload}: "
                       f"declared path {rel_path!r} {reason}. Refusing to run for real — packs must "
                       "be frozen and committed before scored rows (README §10 pack-freeze protocol). "
                       "Use --dry-run to preview.")


def load_fixture_content(fixture):
    """Blind protocol (run_benchmark.py's strip_answer_key, reused
    unchanged): withhold the fixture's '## Accessibility Issues...' answer
    key from the model prompt."""
    abs_path = resolve_repo_path(fixture["fixture_path"])
    with open(abs_path) as f:
        raw = f.read()
    return rb.strip_answer_key(raw)


# ── prompt assembly ──────────────────────────────────────────────────────

def assemble_prompt(fixture_content, pack_text, payload):
    """See the SCHEMA NOTE in the module docstring — best-effort default
    pending §5 confirmation. Order: [PROMPT_PREFIX ask] + [fixture source] +
    [labeled pack block]."""
    heading = PACK_HEADING.get(payload, f"## Evidence Pack ({payload})")
    pack_block = f"\n\n{heading}\n\n{pack_text}\n"
    return rb.PROMPT_PREFIX + fixture_content + pack_block


# ── validation ───────────────────────────────────────────────────────────

def validate_cell_args(condition, allow_overflow_receipt, *, fixture_id=None, overflow_receipt_fixture=None):
    """scored xor allow_overflow_receipt must hold for a REAL run. Skipped
    entirely in --dry-run mode (a caller may want to preview an overflow
    cell without the flag).

    fixture_id/overflow_receipt_fixture (optional, added 2026-08-25 per
    phase3-lane-designer's manifest pin): if the manifest pins a specific
    OVERFLOW-receipt fixture, a real --allow-overflow-receipt run against
    any OTHER fixture is rejected rather than silently accepted — the plan
    means one deliberate fixture, not operator's pick. Both None (older
    manifest, or a non-overflow call site that never passes them) skips
    this check entirely — unchanged, backward-compatible behavior."""
    scored = condition.get("scored", True)
    cid = condition.get("condition_id")
    if not scored and not allow_overflow_receipt:
        raise RunnerError(f"condition {cid!r} is unscored (receipt-only, note="
                           f"{condition.get('note')!r}). Real execution requires "
                           "--allow-overflow-receipt. (--dry-run previews it without the flag.)")
    if scored and allow_overflow_receipt:
        raise RunnerError(f"--allow-overflow-receipt was passed but condition {cid!r} is scored — "
                           "this flag only applies to unscored receipt conditions. Remove it.")
    if allow_overflow_receipt and overflow_receipt_fixture and fixture_id != overflow_receipt_fixture:
        raise RunnerError(f"the manifest pins the OVERFLOW receipt to fixture_id="
                           f"{overflow_receipt_fixture!r}; you passed {fixture_id!r}. Pass "
                           f"--fixture-id {overflow_receipt_fixture} (or omit --fixture-id to use "
                           "it by default).")


# ── output path / idempotency / quota ───────────────────────────────────

def build_out_path(fixture_id, condition_id, draw, model, *, results_dir=None):
    results_dir = rb.RESULTS_DIR if results_dir is None else results_dir
    model_tag = rb.make_model_tag(model)
    name = f"{OUTPUT_PREFIX}-{fixture_id}-{condition_id}-draw{draw}-{model_tag}-response.json"
    return os.path.join(results_dir, name)


def existing_valid_row(out_path):
    """A prior real (non-INVALID) row already recorded for this exact cell."""
    return os.path.exists(out_path)


def refuse_if_receipt_quota_exceeded(model, condition_id, *, force, results_dir=None):
    """The plan allows exactly 1 fixture x 1 draw per model for an unscored
    (receipt-only) condition. Mechanically enforced by globbing for any
    already-recorded row on this model+condition, regardless of fixture/draw
    — --force overrides for a deliberate re-record."""
    if force:
        return
    results_dir = rb.RESULTS_DIR if results_dir is None else results_dir
    model_tag = rb.make_model_tag(model)
    pattern = os.path.join(results_dir, f"{OUTPUT_PREFIX}-*-{condition_id}-draw*-{model_tag}-response.json")
    existing = sorted(glob.glob(pattern))
    if existing:
        raise RunnerError(f"OVERFLOW receipt quota exceeded for model={model!r} "
                           f"condition={condition_id!r}: already recorded at {existing[0]!r}. The "
                           "plan allows exactly 1 fixture x 1 draw per model for this condition "
                           "(README §5/§8). Pass --force to re-record deliberately.")


# ── network ──────────────────────────────────────────────────────────────

def stream_ollama_response(model, system_prompt, prompt, num_ctx):
    """Byte-identical request shape to run_benchmark.py's run_ollama (the
    critic lane): stream=True, temperature=0.3, a 300s timeout."""
    payload = {"model": model, "system": system_prompt, "prompt": prompt,
               "stream": True, "options": {"num_ctx": num_ctx, "temperature": 0.3}}
    req = urllib.request.Request(rb.OLLAMA_URL, data=json.dumps(payload).encode(),
                                  headers={"Content-Type": "application/json"})
    response_text, thinking_chars, final_chunk = "", 0, {}
    start = time.time()
    with urllib.request.urlopen(req, timeout=300) as resp:
        for line in resp:
            chunk = json.loads(line)
            if chunk.get("response"):
                response_text += chunk["response"]
            if chunk.get("thinking"):
                thinking_chars += len(chunk["thinking"])
            if chunk.get("done"):
                final_chunk = chunk
                break
    return response_text, thinking_chars, final_chunk, time.time() - start


def build_row(cell, *, overflow_receipt):
    text, thinking_chars, final_chunk, elapsed = stream_ollama_response(
        cell["model"], cell["system_prompt"], cell["prompt"], cell["num_ctx"],
    )
    prompt_bytes = (cell["system_prompt"] + cell["prompt"]).encode("utf-8")
    prompt_eval_count = final_chunk.get("prompt_eval_count")
    done_reason = final_chunk.get("done_reason")
    bench = {
        "model": cell["model"], "skill": "a11y-critic", "lane": LANE_ID,
        "fixture_id": cell["fixture_id"], "condition": cell["condition_id"],
        "payload": cell["payload"], "draw": cell["draw"], "num_ctx": cell["num_ctx"],
        "declared_context_length": cell["declared_context_length"],  # F13
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "done_reason": done_reason,
        "output_clipped": done_reason == "length",  # gate F7
        "thinking_chars": thinking_chars,
        "estimated_prompt_tokens": cell["estimated"], "prompt_eval_count": prompt_eval_count,
        "context_pressure": rb.flag_context_pressure(prompt_eval_count, cell["num_ctx"]),
        "prompt_sha256": sha256_hex(prompt_bytes), "prompt_byte_length": len(prompt_bytes),
        "overflow_receipt": overflow_receipt, "guard_tripped": cell["overflow"],
    }
    bench.update(cell["pack_meta"])
    return {"response": text, "done": True, "total_duration": final_chunk.get("total_duration"),
            "eval_count": final_chunk.get("eval_count"), "_benchmark": bench}


# ── cell orchestration ───────────────────────────────────────────────────

def prepare_cell(manifest, fixture_id, condition_id, draw, model, system_prompt, *, dry_run):
    rb.validate_fixture_id(fixture_id)
    fixture = resolve_fixture_config(manifest, fixture_id)
    condition = resolve_condition(manifest, condition_id)
    if model not in manifest["models"]["local"]:
        raise RunnerError(f"model {model!r} not in manifest models.local {manifest['models']['local']}")
    num_ctx = resolve_num_ctx(condition, model)
    payload = condition["payload"]
    declared_context_length, declared_known = resolve_declared_context_length(model, dry_run=dry_run)  # F13
    fixture_content = load_fixture_content(fixture)
    pack_text, pack_meta = resolve_pack(fixture, payload, dry_run=dry_run)
    prompt = assemble_prompt(fixture_content, pack_text, payload)
    overflow, estimated = rb.context_overflow(system_prompt, prompt, num_ctx, declared_context_length)
    return {"fixture_id": fixture_id, "condition_id": condition_id, "draw": draw, "model": model,
            "condition": condition, "num_ctx": num_ctx, "payload": payload,
            "system_prompt": system_prompt, "prompt": prompt, "pack_meta": pack_meta,
            "overflow": overflow, "estimated": estimated,
            "declared_context_length": declared_context_length, "declared_known": declared_known,
            "overflow_receipt_fixture": resolve_overflow_receipt_fixture(manifest)}


def execute_cell(cell, *, dry_run, allow_overflow_receipt, force, results_dir=None):
    if dry_run:
        report = build_dry_run_report(cell)
        print_dry_run_stats(report)
        return report

    validate_cell_args(cell["condition"], allow_overflow_receipt, fixture_id=cell["fixture_id"],
                        overflow_receipt_fixture=cell["overflow_receipt_fixture"])
    out_path = build_out_path(cell["fixture_id"], cell["condition_id"], cell["draw"], cell["model"],
                               results_dir=results_dir)
    if not force and existing_valid_row(out_path):
        print(f"SKIP (already recorded): {out_path}")
        return {"skipped": True, "path": out_path}

    if allow_overflow_receipt:
        refuse_if_receipt_quota_exceeded(cell["model"], cell["condition_id"], force=force,
                                          results_dir=results_dir)
    elif cell["overflow"]:
        path = rb.write_overflow_row(out_path, cell["model"], cell["fixture_id"], cell["estimated"],
                                      cell["num_ctx"], skill="a11y-critic", condition=cell["condition_id"],
                                      declared_context_length=cell["declared_context_length"])
        return {"invalid": "context_overflow", "path": path}

    row = build_row(cell, overflow_receipt=allow_overflow_receipt)
    rb.write_json_atomic(out_path, row)
    print(f"Wrote {out_path}")
    return row


# ── dry-run reporting ────────────────────────────────────────────────────

def build_dry_run_report(cell):
    prompt_bytes = (cell["system_prompt"] + cell["prompt"]).encode("utf-8")
    declared = cell["declared_context_length"]
    effective_ctx = cell["num_ctx"] if declared is None else min(cell["num_ctx"], declared)  # F13
    ceiling_note = f" (requested num_ctx={cell['num_ctx']})" if effective_ctx != cell["num_ctx"] else ""
    return {
        "fixture_id": cell["fixture_id"], "condition_id": cell["condition_id"],
        "payload": cell["payload"], "num_ctx": cell["num_ctx"], "draw": cell["draw"],
        "model": cell["model"], "scored": cell["condition"].get("scored", True),
        "declared_context_length": declared, "declared_known": cell["declared_known"],
        "effective_ctx": effective_ctx,
        "system_prompt_bytes": len(cell["system_prompt"].encode("utf-8")),
        "prompt_prefix_bytes": len(rb.PROMPT_PREFIX.encode("utf-8")),
        "assembled_prompt_bytes": len(cell["prompt"].encode("utf-8")),
        "total_bytes": len(prompt_bytes), "estimated_tokens": cell["estimated"],
        "response_reserve": rb.RESPONSE_RESERVE, "guard_would_fire": cell["overflow"],
        "budget_check": f"{cell['estimated']} est + {rb.RESPONSE_RESERVE} reserve "
                         f"{'>' if cell['overflow'] else '<='} effective ceiling {effective_ctx}{ceiling_note}",
        "pack_meta": cell["pack_meta"],
    }


def print_dry_run_stats(report):
    print(f"\n=== DRY RUN: {report['fixture_id']} / {report['condition_id']} "
          f"(draw {report['draw']}, model {report['model']}) ===")
    print(f"  payload={report['payload']} num_ctx={report['num_ctx']} scored={report['scored']}")
    # F13: print the declared ceiling next to num_ctx when /api/tags was
    # reachable; degrade gracefully (never block the preview) when it
    # wasn't — a real run fails loud instead of degrading (team-lead design
    # note, 2026-08-25).
    if report["declared_known"]:
        declared_display, note = report["declared_context_length"], ""
    else:
        declared_display, note = "unavailable (offline dry-run)", "  [a real run fails loud instead]"
    print(f"  declared_context_length={declared_display} "
          f"(effective ceiling={report['effective_ctx']}){note}")
    pm = report["pack_meta"]
    pack_state = "available" if pm.get("pack_available") else "PLACEHOLDER (not yet built)"
    print(f"  pack_path={pm.get('pack_path')!r} [{pack_state}] "
          f"bytes={pm.get('pack_byte_length')} sha256={pm.get('pack_sha256')}")
    print(f"  system_prompt={report['system_prompt_bytes']}B  prompt_prefix={report['prompt_prefix_bytes']}B  "
          f"assembled_prompt={report['assembled_prompt_bytes']}B  total={report['total_bytes']}B")
    verdict = "GUARD WOULD FIRE (INVALID row)" if report["guard_would_fire"] else "fits"
    if not report["guard_would_fire"] and not pm.get("pack_available"):
        verdict += "  [caveat: pack is a placeholder — a real pack changes this estimate]"
    print(f"  estimated_tokens={report['estimated_tokens']} ({report['budget_check']}) -> {verdict}")


# ── --all enumeration ────────────────────────────────────────────────────

def enumerate_all_cells(manifest, *, fixture_id=None, condition_id=None, model=None):
    """Every SCORED local cell by default (fixtures x scored conditions x
    models x draws_per_cell) — unscored (receipt) conditions are excluded
    unless the caller names one explicitly via condition_id, since they
    require single-cell --allow-overflow-receipt execution (gate F6:
    'refuse to run overflow mode beyond that without the flag')."""
    fixtures = [fixture_id] if fixture_id else [f["fixture_id"] for f in manifest["fixtures"]]
    conditions = [condition_id] if condition_id else [
        c["condition_id"] for c in manifest["conditions"]["local"] if c.get("scored", True)
    ]
    models = [model] if model else manifest["models"]["local"]
    # manifest field renamed draws_per_cell -> draws in the 2026-08-25 REVISE
    # fixes revision (lane_manifest.yaml "Runner interface contract" section);
    # the fallback key keeps this working against an older manifest snapshot.
    draws = range(1, manifest.get("draws", manifest.get("draws_per_cell", 1)) + 1)
    for fx in fixtures:
        for cond in conditions:
            for mdl in models:
                for draw in draws:
                    yield fx, cond, mdl, draw


# ── selftest (synthetic data only — no manifest file, no network) ───────

def _check(label, cond):
    print(f"  {'+' if cond else 'X'} {label}")
    return bool(cond)


def _does_not_raise(fn, *a, **kw):
    try:
        fn(*a, **kw)
        return True
    except RunnerError:
        return False


def _selftest_num_ctx():
    plain = {"condition_id": "curated-32k", "num_ctx": 32768}
    ok = _check("flat num_ctx resolves for any model", resolve_num_ctx(plain, "qwen3.6:35b") == 32768)
    # Deliberately synthetic condition_id, decoupled from any real manifest
    # cell name (past or future) — flagged by phase3-lane-designer as a
    # stale-looking "dump-49k" label pre-fix; renamed so it never needs to
    # be kept in sync with the manifest's actual condition IDs again.
    overridden = {"condition_id": "test-condition-with-override", "num_ctx": 49152,
                  "num_ctx_by_model": {"qwen3:32b": 40960}}
    ok &= _check("per-model override wins when present",
                 resolve_num_ctx(overridden, "qwen3:32b") == 40960)
    ok &= _check("falls back to flat value for a model with no override",
                 resolve_num_ctx(overridden, "qwen3.6:35b") == 49152)
    ok &= _check("missing num_ctx (and no override) raises RunnerError",
                 not _does_not_raise(resolve_num_ctx, {"condition_id": "broken"}, "qwen3:32b"))
    return ok


def _selftest_pack_resolution(tmp):
    real_path = os.path.join(tmp, "digest.md")
    with open(real_path, "w") as f:
        f.write("EVIDENCE DIGEST TEXT")
    fx_packs = {"fixture_id": "x", "packs": {"CURATED": real_path, "DUMP": "TBD"}}
    fx_flat = {"fixture_id": "y", "curated_pack_path": real_path}

    ok = _check("packs{} shape resolves", resolve_pack_path(fx_packs, "CURATED") == real_path)
    ok &= _check("TBD resolves to None", resolve_pack_path(fx_packs, "DUMP") is None)
    ok &= _check("flat *_pack_path fallback resolves", resolve_pack_path(fx_flat, "CURATED") == real_path)

    text, meta = resolve_pack(fx_packs, "CURATED", dry_run=False)
    ok &= _check("real pack read returns exact content", text == "EVIDENCE DIGEST TEXT")
    ok &= _check("sha256 matches an independent hash",
                 meta["pack_sha256"] == sha256_hex("EVIDENCE DIGEST TEXT"))

    _, meta2 = resolve_pack(fx_packs, "DUMP", dry_run=True)
    ok &= _check("dry-run on TBD pack degrades gracefully (no raise)", meta2["pack_available"] is False)
    ok &= _check("real run on TBD pack fails loud",
                 not _does_not_raise(resolve_pack, fx_packs, "DUMP", dry_run=False))
    return ok


def _selftest_overflow_guard_arithmetic():
    tiny_overflow, _ = rb.context_overflow("", "x" * 10, 100)
    ok = _check("reserve alone exceeds a tiny num_ctx -> overflow True", tiny_overflow is True)

    roomy_overflow, _ = rb.context_overflow("", "hello world", 32768)
    ok &= _check("tiny prompt at 32768 num_ctx -> overflow False", roomy_overflow is False)

    edge_ctx = rb.RESPONSE_RESERVE + 100
    just_under = "x" * int((edge_ctx - rb.RESPONSE_RESERVE - 5) * rb.CHARS_PER_TOKEN_CONSERVATIVE)
    just_over = "x" * int((edge_ctx - rb.RESPONSE_RESERVE + 50) * rb.CHARS_PER_TOKEN_CONSERVATIVE)
    under_overflow, _ = rb.context_overflow("", just_under, edge_ctx)
    over_overflow, _ = rb.context_overflow("", just_over, edge_ctx)
    ok &= _check("just-under-budget prompt does not trip the guard", under_overflow is False)
    ok &= _check("just-over-budget prompt trips the guard", over_overflow is True)
    return ok


def _raise_guard_config_error(model):
    raise rb.GuardConfigError(f"selftest: simulated /api/tags failure for {model!r}")


def _selftest_declared_context_length():
    """F13: this runner's own wiring of the declared-ceiling fix — the
    shared context_overflow arithmetic is proven in
    ollama/test_context_guard.py; this checks resolve_declared_context_length's
    dry-run-degrades / real-run-fails-loud contract and that a smaller
    declared ceiling actually flips this runner's guard decision. The
    `fetch` param is injected so none of this touches the network."""
    ok = _check("dry-run degrades gracefully when the fetch fails",
                resolve_declared_context_length("x", dry_run=True, fetch=_raise_guard_config_error)
                == (None, False))
    ok &= _check("real run re-raises the fetch failure as RunnerError",
                 not _does_not_raise(resolve_declared_context_length, "x", dry_run=False,
                                      fetch=_raise_guard_config_error))
    ok &= _check("a successful fetch passes the value straight through",
                 resolve_declared_context_length("x", dry_run=False, fetch=lambda m: 40960) == (40960, True))

    # This runner's own call into rb.context_overflow (test_context_guard.py
    # proves the shared arithmetic; this proves THIS file passes the 4th
    # arg through correctly end to end).
    reserve = rb.RESPONSE_RESERVE
    text = "a" * int((40960 - reserve + 200) * rb.CHARS_PER_TOKEN_CONSERVATIVE)
    fits_without_declared, _ = rb.context_overflow("", text, 49152)
    fires_with_declared, _ = rb.context_overflow("", text, 49152, 40960)
    ok &= _check("declared ceiling smaller than requested flips fits -> fires",
                 fits_without_declared is False and fires_with_declared is True)
    return ok


def _selftest_prompt_assembly():
    prompt = assemble_prompt("FIXTURE_TEXT", "PACK_TEXT", "CURATED")
    ok = _check("assembled prompt starts with PROMPT_PREFIX", prompt.startswith(rb.PROMPT_PREFIX))
    ok &= _check("fixture text precedes pack text",
                 prompt.index("FIXTURE_TEXT") < prompt.index("PACK_TEXT"))
    ok &= _check("CURATED heading present", "CURATED" in prompt)
    ok &= _check("DUMP heading present", "DUMP" in assemble_prompt("F", "P", "DUMP"))
    return ok


def _selftest_validate_and_quota(tmp):
    unscored = {"condition_id": "overflow-32k", "scored": False}
    scored = {"condition_id": "curated-32k", "scored": True}
    cases = [(unscored, False, True), (unscored, True, False),
             (scored, True, True), (scored, False, False)]
    ok = True
    for cond, flag, should_raise in cases:
        raised = not _does_not_raise(validate_cell_args, cond, flag)
        ok &= _check(f"validate_cell_args scored={cond['scored']} flag={flag} -> raises={should_raise}",
                     raised == should_raise)

    # Manifest fixture pin (2026-08-25, phase3-lane-designer's
    # overflow_receipt_fixture key) — added on top of the existing
    # scored/flag checks above, all via the same function's new kwargs.
    ok &= _check("pinned fixture + matching fixture_id -> does not raise",
                 _does_not_raise(validate_cell_args, unscored, True,
                                  fixture_id="tabs-missing-arrow-nav",
                                  overflow_receipt_fixture="tabs-missing-arrow-nav"))
    ok &= _check("pinned fixture + a DIFFERENT fixture_id -> raises",
                 not _does_not_raise(validate_cell_args, unscored, True,
                                      fixture_id="heading-hierarchy-skipped",
                                      overflow_receipt_fixture="tabs-missing-arrow-nav"))
    ok &= _check("unpinned manifest (overflow_receipt_fixture=None) -> any fixture_id is fine",
                 _does_not_raise(validate_cell_args, unscored, True,
                                  fixture_id="anything-at-all", overflow_receipt_fixture=None))

    ok &= _check("empty results dir: quota guard does not raise",
                 _does_not_raise(refuse_if_receipt_quota_exceeded, "qwen3:32b", "overflow-32k",
                                  force=False, results_dir=tmp))
    open(build_out_path("fx", "overflow-32k", 1, "qwen3:32b", results_dir=tmp), "w").close()
    ok &= _check("existing receipt row: quota guard raises",
                 not _does_not_raise(refuse_if_receipt_quota_exceeded, "qwen3:32b", "overflow-32k",
                                      force=False, results_dir=tmp))
    ok &= _check("--force bypasses the quota guard",
                 _does_not_raise(refuse_if_receipt_quota_exceeded, "qwen3:32b", "overflow-32k",
                                  force=True, results_dir=tmp))
    return ok


def selftest():
    """Proves the num_ctx-per-cell resolver and the overflow-guard
    arithmetic (the two things the gate review most wants verified), plus
    pack resolution, the F13 declared-context-length wiring, prompt
    assembly, and the validation/quota guards. Synthetic data only — no
    real manifest, no network, no scored rows."""
    print("=== run_evidence_lane.py selftest ===\n")
    with tempfile.TemporaryDirectory() as tmp:
        ok = _selftest_num_ctx()
        ok &= _selftest_pack_resolution(tmp)
        ok &= _selftest_overflow_guard_arithmetic()
        ok &= _selftest_declared_context_length()
        ok &= _selftest_prompt_assembly()
        ok &= _selftest_validate_and_quota(tmp)
    print(f"\nSelftest: {'ALL PASS' if ok else 'FAILURES ABOVE'}")
    return ok


# ── CLI ──────────────────────────────────────────────────────────────────

def build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--manifest", default=DEFAULT_MANIFEST)
    p.add_argument("--fixture-id")
    p.add_argument("--condition")
    p.add_argument("--draw", type=int)
    p.add_argument("--model")
    p.add_argument("--all", action="store_true", help="Enumerate the manifest's scored local matrix")
    p.add_argument("--dry-run", action="store_true", help="Print assembled-prompt stats, no API call")
    p.add_argument("--allow-overflow-receipt", action="store_true",
                    help="Send an unscored (receipt-only) cell anyway, bypassing the overflow guard")
    p.add_argument("--force", action="store_true", help="Re-run even if an output row already exists")
    p.add_argument("--selftest", action="store_true")
    return p


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.selftest:
        sys.exit(0 if selftest() else 1)

    if args.all and args.allow_overflow_receipt:
        parser.error("--all and --allow-overflow-receipt cannot be combined — overflow receipts are "
                      "single-cell, explicit-fixture runs (see module docstring).")

    try:
        manifest = load_manifest(args.manifest)
        system_prompt = rb.load_system_prompt()
        if args.all:
            cells = list(enumerate_all_cells(manifest, fixture_id=args.fixture_id,
                                              condition_id=args.condition, model=args.model))
            print(f"--all: {len(cells)} cell(s) to {'preview' if args.dry_run else 'run'}")
            for fixture_id, condition_id, model, draw in cells:
                cell = prepare_cell(manifest, fixture_id, condition_id, draw, model, system_prompt,
                                     dry_run=args.dry_run)
                execute_cell(cell, dry_run=args.dry_run, allow_overflow_receipt=False, force=args.force)
        else:
            fixture_id = args.fixture_id
            if fixture_id is None and args.allow_overflow_receipt:
                # Manifest pin (2026-08-25, phase3-lane-designer): default
                # rather than force the operator to look it up and retype it.
                # Still overridable — passing a different --fixture-id here
                # falls through to validate_cell_args's mismatch check below.
                fixture_id = resolve_overflow_receipt_fixture(manifest)
            missing = [n for n, v in (("--fixture-id", fixture_id), ("--condition", args.condition),
                                       ("--draw", args.draw), ("--model", args.model)) if v is None]
            if missing:
                parser.error(f"missing required argument(s) for single-cell mode: {', '.join(missing)} "
                              "(or pass --all)")
            cell = prepare_cell(manifest, fixture_id, args.condition, args.draw, args.model,
                                 system_prompt, dry_run=args.dry_run)
            execute_cell(cell, dry_run=args.dry_run, allow_overflow_receipt=args.allow_overflow_receipt,
                         force=args.force)
    except (RunnerError, ScorerError) as e:
        sys.exit(f"ERROR: {e}")


if __name__ == "__main__":
    main()
