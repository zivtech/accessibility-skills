<!-- GT-16 bench-reviewer gate on fixture revision 1 (cbd2f41), model=opus, 2026-09-03. Verbatim; recovered from the agent's session transcript. Read-only pass over the pair, rubrics, canaries, prompts, and score_output.check_finding. -->

## Predictions (pre-read) — confirm/refute

| # | Prediction | Result |
|---|---|---|
| P1 | A line-number citation in metadata/rubrics has drifted | **REFUTED.** All 24 citations across both metadata + both rubrics resolve exactly. So do the derived spec-file line numbers (`spec.js:9`/`:30` in BUG, `:9`/`:32`/`:36` in CLEAN). Only stray: a canary comment cites `:230` for "the dismiss/return step" (`canaries.py:65`) — CLEAN `:230` is a blank line; the step is `:225`. |
| P2 | The CLEAN half carries a real unplanted defect | **CONFIRMED, worse than predicted** — it's in the shared component, so it's in *both* halves. See C-1. |
| P3 | Answer-key leakage above the cut line | **PARTIALLY CONFIRMED.** No verdict/defect leak; both prompts cut cleanly before `## Accessibility Issues`; H1s identical; task prefix condition-neutral with no selector hint. But `## Expected Behavior` pre-argues three of the four declared traps. See M-3. |
| P4 | The two components are not byte-identical | **REFUTED.** JSX md5 `2c3fe706…` and CSS md5 `459fc82e…` match exactly across both files. |
| P5 | A false-positive trap penalises a correct reviewer | **CONFIRMED** (C-1 via probe E; also M-4, m-2). |
| P6 | Keyword sets over-constrain correct phrasings / credit wrong ones | **CONFIRMED in both directions** (C-2, M-1) — four executed probes. |
| P7 | Run output internally inconsistent | **CONFIRMED,** but not where I guessed. Tab order, wrap logic, trace/stdout/findings line numbers, and press counts are all *correct* and mutually consistent. The census reading order and CLEAN trace step 3 are not. See M-2, C-1. |
| P8 | README overclaims | **CONFIRMED** (C-2, C-1). |

---

## VERDICT: REVISE

The fixture *craft* is strong — Tab-order derivation, the six-press bound, the call-log shape, and every cross-artifact line number are right. The lane is not currently sound because (a) a real, flaggable component defect sits in the byte-identical component that both rubrics score as a false alarm, and (b) the scorer gives **PASS to a review that reaches the opposite conclusion from the one the lane exists to measure**.

---

## Findings

### CRITICAL

**C-1 — Both halves share an unplanted, legitimately flaggable focus-return defect; the CLEAN half's run output asserts behaviour the component cannot produce.**
`evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe.md:15-18` (identical at `-clean.md:15-18`):

```js
function finish() {
  setConfirming(null);            // React 18 batches — flush is AFTER this handler returns
  triggerRef.current?.focus();    // runs while #app-root still has inert (:22)
}
```

`finish()` is only ever called from React synthetic handlers (`:45`, `:48`, `:67`). Under React 18 automatic batching the state flush happens after the handler returns, so `.focus()` executes while `#app-root` still carries `inert` (`:22`). Inert elements are not focusable areas, so `HTMLElement.focus()` is a no-op; the dialog then unmounts and `document.activeElement` falls to `<body>`. Focus return is broken for every dismissal route — a genuine 2.4.3 finding, and the exact pattern the system slice's own React-focus-after-unmount note points at.

Consequences, in order of severity:

1. `-clean.md:225` (`trace.json` step 3, `focus_after: { name: "Delete report" }`) and `-clean.md:256-263` (`kbd-dialog-close-dismiss-focus-return`, 2.4.3 **PASS**) record an outcome this component does not produce. The CLEAN half's headline evidence is not reproducible from its own subject.
2. A reviewer who flags it is scored `FALSE ALARM`. Executed probe E against the real scorer:
   `Verdict: REVISE (expected: ACCEPT or ACCEPT-WITH-RESERVATIONS) | Verdict correct: NO — FALSE ALARM | Status: FAIL`
3. The **skill condition steers models into it**: `prompts/system-recipe-slice.md:92` is a bullet about focus-after-unmount requiring a `setTimeout(0)` wrap. A `recipe-skill` draw that applies its own system prompt to `finish()` is penalised; the `baseline-zero-shot` draw is less likely to be. The A/B is contaminated in the direction that makes the skill look worse.
4. It falsifies `README.md:15` ("The component in every fixture here is correct"), `README.md:16-17` ("the rubrics score that as a false alarm"), `dialog-dismiss-recipe.md:298` ("The component has no planted defect"), and `-clean.metadata.yaml:70-71` ("any component finding a reviewer raises here is a false alarm **by construction**").

This is precisely the GT-07 failure the sibling precedent records — *"GT-09 CLEAN carried an unplanted defect … That is the failure a CLEAN half exists to avoid"* (`evals/results/gt-siblings-rows/README.md`, §What the draws found in the instrument).

Confidence ~85%. Falsification test: mount the component in React 18.3 + Chromium, Escape the dialog, read `document.activeElement`. If it is `<body>`, the finding stands. The cheap repairs are `flushSync` around `setConfirming(null)`, moving the focus into a cleanup/effect, or dropping `inert` from the fixture — but note that removing `inert` costs trap 2.

**C-2 — The BUG scorer gives `Status: PASS` to a review that ratifies the false FAIL and blames the component.**
`ollama/score_output.py:91-114` (explicit-keywords branch) + `evals/suites/a11y-test-recipe/rubrics/dialog-dismiss-recipe.rubric.yaml:47-48, 58-59`.

Four probes I ran against the shipped scorer and rubrics:

| Probe | Review | Scored |
|---|---|---|
| **B** | `VERDICT: REVISE` — *"the close control is genuinely not reachable; the component must add the close button to the focus trap. As a nit, prefer getByRole over `button:has-text("Close")`"* | must **1/1**, **Status: PASS** |
| **A** | Wrong diagnosis (scope the selector to the dialog, *"FAIL stands"*), phrased with "text content" | must **1/1**, **Status: PASS** |
| **C** | Ratifies the FAIL, quotes `trace.json`, says *"this is not a false positive"* | should **1/1** credited |
| **D** | Fully correct diagnosis phrased as *"selects by rendered text content, not by accessible name"* — no literal `has-text` token | must **0/1**, **Status: FAIL** |

Three distinct defects:

- **Status is must-find-only.** Probe B ratifies the FAIL, files the wrong component finding, and still passes. The judgment the lane exists to grade — *"is the recorded outcome supported by its own evidence"* (the task prefix's literal question) — is tiered `should_find` (`:54-63`, weight 2) and does not gate the status.
- **`keywords_any` "text content" is shared vocabulary with the wrong diagnosis** (probe A). `README.md:89` claims *"a 'scope the selector to the dialog' review (wrong diagnosis) scores 0/1"*; that holds only for the canary's exact wording (`canaries.py:41-45` avoids the phrase). The claim is an artifact of canary authorship, not a property of the rubric.
- **`should_find.keywords_any` at `:59` contains `"false"`, `"artifact"`, `"instrument"`** — all three fire on ordinary review vocabulary ("false positive", "the trace artifact", "the test instrument", and the `false` literals inside the JSON the model is quoting). Combined with `keywords_all: ["trace"]`, which any review quoting `trace.json` satisfies, the should-find is close to free — probe C earns it while asserting the opposite. **No canary case exercises a should-find negative**; `canaries.py:33-49` asserts only `Must-find issues: 0/1`.
- **`keywords_all: ["has-text"]` under-credits** (probe D) — a correct diagnosis that names the semantics without pasting the literal token scores 0.

`README.md:86-89` and `dialog-dismiss-recipe.metadata.yaml:79-86` both state the explicit fields *fix* the polarity blindness. They narrow it. Probes A/B/C are the counter-examples.

### MAJOR

**M-1 — `canaries.py` does not cover the classes that actually break.** `evals/results/gt16-dialog-dismiss-recipe/canaries.py:32-72`: six cases, all passing (`EXIT=0`, reproduced). Missing: any ratifies-the-FAIL case (probe B), any should-find negative (probe C), any correct-but-differently-worded must-find (probe D), and any CLEAN case that raises the real focus-return defect (probe E). The canaries are the lane's standing proof under `README.md:89` and `rubric:117`; as written they prove less than claimed.

**M-2 — `screen-reader-census.json` reading order contradicts the component's DOM in both halves.** `dialog-dismiss-recipe.md:254-259` (and `-clean.md:233-238`) list `button "Close dialog"` **before** `heading "Delete this report?"`. The JSX at `:94-101` puts `<h2 id="delete-title">` first and the close `<button>` second, inside a flex header that does not reorder. The census is the artifact the whole lane leans on as *"the accessible-name inventory a recipe's selectors should be derived from"* (`README.md:63`) — and it is wrong about order. A reviewer who flags either the reading order (from the census) or the census/DOM disagreement (from both) is correct and is scored as a false alarm.

**M-3 — `## Expected Behavior` pre-argues three of the four declared traps, contradicting the fixture's own blind-envelope claim.** `dialog-dismiss-recipe.md:282-284` states the page *is made inert* (defusing trap 2, rubric `:80-82`), that focus *lands on Cancel, the least destructive action* (trap 3, `:84-86`), and that Tab *cycles through the dialog's three controls* (trap 4's premise, `:88-90`). `dialog-dismiss-recipe.metadata.yaml:74-77` claims *"no 'Accessibility Features Present' section precedes the cut line, so the traps are not pre-argued to the model"*; `-clean.metadata.yaml:75-76` repeats it. Same text is in both blind prompts. The false-positive measurement is inflated by whatever these three sentences suppress.

**M-4 — The CLEAN half files a 2.1.1 conformance PASS from one control, which the repo's own doctrine calls an overclaim.** `-clean.md:246-254`: `wcag: "2.1.1"`, `outcome: "PASS"`, `evidence: ["trace.json#step-2"]`, message scoped to a single control. The BUG rubric's own `known_judgment_calls` (`dialog-dismiss-recipe.rubric.yaml:116`) penalises *"additionally files a 'PASS' for reachability from the trace alone"* as over-claiming, and `prompts/system-recipe-slice.md` (detector-lane authority boundary) says an absence of detection is never a conformance verdict. A reviewer who REVISEs the CLEAN half on that scope overclaim is applying the lane's own doctrine and is scored `FALSE ALARM`. Neither CLEAN trap (`-clean.rubric.yaml:59-77`) covers it, so it isn't even a declared judgment call.

### MINOR

**m-1 — `ACCEPT-WITH-RESERVATIONS` is a rubric-blessed verdict the prompt never offers.** `-clean.rubric.yaml:102` and `-clean.metadata.yaml:67-68` allow it; `-clean.rubric.yaml:98-99` (`verdict_expectations: ACCEPT`) does not list it; the task prefix (`prompts/*.blind.md:1`) offers only ACCEPT or REVISE. The scorer handles it correctly (probe: `Verdict correct: YES | Status: PASS`), so this is a documentation inconsistency, not a scoring one — but a model that follows the prompt literally will never emit the verdict two of three documents describe as expected.

**m-2 — CLEAN trap 6 penalises a reviewer applying the system prompt's own number.** `-clean.rubric.yaml:75-76` declares the 100 ms settle (`-clean.md:194`) to be *"the React-state settle the a11y-test method calls for."* `prompts/system-recipe-slice.md` (SPA patterns) says *"Add `waitForTimeout(200–500)`"*. 100 ms is below the slice's stated range; flagging it is defensible in the skill condition and scored −2.

**m-3 — Metadata and rubric give opposite garbled wordings of CLEAN trap 2.** `-clean.metadata.yaml:42` "…would not reach it even if it were." vs `-clean.rubric.yaml:64` "…would not reach it even if it were not." Neither sentence completes; they contradict each other.

**m-4 — Canary evidence cite is off.** `canaries.py:65` cites `(:230)` for the dismiss/return step; `-clean.md:230` is blank (step 3 is `:225`, the PASS row `:256-263`). Cosmetic — canary citations aren't validated — but it's inside the artifact the README names as proof.

**m-5 — Census rows give `paragraph` an accessible `name`.** `dialog-dismiss-recipe.md:257`, `-clean.md:236`. Paragraphs have no accessible name under accname; the field is carrying text content. Pedantically flaggable, and the flag would be right.

**m-6 — Playwright code-frame realism.** `dialog-dismiss-recipe.md:230-231` shows a single-line code frame; Playwright prints several lines of surrounding context. Does not affect grading.

### OBSERVATION — what checked out clean

Worth recording, because it's most of the fixture: Tab order derives correctly from `querySelectorAll` DOM order `[Close dialog, Cancel, Delete]` plus the wrap logic — initial focus Cancel → Delete (native) → wrap to Close dialog (`items[0]`) → Cancel (native), giving exactly the trace at `:241-246` with "Close dialog" on presses 2 and 5. The six-press bound is genuinely two cycles. `button:has-text("Close")` genuinely matches only `button.account__close` (no strict-mode ambiguity), and `locator.evaluate()` genuinely resolves inside an inert subtree. Both spec-file line numbers in stdout and `findings.json` (`:9`, `:30`; `:9`, `:32`, `:36`) count out correctly against the recipe blocks. Contrast passes (`#1a4fd1` on white 6.8:1; `#fff` on `#b3261e` 6.6:1); target size 32 px ≥ 24; heading levels, `focusable="false"`, `aria-hidden` SVG, `aria-modal` + `labelledby`/`describedby`, Escape handling, and Shift+Tab wrap are all correct. `inert={confirming ? '' : undefined}` is the right React 18 idiom. The blind cut is clean in both prompts and the task prefix is condition-neutral.

---

## What I did NOT check

- Did not execute the component. C-1 is a static reading of React 18 batching + inert focusability; it is unverified against a browser.
- Did not read anything under `evals/results/gt16-dialog-dismiss-recipe/` beyond `canaries.py` and `prompts/`, per instruction — no draw outputs, no results README, no run receipts.
- Did not read `run_benchmark.py`, so I did not verify `RECIPE_SLICES`, fixture registration, `ANSWER_KEY_RE`, or that `prompts/*.blind.md` are byte-derivable from the fixtures. I compared their visible head/tail against the fixtures only.
- Did not read `score_output.py` outside `check_finding` and `count_false_positives`'s head; the composite-score formula, threshold application, and `evidence_quality` / `format_compliance` dimensions are unaudited (note: those two dimensions appear in both rubrics but I did not confirm the scorer implements them).
- Did not verify the Playwright doc quotations at `README.md:21-27` / `metadata.yaml:58-66` against playwright.dev.
- Did not cross-check this suite's metadata schema against the other eval suites, or check `scripts/validate_fixtures.py` registration (issue #25 territory).
- Did not assess the `nice_to_find` items' scorability — they carry no keywords and no `expected_to_find` in the CLEAN rubric.

---

## Provenance

Read (all under `/Users/AlexUA_1/claude/accessibility-skills-gt16`, commit `cbd2f41`):

1. `evals/suites/a11y-test-recipe/README.md`
2. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe.md`
3. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe.metadata.yaml`
4. `evals/suites/a11y-test-recipe/rubrics/dialog-dismiss-recipe.rubric.yaml`
5. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe-clean.md`
6. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe-clean.metadata.yaml`
7. `evals/suites/a11y-test-recipe/rubrics/dialog-dismiss-recipe-clean.rubric.yaml`
8. `evals/results/gt16-dialog-dismiss-recipe/canaries.py`
9. `evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe.blind.md` (head 1-20, tail 255-294, plus grep for cut-line headings)
10. `evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe-clean.blind.md` (head 1-20, tail 252-281, same greps)
11. `evals/results/gt16-dialog-dismiss-recipe/prompts/system-recipe-slice.md` (full)
12. `ollama/score_output.py` lines 91-171 (`check_finding`, head of `count_false_positives`)
13. `ollama/score_common.py` lines 25-55 (`detect_verdict`)
14. `docs/plans/2026-09-02-promotion-candidate-dispositions.md` lines 135-150 (GT-16 row at :141)
15. `evals/results/gt-siblings-rows/README.md`, section "What the draws found in the instrument"

Commands run (read-only w.r.t. the worktree): `git log`, `find`, `diff`/`md5` on the two fixtures, `grep`, `sed`, `python3 evals/results/gt16-dialog-dismiss-recipe/canaries.py` (exit 0, 6/6 ok), and two ad-hoc scorer probe scripts written to and run from `/tmp/gt16probe/` only. No file in the worktree was created, edited, or committed; no agents spawned; no `evals/results/gt16-dialog-dismiss-recipe/` draw outputs read.