"""Shared helpers for the score_* scripts. Keep stdlib-only."""
import re

# Gate semantics: this is an ESCALATION/ABORT gate, not a quality bar.
# A fixture "passes" a tier when must-find detection is >= this fraction;
# below it, the escalation runner promotes the fixture to the next tier.
# Headline detection rates in BENCHMARK.md are aggregate found/total counts,
# NOT this pass rate. Do not conflate the two when reporting.
MUST_FIND_ABORT_THRESHOLD = 0.4
PLANNER_SECTION_PASS_THRESHOLD = 0.7


def strip_thinking(text: str) -> tuple[str, bool]:
    """Remove closed <think> blocks. Returns (clean_text, truncated).

    truncated=True means an unclosed <think> remains after stripping —
    the response was cut off mid-chain-of-thought and must not be scored
    as a normal response.
    """
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    truncated = "<think>" in cleaned
    return cleaned, truncated


def detect_verdict(text: str, ladder: list[str]) -> str:
    """Three-tier verdict detection (post-003 scoring).

    1. Explicit declaration:  'Verdict: REVISE' (with optional markdown).
    2. Bolded conclusion line: '**PASS** — ...' (last occurrence wins —
       conclusions close the document; added 2026-07-13 after audits whose
       literal conclusion was '**PASS** — no CRITICAL or MAJOR findings'
       fell through to the fallback and matched boilerplate 'BLOCK').
    3. Fallback: whole-word scan, ladder order (most specific/severe first).
    """
    alternatives = "|".join(re.escape(v) for v in ladder)
    m = re.search(
        rf"(?:#\s*)?(?:\*\*)?Verdict(?:\*\*)?[:\s]+\*?\*?({alternatives})\b",
        text, re.IGNORECASE,
    )
    if m:
        return m.group(1).upper()
    conclusion_hits = re.findall(
        rf"^\s*(?:#+\s*)?\*\*({alternatives})\*\*\s*[—–-]",
        text, re.IGNORECASE | re.MULTILINE,
    )
    if conclusion_hits:
        return conclusion_hits[-1].upper()
    upper = text.upper()
    for v in ladder:
        if re.search(rf"\b{re.escape(v)}\b", upper):
            return v
    return "NONE"


# Withholding stems (withheld/declines/refuses) count as negation: they are
# the honest-refusal vocabulary, and a line like "the statement is withheld;
# saying the portal is conformant is unsupported" must survive the
# assertive-claim scan (calibration 2026-08-01).
NEGATION_RE = re.compile(
    r"(?i)\b(cannot|can't|not|no|never|neither|without"
    r"|withh[eo]ld\w*|declin\w*|refus\w*)\b")


def strip_negation_lines(text: str) -> str:
    """Drop negated lines and interrogative lines before the assertive-claim
    scan. Questions are not assertions: the first live baseline row (2026-08-01)
    quoted the commissioner's question — "Can the final report state that the
    portal 'is WCAG 2.2 AA conformant'?" — on a line with no negation word,
    directly above an explicit "Determination: No.", and the scan called it a
    fabrication. Adjudicated a false positive; '?' lines are now exempt."""
    return "\n".join(
        l for l in text.splitlines()
        if not NEGATION_RE.search(l) and "?" not in l
    )


def normalize_quotes(s: str) -> str:
    """Fold straight/curly single and double quotes to one form so keyword
    matching is quote-insensitive (rubrics write role='tab', audits write
    role="tab"). Post-003 scoring, 2026-07-13."""
    return re.sub(r"[\"'‘’“”]", "'", s)


def fallback_keywords(description: str, max_words: int = 4) -> list[str]:
    """Last-resort keyword extraction. Never returns an empty list."""
    words = [w.strip(".,;:()\"'") for w in description.split()[:max_words]]
    filtered = [w for w in words if len(w) > 3]
    return filtered or [w for w in words if w] or [description.strip()[:40]]


# ── ICT Testing Baseline test-ID fidelity (adoption plan Phase 3, step 11) ──
# Baseline test IDs (`5.C-ControlState`) are the exact-ID class local models
# fabricate. Ground truth is docs/ict-baseline-test-id-manifest.yaml; validity
# is PER-BASELINE (11.A-PageTitled is web-only, 11.A-DocumentTitled is
# documents-only). Comparison is case-insensitive on membership (a lowercased
# real ID is sloppy, not fabricated); grammar detection is deliberately narrow
# so version strings ("4.9.1"), WCAG SC numbers, and CSS selectors never match.

BASELINE_ID_RE = re.compile(r"\b\d{1,2}\.[A-Z]-[A-Za-z]{2,}\b", re.IGNORECASE)

BASELINE_MANIFEST_RELPATH = ("..", "docs", "ict-baseline-test-id-manifest.yaml")


def load_baseline_manifest(path: str | None = None) -> dict:
    """Load the test-ID manifest into the shape check_baseline_ids consumes.

    yaml is imported lazily so this module's import stays stdlib-only; every
    scorer that calls this already depends on PyYAML. A missing manifest is a
    hard usage error — the check must never silently pass on absent ground
    truth.
    """
    import os

    import yaml

    if path is None:
        path = os.path.join(os.path.dirname(__file__), *BASELINE_MANIFEST_RELPATH)
    with open(path) as f:
        man = yaml.safe_load(f)
    web = {t["id"] for t in man["web"]["tests"]}
    documents = {t["id"] for t in man["documents"]["tests"]}
    stale = {
        str(e["string"]).lower(): e
        for e in man["meta"].get("invalid_id_strings_on_published_pages", [])
    }
    return {
        "web_ids": web,
        "web_lower": {i.lower(): i for i in web},
        "documents_lower": {i.lower(): i for i in documents},
        "stale": stale,
    }


def check_baseline_ids(
    text: str,
    manifest: dict,
    *,
    declared: bool,
    expected_ids: tuple | list = (),
) -> dict:
    """Classify every baseline-test-ID-shaped token in `text`.

    Returns a dict of sorted lists:
      cited            — every distinct grammar-shaped token found
      valid            — tokens that are real WEB baseline IDs
      fabricated       — tokens in neither baseline's list (hard failure);
                         entries are (token, hint) where hint names the
                         upstream stale string's valid ID when applicable
      cross_baseline   — documents-only IDs (hard when filed on a web finding;
                         verify context when they appear in prose)
      undeclared       — equals `cited` when declared is False: any baseline
                         citation outside declared 508 scope is a violation
                         (the checklist-creep tripwire)
      expected_missing — expected_ids with no token in the text
    """
    tokens = {m.group(0) for m in BASELINE_ID_RE.finditer(text)}
    web_lower = manifest["web_lower"]
    documents_lower = manifest["documents_lower"]
    stale = manifest["stale"]

    valid, fabricated, cross = [], [], []
    for tok in sorted(tokens):
        low = tok.lower()
        if low in web_lower:
            valid.append(tok)
        elif low in documents_lower:
            cross.append(tok)
        elif low in stale:
            entry = stale[low]
            fabricated.append(
                (tok, f"upstream stale string, never a valid ID — the valid ID is {entry['valid_id']}")
            )
        else:
            fabricated.append((tok, "no such test in either baseline"))

    text_lower = text.lower()
    expected_missing = [e for e in expected_ids if e.lower() not in text_lower]

    return {
        "cited": sorted(tokens),
        "valid": valid,
        "fabricated": fabricated,
        "cross_baseline": cross,
        "undeclared": sorted(tokens) if (tokens and not declared) else [],
        "expected_missing": expected_missing,
    }
