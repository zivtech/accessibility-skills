#!/usr/bin/env python3
"""Compare our baseline axe-core scanner against Lighthouse's accessibility category."""
import json
import glob
import os

WORKDIR = os.path.dirname(os.path.abspath(__file__))

URLS = [
    ("product-b-home", "https://product-b.epa.gov/dashboard/"),
    ("product-b-search", "https://product-b.epa.gov/dashboard/search-results?input_type=synonym_substring&inputs=caffeine"),
    ("fire-map", "https://fire.product-a.gov/"),
    ("gispub-map", "https://gispub.epa.gov/product-a/?monitors=ozonepm"),
    ("product-a-about", "https://www.product-a.gov/about-product-a/"),
]

def load_ours():
    """Return {url: {rule_id: {viewports:set, impact, nodes}}} union across viewports."""
    ours = {}
    for f in sorted(glob.glob(os.path.join(WORKDIR, "ours", "0*.json"))):
        d = json.load(open(f))
        url = d["url"]
        rules = {}
        for vpkey, vp in d["viewports"].items():
            for v in vp.get("violations", []):
                entry = rules.setdefault(v["id"], {"viewports": set(), "impact": v["impact"], "nodes": 0, "tags": v.get("tags", [])})
                entry["viewports"].add(vpkey)
                entry["nodes"] += v["node_count"]
        ours[url] = rules
    return ours

def load_lighthouse_lhr(name, mode):
    path = os.path.join(WORKDIR, "lighthouse", f"{name}-{mode}.json")
    if not os.path.exists(path):
        return None
    return json.load(open(path))

def classify_lhr(lhr):
    """Return (failing_rule_ids:set, manual_rule_ids:set, all_audit_count:int, version:str, formfactor:str)."""
    cat = lhr["categories"]["accessibility"]
    failing = set()
    manual = set()
    for ref in cat["auditRefs"]:
        aid = ref["id"]
        audit = lhr["audits"].get(aid, {})
        mode_ = audit.get("scoreDisplayMode")
        score = audit.get("score")
        if mode_ == "manual":
            manual.add(aid)
            continue
        if mode_ == "binary" and score is not None and score < 1:
            failing.add(aid)
    return failing, manual, len(cat["auditRefs"]), lhr.get("lighthouseVersion"), lhr.get("configSettings", {}).get("formFactor")

def main():
    ours = load_ours()
    report = {"urls": {}}
    lh_version = None
    for name, url in URLS:
        entry = {"url": url, "name": name}
        mobile = load_lighthouse_lhr(name, "mobile")
        desktop = load_lighthouse_lhr(name, "desktop")
        entry["load_status"] = {
            "ours": "measured" if url in ours else "MISSING",
            "lighthouse_mobile": "measured" if mobile else "MISSING",
            "lighthouse_desktop": "measured" if desktop else "MISSING",
        }

        our_rules = ours.get(url, {})
        our_rule_ids = set(our_rules.keys())

        lh_failing_mobile, lh_manual_mobile, n_audits_m, ver_m, ff_m = (set(), set(), 0, None, None)
        lh_failing_desktop, lh_manual_desktop, n_audits_d, ver_d, ff_d = (set(), set(), 0, None, None)
        if mobile:
            lh_failing_mobile, lh_manual_mobile, n_audits_m, ver_m, ff_m = classify_lhr(mobile)
            lh_version = lh_version or ver_m
        if desktop:
            lh_failing_desktop, lh_manual_desktop, n_audits_d, ver_d, ff_d = classify_lhr(desktop)
            lh_version = lh_version or ver_d

        lh_failing_union = lh_failing_mobile | lh_failing_desktop
        manual_count = len(lh_manual_mobile or lh_manual_desktop)

        both_fire = sorted(our_rule_ids & lh_failing_union)
        ours_only = sorted(our_rule_ids - lh_failing_union)
        lighthouse_only = sorted(lh_failing_union - our_rule_ids)

        entry["our_rule_ids"] = sorted(our_rule_ids)
        entry["lighthouse_failing_mobile"] = sorted(lh_failing_mobile)
        entry["lighthouse_failing_desktop"] = sorted(lh_failing_desktop)
        entry["lighthouse_failing_union"] = sorted(lh_failing_union)
        entry["lighthouse_manual_audit_count"] = manual_count
        entry["both_fire"] = both_fire
        entry["ours_only"] = ours_only
        entry["lighthouse_only"] = lighthouse_only
        entry["lighthouse_formfactor"] = {"mobile": ff_m, "desktop": ff_d}

        report["urls"][name] = entry

        print(f"=== {name} :: {url} ===")
        print(f"  ours (union both viewports):        {sorted(our_rule_ids)}")
        print(f"  lighthouse mobile failing:           {sorted(lh_failing_mobile)}")
        print(f"  lighthouse desktop failing:          {sorted(lh_failing_desktop)}")
        print(f"  lighthouse union failing:            {sorted(lh_failing_union)}")
        print(f"  BOTH FIRE:                           {both_fire}")
        print(f"  OURS ONLY:                           {ours_only}")
        print(f"  LIGHTHOUSE ONLY:                     {lighthouse_only}")
        print(f"  lighthouse manual-audit count:       {manual_count}")
        print()

    report["lighthouse_version"] = lh_version
    with open(os.path.join(WORKDIR, "lighthouse-compare-summary.json"), "w") as f:
        json.dump(report, f, indent=2, default=list)
    print("Wrote lighthouse-compare-summary.json")

if __name__ == "__main__":
    main()
