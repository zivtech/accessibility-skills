#!/usr/bin/env python3
"""Score keyboard-a11y-tester deterministic findings against a11y-critic eval ground truth.

Each must_find item is pre-classified by reachability for KAT's instrument set:
  DET:<check>  — one of KAT's 13 deterministic checks should catch it (blind crawl)
  AI           — reachable only by KAT's AI-judgment layer (trace/census/driven session)
  OOS          — outside KAT's design scope (media, table header semantics, hover-only)
Classification is ours (2026-07-10), applied before seeing batch output; disagreements
between prediction and observation are reported, not hidden.
"""
import json
import glob
import os
import yaml

FIXTURES = "/Users/AlexUA_1/claude/a11y-meta-skills/evals/suites/a11y-critic/fixtures"
RESULTS = "/private/tmp/claude-501/-Users-AlexUA-1-claude-a11y-meta-skills/083549b3-a213-4de3-865a-02c09d7d8a7a/scratchpad/kat-eval/results"

# Per-fixture labels, parallel to must_find item order in metadata.
CLASSIFICATION = {
    "accordion-no-region-role": ["AI", "AI"],
    "app-focus-order-illogical": ["AI"],
    "async-form-vague-success": ["AI"],
    "breadcrumb-navigation-no-nav-landmark": ["AI", "AI"],
    "checkbox-group-no-fieldset": ["AI", "AI"],
    "combobox-autocomplete-no-listbox-role": ["AI", "AI", "AI", "AI"],
    "dashboard-heading-inconsistency": ["DET:1.3.1-heading"],
    "data-table-missing-scope": ["OOS", "OOS"],
    "expandable-section-no-button": ["AI", "AI", "AI", "AI"],
    "file-input-no-labels": ["DET:4.1.2-name", "AI", "AI", "AI"],
    "form-validation-missing-aria-describedby": ["AI", "AI"],
    "heading-hierarchy-skipped": ["DET:1.3.1-heading", "AI"],
    "image-carousel-no-region": ["AI", "AI", "AI", "AI"],
    "infinite-scroll-no-announcement": ["AI", "AI", "AI", "AI"],
    "interactive-dropdown-focus-bug": ["AI", "AI"],
    "loading-state-missing-aria-busy": ["AI", "AI"],
    "megamenu-no-structure": ["AI", "AI", "AI", "AI", "AI", "AI"],
    "multistep-form-error-clearing": ["AI"],
    "pagination-no-nav-landmark": ["AI", "AI", "AI"],
    "popover-no-focus-management": ["AI", "AI", "AI", "AI", "AI"],
    "radio-button-group-no-grouping": ["AI", "AI"],
    "tabs-incomplete-aria-selected": ["AI"],
    "tabs-missing-arrow-nav": ["AI"],
    "toast-notification-no-role": ["AI", "AI", "AI", "AI"],
    "tooltip-no-role-no-association": ["AI", "AI", "AI"],
    "video-player-missing-captions": ["OOS", "OOS", "OOS"],
}

# Map a DET label to a matcher over KAT findings.
def det_matches(label, findings):
    kind = label.split(":", 1)[1]
    for f in findings:
        w = f.get("wcag", "")
        s = (f.get("summary", "") or "").lower()
        if kind == "1.3.1-heading" and w == "1.3.1" and "heading" in s:
            return f
        if kind == "4.1.2-name" and w == "4.1.2" and ("accessible name" in s or "no accessible name" in s):
            return f
        if kind == "4.1.3-live" and w == "4.1.3":
            return f
        if kind == "2.1.2-trap" and w == "2.1.2":
            return f
    return None


def load_findings(fid):
    p = os.path.join(RESULTS, fid, "127-0-0-1", "desktop", "deterministic-findings.json")
    if not os.path.exists(p):
        return None
    data = json.load(open(p))
    return data["findings"] if isinstance(data, dict) else data


def main():
    det_caught, det_missed, ai_n, oos_n = [], [], 0, 0
    fp_rows = []       # AA findings on CLEAN/ADVERSARIAL fixtures
    extra_rows = []    # AA findings on buggy fixtures not tied to a must-find (surprises)
    missing_results = []

    for meta_path in sorted(glob.glob(os.path.join(FIXTURES, "*.metadata.yaml"))):
        m = yaml.safe_load(open(meta_path))
        fid = m["fixture_id"]
        diff = m["difficulty"]
        items = next((e for e in m.get("expected_findings", []) if e.get("category") == "must_find"), {}).get("items") or []
        findings = load_findings(fid)
        if findings is None:
            missing_results.append(fid)
            continue
        aa = [f for f in findings if f.get("conformance_level") == "AA"]
        labels = CLASSIFICATION.get(fid, [])
        assert len(labels) == len(items), f"{fid}: {len(labels)} labels vs {len(items)} items"

        matched_ids = set()
        for label, item in zip(labels, items):
            desc = item.get("description", "")[:70]
            if label.startswith("DET"):
                hit = det_matches(label, aa + findings)
                if hit:
                    det_caught.append((fid, desc, hit.get("wcag"), hit.get("id")))
                    matched_ids.add(hit.get("id"))
                else:
                    det_missed.append((fid, desc, label))
            elif label == "AI":
                ai_n += 1
            else:
                oos_n += 1

        if diff in ("CLEAN", "ADVERSARIAL"):
            for f in aa:
                fp_rows.append((fid, diff, f.get("wcag"), f.get("persona"), (f.get("summary", "") or "")[:100]))
        else:
            for f in aa:
                if f.get("id") in matched_ids:
                    continue
                extra_rows.append((fid, f.get("wcag"), f.get("persona"), (f.get("summary", "") or "")[:100]))

    total = len(det_caught) + len(det_missed) + ai_n + oos_n
    print(f"TOTAL must-finds: {total}")
    print(f"  deterministic-scope: {len(det_caught) + len(det_missed)}  (caught {len(det_caught)}, missed {len(det_missed)})")
    print(f"  AI-judgment-layer-scope: {ai_n}")
    print(f"  out-of-scope by design: {oos_n}")
    print()
    print("== DET caught ==")
    for r in det_caught:
        print("  ", r)
    print("== DET missed ==")
    for r in det_missed:
        print("  ", r)
    print()
    print("== AA findings on CLEAN/ADVERSARIAL fixtures (candidate false positives) ==")
    for r in fp_rows:
        print("  ", r)
    print()
    print("== AA findings on buggy fixtures beyond matched must-finds (extras/surprises) ==")
    for r in extra_rows:
        print("  ", r)
    if missing_results:
        print()
        print("MISSING RESULTS:", missing_results)


if __name__ == "__main__":
    main()
