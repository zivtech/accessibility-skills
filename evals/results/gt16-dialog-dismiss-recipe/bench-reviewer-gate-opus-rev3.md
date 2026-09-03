<!-- GT-16 bench-reviewer gate on fixture revision 3 (18ba1e8 / rows at 0827f86), model=opus, 2026-09-03, third attempt (two died on API 529). Verbatim; recovered from the agent's session transcript. -->

## VERDICT: **REVISE**

rev3's fixture craft is clean — every rev2 finding on the *artifacts* is genuinely closed, and I could not break the blind protocol, the citations, or the component parity. What blocks is the scorer: the rev2 C-1 repair removed five bad tokens and added ten new ones, three of which re-open the same hole, and the negation window that was supposed to close it is applied group-blind and demonstrably flips correct reviews to 0/1.

---

## Predictions — confirm/refute

| # | Prediction | Result |
|---|---|---|
| P1 | Negation window too **narrow** in ≥1 direction | **CONFIRMED**, on a different axis than guessed: it cannot see negation *after* the token ("contradicts nothing" → PASS), and it is structurally blind to self-negating tokens (`does not exist`). |
| P2 | Window too **wide** — ratifying "contradicts nothing" wrongly discarded | **REFUTED as stated** (that probe is wrongly *credited*, not discarded) — but **CONFIRMED in stronger form**: the window gates groups 1 and 2, where polarity is meaningless. See **M-1**. |
| P3 | A citation drifted by the 2 added recipe lines | **REFUTED.** All 47 citations across both metadata files, both rubrics and both answer keys re-sweep exactly, including the two spec-file line remaps. One off-by-one survives inside `canaries.py` review *text* (m-3). |
| P4 | `// OP-CLOSE-DISMISS` leaks the defect above the cut line | **REFUTED.** Neither comment names an outcome, a verdict, or a trap. See OBSERVATION. |
| P5 | The CLEAN "Escape after a backdrop click" judgment call is not defensible | **PARTIALLY CONFIRMED.** The tiering defence holds; the CLEAN half's own "no component defect" claim does not. See m-4. |
| P6 | `claim_boundary` provenance only partly repaired | **REFUTED.** Declared in both recipes, cited by both rubrics, and the unsupported slice claim is withdrawn. |
| P7 | Components still byte-identical | **CONFIRMED.** md5 `6629169b…` over lines 1-161 in both. |
| P8 | A rev2 MINOR marked resolved but only partial | **REFUTED** for the blind-protocol items (m-2, m-3 fully closed); the residuals are all new. |

---

## Findings

### CRITICAL

**C-1 (rev3) — The withdrawal group's replacement tokens re-open the exact class rev2 C-1 closed. Three probes, three PASSes.**
`rubrics/dialog-dismiss-recipe.rubric.yaml:52` (dup at `fixtures/dialog-dismiss-recipe.metadata.yaml:35`).

rev2 removed `unsupported`, `not supported`, `does not support`, `doesn't support`, `spurious` — correct, and P1a/P1b/P1c now all score `Must-find issues: 0/1 | Status: FAIL`. But rev3 added **ten** new tokens, and three of them are not finding-directed:

| Probe | Ratifying review (blames the component, ratifies the FAIL) | Token that fired | Scored |
|---|---|---|---|
| R1 | *"a keyboard route to the close control **does not exist** … Ratify the filed FAIL and add the button to the focus trap."* | `does not exist` | must **1/1**, **Status: PASS** |
| R2 | *"the close button is **not in the component**'s focus trap … The filed FAIL is correct as recorded."* | `not in the component` | must **1/1**, **Status: PASS** |
| R3 | *"I considered whether this was a **false positive** and ruled that out … The FAIL stands; fix the component."* | `false positive` | must **1/1**, **Status: PASS** |

G1/G2 are free in all three (`has-text` from quoting the selector, `aria-label` from quoting the button), exactly as rev2 documented — group 3 is the only discriminating group, so any leak in it is a full pass.

`does not exist` is bare negative-capability vocabulary of precisely the kind rev2 named, and it is *self-negating*, so the new polarity window can never catch it. `not in the component` matches as a substring of *"not in the component's focus trap"* — a modal ratifying phrase. `false positive` is bidirectional: the negation window catches *"this is **not** a false positive"* (canary C) but not *"ruled out a false positive"*, *"I checked for a false positive"*, *"whether this is a false positive"*.

The disclosed residual also still passes (N1: *"the trace **contradicts** nothing here … The 2.1.1 FAIL stands as filed"* → must **1/1**, PASS), so the withdrawal group now leaks on **four** distinct ratifying phrasings, three of them introduced by the repair.

Consequence is unchanged from rev2: the headline BUG must-find rate is inflated by an unknown share of ratifying draws, in the direction that flatters both conditions. `README.md:104` (*"The withdrawal group holds only finding-directed forms"*) and `metadata:110-111` (*"rev3 keeps only finding-directed forms"*) are **false as written**.

Minimal fix, no re-authoring: delete `does not exist`, `not in the component`, and `false positive` (keep `false fail`, which is finding-directed); canary R1–R3.

---

### MAJOR

**M-1 — The negation window is applied group-blind. It gates the two descriptive groups, where polarity is meaningless, and it discards legitimate withdrawals.**
`ollama/score_output.py:110-119` — `token_ok` is called from `group_ok` for *every* group, including `keywords_all[0]` (has-text / rendered text / text content) and `keywords_all[1]` (getByRole / accessible name / aria-label).

Groups 1 and 2 name **semantics and remedy**. Negation immediately before them is the natural register of a correct diagnosis — *"the control has **no text content**"*, *"the selector **does not match** the **accessible name**"*, *"this is **not** a role-and-name locator"*. The scorer silently drops those.

Measured, against the shipped scorer and BUG rubric:

| Probe | Correct review (right diagnosis, right remedy, withdraws the FAIL) | Scored |
|---|---|---|
| G2 | *"the selector at :185 **does not match the accessible name** of the control under test … the call log (:226) proves it resolved to 'Close account'. The filed FAIL (:275) is an instrument artifact and must be withdrawn."* | must **0/1**, **Status: FAIL** |
| N5 | *"…Rebuild the locator from the census row (:261). The filed 2.1.1 FAIL is **not sound; withdraw** it and re-run."* | must **0/1**, **Status: FAIL** |
| N6 | *"…The trace **does not support it, so retract** the finding and re-run."* | must **0/1**, **Status: FAIL** |

G2's only name-source token was `accessible name`, one word after `does not match` → discarded → the whole conjunction fails. N5 and N6 are correct *withdrawals* whose sentence opens with a negation of the finding's soundness; the window reads the negation as attaching to the withdrawal verb.

I also found the window firing on a *cross-group* token by accident: in the `does not exist` probe as I first wrote it, `has-text` was discarded because the preceding clause was *"does not exist — \`button:has-text(…)\`"* (debug output: `has-text -> blocked=True`). Group 1 is a *description of Playwright semantics*; it has no polarity to get wrong.

**Answer to the brief's question — the window is both too wide and too narrow, on different axes:**

- **Too wide in scope.** It should apply to `keywords_all[2]` only. Applied to groups 1–2 it produces false negatives on correct reviews with no compensating benefit.
- **Too narrow in mechanism.** It reads only *backwards*, so `contradicts nothing` (negation after) passes, and it cannot see tokens that carry their own negation (`does not exist`, `not in the component`).
- **Reach is about right where it belongs.** Measured boundary: ≤3 intervening words blocks, ≥4 does not. The brief's example — *"the finding **does not** survive its own trace and must be **withdrawn**"* (7 intervening words) — is **not** discarded (N2: must 1/1, PASS), and *"this is a **false positive**"* is credited (N3: must 1/1, should 1/1, PASS). Those two are correct.

Fix: scope `token_ok` to groups the rubric marks polarity-sensitive (a `polarity: true` flag on the group, or apply it only to the last group), and stop shipping self-negating tokens so the window has a fighting chance.

---

### MINOR

**m-1 — Neither rev3-introduced defect class has a canary.** `canaries.py:47-139`. The rev2 gate's recommendation ("add P1a as a canary") was followed and P1a/b/c are cases 7-9. But 13/13 pass while R1, R2, R3, G2, N5 and N6 all mis-score — the canary set validates the *removals* and not one of the ten *additions*. This is rev1 C-2's "artifact-of-canary-authorship" problem recurring one revision later: the canaries were written from the previous gate's probe list, not from the new token list.

**m-2 — `canaries.py:2` still says "rev2".** The file header reads *"Scorer-discrimination canaries for the GT-16 pair (a11y-test-recipe), **rev2**"* while both rubrics and both metadata files carry `fixture_revision: 3`. `:25-27` correctly annotate P1a/b/c as rev2 regressions, so only the header is stale.

**m-3 — One canary citation is off by one.** `canaries.py:56`: *"MINOR: six Tab presses is an arbitrary bound (**:189**)."* `fixtures/dialog-dismiss-recipe.md:189` is `let reached = false;`. The bound is at `:190` (`for (let i = 0; i < 6 && !reached; i++)`) and its explanation at `:188`. Every other citation in the file resolves, including all the +2 remaps (`:185`, `:195`, `:226`, `:245-251`, `:247`, `:250`, `:261`, `:275`; CLEAN `:183`, `:187`, `:225`, `:226`, `:236`, `:251`, `:261`).

**m-4 — The CLEAN half's "no component defect" claim is falsified by its own judgment-call list.** `rubrics/dialog-dismiss-recipe-clean.rubric.yaml:111` concedes a real behaviour (*"a mouse click on the backdrop moves focus to `<body>` and Escape is inert until Tab re-enters"*) and names the fix (*"Open item: `onMouseDown={e => e.preventDefault()}` … or a document-level Escape listener, in a future revision"*). Meanwhile `metadata:77-78` and `README.md:21-22` assert *"any component finding a reviewer raises here is a false alarm"* / *"the component here is gated correct."*

**Is the judgment call defensible? On tiering, yes; on the claim, no.**

- Defensible: the task prefix's binary is about **the recipe** (`ACCEPT` = "the recipe and its recorded outcome stand as filed"; `REVISE` = "the recipe must change"). A component gap does not require the recipe to change, so REVISE really is mis-tiered, and the issue is mouse-then-keyboard — outside the keyboard route the recipe covers. It is also broader than the rubric says: clicking the `<p>` or `<h2>` *inside* the dialog has the same effect, since the handler is bound to `div.dialog` (`:91`), not the document.
- Not defensible: the machine does not know any of that. Measured — a reviewer who raises it as **MINOR or ENHANCEMENT under ACCEPT scores PASS** (probes E1, E2: `Verdict correct: YES | Status: PASS`), which is the important result and materially milder than rev2's M-1. But **as MAJOR under REVISE it scores `Verdict correct: NO — FALSE ALARM | Status: FAIL`** (probe E3). So a reviewer who is *substantively right about a real gap* is punished for the tier, on a fixture whose documentation says there is nothing to find.

Not a blocker on its own; it is a documentation defect (`metadata:77-78`, `README:21-22` overstate) plus a deferred repair. Either fix the component in rev4 (two lines) or stop claiming the CLEAN half has no component gap.

**m-5 — `should_find` prompt-relative tokens are asymmetric.** `rubric:64` / `metadata:49` carry `":247"`, `":250"`, `"line 247"`, `"line 250"`, `":249"`, `":252"` — the `line NNN` spelling exists for the fixture-relative pair but not the prompt-relative pair. Harmless in practice (`"step 2"` / `"second press"` carry the group), but the +2 offset is now applied inconsistently within one list.

---

### OBSERVATION — what checked out clean

**The operation-id comments are good work.** `fixtures/dialog-dismiss-recipe.md:187,197` and `-clean.md:189,199`. They read as ordinary recipe practice — an id plus the operation's intent, sitting directly above the assertions they scope, which is how an evidence-contract-aware recipe would be written, and they satisfy the BUG rubric's own `nice_to_find` #2 on selector/operation provenance (`rubric:75-76`). **rev2 M-1 is fully closed**: the ids in `-clean.md:251`/`:261` and BUG `:277` now have a source in the subject; `-clean.rubric.yaml:82` cites `(:189, :199)` and both resolve; and the unsupported claim at old `-clean.rubric.yaml:98` is withdrawn and replaced with the true statement (*"The slice says nothing about `claim_boundary`"*) — verified, `grep -ic claim_boundary prompts/system-recipe-slice.md` = **0**.

**No leak.** Neither comment names an outcome, a verdict, or a trap. The one thing I'd change is register: both are declarative (*"the close control **is** reachable by Tab"*) while the `claim_boundary` they pair with is infinitival (*"reach the dialog close control by Tab"*). In the BUG half that declarative sits three lines from a FAIL asserting the opposite. It does not pre-argue — the tension is exactly what the fixture wants resolved from the trace — but matching the `claim_boundary` phrasing verbatim would cost nothing and remove the question.

**Blind protocol is sound.** Both prompts' line 1 is the identical task prefix; both H1s are the identical neutral `# Fixture: Delete-Report Dialog — Keyboard Dismiss Recipe`; nothing above `## Accessibility Issues` names a verdict, a defect, or a trap. `diff` of `tail -n +3 prompts/X.blind.md` against `sed -n '1,295p'`/`'1,279p'` of each fixture is **empty** — bodies byte-identical, answer keys stripped, offset exactly +2 in both halves (BUG prompt 297 lines / fixture cut at 297; CLEAN prompt 281 / cut at 281). rev2's m-2 residual (*"On dismissal by any route, focus returns to the Delete report trigger"*) is **gone** from both Expected Behavior sections.

**Line citations.** All rubric and metadata cites re-sweep against the +2 fixtures: BUG `:185`, `:226`, `:95-99`, `:261`, `:275`, `:247`, `:250`, `:198-200`, `:188-194`, `:245-251`, `:56-61`, `:58-60`, `:17`, `:32-34`, `:88`; CLEAN `:183`, `:187`, `:189`, `:190-196`, `:199`, `:251`, `:261`, `:236`, `:95`. Both spec-file remaps are correct against the recipe block: BUG `assertion:…spec.js:31` = fixture `:195`, code frame `29|30|>31|32|33` counts out exactly (spec N = fixture 164+N); CLEAN `:33` = `:197` and `:37-38` = `:201-202`.

**Component parity and CLEAN cleanliness.** Lines 1-161 md5-identical. Beyond the conceded Escape gap (m-4), I re-derived the CLEAN half and found no unplanted defect: trace step 3 (`:226`) and the 2.4.3 PASS row (`:257-266`) are reproducible from the passive-cleanup return (React 18.3 defers passive destroys to `flushPassiveEffects`, after the sibling root's `inert` removal commits); census is in DOM order; the two-Tab loop exit is correct against `for (i<6 && !reached)`.

**rev2 m-3 resolved.** The slice's React-16 `setTimeout(0)` line is still at `system-recipe-slice.md:92`, but it is now named explicitly in both `known_judgment_calls` (`rubric:122`, `-clean.rubric.yaml:110`), which was the fix asked for.

---

## rev2 finding-by-finding resolution

| rev2 | Status | Evidence |
|---|---|---|
| **C-1** scorer PASSes a ratifying review (P1a/b/c) | **PARTIAL → C-1 (rev3)** | The five named tokens are gone and P1a/b/c now FAIL. But ten tokens were added; `does not exist`, `not in the component`, `false positive` re-open the class (R1/R2/R3 all PASS). Net: repaired on the measured probes, **regressed on the unmeasured ones**. |
| **M-1** `claim_boundary` operation IDs have no provenance; a reviewer who says so is FALSE ALARM | **RESOLVED** | Ids declared at BUG `:187`,`:197` / CLEAN `:189`,`:199`; trap 7 cites them (`-clean.rubric.yaml:82`); the provenance question no longer exists to be raised. |
| **M-1 related** `-clean.rubric.yaml:98` claims the slice steers onto `claim_boundary` | **RESOLVED** | Line now reads *"The slice says nothing about claim_boundary"*; slice grep = 0 hits. |
| **m-1** rubric prescribes a credit reduction the scorer cannot apply | **RESOLVED (as documentation)** | `rubric:67` now marks it *"Hand-adjudicated, not machine-scored (known_judgment_calls)"*; canary P7 encodes the PASS-by-design. |
| **m-2** `## Expected Behavior` pre-argues trap 5 | **RESOLVED** | Focus-return sentence removed from BUG `:288-289` and CLEAN `:272-273`; nothing above the cut line asserts the mechanism. |
| **m-3** slice's `setTimeout(0)` is an undeclared false alarm | **RESOLVED** | Named in `rubric:122` and `-clean.rubric.yaml:110`. |
| **m-4** prompts +2 from fixtures, rubric line tokens fixture-relative | **RESOLVED (one asymmetry)** | `rubric:64` carries `:249`/`:252` alongside `:247`/`:250` with the offset documented inline and at `README:108-109`; `line 249`/`line 252` missing (m-5). |

**New defects from the repair round:** C-1 (rev3) from the C-1 repair, M-1 from the polarity window that repair introduced, m-1/m-2/m-3 in `canaries.py`, m-4's documentation overreach.

---

## What I did NOT check

- **Did not execute the component or run React.** The passive-cleanup verdict is a static re-derivation of React 18.3's commit order, agreeing with the rev2 gate's independent reading. ~90% confidence; falsifier is a one-line browser test.
- **Did not read any draw outputs** (`claude-*-rev2/rev3.md`), the results `README.md`, or `bench-reviewer-gate-opus-rev1.md`, per instruction.
- **Did not read `run_benchmark.py`.** `RECIPE_SLICES`, fixture registration, and `ANSWER_KEY_RE` are unverified; I verified prompt/fixture body identity by `diff` instead, which proves the stripping happened for these two artifacts but not that the runner would reproduce them.
- **Read `score_output.py` only at `check_finding` (`:91-140`)** plus the head of `count_false_positives`, per instruction. Unaudited: the composite-score formula, the 0.4 abort threshold, threshold application, and whether `evidence_quality` / `format_compliance` are implemented at all — both rubrics declare those two dimensions and I did not confirm the scorer reads them. `nice_to_find` (2 BUG / 3 CLEAN) still carries no keywords in either rubric; whether it is scorable or deflates the denominator is unchecked. Carried forward unresolved from rev2.
- **Did not audit the other seven new withdrawal tokens** individually (`refute`, `contradict`, `not be filed`, `before any outcome is filed`, `before anything is filed`, `fabricated`, `invalid measurement`). `contradict` is known-leaky from N1; the rest are untested and should be assumed suspect until canaried.
- **Did not read the full `system-recipe-slice.md`** — headings plus targeted greps (`claim_boundary`, `operation`, `OP-CLOSE`, `has-text`, `getByRole`, `selector provenance`, `setTimeout`) only.
- **Did not verify the Playwright doc quotations** at `README.md:26-32` / `metadata:70-75` against playwright.dev.
- **Did not cross-check this suite's metadata schema against the other suites**, or run `scripts/validate_fixtures.py` (issue #25 territory).
- **Did not test scorer behaviour on thinking-tagged or truncated responses.**
- **Did not evaluate whether the negation-window change regresses any other suite** that uses `keywords`/`keywords_any` — `score_output.py` is shared, and `token_ok` now applies to every rubric in the repo that carries those fields. Untested and worth checking before merge.

---

## Provenance

Read (all under `/Users/AlexUA_1/claude/accessibility-skills-gt16`, commit `0827f86`):

1. `evals/results/gt16-dialog-dismiss-recipe/bench-reviewer-gate-opus-rev2.md`
2. `evals/suites/a11y-test-recipe/README.md`
3. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe.md`
4. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe.metadata.yaml`
5. `evals/suites/a11y-test-recipe/rubrics/dialog-dismiss-recipe.rubric.yaml`
6. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe-clean.md`
7. `evals/suites/a11y-test-recipe/fixtures/dialog-dismiss-recipe-clean.metadata.yaml`
8. `evals/suites/a11y-test-recipe/rubrics/dialog-dismiss-recipe-clean.rubric.yaml`
9. `evals/results/gt16-dialog-dismiss-recipe/canaries.py`
10. `evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe.blind.md` (head 1-12, tail 20, full-body `diff` vs fixture, `wc -l`)
11. `evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe-clean.blind.md` (same)
12. `evals/results/gt16-dialog-dismiss-recipe/prompts/system-recipe-slice.md` (targeted greps only: `claim_boundary`, `operation`, `OP-CLOSE`, `has-text`, `getByRole`, `selector provenance`, `setTimeout`)
13. `ollama/score_output.py:80-180` (`check_finding`, head of `count_false_positives`)
14. `git show df05648:evals/suites/a11y-test-recipe/rubrics/dialog-dismiss-recipe.rubric.yaml:45-60` (rev2 withdrawal group, for the added/removed token diff)
15. `git diff df05648 HEAD -- ollama/score_output.py` (the negation-window patch)

Commands run (read-only w.r.t. the worktree): `git log`, `git show`, `git diff`, `ls`, `sed`, `tail`, `wc`, `grep`, `diff`, `md5` on lines 1-161 of both fixtures, `python3 evals/results/gt16-dialog-dismiss-recipe/canaries.py` (13/13 ok, `EXIT=0`, reproduced), and four probe/debug scripts written to and run from `/tmp/gt16rev3/` only (21 scored probes total). No file in the worktree was created, edited, or committed; no agents spawned; nothing under `evals/results/gt16-dialog-dismiss-recipe/` read beyond `canaries.py`, `prompts/`, and the rev2 gate report.