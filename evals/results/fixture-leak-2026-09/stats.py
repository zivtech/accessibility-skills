#!/usr/bin/env python3
"""Significance and power for the two issue-#51 leak lanes.

The scorers report rates. This reports whether the rates differ, and what
size of difference the design could have caught. Run from the repo root:

    python3 evals/results/fixture-leak-2026-09/stats.py
"""
import collections
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
Z = 1.96


def fisher_two_sided(a, b, c, d):
    """Exact p for the 2x2 [[a, b], [c, d]]."""
    n, r1, c1 = a + b + c + d, a + b, a + c
    def p(x):
        return (math.comb(r1, x) * math.comb(n - r1, c1 - x)) / math.comb(n, c1)
    p0 = p(a)
    lo, hi = max(0, c1 - (n - r1)), min(r1, c1)
    return sum(p(x) for x in range(lo, hi + 1) if p(x) <= p0 + 1e-12)


def wilson(k, n):
    if n == 0:
        return 0.0, 0.0
    p, d = k / n, 1 + Z * Z / n
    centre = (p + Z * Z / (2 * n)) / d
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return max(0.0, centre - half), min(1.0, centre + half)


def power(p1, p2, n):
    """Two-proportion power, alpha .05 two-sided."""
    pbar = (p1 + p2) / 2
    se0 = math.sqrt(2 * pbar * (1 - pbar) / n)
    se1 = math.sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / n) or 1e-12
    return 1 - 0.5 * (1 + math.erf((Z * se0 - abs(p1 - p2)) / (se1 * math.sqrt(2))))


def mde(p1, n, target=0.80):
    """Smallest p2 > p1 this arm size could catch at `target` power."""
    p2 = p1
    while p2 < 0.995 and power(p1, p2, n) < target:
        p2 += 0.005
    return p2


def contrast(label, a, n1, c, n2):
    b, d = n1 - a, n2 - c
    p = fisher_two_sided(a, b, c, d)
    lo1, hi1 = wilson(a, n1)
    lo2, hi2 = wilson(c, n2)
    print(f"  {label}")
    print(f"    arm A {a:3d}/{n1:<3d} = {a/n1:6.1%}  95% CI [{lo1:.1%}, {hi1:.1%}]")
    print(f"    arm B {c:3d}/{n2:<3d} = {c/n2:6.1%}  95% CI [{lo2:.1%}, {hi2:.1%}]")
    print(f"    two-sided Fisher p = {p:.4f}   observed power = {power(a/n1, c/n2, n1):.0%}")
    return p


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def featurehint():
    rows = load("score-featurehint.json")["rows"]
    print("=== features-section lane (withfeatures = arm A, nofeatures = arm B)")
    band = {"ACCEPT", "ACCEPT-WITH-RESERVATIONS"}
    for tier in ("CLEAN", "HAS-BUGS"):
        tier_rows = [r for r in rows if r["tier"] == tier]
        arms = {c: [r for r in tier_rows if r["condition"] == c]
                for c in ("withfeatures", "nofeatures")}
        n1, n2 = len(arms["withfeatures"]), len(arms["nofeatures"])
        print(f"\n{tier}  (n = {n1} / {n2})")
        for cond in ("withfeatures", "nofeatures"):
            counts = collections.Counter(r["verdict"] for r in arms[cond])
            print(f"    {cond:14s} " + "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        if tier == "CLEAN":
            for label, pred in (
                ("strict ACCEPT", lambda r: r["verdict"] == "ACCEPT"),
                ("ACCEPT + reservations", lambda r: r["verdict"] in band),
                ("raised >=1 structured finding", lambda r: r["structured_findings"] > 0),
            ):
                contrast(label,
                         sum(1 for r in arms["withfeatures"] if pred(r)), n1,
                         sum(1 for r in arms["nofeatures"] if pred(r)), n2)
            base = sum(1 for r in arms["withfeatures"] if r["verdict"] == "ACCEPT") / n1
            print(f"\n    MDE at n={n1}/arm from a {base:.1%} base: only a rise to "
                  f"~{mde(base, n1):.0%} was catchable at 80% power "
                  f"(~{mde(base, n1)/base:.1f}x).")
        else:
            for cond in ("withfeatures", "nofeatures"):
                f = sum(r["must_found"] for r in arms[cond])
                t = sum(r["must_total"] for r in arms[cond])
                print(f"    must-find {cond:14s} {f}/{t} = {f/t:.1%}")
            contrast("REJECT (severity, not detection)",
                     sum(1 for r in arms["withfeatures"] if r["verdict"] == "REJECT"), n1,
                     sum(1 for r in arms["nofeatures"] if r["verdict"] == "REJECT"), n2)


def titlehint():
    d = load("score-titlehint.json")
    rows = d["rows"] if "rows" in d else []
    print("\n\n=== H1-title lane (titled = arm A, neutral = arm B)")
    for cond in ("titled", "neutral"):
        arm = [r for r in rows if r["condition"] == cond]
        f = sum(r["found"] for r in arm)
        t = sum(r["total"] for r in arm)
        echo = sum(1 for r in arm if r["echoes_title"])
        trunc = sum(1 for r in arm if r["truncated"])
        print(f"  must-find {cond:8s} {f}/{t} = {f/t:.1%}  (n={len(arm)} draws, "
              f"title echoed in {echo}, truncated {trunc})")
    print("  Both arms sit on the ceiling. A ceiling cannot move up, so this lane")
    print("  bounds the title effect from below only: no detectable effect, on")
    print("  fixtures already found 100% of the time without the title.")


if __name__ == "__main__":
    featurehint()
    titlehint()
