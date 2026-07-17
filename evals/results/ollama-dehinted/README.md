# Ollama de-hinted re-run lane — raw artifacts (2026-07-16)

First **post-de-hint** lane: the remediation run promised by the hint-comment disclosure in
`ollama/BENCHMARK.md`. Same model, settings, and machine protocol as the 2026-07-13 blind lane;
the fixtures no longer carry the inline `// BUG:` hint comments that every earlier lane saw.

- Run date: 2026-07-16 (17:21:58–20:18:54); transport: local Ollama **0.31.1** on a **dedicated
  `127.0.0.1:11435` server** (Ollama.app quit for the run — SIGTERM via `killall`; the AppleScript
  quit event is refused non-interactively — with `*:11434` reverting to the OrbStack container so
  claude-smart traffic never touched the benchmark GPU). Full Metal offload verified via `/api/ps`
  (`size == size_vram`, 24.2 GB). The dedicated-server requirement was independently re-verified
  the same day by the coordinating session: a single CLEAN fixture stalled 15+ minutes mid-stream
  on the app server vs 66–215 s on `:11435`.
- Runner: `python3 ollama/run_benchmark.py critic-remaining qwen3:32b` then
  `perspective-remaining qwen3:32b`, with `OLLAMA_URL=http://127.0.0.1:11435/api/generate` and
  `BENCHMARK_RESULTS_DIR` pointed at this directory. Same prompt prefixes, num_ctx (16384 critic /
  32768 perspective), and temperature (0.3) as the blind lane.
- Fixture state: content-identical to **main@ff982fb** — the de-hint pass (c0d21cc fixtures,
  0011346 guard, f1f0b2b disclosure) plus the `modal-complete-clean` repair (6420ea9) — run from
  branch merge commits 22ca16b/90752a8, verified byte-identical to main under `evals/suites/`,
  `ollama/`, and `.claude/skills/` before and during the run.
- Blindness receipts, this worktree, post-merge: `python3 ollama/test_blind_prompts.py` →
  "OK — 166 prompts checked across both runners; no answer-key markers, no hint comments"
  (run after each merge), and the leak one-liner
  (`re.search(r'\bBUG\b', load_fixture(f))` over all critic fixtures) prints `[]`.
- Scoring: post-003 `ollama/score_output.py` / `ollama/score_perspective.py`, unmodified; one
  output per fixture under `scores/`. Raw response JSONs (`response` + `_benchmark` provenance)
  committed so every number below re-derives.
- Wall-clock: critic 33 fixtures in **1.57 h** (median 159 s; HAS-BUGS 152 s / FLAWED 200 s /
  ADVERSARIAL 236 s / CLEAN 189 s); perspective 25 in **1.38 h** (median 192 s). Reproduces the
  blind lane's uncontended profile — no FLAWED/ADVERSARIAL blowup.

## What changed vs the 2026-07-13 blind lane (attribution ledger)

Read every delta below against this ledger — the lanes differ by more than the de-hint alone:

1. **Intended change**: inline hint comments stripped from 24/33 critic and 20/25 perspective
   fixtures (c0d21cc). For those fixtures, prompt deltas are the de-hint.
2. **`modal-complete-clean` conflates two changes**: 6420ea9 both repaired the fixture's two
   real unplanted defects (focus-trap selector, backdrop dismissal) **and** stripped its
   verdict hints (h1 "(CLEAN)" suffix, ACCEPT prose moved below the strip boundary). Its row is
   not a pure de-hint data point. The other 32 critic / 25 perspective fixtures differ from the
   blind lane only on the hint-comment axis (critic also sees the +3-line skill rule, next item).
3. **Critic system prompt is not identical across lanes**: `.claude/skills/a11y-critic/SKILL.md`
   gained 3 lines (native-HTML-first rule, 4d8f196) between the lanes. Small, but it plausibly
   nudges div-vs-button findings — see the `expandable-section` keyword note below. The
   perspective system prompt (SKILL + references) is byte-identical across lanes.
4. **Still open, disclosed, deliberate**: the CLEAN verdict-prose/title axis on the other 3
   critic CLEAN fixtures, and the HAS-BUGS/FLAWED title-leakage axis (fixture h1 titles name
   their planted bugs), both per 6420ea9's changelog entry. This lane is **comment-axis
   de-hinted, not fully unhinted**. Reassurance comments ("NOT a bug", "Works:") are deliberately
   kept per c0d21cc (FP-trap difficulty the rubrics were normed on); their fate is a separate
   calibration decision under discussion — if they change, that is a new changelog entry and a
   follow-up lane, not a revision of this one.

## Headline — qwen3:32b

| Suite | De-hinted (this run) | Hinted blind lane (2026-07-13) | Verdict on the hint effect |
|---|---|---|---|
| a11y-critic, 33 fixtures | **33/33 PASS**, must-find **67/68 scorer** / **67/68 content-adjudicated**, CLEAN 4/4 with **0** structured findings, ADVERSARIAL 3/3 articulated | 33/33 PASS, 66/68 scorer / 67/68 content, CLEAN 4/4, ADVERSARIAL 3/3 | **No measurable detection loss.** The hints were redundant for this model on this suite. |
| perspective-audit, 25 fixtures | **20 PASS / 4 WARN / 1 FAIL**; HAS-BUGS 16/16, ADVERSARIAL 4/4; must-find **35/37 scorer** / **36/37 content** | 20 PASS / 1 WARN / 4 FAIL; 16/16, 4/4; 36/37 scorer / 37/37 content | **One real must-find item proved hint-dependent** (map-interface target size). CLEAN flip is variance, not de-hinting — see below. |

## a11y-critic detail (33 fixtures)

- Tier statuses: HAS-BUGS 21/21 PASS, FLAWED 5/5 PASS, CLEAN 4/4 PASS, ADVERSARIAL 3/3 PASS.
- Must-find 67/68 scorer-level — one better than the hinted blind lane, because the
  `expandable-section-no-button` keyword artifact resolved itself: this run's audit emits the
  literal `<div>` string the rubric keys on ("Using `<div>` instead of `<button>`"). Plausibly
  nudged by the new native-HTML-first skill rule (ledger item 3); content-level coverage was
  already 4/4 in both lanes, so the delta is keyword-only.
- The single miss, adjudicated against the committed response: `infinite-scroll-no-announcement`
  → "Scroll-to-load mechanism not discoverable" is a **genuine miss again**. The audit notes the
  impact in passing ("Would need to manually scroll to new content without focus guidance") but
  never raises discoverability or a manual load-more control as a finding. Same item, same
  adjudication as the blind lane — the suite's hardest item for local models holds de-hinted.
  Content-adjudicated must-find: **67/68 (98.5%)** — identical to the hinted lane's
  content-level number. **De-hinting cost qwen3:32b nothing on critic detection.**
- CLEAN: 4/4 PASS, **zero** structured findings, correct verdicts (2 ACCEPT, 2
  ACCEPT-WITH-RESERVATIONS). `modal-complete-clean` — repaired and verdict-hint-stripped in
  6420ea9 — scores ACCEPT-WITH-RESERVATIONS with 0 findings: per the erratum's own criterion,
  this is the **first valid false-positive-avoidance data point for that fixture** (all earlier
  ACCEPT rows were hint-following plus defect blindness). Two-change conflation caveat applies
  (ledger item 2).
- ADVERSARIAL: 3/3 ACCEPT-WITH-RESERVATIONS with the central tradeoff articulated (semantic
  mismatch on `tabbed-nav-vs-tab-pattern`; dual-announcement tradeoff on
  `form-field-vs-summary-errors`; intentional focus retention on `search-focus-stays-in-input`).
- Verdict severity inflation persists but softer: 5 REJECT verdicts (3 where the rubric expects
  REVISE — popover, toast, video-player; 2 where no expected verdict is recorded) vs 7 in the
  blind lane. As before, the gate scores detection, not verdict match, on HAS-BUGS/FLAWED.

## perspective-audit detail (25 fixtures)

- HAS-BUGS 16/16 PASS, ADVERSARIAL 4/4 PASS.
- Must-find 35/37 scorer-level. The two misses, adjudicated:
  1. `tab-panel-arrow-keys` — the known compound-keyword rubric artifact
     (`role='tablist'/role='tab'/role='tabpanel'` as one literal string; scorer shows `[W]`).
     The audit raises "ARIA roles missing for tab components — MAJOR — 4.1.2" with evidence
     lines naming all three roles. Content-adjudicated: found. Same artifact in every lane.
  2. `map-interface-zoom` — "Zoom +/- buttons 18x18px — below minimum target size":
     **genuine miss, and the single measured de-hint effect in this run.** The hinted lane
     found it; this audit never discusses control size at all (no hit for 18/24/44/"target"/
     "small"; its only size findings are map-container reflow). The fixture's stripped hint
     comment named the defect. Content-adjudicated must-find: **36/37 (97.3%)** vs the hinted
     lane's 37/37.
- **CLEAN lane — the finding of this run, and it is about variance, not hints.** Wrong verdicts
  fell from 4/5 (hinted blind lane) to **1/5** — but the de-hint cannot explain this: no CLEAN
  perspective fixture carried hints, none of the five `.md`/`.metadata.yaml` files changed since
  2026-03-28..2026-06-13 (all pre-blind-lane; verified via `git log`), and the perspective
  system prompt is byte-identical across lanes. **The five CLEAN prompts are byte-identical in
  both runs; the flip is run-to-run sampling variance at temperature 0.3.** Per fixture:

  | Fixture | Blind lane (2026-07-13) | This run | Stable? |
  |---|---|---|---|
  | `article-page-clean` | PASS verdict + findings → WARN | PASS + 1 MINOR → WARN | Stable correct |
  | `dashboard-text-labels` | REVISE on 2 manufactured MAJORs → FAIL | **PASS, severity table all zeros** → WARN (scorer counts 2 structured blocks) | Full flip |
  | `login-form-clean` | internally-inconsistent REVISE → FAIL | PASS + 1 MINOR + 1 ENHANCEMENT → WARN | Full flip |
  | `nav-menu-landmarks` | BLOCK on manufactured missing-`<title>`/`lang` page-shell findings → FAIL | **Same two manufactured items** (as MAJORs), verdict REVISE (metadata accepts PASS/REVISE) → WARN | Substance persists; verdict de-escalated |
  | `media-player-captions` | REVISE over two MINOR open questions → FAIL | REVISE on a **manufactured MAJOR**: "Missing `aria-expanded` on transcript toggle" (cited as 2.4.4) — the transcript is a native `<details>`/`<summary>` disclosure whose expanded state is exposed natively, and 2.4.4 is Link Purpose → FAIL | **Wrong REVISE both runs**, different manufactured rationale |

- What is actually stable across the two identical-prompt runs: correct PASS on
  `article-page-clean`; wrong REVISE on `media-player-captions`; the page-shell over-flagging
  substance on `nav-menu-landmarks` (two document-shell findings against a React component
  fixture, both runs — only the severity/verdict moved). What is not stable: everything else.
  **Single-run CLEAN characterizations on a 5-fixture lane are two samples from a high-variance
  distribution — neither "4/5 wrong" nor "1/5 wrong" is the model's stable rate.** This
  generalizes the blind README's own toast-`role="alert"` stability warning. The routing rule —
  don't route CLEAN-confirmation perspective audits to local models without a second opinion —
  is reinforced, with **verdict instability** (not consistently-wrong verdicts) as the mechanism.

## What changes in the published story

- qwen3:32b's **critic detection survives de-hinting intact**: 67/68 content-adjudicated both
  lanes, CLEAN 4/4 with zero findings, ADVERSARIAL 3/3. The hint-assisted-upper-bound caveat on
  the historical critic rows stands as written, but for this model/suite the measured hint
  effect is nil (scorer-level actually +1 via the `<div>` keyword).
- qwen3:32b's **perspective detection loses exactly one item de-hinted** (36/37 vs 37/37
  content): the `map-interface-zoom` target-size defect was hint-carried. Historical perspective
  detection rows remain upper bounds; the bound is now measured at −1 item for this model.
- The **perspective CLEAN false-positive story must be re-told as variance**: the blind lane's
  "4/5 wrong verdicts" was one draw, this lane's "1/5" is another, on byte-identical prompts.
  Cite both, or cite neither — never one alone.
- `modal-complete-clean` gains its first valid FP-avoidance evidence (ACCEPT-W-R, 0 findings,
  post-repair, post-verdict-hint-strip).
- Negative space: this lane says nothing about the hint effect on other models (unmeasured);
  nothing about the still-open title/CLEAN-prose hint axes; its own numbers are a single run and
  carry the same single-sample caveat it documents; and the critic comparison is mildly
  confounded by the +3-line skill-rule delta (ledger item 3).

Score any response here with:

```bash
python3 ollama/score_output.py <response.json> evals/suites/a11y-critic/fixtures/<id>.metadata.yaml
python3 ollama/score_perspective.py <response.json> evals/suites/perspectives/fixtures/<id>.metadata.yaml
```
