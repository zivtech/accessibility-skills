I'll read the single file I've been given and run the full protocol on it.

---

**VERDICT: ACCEPT**

**Overall Assessment**: The three map controls are native `<button type="button">` elements with visible text names and `aria-hidden` icons — the semantics, naming, and state model are all correct for momentary actions, and no toggle state is falsely implied. The map's visual-only content has a declared peer text route, the new-tab anchor carries a real destination plus a visually-hidden disclosure, and no rule anywhere in the CSS removes a focus indicator. I found no CRITICAL or MAJOR defect; what remains are two enhancements and four verification gaps that the supplied file cannot settle.

---

**Pre-commitment Predictions** (made before reading the code, from the component type "map zoom/reset controls"):

| # | Predicted | Actual |
|---|---|---|
| 1 | Icon-only buttons with no accessible name | **Wrong.** Each button has visible text (`map-controls-clean.md:31,35,39`) |
| 2 | `<div>` or `<a href="#">` used as the zoom control | **Wrong.** Real `<button type="button">` (`:29,33,37`) |
| 3 | No text alternative for the map canvas | **Wrong.** Peer data-table route present (`:22–26`) |
| 4 | Map state change not announced after activation | **Partly right** — see Enhancement 1. Calibrated down, not a WCAG failure |
| 5 | `target="_blank"` with no disclosure | **Wrong.** Visually-hidden disclosure present (`:46`) |
| 6 | Focus indicator suppressed or too faint | **Wrong.** 3px outline, no `outline: none` anywhere in the stylesheet |

Five of six predictions failed. That is the honest signal here: this component was built by someone who already knew the traps.

---

**Critical Findings** (blocks access): **None.**

**Major Findings** (significantly degrades experience): **None.**

**Minor Findings**:

1. **Spec text and source order disagree about control placement.** "Expected Behavior" says the three actions sit *above* the map (`map-controls-clean.md:143`), but in source order the controls come *after* the canvas and after the table link (`:20`, `:22–26`, `:28–41`), and nothing in the CSS reorders them — `.map-panel` (`:59–65`) is not a flex or grid container, `.map-controls` (`:79–83`) sets no `order`, and there is no absolute positioning. **As written, DOM order equals visual order, so WCAG 1.3.1 / 2.4.3 pass.** I flag it only because the discrepancy means one of the two artifacts is stale; if the shipped layout actually raises the controls visually above the canvas without moving them in the DOM, that becomes a real 2.4.3 Focus Order finding. Confidence: HIGH on the discrepancy, no claim of a violation.

**Enhancements** (best practice, no access barrier):

1. **No programmatic result from the three controls.** Pressing Zoom in / Zoom out / Reset view (`:29,33,37`) changes only the canvas rendering; nothing announces the outcome and no current-zoom value is exposed. WCAG **4.1.3 Status Messages does not bite here** — 4.1.3 applies to status text presented visually, and this design presents no status text at all — so this is a coherence note, not a failure. Still, a screen reader user who tabs onto "Zoom in" and activates it perceives nothing whatsoever. Consider a `role="status"` region reporting "Zoom level 5 of 12", or accept the current design explicitly on the grounds that the data table (`:23`) is the SR-facing route and the zoom controls are a visual-view affordance. Either is defensible; the design should say which.
2. **File format not disclosed on the report link.** The expected behavior says the destination is a PDF (`:145`), but the accessible name is "Open full report (opens in a new tab)" (`:44–47`) with no format cue and an extension-less href. No SC requires it; adding "(PDF)" is a low-cost cognitive-accessibility win.
3. **Touch target is ~33px tall, not 44px.** `.map-control` (`:85–95`) resolves to roughly 6+6px padding + ~19px line box + 2px border ≈ 33px. This **passes WCAG 2.2 2.5.8 Target Size (Minimum, AA, 24×24)** and fails only 2.5.5 (AAA). Reported as an enhancement, not a finding, per the AA target.

---

**What's Missing** (gap analysis):

- No live region or `aria-busy` anywhere — covered in Enhancement 1; deliberate-looking rather than accidental, given the text-alternative strategy.
- No disabled/boundary state on the buttons at max/min zoom. Handlers are `console.log` stubs (`:9–11`), so this is unknowable from the file — noted, not scored.
- No `prefers-reduced-motion` block. There is also no motion in the supplied CSS, so nothing is missing *yet*; it becomes relevant only if the third-party library animates zoom transitions.
- No keyboard route for panning the map, only zoom/reset. The canvas is third-party (`:17–20`) and the table is the declared peer route, so this is out of the reviewable surface.
- **Checked and clean, worth stating explicitly:** no `outline: none` / `outline: 0` anywhere; no `text-decoration: none` on either link, so the UA underline survives and WCAG 1.4.1 is satisfied for the in-paragraph links; `aria-labelledby="map-heading"` (`:14`) resolves to a real id in the same file (`:15`); `.visually-hidden` (`:128–138`) is the correct clip pattern including `white-space: nowrap` and `border: 0`, so the disclosure text is not collapsed; the outline-based focus indicator survives Windows High Contrast Mode (a `box-shadow` ring would not).

---

**Multi-Perspective Notes**:

- **Screen reader user**: The `<section>` gains a `region` role from its accessible name (`:14–15`), giving a landmark to jump to. Buttons announce as "Zoom in, button" etc. with names from visible text, so there is zero risk of an `aria-label` drifting from the label on screen. Correct absence of `aria-pressed` — nothing is falsely announced as a toggle. The one soft spot is Enhancement 1: activation produces no announcement.
- **Keyboard-only user**: Tab order is table link → three buttons → report link, matching source and visual order. All three controls are real buttons, so Enter *and* Space both fire — the single most common failure mode for map controls, avoided. No trap, no custom key handling to discover, nothing focusable hidden behind `visibility: hidden`.
- **Low vision (200% zoom, high contrast)**: Button text `#0b5fff` on the explicitly-declared `background: #fff` (`:90–93`) computes to **5.13:1** — passes 1.4.3 AA. The focus ring is 3px with 2px offset (`:97–100`), well past 1.4.11's 3:1 against white. Two caveats below in Open Questions. `max-width: 640px` with `margin: auto` (`:60–61`) reflows without horizontal scroll.
- **Cognitive**: Three plainly-named actions, an explicit "Reset view" escape hatch, no timeout, no destructive action needing confirmation. New-tab behavior is disclosed rather than sprung. The gap is the absence of any zoom-level readout — a user who loses track of where they are must press Reset and restart.

---

**Verdict Justification**: ACCEPT. Every claim in the file's "Accessibility Features Present" section survived independent verification against the code, and I could not construct a realistic user-blocking scenario for any perspective. Severity calibration applied twice: the state-communication observation was held at ENHANCEMENT rather than promoted to MAJOR under 4.1.3, because 4.1.3 governs *visually presented status text* and this design presents none — promoting it would be a manufactured violation; and the target-size item was held at ENHANCEMENT because the AA criterion is 2.5.8 (24×24), which it passes, not the AAA 2.5.5 (44×44), which it does not. An upgrade past ACCEPT is not available; a downgrade would require either the layout discrepancy in Minor 1 to resolve against the code, or one of the Open Questions to resolve badly.

---

**Open Questions (unscored — cannot be settled from the single file I was given)**:

1. **Does `aria-hidden="true"` actually reach the rendered `<svg>`?** `ZoomInIcon` / `ZoomOutIcon` / `ResetViewIcon` (`:30,34,38`) are React components imported from `../icons`, which is not in scope. `aria-hidden` on a component is inert unless that component spreads props onto its root element. Worst case is bounded — the buttons carry their own visible text names, so a leaked `<title>` would produce a redundant announcement, not a nameless button.
2. **What background does the focus ring actually sit on?** `.map-panel` (`:59–65`) declares no `background`, so the 2px offset gap exposes the inherited page background. My 5.13:1 figure for `#0b5fff` is computed against white. On a mid-blue or dark host page the ring could fall under 1.4.11's 3:1. This needs a measured runtime contrast reading in context, not a hex computation.
3. **Is `id="map-heading"` (`:15`) safe against multiple instances?** The id is hard-coded in a reusable component. Two `WatershedMapPanel`s on one page would duplicate it and make the `aria-labelledby` resolution ambiguous (cite 1.3.1 — 4.1.1 Parsing was removed in WCAG 2.2). Almost certainly a single-instance panel; worth one line of confirmation.
4. **What semantics does the third-party library inject into `.map-canvas` (`:20`)?** If it mounts focusable elements, keyboard controls, or an unlabeled `<canvas>`, none of that is visible here. The declared table alternative (`:22–26`) covers the *content*; it does not cover semantics the library adds to the tab order.

---

## Provenance

I read exactly one file, in full, and nothing else:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt-siblings-rows/prompts/map-controls-clean.blind.md` (155 lines, single `Read` call)

No other file was read. No `Grep`, `Glob`, `Bash`, or `git` command was run. Nothing under `evals/suites/` was accessed, and no `*.metadata.yaml` or `*.rubric.yaml` was opened. The repo was not searched for this fixture's name. Line citations use the line numbers of the file as given to me. The one contrast ratio quoted (5.13:1) is computed from the declared hex values in that file via the WCAG relative-luminance formula, not measured in a browser — flagged as such in Open Question 2.