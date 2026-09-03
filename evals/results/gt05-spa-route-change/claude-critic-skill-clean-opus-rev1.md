I'll start by reading the fixture file.

---

# VERDICT: ACCEPT-WITH-RESERVATIONS

**Overall Assessment**: The route-change accessibility design — the thing this component is actually about — is correct and complete. Title, focus, first-render exemption, scroll/focus separation, and `aria-current` are all handled the way the WAI-recommended SPA pattern says to handle them, and the three decisions most likely to be misread as defects (no `aria-live` announcer, `tabIndex={-1}` on a heading, `preventScroll`) are each right. My one above-minor finding is orthogonal to that design: the header is a non-wrapping flex row that appears to overflow below ~408px, which is a 1.4.10 Reflow risk. Everything else is minor or forward-looking.

---

## Pre-commitment Predictions

Before reading, for a "client-side route change" component I predicted the seven usual failures:

| # | Predicted defect | Found? |
|---|---|---|
| 1 | Focus never moves on route change | **No** — `:33-43` |
| 2 | `document.title` not updated per route | **No** — `:26-28` |
| 3 | Focus set synchronously, lost to the re-render | **No** — deferred via `requestAnimationFrame` `:38-41` |
| 4 | `aria-live` announcer *and* focus move → double announcement | **No** — no announcer, correctly |
| 5 | Focus moved on initial page load too (no first-render guard) | **No** — `:34-37` (but see MINOR 3) |
| 6 | `aria-current` missing on the active nav link | **No** — `:60` |
| 7 | Skip-link target not focusable / skip link absent | **No** — `:47-49` → `:70` |

Zero of seven. What I actually found came from places I hadn't predicted: the stylesheet, the route table, and React's dev-mode effect behavior. That inversion is worth naming — this is a file where the JSX under scrutiny is sound and the incidental supporting material carries the defects.

---

## Critical Findings

None.

---

## Major Findings

**1. Header is a non-wrapping flex row; likely horizontal scroll at 320px (WCAG 1.4.10 Reflow, AA)**

- Evidence: `spa-route-change-clean.md:132-138` — `.portal-header { display: flex; align-items: center; gap: 32px; padding: 12px 24px; }` with no `flex-wrap`. `spa-route-change-clean.md:140-146` — `.section-nav { display: flex; gap: 20px; }`, also no wrap.
- Mechanism (HIGH confidence): both flex items keep the default `min-width: auto`, so neither the brand `<span>` (`:52`) nor the nav `<ul>` can shrink below its min-content width. The nav's min-content is the sum of three non-breakable words plus two 20px gaps.
- Estimated threshold (MEDIUM confidence): at 16px in a typical UI sans — "Accounts" ≈64px, "Transfers" ≈72px, "Statements" ≈80px, + 40px gaps = ~256px for the nav; + ~72px for the brand's longest word; + 32px gap; + 48px padding ≈ **408px minimum**. Above 320px, so `1.4.10` fails; below 640px, so **1.4.4 Resize Text at 200% still passes**. The exposure is specifically 320px viewports and 400% zoom on a 1280px screen, not ordinary 200% zoom.
- User group: low vision (screen magnifier, 400% zoom), plus small-viewport mobile.
- Why the SC has no exception here: 1.4.10's carve-out is for content "which requires two-dimensional layout for usage or meaning." A three-item horizontal nav does not qualify.
- Confidence: **MEDIUM** — the mechanism is certain, the exact breakpoint is a font-metric estimate. This needs one measurement (resize to 320px, check `document.documentElement.scrollWidth > 320`) before it is a fact rather than a reasoned prediction.
- Fix: `.portal-header { flex-wrap: wrap; row-gap: 8px; }` and `.section-nav { flex-wrap: wrap; }`. If the brand must stay on one line, add `min-width: 0` to the nav so it shrinks first.
- Realist Check: held at MAJOR. Content below the header (`:182-186`, `max-width` + percentage-safe padding) reflows correctly, so this is a header strip, not a page-wide failure — but I declined to downgrade on "the user can just scroll horizontally," because horizontal scrolling is the exact behavior the criterion prohibits, and treating it as a mitigating workaround would be circular.
- Refutation path: if a global stylesheet outside this excerpt already sets `flex-wrap` or a media query collapses the header, this is moot.

---

## Minor Findings

**1. `list-style: none` suppresses list semantics in Safari/VoiceOver (WCAG 1.3.1)**

`spa-route-change-clean.md:143` (`.section-nav`) and `:193-198` (`.account-list`, `.statement-list`) all set `list-style: none`. WebKit intentionally removes the `list` role from the accessibility tree when list markers are removed. A VoiceOver user hears three separate links instead of "list, 3 items" — losing the count and the group boundary. It matters most for `.account-list` and `.statement-list`, where the count *is* the information ("how many accounts do I have").

- Fix: add `role="list"` to the three `<ul>` elements (`:54`, `:81`, `:95`). This is the standard counter-measure and has no effect in other UAs.
- Confidence: HIGH on the mechanism, and it is UA-specific, which is what caps it at MINOR.

**2. The `Not found` branch is unreachable; unmatched URLs render an empty document**

`spa-route-change-clean.md:72` renders `'Not found'` when no section matches, and `:27` falls back to the bare site name. Neither can fire. `PortalShell` is attached to a **pathless layout route** (`:103`), which React Router renders only when one of its child routes matches. With only `/accounts`, `/transfers`, `/statements` defined (`:104-106`) and no `path="*"` or index route, hitting `/` or a stale URL matches nothing and `<Routes>` renders `null`.

- Accessibility consequence: an unmatched URL produces a document with no `<main>`, no `<h1>`, no landmarks, and a title left at whatever `index.html` set (`:120`). A screen reader user following a broken or bookmarked link lands in silence with no indication anything went wrong. WCAG 2.4.2 Page Titled and 1.3.1 both have a claim here, though the underlying issue is routing correctness, not markup.
- Fix: add `<Route index element={<Navigate to="/accounts" replace />} />` and `<Route path="*" element={null} />` inside the layout route so the shell (and the `Not found` heading the author already wrote) actually renders.
- Confidence: HIGH on the router mechanism, MEDIUM that it matters — this file may be an excerpt. The `'Not found'` string is evidence the author intended the branch to be reachable, which is why I'm reporting it rather than assuming it's deliberate.

**3. React StrictMode defeats the first-render guard in development**

`spa-route-change-clean.md:34-37` uses a boolean ref. In StrictMode dev builds React runs effect setup → cleanup → setup again while preserving refs. The first setup flips `isFirstRender.current` to `false` and early-returns (creating no cleanup); the second setup therefore falls through and moves focus to the `<h1>` **on initial page load** — precisely the behavior the guard exists to prevent.

- Production impact: **zero**. The risk is that a developer verifying this behavior in `npm run dev` sees the guard "not working" and either removes it or adds a wrong workaround.
- Fix: compare the previous pathname instead of a boolean — `const prevPath = useRef(null); if (prevPath.current === pathname) return; prevPath.current = pathname;` — which is idempotent across a double-invoked effect.
- Confidence: HIGH.

---

## Enhancements

- **Focus indicator is defined for four selectors, not for content links.** `:161-167` styles `.nav-link`, `.skip-link`, `.primary`, and `.view-heading`, but the account and statement links (`:82-83`, `:96-97`) fall back to the UA default ring. Not a 2.4.7 failure — the UA default is visible and meets contrast — but focus appearance is inconsistent across the page. Add `.portal-main a:focus-visible` to the same rule.
- **Back/Forward always scrolls to top and re-focuses the heading.** `:38-41` treats a popstate the same as a forward navigation, so returning to a scrolled view loses position. Defensible here because the views are short; worth revisiting if a view grows long. Cognitive-accessibility cost, no WCAG failure.
- **The pattern assumes synchronous view content.** Focus-to-heading announces the arrival because the Outlet content is already committed. A real banking portal fetches accounts and statements; the moment a view becomes async, focus lands on a heading above an empty region and the data's arrival is silent. That would need `aria-busy` on `<main>` or a `role="status"` region — but only then. As written, adding either would be wrong.
- **The stylesheet never declares a page background.** Every contrast ratio below assumes the UA default white. Worth pinning explicitly so a later dark-theme or brand-background change can't silently invalidate them.

---

## What's Missing (gap analysis)

Things I looked for and confirmed are genuinely absent-and-fine, so a later reviewer doesn't re-litigate them:

- **`prefers-reduced-motion` guard** — not needed. `window.scrollTo({ top: 0 })` at `:39` omits `behavior`, which defaults to instant, and no `scroll-behavior: smooth` exists in the stylesheet. There is no motion to reduce. (This would change the day someone adds a global `scroll-behavior: smooth`.)
- **`aria-live` route announcer** — correctly absent. Focus movement to the heading already announces the arrival; adding a live region would double-announce. This is the deliberate-decision-that-looks-like-a-defect.
- **`tabindex="-1"` on `<main>` for the skip link** — `:47-49` → `:70`. Current Chromium, Firefox, and WebKit set the sequential focus navigation starting point on fragment activation, so Tab continues correctly from `<main>` without it. The belt-and-braces `tabindex="-1"` is still common advice; I'm not recording it as a finding because the behavior is correct in current browsers.
- **Error / loading / disabled / selected state communication** — no such states exist in this component. The only state is "which section am I in," and it is carried three ways: `aria-current="page"` (`:60`), a color change, and a border + font-weight change (`:155-159`). Not color alone. 1.4.1 satisfied.
- **`lang`** — present (`:117`). **Landmarks** — `<header>` (banner, correctly not nested inside sectioning content), `<nav aria-label="Account sections">`, `<main>`; all content is inside one, except the skip link, which is conventional.
- **Heading hierarchy** — one `<h1>` per view, no skips, no headings in the child views to conflict with it.
- **ARIA audit** — the only ARIA in the file is `aria-label` on `<nav>` and `aria-current="page"`. Both are enhancement-of-native, not replacement-of-native. There is no widget here that maps to an APG pattern, and no `div`/`span` masquerading as a control. Nothing to critique.

---

## Multi-Perspective Notes

**Screen reader user** — Activating a nav link produces: a title change to "Accounts — Ridgeline Credit Union" (`:27`), then focus on `<h1 tabindex="-1">Accounts</h1>` (`:71`), announced as "Accounts, heading level 1." That is a complete, non-redundant route-change announcement. The next Tab lands on the first link inside the new view rather than back in the nav, because the `<h1>` sits at the top of `<main>` (`:70-74`). Two things degrade: Safari/VoiceOver loses the list grouping (MINOR 1), and an unmatched URL produces total silence (MINOR 2). Reading order matches visual order. `aria-current="page"` correctly marks the active link — note that `NavLink` supplies this by default too, so `:60` is redundant but produces the identical result and is not a defect.

**Keyboard-only user** — Tab order is skip link → brand (not focusable) → three nav links → main content. Logical, matches visual. No traps, no custom key handling, no arrow-key widget to discover. Enter activates the links natively. Focus visibly moves to the heading after navigation via `.view-heading:focus-visible` (`:164`). Notably, re-activating the link for the *current* route does nothing, because the effect depends on `[pathname]` (`:43`) — correct, and a spurious focus jump there would have been the annoying failure mode.

**Low vision (200% zoom, magnifier, high contrast)** — This is where the one MAJOR lives. At 200% the header still fits; at 400%/320px it appears to overflow horizontally. Contrast, by contrast, is strong: `#1d2939` on white = **14.7:1**; `#0b4fa8` on white (active link and focus outline) = **7.78:1**, well past the 4.5:1 text and 3:1 non-text thresholds; white on `#0b4fa8` (the button) = 7.78:1. The 3px outline at 2px offset (`:165-166`) is a substantial indicator. **2.4.11 Focus Not Obscured (AA)** passes — nothing is `position: sticky` or `fixed`, and the code scrolls to top before focusing. Target sizes: nav links ≈68×31px and the button ≈35px tall both clear **2.5.8's** 24×24 outright; the inline account/statement links are only ~19px tall but pass via the *spacing* exception, since `li { padding: 10px 0 }` (`:200-204`) puts their centers ~39px apart. That last one is close — dropping the `li` padding below ~3px would break it.

**Cognitive accessibility** — Consistent: every section navigates the same way, and the title format is uniform because nav label, route, and title all come from one `SECTIONS` array (`:11-15`), so they cannot drift apart. No timeouts, no destructive actions, no ambiguous instructions. Two friction points: Back always jumps to the top of the page (Enhancement 2), and the nav uses client-side `NavLink` while the account/statement links (`:82-83`, `:96-97`) are plain `<a href>` triggering full page loads — so navigation feels different depending on which link you click. The full-load path is natively accessible, so it is a consistency observation, not a defect.

---

## Verdict Justification

**ACCEPT-WITH-RESERVATIONS**, and the split matters more than the label: the route-change design earns a clean ACCEPT on its own terms. Every one of the five claims in the file's "Accessibility Features Present" section checks out against the code — I verified the layout route keeps `PortalShell` mounted so `isFirstRender` genuinely persists (`:103`), that `SECTIONS.find` returns a stable object reference so the `[section]` dependency at `:28` fires correctly and doesn't loop, and that `requestAnimationFrame` + `preventScroll` are ordered correctly relative to React's commit.

The reservation is one CSS rule in the header, not the route-change machinery. Upgrade to ACCEPT requires: measure the header at 320px and add `flex-wrap` if it overflows.

**Severity recalibrations:** the reflow finding was held at MAJOR rather than downgraded, on the ground that "the user can scroll horizontally" is the prohibited behavior itself, not a mitigation. The StrictMode issue was initially drafted as MAJOR (the focus guard demonstrably fails) and downgraded to MINOR — **Mitigated by:** it is a dev-build-only artifact with zero production user impact; the real risk is a developer mis-diagnosing it. Two candidate findings were dropped entirely rather than reported at low severity: "missing `prefers-reduced-motion`" (no motion exists) and "missing `aria-live` route announcer" (would cause double announcement). Both would have been manufactured violations.

---

## Open Questions (unscored)

1. **Does `:focus-visible` match on the programmatically focused `<h1>`?** `:164` styles `.view-heading:focus-visible`, and the element is only ever focused by script (`:40`). The CSS spec's heuristic says a script-focused element matches `:focus-visible` if the previously focused element did — so a keyboard user who Tabbed to the nav link and pressed Enter *should* see the outline, and a mouse user correctly should not, which is exactly the stated intent. I could not measure this, and cross-browser behavior for script-focused `tabindex="-1"` non-interactive elements has historically been uneven (particularly older Safari). If the team wants a guaranteed indicator, `.view-heading:focus` would be unconditional; the tradeoff is that mouse-clicking a nav link would then also draw an outline. Worth one manual check in Safari before changing anything.
2. **Is this the complete route table?** MINOR 2 assumes `PortalRoutes` (`:101-109`) is the app's whole `<Routes>` because it is the module's default export. If a parent `<Routes>` or a redirect lives outside this file, that finding dissolves.
3. **Are `/accounts/checking` and `/statements/2026-08` (`:82`, `:96`) real routes?** They are plain `<a href>` pointing at paths this route table doesn't define, so as written they trigger a full page load into a blank document. I have not made a finding of this, because it is much more likely the fixture is illustrative than that the app is broken this way — but if these are meant to be in-app routes, they need `<Link>` and route definitions, and the full-load/client-side split noted in the cognitive perspective becomes a real inconsistency.
4. **No test evidence was available.** There was no axe-core scan, Playwright keyboard run, `keyboard-a11y-tester` trace, or `virtual-screen-reader` log attached to this review. Three claims above would be materially stronger as measurements rather than reasoning: the 320px reflow threshold (MAJOR 1), the `:focus-visible` behavior (Q1), and the VoiceOver list-role suppression (MINOR 1). All three are single-command checks.

---

## Provenance

I read exactly one file:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-clean.blind.md`

No other file was read, opened, or searched. I ran no `grep`/`glob` over the repository, read nothing under `evals/suites/`, opened no `*.metadata.yaml` or `*.rubric.yaml`, and ran no `git` commands. No subagents were spawned. All line citations refer to the line numbering of that file as presented to me.

---

Resuming from the Realist Check on MAJOR 1.

---

**MAJOR 1 (continued) — Realist Check and remediation**

- Realist Check: **held at MAJOR.** Content below the header (`spa-route-change-clean.md:182-186` — `max-width` plus percentage-safe padding) reflows correctly, so this is a header strip, not a page-wide failure. I declined to downgrade on "the user can just scroll horizontally," because horizontal scrolling is the exact behavior the criterion prohibits; treating it as a mitigating workaround would be circular reasoning.
- Bounding the exposure precisely: at 200% zoom on a 1280px viewport the effective width is ~640px, which the header clears — so **1.4.4 Resize Text passes**. The failure window is 320px viewports and 400% zoom, i.e. **1.4.10 Reflow only**.
- Fix: `.portal-header { flex-wrap: wrap; row-gap: 8px; }` and `.section-nav { flex-wrap: wrap; }`. If the brand must stay on one line, add `min-width: 0` to the nav so it shrinks first.
- Confidence: **MEDIUM.** The mechanism is certain; the exact breakpoint is a font-metric estimate. One measurement settles it: resize to 320px and check `document.documentElement.scrollWidth > 320`.
- Refutation path: if a global stylesheet outside this excerpt sets `flex-wrap`, or a media query collapses the header, this finding is moot.

---

## Minor Findings

**MINOR 1 — `list-style: none` suppresses list semantics in Safari/VoiceOver (WCAG 1.3.1)**

`spa-route-change-clean.md:143` (`.section-nav`) and `:193-198` (`.account-list`, `.statement-list`) all set `list-style: none`. WebKit intentionally removes the `list` role from the accessibility tree when list markers are removed. A VoiceOver user hears three separate links instead of "list, 3 items" — losing both the count and the group boundary. It matters most on `.account-list` and `.statement-list`, where the count *is* the information ("how many accounts do I have").

- User group: screen reader (Safari/VoiceOver specifically).
- Fix: add `role="list"` to the three `<ul>` elements at `:54`, `:81`, `:95`. Standard counter-measure; no effect in other UAs.
- Confidence: HIGH on the mechanism. Being UA-specific is what caps it at MINOR.

**MINOR 2 — The `Not found` branch is unreachable; unmatched URLs render an empty document**

`spa-route-change-clean.md:72` renders `'Not found'` when no section matches, and `:27` falls back to the bare site name. Neither can ever fire. `PortalShell` is attached to a **pathless layout route** (`:103`), which React Router renders only when one of its child routes matches. With only `/accounts`, `/transfers`, `/statements` defined (`:104-106`) and no `path="*"` or index route, hitting `/` or a stale URL matches nothing and `<Routes>` renders `null`.

- Accessibility consequence: an unmatched URL produces a document with no `<main>`, no `<h1>`, no landmarks, and a title left at whatever `index.html` set (`:120`). A screen reader user following a broken or bookmarked link lands in silence with no indication anything went wrong. WCAG 2.4.2 Page Titled and 1.3.1 both have a claim, though the root cause is routing correctness rather than markup.
- Fix: `<Route index element={<Navigate to="/accounts" replace />} />` plus a `path="*"` child inside the layout route, so the shell — and the `Not found` heading the author already wrote — actually renders.
- Confidence: HIGH on the router mechanism, MEDIUM that it matters in practice, since this file may be an excerpt. The `'Not found'` string is itself evidence the author intended the branch to be reachable, which is why I report it rather than assume it deliberate.

**MINOR 3 — React StrictMode defeats the first-render guard in development**

`spa-route-change-clean.md:34-37` uses a boolean ref to skip focus movement on initial mount. In StrictMode dev builds, React runs effect setup → cleanup → setup again while preserving refs. The first setup flips `isFirstRender.current` to `false` and early-returns (creating no cleanup function); the second setup therefore falls through, schedules the `requestAnimationFrame`, and moves focus to the `<h1>` **on initial page load** — precisely the behavior the guard exists to prevent.

- Production impact: **zero.** The risk is diagnostic: a developer verifying the exemption in `npm run dev` sees the guard "not working" and either deletes it or bolts on a wrong workaround.
- Fix: compare the previous pathname instead of a boolean — `const prevPath = useRef(null); if (prevPath.current === pathname) return; prevPath.current = pathname;` — which is idempotent across a double-invoked effect and preserves the intended semantics.
- Confidence: HIGH.
- Recalibration note: drafted as MAJOR (the guard demonstrably fails), downgraded to MINOR. **Mitigated by:** dev-build-only artifact, no production user is ever affected.

---

## Enhancements

- **Focus indicator defined for four selectors, not for content links.** `:161-167` styles `.nav-link`, `.skip-link`, `.primary`, and `.view-heading`, but the account and statement links (`:82-83`, `:96-97`) fall back to the UA default ring. Not a 2.4.7 failure — the UA default is visible and meets contrast — but focus appearance is inconsistent across the page. Add `.portal-main a:focus-visible` to the same rule.
- **Back/Forward always scrolls to top and re-focuses the heading.** `:38-41` treats a popstate identically to a forward navigation, so returning to a scrolled view loses position. Defensible here because the views are short; worth revisiting if a view grows long. Cognitive cost, no WCAG failure.
- **The pattern assumes synchronous view content.** Focus-to-heading announces arrival because the Outlet content is already committed. A real banking portal fetches accounts and statements; the moment a view goes async, focus lands on a heading above an empty region and the data's arrival is silent. That would need `aria-busy` on `<main>` or a `role="status"` region — but *only* then. Adding either today would be wrong.
- **The stylesheet never declares a page background.** Every contrast ratio I computed assumes the UA default white. Worth pinning explicitly so a later dark-theme or brand-background change cannot silently invalidate them.

---

## What's Missing (negative space — checked, and correctly absent)

Recorded so a later reviewer doesn't re-litigate these:

- **`prefers-reduced-motion` guard** — not needed. `window.scrollTo({ top: 0 })` at `:39` omits `behavior`, defaulting to instant, and no `scroll-behavior: smooth` exists in the stylesheet. There is no motion to reduce. This changes the day someone adds a global `scroll-behavior: smooth`.
- **`aria-live` route announcer** — correctly absent. Focus movement to the heading already announces arrival; a live region would double-announce. This is the deliberate decision most likely to be misread as a defect.
- **`tabindex="-1"` on `<main>` for the skip link** (`:47-49` → `:70`) — current Chromium, Firefox, and WebKit set the sequential focus navigation starting point on fragment activation, so Tab continues correctly without it. The belt-and-braces `tabindex="-1"` remains common advice; I am not recording it as a finding because behavior is correct in current browsers.
- **Error / loading / disabled / selected state communication** — no such states exist in this component. The only state is "which section am I in," carried three ways: `aria-current="page"` (`:60`), color, and border + font-weight (`:155-159`). Not color alone; 1.4.1 satisfied.
- **`lang`** — present (`:117`). **Landmarks** — `<header>` (banner, correctly not nested in sectioning content), `<nav aria-label="Account sections">`, `<main>`. All content sits inside one, except the skip link, which is conventional.
- **Heading hierarchy** — one `<h1>` per view, no skips, no competing headings in the child views.
- **ARIA audit** — the only ARIA in the file is `aria-label` on `<nav>` and `aria-current="page"`. Both enhance native semantics rather than replace them. No widget maps to an APG pattern here, and no `div`/`span` masquerades as a control. Nothing to critique.

---

## Multi-Perspective Notes

**Screen reader user** — Activating a nav link produces: title change to "Accounts — Ridgeline Credit Union" (`:27`), then focus on `<h1 tabindex="-1">Accounts</h1>` (`:71`), announced as "Accounts, heading level 1." A complete, non-redundant route-change announcement. The next Tab lands on the first link inside the new view rather than back in the nav, because the `<h1>` sits at the top of `<main>` (`:70-74`). Two degradations: Safari/VoiceOver loses list grouping (MINOR 1), and an unmatched URL produces total silence (MINOR 2). Reading order matches visual order. Note that `NavLink` supplies `aria-current="page"` by default, so the explicit prop at `:60` is redundant — but it resolves to the identical value and is not a defect.

**Keyboard-only user** — Tab order: skip link → three nav links → main content. Logical, matches visual. No traps, no custom key handling, no arrow-key widget to discover. Enter activates natively. Focus visibly moves to the heading via `.view-heading:focus-visible` (`:164`). Notably, re-activating the link for the *current* route does nothing, because the effect depends on `[pathname]` (`:43`) — correct, and a spurious focus jump there would have been the annoying failure mode.

**Low vision (200% zoom, magnifier, high contrast)** — Where the one MAJOR lives. Contrast, by contrast, is strong: `#1d2939` on white = **14.7:1**; `#0b4fa8` on white (active link and focus outline) = **7.78:1**, well past the 4.5:1 text and 3:1 non-text thresholds; white on `#0b4fa8` (the button) = 7.78:1. The 3px outline at 2px offset (`:165-166`) is a substantial indicator. **2.4.11 Focus Not Obscured (AA) passes** — nothing is `position: sticky` or `fixed`, and the code scrolls to top before focusing. Target sizes: nav links ≈68×31px and the button ≈35px tall clear **2.5.8's** 24×24 outright; the inline account/statement links are only ~19px tall but pass via the *spacing* exception, since `li { padding: 10px 0 }` (`:200-204`) puts their centers ~39px apart. That last one is close — dropping the `li` padding below ~3px would break it.

**Cognitive accessibility** — Consistent: every section navigates the same way, and the title format cannot drift from the nav label because both come from one `SECTIONS` array (`:11-15`). No timeouts, no destructive actions, no ambiguous instructions. Two friction points: Back always jumps to the top (Enhancement 2), and the nav uses client-side `NavLink` while account/statement links (`:82-83`, `:96-97`) are plain `<a href>` triggering full page loads — navigation feels different depending on which link you click. The full-load path is natively accessible, so this is a consistency observation, not a defect.

---

## Verdict Justification

**ACCEPT-WITH-RESERVATIONS**, and the split matters more than the label: the route-change design earns a clean ACCEPT on its own terms. All five claims in the file's "Accessibility Features Present" section check out against the code — I verified that the layout route keeps `PortalShell` mounted so `isFirstRender` genuinely persists (`:103`), that `SECTIONS.find` returns a stable object reference so the `[section]` dependency at `:28` fires correctly without looping, and that `requestAnimationFrame` + `preventScroll` are ordered correctly relative to React's commit.

The reservation sits in one CSS rule in the header, not in the route-change machinery. Upgrade to ACCEPT requires exactly one action: measure the header at 320px and add `flex-wrap` if it overflows.

**Severity recalibrations:** MAJOR 1 held (rationale above). MINOR 3 downgraded from MAJOR (dev-only, no production impact). Two candidate findings were dropped entirely rather than reported at low severity — "missing `prefers-reduced-motion`" (no motion exists) and "missing `aria-live` route announcer" (would cause double announcement). Both would have been manufactured violations, and both are exactly the trap this component sets.

---

## Open Questions (unscored)

1. **Does `:focus-visible` match on the programmatically focused `<h1>`?** `:164` styles `.view-heading:focus-visible`, and the element is only ever focused by script (`:40`). The CSS spec heuristic says a script-focused element matches `:focus-visible` if the previously focused element did — so a keyboard user who Tabbed to the nav link and pressed Enter *should* see the outline, and a mouse user correctly should not, which is precisely the stated intent. I could not measure it, and cross-browser behavior for script-focused `tabindex="-1"` non-interactive elements has historically been uneven, notably in older Safari. If the team wants an unconditional indicator, `.view-heading:focus` would deliver it, at the cost of also outlining after a mouse click. One manual Safari check settles it — do not change the CSS before that.
2. **Is this the complete route table?** MINOR 2 assumes `PortalRoutes` (`:101-109`) is the app's entire `<Routes>`, because it is the module's default export. If a parent `<Routes>` or redirect lives outside this file, the finding dissolves.
3. **Are `/accounts/checking` and `/statements/2026-08` (`:82`, `:96`) real routes?** They are plain `<a href>` pointing at paths this route table does not define, so as written they trigger a full page load into a blank document. I made no finding of this — far more likely the fixture is illustrative than the app broken this way — but if they are meant to be in-app routes they need `<Link>` plus route definitions, and the client-side/full-load inconsistency noted in the cognitive perspective becomes real.
4. **No test evidence was available.** No axe-core scan, Playwright keyboard run, `keyboard-a11y-tester` trace, or `virtual-screen-reader` log accompanied this review. Three claims would be materially stronger as measurements rather than reasoning: the 320px reflow threshold (MAJOR 1), the `:focus-visible` behavior (Q1), and the VoiceOver list-role suppression (MINOR 1). Each is a single-command check.

---

## Provenance

I read exactly one file:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-clean.blind.md`

No other file was read, opened, or searched. I ran no `grep`/`glob` over the repository, read nothing under `evals/suites/`, opened no `*.metadata.yaml` or `*.rubric.yaml`, and ran no `git` commands. No subagents were spawned. All line citations refer to the line numbering of that file as presented to me.