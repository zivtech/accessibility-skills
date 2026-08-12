#!/usr/bin/env python3
"""Rule-based scorer for the acr-reporting eval lane (integration plan
Phase 2, docs/plans/2026-08-12-openacr-integration-plan.md).

Scores a model-produced OpenACR draft (the serialization of a finished
audit-scope evaluation, shaped by .claude/skills/acr-reporting/SKILL.md)
against a fixture's metadata expectations
(evals/suites/acr-reporting/fixtures/*.metadata.yaml):

1. Structural — one ACR-shaped ```yaml fence, parseable; the pinned
   @openacr/openacr CLI validates the exact document text
2. Catalog A/AA completeness (ground truth read from the installed catalog
   file — the check the CLI provably lacks, per the Phase 0 spike)
3. Per-level term legality — not-evaluated outside AAA is a must-fail even
   though the CLI validates it (spike-verified gap)
4. Term mapping per SC (deterministic; severity never moves a term)
5. Canonical note forms + finding_id citations (the cited value is
   compared per SC, per score_bugreport discipline) + forbidden ids
6. Value provenance — exact metadata fields; withheld fields stay absent;
   a different well-formed value is a fabrication, not a miss
7. INCOMPLETE protocol (marker + gap list + omissions + handoff reasons),
   and its false-positive direction on complete fixtures
8. Out-of-catalog annex (dual-catalog fixtures)
9. Chapter policy — disabled 508 chapters with canonical boundary notes,
   web-only scope statement, AAA evidence map

Status: PASS (all musts, no fabrication), WARN (musts pass, should
missed), FAIL (any must missed or fabrication detected). Results always
exit 0; non-zero exits are reserved for usage errors.

CLI provisioning (once per machine; the repo gains no package.json):
    mkdir -p /tmp/acr-check && cd /tmp/acr-check && npm init -y \
        && npm i @openacr/openacr@0.3.8
    export OPENACR_CLI_DIR=/tmp/acr-check

Usage:
    python3 ollama/score_acr.py <response.json> <metadata.yaml> \
        [--cli-dir DIR] [--skip-cli]
"""

import datetime
import json
import os
import re
import subprocess
import sys
import tempfile

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from score_common import strip_thinking  # noqa: E402

YAML_FENCE_RE = re.compile(r"```ya?ml\s*\n(.*?)```", re.DOTALL)
SUCCESS_CHAPTERS = (
    "success_criteria_level_a",
    "success_criteria_level_aa",
    "success_criteria_level_aaa",
)
DISABLED_STEM = "Outside the web evaluation method's coverage:"
INCOMPLETE_RE = re.compile(
    r"INCOMPLETE DRAFT\s*[—–-]+\s*untested A/AA criteria:", re.IGNORECASE)
SC_TOKEN_RE = re.compile(r"\b\d\.\d+\.\d+\b")
FAIL_CLASS = ("fail", "not met", "does-not-support", "does not support",
              "partially-supports", "partially supports")
PASS_CLASS = ("pass", "supports", "met")


def norm_scalar(v):
    """Fold YAML-typed scalars (dates, floats) to comparison strings."""
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.strftime("%Y-%m-%d")
    return str(v).strip()


def get_path(doc, dotted):
    cur = doc
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def load_response(path):
    with open(path) as f:
        data = json.load(f)
    text = data["response"] if isinstance(data, dict) else str(data)
    return strip_thinking(text)


def extract_acr_yaml(text):
    """Return (yaml_text, doc, remainder). Picks the largest fence whose
    parse is a dict with 'chapters'; remainder is the response minus the
    chosen fence (handoff prose; other fences stay in the remainder)."""
    best = None
    for m in YAML_FENCE_RE.finditer(text):
        body = m.group(1)
        try:
            parsed = yaml.safe_load(body)
        except yaml.YAMLError:
            continue
        if isinstance(parsed, dict) and "chapters" in parsed:
            if best is None or len(body) > len(best[0]):
                best = (body, parsed, m.span())
    if best is None:
        return None, None, text
    start, end = best[2]
    return best[0], best[1], text[:start] + text[end:]


def resolve_cli_dir(arg_dir):
    for cand in (arg_dir, os.environ.get("OPENACR_CLI_DIR"), "/tmp/acr-check"):
        if cand and os.path.isdir(
                os.path.join(cand, "node_modules", "@openacr", "openacr")):
            return cand
    return None


def cli_validate(cli_dir, yaml_text):
    """Run the pinned CLI's validate on the exact document text."""
    bin_path = os.path.join(cli_dir, "node_modules", ".bin", "openacr")
    with tempfile.NamedTemporaryFile(
            "w", suffix=".yaml", delete=False) as tf:
        tf.write(yaml_text)
        tmp = tf.name
    try:
        proc = subprocess.run(
            [bin_path, "validate", "-f", tmp],
            capture_output=True, text=True, timeout=120, cwd=cli_dir)
        out = (proc.stdout + proc.stderr).strip()
        return "Valid!" in out, out
    finally:
        os.unlink(tmp)


def load_catalog(cli_dir, catalog_id):
    """Ground truth from the installed catalog: {'a': [...], 'aa': [...],
    'aaa': [...], 'chapter_of': {sc: chapter}, 'terms': [...],
    'five08': [...]}."""
    path = os.path.join(cli_dir, "node_modules", "@openacr", "openacr",
                        "catalog", f"{catalog_id}.yaml")
    with open(path) as f:
        cat = yaml.safe_load(f)
    out = {"a": [], "aa": [], "aaa": [], "chapter_of": {}, "five08": [],
           "terms": [t["id"] for t in cat.get("terms", [])]}
    for ch in cat["chapters"]:
        ids = [str(c["id"]) for c in ch.get("criteria", [])]
        if ch["id"] == "success_criteria_level_a":
            out["a"] = ids
        elif ch["id"] == "success_criteria_level_aa":
            out["aa"] = ids
        elif ch["id"] == "success_criteria_level_aaa":
            out["aaa"] = ids
        else:
            out["five08"].append(ch["id"])
        if ch["id"] in SUCCESS_CHAPTERS:
            for i in ids:
                out["chapter_of"][i] = ch["id"]
    return out


def collect_entries(doc):
    """{sc: {'chapter': id, 'level': term, 'notes': str}} for web/default
    adherence entries across the success chapters. The web component is the
    graded one; FPC-style 'none' components are ignored here."""
    entries = {}
    chapters = doc.get("chapters") or {}
    for ch_id in SUCCESS_CHAPTERS:
        ch = chapters.get(ch_id)
        if not isinstance(ch, dict):
            continue
        for crit in ch.get("criteria") or []:
            num = str(crit.get("num", "")).strip()
            for comp in crit.get("components") or []:
                if comp.get("name") != "web":
                    continue
                adh = comp.get("adherence") or {}
                entries[num] = {
                    "chapter": ch_id,
                    "level": str(adh.get("level", "")).strip(),
                    "notes": str(adh.get("notes", "") or ""),
                }
    return entries


def any_token(text, tokens):
    low = text.lower()
    return any(t.lower() in low for t in tokens)


def sc_lines(text, sc):
    return [l for l in text.splitlines() if sc in l]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    skip_cli = "--skip-cli" in sys.argv
    cli_arg = None
    for i, a in enumerate(sys.argv):
        if a == "--cli-dir" and i + 1 < len(sys.argv):
            cli_arg = sys.argv[i + 1]
            args = [x for x in args if x != cli_arg]
    if len(args) != 2:
        sys.exit("Usage: ollama/score_acr.py <response.json> <metadata.yaml>"
                 " [--cli-dir DIR] [--skip-cli]")

    text, truncated = load_response(args[0])
    if truncated:
        print("Response truncated mid-<think> block — not scoring")
        print("Status: INCOMPLETE — truncated response")
        return
    with open(args[1]) as f:
        meta = yaml.safe_load(f)

    cli_dir = resolve_cli_dir(cli_arg)
    if cli_dir is None and not skip_cli:
        sys.exit(
            "Pinned CLI not found. Provision it once:\n"
            "  mkdir -p /tmp/acr-check && cd /tmp/acr-check && "
            "npm init -y && npm i @openacr/openacr@0.3.8\n"
            "then re-run (or set OPENACR_CLI_DIR / pass --cli-dir; "
            "--skip-cli scores without schema validation — smoke only).")

    must_miss, should_miss, fabrications = [], [], []
    print(f"Fixture: {meta['fixture_id']}")
    print(f"Response length: {len(text)} chars")

    # 1. structural: fence + parse + CLI validate
    yaml_text, doc, remainder = extract_acr_yaml(text)
    if doc is None:
        must_miss.append("no parseable ACR-shaped ```yaml fence "
                         "(dict with 'chapters')")
        print("\nStructural: X no ACR YAML fence found")
        doc, yaml_text = {}, ""
    else:
        print(f"\nStructural: + ACR YAML fence parsed "
              f"({len(yaml_text)} chars)")
    if yaml_text and cli_dir and not skip_cli:
        ok, out = cli_validate(cli_dir, yaml_text)
        print(f"CLI validate: {'+ Valid!' if ok else 'X ' + out[:300]}")
        if not ok:
            must_miss.append(f"openacr validate failed: {out[:200]}")
    elif skip_cli:
        print("CLI validate: SKIPPED (--skip-cli — smoke only, "
              "not a scoreable gate row)")

    catalog_id = meta["catalog"]
    doc_catalog = str(doc.get("catalog", "")).strip()
    if doc_catalog != catalog_id:
        must_miss.append(f"catalog is '{doc_catalog}', engagement requires "
                         f"'{catalog_id}' (no silent catalog change)")
    print(f"Catalog: {'+' if doc_catalog == catalog_id else 'X'} "
          f"{doc_catalog or '(absent)'}")

    cat = None
    if cli_dir:
        cat = load_catalog(cli_dir, catalog_id)
    entries = collect_entries(doc)

    # 2. catalog A/AA completeness (present-or-blocked)
    gap_scs = [str(s) for s in (meta.get("incomplete") or {}).get(
        "gap_scs", [])] if (meta.get("incomplete") or {}).get(
        "expected") else []
    if cat:
        missing = [sc for sc in cat["a"] + cat["aa"]
                   if sc not in entries and sc not in gap_scs]
        extra = [sc for sc in entries
                 if sc not in cat["chapter_of"]]
        misplaced = [sc for sc, e in entries.items()
                     if sc in cat["chapter_of"]
                     and e["chapter"] != cat["chapter_of"][sc]]
        print(f"\nA/AA completeness: {len(cat['a'] + cat['aa']) - len(missing)}"
              f"/{len(cat['a'] + cat['aa'])} present-or-blocked"
              f"{'' if not missing else ' — missing: ' + ', '.join(missing[:8])}")
        if missing:
            must_miss.append(f"A/AA criteria absent (not blocked): "
                             f"{', '.join(missing[:10])}")
        if extra:
            must_miss.append(f"criteria outside the {catalog_id} catalog: "
                             f"{', '.join(extra[:6])}")
        if misplaced:
            must_miss.append(f"criteria in the wrong chapter: "
                             f"{', '.join(misplaced[:6])}")

    # 3. per-level term legality — the load-bearing gate
    illegal = [sc for sc, e in entries.items()
               if e["level"] == "not-evaluated"
               and e["chapter"] != "success_criteria_level_aaa"]
    if illegal:
        must_miss.append(f"not-evaluated outside AAA (the untested gate): "
                         f"{', '.join(illegal)}")
    print(f"Term legality: {'X not-evaluated on ' + ', '.join(illegal) if illegal else '+ not-evaluated confined to AAA'}")
    if cat:
        bad_terms = {sc: e["level"] for sc, e in entries.items()
                     if e["level"] not in cat["terms"]}
        if bad_terms:
            must_miss.append(f"non-catalog term strings: {bad_terms}")

    # 4. term mapping per SC
    expected_terms = {str(k): v for k, v in
                      (meta.get("expected_terms") or {}).items()}
    wrong = []
    for sc, want in expected_terms.items():
        got = entries.get(sc, {}).get("level")
        if got is not None and got != want:
            wrong.append(f"{sc}: {got} (expected {want})")
    print(f"\nTerm mapping: {len(expected_terms) - len(wrong)}"
          f"/{len(expected_terms)} as expected")
    for w in wrong:
        print(f"  X {w}")
        must_miss.append(f"term: {w}")

    # AAA evidence map: named AAA SCs take their evidenced term; every other
    # AAA entry must be not-evaluated (unevidenced terms are inventions).
    aaa_expected = {str(k): v for k, v in
                    (meta.get("expected_terms_aaa") or {}).items()}
    aaa_entries = {sc: e for sc, e in entries.items()
                   if e["chapter"] == "success_criteria_level_aaa"}
    for sc, want in aaa_expected.items():
        got = aaa_entries.get(sc, {}).get("level")
        if got != want:
            must_miss.append(f"AAA evidenced term: {sc} is {got} "
                             f"(expected {want})")
    aaa_invented = [sc for sc, e in aaa_entries.items()
                    if sc not in aaa_expected
                    and e["level"] != "not-evaluated"]
    if aaa_invented:
        must_miss.append(f"unevidenced AAA term(s): {', '.join(aaa_invented[:6])}")
    if not aaa_entries and (aaa_expected or cat):
        should_miss.append("AAA chapter absent (catalog device unused)")

    # 5. note forms + citations
    n_s = meta.get("supports_note_counts") or {}
    stem_re = None
    if n_s:
        stem_re = re.compile(
            rf"^Sample-scoped: passes across {n_s['structured']} structured "
            rf"\+ {n_s['random']} random samples? \(WCAG-EM\)\.")
    all_ids = set(meta.get("expected_finding_ids") or [])
    bad_stem, citing_supports = [], []
    for sc, e in entries.items():
        if e["level"] == "supports" and e["chapter"] != \
                "success_criteria_level_aaa":
            if stem_re and not stem_re.match(e["notes"].strip()):
                bad_stem.append(sc)
            if any(i in e["notes"] for i in all_ids):
                citing_supports.append(sc)
    if bad_stem:
        must_miss.append(
            f"supports notes off the canonical stem ({len(bad_stem)}): "
            f"{', '.join(sorted(bad_stem)[:8])}")
    if citing_supports:
        must_miss.append(f"supports note cites a finding (contract forbids "
                         f"findings for passing checks): "
                         f"{', '.join(citing_supports)}")
    print(f"Supports-note stem: {len(bad_stem)} nonconforming; "
          f"{len(citing_supports)} citing findings")

    dns_stem = "Sample-scoped: fails in"
    for sc, ids in (meta.get("note_citations") or {}).items():
        sc = str(sc)
        e = entries.get(sc)
        if not e:
            continue  # absence already scored by completeness
        if not e["notes"].strip().startswith(dns_stem):
            must_miss.append(f"{sc} note lacks the '{dns_stem}' stem")
        if not any(i in e["notes"] for i in ids):
            must_miss.append(f"{sc} note cites none of {ids}")
        samples = (meta.get("note_samples") or {}).get(sc, [])
        if samples and not any_token(e["notes"], samples):
            must_miss.append(f"{sc} note names no failing sample of {samples}")

    for sc, ids in (meta.get("forbidden_citations") or {}).items():
        e = entries.get(str(sc))
        if e and any(i in e["notes"] for i in ids):
            must_miss.append(f"{sc} adherence note cites forbidden id(s) "
                             f"{ids} (resolved/out-of-component evidence)")

    forbidden_ids = meta.get("forbidden_in_criteria_ids") or []
    hit = [i for i in forbidden_ids
           if any(i in e["notes"] for e in entries.values())]
    if hit:
        must_miss.append(f"non-web evidence inside web criteria notes: "
                         f"{', '.join(hit)} (component policy)")

    na_off = [sc for sc, e in entries.items()
              if e["level"] == "not-applicable"
              and not e["notes"].strip().startswith("Not present:")]
    if na_off:
        should_miss.append(f"not-applicable notes off the 'Not present:' "
                           f"stem: {', '.join(sorted(na_off)[:6])}")

    # 6. value provenance
    print("\nValue provenance:")
    for path, want in (meta.get("exact_fields") or {}).items():
        got = get_path(doc, path)
        if got is None:
            must_miss.append(f"metadata field absent: {path}")
            print(f"  X {path}: absent")
        elif norm_scalar(got) != str(want):
            fabrications.append(
                f"{path} is '{norm_scalar(got)}' — record says '{want}'")
            print(f"  X {path}: '{norm_scalar(got)}' != '{want}'")
        else:
            print(f"  + {path}")
    for field in meta.get("forbidden_root_fields") or []:
        if field in doc:
            fabrications.append(
                f"withheld field invented: {field}: {doc[field]!r}")
    lm = doc.get("last_modified_date")
    rd_expected = (meta.get("exact_fields") or {}).get("report_date")
    if lm is not None and rd_expected and norm_scalar(lm) != str(rd_expected):
        fabrications.append(
            f"last_modified_date '{norm_scalar(lm)}' has no source "
            f"(report_date is {rd_expected})")
    ver_want = meta.get("doc_version_expected")
    if ver_want is not None and doc.get("version") != ver_want:
        should_miss.append(f"document version {doc.get('version')!r} "
                           f"(record says {ver_want})")

    found_ids = set(re.findall(meta["finding_id_pattern"], text))
    invented = sorted(found_ids - all_ids)
    for i in invented:
        fabrications.append(f"invented finding_id: {i}")
    print(f"  finding_id tokens: {len(found_ids & all_ids)} known, "
          f"{len(invented)} invented")
    for tok in meta.get("fabricated_tokens") or []:
        if re.search(rf"(?i)\b{re.escape(tok)}\b", text):
            fabrications.append(f"environment token never in input: {tok}")

    # 7. INCOMPLETE protocol
    inc = meta.get("incomplete") or {}
    notes_field = str(doc.get("notes", "") or "")
    if inc.get("expected"):
        m = INCOMPLETE_RE.search(notes_field)
        print(f"\nINCOMPLETE protocol: marker "
              f"{'present' if m else 'ABSENT'}")
        if not m:
            must_miss.append("document notes lack the INCOMPLETE DRAFT "
                             "marker + gap list")
        else:
            if not notes_field.strip().startswith(
                    notes_field[m.start():m.start() + 10]):
                should_miss.append("INCOMPLETE marker not at the start of "
                                   "the document notes")
            line = notes_field[m.end():].split("\n", 1)[0]
            listed = set(SC_TOKEN_RE.findall(line))
            expected_gaps = set(gap_scs)
            if listed != expected_gaps:
                must_miss.append(f"gap list is {sorted(listed)}, expected "
                                 f"{sorted(expected_gaps)}")
        present = [sc for sc in gap_scs if sc in entries]
        if present:
            must_miss.append(f"blocked SC(s) carry adherence entries: "
                             f"{', '.join(present)} (the untested gate)")
        for sc, toks in (inc.get("reason_tokens") or {}).items():
            lines = sc_lines(remainder, str(sc))
            if not lines or not any_token("\n".join(lines), toks):
                must_miss.append(f"handoff carries no reason for {sc}")
    else:
        if INCOMPLETE_RE.search(notes_field):
            must_miss.append("spurious INCOMPLETE marker on complete "
                             "evidence (false-positive control)")

    # 8. out-of-catalog annex
    annex = meta.get("annex")
    if annex:
        print("\nAnnex:")
        if annex["notes_marker"].lower() not in notes_field.lower():
            must_miss.append(f"document notes lack the "
                             f"'{annex['notes_marker']}' marker")
            print(f"  X notes marker absent")
        else:
            print(f"  + notes marker")
        for sc, outcome in (annex.get("scs") or {}).items():
            sc = str(sc)
            if sc in entries:
                must_miss.append(f"annex SC {sc} appears as a criteria row "
                                 f"(no catalog row exists for it)")
            lines = sc_lines(text, sc)
            klass = FAIL_CLASS if outcome == "fail" else PASS_CLASS
            ok = lines and any_token("\n".join(lines), klass)
            print(f"  {'+' if ok else 'X'} {sc} accounted ({outcome})")
            if not ok:
                must_miss.append(f"annex SC {sc} not accounted with its "
                                 f"{outcome} outcome")
            for i in (annex.get("citations") or {}).get(sc, []):
                if not any(i in l for l in lines):
                    must_miss.append(f"annex SC {sc} lacks citation {i}")

    # 9. chapter policy
    print("\n508 chapters:")
    chapters = doc.get("chapters") or {}
    for ch_id, spec in (meta.get("disabled_chapters") or {}).items():
        ch = chapters.get(ch_id) or {}
        disabled = ch.get("disabled") is True
        note = str(ch.get("notes", "") or "")
        stem_ok = note.strip().startswith(DISABLED_STEM)
        print(f"  {'+' if disabled and stem_ok else 'X'} {ch_id}"
              f" (disabled={disabled}, stem={'ok' if stem_ok else 'off'})")
        if not disabled:
            must_miss.append(f"{ch_id} not disabled: true")
        if not stem_ok:
            must_miss.append(f"{ch_id} note lacks the canonical "
                             f"boundary stem")
        for grp in spec.get("should_tokens") or []:
            if not any_token(note, grp):
                should_miss.append(f"{ch_id} note misses all of {grp[:3]}")

    for grp in meta.get("doc_notes_must") or []:
        if not any_token(notes_field, grp):
            must_miss.append(f"document notes miss all of {grp[:3]} "
                             f"(web-only scope statement)")
    methods = str(doc.get("evaluation_methods_used", "") or "")
    for grp in meta.get("methods_tokens") or []:
        if not any_token(methods, grp):
            must_miss.append(f"evaluation_methods_used misses all of "
                             f"{grp[:3]}")
    disclaimer = str(doc.get("legal_disclaimer", "") or "")
    for grp in meta.get("disclaimer_tokens_must") or []:
        if not any_token(disclaimer, grp):
            must_miss.append(f"legal_disclaimer misses all of {grp[:3]} "
                             f"(draft, never final)")
    for grp in meta.get("disclaimer_tokens_should") or []:
        if not any_token(disclaimer, grp):
            should_miss.append(f"legal_disclaimer misses all of {grp[:3]}")

    for grp in meta.get("handoff_should") or []:
        if not any_token(remainder, grp):
            should_miss.append(f"handoff misses all of {grp[:3]}")

    # verdict
    print(f"\nMust misses: {len(must_miss)}")
    for m in must_miss:
        print(f"  - {m}")
    print(f"Fabrications: {len(fabrications)}")
    for f_ in fabrications:
        print(f"  - {f_}")
    print(f"Should misses: {len(should_miss)}")
    for s in should_miss:
        print(f"  - {s}")

    if must_miss or fabrications:
        status = "FAIL"
    elif should_miss:
        status = "WARN"
    else:
        status = "PASS"
    print(f"\nStatus: {status}")


if __name__ == "__main__":
    main()
