<!-- GT-16 bench-reviewer gate on fixture revision 2 (df05648), model=opus, 2026-09-03. Verbatim; recovered from the agent's session transcript. Read-only pass over the pair, rubrics, canaries, prompts, score_output.check_finding, and the rev1 gate report. -->

# GT-16 bench-reviewer gate — fixture revision 2 (`df05648`)

## Predictions (pre-read) — confirm/refute

| # | Prediction | Result |
|---|---|---|
| P1 | The `useEffect`-cleanup focus repair is still wrong on some route | **REFUTED.** The repair is correct on all four routes, and correct for a subtle reason the authors got right. See "Focus-return repair" below. |
| P2 | StrictMode dev double-invoke produces a spurious restore nobody documented | **REFUTED.** mount→cleanup→mount ends with focus on Cancel: the cleanup's `.focus()` fires while `#app-root` is still `inert` (dialog open), so it is a no-op, and the re-run re-focuses Cancel. Dev-only and harmless. |
| P3 | A line citation drifted in the repair round | **REFUTED.** All 41 citations across both metadata files, both rubrics, the BUG answer key and `canaries.py` resolve exactly. rev1's m-4 (`:230`) is fixed. |
| P4 | The two components are no longer byte-identical | **REFUTED.** JSX md5 `2890b04a…`, CSS md5 `ff889a3e…` — identical. |
| P5 | rev1 M-3 (blind leakage) only partially fixed | **PARTIALLY CONFIRMED.** The three pre-argued traps are gone; one residual sentence now maps onto the *new* trap 5. See m-2. |
| P6 | `check_finding` credits a ratifying review via an out-of-sense withdrawal token | **CONFIRMED, and wider than the docs admit.** Three probes, three PASSes. See **C-1**. |
| P7 | `ACCEPT-WITH-RESERVATIONS` misparses | **REFUTED.** `Verdict correct: YES | Status: PASS`. rev1 m-1 is now documented consistently. |
| P8 | New CLEAN trap 7 penalises a defensible reviewer | **CONFIRMED, but not on the axis I guessed** — not the PASS-row scope, the operation-ID provenance. See **M-1**. |
| P9 | `claim_boundary` internally inconsistent / implausible as harness output | **CONFIRMED.** See **M-1**. |

---

## VERDICT: REVISE

Narrow. rev1's killer (C-1) is **fully and correctly repaired** — this is materially better work than rev1, and none of the fixture craft should be redone. Two items block: the scorer still passes the review class the lane exists to reject, at a phrasing that is not exotic but *modal*; and the repair that closed rev1 M-4 introduced an undeclared false-alarm penalty on the CLEAN half.

---

## Focus-return repair — verified correct

`fixtures/dialog-dismiss-recipe.md:56-61` (identical at `-clean.md:56-61`). The comment at `:58-59` is accurate, and so is the counterfactual the rubric states at `rubrics/dialog-dismiss-recipe.rubric.yaml:121`.

Mechanism, React 18.3, one commit from `setConfirming(null)`:

1. `recursivelyTraverseMutationEffects` on the Fragment fiber processes `parentFiber.deletions` **first** — the dialog subtree. `commitDeletionEffectsOnFiber` calls only `HookInsertion` and `HookLayout` destroys synchronously. **Passive (`useEffect`) destroys are explicitly not called here.**
2. It then iterates children, reaching `#app-root`'s `HostComponent` `Update` flag → `commitUpdate` removes the `inert` attribute (`inert={confirming ? '' : undefined}`, `:17`).
3. Layout phase.
4. `flushPassiveEffects` (scheduled `NormalSchedulerPriority`) runs the deleted subtree's passive destroy → `returnFocusRef.current?.focus()`, with `inert` already gone.

So the cleanup is guaranteed to run after the `inert` removal in the same commit, and focus lands on the trigger on **all four routes** (Escape `:64-68`, Cancel `:41`, close button `:95`, Delete `:42-45`) — all funnel through `setConfirming(null)`. `[returnFocusRef]` is a stable `useRef` object, so no spurious re-runs.

The non-obvious part the authors got right: a `useLayoutEffect` cleanup **would** be broken, because deletions are processed before the sibling root's attribute update. `:121` states exactly that. Nothing left lands on `<body>` except a sub-frame interval before the passive flush, which `toBeFocused()` auto-retries through and which trap 5 correctly declares a false alarm.

CLEAN `-clean.md:224` (trace step 3, `focus_after: "Delete report"`, `dialog_open_after: false`) and the 2.4.3 PASS row `:255-264` are now reproducible from their own subject. **rev1 C-1 is closed.**

---

## Findings

### CRITICAL

**C-1 — The BUG scorer still gives `Status: PASS` to a review that ratifies the FAIL and blames the component. Three of the seven generic tokens in withdrawal group 3 are ordinary negative-capability vocabulary.**
`rubrics/dialog-dismiss-recipe.rubric.yaml:51` (dup at `fixtures/dialog-dismiss-recipe.metadata.yaml:34`) + `ollama/score_output.py:110-115` (`group_ok` is a bare lowercased substring test; no negation handling, no per-finding scoping).

Group 3 contains `"unsupported"`, `"not supported"`, `"does not support"`, `"doesn't support"`, `"spurious"`, `"misattributed"`, `"mis-attributed"` — none of which are withdrawal-directed. Three probes I ran against the shipped scorer and rubric:

| Probe | Ratifying review | Firing token | Scored |
|---|---|---|---|
| P1a | *"the dialog **does not support** keyboard access to its close control … The component must add the close button to the focus trap. The FAIL stands as filed."* | `does not support` | must **1/1**, **Status: PASS** |
| P1b | *"aria-label over an aria-hidden svg, which is **unsupported** in older assistive technology … Ratify the 2.1.1 FAIL and fix the component."* | `unsupported` | must **1/1**, **Status: PASS** |
| P1c | *"confirmed genuine, **not spurious** … The filed FAIL is correct."* | `spurious` | must **1/1**, **Status: PASS** |

P1c is a polarity inversion: the review asserts the negation of the token and is credited for it.

This is not the disclosed residual. `README.md:101-103`, `metadata:105-107` and `rubric:122` all describe it as *"a ratifying review that also uses a withdrawal token in another sense — adjudicate by hand,"* which reads as a rare accident. In fact "the component does not support keyboard access to X" is the **modal phrasing** for a ratifying review of a keyboard FAIL. All three probes also carry `has-text` (group 1) and `aria-label` (group 2) simply by quoting the fixture, so both other groups are free.

Consequence: the headline BUG must-find rate is inflated by an unknown share of ratifying draws, in the direction that makes both conditions look better than they are — and `README.md:96-100`'s claim that the conjunction makes *"a review that ratifies the FAIL with a getByRole 'nit' … score 0/1"* holds only for canary B's specific wording, exactly the artifact-of-canary-authorship problem rev1 C-2 named.

Cheap fix, no re-authoring: delete the five bare tokens from group 3 (`unsupported`, `not supported`, `does not support`, `doesn't support`, `spurious`), keeping the finding-directed multiword forms already present (`the finding is invalid`, `cannot be filed`, `instrument artifact`, `not a component defect`, `withdraw`, `retract`, `false fail`, `misattributed`). Then add P1a as a canary. Re-verified: all six BUG canaries still pass under that trim, because `correct` (`canaries.py:80-89`) matches on `withdrawn` and `D` (`:70-79`) on `must be withdrawn`.

**Rev1 C-2 is therefore partially resolved:** the two sub-defects that *were* fixed are real wins — the `should_find` `keywords_any: ["false","artifact","instrument"]` free-credit hole is gone (replaced by `keywords_all` `[["trace"],["step 2"…]]` at `:61-63`, and canary C now forbids the credit), and probe D's under-crediting is fixed. The polarity hole itself is narrowed, not closed.

### MAJOR

**M-1 — The `claim_boundary` operation IDs have no provenance in the fixture or the slice, and a reviewer who says so is scored FALSE ALARM on the CLEAN half.**
`-clean.md:249` and `:259` (dup at BUG `:275`); traps at `-clean.rubric.yaml:81-83`.

Both PASS rows declare `operation OP-CLOSE-REACH` / `OP-CLOSE-DISMISS`. `findings.json` is captioned *"filed by the harness from the assertions that ran"* (`:241`), but neither identifier appears anywhere in the recipe (`:164-201`), and `grep -i "claim_boundary\|operation"` over `prompts/system-recipe-slice.md` returns **zero hits** — the verification-evidence-contract slice the model is given never defines the field or the operation vocabulary. So the harness has no source for these IDs, and the model has no basis to accept them.

Probe P5 — a `MINOR` note saying exactly that, with correct citations:
`Verdict: REVISE (expected: ACCEPT or ACCEPT-WITH-RESERVATIONS) | Verdict correct: NO — FALSE ALARM | Status: FAIL`

Trap 7 covers *"reads the rows as 'this dialog conforms to 2.1.1'"*. It does **not** cover *"the operation IDs are unverifiable"*, so this isn't even a declared judgment call. This is the rev1-M-4 repair introducing a new defect — milder than rev1 C-1 (a realism/provenance gap, not a behavioural contradiction), but the same class: the CLEAN half asserting something its own materials cannot support.

Two clean exits: declare the operation IDs in the recipe (a comment above each assertion, which also satisfies the BUG rubric's own `nice_to_find` #2 on selector provenance, `rubric:74-75`), or add an eighth trap naming the provenance question as out of scope.

Related, same root: `-clean.rubric.yaml:98` claims the skill condition is steered *"onto the `claim_boundary` fields"* by the slice. The slice contains no such content. That reasoning line is unsupported.

### MINOR

**m-1 — The rubric prescribes a credit reduction the scorer cannot apply.** `rubric:66`: *"credit is reduced if the review withdraws the FAIL but then certifies the dialog."* Probe P7 (correct diagnosis + *"the dialog PASSES 2.1.1 … and can be certified conformant"*) scores must **1/1**, should **1/1**, **Status: PASS** — full credit. It is covered by `known_judgment_calls:120` for hand adjudication, so this is a rubric/scorer mismatch, not a scoring error; but `:66` reads as a machine rule and isn't one.

**m-2 — `## Expected Behavior` still pre-argues half of the new trap 5.** `dialog-dismiss-recipe.md:287` / `-clean.md:271`: *"On dismissal by any route, focus returns to the **Delete report** trigger."* Above the cut line in both prompts. Trap 5 (`-clean.rubric.yaml:75`) declares *"focus return from the effect cleanup is correct, not a race"* a false-positive trap; this sentence asserts the conclusion. Mitigating, and why this is MINOR not MAJOR: rev1's three pre-arguments (inert root, initial focus, three-control cycle) are genuinely gone, `Expected Behavior` is legitimately a spec section a reviewer checks the implementation against, and the sentence states the *outcome* while trap 5 is about the *mechanism* — canary E (`canaries.py:102-107`) shows the trap still fires despite it. **rev1 M-3 is mostly resolved.**

**m-3 — The slice prescribes `setTimeout(0)` for focus-after-unmount; recommending it is an undeclared false alarm that only the skill condition can hit.** `prompts/system-recipe-slice.md:92`. Probe P6 (a review applying that rule to `:60`) → `FALSE ALARM | Status: FAIL`. The slice self-scopes to React 16 and the fixture is React 18.3, so a careful model won't misapply it — and `known_judgment_calls` (`rubric:121`, `-clean.rubric.yaml:110`) covers `flushSync` and layout-cleanup preferences in spirit. But it names neither `setTimeout`, and this is the residual of rev1 C-1's contamination point 3: it still biases the A/B against the skill condition. One clause in the judgment-call list closes it.

**m-4 — The blind prompts are offset +2 from the fixtures, and the rubric's line-number keywords are fixture-relative.** `prompts/*.blind.md:1` is the task prefix, `:2` blank, so `## Run Output` sits at prompt `:204`/`:206` vs fixture `:202`/`:204` (bodies otherwise byte-identical above the cut — verified by diff). The task prefix asks for `filename.md:<line>` citations; the `should_find` any-of group (`rubric:63`) contains `":245"`, `":248"`, `"line 245"`, `"line 248"`. Low practical impact — models cannot count lines in an ungutter'd prompt anyway, and the same group carries `"step 2"`/`"second press"`, which is what a model will actually write. But hand adjudication of any draw's line citations must subtract 2, and that is written down nowhere.

### OBSERVATION — what checked out clean

Everything rev1 praised still holds and was re-derived, not assumed: Tab order from `querySelectorAll` DOM order `[Close dialog, Cancel, Delete]` plus the wrap logic reproduces the BUG trace `:243-249` exactly (Close dialog on presses 2 and 5); the CLEAN trace's two-Tab loop exit is correct against `for (i<6 && !reached)`. Both spec-file line mappings are right — BUG `:9`/`:30` and the new multi-line code frame `28|29|>30|31|32` (`:229-235`) all count out against the recipe block, and CLEAN's `:9`/`:32`/`:35-36` do too. `dialog.getByRole('button', {name:'Close dialog', exact:true})` resolves; `p:has-text("cannot be undone")` resolves uniquely and is tag-scoped as Playwright's docs advise.

Repaired and verified: census now in DOM order in both halves (heading before close button, `:257-262` / `:232-237`); the paragraph row carries `text`, not `name`; the settle is 250 ms, inside the slice's stated `waitForTimeout(200–500)` at `slice:90`, and trap 6 quotes that range accurately; trap 2's garbled sentence now completes identically in both metadata `:46` and rubric `:67`; every canary evidence cite resolves. `canaries.py` runs 9/9, `EXIT=0`, reproduced.

---

## rev1 finding-by-finding resolution

| rev1 | Status | Evidence |
|---|---|---|
| **C-1** focus-return defect; CLEAN asserts impossible behaviour | **RESOLVED** | `md:56-61`; passive-destroy ordering verified; `-clean.md:224`, `:255-264` now reproducible |
| **C-2** scorer PASSes a ratifying review | **PARTIAL** → **C-1 (new)** | should-find free-credit and probe-D under-crediting fixed; polarity hole narrowed, not closed — P1a/b/c PASS |
| **M-1** canaries miss the classes that break | **RESOLVED** (one gap) | 9 cases incl. A–E, 9/9 pass; no canary for the P1a class |
| **M-2** census contradicts DOM order | **RESOLVED** | `:257-262` / `:232-237` |
| **M-3** Expected Behavior pre-argues 3 traps | **MOSTLY RESOLVED** → **m-2** | three removed; focus-return sentence residual |
| **M-4** CLEAN files criterion-level 2.1.1 PASS | **RESOLVED** → **M-1 (new)** | `claim_boundary` + trap 7; repair introduced the provenance gap |
| **m-1** `ACCEPT-WITH-RESERVATIONS` undocumented | **RESOLVED** | `metadata:73-75`, `rubric:108`; P4 scores `PASS` |
| **m-2** 100 ms settle below slice range | **RESOLVED** | `:193` = 250 ms; trap 6 text updated |
| **m-3** garbled trap 2 wording | **RESOLVED** | metadata `:46` = rubric `:67` |
| **m-4** canary cite `:230` | **RESOLVED** | all canary cites resolve |
| **m-5** paragraph given accessible `name` | **RESOLVED** | `"text"` in both |
| **m-6** single-line code frame | **RESOLVED** | `:229-235`, spec lines correct |

**New defects from the repair round:** M-1 (from the M-4 repair), m-3 (residual of C-1's contamination), plus the unsupported reasoning claim at `-clean.rubric.yaml:98`.

---

## What I did NOT check

- Did not execute the component or run React. The focus-repair verdict is a static reading of React 18.3's commit order (`recursivelyTraverseMutationEffects` deletion-first, passive destroys deferred to `flushPassiveEffects`). Confidence ~90%; falsification is the same one-line browser test rev1 named.
- Did not read any draw outputs, the results README, or `claude-baseline-clean-opus-rev1.md`, per instruction.
- Did not read `run_benchmark.py` — `RECIPE_SLICES`, fixture registration, and `ANSWER_KEY_RE` are unverified. I verified prompt/fixture body identity by diff instead.
- Read `score_output.py` only around `check_finding` (`:91-122`) and the head of `count_false_positives`. The composite-score formula, the 0.4 abort threshold, threshold application, and whether `evidence_quality` / `format_compliance` are implemented at all remain unaudited — both rubrics declare those two dimensions and I did not confirm the scorer reads them. Likewise `nice_to_find` (2 items BUG, 3 CLEAN) carries no keywords in either rubric; whether it is scorable, and whether it deflates the composite denominator, is unchecked.
- Did not verify the Playwright doc quotations at `README.md:26-32` / `metadata:66-74` against playwright.dev.
- Did not cross-check this suite's metadata schema against the other suites, or run `scripts/validate_fixtures.py` (issue #25 territory).
- Did not test scorer behaviour on thinking-tagged or truncated responses.

---

## Provenance

Read (all under `/Users/AlexUA_1/claude/accessibility-skills-gt16`, commit `df05648`):

1. `evals/results/gt16-dialog-dismiss-recipe/bench-reviewer-gate-opus-rev1.md`
2. `evals/suites/a11y-test-recipe/README.md`
3. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe.md`
4. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe.metadata.yaml`
5. `evals/suites/a11y-test-recipe/rubrics/dialog-dismiss-recipe.rubric.yaml`
6. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe-clean.md`
7. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe-clean.metadata.yaml`
8. `evals/suites/a11y-test-recipe/rubrics/dialog-dismiss-recipe-clean.rubric.yaml`
9. `evals/results/gt16-dialog-dismiss-recipe/canaries.py`
10. `evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe.blind.md` (headings, head 1-12, tail, full-body diff vs fixture)
11. `evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe-clean.blind.md` (same)
12. `evals/results/gt16-dialog-dismiss-recipe/prompts/system-recipe-slice.md` (headings + targeted greps: settle range, setTimeout/unmount, claim_boundary, operation, aria-label checks)
13. `ollama/score_output.py:80-175` (`check_finding`, head of `count_false_positives`)

Commands run (read-only w.r.t. the worktree): `git log`, `ls`, `sed`, `grep`, `diff`, `md5` on the two fixtures' JSX/CSS blocks, `python3 evals/results/gt16-dialog-dismiss-recipe/canaries.py` (exit 0, 9/9 ok), and two probe scripts written to and run from `/tmp/gt16rev2/` only. No file in the worktree was created, edited, or committed; no agents spawned; nothing under `evals/results/gt16-dialog-dismiss-recipe/` read beyond `canaries.py`, `prompts/`, and the rev1 gate report.