#!/usr/bin/env python3
"""EM-depth markers: methodology content the PROTOCOL teaches but the fixture never names.
The fixture cues 'WCAG-EM' by name, so bare mentions don't discriminate; these do."""
import json, re, sys, os

MARKERS = {
    "random sample":            r"random(ly)?[- ]selected sample|random sample",
    "10% sizing rule":          r"10\s?%",
    "representativeness check": r"representativen|structured (sample )?(set )?(vs\.?|versus|and|against).{0,30}random|random.{0,30}(vs\.?|versus|against).{0,30}structured|compare.{0,40}(structured|random)",
    "a11y support baseline":    r"accessibility[- ]support baseline",
    "sample set (EM term)":     r"sample set",
    "complete process (EM term)": r"complete process",
    "WCAG-EM 2.0 identity":     r"WCAG-EM 2|wcag-em-2|WCAG Evaluation Methodology",
    "product enclosure":        r"product enclosure|full product|entire product",
    "per-SC outcome vocab":     r"cantTell|inapplicable|untested",
    "evaluation report contract": r"evaluation[- ]report contract|a11y-evaluation-report-contract",
    "default/branch sequence":  r"default sequence|branch sequence",
    "evaluation commissioner":  r"commissioner",
}

def text_of(path):
    if path.endswith(".json"):
        return json.load(open(path))["response"]
    return open(path).read()

files = sys.argv[1:]
names = [os.path.basename(f).replace("-response.json","").replace(".json","").replace(".md","").replace("plan-","") for f in files]
texts = {n: text_of(f) for n, f in zip(names, files)}
w = max(len(m) for m in MARKERS) + 2
print(f"{'marker':<{w}}" + "".join(f"{n:>12}" for n in names))
for label, pat in MARKERS.items():
    row = f"{label:<{w}}"
    for n in names:
        hits = len(re.findall(pat, texts[n], re.IGNORECASE))
        row += f"{hits:>12}"
    print(row)
print(f"{'TOTAL markers present':<{w}}" + "".join(f"{sum(1 for p in MARKERS.values() if re.search(p, texts[n], re.IGNORECASE)):>12}" for n in names))
