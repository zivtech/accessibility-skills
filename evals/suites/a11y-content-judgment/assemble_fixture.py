#!/usr/bin/env python3
"""Assemble fixtures/<id>.md from sources/<id>/ (scenario.md + build/rows.jsonl)
and check the metadata `deterministic:` block against what the pipeline
emitted. Called by build-fixtures.sh; usable alone once build/ exists.

The task instruction below is the whole of what the fixture tells the model
about HOW to answer: the output contract (keys, one line per row, the
fence) so a no-rubric baseline is scorable at all. Every judgment rule the
lane grades lives in the rubric (the system prompt), never here.
"""
import csv
import json
import os
import sys

import yaml

SUITE = os.path.dirname(os.path.abspath(__file__))

TASK = """Draft one accessibility judgment per row below for a named human ratifier.
Each row is one element captured from a live page of the product described
above: `type` (title | heading | link | image | field | ident), `sc` (the WCAG
success criterion the row belongs to), `name` (the text or accessible name the
user receives), `detail`, `href`, `context` (the surrounding text block),
`landmark`, `visible`, `views` (how many captured pages carry this unit), and
`flags` (heuristic labels attached by the inventory tool).

Return exactly one JSON line per input row, in input order, inside a single
```jsonl fence, with these keys and nothing else:

{"id","judgment":"yes|no|unsure","confidence":"high|medium|low","rationale":"one sentence, at most 25 words","fix":"at most 20 words; empty when yes","needs_human":true|false,"drafted_by":"<your model id>"}
"""


def load_rows(src):
    with open(os.path.join(src, "build", "rows.jsonl")) as f:
        rows = [json.loads(line) for line in f if line.strip()]
    order = {"title": 0, "heading": 1, "field": 2, "link": 3, "image": 4, "ident": 5}
    return sorted(rows, key=lambda r: (order.get(r["type"], 9), r["id"]))


def check_deterministic(fid, src, rows, det, meta_rows=None):
    """Compare the emitted rows / nav csv with the metadata block. Returns problems."""
    problems = []
    counts = {}
    for r in rows:
        counts[r["type"]] = counts.get(r["type"], 0) + 1
    for t, n in (det.get("row_counts") or {}).items():
        if counts.get(t, 0) != n:
            problems.append(f"{fid}: row_counts[{t}] expected {n}, pipeline emitted {counts.get(t, 0)}")
    for t in counts:
        if t not in (det.get("row_counts") or {}):
            problems.append(f"{fid}: pipeline emitted {counts[t]} {t} rows not declared in row_counts")
    for frag in det.get("absent_ident_hrefs") or []:
        hits = [r["id"] for r in rows if r["type"] == "ident" and frag in (r.get("href") or "")]
        if hits:
            problems.append(f"{fid}: ident rows must not exist for href containing {frag!r}: {hits}")
    for frag in det.get("absent_link_hrefs") or []:
        hits = [r["id"] for r in rows if r["type"] == "link" and frag in (r.get("href") or "")]
        if hits:
            problems.append(f"{fid}: link rows must not exist for href containing {frag!r}: {hits}")
    nav_path = os.path.join(src, "build", "nav-consistency.csv")
    # M4: each expectation row must carry, in the emitted row's own fields, the
    # evidence its verdict needs (blind-authored evidence_contains/evidence_absent)
    by_id = {r["id"]: r for r in rows}
    for rid, m in (meta_rows or {}).items():
        r = by_id.get(rid)
        if r is None or m.get("invalid"):
            continue
        hay = " ".join(str(r.get(k) or "") for k in ("name", "detail", "context", "href")).lower()
        text_only = " ".join(str(r.get(k) or "") for k in ("name", "context")).lower()
        for phrase in m.get("evidence_contains") or []:
            if str(phrase).lower() not in hay:
                problems.append(f"{fid}: row {rid} lacks evidence phrase {phrase!r} in name/detail/context/href — row cannot be decided as expected")
        for phrase in m.get("evidence_absent") or []:
            if str(phrase).lower() in text_only:
                problems.append(f"{fid}: row {rid} carries forbidden phrase {phrase!r} — the planted defect is not reproduced")
    nav = {}
    if os.path.exists(nav_path):
        with open(nav_path) as f:
            for row in csv.DictReader(f):
                nav[row["view_id"]] = row
    for view, exp in (det.get("nav_consistency") or {}).items():
        row = nav.get(view)
        if row is None:
            problems.append(f"{fid}: nav_consistency has no row for view {view!r}")
            continue
        if "order_consistent" in exp and row["order_consistent"] != str(exp["order_consistent"]).lower():
            problems.append(f"{fid}: nav {view}: order_consistent={row['order_consistent']} expected {exp['order_consistent']}")
        if "note_contains" in exp and exp["note_contains"].lower() not in row["note"].lower():
            problems.append(f"{fid}: nav {view}: note {row['note']!r} lacks {exp['note_contains']!r}")
    return problems


def main():
    fid = sys.argv[1]
    src = os.path.join(SUITE, "sources", fid)
    rows = load_rows(src)
    with open(os.path.join(src, "scenario.md")) as f:
        scenario = f.read().strip()
    lines = [f"# Input: content-judgment batch — {fid}", "", scenario, "", TASK.strip(), "", "```jsonl"]
    lines += [json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in rows]
    lines += ["```", ""]
    out = os.path.join(SUITE, "fixtures", f"{fid}.md")
    with open(out, "w") as f:
        f.write("\n".join(lines))
    meta_path = os.path.join(SUITE, "fixtures", f"{fid}.metadata.yaml")
    problems = []
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            meta = yaml.safe_load(f) or {}
        problems = check_deterministic(fid, src, rows, meta.get("deterministic") or {}, meta.get("rows") or {})
        expected = set((meta.get("rows") or {}).keys())
        emitted = {r["id"] for r in rows}
        for i in sorted(expected - emitted):
            problems.append(f"{fid}: metadata row {i} not emitted by the pipeline")
        for i in sorted(emitted - expected):
            problems.append(f"{fid}: emitted row {i} has no metadata expectation")
    tally = {}
    for r in rows:
        tally[r["type"]] = tally.get(r["type"], 0) + 1
    print(f"{fid}: {len(rows)} rows {tally} -> {os.path.relpath(out, SUITE)}" + ("" if not problems else "  DETERMINISTIC MISMATCH"))
    for p in problems:
        print("  " + p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
