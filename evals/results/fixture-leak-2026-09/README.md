# Fixture Leak Classes 1 and 2 — Measured (2026-09-03)

Two A/B lanes built for [issue #51](https://github.com/zivtech/accessibility-skills/issues/51),
which argued that the critic fixtures hand the model its own answer twice: the
H1 title names the defect (**leak class 1**), and an `## Accessibility Features
Present` section names the non-defects (**leak class 2**). Between them they
bracket the answer key above the blind cut line.

The deterministic half of #51 — one canonical cut-line spelling, a blind-prompt
guard over every suite, a manifest pinning every H1 — shipped in
[#56](https://github.com/zivtech/accessibility-skills/pull/56). This is the
measured half: **how much were those two sections actually worth?**

## Headline

**Neither leak moved a number that reaches significance, and the reason is
worse than the leak.** Removing the answer-key sections does not degrade
detection. What it exposes is that the CLEAN half of the suite was never
carrying the claim it was built to carry.

| Lane | Arms | Result |
|---|---|---|
| **class 1 — H1 title** | titled vs neutral, 9 max-leak BUG fixtures × 5 draws | must-find **150/150 in both arms**. Delta 0. Title echoed in 0 of 90 responses. |
| **class 2 — features section** | withfeatures vs nofeatures, 11 CLEAN × 5 draws + 9 BUG × 3 draws | must-find **89/90 in both arms** (p = 1.0). CLEAN strict-ACCEPT 6/55 vs 2/55 (p = 0.27). |

The number to read is not the delta. It is **6/55**. On the eleven fixtures
whose expected verdict is ACCEPT — the CLEAN halves that exist to prove the
critic does not flag correct code — qwen3.6:35b returned a clean ACCEPT **11%
of the time with the answer key present, and 4% without it.** The features
section was not propping up the CLEAN verdicts. There were no CLEAN verdicts
to prop up.

This is the same conclusion the repo already routes on — *detector, never a
verdict authority* — but measured under an A/B rather than inferred from
single draws.

## What the lanes did

Runner: `ollama/run_benchmark.py {titlehint,featurehint}`, added in
[#56](https://github.com/zivtech/accessibility-skills/pull/56). Model
`qwen3.6:35b`, temperature 0.3, one draw per cell, no retries. Scorers
`ollama/score_titlehint.py` and `ollama/score_featurehint.py`. The arms differ
by exactly one edit to the prompt; nothing else changes.

**Class 1 (titlehint).** The H1 is either left alone or replaced by the
`neutral_title` pinned in `evals/fixture-title-manifest.yaml`. The runner
aborts if the fixture's live H1 does not match the manifest, so the arm cannot
silently drift:

```
titled : # Fixture: Toast Notification Without Alert Role
neutral: # Fixture: Toast Notification
```

Fixtures were the nine maximum-leak candidates, selected by a strict rule:
**every content word the title drops appears verbatim in a `must_find`
description.** If a title can carry the answer anywhere, it is on these nine.
9 × 2 arms × 5 draws = **90 draws**, 300 must-find item checks.

**Class 2 (featurehint).** The `## Accessibility Features Present` section is
either kept or removed by a regex that aborts unless it matches exactly once.
Nothing else is touched. 11 CLEAN × 2 × 5 = 110 measurement draws, plus 9 BUG
× 2 × 3 = 54 control draws. **164 draws**, zero failures, zero truncations.

The CLEAN arm carries the measurement (does removing the list of things that
are fine change the verdict on code that is fine?); the BUG arm is the control
(removing a list of non-defects should not change what defects are found).

## Numbers

Full output in [`stats.txt`](stats.txt), reproducible with
`python3 evals/results/fixture-leak-2026-09/stats.py`.

### Class 2, CLEAN tier (n = 55 per arm)

| verdict | withfeatures | nofeatures |
|---|---|---|
| ACCEPT | 6 | 2 |
| ACCEPT-WITH-RESERVATIONS | 26 | 26 |
| REVISE | 21 | 26 |
| REJECT | 1 | 1 |
| no parseable verdict | 1 | 0 |

| contrast | with | without | Fisher p | observed power |
|---|---|---|---|---|
| strict ACCEPT | 10.9% | 3.6% | 0.27 | 31% |
| ACCEPT + reservations | 58.2% | 50.9% | 0.57 | 12% |
| raised ≥1 structured finding | 10.9% | 20.0% | 0.29 | 26% |

### Class 2, HAS-BUGS tier (n = 27 per arm)

must-find **89/90 in both arms**. The single miss in each arm is
`infinite-scroll-no-announcement` at 3/4 — different draws, so it is draw
variance, not an arm effect. Severity drifts harsher without the section
(REJECT 7 → 10, p = 0.56), which is the direction you would expect if the
section were doing anything at all, but it is one of five contrasts run and
does not survive as a finding.

## Honest limits

**This design could only have caught a 3× swing.** At n = 55 per arm from a
10.9% base, the smallest effect detectable at 80% power is a rise to ~33%.
Observed power on the effect actually seen was 31%. A real features-section
effect of, say, 11% → 20% would have been missed more often than not. **These
are null results at low power, not evidence of absence.** Closing #51's
measurement half on them means accepting that bound, not pretending it away.

**The title lane is pinned to the ceiling.** Both arms found 100% of must-find
items. A ceiling cannot move up, so this lane bounds the title effect from
below only: no detectable effect *on fixtures the model already finds every
time without the title*. It says nothing about titles on harder fixtures — and
the fixtures chosen were, by construction, the ones where the title gave away
the most. The right reading is that these particular defects are so easy the
title is redundant, not that titles never help.

**One model, one temperature.** qwen3.6:35b at 0.3. The repo's own record says
byte-identical prompts flip 2–3 items at this temperature. No hosted row was
drawn on either lane; a leak that a local detector shrugs off could still be
load-bearing for a different model class.

**The lanes measure the consequence, not the mechanism.** #51 argued the
features section is what the `false_positive_trap` rubric dimension actually
scores. That turned out to be unmeasurable, because the dimension is not
scored at all — verified here: `false_positive_trap` is declared in **50 of 50**
critic rubrics and read by **no scorer** (`llm_judge`, `hybrid_weights` and
`scoring_method` likewise; positive control: `must_find` is read by 4 scorers).
So these lanes measure the outcome the trap dimension was supposed to stand
for, directly. Whether to score the declared dimension, or delete it, is
still open.

**Not claimed:** that the fixtures are now leak-free; that the CLEAN halves
should be rewritten; that the features section should be removed from the
fixtures (it is realistic content — a developer handing over a component
really would say what they handled). What *is* claimed is that the section can
be removed without measurable cost to detection, and that its presence is not
what makes the CLEAN verdicts look the way they do.

## Files

```
titlehint/            90 raw responses  (ollama-titlehint-<arm>-<fixture>-qwen36-35b-d<n>-response.json)
featurehint/         164 raw responses  (ollama-featurehint-<arm>-<fixture>-qwen36-35b-d<n>-response.json)
score-titlehint.{txt,json}     per-fixture rates, both arms
score-featurehint.{txt,json}   per-fixture verdicts and finding counts, both arms
stats.py / stats.txt           significance, Wilson intervals, power and MDE
run_titlehint.sh / run_featurehint.sh   the exact draw loops, as run
titlehint-run.log / featurehint-run.log run order and wall-clock timings
```

## Server disclosure

Both lanes ran against a **dedicated Ollama server on `127.0.0.1:11435`**, not
the default `:11434`, which is shared with a background tool on this host.
Draws on the shared port stall. The first attempt at the title lane was
discarded for exactly this reason before the run recorded here; the discarded
artifacts are not committed. Every response in this directory comes from the
dedicated server, sequentially, with no other model loaded.
