I'll read the file and review it.

---

## Verdict: REVISE

One unambiguous MAJOR defect, one conditional MAJOR needing verification, plus MINOR/ENHANCEMENT items.

### Findings

**F1 — MAJOR — 4.1.2 Name, Role, Value — `:27`, `:30`, `:33`**
The three map controls are `<a href="javascript:void(0)">` performing in-page actions. Line 137 states none of them navigates. Screen readers announce "link"; the actions pollute the links-list rotor; Space doesn't activate them despite `.map-control` (`:80`–`:88`) styling them to look exactly like buttons. Enter does work, so this isn't a 2.1.1 failure — it's the operability cost of the role lie. `javascript:` URIs also break under strict CSP. Fix: `<button type="button">`.

**F2 — MAJOR (conditional, needs verification) — 2.5.7 Dragging Movements / 2.1.1 — `:26`–`:36`, `:137`**
Line 137 says the controls update "zoom/pan state," but only zoom and reset exist — no pan control, no keyboard affordance on the canvas (`:18`). If the third-party library pans by drag (the usual default), that's a 2.5.7 and 2.1.1 failure. Not confirmable from this file; flagged for verification, not filed as confirmed.

**F3 — MINOR — 4.1.3 (soft mapping) — `:27`–`:35`** No feedback on activation; no way to know a zoom limit was hit. SC mapping is arguable — flagged on impact to low-vision and cognitive users, not rule weight. MINOR because a blind user gets nothing from the canvas either way.

**F4 — ENHANCEMENT — 1.1.1 met but weak — `:18`, `:20`–`:24`** The comment at `:15`–`:17` is correct that the linked table is a real text alternative. Not a failure. But the tie between the empty canvas div and the link is spatial only.

**F5 — ENHANCEMENT — `:26`** No group name on `.map-controls`.
**F6 — ENHANCEMENT — `:39`, `:138`** Link doesn't disclose the PDF format (new-tab warning at `:41` is correctly done).
**F7 — MINOR (conditional) — `:136` vs `:26`** Spec says controls are "above the map"; DOM renders them after it, with no CSS reorder — so no violation today. Flagged because satisfying line 136 with CSS instead of JSX would split visual and focus order.

### Checked and deliberately not flagged
Contrast (`#0b5fff` on `#fff` ≈ 5.13:1, passes 1.4.3 and 1.4.11); focus visibility (`:focus-visible` is the right selector, 3px outline everywhere); target size (~33×83px, clears 2.5.8); the new-tab warning (span inside the anchor, correct clip-rect at `:121`, `rel` present); `text-decoration: none` at `:86` (no adjacent body text, so not 1.4.1); missing `<h1>` (out of component scope); third-party canvas internals.

Full review sent to team-lead.

## Provenance
- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt-siblings-rows/prompts/pseudo-link-map-controls.blind.md`

No other files read; no grep, no git, no skill invoked.