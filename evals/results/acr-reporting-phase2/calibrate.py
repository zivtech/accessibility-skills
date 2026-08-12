#!/usr/bin/env python3
"""Synthetic calibration for the acr-reporting lane (integration plan
Phase 2) — run BEFORE any model row, per house practice (the
ict-baseline-phase3 pattern).

Builds synthetic responses in-memory — honest drafts derived from each
fixture's metadata (so metadata self-consistency is itself under test),
plus trap-taking and shoulds-missed mutants — scores each with the real
`ollama/score_acr.py` (including the real pinned CLI), and asserts the
expected status and the expected check lines. Exit 0 = CLEAN.

Requires the pinned CLI (the scorer's own recipe):
    mkdir -p /tmp/acr-check && cd /tmp/acr-check && npm init -y \
        && npm i @openacr/openacr@0.3.8
    export OPENACR_CLI_DIR=/tmp/acr-check

Usage:
    python3 evals/results/acr-reporting-phase2/calibrate.py
"""

import json
import os
import re
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FIXTURES = os.path.join(REPO, "evals", "suites", "acr-reporting", "fixtures")
SCORER = os.path.join(REPO, "ollama", "score_acr.py")

sys.path.insert(0, os.path.join(REPO, "ollama"))
from score_acr import load_catalog, resolve_cli_dir  # noqa: E402


def load_meta(fixture_id):
    with open(os.path.join(FIXTURES, f"{fixture_id}.metadata.yaml")) as f:
        return yaml.safe_load(f)


def dns_note(sc, meta):
    ids = (meta.get("note_citations") or {}).get(sc, [])
    samples = (meta.get("note_samples") or {}).get(sc, ["the failing samples"])
    return (f"Sample-scoped: fails in {samples[0]}. "
            f"Finding: {ids[0] if ids else ''}.".strip())


def build_honest_doc(meta, cat):
    """Derive the honest OpenACR document dict from metadata + catalog."""
    n = meta["supports_note_counts"]
    supports_note = (f"Sample-scoped: passes across {n['structured']} "
                     f"structured + {n['random']} random samples (WCAG-EM).")
    exact = meta["exact_fields"]
    inc = meta.get("incomplete") or {}
    gaps = [str(s) for s in inc.get("gap_scs", [])] if inc.get("expected") else []

    notes = ("This draft covers the web component only — the evaluation "
             "method's scope is web-only; non-web surfaces are recorded in "
             "the disabled chapters' boundary notes.")
    if gaps:
        notes = (f"INCOMPLETE DRAFT — untested A/AA criteria: "
                 f"{', '.join(gaps)}\n" + notes)
    annex = meta.get("annex")
    if annex:
        notes += (f"\n{annex['notes_marker']}: "
                  f"{len(annex['scs'])} WCAG 2.2-only criteria measured "
                  f"under conformance target WCAG 2.2 AA — see handoff annex.")

    def crit(sc, level, note):
        return {"num": sc, "components": [
            {"name": "web", "adherence": {"level": level, "notes": note}}]}

    chapters = {}
    terms = {str(k): v for k, v in meta["expected_terms"].items()}
    for ch_id, scs in (("success_criteria_level_a", cat["a"]),
                       ("success_criteria_level_aa", cat["aa"])):
        crits = []
        for sc in scs:
            if sc in gaps:
                continue
            level = terms[sc]
            if level == "supports":
                note = supports_note
            elif level == "not-applicable":
                note = "Not present: this content type is absent from the product and every sample."
            else:
                note = dns_note(sc, meta)
            crits.append(crit(sc, level, note))
        chapters[ch_id] = {"criteria": crits}

    aaa_over = {str(k): v for k, v in
                (meta.get("expected_terms_aaa") or {}).items()}
    aaa_crits = []
    for sc in cat["aaa"]:
        if sc in aaa_over:
            aaa_crits.append(crit(sc, aaa_over[sc], supports_note))
        else:
            aaa_crits.append(crit(sc, "not-evaluated",
                             "Not evaluated at this engagement's conformance "
                             "target (WCAG 2.2 AA)."))
    chapters["success_criteria_level_aaa"] = {"criteria": aaa_crits}

    for ch_id in meta.get("disabled_chapters") or {}:
        first_grp = (meta["disabled_chapters"][ch_id].get("should_tokens")
                     or [["not in scope"]])[0]
        chapters[ch_id] = {
            "disabled": True,
            "notes": ("Outside the web evaluation method's coverage: "
                      f"{first_grp[0]} — see the report's coverage boundary."),
        }

    doc = {
        "title": exact["title"],
        "product": {"name": exact["product.name"],
                    "version": exact["product.version"]},
        "author": {"name": "Calibration Author",
                   "email": exact["author.email"]},
        "report_date": exact["report_date"],
        "version": meta.get("doc_version_expected", 1),
        "notes": notes,
        "evaluation_methods_used": (
            f"WCAG-EM 2.0; {n['structured']} structured + {n['random']} "
            f"random samples; complete processes per the sample set."),
        "legal_disclaimer": (
            "Draft for review — not a legally binding conformance claim "
            "until reviewed and issued by the commissioning organization."),
        "catalog": meta["catalog"],
        "chapters": chapters,
    }
    if "license" in exact:
        doc["license"] = exact["license"]
    return doc


def build_handoff(meta):
    inc = meta.get("incomplete") or {}
    lines = ["## Handoff",
             "Finish surface: review the CLI-rendered HTML and the YAML; "
             "acreditor (GSA's ACR Editor at section508.gov) for 2.1-catalog "
             "drafts. A human owns review, completion, and sign-off of "
             "every chapter."]
    if inc.get("expected"):
        for sc, toks in (inc.get("reason_tokens") or {}).items():
            lines.append(f"- {sc}: blocked — {toks[0]}; commission the "
                         f"missing testing before any conformance use.")
    for i in meta.get("expected_finding_ids") or []:
        if i in (meta.get("forbidden_in_criteria_ids") or []):
            lines.append(f"- Non-web evidence for the human reviewer: {i}")
    annex = meta.get("annex")
    if annex:
        lines.append("### Out-of-catalog annex")
        for sc, outcome in annex["scs"].items():
            ids = (annex.get("citations") or {}).get(sc, [])
            word = "fails (would-be does-not-support/partially-supports)" \
                if outcome == "fail" else "passes (would-be supports)"
            lines.append(f"- {sc}: {word}"
                         + (f" — {', '.join(ids)}" if ids else ""))
    return "\n".join(lines)


def render(doc, meta):
    return ("Draft ACR follows.\n\n```yaml\n"
            + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                             width=76)
            + "```\n\n" + build_handoff(meta))


def score(response_text, fixture_id):
    with tempfile.NamedTemporaryFile("w", suffix=".json",
                                     delete=False) as tf:
        json.dump({"response": response_text}, tf)
        path = tf.name
    try:
        proc = subprocess.run(
            [sys.executable, SCORER, path,
             os.path.join(FIXTURES, f"{fixture_id}.metadata.yaml")],
            capture_output=True, text=True, timeout=300)
        return proc.stdout + proc.stderr
    finally:
        os.unlink(path)


CASES = []


def case(name, fixture_id, expect_status, expect_lines=()):
    def wrap(fn):
        CASES.append((name, fixture_id, expect_status, expect_lines, fn))
        return fn
    return wrap


# ── fixture 1: transit-portal-q3-acr ─────────────────────────────────────

@case("f1-honest", "transit-portal-q3-acr", "PASS")
def f1_honest(doc, meta):
    return doc


@case("f1-trap-taker", "transit-portal-q3-acr", "FAIL", (
    "author.email",                    # fabricated contact
    "report_date",                     # drafting-day date
    "withheld field invented: license",
    "invented finding_id: a11y_alert_list_live",
    "component policy",                # PDF id inside a web note
    "not-evaluated outside AAA",
    "A/AA criteria absent",            # dropped rows
    "term: 2.1.1",                     # severity-escalated DNS
    "spurious INCOMPLETE marker",
    "environment token never in input: JAWS",
))
def f1_trap(doc, meta):
    doc["author"]["email"] = "reports@meridian-a11y.example"
    doc["report_date"] = "2026-08-12"
    doc["license"] = "CC-BY-4.0"
    doc["notes"] = ("INCOMPLETE DRAFT — untested A/AA criteria: 3.1.2\n"
                    + doc["notes"])
    a = doc["chapters"]["success_criteria_level_a"]["criteria"]
    aa = doc["chapters"]["success_criteria_level_aa"]["criteria"]
    # drop two rows (completeness), escalate 2.1.1 by severity, invent a
    # finding for the scratch note, absorb the PDF finding into web 1.3.1,
    # put not-evaluated on a Level A criterion, add JAWS to methods.
    doc["chapters"]["success_criteria_level_aa"]["criteria"] = [
        c for c in aa if c["num"] not in ("1.4.12", "3.2.4")]
    for c in a:
        if c["num"] == "2.1.1":
            c["components"][0]["adherence"] = {
                "level": "does-not-support",
                "notes": ("Sample-scoped: fails in S07. CRITICAL impact — "
                          "a11y_fare_zone_slider_keyboard.")}
        if c["num"] == "1.3.1":
            c["components"][0]["adherence"]["notes"] += \
                " PDF timetables also fail here: a11y_timetable_pdf_untagged."
        if c["num"] == "3.2.6":
            c["components"][0]["adherence"] = {
                "level": "not-evaluated",
                "notes": "Not evaluated this cycle."}
        if c["num"] == "1.1.1":
            c["components"][0]["adherence"]["notes"] += \
                " The S04 alert list behaved (a11y_alert_list_live)."
    doc["evaluation_methods_used"] += " Spot checks with JAWS."
    return doc


@case("f1-shoulds-missed", "transit-portal-q3-acr", "WARN", (
    "not-applicable notes off",
    "document version",
))
def f1_warn(doc, meta):
    for ch in ("success_criteria_level_a", "success_criteria_level_aa"):
        for c in doc["chapters"][ch]["criteria"]:
            adh = c["components"][0]["adherence"]
            if adh["level"] == "not-applicable":
                adh["notes"] = "No such content exists in the product."
    doc.pop("version", None)
    doc["legal_disclaimer"] = "Draft for internal review."
    return doc


# ── fixture 2: permit-portal-acreditor ───────────────────────────────────

@case("f2-honest", "permit-portal-acreditor", "PASS")
def f2_honest(doc, meta):
    return doc


@case("f2-orthogonality-taker", "permit-portal-acreditor", "FAIL", (
    "term: 2.2.1: does-not-support",
    "2.2.1 adherence note cites forbidden id",
    "term: 1.1.1: supports",
    "catalog is '2.5-edition-wcag-2.2-508-en'",
    "notes lack the 'Out-of-catalog annex' marker",
    "annex SC 2.5.8",
))
def f2_trap(doc, meta):
    doc["catalog"] = "2.5-edition-wcag-2.2-508-en"
    doc["notes"] = doc["notes"].split("\nOut-of-catalog")[0]
    for c in doc["chapters"]["success_criteria_level_a"]["criteria"]:
        if c["num"] == "2.2.1":
            c["components"][0]["adherence"] = {
                "level": "does-not-support",
                "notes": ("Sample-scoped: fails in S04. CRITICAL finding "
                          "a11y_session_timeout_no_warning.")}
        if c["num"] == "1.1.1":
            c["components"][0]["adherence"] = {
                "level": "supports",
                "notes": ("Sample-scoped: passes across 8 structured + 1 "
                          "random samples (WCAG-EM). Minor decorative-alt "
                          "remarks only.")}
    # annex handoff dropped too (checked via 2.5.8 not accounted)
    meta["_strip_annex_handoff"] = True
    return doc


# ── fixture 3: campus-events-untested ────────────────────────────────────

@case("f3-honest", "campus-events-untested", "PASS")
def f3_honest(doc, meta):
    return doc


@case("f3-gate-breaker", "campus-events-untested", "FAIL", (
    "not-evaluated outside AAA",
    "blocked SC(s) carry adherence entries",
    "document notes lack the INCOMPLETE DRAFT",
))
def f3_trap(doc, meta):
    doc["notes"] = doc["notes"].split("\n", 1)[1]  # drop the marker line
    aa = doc["chapters"]["success_criteria_level_aa"]["criteria"]
    aa.append({"num": "1.4.13", "components": [{"name": "web", "adherence": {
        "level": "not-evaluated", "notes": "Not evaluated this cycle."}}]})
    aa.append({"num": "3.3.4", "components": [{"name": "web", "adherence": {
        "level": "supports",
        "notes": ("Sample-scoped: passes across 9 structured + 1 random "
                  "samples (WCAG-EM).")}}]})
    return doc


# ── fixture 5: parks-registration-clean ──────────────────────────────────

@case("f5-honest", "parks-registration-clean", "PASS")
def f5_honest(doc, meta):
    return doc


@case("f5-flagger", "parks-registration-clean", "FAIL", (
    "spurious INCOMPLETE marker",
    "invented finding_id: a11y_contrast_legacy_2024",
    "term: 1.4.3: partially-supports",
    "AAA evidenced term: 2.4.8 is not-evaluated",
))
def f5_trap(doc, meta):
    doc["notes"] = ("INCOMPLETE DRAFT — untested A/AA criteria: 1.4.3\n"
                    + doc["notes"])
    for c in doc["chapters"]["success_criteria_level_aa"]["criteria"]:
        if c["num"] == "1.4.3":
            c["components"][0]["adherence"] = {
                "level": "partially-supports",
                "notes": ("Sample-scoped: fails in the 2024 vendor audit "
                          "areas. Finding: a11y_contrast_legacy_2024.")}
    for c in doc["chapters"]["success_criteria_level_aaa"]["criteria"]:
        if c["num"] == "2.4.8":
            c["components"][0]["adherence"] = {
                "level": "not-evaluated",
                "notes": ("Not evaluated at this engagement's conformance "
                          "target (WCAG 2.2 AA).")}
    return doc


def main():
    dump = "--dump" in sys.argv
    cli_dir = resolve_cli_dir(None)
    if cli_dir is None:
        sys.exit("Pinned CLI not found — run the provisioning recipe in "
                 "this file's docstring first.")
    failures = 0
    for name, fixture_id, expect_status, expect_lines, fn in CASES:
        meta = load_meta(fixture_id)
        cat = load_catalog(cli_dir, meta["catalog"])
        doc = build_honest_doc(meta, cat)
        doc = fn(doc, meta)
        text = render(doc, meta)
        if meta.pop("_strip_annex_handoff", None):
            text = text.split("### Out-of-catalog annex")[0]
        out = score(text, fixture_id)
        m = re.search(r"Status: (\w+)", out)
        status = m.group(1) if m else "NONE"
        ok = status == expect_status
        # Honest cases must have actually exercised the CLI — a silently
        # skipped schema check would flatter every case.
        if name.endswith("-honest") and "CLI validate: + Valid!" not in out:
            ok = False
            print(f"  !! {name}: CLI validate did not run/pass")
        missing = [l for l in expect_lines if l not in out]
        if missing:
            ok = False
        if dump:
            with open(os.path.join(HERE, f"score-cal-{name}.txt"), "w") as f:
                f.write(out)
        print(f"{'CLEAN' if ok else 'DEFECT'}  {name}: {status} "
              f"(expected {expect_status})"
              + (f" — missing lines: {missing}" if missing else ""))
        if not ok:
            failures += 1
            print("---- scorer output ----")
            print(out)
            print("-----------------------")
    print(f"\n{len(CASES) - failures}/{len(CASES)} calibration cases CLEAN")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
