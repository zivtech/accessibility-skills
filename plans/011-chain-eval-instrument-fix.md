# Plan 011 — Chain-Eval Instrument Fix

> **Created**: 2026-06-13 (follow-up to plan 009's pilot)
> **Priority**: P3 · **Effort**: M · **Depends on**: 009 (pilot evidence)
> **Status**: IN PROGRESS — free scorer/fixture work landed (commits `0761855` + `e6c56aa`); proposal-critic (Opus) returned **REVISE / NOT-READY** for the paid re-run. See "Proposal-critic review" at the end.
> **Source of findings**: `evals/suites/chain/pilot/PILOT-REPORT.md` (I1–I8) plus two
> findings this plan adds from re-reading the captured pilot outputs (I2-semantic, I9).

## Goal & gate

Make the chain-eval **measurement apparatus** trustworthy so the full 8-fixture
`/a11y-workflow` run produces scores worth paying for. The pilot proved the *chain under
test* is healthy (handoff 2/2, escalation mechanically correct, audits excellent); the
blocker is the scorer + harness, not the workflow.

**STOP condition / gate**: do NOT launch the paid 8-fixture run (or even the 3-fixture
pilot re-run, ~12 Opus/Haiku subagent calls) until I1 + I2–I4 + I8 land AND the free
smoke-test validation (below) passes. The paid re-run is the *integration* confirmation,
not the validation mechanism — most fixes are validated for free against extracted pilot
snippets first.

## What the pilot actually showed (so we fix the right thing)

- Only the **video** critic peeked (operator INTEGRITY annotation, video `critic.txt:3-9`).
  Modal and login critics stayed blind. The contamination *hole* is nonetheless real and
  general: `targets/<id>/` sits one `../` hop from the answer key `rubrics/<id>.chain.yaml`.
- The three critics emitted **three different perspective vocabularies** — none a clean
  bijection to the perspectives suite's canonical 7. This is the dominant S3 distortion.
- Both defined tracers **did** survive end-to-end; the scorer just couldn't see them
  (18-char leading-substring match).

## Fixes

### I1 — CRITICAL: contamination (agents can read the answer key)

Two layers, because the chain runs through real Claude Code subagents (the production
mechanism IS the test — no per-spawn filesystem jail available):

1. **Prevention (primary)** — stage isolation. A `stage_target.py` helper copies a target
   into an isolated working dir OUTSIDE the eval tree (mirrors the cloud runner's
   `GEMINI_NEUTRAL_CWD` pattern); the orchestrator passes the agent ONLY that path.
   Navigating `../` from there lands in scratch space, not the repo. Plus explicit
   orchestrator prompt language: *do not read any `rubrics/`, `*.chain.yaml`,
   `*.metadata.yaml`, or `evals/suites/perspectives/` path.*
2. **Detection (backstop)** — `detect_peek()` in `score_chain.py` flags any stage output
   containing answer-key fingerprints (`expected_alarm_levels`, "expected alarm levels are",
   `tracer_finding`, `.chain.yaml`, `expected_escalated_perspectives`, `s3_scoring_mode`,
   `expected_audit_verdict`, `must_find`). A flagged stage's S3/S4/tracer are marked
   INVALID, not scored.

**Decision — detector input must be pristine (see I9).** The detector runs on raw agent
output only. Operator annotations that legitimately quote the answer key must live in a
separate file or the scorer will false-positive (it would on the current captured `.txt`).

### I2 — MAJOR: perspective taxonomy crosswalk + the absent-vs-LOW semantic

Two coupled changes in `score_chain.py`:

**(a) Crosswalk.** Expand `P_MAP` to a lens→canonical-key crosswalk covering every observed
lens. Documented mapping decisions (imperfect where the critic taxonomy has no clean
canonical home — recorded as a limitation):

| critic lens | → canonical key | note |
|---|---|---|
| screen reader | screen_reader_semantic | |
| keyboard / keyboard-only / motor / switch access / voice control / speech / voice | keyboard_motor | all = input-modality/motor axis; the canonical 7 has no separate voice/switch axis |
| low vision | magnification_reflow | **ambiguous**: low vision spans magnification AND contrast; mapped to the dominant zoom/reflow axis. `contrast`/`color` keep mapping to environmental_contrast |
| seizure / vestibular / photosensitive | vestibular_motion | |
| auditory / caption / hearing / deaf | auditory_access | |
| cognitive / neurodivergent | cognitive_neurodivergent | |

When multiple lenses collapse to one canonical key, take the **highest** alarm among them
(most conservative — reflects the critic's strongest concern on that axis), not first-match.

**(b) Absent → LOW, not MISSING→0.** A critic's job is to *raise* alarms, not enumerate a
fixed 7. A perspective the critic doesn't mention is *not an alarm* = LOW, not a zero.
Current scorer scores absent = 0.0 even against expected LOW — penalizing correct silence,
the biggest S3 depressor. Fix: absent canonical key → actual = "LOW". Then
`alarm_score(LOW, expected)` naturally gives 1.0 for expected-LOW, 0.5 for expected-MEDIUM,
0.0 for expected-HIGH.

> Validation target (modal): broken scorer = 0.214; fixed ≈ 0.71; manual ≈ 0.6. Both in the
> healthy band, far from the artifact floor. We do NOT over-fit to 0.6 — the report's manual
> figure is explicitly approximate.

### I3 — MAJOR: concept-based tracer match

Replace the 18-char leading-substring with a content-word overlap test: tokenize the
tracer's distinctive content words (drop stopwords), require ≥ N present in the final
stage output (N = min(3, #content_words), case-insensitive). Validates against the real
audit phrasings:
- modal tracer "Focus not moved to modal on open — stays on trigger button" vs audit
  "No focus movement INTO the dialog on open … Focus stays on the trigger" → MATCH.
- video tracer "Missing `<track kind=captions>`" vs audit "no `<track>` child … NO
  captions" → MATCH.

### I4 — MAJOR: audit-verdict parsing (verdict line + finding counts, not "PASS" token)

The audit's verdict vocabulary is ACCEPT / ACCEPT-WITH-RESERVATIONS / REVISE / REJECT — the
rubric's `expected_audit_verdict: PASS` means **"came back clean."** Define:

```
PASS  ⟺  verdict ∈ {ACCEPT, ACCEPT-WITH-RESERVATIONS}  AND  CRITICAL count = 0  AND  MAJOR count = 0
```

Parse the explicit recommendation line (`Overall recommendation: <VERDICT>`) and count
`CRITICAL`/`MAJOR` finding markers — never a bare `\bPASS\b` token (which matches "Many PASS
items recorded"). Validation: captured login audit (`Overall recommendation: REVISE`,
`MAJOR: 3`) → audit-verdict = 0 (correctly non-PASS). Synthetic clean audit (ACCEPT, 0/0) → 1.

### I5 — MINOR: scope S5a leak check per-perspective

Only flag LOW-perspective leakage when an impact word co-occurs **inside that perspective's
own section**, not anywhere in the audit. (Modal/login scored S5a=0 despite correct scoping.)

### I6 — MINOR: read `.md` with `.txt` fallback

`score_chain.py` reads `<stage>.md` then falls back to `<stage>.txt`. Removes the manual
copy step. (Protocol already standardizes on `.md`.)

### I7 — MINOR: S1a budget

Raise the S1a scout budget from 1500 → 2000 chars (all 3 pilot scouts ran 1779–2072 on a
multi-file directory target; 1500 is unrealistic). Document the rationale in the protocol.

### I8 — FIXTURE: make `login-form-clean` genuinely clean

The component carries a real MAJOR stale-error bug (`component.jsx`: errors set only in
`handleSubmit:22`, never cleared in `onChange:51/:68`; `submitted` latches at `:23`, so a
corrected field keeps `aria-invalid` + stale error text/`describedby` until re-submit). The
chain *correctly* caught it (planner, critic, AND audit independently). **Decision: FIX the
component, don't re-label** — re-labeling would destroy the suite's narrow-escalation +
clean-audit probe (only fixtures 4 & 5 fill that role). Fix = clear each field's error on
change so it returns to neutral after correction. Then re-run `extract_targets.py` and
re-confirm no "CLEAN"/answer hints leak into the target (protocol maintenance note).

Post-fix expectation, consistent end-to-end: genuinely-clean login → critic escalates
cognitive_neurodivergent ONLY (ground truth keeps it MEDIUM) → S4=1 → audit ACCEPT, 0
MAJOR → PASS.

### I9 — NEW (this plan): capture hygiene — scored artifacts must be pristine

Discovered re-reading the pilot: the captured `critic.txt`/`audit.txt` interleave raw agent
output with operator commentary that *quotes the answer key and restates verdicts/tracers*.
Any automated scorer (and the I1 detector) reads that operator text as if the agent wrote
it. Fix the **protocol**: stage outputs are saved verbatim (agent output only) to
`<stage>.md`; all operator notes go to a sibling `<stage>.notes.md` or into `RESULTS.md`.
The scorer reads only the pristine file. Without this, I1 detection and I2/I3/I4 parsing are
unreliable regardless of the agent's behavior.

## Decisions needing operator input (flagged, not assumed)

1. **All-LOW never-escalate fixture** (protocol's stated highest-value gap; PILOT-REPORT
   rec #3). Authoring it is free (one component + rubric, no paid run), but it adds a 9th
   fixture and changes pilot composition. **Recommend: author it now** (closes the only
   unprobed S4 branch) — but it's separable; confirm include vs defer.
2. **I2 ambiguous mappings** (`low vision → magnification_reflow`; voice/switch/speech →
   keyboard_motor). Reasonable but lossy. Acceptable as a documented limitation, or we
   standardize the critic's output taxonomy upstream (bigger change, out of scope here).

## Validation (free, before any paid run)

Extend `scripts/smoke_scorers.sh` (or a new `smoke_chain.sh`) with unit cases built from
pristine extracted snippets — NOT by re-scoring the annotated captured files:
- I2 crosswalk + absent-LOW: feed modal & login alarm tables → assert S3 in healthy band, > 0.
- I3: feed the two tracer/audit pairs → assert MATCH; feed an unrelated sentence → assert MISS.
- I4: feed `Overall recommendation: REVISE`/`MAJOR: 3` → 0; synthetic ACCEPT/0/0 → 1;
  "Many PASS items" with no verdict line → not a false 1.
- I1 detector: feed video's "Expected alarm levels are pre-defined…" → FLAG; pristine clean
  snippet → no flag.

## Then (gated): 3-fixture pilot re-run

Only after the above. ~12 subagent calls (Haiku scout + Opus planner/critic/audit ×3),
Claude Code subagents (production mechanism). Confirms the fixed instrument end-to-end —
especially that I1 staging actually blocks the peek and I9 capture is pristine. Requires
explicit operator cost approval at the gate.

## Files touched

- `evals/suites/chain/score_chain.py` (I2–I7, I1 detector)
- `evals/suites/chain/stage_target.py` (NEW — I1 staging helper)
- `evals/suites/chain/targets/login-form-clean/component.jsx` (I8) + re-run extract_targets
- `evals/suites/chain/CHAIN-EVAL-PROTOCOL.md` (I1 instruction, I6, I7, I9 capture rule, S3 semantic)
- `scripts/smoke_*.sh` (validation cases)
- `evals/suites/chain/RESULTS-TEMPLATE.md` (I9 pristine-vs-notes split, if needed)

## Proposal-critic review (2026-06-13) — REVISE / NOT-READY for the paid re-run

An Opus proposal-critic ran the real scorer against the real captured pilot sessions — the
integration this plan deferred — and found the free validation was **circular** (it tests the
scorer against hand-authored pristine snippets, not real session output). Must-fix BEFORE
funding the ~12-subagent re-run; **all free**:

- **C1/C2 — validate on real captures, not authored snippets.** The 19 unit tests use hand-built
  tables; the real `.md` captures are still annotated (`.md` == `.txt`; no `.notes.md` exists).
  Running the real scorer today, `login-form-clean` → CONTAMINATED because `detect_peek` matched
  the OPERATOR's annotation token `expected_escalated_perspectives` (the login critic actually
  stayed blind). Fix: implement/enforce I9 pristine capture (agent output verbatim to `<stage>.md`;
  operator notes in a marked zone the scorer strips), then re-score the 3 existing sessions with
  explicit pass criteria (login un-flagged, video flagged, modal PASS). That free re-score IS the
  missing integration test and the real gate.
- **M2 — `parse_alarms` binds prose, not just alarms.** "The screen reader experience is HIGH
  quality" → `screen_reader_semantic: HIGH`. Real critic prose ("high confidence", "major
  strength") corrupts S3/S4/S5. Fix: parse only structured alarm rows (table `|` or explicit
  marker) or require level-near-lens proximity excluding quality words; require the critic to emit
  a parseable alarm table in the orchestrator prompt.
- **M1 — the all-LOW breadcrumb penalizes defensible judgment.** A competent critic may rate
  `cognitive_neurodivergent: MEDIUM` on a deep breadcrumb (truncation/disclosure) → spurious S4=0
  on the headline metric. Fix: reclassify fixture-9 S4-on-escalation as observational (investigate,
  not auto-fail), or accept the all-LOW branch may be unprobeable with a realistic component.
- **Document honestly (no code):** `detect_peek` catches verbatim leaks only (paraphrase evades it,
  M4); I1 staging is defense-in-depth, not a filesystem jail (an agent can read an absolute path,
  M5); the crosswalk's low-vision→magnification is a one-way contrast-facet loss (M3); S5b is a
  substring presence check, not coverage (m1); wire chain tests into a named smoke script (m2).
- **No capture harness exists** — the run is hand-orchestrated, so the I9 rule is unenforced and
  broke in the very pilot that motivated this plan. Define the capture discipline before the re-run.

Full review: proposal-critic agent `a3a8268b82500561c`.
