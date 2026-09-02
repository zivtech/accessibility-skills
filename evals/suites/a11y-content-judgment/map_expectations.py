#!/usr/bin/env python3
"""Map a fixture's blind-authored expectations.yaml onto the unit ids the
skill's builder emitted, and write the triplet's machine halves:
fixtures/<id>.metadata.yaml and rubrics/<id>.rubric.yaml, plus a mapping log
under sources/<id>/build/mapping.log.

This is the one non-blind step of the lane and it is a LOOKUP, not a
judgment: each expectation names an element by view + type + text/href/alt,
and this script finds the emitted unit with those values. Unmatched or
ambiguous locators are authoring errors — logged, fixed in the source before
the freeze, never resolved by editing the expectation to fit a row.

Rows the builder emitted that the blind author did not list (incidental
nav/footer links, h1s) become calibration-tier "incidental" rows: expected
yes, reported by the scorer, never counted toward status.

    python3 evals/suites/a11y-content-judgment/map_expectations.py <fixture-id> [--fabricated a,b,c]
"""
import json
import os
import re
import sys
from urllib.parse import urlparse

import yaml

SUITE = os.path.dirname(os.path.abspath(__file__))
WS = re.compile(r"\s+")


def norm(s):
    return WS.sub(" ", str(s or "")).strip().lower()


def load(fid):
    src = os.path.join(SUITE, "sources", fid)
    with open(os.path.join(src, "expectations.yaml")) as f:
        exp = yaml.safe_load(f) or []
    with open(os.path.join(src, "build", "judgment-units.json")) as f:
        units = json.load(f)
    units = units.get("units") if isinstance(units, dict) and "units" in units else units
    with open(os.path.join(src, "build", "rows.jsonl")) as f:
        rows = [json.loads(l) for l in f if l.strip()]
    return src, exp, units, rows


def path_of(href):
    try:
        u = urlparse(href)
        return (u.path or "") + (("?" + u.query) if u.query else "") + (("#" + u.fragment) if u.fragment else "")
    except Exception:
        return href or ""


def usable_href(h):
    return h if h and h.startswith("/") else None


def candidates(e, units):
    t = e["type"]
    loc = e.get("locator") or {}
    text = norm(loc.get("text"))
    prose = text.startswith("(")          # a descriptor, not the element's text
    href = usable_href(loc.get("href"))    # "not applicable …" prose is ignored
    out = []
    for u in units:
        if u["type"] != t:
            continue
        if e.get("view") and e["view"] not in (u.get("views") or []):
            continue
        if t == "title":
            out.append(u)
        elif t in ("heading", "field"):
            name = norm(u.get("name"))
            if prose and "empty" in text and t == "heading" and "heading_empty" in (u.get("flags") or []):
                out.append(u)
            elif text and not prose and (name == text or (t == "field" and text in norm(u.get("detail")))):
                out.append(u)
            elif not text and t == "heading" and "heading_empty" in (u.get("flags") or []):
                out.append(u)
        elif t == "link":
            if text and not prose and norm(u.get("name")) != text:
                continue
            if href and path_of(u.get("href")).rstrip("/") != href.rstrip("/"):
                continue
            out.append(u)
        elif t == "image":
            name = norm(u.get("name"))
            detail = norm(u.get("detail"))
            if prose:
                if "functional" not in text and ("no alt" in text and "alt empty" not in text) and name != "(no alt attribute)":
                    continue
                if ("alt empty" in text or "empty alt" in text) and name != '(alt="")':
                    continue
                if "functional" in text and "role:functional" not in detail:
                    continue
                if "decorative" in text and "role:decorative" not in detail:
                    continue
            elif text and name != text:
                continue
            if loc.get("src") and loc["src"] not in (u.get("detail") or "") and loc["src"] not in (u.get("href") or ""):
                continue
            out.append(u)
        elif t == "ident":
            upath = "/" + (u.get("href", "").split("/", 1)[1] if "/" in u.get("href", "") else "")
            if href and upath.rstrip("/") != href.rstrip("/"):
                continue
            out.append(u)
    if len(out) > 1 and e.get("evidence_contains"):
        ev = [norm(x) for x in e["evidence_contains"]]
        narrowed = [u for u in out if all(x in norm(u.get("context")) + " " + norm(u.get("name")) for x in ev)]
        if narrowed:
            out = narrowed
    nth = loc.get("nth")
    if nth and len(out) >= nth:
        return [out[nth - 1]]
    return out


def rubric_for(fid, meta):
    n_no = sum(1 for r in meta["rows"].values() if r["expected"] == "no" and r["tier"] == "must")
    n_yes = sum(1 for r in meta["rows"].values() if r["expected"] == "yes" and r["tier"] == "must")
    n_cal = sum(1 for r in meta["rows"].values() if r["tier"] == "calibration")
    return {
        "fixture_id": fid,
        "suite": "a11y-content-judgment",
        "rubric_version": "1.0",
        "scoring_method": "rule_based",
        "scorer": "ollama/score_content_judgment.py",
        "dimensions": [
            {"id": "c1_one_line_per_id", "name": "Exactly one JSON line per input id; no extras", "tier": "must", "priced_by": "contract"},
            {"id": "c2_enums_and_author", "name": "judgment in {yes,no,unsure}; drafted_by present", "tier": "must", "priced_by": "contract"},
            {"id": "c3_shape", "name": "confidence enum; needs_human on unsure; empty fix on yes; rationale <= 25 words", "tier": "should", "priced_by": "contract"},
            {"id": "r1_defects_found", "name": f"All {n_no} planted defective must-rows judged no (unsure only where unsure_ok)", "tier": "must", "priced_by": "rubric"},
            {"id": "r2_no_false_alarm", "name": f"None of the {n_yes} planted clean must-rows judged no; unsure on them is a should-tier over-hedge", "tier": "must", "priced_by": "rubric",
             "note": "The half that matters more: a judge that flags everything is dead."},
            {"id": "r3_calibration_rows", "name": f"{n_cal} calibration-tier rows (borderline, convention-dependent, incidental) reported, never counted", "tier": "info", "priced_by": "rubric"},
            {"id": "r4_fabricated_tokens", "name": "No metadata-listed invented value in any rationale or fix", "tier": "must", "priced_by": "rubric"},
            {"id": "r5_quoted_spans", "name": "Quoted spans >= 3 words trace to the row (should-tier by origin-run calibration: recall 2/6, 8.5 % false-fire)", "tier": "should", "priced_by": "rubric"},
            {"id": "r6_loses", "name": "A no-rationale names what the person loses (blind-authored phrases; uncalibrated WARN rate)", "tier": "should", "priced_by": "rubric"},
            {"id": "r7_pattern_groups", "name": "Identical constructs get one verdict", "tier": "should", "priced_by": "rubric"},
        ],
        "status_semantics": {
            "PASS": "All must-tier checks pass, no fabrication",
            "WARN": "Musts pass; should-tier gaps listed by the scorer",
            "FAIL": "Any must-tier miss or any fabrication",
        },
        "expected_status_competent": "PASS",
        "conditions": {
            "cj": ".claude/skills/a11y-content-judgment/references/judgment-rubric.md as system prompt",
            "cj-baseline": "identical fixture, no system prompt (output contract only, from the task line)",
        },
        "known_judgment_calls": [
            "Calibration-tier rows never move the status; read their mismatches before adjudicating a WARN.",
            "A demonstrated row-evidence defect after the freeze makes the row invalid (excluded + disclosed); it is never a model miss and never a silent edit.",
            "Scorer statuses are detector output, not verdict authority.",
        ],
    }


def main():
    fid = sys.argv[1]
    fab = None
    if "--fabricated" in sys.argv:
        fab = [t.strip() for t in sys.argv[sys.argv.index("--fabricated") + 1].split(",") if t.strip()]
    src, exp, units, rows = load(fid)
    over = {}
    if os.path.exists(os.path.join(src, "overrides.yaml")):
        with open(os.path.join(src, "overrides.yaml")) as f:
            over = yaml.safe_load(f) or {}
    fab = fab or list(over.get("fabricated_tokens") or [])
    det = {"row_counts": {}, "absent_ident_hrefs": [], "absent_link_hrefs": [], "nav_consistency": {}}
    log, meta_rows, seen = [], {}, {}
    for e in exp:
        loc = e.get("locator") or {}
        note = (e.get("note") or "").lower()
        if e["type"] == "nav":
            # deterministic layer: pseudo-hrefs never become ident rows; nav order per view
            if str(loc.get("href", "")).startswith("javascript"):
                det["absent_ident_hrefs"].append("javascript")
                log.append(f"deterministic: no ident row for pseudo-href ({e.get('view')} {loc.get('text')!r})")
            elif "no shared" in note:
                det["nav_consistency"][e["view"]] = {"note_contains": "no shared navigation"}
                log.append(f"deterministic: nav note for {e.get('view')} must say no shared navigation")
            else:
                det["nav_consistency"][e["view"]] = {"order_consistent": True}
                log.append(f"deterministic: nav order consistent on {e.get('view')}")
            continue
        c = candidates(e, units)
        tag = f"{e.get('view')}/{e['type']}/{json.dumps(e.get('locator'), ensure_ascii=False)}"
        if not c and e["type"] == "ident" and "determin" in note and usable_href(loc.get("href")):
            det["absent_ident_hrefs"].append(usable_href(loc.get("href")))
            log.append(f"deterministic: no ident row for paired-column destination {loc.get('href')}")
            continue
        if len(c) != 1:
            log.append(f"{'UNMATCHED' if not c else 'AMBIGUOUS(' + str(len(c)) + ')'}: {tag}")
            continue
        uid = c[0]["id"]
        if uid in seen:
            log.append(f"DUPLICATE-TARGET {uid}: {tag} (already {seen[uid]})")
            continue
        seen[uid] = tag
        meta_rows[uid] = {
            "expected": e["expected"], "tier": e.get("tier", "must"), "unsure_ok": bool(e.get("unsure_ok", False)),
            "reference": e.get("reference", ""), "polarity": e.get("polarity", ""),
            "clause1_evidence": bool(e.get("clause1_evidence", False)),
            "loses": list(e.get("loses") or []), "evidence_contains": list(e.get("evidence_contains") or []),
            "evidence_absent": list(e.get("evidence_absent") or []), "pattern_group": e.get("pattern_group"),
            "note": e.get("note", ""), "locator": {"view": e.get("view"), **(e.get("locator") or {})},
        }
        log.append(f"{uid} <- {tag}")
    for r in rows:
        if r["id"] not in meta_rows:
            meta_rows[r["id"]] = {
                "expected": "yes", "tier": "calibration", "unsure_ok": True, "reference": "incidental (unplanted element; blind author did not list it)",
                "polarity": "sufficient", "clause1_evidence": False, "loses": [], "evidence_contains": [], "evidence_absent": [],
                "pattern_group": None, "note": "incidental", "locator": {},
            }
            log.append(f"{r['id']} incidental -> calibration yes ({r['type']} {r.get('name')!r})")
    # maintainer overrides (sources/<id>/overrides.yaml, receipted in mapping.log):
    # row patches never change a planted verdict's tier upward — they move
    # convention-dependent rows to calibration, or give an incidental twin of
    # a planted element the value the planted row carries.
    for rid, patch in (over.get("rows") or {}).items():
        if rid not in meta_rows:
            log.append(f"OVERRIDE-TARGET-MISSING {rid}")
            continue
        if patch.get("tier") == "must" and meta_rows[rid].get("tier") != "must":
            log.append(f"OVERRIDE-REFUSED {rid}: overrides may not promote a row to must")
            continue
        if "expected" in patch and meta_rows[rid].get("note") != "incidental" and patch["expected"] != meta_rows[rid].get("expected"):
            log.append(f"OVERRIDE-REFUSED {rid}: overrides may not change the blind author's expected verdict (only incidental rows take a value)")
            continue
        meta_rows[rid].update(patch)
        meta_rows[rid]["note"] = f"[maintainer override] {patch.get('note', '')} | was: {meta_rows[rid].get('note', '')}".strip()
        log.append(f"{rid} OVERRIDE {json.dumps(patch, ensure_ascii=False)}")
    for rid, reason in (over.get("invalid") or {}).items():
        if rid in meta_rows:
            meta_rows[rid]["invalid"] = True
            meta_rows[rid]["invalid_reason"] = reason
            log.append(f"{rid} INVALID (maintainer override): {reason}")
        else:
            log.append(f"OVERRIDE-TARGET-MISSING {rid}")
    with open(os.path.join(src, "scenario.md")) as f:
        scenario = f.read().strip()
    meta = {
        "fixture_id": fid, "suite": "a11y-content-judgment",
        "input_format": "content-judgment batch rows (the skill's own inventory + builder output over blind-authored HTML) + product/audience note",
        "difficulty": "CLEAN" if all(r["expected"] == "yes" for r in meta_rows.values()) else "PLANTED",
        "description": scenario,
        "fabricated_tokens": fab, "fabrication_quoted_span_tier": "should",
        "deterministic": {**det, "absent_ident_hrefs": sorted(set(det["absent_ident_hrefs"])), "absent_link_hrefs": sorted(set(det["absent_link_hrefs"]))},
        "rows": {k: meta_rows[k] for k in sorted(meta_rows)},
        "input_rows": rows,
    }
    counts = {}
    for r in rows:
        counts[r["type"]] = counts.get(r["type"], 0) + 1
    meta["deterministic"]["row_counts"] = counts
    with open(os.path.join(SUITE, "fixtures", f"{fid}.metadata.yaml"), "w") as f:
        yaml.safe_dump(meta, f, sort_keys=False, allow_unicode=True, width=100)
    with open(os.path.join(SUITE, "rubrics", f"{fid}.rubric.yaml"), "w") as f:
        yaml.safe_dump(rubric_for(fid, meta), f, sort_keys=False, allow_unicode=True, width=100)
    with open(os.path.join(src, "build", "mapping.log"), "w") as f:
        f.write("\n".join(log) + "\n")
    bad = [l for l in log if l.startswith(("UNMATCHED", "AMBIGUOUS", "DUPLICATE", "OVERRIDE"))]
    n_planted = sum(1 for e in exp if e["type"] != "nav")
    print(f"{fid}: {n_planted} expectations, {n_planted - len(bad)} mapped, {len(bad)} problems, "
          f"{sum(1 for l in log if 'incidental' in l)} incidental rows; rows {counts}")
    for b in bad:
        print("  " + b)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
