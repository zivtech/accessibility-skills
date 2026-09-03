#!/usr/bin/env python3
"""Score the features-section A/B lane (issue #51 leak class 2).

45 of 50 critic fixtures show the model an `## Accessibility Features Present`
section above the blind cut line. Issue #51 argues that section is what the
`false_positive_trap` dimension actually measures. Measured 2026-09-03:
`false_positive_trap` is declared in all 50 rubrics and read by no scorer at
all — nor are `llm_judge`, `hybrid_weights` or `scoring_method`. So this
scorer does not report a trap score; it reports the consequence the trap
dimension was supposed to stand for.

CLEAN fixtures (expected verdict ACCEPT) carry the measurement: with the
section removed, does the model still accept correct code, or does it start
raising findings? BUG fixtures carry the control: must-find should be
unaffected by removing a list of things that are fine.

Usage:
    python3 ollama/score_featurehint.py <results_dir> [--json out.json]
"""

import glob
import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from score_output import (  # noqa: E402
    check_finding,
    check_verdict,
    count_false_positives,
    load_response,
)

BASE_DIR = os.path.dirname(__file__)
RUBRICS_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "a11y-critic", "rubrics")
NAME_RE = re.compile(
    r"ollama-featurehint-(?P<cond>withfeatures|nofeatures)-(?P<rest>.+)"
    r"-d(?P<draw>\d+)-response\.json$"
)
CONDITIONS = ("withfeatures", "nofeatures")


def fixture_ids():
    sys.path.insert(0, BASE_DIR)
    import run_benchmark as rb

    return {
        **{f: "CLEAN" for f in rb.CLEAN_FIXTURES},
        **{f: "HAS-BUGS" for f in rb.HAS_BUGS_FIXTURES},
        **{f: "FLAWED" for f in rb.FLAWED_FIXTURES},
        **{f: "ADVERSARIAL" for f in rb.ADVERSARIAL_FIXTURES},
    }


def must_find_items(fixture):
    with open(os.path.join(RUBRICS_DIR, f"{fixture}.rubric.yaml")) as f:
        rubric = yaml.safe_load(f)
    for block in rubric.get("expected_findings", []):
        if block.get("category") == "must_find":
            return block.get("items") or []
    return []


def score_dir(results_dir):
    tiers, rows, cache = fixture_ids(), [], {}
    for path in sorted(glob.glob(os.path.join(results_dir, "ollama-featurehint-*.json"))):
        m = NAME_RE.search(os.path.basename(path))
        if not m:
            continue
        rest = m.group("rest")
        candidates = [f for f in tiers if rest.startswith(f + "-")]
        if not candidates:
            sys.exit(f"{os.path.basename(path)}: no known fixture id in {rest!r}")
        fixture = max(candidates, key=len)
        text, truncated = load_response(path)
        verdict = check_verdict(text)
        fp = count_false_positives(text, verdict)
        items = cache.setdefault(fixture, must_find_items(fixture))
        rows.append({
            "fixture": fixture,
            "tier": tiers[fixture],
            "condition": m.group("cond"),
            "draw": int(m.group("draw")),
            "verdict": verdict,
            "structured_findings": fp["structured_findings"],
            "must_found": sum(bool(check_finding(text, i)["found"]) for i in items),
            "must_total": len(items),
            "truncated": truncated,
            "chars": len(text),
        })
    return rows


def cell(rows):
    n = len(rows)
    if not n:
        return None
    return {
        "draws": n,
        "accept": sum(r["verdict"] == "ACCEPT" for r in rows),
        "accept_rate": sum(r["verdict"] == "ACCEPT" for r in rows) / n,
        "findings_mean": sum(r["structured_findings"] for r in rows) / n,
        "must_found": sum(r["must_found"] for r in rows),
        "must_total": sum(r["must_total"] for r in rows),
        "truncated": sum(r["truncated"] for r in rows),
    }


def summarize(rows):
    by = {}
    for r in rows:
        by.setdefault((r["tier"], r["fixture"], r["condition"]), []).append(r)
    out = {"fixtures": {}, "tiers": {}}
    for tier in ("CLEAN", "ADVERSARIAL", "FLAWED", "HAS-BUGS"):
        fx = sorted({f for t, f, _ in by if t == tier})
        if not fx:
            continue
        print(f"\n=== {tier} "
              + ("(expected ACCEPT — the 'don't flag correct code' claim)"
                 if tier == "CLEAN" else "(control)"))
        print(f"{'fixture':40} {'ACCEPT with':>12} {'ACCEPT without':>15} "
              f"{'findings w/':>12} {'findings w/o':>13}")
        for f in fx:
            c = {k: cell(by.get((tier, f, k), [])) for k in CONDITIONS}
            out["fixtures"][f] = {"tier": tier, **c}
            if not all(c.values()):
                print(f"{f:40}   incomplete")
                continue
            print(f"{f:40} {c['withfeatures']['accept']:>4}/"
                  f"{c['withfeatures']['draws']:<7} "
                  f"{c['nofeatures']['accept']:>7}/{c['nofeatures']['draws']:<7}"
                  f"{c['withfeatures']['findings_mean']:>12.1f}"
                  f"{c['nofeatures']['findings_mean']:>13.1f}")
        agg = {}
        for k in CONDITIONS:
            rs = [r for r in rows if r["tier"] == tier and r["condition"] == k]
            agg[k] = cell(rs)
        out["tiers"][tier] = agg
        if all(agg.values()):
            print(f"{'TIER TOTAL':40} {agg['withfeatures']['accept']:>4}/"
                  f"{agg['withfeatures']['draws']:<7} "
                  f"{agg['nofeatures']['accept']:>7}/{agg['nofeatures']['draws']:<7}"
                  f"{agg['withfeatures']['findings_mean']:>12.1f}"
                  f"{agg['nofeatures']['findings_mean']:>13.1f}")
            if agg["withfeatures"]["must_total"]:
                for k in CONDITIONS:
                    a = agg[k]
                    print(f"    must-find {k:14} {a['must_found']}/{a['must_total']}"
                          f" = {a['must_found']/a['must_total']:.1%}")
            d = agg["withfeatures"]["accept_rate"] - agg["nofeatures"]["accept_rate"]
            print(f"    ACCEPT-rate delta (with - without): {d:+.1%}")
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    rows = score_dir(sys.argv[1])
    if not rows:
        sys.exit("no features-section response files found")
    summary = summarize(rows)
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        with open(out, "w") as f:
            json.dump({"rows": rows, "summary": summary}, f, indent=2, sort_keys=True)
        print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
