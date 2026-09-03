I'll read the single file I've been given and run the full protocol against it.

---

**VERDICT: REVISE**

**Overall Assessment**: One real design defect: the three map controls are anchors with `javascript:void(0)` hrefs performing in-place actions, so they are announced and navigable as links while looking and behaving like buttons. Everything else in this component is deliberately sound — the new-tab disclosure, focus indicator, contrast, section labeling, and text-alternative link are all correct and should not be touched. The fix is a one-element swap, but the defect ships silently past automated scanners.

---

**Pre-commitment Predictions** (written before reading the code, from the component type "map panel with zoom/reset controls"):

1. Zoom/reset implemented as `div` or `a` with click handlers instead of `<button>` — **CONFIRMED** (`pseudo-link-map-controls.md:27,30,33`)
2. Map canvas has no text alternative / no keyboard operability — **PARTIALLY REFUTED**; a text-alternative table link is present and precedes the controls in DOM order (`:20-24`). Canvas operability is unverifiable from this file → Open Questions.
3. Zoom state changes not announced to AT — **CONFIRMED but downgraded**; real gap, weak SC hook, and mitigated by the alternative table.
4. Touch targets under minimum — **REFUTED**. Computed ≈83×33 CSS px; passes 2.5.8 AA (24×24). See Enhancements for the AAA note.
5. Focus indicator missing or low-contrast on a map surface — **REFUTED**. `:focus-visible` is defined with adequate contrast (`:90-93`).

I was surprised by how much of this component is correct. Three of five predictions did not survive contact with the source. Prediction 4 is the one I would have gotten wrong if I had asserted it from pattern rather than computing it.

---

**Critical Findings** (blocks access): none.

---

**Major Findings**

**1. Zoom in / Zoom out / Reset view are anchors performing button actions — wrong role exposed to assistive technology**

Evidence — `pseudo-link-map-controls.md:27,30,33`:
```jsx
<a href="javascript:void(0)" className="map-control" onClick={handleZoomIn}>
```
Reinforced visually as buttons by `pseudo-link-map-controls.md:80-88` (border, padding, background, `text-decoration: none`, `cursor: pointer`), and confirmed non-navigational by the spec at `pseudo-link-map-controls.md:137` ("none of them navigates the browser anywhere or changes the URL").

- **Confidence**: HIGH
- **User groups impacted**: screen reader (primary), keyboard-only (secondary), motor/cognitive (tertiary)
- **Expected behavior**: WCAG 2.2 **4.1.2 Name, Role, Value** — the role exposed must match the element's function. An element that performs an in-page action and does not navigate is a button. Native HTML first: `<button type="button">` supplies the role, Enter *and* Space activation, and the correct AT gestures with no ARIA.
- **Why this matters** — three distinct concrete harms, not one abstract one:
  - **Structural navigation breaks.** NVDA/JAWS `B` (next button) and the VoiceOver rotor's Buttons list skip these entirely — the panel's Buttons collection is empty. Meanwhile `K` / the Links list surfaces "Zoom in", "Zoom out", "Reset view" as if they were destinations. A screen reader user hunting for map controls by the correct navigation key never finds them.
  - **Space does nothing.** A sighted keyboard user reads a button, presses Space, and the page scrolls. Links do not activate on Space. There is no error, no feedback, no clue. (I am **not** citing 2.1.1 Keyboard here — Tab+Enter does reach and fire the handler, so 2.1.1 passes. This is a 4.1.2 role-mismatch consequence, and I am rating it as such rather than inflating it into a keyboard-operability failure.)
  - **Link affordances are false.** Middle-click, Ctrl/Cmd-click, and "Open link in new tab" produce a dead blank tab; "Copy link address" yields `javascript:void(0)`. Touch AT (VoiceOver iOS, TalkBack) announce "Link. Double tap to open," promising navigation that never happens.
- **Fix**:
  ```jsx
  <div className="map-controls" role="group" aria-label="Map view controls">
    <button type="button" className="map-control" onClick={handleZoomIn}>Zoom in</button>
    <button type="button" className="map-control" onClick={handleZoomOut}>Zoom out</button>
    <button type="button" className="map-control" onClick={handleReset}>Reset view</button>
  </div>
  ```
  CSS at `:80-93` needs no change beyond adding `font: inherit;` and `appearance: none;` to `.map-control` so the native button inherits the panel's type. Do **not** patch this with `role="button"` + `onKeyDown` on the anchors — that is ARIA masking a native element that already exists, and it still leaves a `javascript:` href in the accessibility tree.
- **Realist Check applied — held at MAJOR, not raised to CRITICAL**: Tab+Enter still reaches and activates every control, and the map's data has an equivalent alternative reachable earlier in DOM order (`:21-23`), so no user category is fully blocked. Not downgraded to MINOR either: there is no workaround for the broken structural navigation, and **no axe-core or Pa11y rule flags an anchor used as a button** — axe checks link *name*, not link *appropriateness*. This defect passes an automated scan clean and only surfaces under manual AT testing, so "detection is fast" does not apply.

---

**Minor Findings**

- **No non-visual feedback when zoom changes** — `pseudo-link-map-controls.md:7-9` handlers mutate map state with no `role="status"` / live region anywhere in the component. A screen reader user who activates "Zoom in" perceives nothing at all and cannot tell whether the control worked. I am rating this MINOR, not MAJOR, and I want to be explicit that **the SC hook here is weak**: 4.1.3 Status Messages governs advisory status text, and a map viewport change is content, not a status message — citing 4.1.3 would be a stretch I am declining to make. It is a genuine design gap on cognitive and screen-reader grounds. *Mitigated by*: the text-alternative table link at `:20-24` precedes the controls in DOM order, so a linear reader encounters the accessible path to the same data before reaching controls that cannot help them. **Fix**: add `<p role="status" className="visually-hidden">` updated to e.g. "Zoom level 4 of 8" / "Map view reset."

- **DOM order does not match the stated layout intent** — `pseudo-link-map-controls.md:136` specifies the three actions appear *above* the map, but `.map-controls` (`:26`) sits after both the canvas (`:18`) and the alt-link paragraph (`:20`), and the CSS (`:74-78`) applies no `order`, `flex-direction: column-reverse`, or positioning that would move them. As written, DOM order and visual order **agree** (controls render below the map), so **this is not a 1.3.1 or 2.4.3 failure today** — I am explicitly not manufacturing one. It is a spec/implementation discrepancy, and it becomes a Focus Order finding the moment someone satisfies line 136 with CSS reordering rather than by moving the markup. Flagging it now so the fix lands in markup.

- **"Open full report" does not disclose the file format** — `pseudo-link-map-controls.md:39-42` correctly warns about the new tab but not that the target is a PDF (per `:138`). Cognitive and screen-reader users benefit from knowing before they leave. Extend the visually-hidden span to " (PDF, opens in a new tab)". Not an SC failure; 2.4.4 is satisfied by the existing name.

---

**Enhancements**

- No group label on `.map-controls` (`:26`). `role="group"` + `aria-label="Map view controls"` gives AT users a boundary around the three actions. Folded into the Major fix above.
- Targets are ≈83×33 CSS px (`:81` padding `6px 14px`, plus 1px borders, over inherited ~16px text). **This passes WCAG 2.2 SC 2.5.8 Target Size (Minimum), which is 24×24 at Level AA** — it fails only 2.5.5 Target Size (Enhanced) at AAA, which is outside this project's AA target. Recording this explicitly because "44×44 minimum under 2.5.8" is a common miscitation; 44×44 is the AAA criterion. No change required.
- No visible zoom-level indicator for anyone. Sighted users also cannot tell how far in they are or that "Zoom in" has bottomed out.
- No `prefers-reduced-motion` block. Nothing in this CSS animates, but the third-party map library's zoom transition likely does, and this component is where the override would live.

---

**What's Missing**

- **A button anywhere in this component.** The panel has four interactive elements and all four are `<a>`. Two of them (`:21`, `:39`) are legitimately links; the three at `:27,30,33` are not. The accessibility tree for this panel contains zero buttons.
- **Any programmatic representation of map state.** No current zoom level, no `aria-disabled` at zoom limits, no announcement of the reset having occurred.
- **Any handling for the controls' zoom-limit edges.** At maximum zoom, "Zoom in" presumably becomes a no-op with no indication to any user.
- **Verification that the mounted map canvas is itself operable.** `:18` is an empty div awaiting a third-party mount; nothing in this file establishes whether the resulting widget is focusable, keyboard-pannable, labeled, or a focus trap.

---

**Multi-Perspective Notes**

- **Screen reader user**: Landmark and heading structure are correct — `<section aria-labelledby="map-heading">` at `:12` with a matching `<h2 id="map-heading">` at `:13` resolves cleanly and exposes a named region. Reading order is sensible: heading → map → text-alternative link → controls → report link. The failure is the links-vs-buttons role mismatch (`:27,30,33`) and the total absence of feedback when a control fires. The new-tab disclosure at `:41` is done correctly and produces the accessible name "Open full report (opens in a new tab)".
- **Keyboard-only user**: All four interactive elements are focusable in logical DOM order; no traps; no positive `tabindex`; no hidden-but-focusable content. `:focus-visible` at `:90-93` gives a 3px outline with 2px offset — #0b5fff on #ffffff computes to **≈5.1:1**, clearing the 3:1 required by 1.4.11 / 2.4.7 with margin. (Ratio computed from the source hex values, not measured by a scanner — see Verification Gaps.) The single defect is Space failing on button-styled controls.
- **Low vision (200% zoom, high contrast, magnifier)**: `max-width: 640px` with `margin: auto` (`:55-56`) and a `flex` control row with `gap: 12px` (`:74-77`) reflow without horizontal scroll. Body text at #0b5fff on white computes ≈5.1:1, clearing 4.5:1 for 1.4.3. Focus outline is 3px — visible under magnification. In Windows High Contrast Mode the `.map-control` background/border are overridden by the forced palette, but because they are anchors they will be forced to the *link* color, not the *button* color — one more place the wrong role produces the wrong signal. Note that `.map-alt-link a` and `.map-report-link a` (`:99`, `:112`) set color only and **do not** set `text-decoration: none`, so the UA underline is retained — **there is no 1.4.1 Use of Color failure here** and I am not reporting one.
- **Cognitive accessibility**: Control labels are plain, specific, and jargon-free. The text-alternative link is descriptive out of context ("View watershed boundaries as a data table"), satisfying 2.4.4. The new-tab warning is present *before* the user leaves. Two frictions: "Reset view" silently discards the user's zoom/pan state with no undo and no confirmation (3.3.4 does not apply — no legal, financial, or data-deletion consequence — so this is advisory only), and no user can tell what zoom level they are currently at.

---

**Verdict Justification**

REVISE rather than ACCEPT-WITH-RESERVATIONS because the Major finding is a role-level defect affecting the component's primary interaction, it is invisible to automated tooling, and the fix is small and unambiguous. REVISE rather than REJECT because exactly one thing is wrong: the semantic structure, focus management, contrast, focus visibility, text alternative, and new-tab handling are all already correct, and a REJECT would misrepresent a well-built component with one bad element swap.

**Recalibrations performed:**
- Finding 1: initial instinct CRITICAL → held at **MAJOR**. Enter still activates; an equivalent data path exists earlier in DOM. Not downgraded further despite the workaround, because structural AT navigation has no workaround and no scanner catches this.
- Prediction 3 (zoom announcements): drafted as MAJOR → **MINOR**. The 4.1.3 citation does not survive scrutiny (a viewport change is not a status message), and the alternative table mitigates. Reported as a design gap with the weak citation stated rather than dressed up.
- Prediction 4 (target size): drafted as a finding → **removed to Enhancements**. Computed dimensions pass 2.5.8 AA; only the AAA criterion fails.
- Layout-order observation: drafted as a 2.4.3 finding → **MINOR non-failure**. DOM and visual order currently agree; flagging the future risk, not asserting a present violation.

**Deliberately not reported** (component scope, and over-flagging page-shell absences is a known failure mode): missing `<main>`/`<nav>`, missing skip link, missing `lang` on `<html>`, and the absence of an `<h1>`. None of these are visible in the supplied excerpt and none are this component's responsibility. Also not reported: "missing `onKeyDown`" on the three controls — anchors with an `href` fire `click` on Enter natively, so that would be a false positive.

**Verification gaps** (Phase 0 produced nothing — no axe-core run, no Playwright spec, no agent-browser trace, no keyboard-a11y-tester or virtual-screen-reader artifacts accompanied this file): every contrast figure above is **computed from the source hex values, not measured**, and every AT-announcement claim is derived from role semantics rather than observed in a spoken-phrase log. Both would be stronger as measured facts. The Major finding does not depend on either — it rests on the element type in the source.

---

**Open Questions (unscored)**

1. **Is the mounted map itself keyboard-operable?** `:18` is an empty container for a third-party library. If the mounted widget is drag-only, 2.1.1 fails at the map level — a far larger issue than the control roles. Not assessable from this file.
2. **Does the map canvas expose an accessible name or role once mounted?** If it renders an unlabeled canvas or SVG, AT users hit an opaque void. If the table at `:21-23` is genuinely a conforming alternative version, `aria-hidden="true"` on the container may be right — but only if nothing inside it is focusable, or you create a keyboard trap that AT users cannot see.
3. **What happens at zoom limits?** No `aria-disabled`, no `disabled`, no announcement. Whether this matters depends on library behavior I cannot see.
4. **Is line 136's "above the map" the real design intent, or stale spec text?** If it is real, move the markup rather than reordering with CSS.
5. **Is `/reports/watershed-2026` a tagged, accessible PDF?** Line 138 says the target is a PDF. Its own conformance is untested and out of this component's scope, but it is in the panel's user journey.

---

## Provenance

Files read for this review — this is the complete list:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt-siblings-rows/prompts/pseudo-link-map-controls.blind.md` (one `Read` call, entire file, 139 lines)

No other file was opened. I ran no `Grep`, no `Glob`, no `Bash`, and no `git` command. I did not read anything under `evals/suites/`, any `*.metadata.yaml`, any `*.rubric.yaml`, or any other fixture, result, or documentation file in this or any repository. Line citations use the line numbers of the file as given to me. Contrast ratios were computed by hand from the sRGB hex values in that file's CSS block using the WCAG relative-luminance formula; no scanner or measurement tool was run.