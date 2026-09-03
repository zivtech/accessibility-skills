# GT-16 — `:has-text()` vs accessible names: fixture-first pair, receipts

Wave-2 gotcha lead GT-16 (`docs/plans/2026-09-02-promotion-candidate-dispositions.md`
line 141): a keyboard recipe that derives a selector from a control's visible
label — `button:has-text("Close")` — cannot resolve an icon-only control whose
name is `aria-label`, because Playwright's `:has-text()` matches rendered text
content, not accessible names. The disposition withdrew a one-sentence skill
fold and asked for a BUG/CLEAN pair first. This directory is the pair's
measurement: one bench-reviewer gate per revision, four blind opus draws per
revision (BUG/CLEAN × skill-slice/baseline), all verbatim.

Suite: `evals/suites/a11y-test-recipe/` (new; README there explains the shape
and why it is not the operation-evidence lane). Scorer: `ollama/score_output.py`
with the explicit-keyword fields added for this lane.

## Headline

| Cell | rev1 (`cbd2f41`) | rev2 (`df05648`) |
|---|---|---|
| BUG · recipe-skill | died (API 529) | **REVISE, PASS** — must 1/1, should 1/1 |
| BUG · baseline | died (API 529) | **REVISE, PASS** — must 1/1, should 1/1 |
| CLEAN · recipe-skill | died (API 529) | **ACCEPT, PASS** — 0 findings above ENHANCEMENT |
| CLEAN · baseline | **REVISE — correctly**: found the unplanted defect | **ACCEPT, PASS** — 2 MINOR, 3 ENHANCEMENT |
| bench-reviewer gate | REVISE (2 CRITICAL, 4 MAJOR, 6 MINOR) | see below |

Every rev2 BUG draw withdrew the filed 2.1.1 FAIL and named the role/name
remedy; neither blamed the component. Every rev2 CLEAN draw ACCEPTed and
declined every declared trap. One opus draw per cell on one day — the same
caveat as the sibling wave: not a calibration, not a local-model row.

## The A/B

Not a detection difference. Both BUG conditions found the selector defect and
the trace contradiction from the call log and `trace.json` alone; nothing in
the skill slice names selector semantics, and the baseline did not need it.
What the slice changed is the *framing*: the skill-condition BUG draw filed
"a test-authoring fault emitted a canonical pass/fail result" as its own MAJOR,
straight from the slice's detector-lane authority boundary (an infrastructure
limit is an abort, not an outcome), and the skill-condition CLEAN draw walked
the slice's own React-16 `setTimeout(0)` focus-after-unmount note and said why
it does not apply to a passive-cleanup return. The baseline CLEAN draw reached
the same conclusion by reasoning about React 18 commit phases unprompted.

So the sentence the disposition withdrew — derive selectors from the
accessible-name inventory / `getByRole` — is not what these four draws needed.
What the pair *does* establish is the reproduction clause 1 requires, and the
CLEAN half's seven traps establish what the sentence must not say: `:has-text()`
on a text-bearing element is correct, and a reviewer who has learned the rule
must not apply it as lint.

## What the measurement found in the instrument (rev1 → rev2)

The rev1 pair shipped with a **real defect in the byte-identical component**,
caught before any row was published — by the blind CLEAN baseline draw
(`claude-baseline-clean-opus-rev1.md`, MAJOR ×2) and, independently, by the
gate (`bench-reviewer-gate-opus-rev1.md`, C-1):

1. **Focus return was a no-op.** `finish()` called `setConfirming(null)` and
   then `triggerRef.current.focus()` in the same handler. React 18 flushes the
   state update after the handler returns, so `#app-root` still carried
   `inert` when `.focus()` ran; inert elements are not focusable, the dialog
   then unmounted, and focus fell to `<body>` on every dismissal route. The
   CLEAN half's `trace.json` step 3 and its 2.4.3 PASS row recorded behaviour
   the component could not produce. rev2 restores focus from the dialog's
   passive `useEffect` cleanup, which runs after the commit that removes
   `inert` (a layout cleanup would not: React processes the dialog's deletion
   before the sibling root's attribute update).
2. **The census was out of DOM order** — close button listed before the
   heading. Both halves. The artifact the lane calls "the accessible-name
   inventory" was wrong about reading order.
3. **The scorer passed a review that reached the opposite conclusion** (gate
   C-2, four executed probes). With the must-find and the withdraw-the-FAIL
   item as separate rows, a review that ratified the FAIL and added a
   `getByRole` "nit" scored must 1/1 → PASS under the 0.4 abort threshold;
   a wrong-diagnosis review phrased with "text content" also passed; a
   correct review that never typed the literal `has-text` failed. rev2 makes
   `keywords_all` entries any-of *groups*, so the single must-find requires
   semantics AND remedy AND withdrawal. `canaries.py` now carries the gate's
   probes A–E; 9/9.
4. **Expected Behavior pre-argued three of four traps** (gate M-3): it stated
   the root is inert, that focus lands on Cancel as the least destructive
   action, and that Tab cycles three controls — the exact reasoning the
   false-positive dimension is supposed to measure. Removed. This is the
   #51 class one level down from the "Accessibility Features Present"
   section: a narrator's prose above the cut line is a features section
   without the heading.
5. **The CLEAN half filed a 2.1.1 conformance PASS from one control** (gate
   M-4), which the repo's own detector-authority doctrine calls an overclaim.
   rev2 rows carry a `claim_boundary` naming the operation, route and
   viewport and disclaiming a criterion verdict — and the CLEAN baseline
   rev2 draw immediately pointed out (MINOR 1) that the boundary names a
   viewport no artifact records. Fair; carried as an open item below.
6. Smaller: 100 ms settle below the slice's own 200–500 ms range (now 250);
   the second PASS row cited one assertion for a two-part claim (now both);
   a census paragraph row carried a `name` (now `text`); `FOCUSABLE` admitted
   disabled inputs; a garbled trap-2 sentence; a canary citation off by
   five lines.

The wave's rule held again: **a repair round is a new authoring round.** Every
rev2 citation in both metadata files, both rubrics, the answer key and the
canaries was re-derived from the rev2 line map and spot-checked, and the gate
was re-run on rev2 rather than trusted from rev1.

## Trap adjudication (rev2, by hand)

| Trap | BUG·skill | BUG·base | CLEAN·skill | CLEAN·base |
|---|---|---|---|---|
| icon-only `aria-label` close button is correct | held | held | held (named as a bait declined) | held |
| inert "Close account" is not a defect | held | held | held | held |
| initial focus on Cancel; cleanup focus return | held | held (M4 asks for a test of the ordering — fair, not a flag) | held (declined the React-16 note) | held (reasoned the passive phase) |
| six-press bound not the defect | held | held | held | held |
| `p:has-text` on a text-bearing paragraph | — | — | held | held |
| `exact: true` deliberate | — | — | held | held |
| PASS rows operation-scoped | — | — | held (ENHANCEMENT: dual-cite 2.1.1) | held (MINOR: viewport unrecorded) |

Tiering observations, not trap hits: both BUG draws filed the recipe's missing
Escape/Cancel coverage as MAJOR or ENHANCEMENT (the rubric lists it as
nice-to-find); the BUG baseline filed "severity from criterion weight, not
user impact" (M3) — the repo's orthogonality rule applied to the harness's
own row — and "the 500 ms assertion timeout is arbitrary" (N3), both
reasonable on the BUG half's defective artifact.

## Scores (rev2, `score_output.py` against the rev2 rubrics)

```
claude-recipe-skill-bug-opus-rev2    Verdict REVISE  must 1/1  should 1/1  PASS
claude-baseline-bug-opus-rev2        Verdict REVISE  must 1/1  should 1/1  PASS
claude-recipe-skill-clean-opus-rev2  Verdict ACCEPT  structured findings 0  PASS
claude-baseline-clean-opus-rev2      Verdict ACCEPT  structured findings 0  PASS
```

## Open items carried out of this measurement

- **`claim_boundary` names a viewport the rows do not record** (CLEAN baseline
  rev2, MINOR 1). The a11y-test evidence contract should say which fields a
  boundary may reference — the fix is on the contract side, not this fixture.
- **Three rev1 draws and the first gate died on API 529 with no partial
  output** (transcripts checked before re-dispatch). Recorded so the cell
  table is honest about what rev1 measured: one draw and one gate.
- The BUG halves' `selector` field carries the recipe's locator, not the
  failing element's stable selector (both BUG draws, M2/M7). True of the
  artifact by design — it is the defective run — but the bug-reporting skill's
  stable-selector rule is the reference if a fixture ever models the
  *corrected* filing.

## Files

```
bench-reviewer-gate-opus-rev1.md          gate on cbd2f41 — REVISE (C-1 focus return, C-2 scorer, M-1..M-4, m-1..m-6)
bench-reviewer-gate-opus-rev2.md          gate on df05648 (added when it lands)
claude-baseline-clean-opus-rev1.md        the draw that found the rev1 defect (REVISE, correctly)
claude-recipe-skill-bug-opus-rev2.md      claude-baseline-bug-opus-rev2.md
claude-recipe-skill-clean-opus-rev2.md    claude-baseline-clean-opus-rev2.md
canaries.py                               scorer discrimination, 9 cases incl. the gate's probes A–E (exit 0 = CLEAN)
prompts/                                  exactly what each draw read: *.blind.md (rev2) + system-recipe-slice.md
```

Draw protocol: `general-purpose` opus subagents, one per cell; the skill
condition reads `prompts/system-recipe-slice.md` first as its procedure, the
baseline reads only the prompt file; both are forbidden any other file, tool,
or search and end with a Provenance section. Reports are recovered verbatim
from each agent's session transcript.

## Not established here

Not a local-model row (no qwen/gemma cell yet; the lane is wired for
`run_benchmark.py recipe` / `recipe-baseline`). Not a multi-draw variance
characterisation. Not evidence about `:has-text()` on text-bearing targets
beyond the one CLEAN trap. Not a Playwright execution — the run outputs are
authored to Playwright's message shapes, not captured. And not the skill
sentence: this PR lands the reproduction, not the rule.
