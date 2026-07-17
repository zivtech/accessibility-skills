#!/usr/bin/env python3
"""Rule-based scorer for the bug-reporting eval lane.

Scores a model-produced accessibility bug report against a fixture's
metadata expectations (evals/suites/bug-reporting/fixtures/*.metadata.yaml):

1. Report count — dedup/split behavior (expected_report_count)
2. Required-field labels present per report (URL, XPath, Full DOM path,
   WCAG SC, Rule, Severity, Frequency) plus an HTML snippet
3. Key values present (must_contain: list of any-of alternation lists)
4. Stable IDs — recomputes sha256(inputs)[:8] per the skill's algorithm and
   looks for the hex token (should-tier)
5. Honest N/A — na_fields rows must not carry invented values (hard trap)
6. Title pattern `(WCAG d.d.d)` (nice-tier)

Status: PASS (all musts, no fabrication), WARN (musts pass, should/nice
missed), FAIL (must missed or fabrication detected).

Usage:
    python3 ollama/score_bugreport.py <response.json> <metadata.yaml>
"""

import hashlib
import json
import re
import sys

import yaml

REQUIRED_LABELS = (
    "URL",
    "XPath",
    "Full DOM path",
    "WCAG SC",
    "Rule",
    "Severity",
    "Frequency",
)

# Honest-absence vocabulary. Live-validated 2026-07-17: models phrase absence
# many ways ("Not reported in scan output", "version not specified",
# "Not generated") — the check is for a negation-of-availability, not the
# literal string N/A.
NA_TOKENS = re.compile(
    r"(?i)\bn/?a\b|not (?:recorded|available|provided|captured|known|"
    r"applicable|used|run|present|emitted|reported|specified|generated|"
    r"included|determined|supplied)|unknown|\bnone\b|cannot be"
)

THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)
TITLE_RE = re.compile(r"(?im)^#{1,3} .*accessibility issue", re.IGNORECASE)
# No closing paren: titles legitimately cite multiple SCs, e.g. "(WCAG 4.1.2, 2.4.4)"
WCAG_TITLE_RE = re.compile(r"\(WCAG \d\.\d+\.\d+")


def label_line_re(label):
    """Match a table row or bold-label line for `label`, capture the value."""
    esc = re.escape(label)
    return re.compile(
        r"(?im)^[\s|>]*\*{0,2}" + esc + r"\*{0,2}\s*[:|]\s*(.*)$"
    )


def load_response(path):
    with open(path) as f:
        data = json.load(f)
    text = data["response"] if isinstance(data, dict) else str(data)
    return THINK_RE.sub("", text)


def split_reports(text):
    """Split response into report blocks by title headings; whole text if none."""
    starts = [m.start() for m in TITLE_RE.finditer(text)]
    if not starts:
        return [text]
    starts.append(len(text))
    return [text[starts[i]:starts[i + 1]] for i in range(len(starts) - 1)]


def count_reports(text):
    n = len(TITLE_RE.findall(text))
    if n:
        return n
    # fallback: count URL label rows
    return max(1, len(label_line_re("URL").findall(text))) if text.strip() else 0


def expected_id_hexes(spec):
    """Return list of (kind, selector, hex8) for a stable_ids metadata spec."""
    out = []
    for inst in spec["instances"]:
        sel = inst["selector"]
        inst_input = f"{spec['page_path']}|{sel}|{spec['rule_id']}|{spec['screen_type']}"
        pat_input = f"{sel}|{spec['rule_id']}|{spec['screen_type']}"
        out.append(("instance", sel, hashlib.sha256(inst_input.encode()).hexdigest()[:8]))
        out.append(("pattern", sel, hashlib.sha256(pat_input.encode()).hexdigest()[:8]))
    return out


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: ollama/score_bugreport.py <response.json> <metadata.yaml>")

    text = load_response(sys.argv[1])
    with open(sys.argv[2]) as f:
        meta = yaml.safe_load(f)

    must_miss = []
    should_miss = []
    nice_miss = []
    fabrications = []

    print(f"Fixture: {meta['fixture_id']}")

    # 1. report count
    expected_n = meta["expected_report_count"]
    got_n = count_reports(text)
    print(f"Reports: {got_n} (expected {expected_n})")
    if got_n != expected_n:
        must_miss.append(f"report count {got_n} != {expected_n}")

    # 2. required labels + snippet, per report block
    blocks = split_reports(text)
    for i, block in enumerate(blocks, 1):
        missing = [
            lab for lab in REQUIRED_LABELS if not label_line_re(lab).search(block)
        ]
        has_snippet = "```html" in block or re.search(r"(?i)html snippet", block)
        if missing:
            must_miss.append(f"report {i} missing labels: {', '.join(missing)}")
        if not has_snippet:
            must_miss.append(f"report {i} has no HTML snippet")
        print(
            f"[report {i}] labels: {len(REQUIRED_LABELS) - len(missing)}"
            f"/{len(REQUIRED_LABELS)} | snippet: {'yes' if has_snippet else 'NO'}"
        )
        for lab in ("Steps to Reproduce", "Expected", "Actual"):
            if not re.search(r"(?i)" + re.escape(lab), block):
                should_miss.append(f"report {i} lacks {lab}")
        first_line = next((l for l in block.splitlines() if l.strip()), "")
        if not WCAG_TITLE_RE.search(first_line):
            nice_miss.append(f"report {i} title lacks (WCAG x.y.z)")

    # 3. must_contain alternation groups
    for group in meta.get("must_contain", []):
        if not any(tok in text for tok in group):
            must_miss.append(f"none of {group!r} found")
    print(f"Key values: {len(meta.get('must_contain', [])) - sum(1 for m in must_miss if m.startswith('none of'))}"
          f"/{len(meta.get('must_contain', []))} groups present")

    # 4. stable IDs (should-tier)
    spec = meta.get("stable_ids")
    if spec:
        hits, total = 0, 0
        for kind, sel, hex8 in expected_id_hexes(spec):
            total += 1
            if hex8 in text:
                hits += 1
            else:
                should_miss.append(f"{kind} id {hex8} ({sel}) not found")
        print(f"Stable IDs: {hits}/{total} verified")
    else:
        print("Stable IDs: not checked for this fixture")

    # 5. honest N/A — hard fabrication trap
    for label in meta.get("na_fields", []):
        rows = label_line_re(label).findall(text)
        if not rows:
            print(f"N/A field '{label}': row absent (accepted — omission is not fabrication)")
            continue
        bad = [v.strip() for v in rows if v.strip() and not NA_TOKENS.search(v)]
        if bad:
            fabrications.append(f"'{label}' carries invented value(s): {bad[:2]}")
        else:
            print(f"N/A field '{label}': OK")

    # verdict
    print()
    for m in must_miss:
        print(f"MUST MISS: {m}")
    for f_ in fabrications:
        print(f"FABRICATION: {f_}")
    for s in should_miss:
        print(f"should miss: {s}")
    for n in nice_miss:
        print(f"nice miss: {n}")

    if must_miss or fabrications:
        status = "FAIL"
    elif should_miss or nice_miss:
        status = "WARN — musts pass, should/nice gaps above"
    else:
        status = "PASS"
    # Match sibling scorers: results always exit 0; the Status line is the
    # machine signal. Non-zero exits are reserved for usage errors.
    print(f"\nStatus: {status}")


if __name__ == "__main__":
    main()
