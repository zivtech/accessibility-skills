#!/usr/bin/env python3
"""Synthetic calibration for the a11y-content-judgment lane — run BEFORE any
model row (the acr-reporting-phase2 / ict-baseline-phase3 house pattern).

Per fixture, builds responses in memory from the frozen metadata — so
metadata self-consistency is itself under test — and scores each with the
real ollama/score_content_judgment.py:

  honest        every must row at its expected value, calibration rows at
                theirs, invalid rows answered (they must be ignored), a
                rationale that carries a `loses` phrase  -> PASS
  hedger        every must-yes row `unsure`                -> WARN (over-hedge)
  flagger       every must-yes row `no`                    -> FAIL (false alarms)
  blind         every must-no row `yes`                    -> FAIL (R1)
  silent        the last input row omitted                 -> FAIL (C1)
  inventor      one rationale quoting a 4-word span absent from the row
                                                           -> WARN (R5, should-tier)
  regression    every must-no rationale stripped of its `loses` phrase
                                                           -> WARN (R6)
  split-group   one row of the largest pattern_group dissenting
                                                           -> R7 fires (WARN; FAIL when the
                                                              group is must-no, since the
                                                              dissent is also an R1 miss)

What CLEAN certifies: C1/C2/R1/R2/R5/R6/R7 wiring and metadata
self-consistency. It does NOT exercise R4 (every fixture's
`fabricated_tokens` is empty — R4 is covered by the smoke case only) or the
C3 word cap (honest rationales are truncated to 25 words by construction).

Exit 0 = CLEAN; `--dump` writes score-cal-<fixture>-<case>.txt beside this
file.

    python3 evals/results/content-judgment-2026-09/calibrate.py [--dump]
"""
import json
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FIXTURES = os.path.join(REPO, "evals", "suites", "a11y-content-judgment", "fixtures")
SCORER = os.path.join(REPO, "ollama", "score_content_judgment.py")
IDS = ["page-titles-shared", "link-purpose-cards", "images-role-routing",
       "headings-fields-labels", "identification-across-views", "clean-control"]


def line(rid, j, rationale, fix=""):
    return json.dumps({"id": rid, "judgment": j, "confidence": "high" if j != "unsure" else "low",
                       "rationale": rationale, "fix": fix, "needs_human": j == "unsure",
                       "drafted_by": "calibration-synthetic"})


def honest_lines(meta):
    out = []
    for rid, m in meta["rows"].items():
        j = m["expected"]
        loses = (m.get("loses") or ["fails the person"])[0]
        rationale = (f"The person {loses}; the text does not do its job." if j == "no"
                     else "The text tells the person what they need in this context.")
        rationale = " ".join(rationale.split()[:25])   # blind-authored loses phrases can be long clauses
        out.append(line(rid, j, rationale, "Replace with specific text" if j == "no" else ""))
    return out


def mutate(meta, lines, case):
    rows = meta["rows"]
    out = []
    for ln in lines:
        o = json.loads(ln)
        m = rows[o["id"]]
        must = m["tier"] != "calibration" and not m.get("invalid")
        if case == "hedger" and must and m["expected"] == "yes":
            o.update(judgment="unsure", confidence="low", needs_human=True)
        elif case == "flagger" and must and m["expected"] == "yes":
            o.update(judgment="no", rationale="Not descriptive enough for the person.", fix="Rewrite it")
        elif case == "blind" and must and m["expected"] == "no":
            o.update(judgment="yes", rationale="Reads fine as written.", fix="")
        out.append(json.dumps(o))
    if case == "silent":
        out = out[:-1]
    if case == "regression":
        for i, ln in enumerate(out):
            o = json.loads(ln)
            if o["judgment"] == "no":
                o["rationale"] = "Not descriptive enough as written."
                out[i] = json.dumps(o)
    if case == "split-group":
        groups = {}
        for rid, m in rows.items():
            if m.get("pattern_group") and not m.get("invalid"):
                groups.setdefault(m["pattern_group"], []).append(rid)
        if groups:
            g = max(groups.values(), key=len)
            # dissent on one row: the R7 line must fire; when the group is
            # must-no the dissent is also an R1 miss (FAIL), else WARN
            for i, ln in enumerate(out):
                o = json.loads(ln)
                if o["id"] == g[0]:
                    o["judgment"] = "unsure" if o["judgment"] != "unsure" else "yes"
                    o["needs_human"] = o["judgment"] == "unsure"
                    out[i] = json.dumps(o)
    if case == "inventor":
        o = json.loads(out[0])
        o["rationale"] = 'The page says "quarterly membership renewal portal" but the text hides it.'
        out[0] = json.dumps(o)
    return out


EXPECT = {
    "honest": ("PASS", ["false alarms: 0"]),
    "hedger": ("WARN", ["R2 over-hedge"]),
    "flagger": ("FAIL", ["R2 false alarm"]),
    "blind": ("FAIL", ["R1 expected-no row"]),
    "silent": ("FAIL", ["C1 missing output for 1 id"]),
    "inventor": ("WARN", ["R5 quoted span(s) absent from the row (1)"]),
    "regression": ("WARN", ["R6 no-rationale names none of the row's loses phrases"]),
    "split-group": ("WARN|FAIL", ["R7 pattern_group"]),
}


def _groups(meta):
    g = {}
    for rid, m in meta["rows"].items():
        if m.get("pattern_group") and not m.get("invalid"):
            g.setdefault(m["pattern_group"], []).append(rid)
    return g


def score(lines, meta_path):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"response": "```jsonl\n" + "\n".join(lines) + "\n```", "done_reason": "stop"}, f)
        path = f.name
    try:
        return subprocess.run([sys.executable, SCORER, path, meta_path], capture_output=True, text=True).stdout
    finally:
        os.unlink(path)


def main():
    dump = "--dump" in sys.argv
    bad = 0
    for fid in IDS:
        meta_path = os.path.join(FIXTURES, f"{fid}.metadata.yaml")
        with open(meta_path) as f:
            meta = yaml.safe_load(f)
        base = honest_lines(meta)
        for case, (status, needles) in EXPECT.items():
            musts = [m for m in meta["rows"].values() if m["tier"] != "calibration" and not m.get("invalid")]
            if case == "hedger" and not any(m["expected"] == "yes" for m in musts):
                continue
            if case in ("flagger",) and not any(m["expected"] == "yes" for m in musts):
                continue
            if case in ("blind", "regression") and not any(m["expected"] == "no" for m in musts):
                continue   # vacuous on the clean control
            if case == "split-group" and not any(len(v) > 1 for v in _groups(meta).values()):
                continue   # no multi-row pattern group in this fixture
            out = score(base if case == "honest" else mutate(meta, base, case), meta_path)
            ok = any(f"Status: {st}" in out for st in status.split("|")) and all(n in out for n in needles)
            print(f"{'CLEAN' if ok else 'MISS '} {fid:30} {case:9} expected {status}")
            if not ok:
                bad += 1
                print(out)
            if dump:
                with open(os.path.join(HERE, f"score-cal-{fid}-{case}.txt"), "w") as f:
                    f.write(out)
    print("\nCALIBRATION CLEAN" if not bad else f"\nCALIBRATION: {bad} miss(es)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
