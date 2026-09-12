#!/usr/bin/env python3
"""Score all Gemini 3.8 Flash critic responses for one effort level against the
fixture rubrics (via score_output.py) and print a tally comparable to the
committed Gemini 2.5 Flash baseline (31/33).

Usage: python3 ollama/tally_gemini_38.py <low|medium|high>
"""
import sys, os, re, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
FIX = os.path.join(REPO, "evals/suites/a11y-critic/fixtures")
OUT = os.path.join(REPO, "evals/results/gemini-3.8")
sys.path.insert(0, BASE)
from run_gemini_agy_critic import BASELINE_33  # noqa: E402


def score_one(fixture, effort):
    resp = os.path.join(OUT, f"gemini-bench-{fixture}-flash-{effort}-response.json")
    meta = os.path.join(FIX, f"{fixture}.metadata.yaml")
    if not os.path.exists(resp):
        return {"fixture": fixture, "status": "NO_RESPONSE"}
    r = subprocess.run(["python3", os.path.join(BASE, "score_output.py"), resp, meta],
                       capture_output=True, text=True)
    out = r.stdout
    status = (re.search(r"Status:\s*(\w+)", out) or [None, "?"])[1]
    verdict = (re.search(r"Verdict:\s*(\w+)\s*\(expected:\s*(\w+)\)", out))
    rate = (re.search(r"Must-find detection rate:\s*(\d+)%", out) or [None, "-"])[1]
    fp = (re.search(r"False positives?:\s*(\d+)", out) or re.search(r"(\d+) false positive", out))
    diff = (re.search(r"difficulty[\"']?\s*[:=]\s*[\"']?(\w+)", out, re.I))
    return {
        "fixture": fixture, "status": status,
        "verdict": verdict.group(1) if verdict else "?",
        "expected": verdict.group(2) if verdict else "?",
        "rate": rate,
        "fp": fp.group(1) if fp else "",
    }


def main():
    effort = sys.argv[1] if len(sys.argv) > 1 else "medium"
    rows = [score_one(f, effort) for f in BASELINE_33]
    npass = sum(1 for r in rows if r["status"] == "PASS")
    nfail = sum(1 for r in rows if r["status"] == "FAIL")
    nmiss = sum(1 for r in rows if r["status"] == "NO_RESPONSE")
    print(f"\nGemini 3.8 Flash ({effort}) — {npass} PASS / {nfail} FAIL / {nmiss} missing  of {len(rows)}")
    print("(Gemini 2.5 Flash baseline: 31/33 PASS)\n")
    print(f"{'fixture':44} {'status':6} {'verdict/exp':16} {'must%':6} {'fp'}")
    for r in rows:
        ve = f"{r.get('verdict','?')}/{r.get('expected','?')}"
        print(f"{r['fixture']:44} {r['status']:6} {ve:16} {r.get('rate','-'):>5} {r.get('fp','')}")
    fails = [r["fixture"] for r in rows if r["status"] in ("FAIL", "NO_RESPONSE")]
    if fails:
        print("\nNon-PASS:", ", ".join(fails))


if __name__ == "__main__":
    main()
