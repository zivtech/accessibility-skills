#!/usr/bin/env python3
"""Rule-based scorer for the a11y-content-judgment eval lane (wave-2 item #1,
2026-09-02; docs/plans/2026-09-02-promotion-candidate-dispositions.md).

Scores a model's per-row content judgments (the judge step of
.claude/skills/a11y-content-judgment — one JSON line per input row) against a
fixture's metadata (evals/suites/a11y-content-judgment/fixtures/*.metadata.yaml).

Two families of checks, labelled so an A/B reader knows what each arm carries:

CONTRACT-priced (the output contract is in the fixture task line, so both the
rubric and the no-rubric baseline receive it):
  C1 must   one output line per input id — no missing, duplicate, or extra ids
  C2 must   judgment in {yes,no,unsure}; drafted_by non-empty
  C3 should confidence in {high,medium,low}; needs_human true whenever unsure;
            fix empty on yes; rationale <= 25 words

RUBRIC-priced (only the rubric arm is told how to judge):
  R1 must   every expected-`no` must-tier row judged `no` (rows marked
            unsure_ok accept `unsure`, counted as deferred)
  R2 must   no expected-`yes` must-tier row judged `no` (false alarm — the
            half that matters more); `unsure` on such a row is a should-tier
            over-hedge (the GT-12 calibration class)
  R3 info   calibration-tier rows (borderline / convention-dependent) are
            reported, never counted toward status
  R4 must   fabricated fact, list form: any metadata `fabricated_tokens` value
            in a rationale or fix
  R5 tiered fabricated fact, quoted-span form: a quoted span of >= 3 words in
            a rationale that appears (normalized) in neither the row's fields
            nor that line's own fix; tier from metadata
            `fabrication_quoted_span_tier` (default should — see the
            calibration receipt before promoting it to must)
  R6 should a `no` rationale names what the person loses (>= 1 of the row's
            `loses` phrases, substring, case-insensitive; the phrases are
            blind-authored, so the WARN rate here is uncalibrated)
  R7 should every pattern_group is unanimous

Rows marked `invalid: true` in the metadata (a demonstrated row-evidence
defect found after the freeze) are excluded from every check and listed.

Status: PASS (all musts, no fabrication), WARN (musts pass, should missed),
FAIL (any must missed or fabrication detected). Results always exit 0;
non-zero exits are reserved for usage errors.

Usage:
    python3 ollama/score_content_judgment.py <response.json> <metadata.yaml>
"""

import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from score_common import normalize_quotes, strip_thinking  # noqa: E402

JUDGMENTS = ("yes", "no", "unsure")
CONFIDENCES = ("high", "medium", "low")
FENCE_RE = re.compile(r"```(?:jsonl?|json)?\s*\n(.*?)```", re.DOTALL)
QUOTED_RE = re.compile(r"[\"“”‘’']([^\"“”‘’']{3,}?)[\"“”‘’']")
WS_RE = re.compile(r"\s+")


def norm(s):
    return WS_RE.sub(" ", normalize_quotes(str(s or "")).lower()).strip()


def load_response(path):
    with open(path) as f:
        data = json.load(f)
    raw = data.get("response") or data.get("content") or ""
    text, truncated = strip_thinking(raw)
    if data.get("done_reason") == "length":
        truncated = True
    return text, truncated


def parse_lines(text):
    """Return (lines, note). Prefer fenced jsonl; fall back to any line that
    parses as an object with an id."""
    blocks = FENCE_RE.findall(text)
    source = "\n".join(blocks) if blocks else text
    lines, bad = [], 0
    for ln in source.splitlines():
        ln = ln.strip().rstrip(",")
        if not ln.startswith("{"):
            continue
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError:
            bad += 1
            continue
        if isinstance(obj, dict) and "id" in obj:
            lines.append(obj)
    return lines, f"{len(blocks)} fence(s), {bad} unparseable object line(s)"


def row_fields_text(row):
    parts = [row.get(k) for k in ("name", "detail", "href", "context", "landmark")]
    parts += [str(f) for f in (row.get("flags") or [])]
    return norm(" | ".join(str(p) for p in parts if p))


def quoted_span_hits(rationale, row, fix):
    """Quoted spans of >= 3 words absent from the row's fields and the line's own fix."""
    haystack = row_fields_text(row) + " | " + norm(fix)
    hits = []
    for span in QUOTED_RE.findall(rationale or ""):
        s = norm(span)
        if len(s.split()) < 3:
            continue
        if s not in haystack:
            hits.append(span)
    return hits


def word_count(s):
    return len(re.findall(r"\S+", s or ""))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit("Usage: ollama/score_content_judgment.py <response.json> <metadata.yaml>")
    text, truncated = load_response(args[0])
    if truncated:
        print("Response truncated (done_reason=length or open <think>) — not scoring")
        print("Status: INCOMPLETE — truncated response")
        return
    with open(args[1]) as f:
        meta = yaml.safe_load(f)
    rows_meta = meta.get("rows") or {}
    fixture_rows = {r["id"]: r for r in meta.get("input_rows") or []}
    fab_tokens = [t for t in (meta.get("fabricated_tokens") or []) if t]
    span_tier = (meta.get("fabrication_quoted_span_tier") or "should").lower()

    must_miss, should_miss, fabrications, info = [], [], [], []

    lines, parse_note = parse_lines(text)
    print(f"Parsed: {len(lines)} judgment line(s) ({parse_note})")
    if not lines:
        print("No judgment lines found")
        print("Status: INCOMPLETE — no parseable output")
        return

    invalid = sorted(i for i, m in rows_meta.items() if m.get("invalid"))
    active = {i: m for i, m in rows_meta.items() if not m.get("invalid")}
    if invalid:
        info.append(f"invalid rows excluded ({len(invalid)}): {', '.join(invalid)}")

    # C1 — one line per id
    seen = {}
    for obj in lines:
        seen.setdefault(str(obj["id"]), []).append(obj)
    missing = sorted(i for i in active if i not in seen)
    dup = sorted(i for i, v in seen.items() if len(v) > 1 and i in active)
    extra = sorted(i for i in seen if i not in rows_meta)
    if missing:
        must_miss.append(f"C1 missing output for {len(missing)} id(s): {', '.join(missing[:8])}{' …' if len(missing) > 8 else ''}")
    if dup:
        must_miss.append(f"C1 duplicate output for {len(dup)} id(s): {', '.join(dup[:8])}")
    if extra:
        must_miss.append(f"C1 output for {len(extra)} id(s) not in the input: {', '.join(extra[:8])}")
    print(f"Coverage: {len(active) - len(missing)}/{len(active)} input ids answered"
          f" ({len(dup)} duplicated, {len(extra)} extra)")

    # per-row checks
    stats = {"must_no": [0, 0], "deferred": 0, "must_yes": [0, 0], "false_alarm": [],
             "over_hedge": [], "cal": [0, 0], "cal_mismatch": [], "loses_miss": [],
             "span_hits": [], "token_hits": [], "long_rationale": [], "needs_human_miss": [],
             "fix_on_yes": [], "bad_conf": [], "bad_judgment": [], "no_drafted_by": []}
    groups = {}
    for rid, m in active.items():
        objs = seen.get(rid)
        if not objs:
            continue
        obj = objs[0]
        j = norm(obj.get("judgment"))
        conf = norm(obj.get("confidence"))
        rationale = str(obj.get("rationale") or "")
        fix = str(obj.get("fix") or "")
        if j not in JUDGMENTS:
            stats["bad_judgment"].append(rid)
            continue
        if not str(obj.get("drafted_by") or "").strip():
            stats["no_drafted_by"].append(rid)
        if conf not in CONFIDENCES:
            stats["bad_conf"].append(rid)
        if j == "unsure" and obj.get("needs_human") is not True:
            stats["needs_human_miss"].append(rid)
        if j == "yes" and fix.strip():
            stats["fix_on_yes"].append(rid)
        if word_count(rationale) > 25:
            stats["long_rationale"].append(rid)

        expected = norm(m.get("expected"))
        tier = norm(m.get("tier") or "must")
        unsure_ok = bool(m.get("unsure_ok"))
        if tier == "calibration":
            stats["cal"][1] += 1
            ok = (j == expected) or (j == "unsure" and unsure_ok)
            if ok:
                stats["cal"][0] += 1
            else:
                stats["cal_mismatch"].append(f"{rid}({expected}->{j})")
        elif expected == "no":
            stats["must_no"][1] += 1
            if j == "no":
                stats["must_no"][0] += 1
            elif j == "unsure" and unsure_ok:
                stats["must_no"][0] += 1
                stats["deferred"] += 1
            else:
                must_miss.append(f"R1 expected-no row {rid} judged {j} ({m.get('reference', '?')})")
        elif expected == "yes":
            stats["must_yes"][1] += 1
            if j == "no":
                stats["false_alarm"].append(rid)
                must_miss.append(f"R2 false alarm: expected-yes row {rid} judged no ({m.get('reference', '?')})")
            elif j == "unsure" and not unsure_ok:
                stats["must_yes"][0] += 1
                stats["over_hedge"].append(rid)
            else:
                stats["must_yes"][0] += 1

        # fabrication, list form (R4) — rationale + fix
        blob = norm(rationale + " " + fix)
        for tok in fab_tokens:
            if norm(tok) in blob:
                stats["token_hits"].append(f"{rid}:{tok}")
        # fabrication, quoted-span form (R5)
        row = fixture_rows.get(rid) or {}
        for span in quoted_span_hits(rationale, row, fix):
            stats["span_hits"].append(f"{rid}:“{span}”")
        # loses (R6)
        if j == "no" and expected == "no" and tier != "calibration":
            loses = [norm(t) for t in (m.get("loses") or []) if t]
            if loses and not any(t in norm(rationale) for t in loses):
                stats["loses_miss"].append(rid)
        g = m.get("pattern_group")
        if g:
            groups.setdefault(g, {}).setdefault(j, []).append(rid)

    if stats["bad_judgment"]:
        must_miss.append(f"C2 judgment outside {{yes,no,unsure}} on {len(stats['bad_judgment'])} row(s): {', '.join(stats['bad_judgment'][:6])}")
    if stats["no_drafted_by"]:
        must_miss.append(f"C2 drafted_by empty on {len(stats['no_drafted_by'])} row(s)")
    for key, label in (("bad_conf", "C3 confidence outside {high,medium,low}"),
                       ("needs_human_miss", "C3 unsure without needs_human:true"),
                       ("fix_on_yes", "C3 non-empty fix on a yes"),
                       ("long_rationale", "C3 rationale over 25 words")):
        if stats[key]:
            should_miss.append(f"{label} on {len(stats[key])} row(s): {', '.join(stats[key][:6])}")
    if stats["over_hedge"]:
        should_miss.append(f"R2 over-hedge: expected-yes row(s) judged unsure ({len(stats['over_hedge'])}): {', '.join(stats['over_hedge'][:8])}")
    if stats["token_hits"]:
        fabrications.append(f"R4 fabricated token(s) in rationale/fix: {', '.join(stats['token_hits'][:8])}")
    if stats["span_hits"]:
        line = f"R5 quoted span(s) absent from the row ({len(stats['span_hits'])}): {'; '.join(stats['span_hits'][:6])}"
        (fabrications if span_tier == "must" else should_miss).append(line)
    if stats["loses_miss"]:
        should_miss.append(f"R6 no-rationale names none of the row's loses phrases on {len(stats['loses_miss'])} row(s): {', '.join(stats['loses_miss'][:8])}")
    for g, byj in groups.items():
        if len(byj) > 1:
            should_miss.append(f"R7 pattern_group {g!r} not unanimous: " + ", ".join(f"{k}={len(v)}" for k, v in byj.items()))

    print(f"Must-no rows (R1): {stats['must_no'][0]}/{stats['must_no'][1]} found"
          + (f" ({stats['deferred']} deferred as unsure_ok)" if stats["deferred"] else ""))
    print(f"Clean rows (R2): {stats['must_yes'][0]}/{stats['must_yes'][1]} unflagged; false alarms: {len(stats['false_alarm'])}"
          + (f" [{', '.join(stats['false_alarm'][:8])}]" if stats["false_alarm"] else "")
          + (f"; over-hedged: {len(stats['over_hedge'])}" if stats["over_hedge"] else ""))
    if stats["cal"][1]:
        print(f"Calibration rows (R3, informational): {stats['cal'][0]}/{stats['cal'][1]} agree"
              + (f" — {', '.join(stats['cal_mismatch'])}" if stats["cal_mismatch"] else ""))
    print(f"Fabrication (R4 tokens): {len(stats['token_hits'])} hit(s); (R5 quoted spans, {span_tier}-tier): {len(stats['span_hits'])} hit(s)")
    for line in info:
        print(f"Info: {line}")
    for line in must_miss:
        print(f"MUST MISS: {line}")
    for line in fabrications:
        print(f"FABRICATION: {line}")
    for line in should_miss:
        print(f"should miss: {line}")

    if must_miss or fabrications:
        status = "FAIL"
    elif should_miss:
        status = "WARN"
    else:
        status = "PASS"
    print(f"\nStatus: {status}")


if __name__ == "__main__":
    main()
