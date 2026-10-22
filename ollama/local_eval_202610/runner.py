"""Immutable cells, strict eligibility, and descriptive scoring."""
import contextlib
import io
import json
import re
import sys
import uuid
from pathlib import Path

import yaml
from ollama import run_benchmark as rb, score_output as so, score_bugreport as sb
from ollama.score_common import strip_thinking
from .freeze import digest, encoded, exclusive, verify
from . import transport as tr

OPTIONS = {"temperature": .3, "num_ctx": 32768, "num_predict": 16384}
VERDICT = re.compile(r"^\s*(?:#+\s*)?(?:\*\*)?Verdict(?:\*\*)?\s*:(?:\*\*)?\s*(?:\*\*)?"
                     r"(ACCEPT-WITH-RESERVATIONS|ACCEPT|REVISE|REJECT)(?:\*\*)?(?=$|[\s.,:;—–(])[\t ]*[^\n]*$", re.I | re.M)


def eligibility(attempt, suite):
    if attempt.get("contaminated"):
        return "INVALID", "co-residency"
    if attempt.get("offload_verified") is False:
        return "INVALID", "full offload not verified"
    if attempt.get("exception"):
        return "NON_EXECUTION", "error"
    terminal = attempt.get("terminal") or {}
    reason = terminal.get("done_reason", terminal.get("finish_reason"))
    if reason != "stop":
        return "NON_EXECUTION", "clipped or missing final stop"
    text, truncated = strip_thinking(attempt.get("response", ""))
    if truncated:
        return "NON_EXECUTION", "unclosed thinking"
    if not text:
        return "NON_EXECUTION", "empty"
    if suite == "critic":
        hits = VERDICT.findall(text)
        if len(hits) != 1:
            return "NON_EXECUTION", "missing or ambiguous explicit verdict"
        return "EXECUTED", hits[0].upper()
    if not report_structure(text):
        return "NON_EXECUTION", "no report structure"
    return "EXECUTED", "REPORT"


def report_structure(text):
    """Require all eight canonical fields per block; content accuracy is separate."""
    for block in sb.split_reports(text):
        for label in sb.REQUIRED_LABELS:
            # The historical scorer accepts label presence and permits whitespace
            # across lines. Eligibility requires a value on this label's line.
            pattern = sb.label_line_re(label).pattern.replace(r"[\s|>]*", r"[\t |>]*").replace(r"\s*", r"[\t ]*")
            values = re.findall(pattern, block)
            if not values or not all(value.strip(" \t|*`_:") for value in values):
                return False
        fences = re.findall(r"```html[^\S\n]*\n(.*?)```", block, flags=re.I | re.S)
        if any(fragment.strip() for fragment in fences):
            continue
        snippet = re.search(r"(?im)^[\t ]*(?:#+[\t ]*)?(?:\*\*)?HTML Snippet(?:\*\*)?[\t ]*:?(?:\*\*)?[\t ]*(.*?)(?=^[\t ]*#+ |\Z)", block, flags=re.S)
        if not snippet or not (re.search(r"<[/!a-zA-Z][^>]*>", snippet[1]) or sb.NA_TOKENS.search(snippet[1])):
            return False
    return True


def evaluate_attempts(attempts, suite):
    selected = len(attempts) - 1
    status, reason = eligibility(attempts[selected], suite)
    return {"status": status, "verdict": reason if status == "EXECUTED" else None,
            "reason": reason, "selected_attempt": selected + 1,
            "first_attempt_completed": eligibility(attempts[0], suite)[0] == "EXECUTED",
            "retry_assisted_completed": status == "EXECUTED", "detection_credit": 0,
            "adjudicated_fabrication": None}


def score(cell_path, frozen, suite, fixture, eligible):
    output = io.StringIO()
    if suite == "critic":
        rubric_path = frozen / f"sources/critic/{fixture}.metadata.yaml"
        rubric = yaml.safe_load(rubric_path.read_text())
        with contextlib.redirect_stdout(output):
            so.score(str(cell_path), str(rubric_path))
        text, _ = strip_thinking(json.loads(cell_path.read_text())["response"])
        findings = [so.check_finding(text, item) for category in rubric.get("expected_findings", [])
                    if category.get("category") == "must_find" for item in category.get("items", [])]
        return {"existing_scorer_output": output.getvalue(), "must_found": sum(f["found"] for f in findings) if eligible else 0,
                "must_total": len(findings), "scorer_detected_findings": so.count_false_positives(text, so.check_verdict(text)),
                "adjudicated_fabrication": None}
    old_argv = sys.argv
    try:
        sys.argv = ["score_bugreport.py", str(cell_path), str(frozen / f"sources/bugreport/{fixture}.metadata.yaml")]
        with contextlib.redirect_stdout(output):
            sb.main()
    finally:
        sys.argv = old_argv
    return {"existing_scorer_output": output.getvalue(), "adjudicated_fabrication": None}


def cells(manifest, stage, draws):
    suite = "bugreport" if stage == "bugreport" else "critic"
    count = draws if stage == "clean" else 1
    return [(suite, fixture, draw) for fixture in manifest[stage] for draw in range(1, count + 1)]


def atomic_progress(path, data):
    temporary = path.with_suffix(".tmp")
    temporary.write_bytes(encoded(data))
    temporary.replace(path)


def validate_resume(path, contract):
    row = json.loads(path.read_text())
    if row.get("contract") != contract:
        raise ValueError(f"resume mismatch: {path}")
    if not row.get("outcome") or not row.get("attempts"):
        raise ValueError(f"missing outcomes: {path}")
    for record in row["attempts"]:
        receipt = path.parent / record["receipt"]
        if digest(receipt.read_bytes()) != record["sha256"]:
            raise ValueError(f"receipt hash mismatch: {receipt}")
    if digest(path.read_bytes()) != path.with_suffix(".sha256").read_text().strip():
        raise ValueError(f"cell hash mismatch: {path}")
    return row


def run(args):
    manifest = verify(args.out)
    url, shared = tr.local_url(args.url), tr.local_url(args.shared_url)
    if url == shared:
        raise ValueError("dedicated generation runtime must differ from shared runtime")
    options = {**OPTIONS, "num_predict": args.num_predict}
    if options != manifest["options"]:
        raise ValueError("run options must match frozen common comparison options")
    if args.num_predict < rb.RESPONSE_RESERVE:
        raise ValueError("output budget must be at least RESPONSE_RESERVE")
    supplied = json.loads(Path(args.identity_file).read_text()) if args.identity_file else None
    runtime = tr.identity(args.backend, url, args.model, supplied)
    if not isinstance(runtime["declared_context_length"], int) or runtime["declared_context_length"] < options["num_ctx"]:
        raise ValueError("declared ceiling cannot qualify the common context")
    lane_id = digest(encoded({"model": args.model, "backend": args.backend}))[:16]
    lane = Path(args.out) / "runs" / lane_id
    lane.mkdir(parents=True, exist_ok=True)
    identity = {"runtime": runtime, "options": options, "backend": args.backend, "shared_url": shared,
                "condition": manifest.get("condition", "neutral-H1-blind-no-features-202610"), "source": manifest["source"],
                "freeze_hash": digest((Path(args.out) / "freeze/manifest.json").read_bytes())}
    identity_path = lane / "identity.json"
    if identity_path.exists():
        if json.loads(identity_path.read_text()) != identity:
            raise ValueError("lane identity/options mismatch; use separate output directory")
    else:
        exclusive(identity_path, identity)
    progress = {"identity": lane_id, "stage": args.stage, "planned_cells": len(cells(manifest, args.stage, args.draws)), "completed": []}
    frozen = Path(args.out) / "freeze"
    for suite, fixture, draw in cells(manifest, args.stage, args.draws):
        key = f"{suite}/{fixture}"
        stem = f"{suite}-{fixture}-draw{draw}"
        path = lane / (stem + ".json")
        contract = {"identity_hash": digest(encoded(identity)), "prompt_hash": manifest["prompts"][key],
                    "suite": suite, "fixture": fixture, "draw": draw}
        if path.exists():
            validate_resume(path, contract)
            progress["completed"].append(stem)
            atomic_progress(lane / "progress.json", progress)
            continue
        if list(lane.glob(stem + "-*.ndjson")):
            raise ValueError(f"incomplete existing cell refuses overwrite: {stem}")
        prompt = json.loads((frozen / f"prompts/{key}.json").read_text())
        before, busy = tr.residency(url, shared, args.backend, args.model)
        if busy:
            exclusive(lane / f"{stem}-blocked-{uuid.uuid4().hex}.json", {"status": "BLOCKED", "before": before, "contract": contract})
            progress["blocked"] = stem
            atomic_progress(lane / "progress.json", progress)
            raise RuntimeError("shared runtime busy or dedicated runtime has foreign model; BLOCKED receipt retained")
        overflow, estimated = rb.context_overflow(prompt["system"], prompt["prompt"], options["num_ctx"], runtime["declared_context_length"])
        if overflow:
            exclusive(lane / f"{stem}-blocked-{uuid.uuid4().hex}.json",
                      {"status": "INVALID", "reason": "conservative context guard overflow", "estimated": estimated, "contract": contract})
            progress["invalid"] = stem
            atomic_progress(lane / "progress.json", progress)
            raise ValueError(f"context guard overflow: {stem} estimated={estimated}; INVALID receipt retained")
        records, attempts = [], []
        def generate(label, probe=False):
            admission, occupied = tr.residency(url, shared, args.backend, args.model)
            if occupied:
                exclusive(lane / f"{stem}-{label}-blocked-{uuid.uuid4().hex}.json",
                          {"status": "BLOCKED", "before": admission, "contract": contract})
                raise RuntimeError("runtime occupied immediately before generation; BLOCKED")
            if args.backend == "ollama" and not probe and not offload_verified({"snapshots": [admission]}, args.model):
                exclusive(lane / f"{stem}-{label}-blocked-{uuid.uuid4().hex}.json",
                          {"status": "INVALID", "reason": "full offload not verified at scored admission", "before": admission, "contract": contract})
                raise ValueError("full offload not verified immediately before scored generation; INVALID receipt retained")
            receipt_path = lane / f"{stem}-{label}.ndjson"
            with receipt_path.open("x") as receipt:
                receipt.write(json.dumps({"kind": "admission_residency", "value": admission}) + "\n")
                result = tr.stream(url, shared, args.backend, args.model,
                                   tr.payload(args.backend, args.model, prompt, options, probe), receipt)
            if args.backend == "ollama" and not probe:
                result["snapshots"] = [admission] + result.get("snapshots", [])
                result["offload_verified"] = offload_verified(result, args.model)
            records.append({"receipt": receipt_path.name, "sha256": digest(receipt_path.read_bytes()), "label": label})
            return result
        probe = generate("probe", True)
        count = (probe.get("terminal") or {}).get("prompt_eval_count") if args.backend == "ollama" else probe.get("usage", {}).get("prompt_tokens")
        problem = qualify_probe(probe, count, args.backend, args.model, options)
        if problem:
            attempts = [probe]
            outcome = {"status": "INVALID", "reason": problem, "detection_credit": 0,
                       "first_attempt_completed": False, "retry_assisted_completed": False}
        else:
            for number in range(1, 4):
                attempts.append(generate(f"attempt{number}"))
                status, reason = eligibility(attempts[-1], suite)
                if reason != "empty" or status != "NON_EXECUTION":
                    break
            outcome = evaluate_attempts(attempts, suite)
        row = {"contract": contract, "before": before, "probe": probe, "attempts": records,
               "attempt_outcomes": attempts, "outcome": outcome, "response": attempts[-1].get("response", "")}
        # Score through an isolated temporary file; publish the final cell exactly once.
        scoring_path = lane / f"{stem}.scoring.tmp"
        exclusive(scoring_path, row)
        try:
            row["scoring"] = score(scoring_path, frozen, suite, fixture, outcome["status"] == "EXECUTED")
            outcome["detection_credit"] = row["scoring"].get("must_found", 0)
        finally:
            scoring_path.unlink()
        exclusive(path, row)
        exclusive(path.with_suffix(".sha256"), (digest(path.read_bytes()) + "\n").encode())
        progress["completed"].append(stem)
        atomic_progress(lane / "progress.json", progress)
    return progress


def qualify_probe(probe, count, backend, model, options):
    if probe.get("exception") or probe.get("contaminated") or not probe.get("terminal"):
        return "probe failed or contaminated"
    if not isinstance(count, int) or count <= 0 or count + rb.RESPONSE_RESERVE > options["num_ctx"]:
        return "measured prompt count missing or reserve exhausted"
    if backend == "ollama":
        if not offload_verified(probe, model, allow_cold_start=True):
            return "full offload not verified by own residency metadata"
    return None


def offload_verified(attempt, model, allow_cold_start=False):
    snapshots = attempt.get("snapshots", [])
    loaded = False
    for snap in snapshots:
        try:
            entries = tr.resident_models(snap.get("own"))
        except (ValueError, AttributeError):
            return False
        if not entries:
            if allow_cold_start and not loaded:
                continue
            return False
        for entry in entries:
            size, vram = entry.get("size"), entry.get("size_vram")
            if (entry.get("name", entry.get("model")) not in rb._tag_variants(model)
                    or not isinstance(size, (int, float)) or isinstance(size, bool) or size <= 0
                    or not isinstance(vram, (int, float)) or isinstance(vram, bool) or not vram >= size):
                return False
        loaded = True
    return loaded


def summary(out):
    manifest = verify(out)
    result = {"source": manifest["source"], "condition": manifest.get("condition", "neutral-H1-blind-no-features-202610"), "lanes": {}}
    for lane in sorted((Path(out) / "runs").glob("*")):
        identity = json.loads((lane / "identity.json").read_text())
        identity_hash = digest(encoded(identity))
        if identity["options"] != manifest["options"] or identity["freeze_hash"] != digest((Path(out) / "freeze/manifest.json").read_bytes()):
            raise ValueError("summary identity/options/freeze mismatch")
        rows = []
        for path in sorted(lane.glob("*.json")):
            if path.name in ("identity.json", "progress.json") or "-blocked" in path.name:
                continue
            contract = json.loads(path.read_text())["contract"]
            expected = {**contract, "identity_hash": identity_hash,
                        "prompt_hash": manifest["prompts"][f'{contract["suite"]}/{contract["fixture"]}']}
            rows.append(validate_resume(path, expected))
        stats = {"cells": len(rows), "unique_fixtures": len({r["contract"]["fixture"] for r in rows}),
                 "ACCEPT": 0, "ACCEPT-WITH-RESERVATIONS": 0, "REVISE+REJECT": 0, "unparseable": 0,
                 "INVALID": 0, "NON_EXECUTION": 0, "first_attempt_completed": 0,
                 "retry_assisted_completed": 0, "must_found": 0, "must_total": 0,
                 "adjudicated_fabrication": None, "adjudication_required": True,
                 "screen_complete": sum(r["contract"]["fixture"] in manifest["screen"] and r["contract"]["suite"] == "critic" and r["contract"]["draw"] == 1 for r in rows) == len(manifest["screen"])}
        indexed = {(r["contract"]["suite"], r["contract"]["fixture"], r["contract"]["draw"]): r for r in rows}
        stats["screen_execution_complete"] = all(indexed.get(key, {}).get("outcome", {}).get("status") == "EXECUTED"
                                                  for key in cells(manifest, "screen", 3))
        stats["stages"] = {stage: stage_summary(manifest, stage, indexed, Path(out) / "freeze")
                           for stage in ("screen", "clean", "bugreport")}
        for row in rows:
            outcome = row["outcome"]
            for key in ("first_attempt_completed", "retry_assisted_completed"):
                stats[key] += bool(outcome.get(key))
            verdict = outcome.get("verdict")
            if verdict in ("ACCEPT", "ACCEPT-WITH-RESERVATIONS"):
                stats[verdict] += 1
            elif verdict in ("REVISE", "REJECT"):
                stats["REVISE+REJECT"] += 1
            elif row["contract"]["suite"] == "critic":
                stats["unparseable"] += 1
            if outcome["status"] in ("INVALID", "NON_EXECUTION"):
                stats[outcome["status"]] += 1
            stats["must_found"] += row["scoring"].get("must_found", 0)
            stats["must_total"] += row["scoring"].get("must_total", 0)
        result["lanes"][lane.name] = stats
    return result


def stage_summary(manifest, stage, indexed, frozen):
    planned = cells(manifest, stage, 3)
    stats = {"planned_cells": len(planned), "unique_fixtures": len(manifest[stage]),
             "completed_cells": 0, "missing_cells": 0, "executed": 0,
             "must_found": 0, "must_total": 0, "ACCEPT": 0,
             "ACCEPT-WITH-RESERVATIONS": 0, "REVISE+REJECT": 0, "unparseable": 0,
             "first_attempt_completed": 0, "retry_assisted_completed": 0,
             "adjudication_required": True}
    for key in planned:
        suite, fixture, _ = key
        if suite == "critic":
            rubric = yaml.safe_load((frozen / f"sources/critic/{fixture}.metadata.yaml").read_text())
            stats["must_total"] += sum(len(category.get("items", [])) for category in rubric.get("expected_findings", [])
                                       if category.get("category") == "must_find")
        row = indexed.get(key)
        if row is None:
            stats["missing_cells"] += 1
            continue
        stats["completed_cells"] += 1
        outcome = row["outcome"]
        stats["executed"] += outcome["status"] == "EXECUTED"
        for name in ("first_attempt_completed", "retry_assisted_completed"):
            stats[name] += bool(outcome.get(name))
        stats["must_found"] += row["scoring"].get("must_found", 0)
        verdict = outcome.get("verdict")
        if verdict in ("ACCEPT", "ACCEPT-WITH-RESERVATIONS"):
            stats[verdict] += 1
        elif verdict in ("REVISE", "REJECT"):
            stats["REVISE+REJECT"] += 1
        elif suite == "critic":
            stats["unparseable"] += 1
    return stats
