# keyboard-a11y-tester × a11y-critic Eval Suite — Cross-Validation (2026-07-10)

Executes the correctness cross-validation gate (Phase 2) of
[docs/keyboard-a11y-tester-adoption-assessment.md](../../../docs/keyboard-a11y-tester-adoption-assessment.md):
run [ezufelt/keyboard-a11y-tester](https://github.com/ezufelt/keyboard-a11y-tester) (KAT, commit `97eb13e`)
against ground truth it did not author — all 33 a11y-critic eval fixtures with their known planted bugs —
and record agreement, misses, false alarms, and surprises. Question under test: **does KAT miss our evals?**

## Method

Fixtures are React/JSX source in markdown; KAT tests rendered pages. Harness (committed under `harness/`):

1. `build_fixtures.py` — extracts JSX+CSS from each fixture, wraps with React 18 UMD + Babel standalone,
   applies per-fixture prop shims (realistic content; long-lived toast; modal behind a clean trigger button;
   a hash-based `useRouter` stub for the one Next.js fixture). Served over `http.server`.
2. `render_check.mjs` — verified all 33 pages render with content and no fatal JS errors before testing.
3. Batch: `node runner.mjs --url <page> --viewport desktop --max-steps 40` per fixture (blind Tab-crawl,
   both personas). Raw output: `findings/<fixture>.json`.
4. Driven: 6 `serve`/`step`/`finish` sessions on interaction-dependent fixtures, agent-driven
   (`harness/drive.sh`). Raw traces: `driven/*.trace.json`.
5. `score.py` — matches findings against each fixture's `must_find` metadata using a **pre-run
   classification** of all 68 must-find items by KAT reachability: `DET` (one of its 13 deterministic
   checks), `AI` (reachable only by its AI-judgment layer reading trace/census), `OOS` (outside KAT's
   declared scope). Classification was written before seeing batch output; disagreements are reported below,
   not silently reclassified.

**Harness caveats.** Rendered via React UMD + Babel, not a production build; prop shims and wrapper
elements are ours (kept minimal and deliberately clean). One fixture (`image-carousel-no-region`) generates
its own alt text, so shim image data cannot pollute it. Judgment-layer results are from one competent
agent driving 6 sessions — an existence proof, not a benchmark.

## Headline results

| Measure | Result |
|---|---|
| Must-finds in suite | 68 across 26 buggy fixtures (+4 CLEAN, +3 ADVERSARIAL fixtures with 0) |
| Reachable by KAT's deterministic layer (pre-run classification) | 3 of 68 (~4%) |
| — of those, caught by blind crawl | 2 of 3 (both heading-hierarchy skips, `sr-heading-skip`) |
| — missed | 1 (file-input missing label — root-caused below, reclassifies to judgment-layer) |
| Judgment-layer-scope must-finds | 60 of 68 (~88%) — sampled via 6 driven sessions, evidence obtained in all 6 |
| Out of KAT's declared scope | 5 of 68 (video captions ×3, table header scope ×2) |
| False positives on CLEAN/ADVERSARIAL fixtures | 3 AA findings, **all one class** (passive-crawl 4.1.3 — see below); **zero** in any other check class |
| Planted bugs caught beyond the must-find list | 1 (positive `tabIndex={1}` on `app-focus-order-illogical` — listed in that fixture's nice-to-finds) |
| Real defects found that our ground truth does not list | 2 (fixture rubric gaps — see below) |

**Answer to the question: yes — by design, KAT's deterministic layer misses ~95% of this suite's ground
truth.** The suite plants *design and semantic* bugs (missing roles, missing associations, missing
grouping, wrong patterns) — critic territory, mostly reviewable only in source or by judgment. This
empirically confirms the complementarity claim in the adoption assessment: KAT is not a critic
replacement. What its deterministic layer does measure, it measured with zero cross-class false alarms;
and its session protocol turned judgment claims into machine-backed evidence everywhere we drove it.

## Deterministic layer — detail

**Caught (2):** `heading-hierarchy-skipped` and `dashboard-heading-inconsistency` — both h1→h3 skips
flagged as `sr-heading-skip` (1.3.1) from the screen-reader census. The second one matters: the fixture
styles h2 and h3 identically so the skip is invisible on screen; the census catches it structurally.

**Missed (1, root-caused):** `file-input-no-labels` — predicted DET (4.1.2 unnamed control), not flagged.
The trace shows why: Chromium's accessibility tree gives `<input type="file">` an intrinsic UA-provided
name, **"Choose File"** (`trace.json step_0001: name='Choose File', role=button`). At the AX level the
control is not nameless, so the check is factually correct; the missing `<label>` is an
announcement-*quality* defect ("Choose File" — of what?) reachable by the judgment layer, and a
label-association defect axe-core catches statically. Lesson recorded: UA-intrinsic names mask missing
labels from pure name-presence checks. (Possible upstream enhancement: CDP exposes name *source*, so
UA-default names on form fields could be distinguished from author-provided ones.)

**Surprise catches:** `app-focus-order-illogical` — the fixture also plants `tabIndex={1}` (its
nice-to-find #4); KAT flagged both elements deterministically (2.4.3). The must-find itself (CSS
`order:-1` visual/DOM mismatch) is correctly *not* deterministic territory — DOM order is legal; only
judgment against the screenshot catches it.

## False-positive analysis

All 3 AA findings on CLEAN/ADVERSARIAL fixtures are the same check: **`sr-live-region-silent` (4.1.3) on
a passive blind crawl** (`search-results-dynamic-clean`, `search-focus-stays-in-input`,
`form-field-vs-summary-errors` — the latter has 4 correctly-wired live regions that simply never fired
because a blind crawl never submits the form). Two buggy fixtures drew the same artifact
(`async-form-vague-success`, `multistep-form-error-clearing`). KAT's own README pre-discloses exactly
this: blind-crawl live-region findings only mean "never fired passively," and need a driven session.
The driven `async-form` session proved the point — its region announced fine when actually operated.

**Consumption rule adopted from this result (encoded in the assessment's Phase 1/3):** batch-mode 4.1.3
findings are never evidence of failure — only a prompt to drive the interaction. Confidence on these
findings was low (0.35–0.4) vs 0.7–0.85 for name/heading findings, so the field is usable as a filter.

One additional artifact class: `pagination-no-nav-landmark` drew a 2.4.1 no-skip-link finding — true of
the page we built but an artifact of rendering a lone component as a full page. Fixture-granularity
noise, not a tool error; it fired on only 1 of 33 component pages.

**No other false positives.** Across 33 pages: no spurious focus-indicator, accessible-name, heading,
landmark, trap, or context-change findings. The 4 CLEAN fixtures produced zero AA findings outside the
passive-4.1.3 class (3 of 4 produced zero findings at all).

## Driven sessions (judgment layer) — 6/6 produced decisive evidence

| Fixture | Planted bug (must-find) | Trace evidence |
|---|---|---|
| `modal-complete-clean` (control) | none — CLEAN | Enter → focus lands on "Close dialog" inside modal; Tab cycles Save↔Close (trap holds); Escape → focus restored to "Open settings". Clean verdict, no false-alarm material. |
| `interactive-dropdown-focus-bug` | focus not restored to trigger after selection/Escape | After Enter on an option: `focused=None` — focus dropped to body, not the trigger. Shift+Tab recovery required. |
| `async-form-vague-success` | success/status message generic | Live announcements captured on submit: "Submitting your feedback…" then "Something went wrong. Please try again." — vagueness directly assessable from captured text; each announced 2–3× (duplication as a bonus quality note). |
| `tabs-missing-arrow-nav` | no arrow-key navigation | On `[role=tab]`: ArrowRight → `focus_moved=false`; ArrowLeft → `focus_moved=false`. |
| `form-validation-missing-aria-describedby` | errors not associated; error summary not announced | After submitting empty: field flips `invalid=true` (errors fired) yet **zero** `live_announcements`; refocused field's AX shows `labelledby` only — **no `describedby` relation**. Both must-finds machine-evidenced. |
| `popover-no-focus-management` | focus not moved into popover; not restored on close | Enter opens popover but `focus_moved=false` (stays on trigger); Escape → `focus_moved=false` (inert — popover doesn't even close). |

Two sessions began with a wrong assumption and the observe→decide loop corrected them (dropdown's
listbox needed Tab-into, not ArrowDown; goal text guessed a button name wrong in the earlier assessment
run) — concrete support for the "Tab until the observation matches, never a counted sequence" rule.

## Two-way value: defects our rubric does not list

1. `tabs-incomplete-aria-selected`: the tabpanel has `tabIndex={0}` with **no `aria-labelledby`** — KAT
   flagged it as an unnamed focusable control (4.1.2, batch mode). Real defect (APG tabs: label the
   panel from its tab); our metadata's "clean" checklist even marks the panel structure as correct.
2. `interactive-dropdown-focus-bug`: the listbox announced as `''/listbox` in the driven trace —
   unnamed listbox, also absent from our must-finds.

Both are fixture-improvement candidates (add as should-finds).

## Reproduction

```bash
# from a clone of ezufelt/keyboard-a11y-tester@97eb13e with npm install done:
python3 harness/build_fixtures.py            # writes pages/ from evals/suites/a11y-critic/fixtures
(cd pages && python3 -m http.server 8777 &)
node harness/render_check.mjs                # all 33 must render before testing
ls pages/*.html | sed 's/.*\///;s/\.html//' | xargs -P 4 -I F \
  node <kat>/scripts/runner.mjs --url http://127.0.0.1:8777/F.html --viewport desktop --max-steps 40 --out results/F
python3 harness/score.py
harness/drive.sh <fixture> <port> "<goal>" press:Tab press:Enter observe ...   # driven sessions
```

Screenshots are not committed (regenerable); traces, findings, and the harness are.
