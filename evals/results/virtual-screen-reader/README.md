# virtual-screen-reader × a11y-critic Eval Suite — Cross-Validation (2026-07-11)

Executes the Phase 2 gate of
[docs/virtual-screen-reader-adoption-assessment.md](../../../docs/virtual-screen-reader-adoption-assessment.md):
run [guidepup/virtual-screen-reader](https://github.com/guidepup/virtual-screen-reader) (VSR, npm `0.32.1`)
against the announcement-class a11y-critic fixtures — ground truth it did not author — in **both
directions**: does the planted defect read as silent (defect evidence), and does the rubric's corrected
pattern announce (fix-confirmation)? Plus the clean fixture as the false-alarm trap.

## Method

Fixtures are React/JSX source in markdown; VSR asserts on a DOM. Harness (committed under `harness/`,
`npm install && node sweep.mjs`): each component is replicated at the DOM layer — the layer VSR sees and
the layer React produces — in plain Node 24 + jsdom 29.1.1 (the environment validated in the adoption
assessment, probes A–H). Announcement capture uses `spokenPhraseLog()` slices around each mutation, with
50ms settles (microtask flush is sufficient per probe B; the margin is belt-and-suspenders). Raw output:
`raw/<fixture>.json`.

The assessment's probe scripts (probes A–H, the fixture spot-validation, the Vitest fake-timer
characterization, and the Chromium ESM run) are archived verbatim with expected outputs in
[`harness/probes/`](harness/probes/README.md).

**Harness caveats.** DOM-layer replication is ours, kept minimal and faithful to each fixture's rendered
output (same roles, attributes, and mutation order as the React state transitions produce). It does not
exercise React itself — VSR sees only DOM mutations either way. Fixed-direction scenarios are written in
the robust persistent-container shape per calibration rule 3; that rule is exactly why the toast rubric
needed reconciliation (below).

## Pre-run classification (written before the sweep ran)

Same discipline as the KAT record: each fixture's announcement-relevant findings classified by VSR
reachability **before** seeing output. `IN` = silence/announcement is direct evidence; `PARTIAL` = the
phrase log is evidence input but the finding needs judgment (or another lane is primary); `OUT` = outside
VSR's scope, recorded, never forced.

| Fixture | Finding | Class |
|---|---|---|
| toast-notification-no-role | MF1 missing role / MF2 missing aria-live (both CRITICAL) | IN |
| toast-notification-no-role | MF3 no keyboard dismiss | OUT (keyboard) |
| toast-notification-no-role | MF4 message type/context | PARTIAL (log = what the user hears) |
| infinite-scroll-no-announcement | MF1 no load announcement / MF2 no loading state (CRITICAL) | IN |
| infinite-scroll-no-announcement | MF3 no main landmark | PARTIAL (walk shows structure; axe primary) |
| infinite-scroll-no-announcement | MF4 mechanism not discoverable | OUT (judgment) |
| image-carousel-no-region | MF3 no live region for image changes (CRITICAL) | IN |
| image-carousel-no-region | MF1 role=region / MF2 label / MF4 aria-current | PARTIAL (walk phrases) |
| async-form-vague-success | MF vague success message | PARTIAL (log captures the exact text; vagueness is the critic's call) |
| async-form-vague-success | SF aria-busy timing gap | OUT (aria-busy unsupported — upstream #36) |
| multistep-form-error-clearing | MF silent error clearance | IN — *contingent on VSR not announcing removals; measured below* |
| multistep-form-error-clearing | SF disabled-Next tab order; NF hidden-panel focusability | OUT (keyboard) |
| form-field-vs-summary-errors | ADVERSARIAL — dual-pattern interaction | measurement demo only, no verdict |
| search-results-dynamic-clean | CLEAN — correctly-wired region | must announce (false-alarm trap) |

## Headline results

| Pass-bar axis | Result |
|---|---|
| (a) Defect evidence — IN-scope planted defects read silent | **4/4**: toast mount `[]`, infinite-scroll append `[]`, carousel image change `[]`, multistep error clearance `[]` — each alongside the structural absence (no role/aria-live in the buggy DOM) |
| (b) Fix-confirmation — rubric fixes (robust shape) announce | **5/5**: `polite: Item saved`, `polite: 3 more items loaded`, `polite: Image 2 of 2`, `polite: Email error resolved.`, `polite: Your feedback has been sent…` |
| (c) False-alarm trap — clean fixture announces | **2/2 transitions**: `polite: Searching...` → `polite: Found 3 results`. Zero false-silent signals. |

The documented trap reproduced exactly as calibrated: the toast rubric's *naive* fix (add `role="alert"`
to the toast mounted with its content) is **still silent** — see Reconciliation below.

## Measured discoveries (beyond the pass bar)

1. **Removal behavior splits on `aria-atomic`.** The multistep error region (no `aria-atomic`) cleared
   **silently** — which is precisely the fixture's must-find premise ("screen readers do not announce text
   removal"), so VSR's model matches the defect being planted and the silent log is valid evidence. But
   async-form's region (`aria-atomic="true"`) announced an **empty phrase** (`"polite: "`) when cleared —
   an atomic re-read of now-empty content. Calibration note: an empty `polite: ` entry in a log marks a
   region-clear event on an atomic region, not noise.
2. **Adversarial dual-pattern measurement.** On simultaneous submit, the four inline errors (inserted into
   persistent `aria-live="polite"` wrappers) fired — 4 announcements — while the `role="alert"` summary
   (conditionally rendered with its content) was **silent** per calibration rule 3. So in VSR's model the
   worst-case "8 announcements" blast does not reproduce; how many a real user hears is engine/AT-dependent.
   This is evidence *input* to the fixture's tradeoff judgment, not a verdict — the double-announcement
   tension the fixture teaches remains a real-AT question.
3. **Structural walks as supporting evidence.** The infinite-scroll walk contains no landmark phrases
   (supports MF3); the carousel walk announces indicator buttons with no current-state and no region
   boundary (supports MF1/MF2/MF4); the carousel image announces exactly `image, Carousel image 1` — the
   phrase log shows literally what a user hears, which is the evidence form the vague-alt and vague-message
   findings need. Position/set-size phrases (`listitem, … position 1, set size 2`) come free.
4. **async-form lifecycle transcript.** As-written, the log reads `Submitting your feedback...` → `` (empty,
   the clearing state) → `Your submission was successful!` — the exact generic text of the must-find,
   machine-transcribed. The `aria-busy` timing dimension of that fixture stays out of scope (upstream #36).

## WPT expected-failure skim (Phase 2 item 7)

VSR 0.32.1's WPT config (`test/wpt-jsdom/to-run.yaml`, 391 lines) attributes its expected failures to:
dom-accessibility-api upstream (~88 entries, accname manual test cases — label/inline-block wrapping,
describedby-from-content edge cases), html-aria upstream (11, role-mapping edges), jsdom (1), plus a
handful of explicit not-supported skips. **None intersect live-region announcement behavior, and none
intersect the assertion patterns validated here.** Consequence for consumers: for *exotic* accessible-name
structures (deep label wrapping, name-from-content chains), cross-check a wrong-name assertion against a
real browser before treating it as fact; mainstream accname paths (aria-label, label[for], text content)
are unaffected.

## Reconciliation applied (Phase 2 item 6)

`toast-notification-no-role` endorsed `Fix: Add role="alert" to notification div` — a fix this sweep
measures as still-silent when the toast mounts with its content (and which real screen readers are also
inconsistent about; that limb is domain knowledge, not measured here). The fixture's fix language and
rubric were amended to the persistent-live-container pattern. The other announcement fixtures already
endorse region-based fixes and needed no change. The planted defects and must-find items are untouched —
only the endorsed-fix shape changed.

## Verdict

Phase 2 pass bar met on all three axes, with no disagreements against the pre-run classification and one
new calibration nuance (aria-atomic empty-phrase on clear) recorded for the skill. VSR spoken-phrase logs
are cleared to enter a11y-critic Phase 0 as hard evidence (assessment Phase 3), carrying calibration
rules 1–4 as consumption rules.
