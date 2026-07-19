# Ollama post-PR-4 re-baseline lane — raw artifacts (2026-07-17 → 2026-07-19)

First lane on the **fully corrected corpus**: comment hints stripped (de-hint pass), verdict-
steering sections cut and reassurance comments removed (PR #4), CLEAN titles de-hinted. This is
the first measurement in the suite's history where critic CLEAN false-positive resistance and
critic ADVERSARIAL analysis quality are **unassisted** — no prompt contained its expected
verdict, grading notes, Ambiguity analysis, or reassurance comments. It is also the third draw
for the perspective CLEAN-variance story, on harder FP traps.

- Transport: local Ollama **0.31.1** on the dedicated `127.0.0.1:11435` server (Ollama.app quit
  for the whole window; `*:11434` on the OrbStack container). Full Metal offload verified via
  `/api/ps` (`size == size_vram`; 24.2 GB at 16K ctx, 29.2 GB at 32K).
- Runner: `critic-remaining qwen3:32b` then `perspective-remaining qwen3:32b`,
  `OLLAMA_URL=http://127.0.0.1:11435/api/generate`, `BENCHMARK_RESULTS_DIR` → this directory.
  Same prompt prefixes, num_ctx (16384 critic / 32768 perspective), temperature 0.3 as every
  prior lane.
- Fixture state: **main@666e6eb** (repo renamed to `accessibility-skills` the same day; content
  equal to the PR #4 merge plus its post-merge docs commit). Pre-flight guard on the exact
  corpus: `test_blind_prompts.py` → "OK — 166 prompts … no answer-key markers, no hint
  comments, no reassurance/verdict text" (the upgraded guard including PR #4's
  REASSURANCE_PATTERNS).
- Scoring: post-003 `score_output.py` / `score_perspective.py`, unmodified; per-fixture outputs
  under `scores/`.

## Run interruptions (documented, artifacts unaffected)

The critic suite started 2026-07-17 12:00 and ran 20 fixtures at normal pace (95–295 s). The
laptop then went to battery and spent ~2026-07-17 13:00 → 2026-07-19 10:05 in macOS
maintenance-sleep cycles (receipts: `pmset -g log` — Deep Idle with 45 s DarkWakes, full wake
on AC reconnect). Generation only progressed during wake slivers, so **fixtures 21–29 carry
sleep-inflated `elapsed_seconds` (1.6 h – 12 h wall-clock each); those timing fields are junk
and excluded from the timing summary below.** Every artifact is nonetheless complete and
uncorrupted (`done_reason=stop`, zero truncations — sleep pauses generation; it does not alter
it). The remainder ran under `caffeinate -is` (now part of the protocol; see the port-topology
protocol note). Two Claude-session restarts also occurred; the runner survived one and was
killed mid-perspective by the other — `*-remaining` resume semantics continued from the
artifacts on disk both times, with the fixture in flight at kill time re-run from scratch
(atomic writes; no partial artifacts).

- Timing, uncontaminated stretches only: critic median **~150 s**/fixture (n=24 awake-stretch
  fixtures); perspective median **218 s** (n=22 caffeinated stretch; 25/25 total ≈ 1.8 h).

## Headline — qwen3:32b, first unassisted rows

| Suite | Post-PR-4 (this run) | De-hinted lane (2026-07-16, verdict-assisted CLEAN/ADVERSARIAL) | What changed |
|---|---|---|---|
| a11y-critic, 33 fixtures | **30 PASS / 2 WARN / 1 FAIL**; must-find **65/68 scorer & content**; CLEAN: 1 clean pass, 2 correct-verdict-with-findings, **1 wrong REVISE**; ADVERSARIAL 3/3 (verdicts stricter, still valid) | 33/33 PASS; 67/68; CLEAN 4/4 zero findings; ADVERSARIAL 3/3 | **The "0% critic CLEAN false positives" era was verdict-assisted.** Unassisted, qwen3:32b over-flags CLEAN code. Detection dip is variance (see adjudication). |
| perspective-audit, 25 fixtures | **19 PASS / 1 WARN / 5 FAIL**; HAS-BUGS **15/16** (first HAS-BUGS FAIL: checkout-form 1/3); ADVERSARIAL 4/4; must-find **33/37 scorer / 34/37 content**; CLEAN **4/5 wrong verdicts** (draw 3) | 20 PASS / 4 WARN / 1 FAIL; HAS-BUGS 16/16; 35/37 scorer / 36/37 content; CLEAN 1/5 wrong (draw 2) | Detection variance now visible on HAS-BUGS too; CLEAN draw 3 lands 4/5 wrong on the harder corpus. |

## a11y-critic detail (33 fixtures)

- Tiers: HAS-BUGS 21/21 PASS, FLAWED 5/5 PASS, ADVERSARIAL 3/3 PASS, CLEAN 1 PASS / 2 WARN /
  1 FAIL.
- **CLEAN lane — the first unassisted draw, receipts:**
  - `button-skip-link-clean` → **REVISE (FAIL)** — the first critic CLEAN false-positive
    verdict recorded for qwen3:32b in any lane. Lead finding: "Skip link does not set focus on
    main content" — the fixture's `<a href="#main-content">` → `<main id="main-content">` is
    the standard pattern (fragment navigation moves the sequential-focus starting point in
    modern browsers; `tabindex="-1"` on the target is belt-and-braces hardening, and its
    absence is not a WCAG failure). Over-flag.
  - `modal-complete-clean` → ACCEPT-W-R (correct) **with structured findings** ("missing live
    region for modal state changes" as a critical-fix recommendation) → WARN. Prompt
    byte-identical to the de-hinted lane (its cut line predates ff982fb; PR #4 did not touch
    it), where the same prompt drew **zero** findings — the CLEAN finding-count is
    run-unstable on the critic side too.
  - `search-results-dynamic-clean` → ACCEPT-W-R (correct) with findings → WARN. Lead claim
    "label hidden with `display:none` instead of `sr-only`" was cross-checked against source:
    the input carries `aria-label="Search query"`, so an accessible name exists and the
    finding is an over-flag — but note the fixture does hide its `<label>` with
    `display:none` under a comment claiming "Hidden but accessible", which is misleading
    authoring (the label element itself is out of the a11y tree; the aria-label is what
    works). Fixture-hygiene note, not an erratum: swapping to `.sr-only` would remove the
    smell.
  - `interactive-dropdown-clean` → ACCEPT-W-R, no findings. The lane's one fully clean CLEAN row.
- Must-find 65/68 scorer = content-adjudicated (95.6%). The three misses, all adjudicated
  against response text:
  1. `accordion-no-region-role` "Missing role='region'" — **genuine; zero mention** of
     region/landmark anywhere in the audit. Prompt byte-identical to the de-hinted lane
     (found 2/2 there) → detection variance on HAS-BUGS.
  2. `tooltip-no-role-no-association` "Tooltip not announced when focused" — **genuine
     partial**: announcement impact is mentioned inside another finding, but no live-region/
     status mechanism finding is raised (found 3/3 in the de-hinted lane; identical prompt →
     variance).
  3. `infinite-scroll-no-announcement` discoverability — genuine, missed in **every** local
     lane; the suite's hardest item.
- ADVERSARIAL, first unassisted draw: 3/3 PASS with articulation gates met, but verdicts
  shifted stricter without the grading notes: `tabbed-nav-vs-tab-pattern` REVISE,
  `search-focus-stays-in-input` REVISE (both metadata-valid), `form-field-vs-summary-errors`
  ACCEPT-W-R. The assisted lanes' uniform ACCEPT-W-R was partly the grading notes talking.
- Verdict calibration: 5 REJECT (3 where the rubric expects REVISE) — stable across all three
  2026-07 lanes. New this run: the two fixtures PR #4 reassurance-stripped on the critic side
  (`app-focus-order-illogical`, `multistep-form-error-clearing`) both drew *lenient* verdicts
  (ACCEPT / ACCEPT-W-R vs expected REVISE) with detection intact (1/1 each) — direction is
  opposite to what reassurance-removal would predict; single-draw observation, not attributed.

## perspective-audit detail (25 fixtures)

- HAS-BUGS 15/16 PASS. **`checkout-form-broken-errors` FAIL at 1/3 must-find — the first
  HAS-BUGS perspective failure for qwen3:32b in any lane.** The two missed items are the
  `htmlFor` label-mismatch bugs; the audit never mentions label-for association (receipt:
  zero `htmlFor`/`for=` hits in the response; its error-association finding is the third,
  [W]-credited item). PR #4 did **not** touch this fixture — the prompt is byte-identical to
  the de-hinted lane, where the same prompt scored 3/3. Detection variance, now demonstrated
  at fixture-FAIL magnitude.
- ADVERSARIAL 4/4 PASS. Must-find 33/37 scorer / 34/37 content:
  - `map-interface-zoom` target-size (18×18 px) missed again — zero size discussion.
    **Hint-dependence now confirmed across two consecutive de-hinted draws** (found only when
    the hint comment named it).
  - `tab-panel-arrow-keys` — the compound-keyword rubric artifact, `[W]` credit, content
    present (same as every lane).
  - checkout ×2 as above (genuine).
- **CLEAN lane, draw 3 — 4/5 wrong verdicts on the harder corpus:**
  | Fixture | Draw 1 (blind, 2026-07-13) | Draw 2 (de-hinted, 2026-07-16) | Draw 3 (this run) |
  |---|---|---|---|
  | `article-page-clean` | PASS ✓ | PASS ✓ | **REVISE ✗** over 1 MINOR + 1 ENHANCEMENT ("REM sleep terminology") — verdict inflation over minor content |
  | `dashboard-text-labels` | REVISE ✗ (manufactured MAJORs) | PASS ✓ (0 findings) | **REVISE ✗** — "stat card borders below 3:1" (the `#e0e0e0` ratio is real, but decorative card borders are not 1.4.11 UI components; criterion misapplied) |
  | `login-form-clean` | REVISE ✗ (self-contradictory) | PASS ✓ (1 MINOR + 1 ENH) | **REVISE ✗** — same "corrective suggestions" item as draw 2, now inflated MINOR→MAJOR |
  | `media-player-captions` | REVISE ✗ | REVISE ✗ | **REVISE ✗** — verdict line says "MAJOR findings present" while its own table lists 4 MINORs; internally inconsistent again |
  | `nav-menu-landmarks` | BLOCK ✗ | REVISE (tolerated) | REVISE (tolerated, WARN) — same manufactured "Missing Page Title" MAJORs against a component fixture, third consecutive draw |
  - Attribution discipline: draws 1↔2 were byte-identical prompts (variance proven there).
    Draw 3 runs on a **changed corpus** — all five CLEAN fixtures had "(CLEAN)"-style titles
    de-hinted and the suite lost its reassurance comments — so 4/5-wrong here is consistent
    with variance, with the harder corpus, or both; n=1 per corpus cannot decompose it.
  - What is stable across all three draws: `media-player-captions` wrong REVISE (3/3 draws,
    each with a different manufactured rationale) and `nav-menu-landmarks` page-shell
    over-flagging (3/3 draws). `article-page-clean`'s flip kills the draw-1/2 "stable
    correct" label — with three draws, **no CLEAN fixture except media-player (stably wrong)
    has a stable outcome.**

## What changes in the published story

- **"Zero critic CLEAN false positives" is retired.** It was a verdict-assisted artifact:
  the first unassisted draw yields 1 wrong REVISE + 2 correct-verdict-with-findings on 4
  CLEAN fixtures. qwen3:32b's over-flagging weakness is not perspective-specific — it was
  masked on the critic side by the fixtures' own grading prose.
- **Detection is run-variable, not just verdict calibration**: byte-identical prompts flipped
  accordion (2/2→1/2), tooltip (3/3→2/3), modal findings (0→2), and checkout-form
  (3/3→1/3, a fixture-level FAIL) between consecutive lanes at temperature 0.3. Single-lane
  must-find deltas of ±2–3 items are within observed variance and should not be read as
  corpus effects without adjudication.
- `map-interface-zoom` target-size is confirmed hint-carried (two de-hinted draws, zero
  mentions).
- The routing rule hardens: local qwen3:32b is a **detector, not a verdict authority** — on
  clean code its verdicts are unstable in both suites, and even detection has draw-to-draw
  spread. Use it to surface candidate findings; verify severity/verdict with a second
  opinion.
- Negative space: single draw on the post-PR-4 corpus (its own numbers carry the variance
  caveat this lane documents); HAS-BUGS/FLAWED titles still name their planted bugs (open
  axis — detection rows remain title-assisted to that extent); nothing here measures other
  models on the corrected corpus.

Score any response here with:

```bash
python3 ollama/score_output.py <response.json> evals/suites/a11y-critic/fixtures/<id>.metadata.yaml
python3 ollama/score_perspective.py <response.json> evals/suites/perspectives/fixtures/<id>.metadata.yaml
```
