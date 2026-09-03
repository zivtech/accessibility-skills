I'll start by reading the single file I'm permitted to read.

---

**VERDICT: REVISE**

**Overall Assessment**: The static accessibility of this shell is genuinely good — correct landmarks, a labeled nav, native `<button>`, one `<h1>` per view, visible focus rings that pass contrast, no ARIA papering over bad HTML. What is absent is the entire *dynamic* layer: the app's central interaction (activating a section) changes the whole content region while producing no focus movement, no announcement, and no title change. A second class of defect sits alongside it — the active-state indicator is computed twice with two different rules, and the visual one is the more permissive of the pair.

**Pre-commitment Predictions** (written before reading the code): (1) no focus management on route change; (2) `document.title` static across routes; (3) no live region announcing the new view; (4) skip-link target lacking `tabindex="-1"`; (5) `aria-current` logic diverging from active-styling logic.

All five confirmed. Two I did not predict and found on inspection: the non-wrapping header flex row (reflow), and the absent index/catch-all route. One prediction I expected to fire and did *not*: I anticipated focus-indicator suppression or a contrast failure in the active nav treatment — neither is present.

---

## Critical Findings

**C1. A route change is unobservable to assistive technology across all three signalling channels.**

Evidence — the absence is complete, and each channel is independently verifiable in the file:
- `spa-route-change-unannounced.md:42-79` — `PortalShell` calls `useLocation()` at `:43` and uses `pathname` for exactly one thing: the `aria-current` ternary at `:60`. There is no `useEffect`, no ref, no focus call anywhere in the component.
- `spa-route-change-unannounced.md:70-76` — `<main id="main-content">` has no `tabindex`, no ref, and no `key`; nothing can receive focus when its children swap.
- `spa-route-change-unannounced.md:5-97` — no `aria-live`, no `role="status"`, no `role="alert"`, no `aria-busy` appears anywhere in the JSX or the HTML.
- `spa-route-change-unannounced.md:84-97` — the comment at `:85` states outright that `index.html` is "the only place a title is set for the whole application"; `<title>Ridgeline Credit Union</title>` at `:90` is therefore the title of `/accounts`, `/transfers`, and `/statements` alike.

Client-side navigation does not trigger the browser's own focus reset, so after activating a `NavLink` at `:57-63`, focus and the virtual cursor remain on that link in the header while everything inside `<main>` is replaced.

- Confidence: HIGH
- User group: screen reader (primary); screen-magnifier users at high zoom (the changed region is off-viewport with no cue); cognitive (no confirmation the activation did anything)
- WCAG: **2.4.2 Page Titled** is the clean, uncontested AA failure here — these are real URLs with real history entries (`:190`), and all three carry one non-descriptive title. The focus/announcement half is weaker on direct SC grounding, and I want to be precise rather than pad the citation: 2.4.3 Focus Order does not strictly prohibit leaving focus in place, and 4.1.3 Status Messages is written for messages the user did *not* initiate. Auditors conventionally record it under **2.4.3**, with the substantive authority being WAI's SPA guidance rather than a bright-line SC.
- Fix: on `pathname` change, set `document.title` to `` `${label} · Ridgeline Credit Union` `` (derive `label` from `SECTIONS`), and move focus to the new view. Cleanest target: give each view's `<section>` (`:9`, `:19`, `:27`) `tabIndex={-1}` plus `aria-labelledby` pointing at its own `<h1>`, and focus it in a `useEffect` keyed on `pathname`, wrapped in `setTimeout(…, 0)` so the assignment survives the route re-render. Suppress the focus move on the very first mount so initial page load is not hijacked. A polite live region is a reasonable *addition* but a poor substitute — it announces without relocating the user.

**Realist Check**: Each channel alone would be MAJOR. What holds this at CRITICAL is that all three are absent simultaneously, on the app's only navigation mechanism, and the failure is silent — axe-core cannot see it, and it will not surface in production except as a user complaint. A reviewer rating this MAJOR on the grounds that the content remains reachable (arrow down two or three times from the nav link and the new `<h1>` reads) would not be wrong; I am calling it CRITICAL because the user has no signal that would prompt them to try.

---

## Major Findings

**M2. `aria-current` is hand-rolled with narrower matching than the visual active state, and overrides `NavLink`'s correct built-in behavior.**

`spa-route-change-unannounced.md:59-60` computes the same state twice by two different rules:
```jsx
className={({ isActive }) => (isActive ? 'nav-link is-active' : 'nav-link')}
aria-current={pathname === path ? 'page' : undefined}
```
`isActive` matches descendants; `pathname === path` is exact equality. The app links to descendant paths at `:12-13` (`/accounts/checking`, `/accounts/savings`) and `:30-31` (`/statements/2026-08`). At `/accounts/checking` the "Accounts" link is styled active — blue, bold, underlined (`:125-129`) — while `aria-current` is `undefined`. Visual state says "you are here"; the accessibility tree says nothing.

`NavLink` already supplies `aria-current="page"` on active by default. Passing an explicit value replaces that default with a stricter one, so this line makes the component *less* accessible than deleting it would.

- Confidence: HIGH on the divergence (the two expressions are literally different, and the stricter one governs ARIA). MEDIUM on the exact React Router internals and therefore on how the defect manifests — see Open Question O1.
- User group: screen reader
- WCAG: 4.1.2 Name, Role, Value (state must be programmatically determinable); 1.3.1 Info and Relationships
- Fix: delete line `:60` and the `useLocation()` call at `:43` that exists only to feed it. If exact matching is genuinely wanted, put it on `NavLink`'s `end` prop so both channels derive from one source of truth.
- If sub-routes turn out to be unreachable (O1), this degrades to MINOR — redundant, fragile duplication rather than an active contradiction.

**M3. Header does not reflow at 320px; produces two-dimensional scrolling.**

`spa-route-change-unannounced.md:102-108` sets `.portal-header { display: flex; gap: 32px; }` and `:110-116` sets `.section-nav { display: flex; gap: 20px; }` — neither declares `flex-wrap`. Flex items cannot shrink below `min-content`, so the floor is roughly: brand min-content ("Ridgeline") ~72px + 32px gap + nav min-content ("Accounts"/"Transfers"/"Statements" ~216px) + 40px of nav gaps + 48px header padding ≈ **408px**, against the 320px reflow threshold.

- Confidence: MEDIUM. The character-width figures are **estimated from default 16px UA font, not measured** — this finding would be materially stronger with a real 320px viewport screenshot or a `scrollWidth` assertion. No test evidence was supplied with this fixture.
- User group: low vision (400% zoom on a 1280px viewport), mobile
- WCAG: 1.4.10 Reflow (AA)
- Fix: `flex-wrap: wrap` on both rules, or collapse the nav below the brand under a `max-width` media query. `.portal-main` at `:151-155` already reflows correctly — only the header is at fault.

**M4. No index route and no catch-all: unmatched URLs render an empty `<main>` with no heading.**

`spa-route-change-unannounced.md:36-40` defines three sections; `:71-75` maps `<Route>` over exactly those and adds neither `<Route index>` nor `<Route path="*">`. Any URL outside the three — including the application root `/` — matches nothing, leaving `<main>` (`:70`) empty. In that state the document contains **no `<h1>` at all**, no error text, no announcement, and (per C1) the same generic title. A screen reader user navigating by heading finds nothing and has no way to distinguish "empty" from "still loading."

- Confidence: MEDIUM. The missing routes are hard evidence in this file; what actually renders depends on `main.jsx`, which I was not given.
- User group: screen reader; cognitive
- WCAG: 1.3.1 Info and Relationships; 2.4.6 Headings and Labels
- Fix: add an index route (redirect `/` → `/accounts`) and a `path="*"` fallback rendering a real `<h1>` plus recovery links. Treat the fallback as a route change for C1's title/focus purposes.

---

## Minor Findings

- **Skip-link target is not focusable.** `spa-route-change-unannounced.md:47-49` targets `#main-content` at `:70`; `<main>` has no `tabindex="-1"`. *Mitigated by:* every current browser implements the sequential-focus-navigation starting point, so Tab-after-activation lands correctly; the residual failure is AT-specific (historically VoiceOver, where the VO cursor does not follow the jump). Add `tabIndex={-1}` to `<main>` — the same attribute C1's fix needs anyway. WCAG 2.4.1.
- **`list-style: none` without `role="list"`.** `:113` and `:162-167`. Safari/VoiceOver strips list semantics from styled-flat lists, so "list, 3 items" is not announced. This is contested WebKit behavior rather than a clear 1.3.1 violation, but `role="list"` costs nothing.
- **Skip link cannot serve as the recovery path for C1.** It sits at `:47`, *before* the header in DOM order, so a user whose focus is stranded on a nav link after a route change would have to Shift+Tab backward past the whole nav to reach it. Worth noting because it means the existing skip link does not accidentally cover the C1 gap.

## Enhancements

- `<section className="view">` at `:9`, `:19`, `:27` has no accessible name, so it maps to `generic`, not `region` — it currently buys nothing. `aria-labelledby` against each view's `<h1>` turns it into a navigable landmark *and* the natural focus target for C1.
- Account/statement anchors (`:12-13`, `:30-31`) are inline; the 10px row padding at `:169-173` is on the `<li>`, so the visually-padded row is not clickable. `display: block` on the anchor enlarges the pointer target. (This is an enhancement, not a 2.5.8 finding — see below.)
- Skip link uses `left: -9999px` (`:138-141`) and `position: absolute` rather than `fixed`; if focus reaches it while the page is scrolled it renders at document top, off-screen. A clip-path visually-hidden utility plus `position: fixed` is more robust.

## What's Missing

- Any `useEffect` on `pathname` — the file contains zero side effects (`:42-79`).
- Any live region of any kind (`:5-97`).
- Any per-route title mechanism; `:85` documents the absence as intentional.
- Any focusable landing point in `<main>` (`:70`).
- Any loading or empty state — routes render synchronously here, but nothing exists for the unmatched case (M4).
- A reverse path back to the nav from deep content; not yet an issue at this content length, but the statement/account sub-pages implied by `:12-13` and `:30-31` will need one.

## Multi-Perspective Notes

- **Screen reader**: Static structure is clean — banner, labeled nav, main, one `<h1>` per view, real list markup, real link and button elements. The dynamic layer is the failure: activating a section produces no announcement, no focus move, no title change (C1), and on descendant routes the "you are here" state disappears from the accessibility tree while remaining visible (M2).
- **Keyboard-only**: The least affected group. Tab order is DOM order and matches the visual order; focus rings are defined at `:131-136` with `3px solid #0b4fa8` at 2px offset — **7.8:1 against white** (computed from hex, not measured), comfortably above the 3:1 required by 2.4.11/2.4.7 — and nothing anywhere sets `outline: none`. Because the header precedes `<main>`, a sighted keyboard user's next Tab after a route change naturally enters the new content, which is exactly why this defect survives sighted keyboard testing.
- **Low vision (200%/400% zoom, high contrast)**: Header does not reflow (M3). Text colors are strong — `#1d2939` on white ≈ 14.7:1, active `#0b4fa8` ≈ 7.8:1, white on `#0b4fa8` for the primary button ≈ 7.8:1 (all computed from hex). Active state is signalled by border-bottom and `font-weight: 600` in addition to color (`:125-129`), so 1.4.1 is satisfied, and body links retain their default underline since no rule targets them. Target sizes pass **2.5.8 Target Size (Minimum), which is 24×24 CSS px at AA** — nav links are ~31px tall, the button ~35px, and the ~19px-tall inline row links clear the bar via the spacing exception (~40px center-to-center). *Note:* my operating instructions cite "44×44 (WCAG 2.5.8)"; that figure is 2.5.5 Target Size (Enhanced), Level AAA. I have graded against the AA criterion, under which nothing here fails.
- **Cognitive**: The core problem is the same one C1 names — activating a nav item gives no confirmation beyond the visual swap, and the browser tab and history entries are identical for all three sections, so back/forward (`:190`) is unlabelled guesswork for everyone. Secondary: the app mixes two navigation models — `NavLink` (client-side, `:57`) in the header, plain `<a href>` (full document load, `:12-13`, `:30-31`) in the content — which behave differently for identical-looking affordances. No timeouts, no destructive actions, no motion, so 2.2.x, 3.3.4, and 2.3.3 are not engaged.

## Verdict Justification

REVISE. The static layer is close to shippable; the dynamic layer has not been designed at all. Upgrading to ACCEPT-WITH-RESERVATIONS requires C1 (title + focus on route change) and M2 (single source of truth for active state) resolved; ACCEPT additionally requires M3 measured and fixed, and M4's fallback route in place.

Recalibrations from Phase 8: **C1 held at CRITICAL** on composite grounds (three simultaneously-silent channels on the app's only navigation), with the one-notch dissent recorded above rather than smoothed over. **M3 downgraded from an assumed hard failure to MEDIUM-confidence MAJOR** because I estimated glyph widths rather than measuring them. **Skip-link `tabindex` downgraded from MAJOR to MINOR** — mitigated by universal browser support for the sequential focus starting point, leaving an AT-specific residual. I deliberately did **not** raise a `prefers-reduced-motion` finding: the CSS contains no transitions or animations, so there is nothing to gate, and flagging it would be a manufactured violation. Likewise no finding on missing landmark roles, `lang`, or ARIA-masking-native-HTML — the file is genuinely clean on all three.

## Open Questions (unscored)

- **O1.** Are `/accounts/checking`, `/accounts/savings`, and `/statements/2026-08` served by route definitions in `main.jsx`? This determines whether M2 manifests as an actual visual/programmatic contradiction or stays a latent duplication defect, and whether those links at `:12-13` and `:30-31` are dead. I could not read `main.jsx`.
- **O2.** React Router version. My reading of M2 assumes v6/v7 `NavLink` semantics — that `isActive` is prefix-matching absent `end`, and that an explicit `aria-current` prop replaces the built-in default. The divergence between the two expressions stands under any version; the precise mechanism does not.
- **O3.** Is `<a className="skip-link" href="#main-content">` intercepted by a router configuration (e.g. a `HashRouter`) that would break fragment navigation outright? Under `BrowserRouter` it is handled natively and works.
- **O4.** No axe-core, Playwright, `agent-browser`, `keyboard-a11y-tester`, or `virtual-screen-reader` evidence accompanied this fixture. C1 is the kind of defect a driven `keyboard-a11y-tester` session or a `virtual-screen-reader` spoken-phrase log would convert from design reasoning to measured fact; M3 needs a 320px viewport measurement.

## Provenance

I read exactly one file:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-unannounced.blind.md`

No other file was read, no directory was listed, no grep or glob was run, no git command was issued, and no subagent was spawned. Nothing under `evals/suites/`, no `*.metadata.yaml`, and no `*.rubric.yaml` was accessed. Contrast ratios cited above were computed by hand from the hex values in that file, not measured in a browser.

---

Resending from C1's Realist Check onward.

**Realist Check (C1)**: Each channel alone would be MAJOR. What holds this at CRITICAL is that all three are absent simultaneously, on the app's only navigation mechanism, and the failure is silent — axe-core cannot see it, and it will not surface in production except as a user complaint. A reviewer rating this MAJOR on the grounds that the content remains reachable (arrow down two or three times from the nav link and the new `<h1>` reads) would not be wrong; I am calling it CRITICAL because the user has no signal that would prompt them to try.

---

## Major Findings

**M2. `aria-current` is hand-rolled with narrower matching than the visual active state, and overrides `NavLink`'s correct built-in behavior.**

`spa-route-change-unannounced.md:59-60` computes the same state twice by two different rules:
```jsx
className={({ isActive }) => (isActive ? 'nav-link is-active' : 'nav-link')}
aria-current={pathname === path ? 'page' : undefined}
```
`isActive` matches descendants; `pathname === path` is exact equality. The app links to descendant paths at `:12-13` (`/accounts/checking`, `/accounts/savings`) and `:30-31` (`/statements/2026-08`). At `/accounts/checking` the "Accounts" link is styled active — blue, bold, underlined (`:125-129`) — while `aria-current` is `undefined`. Visual state says "you are here"; the accessibility tree says nothing.

`NavLink` already supplies `aria-current="page"` on active by default. Passing an explicit value replaces that default with a stricter one, so this line makes the component *less* accessible than deleting it would.

- Confidence: HIGH on the divergence (the two expressions are literally different, and the stricter one governs ARIA). MEDIUM on the exact React Router internals and therefore on how the defect manifests — see Open Question O1.
- User group: screen reader
- WCAG: 4.1.2 Name, Role, Value (state must be programmatically determinable); 1.3.1 Info and Relationships
- Fix: delete line `:60` and the `useLocation()` call at `:43` that exists only to feed it. If exact matching is genuinely wanted, put it on `NavLink`'s `end` prop so both channels derive from one source of truth.
- If sub-routes turn out to be unreachable (O1), this degrades to MINOR — redundant, fragile duplication rather than an active contradiction.

**M3. Header does not reflow at 320px; produces two-dimensional scrolling.**

`spa-route-change-unannounced.md:102-108` sets `.portal-header { display: flex; gap: 32px; }` and `:110-116` sets `.section-nav { display: flex; gap: 20px; }` — neither declares `flex-wrap`. Flex items cannot shrink below `min-content`, so the floor is roughly: brand min-content ("Ridgeline") ~72px + 32px gap + nav min-content ("Accounts"/"Transfers"/"Statements" ~216px) + 40px of nav gaps + 48px header padding ≈ **408px**, against the 320px reflow threshold.

- Confidence: MEDIUM. The character-width figures are **estimated from default 16px UA font, not measured** — this finding would be materially stronger with a real 320px viewport screenshot or a `scrollWidth` assertion. No test evidence was supplied with this fixture.
- User group: low vision (400% zoom on a 1280px viewport), mobile
- WCAG: 1.4.10 Reflow (AA)
- Fix: `flex-wrap: wrap` on both rules, or collapse the nav below the brand under a `max-width` media query. `.portal-main` at `:151-155` already reflows correctly — only the header is at fault.

**M4. No index route and no catch-all: unmatched URLs render an empty `<main>` with no heading.**

`spa-route-change-unannounced.md:36-40` defines three sections; `:71-75` maps `<Route>` over exactly those and adds neither `<Route index>` nor `<Route path="*">`. Any URL outside the three — including the application root `/` — matches nothing, leaving `<main>` (`:70`) empty. In that state the document contains **no `<h1>` at all**, no error text, no announcement, and (per C1) the same generic title. A screen reader user navigating by heading finds nothing and has no way to distinguish "empty" from "still loading."

- Confidence: MEDIUM. The missing routes are hard evidence in this file; what actually renders depends on `main.jsx`, which I was not given.
- User group: screen reader; cognitive
- WCAG: 1.3.1 Info and Relationships; 2.4.6 Headings and Labels
- Fix: add an index route (redirect `/` → `/accounts`) and a `path="*"` fallback rendering a real `<h1>` plus recovery links. Treat the fallback as a route change for C1's title/focus purposes.

---

## Minor Findings

- **Skip-link target is not focusable.** `spa-route-change-unannounced.md:47-49` targets `#main-content` at `:70`; `<main>` has no `tabindex="-1"`. *Mitigated by:* every current browser implements the sequential-focus-navigation starting point, so Tab-after-activation lands correctly; the residual failure is AT-specific (historically VoiceOver, where the VO cursor does not follow the jump). Add `tabIndex={-1}` to `<main>` — the same attribute C1's fix needs anyway. WCAG 2.4.1.
- **`list-style: none` without `role="list"`.** `:113` and `:162-167`. Safari/VoiceOver strips list semantics from styled-flat lists, so "list, 3 items" is not announced. This is contested WebKit behavior rather than a clear 1.3.1 violation, but `role="list"` costs nothing.
- **Skip link cannot serve as the recovery path for C1.** It sits at `:47`, *before* the header in DOM order, so a user whose focus is stranded on a nav link after a route change would have to Shift+Tab backward past the whole nav to reach it. Worth noting because it means the existing skip link does not accidentally cover the C1 gap.

## Enhancements

- `<section className="view">` at `:9`, `:19`, `:27` has no accessible name, so it maps to `generic`, not `region` — it currently buys nothing. `aria-labelledby` against each view's `<h1>` turns it into a navigable landmark *and* the natural focus target for C1.
- Account/statement anchors (`:12-13`, `:30-31`) are inline; the 10px row padding at `:169-173` is on the `<li>`, so the visually-padded row is not clickable. `display: block` on the anchor enlarges the pointer target. (This is an enhancement, not a 2.5.8 finding — see the low-vision note below.)
- Skip link uses `left: -9999px` (`:138-141`) and `position: absolute` rather than `fixed`; if focus reaches it while the page is scrolled it renders at document top, off-screen. A clip-path visually-hidden utility plus `position: fixed` is more robust.

## What's Missing

- Any `useEffect` on `pathname` — the file contains zero side effects (`:42-79`).
- Any live region of any kind (`:5-97`).
- Any per-route title mechanism; `:85` documents the absence as intentional.
- Any focusable landing point in `<main>` (`:70`).
- Any loading or empty state — routes render synchronously here, but nothing exists for the unmatched case (M4).
- A reverse path back to the nav from deep content; not yet an issue at this content length, but the statement/account sub-pages implied by `:12-13` and `:30-31` will need one.

## Checked and Clean (negative space)

Stating what I examined and am *not* claiming, so the absence of a finding is legible as a decision rather than an oversight:

- **Semantic HTML** — no ARIA substituting for native elements anywhere. `<button type="button">` at `:22`, real `<a>` elements at `:12-13`/`:30-31`, real `<ul>/<li>`. No `div role="button"`, no clickable non-interactive elements.
- **Landmarks** — `<header>` at `:51` is not nested inside `article`/`aside`/`main`/`nav`/`section`, so it maps to `banner` despite the `<div className="portal">` wrapper; `<nav aria-label="Account sections">` at `:53` is correctly labeled; `<main>` at `:70` is present and unique. No `<footer>` is required.
- **Heading hierarchy** — exactly one `<h1>` per mounted view (`:10`, `:20`, `:28`), and the brand at `:52` is correctly a `<span>` rather than a competing heading. No skipped levels.
- **`lang`** — `<html lang="en">` present at `:87`.
- **Focus visibility** — `:131-136` defines `3px solid #0b4fa8` at 2px offset; **≈7.8:1 against white** (computed from hex), well past the 3:1 of 2.4.7/2.4.11. Nothing anywhere sets `outline: none`. Unstyled body links retain the UA focus ring.
- **Color contrast** — `#1d2939` on white ≈ 14.7:1; active `#0b4fa8` ≈ 7.8:1; white on `#0b4fa8` (`:175-182`) ≈ 7.8:1. All computed from hex, not measured.
- **Color as sole indicator (1.4.1)** — the active nav state adds `border-bottom` and `font-weight: 600` alongside color (`:125-129`); body links keep their default underline because no rule targets them. Passes.
- **Target size** — graded against **2.5.8 Target Size (Minimum), 24×24 CSS px at AA**. Nav links ~31px tall, button ~35px, and the ~19px inline row links clear the bar via the spacing exception (~40px center-to-center). Nothing fails. *Note:* my operating instructions cite "44×44 (WCAG 2.5.8)"; that figure is 2.5.5 Target Size (Enhanced), Level AAA. I graded to the AA criterion.
- **Reduced motion** — deliberately **not** raised. The CSS contains no transitions or animations, so a `prefers-reduced-motion` block would gate nothing; flagging it would be a manufactured violation.
- **Timeouts, destructive actions, error handling** — none present in this component, so 2.2.x, 3.3.x, and 3.3.4 are not engaged. No finding.
- **Keyboard traps, tab order** — tab order is DOM order and matches visual order; no `tabindex` above 0; no traps.

## Verdict Justification

REVISE. The static layer is close to shippable; the dynamic layer has not been designed at all. Upgrading to ACCEPT-WITH-RESERVATIONS requires C1 (title + focus on route change) and M2 (single source of truth for active state) resolved; ACCEPT additionally requires M3 measured and fixed, and M4's fallback route in place.

Recalibrations from Phase 8: **C1 held at CRITICAL** on composite grounds, with the one-notch dissent recorded above rather than smoothed over. **M3 downgraded from an assumed hard failure to MEDIUM-confidence MAJOR** because I estimated glyph widths rather than measuring them. **Skip-link `tabindex` downgraded from MAJOR to MINOR** — *mitigated by* universal browser support for the sequential focus starting point, leaving an AT-specific residual.

One honesty note that belongs in the verdict rather than buried in C1: the strongest WCAG citation available for the headline defect is **2.4.2 Page Titled**, not the focus/announcement half. 2.4.3 does not strictly forbid leaving focus in place, and 4.1.3 is written for messages the user did not initiate. I have kept C1 at CRITICAL on user-impact grounds while declining to overstate its SC grounding — a team that wants a bright-line conformance failure to point at should lead with the title.

## Open Questions (unscored)

- **O1.** Are `/accounts/checking`, `/accounts/savings`, and `/statements/2026-08` served by route definitions in `main.jsx`? This determines whether M2 manifests as an actual visual/programmatic contradiction or stays a latent duplication defect, and whether those links at `:12-13` and `:30-31` are dead. I could not read `main.jsx`.
- **O2.** React Router version. My reading of M2 assumes v6/v7 `NavLink` semantics — that `isActive` is prefix-matching absent `end`, and that an explicit `aria-current` prop replaces the built-in default. The divergence between the two expressions stands under any version; the precise mechanism does not.
- **O3.** Is `<a className="skip-link" href="#main-content">` intercepted by a router configuration (e.g. a `HashRouter`) that would break fragment navigation outright? Under `BrowserRouter` it is handled natively and works.
- **O4.** No axe-core, Playwright, `agent-browser`, `keyboard-a11y-tester`, or `virtual-screen-reader` evidence accompanied this fixture. C1 is the kind of defect a driven `keyboard-a11y-tester` session or a `virtual-screen-reader` spoken-phrase log would convert from design reasoning to measured fact; M3 needs a 320px viewport measurement.

## Provenance

I read exactly one file:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-unannounced.blind.md`

No other file was read, no directory was listed, no grep or glob was run, no git command was issued, and no subagent was spawned. Nothing under `evals/suites/`, no `*.metadata.yaml`, and no `*.rubric.yaml` was accessed. Contrast ratios cited above were computed by hand from the hex values in that file, not measured in a browser. This resend added no new investigation — it is the same analysis, untruncated.