# Plan 002: Fix scoring-logic defects that distort benchmark results

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat de0031f..HEAD -- ollama/score_output.py ollama/score_perspective.py ollama/score_planner.py evals/suites/smoke/ scripts/smoke_scorers.sh`
> If `score_*.py` changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition. (Changes to `evals/suites/smoke/`
> and `scripts/` from plan 001 are expected and required.)

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (scoring semantics change; future runs will not be number-compatible with old runs)
- **Depends on**: plans/001-ci-verification-baseline.md (smoke tests must exist first)
- **Category**: bug
- **Planned at**: commit `de0031f`, 2026-06-11

## Why this matters

The three `ollama/score_*.py` scripts produce the numbers published in `ollama/BENCHMARK.md` (e.g. "96% must-find detection", "0% false positives"). Verified defects in them bias results in both directions:

1. `score_perspective.py`'s verdict detector is a bare substring scan with BLOCK checked first — a response saying "this does not block users" is scored as verdict BLOCK. Every CLEAN perspective fixture's PASS/FAIL flows through this.
2. The CLEAN false-positive check re-scans the whole response body for the words BLOCK/REVISE instead of using the declared verdict, so hedged-but-correct PASS responses can be failed.
3. A response truncated mid-`<think>` block (a real failure mode — BENCHMARK.md documents qwen3.5 `/think` stalls) is scored as if the chain-of-thought were the final answer, because the strip regex only removes *closed* think blocks.
4. Keyword extraction silently degrades: `score_output.py`'s fallback takes the first 3 words of the rubric description with no length filter (stop-words like "the" match anything → inflates detection); `score_perspective.py`'s fallback filters words ≤3 chars and can return an **empty list**, which guarantees "not found" (deflates detection). Neither warns.

These fixes make future benchmark runs trustworthy. They do NOT retroactively validate or invalidate published numbers — the raw response artifacts lived in `/tmp` and are gone (see plan 003).

## Current state

All three scorers are standalone scripts: stdlib + PyYAML, flat functions, invoked as `python3 ollama/score_X.py <response.json> <metadata.yaml>`, communicating with the escalation runner solely through stdout — `run_cloud_benchmark.py:504` does `if "Status: PASS" not in proc.stdout`. **Any new status string must therefore NOT contain the substring `Status: PASS` unless it means pass.**

Key excerpts (verified at commit `de0031f`):

`ollama/score_perspective.py:61-69` — the defective verdict detector:
```python
def check_verdict(text: str) -> str:
    text_upper = text.upper()
    if "BLOCK" in text_upper:
        return "BLOCK"
    if "REVISE" in text_upper:
        return "REVISE"
    if "PASS" in text_upper:
        return "PASS"
    return "NONE"
```

`ollama/score_output.py:47-60` — the GOOD two-tier detector to model on (explicit `Verdict:` declaration first, keyword fallback second):
```python
def check_verdict(text: str) -> str:
    verdict_pattern = re.search(
        r"(?:#\s*)?(?:\*\*)?Verdict(?:\*\*)?[:\s]+\*?\*?(REJECT|REVISE|ACCEPT-WITH-RESERVATIONS|ACCEPT)\b",
        text, re.IGNORECASE,
    )
    if verdict_pattern:
        return verdict_pattern.group(1).upper()
    for verdict in ["ACCEPT-WITH-RESERVATIONS", "REJECT", "REVISE", "ACCEPT"]:
        if verdict in text.upper():
            return verdict
    return "NONE"
```

`ollama/score_perspective.py:247-249` — body-wide regex used for CLEAN false-positive "wrong verdict":
```python
    wrong_verdict = bool(re.search(r"\b(BLOCK|REVISE)\b", text))
    return {"structured_findings": count, "wrong_verdict": wrong_verdict}
```
and its consumer at `:289`:
```python
        passed = correct and (not fp["wrong_verdict"] or verdict in [v.upper() for v in alt])
```

`ollama/score_output.py:20-25` (same shape at `score_perspective.py:34-35`, `score_planner.py:17-18`) — strip regex that misses unclosed blocks:
```python
def strip_thinking(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
```

`ollama/score_output.py:82-83` — fallback keywords, no length filter:
```python
    else:
        keywords = description.lower().split()[:3]
```

`ollama/score_perspective.py:220-221` — fallback keywords, can return `[]`:
```python
    words = description.split()[:4]
    return [w.strip(".,;:") for w in words if len(w) > 3]
```

Thresholds (keep VALUES, name them): `score_output.py:236-237` and `score_perspective.py:362-364` print `Abort threshold: 40%` and gate `PASS` on `must_score >= 0.4`; `score_planner.py:132` gates on `>= 0.7`.

Smoke tests from plan 001: `evals/suites/smoke/*` + `scripts/smoke_scorers.sh` pin current behavior and MUST be updated in step 6 where behavior intentionally changes.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Compile | `python3 -m py_compile ollama/score_output.py ollama/score_perspective.py ollama/score_planner.py ollama/score_common.py` | exit 0 |
| Smoke | `bash scripts/smoke_scorers.sh` | exit 0, `ALL SMOKE TESTS PASSED` |
| Fixture validation | `python3 scripts/validate_fixtures.py` | exit 0 |
| Single scorer run | `python3 ollama/score_perspective.py evals/suites/smoke/perspective-clean-response.json evals/suites/smoke/perspective-clean.metadata.yaml` | output inspectable by eye |

## Scope

**In scope**:
- `ollama/score_common.py` (create — shared helpers)
- `ollama/score_output.py`, `ollama/score_perspective.py`, `ollama/score_planner.py` (modify)
- `evals/suites/smoke/` (add 2 new truncation smoke files; adjust existing expectations ONLY where this plan changes behavior)
- `scripts/smoke_scorers.sh` (extend)

**Out of scope** (do NOT touch):
- `ollama/run_benchmark.py`, `ollama/run_cloud_benchmark.py` — plan 003. The stdout contract (`Status: PASS` substring) must keep working unchanged.
- `ollama/BENCHMARK.md` result tables — historical record. You add ONE changelog note (step 7); never edit existing numbers.
- Fixture/rubric files under `evals/suites/{a11y-critic,a11y-planner,perspectives}/`.

## Git workflow

- Branch: `advisor/002-scorer-correctness`
- Conventional commits per step, e.g. `fix: two-tier verdict detection in perspective scorer`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Create `ollama/score_common.py`

Content (exactly this logic; docstrings may vary):

```python
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
    """Two-tier verdict detection.

    1. Explicit declaration:  'Verdict: REVISE' (with optional markdown).
    2. Fallback: whole-word scan, longest/most-specific ladder entry first.
    ladder example: ["BLOCK", "REVISE", "PASS"] or
                    ["ACCEPT-WITH-RESERVATIONS", "REJECT", "REVISE", "ACCEPT"].
    """
    alternatives = "|".join(re.escape(v) for v in ladder)
    m = re.search(
        rf"(?:#\s*)?(?:\*\*)?Verdict(?:\*\*)?[:\s]+\*?\*?({alternatives})\b",
        text, re.IGNORECASE,
    )
    if m:
        return m.group(1).upper()
    upper = text.upper()
    for v in ladder:
        if re.search(rf"\b{re.escape(v)}\b", upper):
            return v
    return "NONE"


def fallback_keywords(description: str, max_words: int = 4) -> list[str]:
    """Last-resort keyword extraction. Never returns an empty list."""
    words = [w.strip(".,;:()\"'") for w in description.split()[:max_words]]
    filtered = [w for w in words if len(w) > 3]
    return filtered or [w for w in words if w] or [description.strip()[:40]]
```

**Verify**: `python3 -m py_compile ollama/score_common.py` → exit 0. Then `python3 -c "import sys; sys.path.insert(0,'ollama'); from score_common import detect_verdict; print(detect_verdict('This does not block users. Verdict: PASS', ['BLOCK','REVISE','PASS']))"` → prints `PASS`.

### Step 2: Wire truncation detection into all three scorers

In each of `score_output.py`, `score_perspective.py`, `score_planner.py`:

1. Add `from score_common import ...` imports (the scripts are run from the repo root as `python3 ollama/score_X.py`; sibling imports work because the script's own directory is on `sys.path`).
2. Replace the local `strip_thinking` definition; in `load_response`, capture the `truncated` flag (return both, or set a module-level via a small refactor — keep it simple: have `load_response` return `(text, truncated)` and update the 1–2 call sites per file).
3. At the top of each `score…()` entry point: if truncated, print `Response truncated mid-<think> block — not scoring` and `Status: INCOMPLETE — truncated response`, then return. (`Status: INCOMPLETE…` does not contain `Status: PASS`, so the escalation runner correctly treats it as a failure and re-runs/escalates — that is the desired behavior for truncated output.)

**Verify**: create the two truncation smoke files and run them:
- `evals/suites/smoke/critic-truncated-response.json`: `{"response": "<think>I was reasoning about aria-describedby and live regions when the stream cut off"}`
- `evals/suites/smoke/perspective-truncated-response.json`: `{"response": "<think>vestibular analysis in progress"}`

`python3 ollama/score_output.py evals/suites/smoke/critic-truncated-response.json evals/suites/smoke/critic-hasbugs.metadata.yaml` → output contains `Status: INCOMPLETE` and does NOT contain `Status: PASS`. Same for the perspective scorer with `perspective-hasbugs.metadata.yaml`.

### Step 3: Replace `check_verdict` in `score_perspective.py`

Replace the body of `check_verdict` (lines 61–69) with a call to `detect_verdict(text, ["BLOCK", "REVISE", "PASS"])`. Note the fallback ladder order stays most-severe-first, but now matches whole words and only after no explicit `Verdict:` declaration is found.

**Verify**: `python3 -c "import sys; sys.path.insert(0,'ollama'); import score_perspective as sp; print(sp.check_verdict('Nothing here blocks users.\nVerdict: PASS')); print(sp.check_verdict('We must BLOCK this release.'))"` → prints `PASS` then `BLOCK`.

### Step 4: Fix the CLEAN false-positive check in `score_perspective.py`

In `check_false_positives` (lines 237–249): the function currently computes `wrong_verdict` from a body-wide regex. Change it to take the already-detected verdict as a parameter: `def check_false_positives(text: str, declared_verdict: str) -> dict:` and set `wrong_verdict = declared_verdict in ("BLOCK", "REVISE")`. Update the call site in the CLEAN branch (line 283) to pass the `verdict` computed at line 272. Leave the `structured_findings` pattern counting unchanged. The `passed` expression at line 289 keeps its shape but now both `correct` and `fp["wrong_verdict"]` derive from the same declared verdict (no more contradictory states from hedged prose).

Apply the same change to `score_output.py`'s `count_false_positives` (lines 101–124): it already uses `check_verdict(text)` internally (line 118) — refactor it to accept the verdict from the caller (line 154 computes `verdict` at line 145) instead of re-deriving it, so there is exactly one verdict source per run. Behavior should be identical for the smoke fixtures.

**Verify**: `python3 ollama/score_perspective.py evals/suites/smoke/perspective-clean-response.json evals/suites/smoke/perspective-clean.metadata.yaml` → `Status: PASS`. Then a hedged-prose probe: temporarily create `/tmp/hedged.json` with `{"response": "A stricter team might revise the spacing, but nothing here harms access.\nVerdict: PASS"}` and run it against `perspective-clean.metadata.yaml` → must now print `Verdict: PASS` and `Status: PASS` (under the old code this failed). Delete `/tmp/hedged.json` after.

### Step 5: Harden keyword extraction and surface misses

1. `score_output.py:82-83`: replace the bare `description.lower().split()[:3]` fallback with `fallback_keywords(description)` from `score_common` (lowercase the result for matching consistency with the existing `kw.lower() in text.lower()` check).
2. `score_perspective.py:220-221`: replace the return with `return fallback_keywords(description)`.
3. In both files' `check_finding`, when `found` is False, print nothing extra — but in the per-item result lines of the score functions (the `X`-marked lines), append the checked keywords so misses are auditable. Current line shape (`score_output.py:222-224`):
```python
        for r in must_find:
            marker = "+" if r["found"] else "X"
            wcag_marker = "W" if r["wcag_cited"] else "-"
            print(f"  {marker} [{wcag_marker}] {r['description'][:80]}")
```
Change the print to append `  (keywords: {', '.join(r['keywords_checked'])})` ONLY when `marker == "X"`. Apply to the must/should loops in both scorers (4 loops total: `score_output.py` must+should in the else-branch and the ADVERSARIAL branch; `score_perspective.py` must+should).

**Verify**: `python3 -c "import sys; sys.path.insert(0,'ollama'); from score_common import fallback_keywords; print(fallback_keywords('No role=\"x\" or y')); print(fallback_keywords('a b c'))"` → both print non-empty lists. Then `bash scripts/smoke_scorers.sh` → still `ALL SMOKE TESTS PASSED` (smoke fixtures use dispatch-table paths, so they are unaffected by fallback changes).

### Step 6: Name the thresholds and label them honestly

1. In `score_output.py` and `score_perspective.py`: replace the literal `0.4` in the Status gate and the literal `40%` in the printed line with `MUST_FIND_ABORT_THRESHOLD` (imported), printing `Abort threshold: {MUST_FIND_ABORT_THRESHOLD:.0%} (escalation gate — see score_common.py)`.
2. In `score_planner.py:132`: use `PLANNER_SECTION_PASS_THRESHOLD`.
3. Update `scripts/smoke_scorers.sh` expectations if any asserted line changed text (the `Status:` lines did not change for passing cases; only the `Abort threshold:` line gained a suffix — the smoke script does not assert on it, so likely no change needed; confirm).
4. Add the two truncation cases from step 2 to `scripts/smoke_scorers.sh` (assert output contains `Status: INCOMPLETE`).

**Verify**: `bash scripts/smoke_scorers.sh` → exit 0, `ALL SMOKE TESTS PASSED` (now 7 cases).

### Step 7: Record the scoring change in BENCHMARK.md (one appended note, no table edits)

Append at the very end of `ollama/BENCHMARK.md`:

```markdown
## Scoring changelog

- 2026-06-XX (plan 002): scorer fixes — two-tier verdict detection in
  score_perspective.py (was: bare substring, BLOCK-first), CLEAN false-positive
  check now uses the declared verdict (was: body-wide BLOCK|REVISE regex),
  truncated `<think>` responses now score `Status: INCOMPLETE` (was: scored as
  normal output), keyword fallback can no longer return an empty list, and the
  40% gate is named MUST_FIND_ABORT_THRESHOLD (escalation gate, not a quality
  bar). Results recorded above this line were produced by the pre-fix scorers
  and are not number-compatible with re-runs. Raw /tmp artifacts were not
  retained, so historical tables stand as-is.
```

**Verify**: `git diff ollama/BENCHMARK.md` shows ONLY the appended section; `grep -c "96%" ollama/BENCHMARK.md` returns the same count as before your change.

## Test plan

- The plan-001 smoke suite is the regression harness; step 6 extends it to 7 cases (2 new truncation cases).
- New behavior covered: truncation → INCOMPLETE (2 cases), hedged-prose CLEAN PASS (step 4 probe — make it permanent if cheap: you MAY add `perspective-hedged-clean-response.json` + a smoke assertion instead of the `/tmp` probe; preferred).
- Pattern to follow: the existing `scripts/smoke_scorers.sh` table style from plan 001.

## Done criteria

ALL must hold:

- [ ] `python3 -m py_compile ollama/*.py` exits 0
- [ ] `bash scripts/smoke_scorers.sh` exits 0 with all cases (≥7) passing
- [ ] `python3 -c "import sys; sys.path.insert(0,'ollama'); import score_perspective as sp; print(sp.check_verdict('does not block users. Verdict: PASS'))"` prints `PASS`
- [ ] Truncated-response runs print `Status: INCOMPLETE` and never `Status: PASS`
- [ ] `grep -n "0.4" ollama/score_output.py ollama/score_perspective.py` shows no remaining bare threshold literals in the gate lines (named constant used)
- [ ] `ollama/BENCHMARK.md` diff is append-only (changelog section)
- [ ] `git status` shows changes only in: `ollama/score_*.py`, `ollama/score_common.py`, `ollama/BENCHMARK.md`, `evals/suites/smoke/`, `scripts/smoke_scorers.sh`
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- Plan 001's smoke suite does not exist (`scripts/smoke_scorers.sh` missing) — dependency not met.
- The live code at the cited lines doesn't match the excerpts above (drift since `de0031f`).
- You find yourself wanting to change `run_cloud_benchmark.py`'s `"Status: PASS" not in proc.stdout` contract — that is plan 003's file; the contract must be preserved from this side.
- Any impulse to "correct" historical numbers in BENCHMARK.md tables.
- A smoke expectation fails for a case this plan did NOT intentionally change.

## Maintenance notes

- Future scorer changes must update `score_common.py` once, not three copies. The remaining duplication (fixture loading in the two runners) is plan 003's and a deferred refactor's territory.
- The first post-fix benchmark run will produce numbers on a corrected basis; whoever updates BENCHMARK.md next should add new tables under a "post-002 scoring" heading rather than mixing bases (and per repo practice, collect the measurements before writing the doc claims).
- Reviewer should scrutinize: that `detect_verdict`'s fallback uses word boundaries (`\bPASS\b`) — "PASSWORD" must not match; add that probe if in doubt.
- Deferred (out of scope here): factoring the must-find keyword dispatch tables into data files shared with the rubrics — bigger design question about rubric-coupled scoring.
