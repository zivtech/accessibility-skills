#!/usr/bin/env python3
"""Score the title-hint A/B lane (issue #51 step 2).

Every fixture's H1 sits above the blind cut line, so it reaches the model in
every prompt-based lane, and 52 of the corpus's 77 titles name the defect they
plant. This scorer answers the only question that decides whether the larger
allowlist-envelope rewrite is worth a corpus re-draw: how much of the published
must-find rate is the title?

It reuses score_output.check_finding verbatim — the same matcher every
published row was scored with — so the two conditions are comparable to the
existing numbers and to each other.

Usage:
    python3 ollama/score_titlehint.py <results_dir> [--json out.json]

Reads ollama-titlehint-{condition}-{fixture}-{model}-d{n}-response.json.
"""

import glob
import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from score_output import check_finding, load_response  # noqa: E402

BASE_DIR = os.path.dirname(__file__)
RUBRICS_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "a11y-critic", "rubrics")
TITLE_MANIFEST = os.path.join(BASE_DIR, "..", "evals", "fixture-title-manifest.yaml")
# Fixture ids and model tags both contain hyphens, so the fixture cannot be
# delimited by a pattern — it is resolved against the manifest's known ids
# (longest match wins). A greedy/non-greedy split here silently mis-attributes
# rows instead of failing, which is worse than a crash.
NAME_RE = re.compile(
    r"ollama-titlehint-(?P<cond>titled|neutral)-(?P<rest>.+)"
    r"-d(?P<draw>\d+)-response\.json$"
)


def must_find_items(fixture):
    with open(os.path.join(RUBRICS_DIR, f"{fixture}.rubric.yaml")) as f:
        rubric = yaml.safe_load(f)
    for block in rubric.get("expected_findings", []):
        if block.get("category") == "must_find":
            return block.get("items") or []
    return []


def titles():
    with open(TITLE_MANIFEST) as f:
        rows = yaml.safe_load(f)["suites"]["a11y-critic"]["fixtures"]
    return {k: v for k, v in rows.items()}


def score_dir(results_dir):
    rows, items_cache, title_rows = [], {}, titles()
    for path in sorted(glob.glob(os.path.join(results_dir, "ollama-titlehint-*.json"))):
        m = NAME_RE.search(os.path.basename(path))
        if not m:
            continue
        rest = m.group("rest")
        candidates = [f for f in title_rows if rest.startswith(f + "-")]
        if not candidates:
            sys.exit(f"{os.path.basename(path)}: no known fixture id in {rest!r}")
        fixture = max(candidates, key=len)
        model = rest[len(fixture) + 1:]
        items = items_cache.setdefault(fixture, must_find_items(fixture))
        if not items:
            sys.exit(f"{fixture}: rubric declares no must_find items")
        text, truncated = load_response(path)
        found = [bool(check_finding(text, i)["found"]) for i in items]
        # A response that quotes the fixture's own H1 can satisfy a keyword
        # match without having detected anything — a confound that only ever
        # inflates the titled arm, so it is counted, not assumed absent.
        real_title = title_rows[fixture]["title"]
        rows.append({
            "fixture": fixture,
            "condition": m.group("cond"),
            "model": model,
            "draw": int(m.group("draw")),
            "found": sum(found),
            "total": len(found),
            "per_item": found,
            "truncated": truncated,
            "chars": len(text),
            "echoes_title": real_title.lower() in text.lower(),
        })
    return rows


def summarize(rows):
    by = {}
    for r in rows:
        by.setdefault((r["fixture"], r["condition"]), []).append(r)
    fixtures = sorted({f for f, _ in by})
    out = {"fixtures": {}, "totals": {}}
    print(f"{'fixture':44} {'titled':>16} {'neutral':>16} {'delta':>8}")
    for fx in fixtures:
        cells = {}
        for cond in ("titled", "neutral"):
            rs = by.get((fx, cond), [])
            f, t = sum(r["found"] for r in rs), sum(r["total"] for r in rs)
            cells[cond] = {
                "draws": len(rs), "found": f, "total": t,
                "rate": f / t if t else None,
                "truncated": sum(r["truncated"] for r in rs),
                "title_echoes": sum(r["echoes_title"] for r in rs),
            }
        d = (cells["titled"]["rate"] or 0) - (cells["neutral"]["rate"] or 0)
        out["fixtures"][fx] = cells
        print(f"{fx:44} {cells['titled']['found']:5d}/{cells['titled']['total']:<4d}"
              f"{cells['titled']['rate']:>6.0%} "
              f"{cells['neutral']['found']:5d}/{cells['neutral']['total']:<4d}"
              f"{cells['neutral']['rate']:>6.0%} {d:>+8.0%}")
    for cond in ("titled", "neutral"):
        f = sum(c[cond]["found"] for c in out["fixtures"].values())
        t = sum(c[cond]["total"] for c in out["fixtures"].values())
        e = sum(c[cond]["title_echoes"] for c in out["fixtures"].values())
        tr = sum(c[cond]["truncated"] for c in out["fixtures"].values())
        out["totals"][cond] = {"found": f, "total": t, "rate": f / t,
                               "title_echoes": e, "truncated": tr}
    ti, ne = out["totals"]["titled"], out["totals"]["neutral"]
    out["totals"]["delta"] = ti["rate"] - ne["rate"]
    print()
    print(f"TOTAL titled  {ti['found']:4d}/{ti['total']:<4d} {ti['rate']:6.1%}"
          f"   (title echoed in {ti['title_echoes']} responses, {ti['truncated']} truncated)")
    print(f"TOTAL neutral {ne['found']:4d}/{ne['total']:<4d} {ne['rate']:6.1%}"
          f"   (title echoed in {ne['title_echoes']} responses, {ne['truncated']} truncated)")
    print(f"DELTA (titled - neutral): {out['totals']['delta']:+.1%}")
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    rows = score_dir(sys.argv[1])
    if not rows:
        sys.exit("no title-hint response files found")
    summary = summarize(rows)
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        with open(out, "w") as f:
            json.dump({"rows": rows, "summary": summary}, f, indent=2, sort_keys=True)
        print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
