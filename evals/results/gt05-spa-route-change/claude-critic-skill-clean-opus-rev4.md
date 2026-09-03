I'll start by reading the single file I'm permitted to read.

---

**VERDICT: ACCEPT**

**Overall Assessment**: This is a correct and internally coherent implementation of the SPA route-change focus pattern — the hard parts (first-render exemption, StrictMode-safe guard, scroll/focus separation, title-from-the-rendered-view) are all handled, and several of the usual traps are avoided deliberately rather than by luck. I found no CRITICAL or MAJOR gaps. Two MINOR findings survived the realist check, both in the CSS rather than the route logic, and both reachable only by keyboard or at high zoom.

**Phase 0 — Test evidence**: None attached. No axe-core scan, no Playwright spec, no `agent-browser` trace, no `keyboard-a11y-tester` artifacts, no `virtual-screen-reader` spoken-phrase log. Every claim below is design reasoning from source. Three claims that would be materially stronger with measurement are listed in Open Questions with the specific mode that would settle each.

**Pre-commitment Predictions** (written before reading the code, from component type "SPA route change"):

| # | Predicted | Actual |
|---|---|---|
| 1 | Focus not moved on client-side nav — focus stranded on the clicked link | **Wrong.** Handled, `spa-route-change-clean.md:46-54` |
| 2 | Focus moved on *first* render too, skipping the skip link and nav | **Wrong.** Deliberately exempt, `:47` |
| 3 | Guard is a `hasMounted` boolean that StrictMode defeats | **Wrong.** Previous-pathname compare, `:40,47-48` — the exact failure predicted is named in the comment |
| 4 | Title derived from a hand-rolled `pathname === path` lookup, desyncing from the router | **Wrong.** Title and heading come from one string in one component, `:21-31` |
| 5 | `focus()` without `preventScroll`, fighting the app's own scroll | **Wrong.** Separated, `:49-52` |
| 6 | Redundant `aria-live` route announcer double-speaking with the focus move | **Wrong.** No live region — correct, since focus-to-heading already announces |

Six for six against the pattern's known failure modes. That is not what an accidentally-clean fixture looks like; the comments at `:17-20`, `:36-39`, and `:272` argue against specific wrong alternatives, which means the decisions were made rather than defaulted into. Where I was surprised was the opposite direction: the two real findings are in CSS geometry and a missing selector, not in the route logic I came in expecting to break.

---

## Findings

**Critical Findings**: None.

**Major Findings**: None.

**Minor Findings**

**M1 — The skip-link target has no focus indicator, while every other programmatic focus target does.**
`spa-route-change-clean.md:58` links to `#main-content`; `:81` is `<main id="main-content" tabIndex={-1}>`. The `:focus-visible` group at `:193-199` covers `.nav-link`, `.skip-link`, `.primary`, and `.view-heading` — it does not cover `.portal-main` (`:214-218` defines no focus state either). A keyboard user activates "Skip to main content", focus lands on `<main>`, and nothing visible changes: `<main>` is already in view, so there is no scroll either. The user cannot tell the skip link fired.

- **Confidence**: HIGH — this is a missing selector, verifiable by reading `:193-199`.
- **User group**: Keyboard-only, and low-vision keyboard users specifically. The skip link is reachable *only* by keyboard (`:201-204` puts it at `left: -9999px`), so this affects 100% of the people who use the feature.
- **Expected behavior**: WCAG 2.4.7 Focus Visible is arguable here and I will not overstate it — `<main tabindex="-1">` is a programmatic target, not a keyboard-operable component, so this is not a clean 2.4.7 failure. The stronger citation is the design's own principle: feature #5 at `:270` states the indicator is kept on `.view-heading` precisely because "a sighted user who navigated by keyboard can see where focus landed." That reasoning applies identically to `.portal-main` and was not carried over. WCAG 2.4.1 Bypass Blocks is satisfied mechanically but is undermined in practice by unobservable success.
- **Fix**: Add `.portal-main:focus-visible` to the selector list at `:193-196`. The existing `outline: 3px solid #0b4fa8; outline-offset: 2px` measures 7.8:1 against white, comfortably over the 3:1 in 1.4.11.

**M2 — Nav link hit areas overlap by ~6px once the header wraps.**
`.nav-link` (`:180-185`) is a default-`inline` anchor with `padding: 6px 2px` and `border-bottom: 2px solid transparent`. Vertical padding and borders on an inline box do not increase the line box, so the anchor's hit box overflows its `<li>` by 6px above and 8px below. `.section-nav` (`:171-178`) is `flex-wrap: wrap` with `gap: 8px 20px`. When the header wraps — narrow viewport, or 200% zoom on a normal one — the vertical distance between one row's anchor box and the next is `8 − 6 − 8 = −6px`, i.e. they overlap. The active link's 2px `border-bottom-color` (`:189`) is drawn inside that overlap.

- **Confidence**: MEDIUM-HIGH on the geometry (the arithmetic is independent of the inherited `line-height`, which is why I am confident despite it not being declared here); MEDIUM on impact, which is small.
- **User group**: Low vision at 200% zoom, and motor/touch users on narrow viewports. Not screen reader users.
- **Expected behavior**: This does *not* fail WCAG 2.5.8 Target Size (Minimum) — each target is roughly 33 × 65 CSS px, over the 24 × 24 AA threshold, so the spacing exception never engages. It is a mis-activation risk rather than an SC failure, and the visual overlap of the active-state underline into the row below is a legibility cost at the zoom level where it appears.
- **Fix**: `display: inline-block` on `.nav-link` (`:180`) makes padding and border contribute to the line box, and the 8px row gap becomes real separation. Alternatively raise the row gap at `:174` to `16px 20px`.

**Enhancements**

- **E1 — The focus move fails silently.** `:51` is `mainRef.current?.querySelector('h1')?.focus(...)`. If a view ever renders without an `<h1>` — a lazy route still suspended, a view refactored to `<h2>`, an error boundary — both optional chains short-circuit, focus stays on the activated nav link, and the screen reader user gets *no* signal that navigation happened. Nothing logs. All four current views comply (`:90,106,114,124`), so this is latent, not live. Fix: fall back to `mainRef.current` when the query misses — it already carries `tabIndex={-1}` at `:81`, so the fallback target exists and costs nothing.
- **E2 — `/` renders "Page not found."** `:135` routes `*` to `NotFoundView`; `:257` confirms `/` is included. The rationale at `:272` weighs a client-side redirect (steals focus on cold entry — correct) against an index route (leaves `NavLink ... end` inactive — also correct), but does not consider a server- or edge-level redirect from `/` to `/accounts`, which resolves before React mounts and therefore causes neither problem. As written, the most likely bookmarked or typed URL for a banking portal announces failure. This is a cognitive-accessibility cost (a false state statement at the primary entry point), not an SC failure.
- **E3 — The skip link sits outside every landmark.** `:58` places it as a direct child of `.portal`, before `<header>` at `:62`. It is the first tabbable element, which is the path users actually take, so impact is near zero — but it is invisible to landmark-based navigation.

---

**What's Missing** (gaps searched for and not found — the absences that matter here are mostly *correct* absences)

- **No route-change live region** — correct. Focus-to-heading already produces the announcement; adding `aria-live` here is the classic double-announcement bug and it was avoided.
- **No `prefers-reduced-motion` block** — correct, and not a gap. `:50` uses `window.scrollTo({ top: 0 })` with no `behavior: 'smooth'`, and the CSS declares zero transitions or animations. There is nothing to gate.
- **No scroll restoration on Back** — `:50` resets scroll to top on every pathname change including history navigation. React Router v6 does not restore scroll by default, so this is not a regression, and moving focus on Back is the right call for screen reader users. Noted, not filed.
- **Query-string and hash changes correctly do not steal focus** — `:34` destructures `pathname` only, so `?sort=name` or `#section` leave the effect dormant. This is a real trap (filter changes yanking focus mid-task) that the code sidesteps. If a view later grows in-page anchor links, the SPA anchor-focus gap would open up; it does not apply to this code.
- **Rapid navigation does not drop focus** — `:53` cancels the pending frame, and `:48` has already advanced `previousPath`, so A→B→C lands on C's heading with no orphaned callback. Verified by tracing, not assumed.
- **No `aria-hidden` needed on decorative symbols** — there are none. No `::before`/`::after` content, no icon fonts, no `+`/`×` text glyphs.
- **Genuinely absent**: the h1-missing fallback (E1), and a `.portal-main` focus style (M1).

---

**Multi-Perspective Notes**

- **Screen reader user**: The structure resolves cleanly — banner (`:62`, `<header>` is not nested in a sectioning element, so it maps), navigation labeled "Account sections" (`:64`, and the SR supplies the word "navigation" so there is no doubling), main (`:81`), one `<h1>` per view, `lang="en"` at `:146`. Each route change produces exactly one announcement: "Accounts, heading level 1." The three `<ul>`s carry `role="list"` (`:65,91,115`) against `list-style: none` (`:175,227`) — the correct Safari/VoiceOver countermeasure, and the `<li>`s at `:232` keep `listitem` under `display: flex`. Statement links name their format in the link text (`:116-117`). Title updates before focus moves, because child effects flush before parent effects, so the page-title command reports the arrived view. Nothing here is visual-only.
- **Keyboard-only user**: No trap (2.1.2 clean). Tab order matches visual order. The skip link is real and reachable (`:201-204` uses off-screen positioning, not `visibility: hidden`, so it stays in the tab order). After a route change, the next Tab from the `<h1>` lands inside the new view rather than back in the nav — the whole point of targeting the heading over `<main>`. The one degraded moment is M1: activating the skip link produces no observable result.
- **Low vision (200% zoom, high contrast, magnifier)**: Reflow is sound — no fixed widths, `max-width: 760px` with `auto` margins (`:214-218`), `flex-wrap` on both the header (`:164`) and the nav (`:173`); no horizontal scroll. Focus indicator measures 7.8:1 against white, well over the 3:1 in 1.4.11. `#0b4fa8` active text on white is also 7.8:1. Forced-colors mode survives: `outline-color` is forced to the system highlight so the indicator persists, and the active state carries `font-weight: 600` (`:190`) and `aria-current` alongside color, so it is never color-alone. The viewport meta at `:149` permits pinch-zoom. M2 is this perspective's finding.
- **Cognitive accessibility**: Interaction model is consistent — every route behaves identically, and the title/heading always agree by construction (`:21-31`). No timeouts, no destructive actions, no motion. Two soft costs: E2's "Page not found" at the app root, and the account rows at `:93-94`, where `$2,418.06` is never labeled as a balance. I am deliberately *not* filing the latter as an accessibility finding — there is no column header or visible label either, so sighted and non-sighted users are equally uninformed. That is a content gap, not an access gap, and calling it an a11y defect would be the manufactured-violation failure mode.

---

**Verdict Justification**

ACCEPT. The route-change pattern is complete, not 80%-complete: focus moves, it moves to the right target, it is exempt where it should be, the exemption survives StrictMode, scroll and focus do not fight, and the title cannot desync from the heading. Findings are two MINOR and three ENHANCEMENT, none of which blocks or significantly degrades any user group.

*Severity recalibrations applied:*
- **M1 was drafted MAJOR, downgraded to MINOR.** Mitigated by: the skip link's actual function (moving the tab position) still works, and the very next Tab produces a visible indicator on a styled element. The user loses confirmation, not capability. It also fails the strict 2.4.7 test — `<main tabindex="-1">` is not a keyboard-operable component — and I am not going to inflate a design-consistency gap into an SC failure to make it land harder.
- **M2 was drafted MAJOR, downgraded to MINOR.** Mitigated by: the overlap only exists once the header wraps, the targets clear the 24×24 AA threshold so 2.5.8 is not engaged, and the mis-tap outcome is navigating to an adjacent section of the same portal — recoverable in one click, not destructive.
- **Nothing was upgraded.** I looked specifically for the reclassification pattern (a "decorative" element that is actually functional) and found no candidates: there are no images, no icon fonts, and no pseudo-element content in this component.

*What would move this to ACCEPT-WITH-RESERVATIONS:* if the `:focus-visible` question in Open Questions resolves against the code — that is, if the indicator does not render after the deferred programmatic focus. That would not create an SC failure, but it would mean feature #5 at `:270` documents a behavior the code does not deliver, and a documented-but-absent focus indicator is worth a reservation.

*A note on the protocol I was given, since propagating it would corrupt findings:* the instructions state WCAG 2.5.8 Target Size as 44×44 CSS px. 2.5.8 Target Size (Minimum) is **24×24** at Level AA in WCAG 2.2; 44×44 is 2.5.5 Target Size (Enhanced), Level AAA. Applying the 44px figure would have turned M2 into a fabricated AA failure — `.nav-link` is roughly 33px tall, which fails 44 and passes 24. The protocol also lists "2.3.3 Label, Name, or Instructions"; 2.3.3 is Animation from Interactions, and the criterion intended is **3.3.2 Labels or Instructions**. Both are worth fixing upstream in the agent definition.

---

**Open Questions (unscored)**

1. **Does `:focus-visible` actually match the `<h1>`?** Feature #5 (`:270`) depends on it, and the focus call at `:51` happens inside a `requestAnimationFrame` callback — outside the task that handled the keypress. Chromium and Gecko track this with a document-level "last input was keyboard" flag rather than a task-scoped one, so I *expect* it works, but the spec text describes propagation from the previously-focused element and does not clearly guarantee it across a deferred callback. **Settle it with:** `agent-browser` — Tab to a nav link, press Enter, then read the computed outline on the `<h1>`; or a Playwright spec asserting a non-`none` `outline-style` after `keyboard.press('Enter')`. If it fails, add a `.view-heading:focus` fallback. Not filed as a finding because I cannot confirm it, and an unverified indicator claim belongs here rather than in the findings list.
2. **Is `aria-current="page"` actually in the DOM?** `:258` asserts NavLink supplies it. That is correct for react-router-dom v6+ by default, and the `className` callback at `:71` does not interfere — but the version is not pinned in what I was given, and per the DOM-verification rule, an asserted `aria-*` attribute is not a verified one. **Settle it with:** an `agent-browser` snapshot or a `get-attr` on the active link. Low risk.
3. **Does `ViewHeading` ever receive non-string children?** `:23` interpolates `children` straight into the title. All four call sites pass plain strings (`:90,106,114,124`), so this is fine as written; it would produce `"[object Object] — Ridgeline Credit Union"` if a future view passed an element. Robustness, not an access barrier — raised only because the title is load-bearing for the screen reader's page-title command.

---

## Provenance

I read exactly one file:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-clean.blind.md` (Read tool, full file, 273 lines)

No other file was read. No Grep, Glob, or Bash call was made — the blind protocol was not breached at any point, and in particular I did not read anything under `evals/suites/`, did not open any `*.metadata.yaml` or `*.rubric.yaml`, did not search the repository for this fixture's name, and did not consult git history. All line citations resolve against the file above, cited as `spa-route-change-clean.md:<line>` per instruction.