#!/usr/bin/env python3
"""Run a11y skill benchmarks on local Ollama models.

Usage:
    python3 ollama/run_benchmark.py critic-remaining [model]       # All un-benchmarked critic fixtures (default: qwen3:32b)
    python3 ollama/run_benchmark.py bugreport <model> <fixture-id> # Bug-reporting single fixture
    python3 ollama/run_benchmark.py bugreport-remaining [model]    # All un-benchmarked bug-reporting fixtures
    python3 ollama/run_benchmark.py evalreport <model> <fixture-id>          # Evaluation-report single fixture (contract = system prompt)
    python3 ollama/run_benchmark.py evalreport-baseline <model> <fixture-id> # Same fixture, no contract (baseline condition)
    python3 ollama/run_benchmark.py evalreport-remaining [model]             # All un-benchmarked evaluation-report fixtures (contract condition)
    python3 ollama/run_benchmark.py acr <model> <fixture-id>                 # ACR-reporting single fixture (skill = system prompt)
    python3 ollama/run_benchmark.py acr-baseline <model> <fixture-id>        # Same fixture, no skill (baseline condition)
    python3 ollama/run_benchmark.py planner-federal <model> <fixture-id>     # Planner + a11y-test crosswalk in-prompt (declared-508 condition)
    python3 ollama/run_benchmark.py cj <model> <fixture-id>                  # Content-judgment single fixture (judgment rubric = system prompt)
    python3 ollama/run_benchmark.py cj-baseline <model> <fixture-id>         # Same fixture, no rubric (baseline condition)
    python3 ollama/run_benchmark.py titlehint <model> <fixture-id> <titled|neutral> <draw>  # H1 leak A/B (issue #51)
    python3 ollama/run_benchmark.py featurehint <model> <fixture-id> <withfeatures|nofeatures> <draw>  # features-section leak A/B (issue #51)
    python3 ollama/run_benchmark.py recipe <model> <fixture-id>              # a11y-test recipe review (a11y-test slice = system prompt)
    python3 ollama/run_benchmark.py recipe-baseline <model> <fixture-id>     # Same fixture, no slice (baseline condition)
    python3 ollama/run_benchmark.py ollama-clean                   # CLEAN fixtures, all models
    python3 ollama/run_benchmark.py ollama-bugs                    # HAS-BUGS fixtures, all models
    python3 ollama/run_benchmark.py single <model> <fixture-id>    # One fixture, one model
    python3 ollama/run_benchmark.py score-all                      # Score all critic response files in /tmp
    python3 ollama/run_benchmark.py perspective <model> <fixture-id>  # Perspective-audit single fixture
    python3 ollama/run_benchmark.py perspective-pilot [model]      # Pilot set (7 fixtures)
    python3 ollama/run_benchmark.py perspective-remaining [model]  # All un-benchmarked perspective fixtures
    python3 ollama/run_benchmark.py score-perspective              # Score all perspective response files in /tmp
"""

import json
import math
import os
import re
import sys
import time
import urllib.request

# --- Context-overflow guard (context-utilization plan Phase 0.2/0.3, 2026-08-24) ---
# Twin copy in ollama/ollama_a11y.py (this file: run_benchmark.py) — keep both
# in sync by hand; these are standalone scripts, not a shared package.
CHARS_PER_TOKEN_CONSERVATIVE = 3.5  # F15 (gate re-review round 4, 2026-08-25):
# real measured ratio — critic protocol (a11y-critic SKILL.md, frontmatter
# stripped, 60,373 chars) / prompt_eval_count on this lane's own
# num_predict=1 probe corpus (2026-08-25) = 4.23 chars/token (qwen3.6:35b) /
# 4.36 chars/token (qwen3:32b) — supersedes the earlier stale "16,157
# tokens / 3.74 chars/token" figure (wrong on both counts). 3.5 stays
# unchanged, still deliberately below both measured ratios — the safe
# direction — but by more than previously documented; see
# estimate_tokens()'s docstring for what that overestimate is in practice.
RESPONSE_RESERVE = 8192  # thinking models: reasoning tokens share num_ctx


def estimate_tokens(text):
    """Conservative token estimate. CHARS_PER_TOKEN_CONSERVATIVE (3.5) was
    documented as a ~7% overestimate against one earlier measured ratio;
    measured against this lane's real num_predict=1 probes
    (context-utilization-phase3, 2026-08-25 — gate F14 part 3, docs/plans/
    2026-08-25-context-utilization-phase3-gate-review.md "Final gate
    ruling") it overestimates by 22-30%, not ~7%: protocol alone, est
    17,480 vs measured 14,276 (qwen3.6:35b) / 13,853 (qwen3:32b) tokens =
    1.224x-1.262x; protocol + tabs-missing-arrow-nav fixture, est 19,004
    vs measured 15,167 / 14,649 = 1.253x-1.297x.

    The asymmetry this creates, stated plainly: a prompt that DOES get
    sent has MORE real headroom than the ~7% figure implies (measured
    margins are looser than believed) — but the guard's pass/fail decision
    runs on this inflated estimate, so it refuses real prompts that would
    have fit more often than a 7%-based mental model predicts (guard
    margins are tighter). CHARS_PER_TOKEN_CONSERVATIVE stays 3.5 — this is
    a documentation-accuracy fix, not a retune."""
    return math.ceil(len(text) / CHARS_PER_TOKEN_CONSERVATIVE)


def context_overflow(system_text, prompt_text, num_ctx, declared_context_length=None):
    """Client-side primary gate (F6/F7): does estimated prompt + response
    reserve exceed num_ctx? Returns (overflow: bool, estimated_tokens: int).

    F13 fast-follow (gate re-review, 2026-08-25): num_ctx alone is the
    REQUESTED window, not what Ollama will actually allocate. Proven live
    the same day — qwen3:32b requested at 49,152 was silently clamped
    server-side to its declared 40,960, and a 45,176-token prompt lost
    54.7% of itself to truncation (`prompt=45176 keep=4 new=20482`) while
    this exact guard, checking only the requested value, would have waved
    it through. declared_context_length (fetch_declared_context_length,
    below) is the model's real ceiling from /api/tags; when supplied, the
    guard compares against min(num_ctx, declared_context_length) instead of
    num_ctx alone — the estimate formula and RESPONSE_RESERVE are otherwise
    unchanged. None (the default) preserves the exact old behavior for any
    caller that hasn't been updated to pass it."""
    estimated = estimate_tokens((system_text or "") + (prompt_text or ""))
    effective_ctx = num_ctx if declared_context_length is None else min(num_ctx, declared_context_length)
    return estimated + RESPONSE_RESERVE > effective_ctx, estimated


class GuardConfigError(Exception):
    """fetch_declared_context_length's own failures (F13) — /api/tags
    unreachable, or the requested model missing from it, or present but
    carrying no context_length field. Always raised, never silently
    swallowed into a default ceiling — that would recreate the exact
    silent-clamp bug this fetch exists to catch."""


_DECLARED_CONTEXT_LENGTH_CACHE = {}  # F13: memoized per model for the process lifetime


def _tag_variants(model):
    """R5 follow-up (2026-08-27): /api/tags ALWAYS reports a tagged name
    ("laguna-xs-2.1:latest"), while callers routinely invoke the bare name
    ("laguna-xs-2.1") and every *_CTX map is keyed on whatever string the
    caller typed. Those are two namespaces, and before this they diverged
    silently: `laguna-xs-2.1` — the exact string with 12 committed critic
    rows AND a CRITIC_CTX entry — raised GuardConfigError, while
    `laguna-xs-2.1:latest` resolved. Try both spellings of the implicit
    ":latest" tag before declaring a model missing. Only ":latest" is
    implied; "qwen3.5:27b" and "qwen3.5:latest" are DIFFERENT models (9.7B
    vs a 27B that is not installed) and are never conflated here."""
    if ":" not in model:
        return [model, model + ":latest"]
    base, _, tag = model.rpartition(":")
    return [model, base] if tag == "latest" else [model]


def _fetch_context_length_from_show(model, show_url):
    """R5 follow-up (2026-08-27): some models list in /api/tags with a null
    details.context_length — gemma4:31b and gemma4:26b do, and both are
    mapped in CRITIC_CTX, so the F13 raise hard-blocked two mapped models
    from running any lane at all. /api/show carries the GGUF metadata the
    tags summary omits, as model_info["<arch>.context_length"].

    This is NOT a fallback guess and NOT a default: verified 2026-08-27 that
    /api/show agrees EXACTLY with /api/tags on every model that reports both
    (qwen3:32b 40960, qwen3.6:35b 262144, llama3.3:70b 131072, and the same
    262144 for gemma4 where tags is null). Same number, fuller source.
    Returns None on any failure so the caller still raises."""
    try:
        req = urllib.request.Request(
            show_url, data=json.dumps({"model": model}).encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            info = json.loads(resp.read()).get("model_info") or {}
    except Exception:
        return None
    hits = [v for k, v in info.items()
            if k.endswith(".context_length") and isinstance(v, int) and v > 0]
    return min(hits) if hits else None  # min: the safe direction if ever ambiguous


def ctx_for(model, mapping, default):
    """num_ctx lookup that tolerates the implicit-":latest" spelling gap
    (_tag_variants). Without it a map entry written bare misses a tagged
    invocation and the run silently falls to the _DEFAULT."""
    for variant in _tag_variants(model):
        if variant in mapping:
            return mapping[variant]
    return default


def fetch_declared_context_length(model, *, tags_url=None, show_url=None):
    """F13 fast-follow: the model's real context_length ceiling, from
    Ollama's own /api/tags (models[].details.context_length — confirmed
    live, 2026-08-25: qwen3:32b -> 40960, qwen3.6:35b -> 262144). Cached per
    model. Fails loud on any of: /api/tags unreachable, model not listed,
    or listed with no context_length field — never a silent default, since
    a default here would be exactly the bug this function exists to close.

    R5 follow-up (2026-08-27): resolves the implicit ":latest" tag
    (_tag_variants) and falls back to /api/show's GGUF model_info when
    /api/tags reports a null context_length (_fetch_context_length_from_show).
    Still fails loud when neither source has a value — never a silent
    default."""
    if model in _DECLARED_CONTEXT_LENGTH_CACHE:
        return _DECLARED_CONTEXT_LENGTH_CACHE[model]
    url = tags_url or OLLAMA_TAGS_URL
    show = show_url or url.replace("/api/tags", "/api/show")
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        raise GuardConfigError(f"F13 guard: cannot fetch declared context_length for {model!r} — "
                                f"/api/tags unreachable at {url}: {e}") from e
    listed = {entry.get("name"): entry for entry in data.get("models", [])}
    matched_name = next((v for v in _tag_variants(model) if v in listed), None)
    if matched_name is None:
        raise GuardConfigError(f"F13 guard: model {model!r} not found in /api/tags at {url} "
                                f"(installed: {sorted(n for n in listed if n)})")
    declared = (listed[matched_name].get("details") or {}).get("context_length")
    if declared is None:
        declared = _fetch_context_length_from_show(matched_name, show)
    if declared is None:
        raise GuardConfigError(f"F13 guard: model {model!r} found in /api/tags but neither its "
                                f"details nor /api/show at {show} carry a context_length — "
                                "cannot verify the real ceiling.")
    _DECLARED_CONTEXT_LENGTH_CACHE[model] = declared
    return declared



BASE_DIR = os.path.dirname(__file__)
RESULTS_DIR = os.environ.get("BENCHMARK_RESULTS_DIR", "/tmp")
FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "a11y-critic", "fixtures")
SKILL_PATH = os.path.join(BASE_DIR, "..", ".claude", "skills", "a11y-critic", "SKILL.md")

PERSPECTIVE_FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "perspectives", "fixtures")
PERSPECTIVE_SKILL_PATH = os.path.join(BASE_DIR, "..", ".claude", "skills", "perspective-audit", "SKILL.md")
PERSPECTIVE_REFS = [
    os.path.join(BASE_DIR, "..", ".claude", "skills", "perspective-audit", "references", "perspectives.md"),
    os.path.join(BASE_DIR, "..", ".claude", "skills", "perspective-audit", "references", "arrm-perspective-mapping.md"),
]

PLANNER_FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "a11y-planner", "fixtures")
PLANNER_SKILL_PATH = os.path.join(BASE_DIR, "..", ".claude", "skills", "a11y-planner", "SKILL.md")

BUGREPORT_FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "bug-reporting", "fixtures")
BUGREPORT_SKILL_PATH = os.path.join(BASE_DIR, "..", ".claude", "skills", "bug-reporting", "SKILL.md")

BUGREPORT_FIXTURES = [
    "axe-button-name-federal",  # 7th fixture, declared-508 (ICT baseline Phase 3 step 11, 2026-08-12) — no model rows yet
    "axe-image-alt-single",
    "axe-select-name-dedup",
    "axe-two-rules-split",
    "kat-focus-appearance",
    "manual-sr-finding-prose",
    "sparse-scan-adversarial",
]

# Declared-508 planner condition (ICT baseline adoption plan, Phase 3 step 10).
# `planner-federal` appends the a11y-test coverage crosswalk to the planner
# system prompt — the report-contract-as-system-prompt precedent: models
# cannot read repo files, so the reference the profile says to source the
# coverage statement from must be supplied in-prompt. Plain `planner` on the
# same fixture is the no-crosswalk condition (the fabrication check
# instruments what the plan does without the reference).
CROSSWALK_PATH = os.path.join(
    BASE_DIR, "..", ".claude", "skills", "a11y-test", "references",
    "ict-baseline-crosswalk.yaml",
)

# Evaluation-report lane (adoption plan step 11b, 2026-08-01). The system
# prompt is the report contract itself — this is a prompt-only repo, so the
# contract IS the skill under test. No prompt prefix: the fixture .md carries
# its own minimal task instruction, and the honesty rules being graded must
# come from the contract, not the task prompt (see fixture metadata notes).
EVALREPORT_FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "evaluation-report", "fixtures")
EVALREPORT_CONTRACT_PATH = os.path.join(BASE_DIR, "..", "docs", "a11y-evaluation-report-contract.md")

EVALREPORT_FIXTURES = [
    "transit-portal-q3",
]

# ACR-reporting lane (OpenACR integration plan Phase 2, 2026-08-12). The
# system prompt is the acr-reporting SKILL.md — the skill IS the instrument,
# same loading idea as the evaluation-report lane. No prompt prefix: the
# fixture .md carries its own minimal task instruction, and the gates being
# graded (mapping, untested gate, note forms, value provenance) must come
# from the skill, not the task prompt.
ACR_FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "acr-reporting", "fixtures")
ACR_SKILL_PATH = os.path.join(BASE_DIR, "..", ".claude", "skills", "acr-reporting", "SKILL.md")

ACR_FIXTURES = [
    "transit-portal-q3-acr",
    "permit-portal-acreditor",
    "campus-events-untested",
    "parks-registration-clean",
    "county-library-retest",
    "utility-billing-retest",
    "court-payments-independence",
]

# a11y-test-operation-evidence lane (WP-B, PT-01, 2026-09-02). The system
# prompt is a heading-anchored slice of the a11y-test SKILL.md — the
# "### Operation-evidence admissibility" section plus its "### Structured
# disposition block" contract, up to (not including) "### PASS partition".
# No prompt prefix beyond the task instruction below: the fixture .md carries
# the operation description + evidence package verbatim, and the five
# admissibility rules being graded must come from the skill slice, not the
# task prompt.
OPEVIDENCE_FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "a11y-test-operation-evidence", "fixtures")

OPEVIDENCE_FIXTURES = [
    "op-dialog-escape-overreach",
    "op-empty-state-coverage-shortcuts",
    "op-human-signature-only",
    "op-human-walkthrough-clean",
    "op-mixed-package-partial",
    "op-retest-clean",
]

# a11y-content-judgment lane (wave-2 item #1, 2026-09-02). The system prompt
# is the skill's judge-facing rubric (references/judgment-rubric.md) — the
# only file the judge step reads in the skill's own pipeline; SKILL.md is the
# orchestrator's protocol and judge-prompt.md is subagent plumbing. The
# fixture .md carries the batch rows plus the output contract (keys, one
# JSON line per row) so the no-rubric baseline is scorable; everything the
# lane grades — in-context judging, image-role routing, "length alone is
# never a no", never inventing destination content, one verdict per
# construct — must come from the rubric.
CJ_FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "a11y-content-judgment", "fixtures")
CJ_RUBRIC_PATH = os.path.join(BASE_DIR, "..", ".claude", "skills", "a11y-content-judgment", "references", "judgment-rubric.md")

CJ_FIXTURES = [
    "page-titles-shared",
    "link-purpose-cards",
    "images-role-routing",
    "headings-fields-labels",
    "identification-across-views",
    "clean-control",
]

# a11y-test-recipe lane (GT-16, wave 2, 2026-09-03). The artifact under
# review is a keyboard test recipe plus the run output it produced, against
# the component it targets; the graded judgment is whether the recipe's
# recorded outcome is supported by its own evidence. The system prompt is
# three heading-anchored slices of the a11y-test SKILL.md: the verification
# evidence contract (with the detector-lane authority boundary), the keyboard
# test method, and the live-site / SPA / CSS / ARIA-check sections that follow
# the APG templates -- the recipe-authoring guidance as it stands. Nothing in
# the slice speaks to selector semantics; that absence is what the lane
# measures, fixture-first, before any SKILL.md sentence lands.
RECIPE_FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "a11y-test-recipe", "fixtures")

RECIPE_FIXTURES = [
    "dialog-dismiss-recipe",
    "dialog-dismiss-recipe-clean",
]

RECIPE_SLICES = (
    ("## Verification evidence contract", "## Retest classification"),
    ("## 1. Keyboard Accessibility Tests", "### WAI-ARIA APG Keyboard Test Templates"),
    ("### Live Site Requirement", "## Section 5:"),
)

RECIPE_PROMPT_PREFIX = (
    "Review the following keyboard test recipe, its run output, and the component "
    "it targets. Decide whether the recipe's recorded outcome is supported by its "
    "own evidence. Open with `VERDICT: ACCEPT` (the recipe and its recorded outcome "
    "stand as filed) or `VERDICT: REVISE` (the recipe must change before its outcome "
    "can be filed), then list every issue with a severity (CRITICAL / MAJOR / MINOR / "
    "ENHANCEMENT) and a `filename.md:<line>` citation into the fixture.\n\n"
)

OPEVIDENCE_PROMPT_PREFIX = (
    "Review the following operation-evidence package for admissibility under "
    "the rules in the system prompt. Give your reasoning, then close with the "
    "structured disposition block.\n\n"
)

PROMPT_PREFIX = "Review the following React component for accessibility design issues. Execute all phases of the investigation protocol.\n\n"
PLANNER_PROMPT_PREFIX = "Plan the accessible implementation for the following component or feature. Execute all phases of the planning protocol.\n\n"
BUGREPORT_PROMPT_PREFIX = (
    "Convert the following raw accessibility finding(s) into bug report(s) ready to file "
    "as GitHub Issue(s), following the bug-reporting skill exactly. Apply every rule "
    "applicable to the input (deduplication/aggregation, both XPath forms, stable "
    "identifiers, severity, frequency, WCAG SC, rule IDs, environment, impact, suggested "
    "fix, steps to reproduce). Where the input genuinely lacks a value, follow the "
    "skill's guidance on absent data instead of inventing one. Return only the finished "
    "report(s) in the skill's Markdown template.\n\n"
)

PLANNER_FIXTURES = [
    "aria-combobox-autocomplete",
    "aria-data-table-sorting",
    "aria-disclosure-widget",
    "aria-modal-form-validation",
    "aria-tab-dynamic-content",
    "keyboard-breadcrumb",
    "keyboard-button-bar",
    "keyboard-menu-dropdown",
    "keyboard-modal-focus-trap",
    "keyboard-roving-tabindex",
    "sr-article-page",
    "sr-form-field-help",
    "sr-notification-system",
    "sr-product-listing",
    "sr-search-results-live",
    "test-data-table",
    "test-federal-agency-audit",  # 27th fixture, de-hinted declared-508 (ICT baseline Phase 3 step 10, 2026-08-12) — no model rows yet
    "test-form",
    "test-hybrid-product-audit",  # 26th fixture, de-hinted (step 11a, 2026-08-01) — no model rows yet
    "test-modal",
    "test-multi-page-audit",
    "test-remediation-mode",  # 29th fixture, de-hinted remediation-scope (Tier-2, 2026-09-01) — no model rows yet
    "test-simple-button",
    "test-standards-subscription-audit",  # 28th fixture, de-hinted WCAG 2.4.5 audit-scope probe (2026-08-14) — no model rows yet
    "visual-animated-transition",
    "visual-dark-mode",
    "visual-data-viz",
    "visual-form-validation",
    "visual-status-colors",
]

PERSPECTIVE_PILOT_FIXTURES = [
    "animated-onboarding-flow",
    "checkout-form-broken-errors",
    "color-only-status-indicators",
    "modal-broken-focus-trap",
    "dense-admin-jargon",
    "login-form-clean",
    "article-page-clean",
]

ALL_PERSPECTIVE_FIXTURES = [
    "animated-onboarding-flow",
    "article-page-clean",
    "autocomplete-fast-timeout",
    "chat-cognitive-load",
    "checkout-form-broken-errors",
    "color-only-status-indicators",
    "custom-select-combobox",
    "dashboard-text-labels",
    "data-table-sortable-columns",
    "data-viz-color-encoding",
    "dense-admin-jargon",
    "hover-reveal-navigation",
    "image-gallery-small-targets",
    "infinite-scroll-cognitive",
    "login-form-clean",
    "map-interface-zoom",
    "media-player-captions",
    "modal-broken-focus-trap",
    "multi-column-pricing",
    "nav-menu-landmarks",
    "podcast-audio-only",
    "product-carousel-autoplay",
    "search-results-dynamic-update",
    "tab-panel-arrow-keys",
    "video-tutorial-no-captions",
]

# 127.0.0.1, not localhost: on dual-stack macOS, localhost resolves ::1
# first, where the CPU-only OrbStack container may listen with a different
# model store — a model missing there 404s even though `ollama list` (native
# Metal server on IPv4) shows it. Matches ollama_a11y.py's default.
# (2026-08-01: the evalreport first-rows run hit exactly this.)
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
# F13: same host, /api/tags instead of /api/generate — fetch_declared_context_length's target.
OLLAMA_TAGS_URL = os.environ.get("OLLAMA_TAGS_URL", "http://127.0.0.1:11434/api/tags")

OLLAMA_MODELS = ["llama3.3:70b", "qwen3:32b", "deepseek-r1:70b", "qwen3.5:27b"]
SMALL_MODELS = ["qwen3.5:latest"]  # 6.6 GB — test as lightweight tier
HAS_BUGS_FIXTURES = [
    "form-validation-missing-aria-describedby",
    "tabs-missing-arrow-nav",
    "toast-notification-no-role",
    "accordion-no-region-role",
    "breadcrumb-navigation-no-nav-landmark",
    "checkbox-group-no-fieldset",
    "combobox-autocomplete-no-listbox-role",
    "data-table-missing-scope",
    "expandable-section-no-button",
    "file-input-no-labels",
    "heading-hierarchy-skipped",
    "image-carousel-no-region",
    "infinite-scroll-no-announcement",
    "interactive-dropdown-focus-bug",
    "loading-state-missing-aria-busy",
    "megamenu-no-structure",
    "pagination-no-nav-landmark",
    "popover-no-focus-management",
    "radio-button-group-no-grouping",
    "tooltip-no-role-no-association",
    "video-player-missing-captions",
    # Remediated-code-with-residue / weak-class shapes (2026-08-14):
    "rehearsal-schedule-panel",
    "seed-availability-panel",
    "slip-reservation-tabs",
    "filing-progress-controls",
    "tool-catalog-layout",
    "garden-plot-directory",
    # GT-07 (PT-16) async failure/recovery status messages (2026-09-03):
    "async-retry-error-unannounced",
    # GT-09 pseudo-href controls are F42 role defects, not 3.2.4 (2026-09-03):
    "pseudo-link-map-controls",
    # GT-11 paired id/name columns are not a 3.2.4 case (2026-09-03):
    "row-action-inconsistent-labels",
    # GT-05 (PT-14) SPA route-change focus + title (2026-09-03):
    "spa-route-change-unannounced",
]
CLEAN_FIXTURES = [
    "button-skip-link-clean",
    "interactive-dropdown-clean",
    "modal-complete-clean",
    "search-results-dynamic-clean",
    "trail-conditions-filter",
    "pool-lesson-registration",
    "composite-descendant-clean",  # Tier-2 R-29 (L-017), no model rows yet
    "async-retry-recovery-clean",  # GT-07 (PT-16) pair member, no model rows yet
    "map-controls-clean",  # GT-09 pair member, no model rows yet
    "paired-id-name-columns-clean",  # GT-11 pair member, no model rows yet
    "spa-route-change-clean",  # GT-05 (PT-14) pair member, no model rows yet
]
FLAWED_FIXTURES = [
    "tabs-incomplete-aria-selected",
    "multistep-form-error-clearing",
    "dashboard-heading-inconsistency",
    "app-focus-order-illogical",
    "async-form-vague-success",
]
ADVERSARIAL_FIXTURES = [
    "tabbed-nav-vs-tab-pattern",
    "form-field-vs-summary-errors",
    "search-focus-stays-in-input",
]
ALL_CRITIC_FIXTURES = CLEAN_FIXTURES + HAS_BUGS_FIXTURES + FLAWED_FIXTURES + ADVERSARIAL_FIXTURES
ALREADY_BENCHMARKED = {
    "qwen3:32b": set(HAS_BUGS_FIXTURES[:3] + CLEAN_FIXTURES),
    "llama3.3:70b": set(HAS_BUGS_FIXTURES[:3] + CLEAN_FIXTURES),
    "qwen3.5:latest": set(HAS_BUGS_FIXTURES[:3] + CLEAN_FIXTURES),
}


import re as _re


def make_model_tag(model):
    """qwen3:32b -> qwen3-32b ; deepseek-r1:70b -> deepseek-r1-70b (dots dropped)."""
    return model.replace(":", "-").replace(".", "")


def validate_fixture_id(fixture_id):
    """Exit with error if fixture_id is not safe kebab-case."""
    if not _re.fullmatch(r"[a-z0-9][a-z0-9-]*", fixture_id):
        sys.exit(f"Invalid fixture id: {fixture_id!r} (expected kebab-case)")


def write_json_atomic(path, data):
    """Write JSON to path atomically via a .tmp sibling (safe under Ctrl-C)."""
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


def write_overflow_row(out_path, model, fixture_id, estimated, num_ctx, skill, condition=None,
                        declared_context_length=None):
    """Context-overflow guard (Phase 0.2/0.3): the client-side estimate says
    this prompt will not fit num_ctx + RESPONSE_RESERVE. Skip the API call —
    do not send a prompt already known to be silently front-truncated (F7) —
    and write an INVALID row instead. The filename carries an -INVALID suffix
    so score-all/score-perspective globs (which match "*-response.json"
    exactly) never pick it up; the various *-remaining commands correctly
    keep treating the fixture as not-yet-benchmarked.

    declared_context_length (F13, optional): the model's real ceiling from
    fetch_declared_context_length, recorded so a row that overflowed because
    Ollama would have clamped below the requested num_ctx is distinguishable
    from one that overflowed on the requested value alone."""
    invalid_path = out_path[: -len(".json")] + "-INVALID.json" if out_path.endswith(".json") else out_path + "-INVALID.json"
    row = {
        "invalid": "context_overflow",
        "estimated_prompt_tokens": estimated,
        "num_ctx": num_ctx,
        "declared_context_length": declared_context_length,
        "response_reserve": RESPONSE_RESERVE,
        "_benchmark": {
            "model": model,
            "fixture_id": fixture_id,
            "skill": skill,
            "condition": condition,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        },
    }
    write_json_atomic(invalid_path, row)
    effective_ctx = num_ctx if declared_context_length is None else min(num_ctx, declared_context_length)
    banner = (
        "\n" + "!" * 60 + "\n"
        "CONTEXT OVERFLOW — generation SKIPPED, not sent to the API\n"
        f"  Model:      {model}\n"
        f"  Fixture:    {fixture_id}\n"
        f"  Estimated:  {estimated} prompt tokens\n"
        f"  num_ctx:    {num_ctx} (declared_context_length={declared_context_length}, "
        f"effective ceiling={effective_ctx})\n"
        f"  Reserve:    {RESPONSE_RESERVE}\n"
        f"  Shortfall:  {estimated + RESPONSE_RESERVE - effective_ctx} tokens over budget\n"
        f"  Row:        {invalid_path}\n"
        "  This fixture FAILS for this model/lane. Raise num_ctx or curate\n"
        "  the input. Batch continues.\n"
        + "!" * 60
    )
    print(banner, file=sys.stderr)
    return invalid_path


def flag_context_pressure(prompt_eval_count, num_ctx):
    """Post-run corroboration (Phase 0.2/0.3): True when the API's own count
    confirms the prompt landed within RESPONSE_RESERVE tokens of num_ctx —
    the row stays valid but is flagged so BENCHMARK.md can note reduced
    generation headroom. Returns False (cannot confirm) when the API didn't
    report prompt_eval_count.

    KNOWN GAP, not fixed here (F13 fast-follow residual — filed as
    github.com/zivtech/accessibility-skills issue #28, fix deferred per the
    gate's own condition): compares against the REQUESTED num_ctx, never
    the F13-clamped effective ceiling (min(num_ctx, declared_context_length)),
    so it under-reports pressure whenever declared_context_length < num_ctx
    — see issue #28 before trusting a False here as "no pressure" on a row
    the server may have actually clamped."""
    if prompt_eval_count is None:
        return False
    pressure = prompt_eval_count >= num_ctx - RESPONSE_RESERVE
    if pressure:
        print(
            f"\nWARNING: context_pressure — prompt_eval_count={prompt_eval_count} "
            f">= num_ctx({num_ctx}) - RESPONSE_RESERVE({RESPONSE_RESERVE}). "
            "Row is valid but ran with reduced response headroom.",
            file=sys.stderr,
        )
    return pressure


def strip_frontmatter(content):
    if content.startswith("---"):
        end = content.index("---", 3)
        return content[end + 3:].strip()
    return content


def load_system_prompt():
    with open(SKILL_PATH) as f:
        return strip_frontmatter(f.read())


def load_perspective_system_prompt():
    with open(PERSPECTIVE_SKILL_PATH) as f:
        content = strip_frontmatter(f.read())
    for ref_path in PERSPECTIVE_REFS:
        if os.path.exists(ref_path):
            with open(ref_path) as f:
                content += "\n\n---\n\n" + f.read()
    return content


ANSWER_KEY_RE = re.compile(r"^## Accessibility Issues.*$", re.MULTILINE)


def strip_answer_key(content):
    """Blind protocol (post-003, 2026-07-13): fixture files embed their expected
    findings under an '## Accessibility Issues…' heading. Withhold that heading
    and everything after it from model prompts — every lane before this date ran
    non-blind. Fixtures without the heading pass through unchanged."""
    blind = ANSWER_KEY_RE.split(content, maxsplit=1)[0].rstrip() + "\n"
    assert "Planted Bugs" not in blind, "answer-key marker survived stripping"
    return blind


def load_fixture(fixture_id, fixtures_dir=None):
    d = fixtures_dir or FIXTURES_DIR
    path = os.path.join(d, f"{fixture_id}.md")
    with open(path) as f:
        return strip_answer_key(f.read())


def build_escalation_prompt(fixture_id):
    """Build perspective-audit user prompt with escalation list from fixture metadata."""
    import yaml
    metadata_path = os.path.join(PERSPECTIVE_FIXTURES_DIR, f"{fixture_id}.metadata.yaml")
    with open(metadata_path) as f:
        meta = yaml.safe_load(f)

    alarm_levels = meta.get("expected_alarm_levels", {})
    escalated = [
        f"- {name.replace('_', ' ').title()}: {level}"
        for name, level in alarm_levels.items()
        if level in ("MEDIUM", "HIGH")
    ]

    fixture_content = load_fixture(fixture_id, PERSPECTIVE_FIXTURES_DIR)

    if escalated:
        escalation_block = "## Escalated Perspectives (from a11y-critic)\n\n" + "\n".join(escalated)
    else:
        escalation_block = "## Escalated Perspectives\n\nAll perspectives at LOW — this is a CLEAN baseline. Produce PASS verdict with no CRITICAL/MAJOR findings."

    return (
        "Run the perspective audit on the following component. "
        "The escalated perspectives are listed below.\n\n"
        f"{escalation_block}\n\n"
        f"## Component Under Review\n\n{fixture_content}"
    )


CRITIC_CTX = {
    # qwen3.6 (thinking-by-default): critic protocol alone measured at 14,276
    # tokens for qwen3.6:35b / 13,853 for qwen3:32b (num_predict=1 probes,
    # 2026-08-25 — supersedes the earlier 16,157 estimate cited here) — at
    # 16384 generation hits done_reason=length inside the thinking stream and
    # the scored response comes back empty.
    "qwen3.6:27b": 32768,
    "qwen3.6:35b": 32768,
    # gemma4 tokenizer: critic prompt alone measures 16,477 tokens (num_predict=1
    # probe, 2026-07-28) — exceeds the 16384 default before generation starts.
    "gemma4:31b": 32768,
    "gemma4:26b": 32768,
    # New-model default: every current-gen tokenizer measured puts the critic
    # prompt at >=16.1K, so new candidates start at 32768 (probe confirms at audit).
    "laguna-s-2.1:q4_k_m": 32768,
    "laguna-xs-2.1": 32768,
    "gpt-oss:120b": 32768,
    "ornith:35b": 32768,
    # qwen3.8 (thinking-by-default, same lineage/tokenizer class as qwen3.6;
    # num_predict=1 probe recorded in the 2026-08 funnel README).
    "qwen3.8:27b": 32768,
    # added 2026-08-24 per context-utilization plan Phase 0.2; historical rows
    # at 16,384 under retro-probe (Phase 0.4). qwen3:32b was the standing
    # fallback baseline with NO entry here — it silently ran the critic suite
    # at CRITIC_CTX_DEFAULT (16384) even though every measured current-gen
    # tokenizer above puts the critic prompt alone at >=16.1K (plan F7).
    "qwen3:32b": 32768,
}
# R5.4 (2026-08-27, R5 decision memo §3): raised 16384 -> 32768.
# At 16,384 the budget is 8,192 and all 41 critic fixtures estimate
# 17,650-19,906 -> 41/41 refuse. An unmapped model got a hard stop, never a run.
# Probe receipt: evals/results/context-utilization-r5/num-ctx-probe-receipts.md
# (num_predict=1 against the assembled production prompt, per model x suite).
# A _DEFAULT is a starting guess for a model that does not exist yet; the
# client-side guard, not this integer, is the safety property (memo §8).
CRITIC_CTX_DEFAULT = 32768


def run_ollama(model, fixture_id, system_prompt, content_override=None,
               out_path_override=None, extra_meta=None):
    fixture_content = content_override or load_fixture(fixture_id)
    prompt = PROMPT_PREFIX + fixture_content
    num_ctx = ctx_for(model, CRITIC_CTX, CRITIC_CTX_DEFAULT)
    declared_context_length = fetch_declared_context_length(model)  # F13

    model_tag = make_model_tag(model)
    out_path = out_path_override or os.path.join(
        RESULTS_DIR, f"ollama-bench-{fixture_id}-{model_tag}-response.json"
    )

    overflow, estimated = context_overflow(system_prompt, prompt, num_ctx, declared_context_length)
    if overflow:
        return write_overflow_row(out_path, model, fixture_id, estimated, num_ctx, skill="a11y-critic",
                                   declared_context_length=declared_context_length)

    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": prompt,
        "stream": True,
        "options": {"num_ctx": num_ctx, "temperature": 0.3},
    }

    print(f"\n{'='*60}")
    print(f"Model: {model} | Fixture: {fixture_id}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")
    print(f"Prompt: {len(system_prompt) + len(prompt)} chars (~{estimated} est. tokens) | num_ctx: {num_ctx}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    response_text = ""
    thinking_chars = 0  # separate reasoning channel (qwen3.6+/gemma4 on ollama >=0.31)
    final_chunk = {}
    with urllib.request.urlopen(req, timeout=300) as resp:
        for line in resp:
            chunk = json.loads(line)
            if chunk.get("response"):
                response_text += chunk["response"]
            if chunk.get("thinking"):
                thinking_chars += len(chunk["thinking"])
            if chunk.get("done"):
                final_chunk = chunk
                break

    elapsed = time.time() - start
    prompt_eval_count = final_chunk.get("prompt_eval_count")
    data = {
        "response": response_text,
        "done": True,
        "total_duration": final_chunk.get("total_duration"),
        "eval_count": final_chunk.get("eval_count"),
        "_benchmark": {
            "model": model,
            "fixture_id": fixture_id,
            "elapsed_seconds": round(elapsed, 1),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            # Hardening (2026-08-23): a thinking model that clips at num_ctx
            # returns done_reason=length with an empty scored response —
            # without these two fields the artifact is indistinguishable
            # from a genuine empty answer (July funnel, finding 2).
            "done_reason": final_chunk.get("done_reason"),
            "thinking_chars": thinking_chars,
            # Context-overflow guard corroboration (Phase 0.2/0.3, 2026-08-24):
            # the client-side estimate is the primary gate (already passed,
            # or this function would have returned above); prompt_eval_count
            # is the API's own count, recorded here for corroboration only.
            "estimated_prompt_tokens": estimated,
            "prompt_eval_count": prompt_eval_count,
            "context_pressure": flag_context_pressure(prompt_eval_count, num_ctx),
            # R5.1 (2026-08-27): the window the row actually ran at. Without it
            # no row is attributable to a num_ctx era after a default is raised
            # (R5 decision memo §5.1). Requested value, not the clamped ceiling —
            # declared_context_length below carries what the server would allow.
            "num_ctx": num_ctx,
            "declared_context_length": declared_context_length,  # F13
        },
    }
    if extra_meta:
        data["_benchmark"].update(extra_meta)

    write_json_atomic(out_path, data)

    resp_len = len(response_text)
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path



# ---------------------------------------------------------------------------
# Title-hint measurement lane (issue #51 step 2, 2026-09-03).
#
# Line 1 of every fixture is above the blind cut line, so the H1 reaches the
# model in every prompt-based lane, and 52 of 77 corpus titles name the defect
# they plant. This lane draws the same fixture under its real title and under
# the neutralised title declared in evals/fixture-title-manifest.yaml, so the
# question "how much of our must-find rate is the title?" gets a number
# instead of an argument. Nothing else about the prompt differs — the swap is
# a single line, verified byte-for-byte by tools/diff below the H1.
#
# The neutralised title is NOT proposed as the corpus default here. This lane
# measures whether adopting it would be worth the re-draw it costs.
# ---------------------------------------------------------------------------

TITLE_MANIFEST_PATH = os.path.join(
    BASE_DIR, "..", "evals", "fixture-title-manifest.yaml"
)


def load_title_manifest():
    import yaml

    with open(TITLE_MANIFEST_PATH) as f:
        return yaml.safe_load(f)["suites"]


def load_fixture_titled(fixture_id, condition, suite="a11y-critic", fixtures_dir=None):
    """Blind fixture content with the H1 either left alone ('titled') or
    replaced by the manifest's neutral_title ('neutral')."""
    content = load_fixture(fixture_id, fixtures_dir or FIXTURES_DIR)
    row = load_title_manifest()[suite]["fixtures"][fixture_id]
    lines = content.split("\n")
    if lines[0] != "# " + row["title"]:
        sys.exit(
            f"load_fixture_titled: {fixture_id} H1 {lines[0]!r} does not match the "
            f"manifest; run ollama/test_blind_prompts.py"
        )
    if condition == "titled":
        return content
    if condition != "neutral":
        sys.exit(f"load_fixture_titled: unknown condition {condition!r}")
    neutral = row.get("neutral_title")
    if not neutral:
        sys.exit(
            f"load_fixture_titled: {fixture_id} is class {row['class']!r} with no "
            f"neutral_title — nothing to neutralise"
        )
    lines[0] = "# " + neutral
    return "\n".join(lines)


def run_titlehint(model, fixture_id, condition, draw, system_prompt):
    content = load_fixture_titled(fixture_id, condition)
    model_tag = make_model_tag(model)
    out_path = os.path.join(
        RESULTS_DIR,
        f"ollama-titlehint-{condition}-{fixture_id}-{model_tag}-d{draw}-response.json",
    )
    print(f"\nTITLE-HINT ({condition}, draw {draw}) | {model} | {fixture_id}")
    print(f"  H1: {content.splitlines()[0]}")
    return run_ollama(
        model, fixture_id, system_prompt,
        content_override=content, out_path_override=out_path,
        extra_meta={"lane": "titlehint", "condition": condition, "draw": draw},
    )



# ---------------------------------------------------------------------------
# Features-section measurement lane (issue #51 leak class 2, 2026-09-03).
#
# 45 of 50 critic fixtures show the model an `## Accessibility Features
# Present` section above the blind cut line. The title names the defect; this
# names the non-defects. Together they bracket the answer.
#
# Issue #51 argues those items are the scored false_positive_trap entries, so
# the trap dimension measures "don't flag what you were told is fine" rather
# than "don't flag correct code". Measured 2026-09-03: `false_positive_trap`
# is declared in all 50 rubrics and read by no scorer — as are `llm_judge`,
# `hybrid_weights` and `scoring_method`. There is no trap metric. So this lane
# measures the consequence directly instead: on the 11 CLEAN fixtures, whose
# expected verdict is ACCEPT, does removing the features section flip the
# verdict or raise spurious findings? That is the "don't flag correct code"
# claim the CLEAN halves exist to establish, stated as something scorable.
#
# The section is realistic content — a developer handing over a component
# really would say what they handled. This lane measures what it is worth,
# not whether it is plausible.
# ---------------------------------------------------------------------------

FEATURES_SECTION_RE = re.compile(
    r"^## Accessibility Features (?:Present|Implemented)[ \t]*$.*?(?=^## |\Z)",
    re.MULTILINE | re.DOTALL,
)


def load_fixture_features(fixture_id, condition, fixtures_dir=None):
    """Blind fixture content with the features section kept ('withfeatures')
    or removed ('nofeatures'). Nothing else differs."""
    content = load_fixture(fixture_id, fixtures_dir or FIXTURES_DIR)
    if condition == "withfeatures":
        return content
    if condition != "nofeatures":
        sys.exit(f"load_fixture_features: unknown condition {condition!r}")
    stripped, n = FEATURES_SECTION_RE.subn("", content)
    if n != 1:
        sys.exit(
            f"load_fixture_features: {fixture_id} has {n} features sections, "
            f"expected exactly 1 — nothing to remove"
        )
    return re.sub(r"\n{3,}", "\n\n", stripped).rstrip() + "\n"


def run_featurehint(model, fixture_id, condition, draw, system_prompt):
    content = load_fixture_features(fixture_id, condition)
    model_tag = make_model_tag(model)
    out_path = os.path.join(
        RESULTS_DIR,
        f"ollama-featurehint-{condition}-{fixture_id}-{model_tag}-d{draw}-response.json",
    )
    print(f"\nFEATURE-HINT ({condition}, draw {draw}) | {model} | {fixture_id}")
    print(f"  prompt chars: {len(content)}")
    return run_ollama(
        model, fixture_id, system_prompt,
        content_override=content, out_path_override=out_path,
        extra_meta={"lane": "featurehint", "condition": condition, "draw": draw},
    )


def load_planner_system_prompt():
    with open(PLANNER_SKILL_PATH) as f:
        return strip_frontmatter(f.read())


def load_planner_federal_system_prompt():
    """Planner protocol + the a11y-test crosswalk supplied in-prompt (the
    declared-508 condition). The FEDERAL PROFILE tells the planner to source
    its coverage statement from the crosswalk; a local model cannot read repo
    files, so the condition supplies it — the report-contract-as-system-prompt
    precedent from the evaluation-report lane."""
    with open(CROSSWALK_PATH) as f:
        crosswalk = f.read()
    return (
        load_planner_system_prompt()
        + "\n\n---\n\nSupplied reference for declared-508 engagements — the "
        "a11y-test ICT Testing Baseline coverage crosswalk "
        "(references/ict-baseline-crosswalk.yaml in the a11y-test skill):\n\n"
        "```yaml\n" + crosswalk + "\n```\n"
    )


# NUM_CTX MAP HYGIENE (context-utilization plan Phase 0.2, 2026-08-24): lifted
# from a hardcoded 32768 literal that applied identically to every model in
# both the "planner" and "planner-federal" conditions. Empty map + a default
# equal to the old literal preserves that exact behavior for every model.
PLANNER_CTX = {}
# R5.4 (2026-08-27, R5 decision memo §3): raised 32768 -> 40960.
# At 32,768 the budget is 24,576 and the plain-planner fixtures estimate
# 23,974-25,709 -> 19/28 refuse, the 9 that clear do so by <=603 tokens; the
# planner-federal condition (crosswalk appended to the system prompt, est
# 30,274-32,009) refuses 28/28. R5.3 measured the output side on 57 committed
# local rows: 3 are clipped (done_reason=length, pec+eval_count = 32,768
# exactly, all three end mid-sentence) and 0/57 would clip at 40,960.
# CAUTION (R5.2): 40,960 clears planner-federal by only 759 ESTIMATED tokens
# (max est 32,009 + 8,192 reserve = 40,201), i.e. ~2,657 chars of protocol
# growth. a11y-planner/SKILL.md grew 11,132 chars in the six weeks to
# 2026-08-25. qwen3:32b's declared ceiling IS 40,960, so for that model there
# is no larger legal value -- the next raise is not available. Watch this.
# Probe receipt: evals/results/context-utilization-r5/num-ctx-probe-receipts.md
# (num_predict=1 against the assembled production prompt, per model x suite).
# A _DEFAULT is a starting guess for a model that does not exist yet; the
# client-side guard, not this integer, is the safety property (memo §8).
PLANNER_CTX_DEFAULT = 40960
PLANNER_FEDERAL_CTX = {}
# The planner-federal condition appends the ICT baseline crosswalk to the
# planner protocol, so its system prompt is far larger than the plain lane's.
# Measured 2026-09-04 while integrating the context-utilization guard: the
# largest federal prompt estimates 33,240 tokens, which with the 8,192
# reserve overruns the 40,960 planner default -- five fixtures would have
# been refused by the guard rather than drawn. Raised for this condition
# only; the plain planner lane keeps its probed default. Per-model declared
# limits are still enforced by the F13 declared-context check.
PLANNER_FEDERAL_CTX_DEFAULT = 49152


def run_planner(model, fixture_id, system_prompt, condition="planner"):
    fixture_content = load_fixture(fixture_id, PLANNER_FIXTURES_DIR)
    prompt = PLANNER_PROMPT_PREFIX + fixture_content
    if condition == "planner-federal":
        num_ctx = ctx_for(model, PLANNER_FEDERAL_CTX, PLANNER_FEDERAL_CTX_DEFAULT)
    else:
        num_ctx = ctx_for(model, PLANNER_CTX, PLANNER_CTX_DEFAULT)
    declared_context_length = fetch_declared_context_length(model)  # F13

    model_tag = make_model_tag(model)
    file_prefix = "ollama-planner-federal" if condition == "planner-federal" else "ollama-planner"
    out_path = os.path.join(RESULTS_DIR, f"{file_prefix}-{fixture_id}-{model_tag}-response.json")

    overflow, estimated = context_overflow(system_prompt, prompt, num_ctx, declared_context_length)
    if overflow:
        return write_overflow_row(
            out_path, model, fixture_id, estimated, num_ctx, skill="a11y-planner", condition=condition,
            declared_context_length=declared_context_length,
        )

    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": num_ctx, "temperature": 0.3},
    }

    print(f"\n{'='*60}")
    print(f"PLANNER | Model: {model} | Fixture: {fixture_id} | Condition: {condition}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")
    print(f"Prompt: {len(system_prompt) + len(prompt)} chars (~{estimated} est. tokens) | num_ctx: {num_ctx}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1200) as resp:
        data = json.loads(resp.read())

    elapsed = time.time() - start
    prompt_eval_count = data.get("prompt_eval_count")
    data["_benchmark"] = {
        "model": model,
        "fixture_id": fixture_id,
        "skill": "a11y-planner",
        "condition": condition,
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "estimated_prompt_tokens": estimated,
        "prompt_eval_count": prompt_eval_count,
        "context_pressure": flag_context_pressure(prompt_eval_count, num_ctx),
        # R5.1 (2026-08-27): the window the row actually ran at. Without it
        # no row is attributable to a num_ctx era after a default is raised
        # (R5 decision memo §5.1). Requested value, not the clamped ceiling —
        # declared_context_length below carries what the server would allow.
        "num_ctx": num_ctx,
        "declared_context_length": declared_context_length,  # F13
    }

    write_json_atomic(out_path, data)

    resp_len = len(data.get("response", ""))
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path


# NUM_CTX MAP HYGIENE (context-utilization plan Phase 0.2, 2026-08-24): lifted
# from a hardcoded 16384 literal that applied identically to every model.
# Empty map + a default equal to the old literal preserves that exact
# behavior for every model.
BUGREPORT_CTX = {}
CJ_CTX = {}
OPEVIDENCE_CTX = {}
RECIPE_CTX = {}
# Lanes added on main after the Phase 0.2-0.3 guard shipped, wired into it
# 2026-09-04 when the context-utilization branch was integrated. Empty map +
# a default equal to each lane's previous literal preserves the exact
# behaviour every existing row was drawn under; only the guard is new.
CJ_CTX_DEFAULT = 40960
OPEVIDENCE_CTX_DEFAULT = 16384
RECIPE_CTX_DEFAULT = 24576
# R5.4 (2026-08-27, R5 decision memo §3): raised 16384 -> 32768.
# At 16,384 the budget is 8,192 and the bug-reporting SKILL.md system prompt
# ALONE estimates 8,518 -- over budget before any fixture is appended. 7/7
# refuse; no local bug-report row could run at all.
# Probe receipt: evals/results/context-utilization-r5/num-ctx-probe-receipts.md
# (num_predict=1 against the assembled production prompt, per model x suite).
# A _DEFAULT is a starting guess for a model that does not exist yet; the
# client-side guard, not this integer, is the safety property (memo §8).
BUGREPORT_CTX_DEFAULT = 32768


def run_bugreport(model, fixture_id, system_prompt):
    fixture_content = load_fixture(fixture_id, BUGREPORT_FIXTURES_DIR)
    prompt = BUGREPORT_PROMPT_PREFIX + fixture_content
    num_ctx = ctx_for(model, BUGREPORT_CTX, BUGREPORT_CTX_DEFAULT)
    declared_context_length = fetch_declared_context_length(model)  # F13

    model_tag = make_model_tag(model)
    out_path = os.path.join(RESULTS_DIR, f"ollama-bugreport-{fixture_id}-{model_tag}-response.json")

    overflow, estimated = context_overflow(system_prompt, prompt, num_ctx, declared_context_length)
    if overflow:
        return write_overflow_row(out_path, model, fixture_id, estimated, num_ctx, skill="bug-reporting",
                                   declared_context_length=declared_context_length)

    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": num_ctx, "temperature": 0.3},
    }

    print(f"\n{'='*60}")
    print(f"BUGREPORT | Model: {model} | Fixture: {fixture_id}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")
    print(f"Prompt: {len(system_prompt) + len(prompt)} chars (~{estimated} est. tokens) | num_ctx: {num_ctx}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1200) as resp:
        data = json.loads(resp.read())

    elapsed = time.time() - start
    prompt_eval_count = data.get("prompt_eval_count")
    data["_benchmark"] = {
        "model": model,
        "fixture_id": fixture_id,
        "skill": "bug-reporting",
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "estimated_prompt_tokens": estimated,
        "prompt_eval_count": prompt_eval_count,
        "context_pressure": flag_context_pressure(prompt_eval_count, num_ctx),
        # R5.1 (2026-08-27): the window the row actually ran at. Without it
        # no row is attributable to a num_ctx era after a default is raised
        # (R5 decision memo §5.1). Requested value, not the clamped ceiling —
        # declared_context_length below carries what the server would allow.
        "num_ctx": num_ctx,
        "declared_context_length": declared_context_length,  # F13
    }

    write_json_atomic(out_path, data)

    resp_len = len(data.get("response", ""))
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path


# NUM_CTX MAP HYGIENE (context-utilization plan Phase 0.2, 2026-08-24): lifted
# from a hardcoded 32768 literal that applied identically to every model in
# both the "contract" and "baseline" conditions. Empty map + a default equal
# to the old literal preserves that exact behavior for every model.
EVALREPORT_CTX = {}
EVALREPORT_CTX_DEFAULT = 32768


def run_evalreport(model, fixture_id, system_prompt, condition="contract"):
    """Evaluation-report lane. condition="baseline" runs the identical fixture
    with no system prompt to measure what the contract carries; its output file
    gets a distinct prefix so the -remaining glob never counts it as a
    contract-condition run."""
    prompt = load_fixture(fixture_id, EVALREPORT_FIXTURES_DIR)
    num_ctx = ctx_for(model, EVALREPORT_CTX, EVALREPORT_CTX_DEFAULT)
    declared_context_length = fetch_declared_context_length(model)  # F13

    file_prefix = "ollama-evalreport" if condition == "contract" else "ollama-evalreport-baseline"
    model_tag = make_model_tag(model)
    out_path = os.path.join(RESULTS_DIR, f"{file_prefix}-{fixture_id}-{model_tag}-response.json")

    overflow, estimated = context_overflow(system_prompt, prompt, num_ctx, declared_context_length)
    if overflow:
        return write_overflow_row(
            out_path, model, fixture_id, estimated, num_ctx, skill="evaluation-report", condition=condition,
            declared_context_length=declared_context_length,
        )

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        # 32k flat: contract + evidence package + a full report is the longest
        # input/output pair in the benchmark, and thinking-by-default models
        # share the window with reasoning tokens.
        "options": {"num_ctx": num_ctx, "temperature": 0.3},
    }
    if system_prompt:
        payload["system"] = system_prompt

    print(f"\n{'='*60}")
    print(f"EVALREPORT ({condition}) | Model: {model} | Fixture: {fixture_id}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")
    print(f"Prompt: {len(system_prompt or '') + len(prompt)} chars (~{estimated} est. tokens) | num_ctx: {num_ctx}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1200) as resp:
        data = json.loads(resp.read())

    elapsed = time.time() - start
    prompt_eval_count = data.get("prompt_eval_count")
    data["_benchmark"] = {
        "model": model,
        "fixture_id": fixture_id,
        "skill": "evaluation-report",
        "condition": condition,
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "estimated_prompt_tokens": estimated,
        "prompt_eval_count": prompt_eval_count,
        "context_pressure": flag_context_pressure(prompt_eval_count, num_ctx),
        # R5.1 (2026-08-27): the window the row actually ran at. Without it
        # no row is attributable to a num_ctx era after a default is raised
        # (R5 decision memo §5.1). Requested value, not the clamped ceiling —
        # declared_context_length below carries what the server would allow.
        "num_ctx": num_ctx,
        "declared_context_length": declared_context_length,  # F13
    }

    write_json_atomic(out_path, data)

    resp_len = len(data.get("response", ""))
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path


def load_evalreport_contract():
    with open(EVALREPORT_CONTRACT_PATH) as f:
        return f.read()


# NUM_CTX MAP HYGIENE (context-utilization plan Phase 0.2, 2026-08-24): lifted
# from a hardcoded 40960 literal that applied identically to every model in
# both the "acr" and "baseline" conditions. Empty map + a default equal to
# the old literal preserves that exact behavior for every model.
ACR_CTX = {}
ACR_CTX_DEFAULT = 40960


def run_acr(model, fixture_id, system_prompt, condition="acr"):
    """ACR-reporting lane. condition="baseline" runs the identical fixture
    with no system prompt to measure what the skill carries; its output file
    gets a distinct prefix so skill-condition globs never count it."""
    prompt = load_fixture(fixture_id, ACR_FIXTURES_DIR)
    num_ctx = ctx_for(model, ACR_CTX, ACR_CTX_DEFAULT)
    declared_context_length = fetch_declared_context_length(model)  # F13

    file_prefix = "ollama-acr" if condition == "acr" else "ollama-acr-baseline"
    model_tag = make_model_tag(model)
    out_path = os.path.join(RESULTS_DIR, f"{file_prefix}-{fixture_id}-{model_tag}-response.json")

    overflow, estimated = context_overflow(system_prompt, prompt, num_ctx, declared_context_length)
    if overflow:
        return write_overflow_row(
            out_path, model, fixture_id, estimated, num_ctx, skill="acr-reporting", condition=condition,
            declared_context_length=declared_context_length,
        )

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        # 40k: the longest pair in the benchmark — a ~10k-token evidence
        # bundle + the skill + a full 56-criterion YAML draft, with
        # thinking-by-default models sharing the window with reasoning.
        "options": {"num_ctx": num_ctx, "temperature": 0.3},
    }
    if system_prompt:
        payload["system"] = system_prompt

    print(f"\n{'='*60}")
    print(f"ACR ({condition}) | Model: {model} | Fixture: {fixture_id}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")
    print(f"Prompt: {len(system_prompt or '') + len(prompt)} chars (~{estimated} est. tokens) | num_ctx: {num_ctx}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1800) as resp:
        data = json.loads(resp.read())

    elapsed = time.time() - start
    prompt_eval_count = data.get("prompt_eval_count")
    data["_benchmark"] = {
        "model": model,
        "fixture_id": fixture_id,
        "skill": "acr-reporting",
        "condition": condition,
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "estimated_prompt_tokens": estimated,
        "prompt_eval_count": prompt_eval_count,
        "context_pressure": flag_context_pressure(prompt_eval_count, num_ctx),
        # R5.1 (2026-08-27): the window the row actually ran at. Without it
        # no row is attributable to a num_ctx era after a default is raised
        # (R5 decision memo §5.1). Requested value, not the clamped ceiling —
        # declared_context_length below carries what the server would allow.
        "num_ctx": num_ctx,
        "declared_context_length": declared_context_length,  # F13
    }

    write_json_atomic(out_path, data)

    resp_len = len(data.get("response", ""))
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path


def load_acr_skill():
    with open(ACR_SKILL_PATH) as f:
        return f.read()


A11Y_TEST_SKILL_PATH = os.path.join(BASE_DIR, "..", ".claude", "skills", "a11y-test", "SKILL.md")
OPEVIDENCE_START_ANCHOR = "### Operation-evidence admissibility"
OPEVIDENCE_END_ANCHOR = "### PASS partition"


def load_opevidence_system_prompt():
    """Heading-anchored slice of a11y-test SKILL.md: the operation-evidence
    admissibility rules plus the Structured disposition block contract that
    immediately follows them, stopping before the PASS-partition section
    (a related but separate concern this lane does not grade). Hard error if
    either anchor is missing — a silent empty/full-file fallback would score
    a model against the wrong instrument."""
    with open(A11Y_TEST_SKILL_PATH) as f:
        content = f.read()
    start = content.find(OPEVIDENCE_START_ANCHOR)
    if start == -1:
        sys.exit(f"load_opevidence_system_prompt: anchor not found in "
                  f"{A11Y_TEST_SKILL_PATH}: {OPEVIDENCE_START_ANCHOR!r}")
    end = content.find(OPEVIDENCE_END_ANCHOR, start)
    if end == -1:
        sys.exit(f"load_opevidence_system_prompt: anchor not found in "
                  f"{A11Y_TEST_SKILL_PATH}: {OPEVIDENCE_END_ANCHOR!r}")
    return content[start:end].strip()


def load_cj_system_prompt():
    with open(CJ_RUBRIC_PATH) as f:
        return f.read()


def run_cj(model, fixture_id, system_prompt, condition="cj"):
    """Content-judgment lane. condition="baseline" runs the identical fixture
    with no system prompt to measure what the rubric carries; its output file
    gets a distinct prefix so rubric-condition globs never count it."""
    prompt = load_fixture(fixture_id, CJ_FIXTURES_DIR)

    file_prefix = "ollama-cj" if condition == "cj" else "ollama-cj-baseline"
    model_tag = make_model_tag(model)
    out_path = os.path.join(RESULTS_DIR, f"{file_prefix}-{fixture_id}-{model_tag}-response.json")
    num_ctx = ctx_for(model, CJ_CTX, CJ_CTX_DEFAULT)
    declared_context_length = fetch_declared_context_length(model)  # F13

    overflow, estimated = context_overflow(system_prompt or "", prompt, num_ctx, declared_context_length)
    if overflow:
        return write_overflow_row(out_path, model, fixture_id, estimated, num_ctx,
                                   skill="a11y-content-judgment",
                                   declared_context_length=declared_context_length)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        # 40k: a batch of up to ~90 rows plus one JSON line per row back,
        # with thinking-by-default models sharing the window with reasoning.
        "options": {"num_ctx": num_ctx, "temperature": 0.3},
    }
    if system_prompt:
        payload["system"] = system_prompt


    print(f"\n{'='*60}")
    print(f"CJ ({condition}) | Model: {model} | Fixture: {fixture_id}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1800) as resp:
        data = json.loads(resp.read())

    elapsed = time.time() - start
    data["_benchmark"] = {
        "model": model,
        "fixture_id": fixture_id,
        "skill": "a11y-content-judgment",
        "condition": condition,
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    write_json_atomic(out_path, data)

    resp_len = len(data.get("response", ""))
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path


def run_opevidence(model, fixture_id, system_prompt, condition="opevidence"):
    """Operation-evidence admissibility lane. condition="baseline" runs the
    identical fixture with no system prompt to measure what the skill slice
    carries; its output file gets a distinct prefix so the skill-condition
    glob never counts it."""
    prompt = OPEVIDENCE_PROMPT_PREFIX + load_fixture(fixture_id, OPEVIDENCE_FIXTURES_DIR)

    file_prefix = "ollama-opevidence" if condition == "opevidence" else "ollama-opevidence-baseline"
    model_tag = make_model_tag(model)
    out_path = os.path.join(RESULTS_DIR, f"{file_prefix}-{fixture_id}-{model_tag}-response.json")
    num_ctx = ctx_for(model, OPEVIDENCE_CTX, OPEVIDENCE_CTX_DEFAULT)
    declared_context_length = fetch_declared_context_length(model)  # F13

    overflow, estimated = context_overflow(system_prompt or "", prompt, num_ctx, declared_context_length)
    if overflow:
        return write_overflow_row(out_path, model, fixture_id, estimated, num_ctx,
                                   skill="a11y-test",
                                   declared_context_length=declared_context_length)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        # 16384: the operation-evidence skill slice measures ~1.5k tokens and
        # each fixture's operation description + evidence package ~1k tokens;
        # the structured disposition block adds little more, but
        # thinking-by-default models share the window with reasoning tokens.
        "options": {"num_ctx": num_ctx, "temperature": 0.3},
    }
    if system_prompt:
        payload["system"] = system_prompt


    print(f"\n{'='*60}")
    print(f"OPEVIDENCE ({condition}) | Model: {model} | Fixture: {fixture_id}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1200) as resp:
        data = json.loads(resp.read())

    elapsed = time.time() - start
    data["_benchmark"] = {
        "model": model,
        "fixture_id": fixture_id,
        "skill": "a11y-test",
        "condition": condition,
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    write_json_atomic(out_path, data)

    resp_len = len(data.get("response", ""))
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path


def load_recipe_system_prompt():
    """Three heading-anchored slices of a11y-test SKILL.md (RECIPE_SLICES),
    joined in file order. Hard error if any anchor is missing -- a silent
    empty/full-file fallback would score a model against the wrong
    instrument."""
    with open(A11Y_TEST_SKILL_PATH) as f:
        content = f.read()
    parts = []
    for start_anchor, end_anchor in RECIPE_SLICES:
        start = content.find(start_anchor)
        if start == -1:
            sys.exit(f"load_recipe_system_prompt: anchor not found in "
                     f"{A11Y_TEST_SKILL_PATH}: {start_anchor!r}")
        end = content.find(end_anchor, start)
        if end == -1:
            sys.exit(f"load_recipe_system_prompt: anchor not found in "
                     f"{A11Y_TEST_SKILL_PATH}: {end_anchor!r}")
        parts.append(content[start:end].strip())
    return "\n\n".join(parts)


def run_recipe(model, fixture_id, system_prompt, condition="recipe"):
    """a11y-test recipe-review lane. condition="baseline" runs the identical
    fixture with no system prompt to measure what the skill slice carries;
    its output file gets a distinct prefix so the skill-condition glob never
    counts it. Scored by ollama/score_output.py against the fixture's rubric
    (verdict + must-find keywords), the same instrument as the critic lane."""
    prompt = RECIPE_PROMPT_PREFIX + load_fixture(fixture_id, RECIPE_FIXTURES_DIR)

    file_prefix = "ollama-recipe" if condition == "recipe" else "ollama-recipe-baseline"
    model_tag = make_model_tag(model)
    out_path = os.path.join(RESULTS_DIR, f"{file_prefix}-{fixture_id}-{model_tag}-response.json")
    num_ctx = ctx_for(model, RECIPE_CTX, RECIPE_CTX_DEFAULT)
    declared_context_length = fetch_declared_context_length(model)  # F13

    overflow, estimated = context_overflow(system_prompt or "", prompt, num_ctx, declared_context_length)
    if overflow:
        return write_overflow_row(out_path, model, fixture_id, estimated, num_ctx,
                                   skill="a11y-test",
                                   declared_context_length=declared_context_length)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        # 24576: the three-slice system prompt measures ~4k tokens and a
        # fixture (component + CSS + recipe + four run artifacts) ~3k;
        # thinking-by-default models share the window with reasoning tokens.
        "options": {"num_ctx": num_ctx, "temperature": 0.3},
    }
    if system_prompt:
        payload["system"] = system_prompt


    print(f"\n{'='*60}")
    print(f"RECIPE ({condition}) | Model: {model} | Fixture: {fixture_id}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1200) as resp:
        data = json.loads(resp.read())

    elapsed = time.time() - start
    data["_benchmark"] = {
        "model": model,
        "fixture_id": fixture_id,
        "skill": "a11y-test",
        "condition": condition,
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    write_json_atomic(out_path, data)

    resp_len = len(data.get("response", ""))
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path


PERSPECTIVE_CTX = {
    "qwen3:32b": 32768,
    "llama3.3:70b": 32768,
    "deepseek-r1:70b": 32768,
    "qwen3.5:27b": 32768,
    # qwen3.6: thinking-by-default — reasoning tokens share the window (2026-07-28)
    "qwen3.6:27b": 32768,
    "qwen3.6:35b": 32768,
    "qwen3.8:27b": 32768,
}
# R5.4 (2026-08-27, R5 decision memo §3): raised 16384 -> 32768.
# At 16,384 the budget is 8,192 and the perspective prompts (SKILL.md + BOTH
# reference files) estimate 7,645-10,106 -> 21/25 refuse. Every current model
# is mapped to 32,768 above, so the exposure was unmapped models only.
# NOTE (R5.2): this is the one suite where the 3.5 chars/token estimator
# UNDER-counts -- est 10,106 vs measured 10,175 (qwen3.6:35b) -- so the
# "deliberately below both measured ratios / the safe direction" claim in
# estimate_tokens() is calibrated on critic text and does not hold here.
# Probe receipt: evals/results/context-utilization-r5/num-ctx-probe-receipts.md
# (num_predict=1 against the assembled production prompt, per model x suite).
# A _DEFAULT is a starting guess for a model that does not exist yet; the
# client-side guard, not this integer, is the safety property (memo §8).
PERSPECTIVE_CTX_DEFAULT = 32768


def run_perspective(model, fixture_id, system_prompt):
    prompt = build_escalation_prompt(fixture_id)
    num_ctx = ctx_for(model, PERSPECTIVE_CTX, PERSPECTIVE_CTX_DEFAULT)
    declared_context_length = fetch_declared_context_length(model)  # F13

    model_tag = make_model_tag(model)
    out_path = os.path.join(RESULTS_DIR, f"ollama-perspective-{fixture_id}-{model_tag}-response.json")

    overflow, estimated = context_overflow(system_prompt, prompt, num_ctx, declared_context_length)
    if overflow:
        return write_overflow_row(out_path, model, fixture_id, estimated, num_ctx, skill="perspective-audit",
                                   declared_context_length=declared_context_length)

    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": prompt,
        "stream": True,
        "options": {"num_ctx": num_ctx, "temperature": 0.3},
    }

    print(f"\n{'='*60}")
    print(f"PERSPECTIVE | Model: {model} | Fixture: {fixture_id}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")
    print(f"Prompt: {len(system_prompt) + len(prompt)} chars (~{estimated} est. tokens) | num_ctx: {num_ctx}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    response_text = ""
    thinking_chars = 0  # separate reasoning channel (qwen3.6+/gemma4 on ollama >=0.31)
    final_chunk = {}
    with urllib.request.urlopen(req, timeout=300) as resp:
        for line in resp:
            chunk = json.loads(line)
            if chunk.get("response"):
                response_text += chunk["response"]
            if chunk.get("thinking"):
                thinking_chars += len(chunk["thinking"])
            if chunk.get("done"):
                final_chunk = chunk
                break

    elapsed = time.time() - start
    prompt_eval_count = final_chunk.get("prompt_eval_count")
    data = {
        "response": response_text,
        "done": True,
        "total_duration": final_chunk.get("total_duration"),
        "eval_count": final_chunk.get("eval_count"),
        "_benchmark": {
            "model": model,
            "fixture_id": fixture_id,
            "skill": "perspective-audit",
            "elapsed_seconds": round(elapsed, 1),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "done_reason": final_chunk.get("done_reason"),
            "thinking_chars": thinking_chars,
            "estimated_prompt_tokens": estimated,
            "prompt_eval_count": prompt_eval_count,
            "context_pressure": flag_context_pressure(prompt_eval_count, num_ctx),
            # R5.1 (2026-08-27): the window the row actually ran at. Without it
            # no row is attributable to a num_ctx era after a default is raised
            # (R5 decision memo §5.1). Requested value, not the clamped ceiling —
            # declared_context_length below carries what the server would allow.
            "num_ctx": num_ctx,
            "declared_context_length": declared_context_length,  # F13
        },
    }

    write_json_atomic(out_path, data)

    resp_len = len(response_text)
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "ollama-clean":
        system_prompt = load_system_prompt()
        for fixture_id in CLEAN_FIXTURES:
            for model in OLLAMA_MODELS:
                run_ollama(model, fixture_id, system_prompt)

    elif cmd == "ollama-bugs":
        system_prompt = load_system_prompt()
        for fixture_id in HAS_BUGS_FIXTURES:
            for model in OLLAMA_MODELS:
                run_ollama(model, fixture_id, system_prompt)

    elif cmd == "single":
        if len(sys.argv) != 4:
            print("Usage: run_benchmark.py single <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        system_prompt = load_system_prompt()
        run_ollama(model, fixture_id, system_prompt)

    elif cmd == "planner":
        if len(sys.argv) != 4:
            print("Usage: run_benchmark.py planner <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        system_prompt = load_planner_system_prompt()
        run_planner(model, fixture_id, system_prompt)

    elif cmd == "planner-federal":
        if len(sys.argv) != 4:
            print("Usage: run_benchmark.py planner-federal <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        system_prompt = load_planner_federal_system_prompt()
        run_planner(model, fixture_id, system_prompt, condition="planner-federal")

    elif cmd == "planner-all":
        model = sys.argv[2] if len(sys.argv) > 2 else None
        models = [model] if model else OLLAMA_MODELS
        system_prompt = load_planner_system_prompt()
        for fixture_id in PLANNER_FIXTURES:
            for m in models:
                run_planner(m, fixture_id, system_prompt)

    elif cmd == "perspective":
        if len(sys.argv) != 4:
            print("Usage: run_benchmark.py perspective <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        system_prompt = load_perspective_system_prompt()
        run_perspective(model, fixture_id, system_prompt)

    elif cmd == "perspective-pilot":
        model = sys.argv[2] if len(sys.argv) > 2 else "qwen3:32b"
        system_prompt = load_perspective_system_prompt()
        for fixture_id in PERSPECTIVE_PILOT_FIXTURES:
            run_perspective(model, fixture_id, system_prompt)

    elif cmd == "perspective-remaining":
        import glob as _glob
        model = sys.argv[2] if len(sys.argv) > 2 else "qwen3:32b"
        model_tag = make_model_tag(model)
        done = set()
        for f in _glob.glob(os.path.join(RESULTS_DIR, f"ollama-perspective-*-{model_tag}-response.json")):
            name = os.path.basename(f).replace("ollama-perspective-", "").replace(f"-{model_tag}-response.json", "")
            done.add(name)
        remaining = [f for f in ALL_PERSPECTIVE_FIXTURES if f not in done]
        print(f"Model: {model}")
        print(f"Total perspective fixtures: {len(ALL_PERSPECTIVE_FIXTURES)}")
        print(f"Already done: {len(done)}")
        print(f"Remaining: {len(remaining)}")
        if not remaining:
            print("All perspective fixtures benchmarked!")
            sys.exit(0)
        print(f"Fixtures: {', '.join(remaining)}")
        system_prompt = load_perspective_system_prompt()
        for i, fixture_id in enumerate(remaining, 1):
            print(f"\n[{i}/{len(remaining)}]")
            run_perspective(model, fixture_id, system_prompt)

    elif cmd == "critic-remaining":
        import glob as _cglob
        model = sys.argv[2] if len(sys.argv) > 2 else "qwen3:32b"
        model_tag = make_model_tag(model)
        done = set()
        for f in _cglob.glob(os.path.join(RESULTS_DIR, f"ollama-bench-*-{model_tag}-response.json")) + \
                 _cglob.glob(os.path.join(RESULTS_DIR, f"ollama-fullproto-*-{model_tag}-response.json")):
            name = os.path.basename(f)
            name = name.replace("ollama-bench-", "").replace("ollama-fullproto-", "")
            name = name.replace(f"-{model_tag}-response.json", "")
            done.add(name)
        remaining = [f for f in ALL_CRITIC_FIXTURES if f not in done]
        print(f"Model: {model}")
        print(f"Total fixtures: {len(ALL_CRITIC_FIXTURES)}")
        print(f"Already done: {len(done)}")
        print(f"Remaining: {len(remaining)}")
        if not remaining:
            print("All critic fixtures benchmarked!")
            sys.exit(0)
        print(f"Fixtures: {', '.join(remaining)}")
        system_prompt = load_system_prompt()
        for i, fixture_id in enumerate(remaining, 1):
            print(f"\n[{i}/{len(remaining)}]")
            run_ollama(model, fixture_id, system_prompt)

    elif cmd == "bugreport":
        if len(sys.argv) < 4:
            print("Usage: run_benchmark.py bugreport <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        with open(BUGREPORT_SKILL_PATH) as f:
            system_prompt = strip_frontmatter(f.read())
        run_bugreport(model, fixture_id, system_prompt)

    elif cmd == "bugreport-remaining":
        import glob as _bglob
        model = sys.argv[2] if len(sys.argv) > 2 else "qwen3:32b"
        model_tag = make_model_tag(model)
        done = set()
        for f in _bglob.glob(os.path.join(RESULTS_DIR, f"ollama-bugreport-*-{model_tag}-response.json")):
            name = os.path.basename(f)
            name = name.replace("ollama-bugreport-", "").replace(f"-{model_tag}-response.json", "")
            done.add(name)
        remaining = [f for f in BUGREPORT_FIXTURES if f not in done]
        print(f"Model: {model}")
        print(f"Total fixtures: {len(BUGREPORT_FIXTURES)}")
        print(f"Already done: {len(done)}")
        print(f"Remaining: {len(remaining)}")
        if not remaining:
            print("All bug-reporting fixtures benchmarked!")
            sys.exit(0)
        with open(BUGREPORT_SKILL_PATH) as f:
            system_prompt = strip_frontmatter(f.read())
        for i, fixture_id in enumerate(remaining, 1):
            print(f"\n[{i}/{len(remaining)}]")
            run_bugreport(model, fixture_id, system_prompt)

    elif cmd == "evalreport":
        if len(sys.argv) < 4:
            print("Usage: run_benchmark.py evalreport <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        run_evalreport(model, fixture_id, load_evalreport_contract())

    elif cmd == "evalreport-baseline":
        if len(sys.argv) < 4:
            print("Usage: run_benchmark.py evalreport-baseline <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        run_evalreport(model, fixture_id, "", condition="baseline")

    elif cmd == "acr":
        if len(sys.argv) < 4:
            print("Usage: run_benchmark.py acr <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        run_acr(model, fixture_id, load_acr_skill())

    elif cmd == "acr-baseline":
        if len(sys.argv) < 4:
            print("Usage: run_benchmark.py acr-baseline <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        run_acr(model, fixture_id, "", condition="baseline")

    elif cmd == "opevidence":
        if len(sys.argv) < 4:
            print("Usage: run_benchmark.py opevidence <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        run_opevidence(model, fixture_id, load_opevidence_system_prompt())

    elif cmd == "opevidence-baseline":
        if len(sys.argv) < 4:
            print("Usage: run_benchmark.py opevidence-baseline <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        run_opevidence(model, fixture_id, "", condition="baseline")

    elif cmd == "titlehint":
        if len(sys.argv) < 6:
            print("Usage: run_benchmark.py titlehint <model> <fixture-id> "
                  "<titled|neutral> <draw>")
            sys.exit(1)
        model, fixture_id, condition, draw = sys.argv[2:6]
        validate_fixture_id(fixture_id)
        run_titlehint(model, fixture_id, condition, draw, load_system_prompt())

    elif cmd == "featurehint":
        if len(sys.argv) < 6:
            print("Usage: run_benchmark.py featurehint <model> <fixture-id> "
                  "<withfeatures|nofeatures> <draw>")
            sys.exit(1)
        model, fixture_id, condition, draw = sys.argv[2:6]
        validate_fixture_id(fixture_id)
        run_featurehint(model, fixture_id, condition, draw, load_system_prompt())

    elif cmd == "recipe":
        if len(sys.argv) < 4:
            print("Usage: run_benchmark.py recipe <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        run_recipe(model, fixture_id, load_recipe_system_prompt())

    elif cmd == "recipe-baseline":
        if len(sys.argv) < 4:
            print("Usage: run_benchmark.py recipe-baseline <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        run_recipe(model, fixture_id, "", condition="baseline")

    elif cmd == "cj":
        if len(sys.argv) < 4:
            print("Usage: run_benchmark.py cj <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        run_cj(model, fixture_id, load_cj_system_prompt())

    elif cmd == "cj-baseline":
        if len(sys.argv) < 4:
            print("Usage: run_benchmark.py cj-baseline <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        validate_fixture_id(fixture_id)
        run_cj(model, fixture_id, "", condition="baseline")

    elif cmd == "evalreport-remaining":
        import glob as _eglob
        model = sys.argv[2] if len(sys.argv) > 2 else "qwen3.6:35b"
        model_tag = make_model_tag(model)
        done = set()
        for f in _eglob.glob(os.path.join(RESULTS_DIR, f"ollama-evalreport-*-{model_tag}-response.json")):
            name = os.path.basename(f)
            name = name.replace("ollama-evalreport-", "").replace(f"-{model_tag}-response.json", "")
            if name.startswith("baseline-"):
                continue  # baseline runs never satisfy the contract condition
            done.add(name)
        remaining = [f for f in EVALREPORT_FIXTURES if f not in done]
        print(f"Model: {model}")
        print(f"Total fixtures: {len(EVALREPORT_FIXTURES)}")
        print(f"Already done: {len(done)}")
        print(f"Remaining: {len(remaining)}")
        if not remaining:
            print("All evaluation-report fixtures benchmarked!")
            sys.exit(0)
        system_prompt = load_evalreport_contract()
        for i, fixture_id in enumerate(remaining, 1):
            print(f"\n[{i}/{len(remaining)}]")
            run_evalreport(model, fixture_id, system_prompt)

    elif cmd == "score-all":
        import glob
        import subprocess
        score_script = os.path.join(os.path.dirname(__file__), "score_output.py")
        responses = sorted(glob.glob(os.path.join(RESULTS_DIR, "ollama-bench-*-response.json")))
        responses += sorted(glob.glob(os.path.join(RESULTS_DIR, "ollama-fullproto-*-response.json")))
        for resp in responses:
            with open(resp) as f:
                bench = json.load(f).get("_benchmark", {})
            fixture_id = bench.get("fixture_id", "")
            model = bench.get("model", "unknown")
            if not fixture_id:
                print(f"SKIP: No _benchmark metadata in {os.path.basename(resp)}")
                continue
            metadata = os.path.join(FIXTURES_DIR, f"{fixture_id}.metadata.yaml")
            if os.path.exists(metadata):
                print(f"\n{'='*60}")
                print(f"Scoring: {fixture_id} ({model})")
                print(f"{'='*60}")
                subprocess.run([sys.executable, score_script, resp, metadata])
            else:
                print(f"SKIP: No metadata for {fixture_id}")

    elif cmd == "small-test":
        system_prompt = load_system_prompt()
        for model in SMALL_MODELS:
            for fixture_id in CLEAN_FIXTURES + HAS_BUGS_FIXTURES:
                run_ollama(model, fixture_id, system_prompt)

    elif cmd == "score-perspective":
        import glob
        import subprocess
        score_script = os.path.join(os.path.dirname(__file__), "score_perspective.py")
        if not os.path.exists(score_script):
            print(f"ERROR: {score_script} not found")
            sys.exit(1)
        responses = sorted(glob.glob(os.path.join(RESULTS_DIR, "ollama-perspective-*-response.json")))
        for resp in responses:
            with open(resp) as f:
                bench = json.load(f).get("_benchmark", {})
            fixture_id = bench.get("fixture_id", "")
            model = bench.get("model", "unknown")
            if not fixture_id:
                print(f"SKIP: No _benchmark metadata in {os.path.basename(resp)}")
                continue
            metadata = os.path.join(PERSPECTIVE_FIXTURES_DIR, f"{fixture_id}.metadata.yaml")
            if os.path.exists(metadata):
                print(f"\n{'='*60}")
                print(f"Scoring perspective: {fixture_id} ({model})")
                print(f"{'='*60}")
                subprocess.run([sys.executable, score_script, resp, metadata])
            else:
                print(f"SKIP: No metadata for {fixture_id}")

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
