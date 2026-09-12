# Stage-A pilot results — qwen detector-step pipeline

**Date:** 2026-09-12 · **Verdict: KILL the cost-saving pipeline (Design 1).**

Judge = `a11y-critic` (Opus) run in-session on the subscription (no metered API).
2 fixtures × 2 arms × 1 draw. Underpowered per the design's own rule (wants
≥3 draws, more fixtures) — but the signal is clean, consistent, and matches the
proposal-critic's predicted structural failure, so it stands as a strong
preliminary kill.

## M0 — value-add (accordion-no-region-role, HAS-BUGS)

| Finding | Blind | With candidates |
|---|---|---|
| Missing `role="region"` + label (the planted bug) | MAJOR | MAJOR |
| Missing heading wrappers (1.3.1) | MAJOR | MINOR |
| Broken `aria-controls` ref | MINOR | MINOR |
| Verdict | REVISE | REVISE |

Same three findings both ways. The candidate list surfaced **nothing the blind
judge missed** (only a severity wording shift). The blind judge caught the
planted region-role bug on its own. **Value-add ≈ 0.**

The with-candidates arm did adjudicate qwen's leads well (c2 + c3 CONFIRMED as
the real issues; c1/c4/c5 REJECTED) — but every confirmed lead was already in
the blind arm's findings.

## M3 — anchoring (button-skip-link-clean, CLEAN)

| | Blind | With candidates |
|---|---|---|
| Verdict | ACCEPT | ACCEPT |
| Findings | none | none |
| qwen leads | — | all 5 REJECTED with sound reasons |

**No anchoring.** The candidate list did not push the judge to confirm any
non-bug. The judge independently rejected all 5 (skip-link pattern correct,
focus ring perceptible, footer contrast ~5.3:1 passes, focus-target hardening
optional, list-semantics mitigated by the nav landmark).

## M1 — cost direction (coarse; total agent tokens, not a clean in/out split)

| Arm | Blind | With candidates |
|---|---|---|
| accordion | 81,426 | 81,485 |
| clean | 82,184 | 84,279 |

With-candidates ≈ blind, trending **higher** (candidates add input; the judge
does the same work). No saving.

## Why (the structural reason)

To protect the detector-not-verdict rule, the hosted judge must investigate
independently and verify every candidate. So it finds the real issues with or
without the list, and the list is pure added input cost. Cost saving and the
safety rule are in direct tension (proposal-critic CRITICAL #2), and the safety
rule wins by design — which leaves no room for the saving.

## Recommendation

- **Shelve Design 1** (candidate-fed cost-saving pipeline). The value
  proposition does not survive first contact.
- **Design 2** (qwen as a recall net catching judge misses) is also unsupported
  here: the blind judge missed nothing, so there was nothing to catch.
- **Kept finding:** the hosted a11y-critic is robust unaided — independent
  detection of the planted bug and correct rejection of 8/10 false leads across
  the two fixtures. Reassurance for the existing workflow.
- If revisited: the only version worth testing is a **lighter** judge pass that
  deliberately trusts candidates to skip investigation — but that is precisely
  what detector-not-verdict forbids, so it would need a different safety story.

The Stage-A harness (pre-sort generator, cost accounting, subscription judge
runner) remains in the repo for reproducibility.
