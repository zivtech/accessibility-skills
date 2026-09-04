# Accessibility Design Review — `MainLayout` (Navigation with Skip Link)

**Citation convention**: the fixture supplies no repository paths, so line references are relative to the two code blocks as presented — `MainLayout.jsx:N` counts from `const MainLayout = ({ children }) => {` as line 1, and `MainLayout.css:N` counts from `.skip-link {` as line 1. Every citation below is reproducible against the fixture text.

---

## Phase 0 — Consume Test Evidence

**Evidence-contract type check (fix-verification rule)**: Not applicable. This is a fresh design pass, not a review of a remediation, so there is no claimed fix whose evidence type could be mismatched. Checked and dismissed rather than skipped.

**Scope of the attached pack.** The evidence pack contains 22 axe-core artifacts from batch `axe-batch-2026-08-25`. **Exactly one is the page under review**: `004-127-0-0-1-8777-button-skip-link-clean-html.json`. The other 21 are sibling pages from the same batch run (`accordion-no-region-role`, `file-input-no-labels`, `pagination-no-nav-landmark`, etc.). Their violations — `landmark-one-main`, `region`, `target-size`, `label`, `tabindex`, `color-contrast` — belong to **other** documents and are cited nowhere in this review as evidence about this component. Importing them would be fabrication. They are useful only as a within-batch control, which I use below.

**In-scope measured facts** (`004-...button-skip-link-clean-html.json`, axe-core 4.13.0, viewport 1280x800, HTTP 200, status `measured`):

| Fact | Value |
|---|---|
| Violations | 1 — `page-has-heading-one`, impact `moderate`, tags `cat.semantics` + `best-practice`, `node_count: 1`, selector `html` |
| Incomplete | `[]` — empty |
| Passes | 27 |
| Inapplicable | 62 |

**What the in-scope run positively establishes** (absence-as-evidence, read against the sibling control):

- **`landmark-one-main` did not fire.** It fires on 15 of the 21 siblings. The rendered page therefore has exactly one `main` landmark. This corroborates `MainLayout.jsx:18`.
- **`region` did not fire.** It fires on 13 of the 21 siblings. All page content is inside landmarks — `nav`, `main`, `footer` between them cover everything. This corroborates the landmark design at `MainLayout.jsx:9,18,22` and specifically confirms that wrapping them in a plain `<div className="layout">` did **not** break the `contentinfo`/`main` role mappings (a `div` is not sectioning content, so `<footer>`/`<main>` still map to `contentinfo`/`main`).
- **`target-size` did not fire.** It fires on siblings 000, 014, and 022 with `serious` impact. The `padding: 16px` nav links (`MainLayout.css:39`) clear WCAG 2.5.8 at this viewport.
- **`incomplete: []`.** axe resolved a contrast value for every text node rather than punting — no unresolvable gradient or transparency layers. Its text-contrast pass is therefore trustworthy for this page, unlike siblings 000, 016, and 017 where `color-contrast` landed in `incomplete`.

**What the pack does not contain — and this is the load-bearing limitation of this review:**

- **One viewport only.** `viewports` has a single key, `1280x800`. There is zero evidence about reflow, 200%/400% zoom, or small-viewport behavior.
- **No keyboard evidence.** No Playwright spec, no `agent-browser` trace, no `keyboard-a11y-tester` `trace.json` or `deterministic-findings.json`. No measurement of what happens after the skip link is activated.
- **No screen-reader evidence.** No `virtual-screen-reader` spoken-phrase log, no `screen-reader-census.json`.
- **No focus-indicator measurement.** axe does not evaluate focus-indicator contrast at all — its `color-contrast` rule inspects text against background only. A clean axe contrast result says *nothing* about the focus ring at `MainLayout.css:43`.

Consequence, stated plainly: **every focus-behaviour and reflow claim below is design reasoning, not measured fact.** I flag each one and give the specific measurement that would upgrade it. Per Phase 0's own rule, I note where a claim would be stronger with measurement rather than dressing reasoning up as evidence.

---

## Phase 1 — Pre-commitment Predictions

Written before working through the source, based on component type (page layout + bypass mechanism):

1. **Skip-link target is not focusable** — `<main>` lacks `tabindex="-1"`, so activating the link scrolls but does not move focus.
2. **Skip link hidden with `display:none` or `visibility:hidden`**, removing it from the tab order entirely (the classic catch-22).
3. **Nav "links" are `div`/`span` with click handlers** instead of native `<a>`.
4. **No `aria-current`** marking the active nav item.
5. **Missing or wrong landmarks** — nav not in `<nav>`, content not in `<main>`.
6. **No visible focus indicator** on the skip link or nav links.

Scored against what I actually found, in Phase 10.

---

## Phase 2 — Semantic HTML Audit

This is the strongest part of the component, and I am going to say so rather than hunt for something to complain about.

- **Native elements throughout.** `MainLayout.jsx:5` is a real `<a href>`. `MainLayout.jsx:11–14` are real `<a href>` elements. There is not a single `div role="button"`, no `span` with `onClick`, no `tabIndex` on a non-interactive element. The non-negotiable native-HTML-first rule is satisfied with nothing to flag.
- **No ARIA masking bad structure.** The component contains exactly one ARIA attribute in total: `aria-label` on `<nav>` (`MainLayout.jsx:9`). It *enhances* a native landmark rather than replacing missing semantics. This is the correct ratio.
- **List semantics are real.** `MainLayout.jsx:10–15` uses `<ul>`/`<li>`, not divs styled as a list. `list-style: none` at `MainLayout.css:28` removes the bullets visually. Worth naming explicitly because there is a real Safari/VoiceOver quirk here — `list-style: none` can suppress list-item announcement in Safari — but the mitigation (`role="list"`) is a Safari-specific workaround, not a WCAG defect, and adding it on spec is cargo-culting. Noted in Open Questions, not filed as a finding.
- **Landmarks complete and correctly nested.** `nav` → `main` → `footer` as siblings inside a non-sectioning `div`. Role mapping is intact, and the axe run confirms it empirically (`landmark-one-main` and `region` both silent).
- **No tables, no forms, no layout tables.** The `role="presentation"` checks, the `<th scope="row">` check, and the label-association checks are all inapplicable. Stated so it is clear they were run, not skipped.
- **Heading hierarchy**: the component renders `{children}` (`MainLayout.jsx:19`) and owns no headings itself. See ENHANCEMENT 1 — this is a contract gap, not a semantic error.

**Phase 2 finding count: zero.** The semantics are correct. Manufacturing a MAJOR here would be exactly the failure mode this protocol warns against.

---

## Phase 3 — ARIA Pattern Compliance Audit

There are **no interactive widgets** in this component. No disclosure, no menu button, no tablist, no combobox, no dialog. A static list of links inside a `nav` landmark is not an APG widget pattern and must not be forced into one.

Specifically, and deliberately **not** flagged:

- The nav does **not** need `role="menubar"`/`role="menuitem"`. The APG Menu/Menubar pattern is for application-style command menus with roving tabindex and arrow-key navigation. Site navigation composed of links is correctly a `<ul>` of `<a>` in a `<nav>`. Applying the menu pattern here would *break* screen-reader interaction by removing the links from the links list and suppressing Tab traversal. This is the single most common false MAJOR on navigation components and I am rejecting it on the merits.
- No roving tabindex is required, because there is no composite widget.
- `aria-label="Main navigation"` is a **valid** value in a valid position (see ENHANCEMENT 3 for a wording refinement, not a correctness problem).

**Phase 3 finding count: zero.** The pattern is not 80% complete — there is no pattern to complete.

---

## Phase 4 — Focus Management Review

- **Tab order** follows DOM order and matches visual order: skip link → 4 nav links → `{children}` → footer. Nothing takes `tabindex` > 0 (contrast with sibling `app-focus-order-illogical`, which does and trips axe's `tabindex` rule — this page does not). WCAG 2.4.3 satisfied.
- **Skip link is focusable when hidden.** `MainLayout.css:1–10` hides it with `position: absolute; top: -40px`, **not** `display: none` and **not** `visibility: hidden`. Prediction 2 was wrong, and this is the correct implementation — the gap-analysis anti-pattern about `visibility:hidden` on focus-reveal elements does not apply here.
- **Reveal on focus works.** `MainLayout.css:12–14` sets `top: 0`. Height is ~35px (16px padding + ~19px line box) against `top: -40px`, so it is fully off-screen when unfocused and fully on-screen when focused.
- **No keyboard trap.** No focus handlers, no `preventDefault`, no modal. WCAG 2.1.2 satisfied.
- **No focus indicator suppression.** Nothing sets `outline: none` anywhere. This matters — the most common WCAG 2.4.7 failure is a global `*:focus { outline: none }` reset, and it is absent.
- **`:focus`, not `:focus-visible`, at `MainLayout.css:42`.** This shows the ring on mouse click too. That is *more* visible, not less. Not a finding.
- **No focus obscuring.** No `position: sticky` or `position: fixed` anywhere in the stylesheet, so WCAG 2.4.11 has nothing to catch. The skip link's own `z-index: 100` (`MainLayout.css:9`) puts it above the unpositioned nav when revealed.
- **Skip target does not receive DOM focus.** `MainLayout.jsx:18` is `<main id="main-content">` with no `tabindex="-1"`. See MINOR 1.
- **SPA route changes**: this layout persists across client-side navigations. Where focus goes on route change is owned by the router, not by this file. Flagged as a gap, not a finding — see What's Missing.

---

## Phase 5 — State Communication Audit

There is no state. No loading, no errors, no success messages, no disabled/readonly, no expanded/pressed/selected, no `aria-live` need, no dynamic content, no visual-only indicators, no `+`/`−`/`×` text symbols standing in for state.

The one legitimate state this component *has* — "which page am I on" — is not communicated. See ENHANCEMENT 2.

**Phase 5 finding count: one, at ENHANCEMENT.** WCAG 4.1.3 is inapplicable; there are no status messages to announce.

---

## Phase 6 — Multi-Perspective Review

**Screen reader user (NVDA / JAWS / VoiceOver).** Reaches a well-formed document: a `navigation` landmark named "Main navigation", a list of 4 items, a `main` landmark, a `contentinfo` landmark. Landmark-rotor navigation works — which is itself the mitigating factor for MINOR 1, because an SR user who finds the skip link ineffective has a second, better bypass mechanism built into this same component. Two frictions: the redundant word "navigation" in the landmark name (ENHANCEMENT 3), and no announcement of which nav item is current (ENHANCEMENT 2). No measured SR evidence exists in the pack; this is reasoning from the DOM.

**Keyboard-only user.** First Tab reveals "Skip to main content" — visible, high-contrast (5.57:1 computed), correctly positioned. Enter navigates the fragment. In current Chrome/Firefox/Edge the sequential focus navigation starting point moves to `#main-content`, so the *next* Tab lands inside main and the bypass functionally works even without `tabindex="-1"`. Through the nav, the focus ring is present but low-contrast (MAJOR 1). At narrow widths the nav row likely overflows (MAJOR 2). No keyboard trace exists in the pack, so none of this is measured.

**Low vision user (200%/400% zoom, magnifier, high contrast).** This is the perspective carrying both MAJOR findings, and it is the perspective the evidence pack covers *least* — a single 1280x800 scan measures nothing a low-vision user experiences. The focus ring at 2.27:1 (MAJOR 1) is the exact indicator a magnifier user depends on to keep their place. The non-wrapping flex nav (MAJOR 2) is the exact construct that breaks at 400% zoom. Text contrast itself is fine: nav links 12.6:1, footer 5.27:1, skip link 5.57:1 — all computed from the declared hex values and corroborated by axe's silent, non-`incomplete` contrast pass.

**Cognitive accessibility.** Four short, literal, unambiguous link labels. Conventional ordering. No timeouts, no destructive actions, no forms, no re-entry, no authentication, no cognitive function test. Notably, putting the nav in a shared layout component is *how* WCAG 3.2.3 Consistent Navigation and 3.2.4 Consistent Identification get satisfied by construction — that is a real accessibility property of this architecture, not just an absence of problems. WCAG 3.2.6 Consistent Help is inapplicable: there is no help mechanism to place consistently.

**Vestibular & motion.** Zero `animation`, `transition`, `transform`, `parallax`, or auto-playing content in the stylesheet. `prefers-reduced-motion` is correctly absent because there is nothing to reduce. Adding an empty media query would be noise.

**Auditory access.** No `<video>`, no `<audio>`, no auditory alerts. Fully inapplicable.

**Environmental contrast.** Text contrast passes throughout. Color is never the sole carrier of meaning — there is no status, error, or required-field signalling. No instruction references shape, size, location, or orientation. The one gap is the focus-indicator ratio (MAJOR 1). Forced-colors mode: the `outline` at `MainLayout.css:43` is preserved and re-colored by the OS, and the skip link's `background`/`color` are overridden by the OS to a guaranteed-contrasting pair, so forced-colors is safe by default here.

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | MEDIUM | Skip-link target focus behaviour unmeasured; no `aria-current`; redundant landmark label |
| Keyboard-only | MEDIUM | Bypass mechanism is this component's whole purpose and has zero keyboard measurement in the pack |
| Low vision | **HIGH** | Focus indicator computes to 2.27:1 (below 3:1); non-wrapping flex nav; evidence covers one desktop viewport only |
| Cognitive | LOW | Static link list, no forms, no timeouts, no destructive actions |
| Vestibular & motion | LOW | Zero animation/transition declarations in the stylesheet |
| Auditory access | LOW | No media elements |
| Environmental contrast | MEDIUM | Focus-indicator ratio below threshold; text contrast otherwise passing |

**Escalation**: Low vision at HIGH warrants `/perspective-audit`, and the escalation is worth spending because it is precisely the perspective the supplied evidence cannot speak to.

---

## Phase 7 — Gap Analysis (What Is Absent)

Worked against the gap checklist. Present-and-correct items are listed so it is clear the check ran:

| Gap check | Result |
|---|---|
| Missing skip link | **Present** — `MainLayout.jsx:5` |
| Missing landmark structure | **Present** — nav/main/footer, axe-confirmed |
| Missing list semantics in nav | **Present** — `<ul>/<li>` |
| `visibility:hidden` on focus-reveal element | **Absent** — uses off-screen positioning |
| Missing `inert` on hidden content | Inapplicable — nothing is hidden from AT |
| CSS pseudo-element content exposed to AT | **None** — no `::before`/`::after` declared |
| Font-icon elements exposed to AT | **None** — no icons |
| Missing `lang` attribute | Out of scope — this component owns a `div`, not `<html>` |
| Missing reduced-motion alternative | Inapplicable — no motion |
| Missing touch-target sizing | **Satisfied** — axe `target-size` silent on this page |
| Missing `aria-current` | **Absent** — ENHANCEMENT 2 |
| Missing `<h1>` | **Absent** — measured by axe; ENHANCEMENT 1 |
| Missing focus restoration | Inapplicable — nothing opens or closes |
| Missing reverse skip-link | Inapplicable — 4 nav links, not a deep-content document |
| Missing dragging alternative / consistent help / caption infrastructure / transcripts / media keyboard controls / audio autoplay control | All inapplicable |

**Prior-audit anti-pattern checks** (all nine run):
1. Broadcast vs. association — no `role="alert"` / `aria-live` anywhere. Clean.
2. `title` vs `aria-label` — no `title` attributes. Clean.
3. ARIA without visible label — the nav's `aria-label` names a landmark, not a control standing in for a missing visible label. Clean.
4. Else-branch coverage — no conditional logic in this component. Inapplicable.
5. Single-selector scope — no JS selector manipulation. Inapplicable.
6. `td` in for-loop row headers — no tables. Inapplicable.
7. `role="presentation"` on data tables — no tables. Inapplicable.
8. Empty/decorative alt on content images — no images. Inapplicable.
9. DOM-verification required — applies to the recommended fixes below, and is written into each one.

**Genuine absences carried forward**: `aria-current`; `tabindex="-1"` on the skip target; an `<h1>` contract for `{children}`; a `flex-wrap`/breakpoint on the nav row.

---

## Phase 8 — Realist Check (Severity Calibration)

**Skip target without `tabindex="-1"`** — initially drafted MAJOR.
1. *Realistic worst case*: In Chrome/Firefox/Edge, fragment navigation moves the sequential focus navigation starting point, so the next Tab does land in main and the bypass works. The reliable breakage is narrower: DOM focus is never set, so `document.activeElement` stays on `body` and a screen reader's virtual cursor may not follow — historically the VoiceOver/Safari failure mode.
2. *Group impacted*: screen reader users primarily; keyboard-only users largely unaffected on current browsers.
3. *Detection*: fast — one keyboard pass or a single Playwright `expect(page.locator('#main-content')).toBeFocused()` assertion catches it.
4. *Proportional?* No. **Downgraded MAJOR → MINOR.** **Mitigated by:** the group most likely to hit the failure (screen reader users) has a *better* bypass mechanism available in this very component — the `main` landmark is present and axe-confirmed, so rotor navigation reaches the same destination. The group with no landmark rotor (keyboard-only) is the group current browsers serve correctly. Not downgraded to ENHANCEMENT, because `tabindex="-1"` is the settled universal practice for skip targets and the fix is one attribute.

**Focus indicator contrast 2.27:1** — held at MAJOR.
1. *Realistic worst case*: a low-vision or magnifier user tabbing the nav cannot reliably locate focus; blue-on-dark-grey at 2.27:1 is a hue change with almost no luminance change.
2. *Group impacted*: low vision, magnifier users, anyone in bright ambient light.
3. *Detection*: **never, silently.** axe does not evaluate focus-indicator contrast, so the clean scan in the pack gives false assurance. This ships and is discovered only by a human tester or an affected user.
4. *Proportional?* Yes. **Survives — not downgraded.** The "workaround exists" downgrade rule was considered and rejected: counting position across four links is not a workaround, it is coping. Silent-failure mode weighs against downgrading.

**Nav reflow at 320px** — held at MAJOR, confidence reduced.
1. *Realistic worst case*: two-dimensional scrolling at 400% zoom on every page of the site, since this is the shared layout.
2. *Group impacted*: low vision.
3. *Detection*: fast if anyone resizes; never, if nobody does — and the supplied evidence proves nobody did, because only 1280x800 was scanned.
4. *Proportional?* Yes as to impact — WCAG 1.4.10 is Level AA and "scroll sideways" is the exact remedy the criterion exists to forbid. **Severity held, confidence set to MEDIUM** because the overflow width is computed from declared CSS with estimated glyph metrics, and a breakpoint in a stylesheet I was not given would void it. Refutation path stated in the finding.

---

## Phase 9 — Self-Audit

| Finding | Confidence | Refutable by developer context? | Gap or preference? |
|---|---|---|---|
| MAJOR 1 — focus ring 2.27:1 | **HIGH** (arithmetic from declared hex; no images, gradients, or transparency in play — corroborated by axe's empty `incomplete`) | No — both adjacent surfaces are `#333` from `MainLayout.css:23`, and the link element declares no background of its own | GAP |
| MAJOR 2 — nav reflow | **MEDIUM** | **Yes** — an unseen media query or a mobile nav swap would void it | GAP (conditional) |
| MINOR 1 — skip target focus | **HIGH** that the attribute is required practice; **MEDIUM** on the exact per-browser breakage | Partially — a global focus-management utility could set it at runtime | GAP |
| ENHANCEMENT 1–3 | HIGH | No | GAP, but below finding threshold |

Applying the rules: MAJOR 2 is refutable, so its refutation condition is stated inline in the finding and the verification step is given, rather than asserting it flatly. Nothing here is LOW confidence. Two candidate items were rejected outright as PREFERENCE and are recorded in Open Questions so the rejection is auditable rather than invisible.

**No `A11y Evidence Finding` blocks are emitted in this review, deliberately.** The contract is reserved for CRITICAL/MAJOR findings backed by *measured* evidence. Both MAJORs here are computed from declared CSS, not measured in a browser; the one genuinely measured item (`page-has-heading-one`) sits at ENHANCEMENT, below the block's threshold. Emitting blocks with `source:` pointing at a CSS line would be inventing fields to make derived reasoning look instrumented — which the contract explicitly forbids.

---

# VERDICT: ACCEPT-WITH-RESERVATIONS

**Overall Assessment**: The accessibility *markup* here is genuinely correct and I am not going to manufacture a structural problem in it — native elements throughout, complete and axe-confirmed landmarks, real list semantics, a properly-hidden-but-focusable skip link, and exactly one ARIA attribute, correctly used. Both reservations live entirely in the **stylesheet**: a focus indicator that computes to 2.27:1 against its own background, and a non-wrapping flex nav row that will not survive 400% zoom. That migration is the real story of this review — this component's accessibility risk has moved out of the HTML, where the attached evidence looks, and into the CSS, where a single-viewport axe scan has no reach at all.

**Pre-commitment Predictions vs. Findings**:

| # | Prediction | Outcome |
|---|---|---|
| 1 | Skip target not focusable | **HIT** — confirmed at `MainLayout.jsx:18`, but recalibrated down to MINOR once the landmark-rotor mitigation was accounted for |
| 2 | Skip link hidden with `display:none`/`visibility:hidden` | **MISS** — correctly uses off-screen positioning |
| 3 | Nav items are divs with click handlers | **MISS** — native `<a>` throughout |
| 4 | Missing `aria-current` | **HIT** — filed at ENHANCEMENT per this skill's own severity scale |
| 5 | Missing/wrong landmarks | **MISS** — complete, and independently confirmed by axe's silence on `landmark-one-main` and `region` |
| 6 | No visible focus indicator | **MISS, and the more interesting result** — I predicted *absence* and found *insufficiency*. The indicator exists and looks deliberate; it is 0.73 short of the threshold. Predicting the presence/absence axis blinded me to the quality axis. |

**Genuine surprise**: the reflow issue. I predicted six failure modes and did not predict the one most likely to bite in production. Nothing in a skip-link-plus-landmarks mental model points at `flex-wrap`, and nothing in the evidence pack could have prompted it — which is exactly why it needed a design pass rather than another scanner.

---

## Findings

### Critical Findings (blocks access)

**None.** No user category is blocked. Screen reader users have complete landmark navigation; keyboard users have a working tab order and no traps; there is no state that fails silently. Stating this plainly rather than promoting a MAJOR to fill the section.

### Major Findings (significantly degrades experience)

**MAJOR 1 — Nav focus indicator computes to 2.27:1 against its own background, below the 3:1 threshold.**

Evidence: `MainLayout.css:42–45`

```css
.main-nav a:focus {
  outline: 3px solid #0066cc;
  outline-offset: -3px;
}
```

The indicator colour is `#0066cc` (relative luminance 0.1386). `outline-offset: -3px` draws the ring **inside** the link box, so both its outer and inner neighbours are the nav's `background: #333` (`MainLayout.css:23`, relative luminance 0.0331). The link element declares no background of its own (`MainLayout.css:35–40`), so `#333` shows through on both sides. Contrast change against adjacent colours: **(0.1386 + 0.05) / (0.0331 + 0.05) = 2.27:1**. Required: 3:1.

- **Confidence**: HIGH. Computed from the declared hex values; there are no images, gradients, or transparency layers to confound it, and axe's empty `incomplete` array confirms it resolved every colour on this page cleanly.
- **User group**: Low vision, magnifier users, users with reduced contrast sensitivity, anyone in bright ambient light. Keyboard-dependent users specifically — this is the only signal telling them where they are.
- **WCAG**: 1.4.11 Non-text Contrast (Level AA) — Understanding 1.4.11 covers the visual information required to identify component *state*, which includes focus indicators. Reinforced by 2.4.13 Focus Appearance, which requires a 3:1 contrast change on at least a 2px perimeter — note honestly that 2.4.13 is **Level AAA** in WCAG 2.2 and is cited here as corroboration, not as the AA basis.
- **Why this matters**: The 3px ring is thick enough to satisfy the area requirement and clearly deliberate — someone thought about this. But `#0066cc` on `#333` is almost pure hue change with negligible luminance change, so for a user with reduced contrast sensitivity the ring is close to invisible against the dark bar. They tab through four links with no reliable position feedback. And **nothing in the attached evidence would ever catch this**: axe's `color-contrast` rule inspects text against background only and does not evaluate focus indicators, so the clean scan on `004` is silent here by design, not by verification. This is the definitional silent failure — it ships, and only a human tester or an affected user finds it.
- **Fix**: Raise the indicator's luminance contrast against `#333`. `outline: 3px solid #ffffff` gives 12.63:1; `#66b3ff` gives roughly 6.9:1 while keeping the brand hue. Alternatively keep `#0066cc` and add a contrasting companion — `outline: 3px solid #0066cc; box-shadow: 0 0 0 6px #fff;` — so the pair reads at any sensitivity. Then **verify in DOM**: focus a nav link in DevTools, sample the rendered outline pixel and the adjacent `#333` pixel with the browser's contrast picker, and confirm ≥ 3:1. Do not treat a passing axe run as verification of this fix — axe does not measure it.

---

**MAJOR 2 — Nav is a non-wrapping flex row with no breakpoint; it will overflow horizontally at 320px / 400% zoom.**

Evidence: `MainLayout.css:27–33` and `MainLayout.css:35–40`

```css
.main-nav ul { display: flex; gap: 20px; }   /* flex-wrap defaults to nowrap */
.main-nav a  { display: block; padding: 16px; }
```

Computed minimum row width at the default 16px font: link text ≈ 193px (Home ≈ 34 + About ≈ 41 + Services ≈ 62 + Contact ≈ 56) + horizontal padding 4 × 32px = 128px + gaps 3 × 20px = 60px → **≈ 381px**. WCAG 1.4.10 requires reflow without two-dimensional scrolling at a 320 CSS px viewport width. Nothing in the supplied stylesheet declares `flex-wrap: wrap`, sets `overflow-x`, or introduces a media query, so the overflow propagates to the document and produces page-level horizontal scrolling.

- **Confidence**: **MEDIUM.** The direction is solid — `flex-wrap` defaults to `nowrap` and there is no breakpoint in the CSS as given — but the exact overflow threshold depends on the inherited font family and size, which the fixture does not specify. **Explicit refutation path**: if a media query, a mobile nav swap, or a hamburger pattern exists in a stylesheet outside this fixture, this finding is void. I cannot see the rest of the project and am not asserting otherwise.
- **User group**: Low vision (400% zoom is the WCAG-equivalent of a 320px viewport), plus every small-screen user.
- **WCAG**: 1.4.10 Reflow (Level AA).
- **Why this matters**: This is the shared layout, so the failure is not one page — it is every page. And "you can scroll sideways" is the precise remedy 1.4.10 exists to eliminate, so the usual workaround-based downgrade does not apply. Note where the evidence stands: the axe artifact's `viewports` object contains the single key `1280x800`. **No one has ever measured this component below desktop width.** The clean scan is not evidence of small-viewport health; it is evidence that small viewports were never in scope.
- **Fix**: Add `flex-wrap: wrap` to `.main-nav ul`, or introduce a breakpoint that stacks the list vertically below ~600px. Then **verify in DOM**: load at a 320px viewport (or 1280px at 400% zoom) and confirm `document.documentElement.scrollWidth <= document.documentElement.clientWidth`. Worth adding a second viewport to the axe batch so this stops being unmeasurable — the harness clearly supports a `viewports` map and currently populates one key.

### Minor Findings (friction, workaround exists)

**MINOR 1 — Skip-link target `<main id="main-content">` has no `tabindex="-1"`, so activating the link never sets DOM focus.** `MainLayout.jsx:18`, targeted by `MainLayout.jsx:5`. On current Chrome/Firefox/Edge, fragment navigation moves the *sequential focus navigation starting point*, so the next Tab does land inside main and keyboard-only users are largely served. But DOM focus is never set — `document.activeElement` stays on `body` — so a screen reader's virtual cursor is not guaranteed to follow, the long-standing VoiceOver/Safari failure. WCAG 2.4.1 Bypass Blocks. **Recalibrated from MAJOR. Mitigated by:** the affected group has a better bypass in this same component — the `main` landmark is present and axe-confirmed, so rotor navigation reaches the identical destination. **Fix**: `<main id="main-content" tabIndex={-1}>`, and add `#main-content:focus { outline: none }` only if the ring on the container is visually unwanted — never as a global reset. Verify with `expect(page.locator('#main-content')).toBeFocused()` after activating the link.

### Enhancements (best practice not met, no access barrier)

**ENHANCEMENT 1 — No `<h1>` on the rendered page, and the layout defines no heading contract for `{children}`.** This is the review's **one measured finding**: axe reports `page-has-heading-one`, `impact: moderate`, `node_count: 1`, selector `html`. Calibration matters here — its tags are `cat.semantics` and **`best-practice`**, *not* a `wcag*` tag. No WCAG 2.2 A/AA success criterion requires an `<h1>`, and a reviewer who calls this a WCAG violation is wrong. It is still worth acting on: this layout owns `<main>` and the skip destination, so it is the natural place to state that consumers must render an `<h1>` as the first heading in `{children}` — via a prop type, a documented contract, or a dev-mode assertion.

**ENHANCEMENT 2 — No `aria-current` on the active nav item.** `MainLayout.jsx:11–14`. Screen reader users get no "you are here" signal in a nav that appears on every page. Filed at ENHANCEMENT to match this skill's own severity scale, which lists exactly this case there. **Fix**: `aria-current={isActive ? 'page' : undefined}` — the value is `"page"`, never `"true"`, and the attribute must be *absent* on inactive items rather than `"false"`.

**ENHANCEMENT 3 — `aria-label="Main navigation"` duplicates the role in the announcement.** `MainLayout.jsx:9`. Screen readers append the landmark role, so this is announced as roughly "Main navigation, navigation, landmark." **Fix**: `aria-label="Main"`. Genuinely marginal — the label is functional as written — but it costs one word and this is a per-page announcement.

---

## What's Missing

- **A heading contract for `{children}`** — the layout provides the skip destination but nothing guarantees a heading exists at it. Measured by axe on the rendered page (ENHANCEMENT 1).
- **A responsive strategy for the nav** — no `flex-wrap`, no breakpoint, no mobile pattern anywhere in the supplied CSS (MAJOR 2).
- **Current-page state** — the one piece of state this component has, uncommunicated (ENHANCEMENT 2).
- **SPA route-change focus management** — this layout persists across client-side navigations, and client-side routing does not reset focus the way a document load does. The router, not this file, owns the fix, so it is not filed as a finding against `MainLayout` — but a layout component is where teams usually discover the gap, and the `<main tabindex="-1">` added for MINOR 1 is the same handle a router-level focus reset needs. Worth raising with whoever owns routing.
- **`lang` on `<html>`** — this component renders a `div`, not the document, so the attribute is out of scope here. Verify at the document shell.
- **Any keyboard, screen-reader, or multi-viewport measurement.** The pack is one axe scan at one viewport. There is no `trace.json`, no spoken-phrase log, no second `viewports` key. For a component whose entire purpose is a *keyboard* bypass mechanism, the attached evidence measures none of the behaviour that matters. That is the largest gap in this review and it is a gap in the evidence, not in the code.

---

## Multi-Perspective Notes

- **Screen reader user**: Well-formed document — `navigation` landmark named "Main navigation", a 4-item list, `main`, `contentinfo`, all confirmed present by axe's silence on `landmark-one-main` and `region`. Frictions: redundant "navigation" in the landmark name, no current-page signal, and an unmeasured cursor jump after the skip link. The landmark rotor is a genuine second bypass and is why MINOR 1 is not a MAJOR.
- **Keyboard-only user**: Clean DOM-order tab sequence, no `tabindex` > 0, no traps, no `outline: none` reset anywhere. The skip link reveals correctly and reads at 5.57:1 while focused. Once inside the nav, the focus ring is present but low-contrast (MAJOR 1). Everything in this paragraph is design reasoning — the pack contains no keyboard measurement whatsoever.
- **Low vision user (200%/400% zoom, high contrast)**: The perspective at HIGH alarm and the one the evidence covers least. Text contrast is fine everywhere (nav 12.63:1, footer 5.27:1, skip link 5.57:1, all computed and corroborated by axe's clean non-`incomplete` contrast pass). The two failures are the 2.27:1 focus ring and the non-wrapping nav row — the exact two things a single desktop-viewport text-contrast scan cannot see. Forced-colors mode is safe: outlines are preserved and re-colored by the OS, and the skip link's colour pair is overridden wholesale.
- **Cognitive accessibility**: Strong, and structurally so. Four literal labels in conventional order; no timeouts, destructive actions, forms, re-entry, or authentication. Housing the nav in a shared layout is *how* WCAG 3.2.3 Consistent Navigation and 3.2.4 Consistent Identification are satisfied by construction across the site — an architectural accessibility property, not merely the absence of defects. 3.2.6 Consistent Help is inapplicable; no help mechanism exists.

---

## Verdict Justification

**ACCEPT-WITH-RESERVATIONS.** The markup layer is correct, and that judgment is backed by measurement rather than inspection alone: within the same axe batch, `landmark-one-main` fires on 15 of 21 sibling pages and `region` on 13 of 21, while this page trips neither. Its only violation is a `best-practice`-tagged missing `<h1>` that this component does not own. Nothing in the ARIA, semantics, or focus-order design needs rethinking, and I explicitly declined to invent a structural finding — the nav is correctly *not* an APG menubar, the `div` wrapper correctly does *not* break the landmark mappings, and the skip link is correctly *not* hidden with `visibility: hidden`.

The reservations are two CSS values, both invisible to the attached evidence by construction.

**Recalibrations applied in Phase 8**: skip-target focus MAJOR → MINOR (mitigated by the axe-confirmed landmark rotor serving the same users better); focus-ring contrast held at MAJOR (workaround downgrade considered and rejected — counting link positions is coping, not a workaround, and the failure is silent); reflow held at MAJOR with confidence reduced to MEDIUM and its refutation condition stated inline rather than buried.

**To upgrade to ACCEPT**: raise the focus-indicator contrast to ≥ 3:1 against `#333` and verify it by pixel sampling, not by re-running axe; add `flex-wrap: wrap` or a breakpoint and verify `scrollWidth <= clientWidth` at 320px; add `tabIndex={-1}` to `<main>`. The three enhancements are optional for the verdict.

**To downgrade to REVISE**: if a 320px check confirms the overflow *and* no breakpoint exists elsewhere in the project, MAJOR 2 becomes an unambiguous Level AA failure shipping on every page of the site, and that is not shippable at the stated target.

**Escalation**: Low vision is at HIGH — `/perspective-audit` is warranted, and unusually well-justified here, because it is the one perspective the evidence pack structurally cannot address.

**A note on the evidence pack, since it shapes every confidence rating above**: 21 of the 22 attached artifacts describe other documents. The single in-scope artifact is one axe run, at one viewport, on a rule set that does not evaluate focus indicators, reflow, keyboard behaviour, or announcements. It is real evidence and I used it — the landmark and target-size conclusions rest on it directly, and the absence-versus-sibling-control reading is stronger than any inspection I could do by eye. But a clean scan from an instrument that cannot see the two failures found here is not a clean bill of health, and reading it as one is exactly how both MAJORs would have shipped.

---

## Open Questions (unscored)

1. **Does a stylesheet outside this fixture handle the nav at small viewports?** A media query, a hamburger swap, or a `flex-wrap` declaration elsewhere would void MAJOR 2 entirely. Check: `grep -rn "main-nav" --include=*.css --include=*.scss` across the project.
2. **Is the app using a hash router?** If so, `href="#main-content"` (`MainLayout.jsx:5`) could be intercepted and interpreted as a route change to `/main-content`, breaking the skip link outright. Not filed as a finding because nothing in the fixture indicates a router. Check: is the app mounted under `HashRouter`?
3. **Does repeat activation of the skip link still work?** Once the URL ends in `#main-content`, a second click produces no fragment change. Browsers generally re-scroll on same-hash activation, but this varies and I will not assert it. Check: activate the skip link twice in Chrome and Safari; confirm focus/scroll lands in main both times.
4. **`list-style: none` and Safari/VoiceOver list announcement.** `MainLayout.css:28` can suppress list-item announcement in Safari. Not filed — it is a browser-specific quirk, not a WCAG defect, and adding `role="list"` on spec is cargo-culting. Raised only so the decision is auditable. Check: VoiceOver + Safari, confirm "list, 4 items" is announced.
5. **REJECTED as preference, recorded so the rejection is visible**: (a) *"Add `prefers-reduced-motion`"* — there is no motion; an empty media query is noise. (b) *"Use `:focus-visible` instead of `:focus`"* — the current `:focus` shows the ring to mouse users too, which is more accessible, not less. Neither belongs in the findings above and neither should be re-raised by a later pass.
