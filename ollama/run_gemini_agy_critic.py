#!/usr/bin/env python3
"""Benchmark Gemini 3.x Flash as a standalone a11y-critic, via the Antigravity
CLI (`agy`) — the repo has no `gemini` CLI. Blind-cuts each fixture with the
same strip_answer_key() the hosted lane uses, prepends the a11y-critic protocol,
and calls agy with the prompt as a single argv arg (no shell expansion — the
protocol contains backticks and $). Writes a {"response","usage",...} file per
fixture that ollama/score_output.py can score.

Usage:
    python3 ollama/run_gemini_agy_critic.py <low|medium|high> [fixture-id ...]
      (no fixture ids  -> the 33-fixture set the Gemini 2.5 Flash baseline used)
"""
import sys, os, json, subprocess, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_cloud_benchmark import strip_answer_key  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
FIX = os.path.join(REPO, "evals/suites/a11y-critic/fixtures")
SKILL = os.path.join(REPO, ".claude/skills/a11y-critic/SKILL.md")
OUT = os.path.join(REPO, "evals/results/gemini-3.8")

# Same 33 fixtures the committed Gemini 2.5 Flash baseline ran (evals/results/gemini/).
BASELINE_33 = [
    "accordion-no-region-role", "app-focus-order-illogical", "async-form-vague-success",
    "breadcrumb-navigation-no-nav-landmark", "button-skip-link-clean", "checkbox-group-no-fieldset",
    "combobox-autocomplete-no-listbox-role", "dashboard-heading-inconsistency", "data-table-missing-scope",
    "expandable-section-no-button", "file-input-no-labels", "form-field-vs-summary-errors",
    "form-validation-missing-aria-describedby", "heading-hierarchy-skipped", "image-carousel-no-region",
    "infinite-scroll-no-announcement", "interactive-dropdown-clean", "interactive-dropdown-focus-bug",
    "loading-state-missing-aria-busy", "megamenu-no-structure", "modal-complete-clean",
    "multistep-form-error-clearing", "pagination-no-nav-landmark", "popover-no-focus-management",
    "radio-button-group-no-grouping", "search-focus-stays-in-input", "search-results-dynamic-clean",
    "tabbed-nav-vs-tab-pattern", "tabs-incomplete-aria-selected", "tabs-missing-arrow-nav",
    "toast-notification-no-role", "tooltip-no-role-no-association", "video-player-missing-captions",
]


def strip_frontmatter(t):
    return t.split("---", 2)[2] if t.startswith("---") else t


def load_protocol():
    return strip_frontmatter(open(SKILL).read())


MAX_ATTEMPTS = 3  # empty-response ("/think stall") retry — repo precedent: a
                  # byte-identical re-draw recovers (qwen3.8 funnel, 2026-08-23).


def _agy_once(prompt, model):
    try:
        r = subprocess.run(
            ["agy", "-p=" + prompt, "--model", model, "--output-format", "json",
             "--print-timeout", "8m"],
            capture_output=True, text=True, timeout=600,
        )
    except subprocess.TimeoutExpired:
        return None, "timeout"
    if r.returncode != 0:
        return None, f"rc={r.returncode} {r.stderr[-160:]}"
    try:
        return json.loads(r.stdout), None
    except json.JSONDecodeError:
        return None, f"badjson {r.stdout[:120]}"


def run_one(fixture, effort, protocol):
    model = f"gemini-3.8-flash-{effort}"
    comp = strip_answer_key(open(os.path.join(FIX, fixture + ".md")).read())
    prompt = (protocol + "\n\n---\n\nReview the following component using the full "
              "protocol above. Output your findings.\n\n" + comp)
    d = None
    attempts = 0
    for attempt in range(1, MAX_ATTEMPTS + 1):
        attempts = attempt
        d, err = _agy_once(prompt, model)
        if err:
            print(f"RETRY {fixture} {effort} attempt {attempt}: {err}", flush=True)
            continue
        # Empty-response stall: valid JSON, clean stop, but 0-char response.
        # Retry (repo precedent: a re-draw recovers).
        if (d.get("response") or "").strip():
            break
        print(f"EMPTY {fixture} {effort} attempt {attempt} (0-char response) — retrying", flush=True)
        d = None
    if d is None or not (d.get("response") or "").strip():
        print(f"FAIL {fixture} {effort}: no non-empty response after {MAX_ATTEMPTS} attempts", flush=True)
        return
    os.makedirs(OUT, exist_ok=True)
    outp = os.path.join(OUT, f"gemini-bench-{fixture}-flash-{effort}-response.json")
    usage = d.get("usage", {})
    json.dump({"response": d.get("response", ""), "usage": usage, "model": model,
               "effort": effort, "attempts": attempts,
               "generated_at": datetime.datetime.utcnow().isoformat() + "Z"},
              open(outp, "w"), indent=2)
    print(f"OK {fixture} {effort} out_tok={usage.get('output_tokens')} "
          f"think={usage.get('thinking_tokens')} attempts={attempts}", flush=True)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("low", "medium", "high"):
        sys.exit("usage: run_gemini_agy_critic.py <low|medium|high> [fixture-id ...]")
    effort = sys.argv[1]
    fixtures = sys.argv[2:] or BASELINE_33
    protocol = load_protocol()
    print(f"Gemini 3.8 Flash ({effort}) critic — {len(fixtures)} fixtures", flush=True)
    for f in fixtures:
        run_one(f, effort, protocol)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
