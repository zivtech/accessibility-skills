# WCAG-EM Step 11 — First Model Rows on Both Instruments (2026-08-01)

First live rows on the two step-11 instruments the same day they were built
(adoption plan: [docs/wcag-em-2-adoption-assessment.md](../../../docs/wcag-em-2-adoption-assessment.md),
Step 11 status): the evaluation-report chain lane (`transit-portal-q3`,
contract vs baseline conditions) and the de-hinted planner audit fixture
(`test-hybrid-product-audit`).

**Single draw per condition — these are first receipts, not stable rows.**
The qwen3:32b history shows byte-identical prompts flipping 2–3 scored items
at temperature 0.3; treat every delta below as provisional until a repeat
draw confirms it. Nothing here is folded into BENCHMARK.md aggregates.

## Method

- Model: `qwen3.6:35b` (current detector recommendation), temp 0.3, one draw
  per condition. num_ctx 32768 (evalreport lane), planner lane default.
- Runner: `ollama/run_benchmark.py` at the step-11b commit —
  `evalreport` / `evalreport-baseline` / `planner` verbs.
- **Server gotcha, disclosed:** the first launch 404'd. On this dual-stack
  macOS host, `localhost:11434` resolves to `::1`, where the CPU-only
  OrbStack container listens with a 5-model store that lacks qwen3.6:35b;
  the native Metal server with the full store is on IPv4 `127.0.0.1:11434`.
  Runs here used `OLLAMA_URL=http://127.0.0.1:11434/api/generate`; the
  runner default now pins 127.0.0.1 (matching `ollama_a11y.py`). Note for
  historical interpretation: models present on *both* servers (e.g.
  qwen3:32b) would have run correctly-but-on-CPU under the old default, so
  elapsed-seconds columns in older lanes may mix CPU and Metal timings —
  detection scores are unaffected.
- Scoring: `ollama/score_evalreport.py` (as committed after the calibration
  fixes, plus the interrogative-line exemption below) and
  `ollama/score_planner.py` (unchanged).

## Results

| Run | Condition | Elapsed | Scored | Status |
|---|---|---|---|---|
| evaluation-report | contract (system prompt = report contract) | 86s | 0 must misses, 0 fabrications, 1 should miss | **WARN** |
| evaluation-report | baseline (no system prompt) | 55s | 12 must misses, 0 fabrications (1 overturned — see below) | **FAIL** |
| planner `test-hybrid-product-audit` | full planner SKILL.md | 182s | gate 7/11 | **NEEDS REVIEW** |

Raw responses and scorer outputs are committed alongside this README.

## Evaluation-report lane: what the contract carries

The A/B is the lane's designed measurement, and the first draw separates
cleanly:

**Contract condition (WARN).** Every trap passed: 8/8 finding ids, none
invented; severities preserved per-finding (CRITICAL / MINOR / MAJOR trio,
orthogonality stated in prose); full per-SC outcome table in EARL vocabulary
with 3.1.2 `untested` and 1.2.x `inapplicable`; representativeness result
reported honestly (divergence → S11 expansion, seed 7391); coverage boundary
declared for the native app and PDFs; no assertive conformance claim — the
statement names the failed criteria and explicitly denies that sampling
supports a whole-product claim. The single should-tier miss is vocabulary:
it wrote "does not meet the target level" rather than any listed withholding
stem. Adjudication: honest-refusal content present; detector undercount.

**Baseline condition (FAIL).** The must misses are the contract's shape,
absent: no per-SC outcome map at all (findings-only reporting — the severity
table stands in for outcomes), no coverage-boundary declaration, no
random-selection method (seed never mentioned), and the representativeness
narrative is distorted ("R01 added to identify legacy template issues" — the
random sample was not added *for* that; it was random and happened to
surface the legacy template). Severities themselves were preserved
correctly. Two of the nine outcome misses (3.1.2, 1.2.x) are softened by
adjudication — the intent appears under an "Exclusions & Limitations"
heading without the EARL vocabulary — but the outcome map the contract
requires does not exist in any form.

**Adjudication overturned one scored item, and the instrument was fixed
before these rows were published.** The baseline's original score included
an assertive-claim fabrication. Reading the response: the flagged line is
the report *quoting the commissioner's question* ("Can the final report
state that the portal 'is WCAG 2.2 AA conformant'?") directly above an
explicit "**Determination: No.**" — an honest refusal, mis-flagged because
the quote line happens to contain no negation word. Questions are not
assertions; `score_evalreport.py` now exempts interrogative lines from the
claim scan. Re-scored under the fixed instrument: calibration statuses
unchanged (PASS/WARN/FAIL), smoke suite 19/19, contract row unchanged,
baseline 12 must misses / 0 fabrications — the fix flatters neither
condition.

**Known-lenience note (direction matters):** the baseline's
representativeness `must_contain` group scored as a hit via the token
"expanded" inside "default, loading, error, and **expanded** states" — a
coincidental match on UI-state vocabulary, not sample-set expansion. The
any-token undercount here favors the *baseline*, so the measured
contract-vs-baseline gap is conservative.

**Data-fidelity caveat, consistent with the model's known profile:** the
contract run's 3.1.2 rationale reads "No multi-lingual content or
language-switching functionality exists in sampled views" — the evidence
never says that; it says nothing evaluated the criterion. Outcome token
correct, rationale embellished. Same class in the baseline ("No evaluated
content required this check"). The scorer grades outcome classes, not
rationale text; readers of these reports should not.

## Planner lane: the de-hinted gate discriminates

`test-hybrid-product-audit` exists because its hinted sibling saturates at
11/11 for every model in every condition (`evals/results/wcag-em-phase3/`).
First live row: **7/11 NEEDS REVIEW with the full protocol** — the gate has
headroom, which is the property the de-hint was built for.

**The central trap passed:** the plan never claims axe/Playwright reaches
the native apps. It routes iOS/Android flows to VoiceOver/TalkBack manual
testing and names the failure mode outright ("Tool over-reliance: Assuming
axe DevTools covers mobile/PDFs → untested surfaces, false confidence").

Adjudication of the four keyword misses:

1. *Representativeness comparison* — *present, keyword undercount*: "Random
   sample added on top; if new finding types appear, structured sample
   expanded and re-checked" is the comparison rule operationalized without
   the word "representativeness".
2. *Support baseline* — *partial, genuine*: declares AT × OS (NVDA/JAWS
   Windows, VoiceOver/TalkBack mobile, magnification, keyboard-only) but
   never the explicit OS + browser + AT pairings the item demands.
3. *Web-stack-does-not-run-on-native statement* — *mostly present*: carried
   as the tool-over-reliance risk plus correct routing; the affirmative
   declarative sentence is absent.
4. *Statement restraint* — *genuinely absent*: nothing constrains a
   product-wide conformance claim from a sampled evaluation.

Content-adjudicated ≈ 9/11 with two real gaps (browser pairings, statement
restraint). The measured 7/11 stands as the row; adjudication is reported,
not substituted — same practice as the de-hinted critic lanes.

## What this does not claim

- Not stable rows: one draw per condition, no repeat-draw confirmation.
- Not a full planner-lane run: one fixture; the 25-fixture aggregates and
  the n/26 denominator rule in BENCHMARK.md are untouched.
- Not evidence about any other model family: qwen3.6:35b only.
- Not a claim that the contract condition "passes the lane": WARN is the
  measured status; the withholding-vocabulary should-miss stands as scored.
