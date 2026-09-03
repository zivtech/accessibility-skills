# a11y-test-recipe eval suite

**Status: one BUG/CLEAN pair + runner lane landed 2026-09-03 (GT-16, wave 2,
fixture-first); first model rows in `evals/results/gt16-dialog-dismiss-recipe/`.**

This suite measures a **test-instrument judgment**: given a keyboard test
recipe, the run output it produced, and the component it targets, does the
reviewer decide correctly whether the recipe's recorded outcome is supported
by its own evidence? It sits beside `a11y-test-operation-evidence` (which
grades an evidence package against the five admissibility rules the a11y-test
skill states) at the level *before* a run is treated as evidence: is the
recipe pointing at the control it claims to test at all.

The component in every fixture here is correct. The defects, where planted,
are in the recipe or in the outcome it filed. A review that blames the
component has found the right symptom for the wrong reason, and the rubrics
score that as a false alarm.

## Why this lane exists (GT-16)

Playwright's `:has-text()` pseudo-class matches an element's **rendered text
content** — "case-insensitive, trims whitespace and searches for a substring"
(playwright.dev/docs/other-locators, *CSS: matching by text*). Its role
locators "follow W3C specifications for ARIA role, ARIA attributes and
accessible name", and `getByRole`'s `name` option matches the **accessible
name** (playwright.dev/docs/locators; api/class-page). A control whose name
comes from `aria-label` over an icon has no text content, so a recipe that
derives its selector from the label it *sees* — `button:has-text("Close")` —
cannot resolve the control, and will bind to whatever else on the page has that
text. The observed failure mode is a keyboard "not reachable" FAIL filed
against a control the run's own trace shows being focused.

The disposition (`docs/plans/2026-09-02-promotion-candidate-dispositions.md`,
GT-16) withdrew a one-sentence SKILL.md fold in favour of a fixture-first pair:
Playwright's documented selector semantics is the independent public reference
the Tier-3 criterion requires, and the pair is the second reproduction clause 1
of the promotion bar demands *before* any skill sentence lands. Nothing in the
a11y-test slice this lane loads mentions `:has-text()`, `getByRole`, or
selector provenance — that absence is what the A/B measures.

## Fixtures

| Fixture | Kind | What is graded |
|---|---|---|
| `dialog-dismiss-recipe` | BUG | must: the `:has-text()` selector cannot resolve an `aria-label`-named control and bound to the wrong button (call log); should: the trace contradicts the filed 2.1.1 FAIL — withdraw it, don't ratify it. Four traps: the icon-only button, the inert "Close account" button, initial focus on Cancel, the six-press bound |
| `dialog-dismiss-recipe-clean` | CLEAN | byte-identical component; selector is `dialog.getByRole('button', { name: 'Close dialog', exact: true })`; two PASS rows with the trace steps that support them. Six traps: the four above plus a `:has-text()` on a text-bearing paragraph (correct) and `exact: true` (deliberate) |

Fixture shape (the blind envelope proposed in issue #51 — no
"Accessibility Features Present" section precedes the cut line):

```
# Fixture: <neutral title>
## Component Code · ## CSS · ## Keyboard Test Recipe · ## Run Output
   (stdout · trace.json · screen-reader-census.json · findings.json)
## Expected Behavior · ## Frameworks & Environment
## Accessibility Issues …        ← blind cut line (ANSWER_KEY_RE)
## Difficulty Level
```

`trace.json` and `screen-reader-census.json` follow the a11y-test verification
evidence contract's shapes (per-step keystroke + accessibility-tree focus
target; reading-order census with role, name, selector). The census is the
**accessible-name inventory** a recipe's selectors should be derived from.

## Running

```bash
python3 ollama/run_benchmark.py recipe <model> dialog-dismiss-recipe            # a11y-test slice = system prompt
python3 ollama/run_benchmark.py recipe-baseline <model> dialog-dismiss-recipe   # no system prompt
python3 ollama/score_output.py <response.json> evals/suites/a11y-test-recipe/rubrics/<id>.rubric.yaml
```

The system prompt is three heading-anchored slices of
`.claude/skills/a11y-test/SKILL.md` (`RECIPE_SLICES` in the runner): the
verification evidence contract with its detector-lane authority boundary, the
keyboard test method, and the live-site / SPA / CSS / ARIA-check sections. The
task prefix asks for `VERDICT: ACCEPT` (recipe and outcome stand as filed) or
`VERDICT: REVISE` (the recipe must change before its outcome can be filed).

## Scoring

`ollama/score_output.py`, the critic lane's instrument: verdict + must-find
detection for BUG, verdict + no-findings for CLEAN. The BUG rubric is the first
to use the scorer's explicit `keywords_all` / `keywords_any` fields (added
2026-09-03): the first-four-words fallback is polarity-blind on this fixture,
because any review that quotes the selector would score the must-find whether
it diagnosed it or not. The must-find requires `has-text` **and** one of the
semantics/remedy tokens; a "scope the selector to the dialog" review (wrong
diagnosis) scores 0/1. Proof: `evals/results/gt16-dialog-dismiss-recipe/canaries.py`.

False-positive traps are adjudicated by hand in the results README, as in the
other GT pairs. Scorer statuses are detector output, not verdict authority.

## What this suite is NOT

- Not a component review — the a11y-critic suite does that; the component here
  is correct by construction and any component finding is a false alarm.
- Not the operation-evidence admissibility lane — those five rules are a closed
  set in SKILL.md and their scorer rejects unknown rule ids; this lane grades a
  judgment that lane cannot express without a sixth rule, which is exactly the
  skill-text change the fixture must precede.
- Not a Playwright execution — the repo is prompt-only; run outputs are fixture
  text, authored to Playwright's real message shapes (`Call log: … locator
  resolved to <…>`), not captured from a browser.
- Not a claim that `:has-text()` is wrong in general — on a text-bearing
  element it is correct, and the CLEAN half scores a reviewer for saying so.
