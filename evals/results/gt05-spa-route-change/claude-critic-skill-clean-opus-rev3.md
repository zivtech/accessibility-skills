I'll start by reading the single file I'm permitted to read.

---

**VERDICT: ACCEPT-WITH-RESERVATIONS**

**Overall Assessment**: The route-change focus design — the actual subject of this file — is sound, and five of its six claimed features verify against the code. The reservation is not in the React: the accompanying `index.html` ships with no viewport meta tag, which makes every responsive rule in the stylesheet inert on mobile and fails 1.4.10 Reflow. Two smaller coherence gaps: the design principle stated for the `<h1>` focus indicator is not applied to the other programmatic focus target, and the `/` route renders Accounts with no section marked current.

**Pre-commitment Predictions** (made before reading, for SPA route-change components):
1. Focus never moves on client-side navigation → **wrong**, handled at `:46-54`
2. `document.title` derived from a second pathname match, desyncing from the rendered view → **wrong**, and pre-empted deliberately at `:21-31`
3. First render exempted with a boolean that StrictMode defeats → **wrong**, ref holds the path, not a flag (`:40`)
4. Focus target lacks `tabindex="-1"` or has no visible indicator → **wrong** for the `<h1>` (`:27`, `:196`), **right** for `<main>` (`:81`, no matching rule at `:193-199`)
5. `focus()` without `preventScroll` fighting a manual scroll → **wrong**, split correctly at `:50-51`

The surprise was that nothing in my predicted set landed on the component itself, and the only AA-level failure is in the HTML shell that was included to illustrate something else.

---

**Critical Findings**: None.

---

**Major Findings**

**1. No viewport meta tag — the responsive CSS never activates on mobile, and the page fails Reflow.**
`spa-route-change-clean.md:148-151` — the `<head>` contains `charset` and `<title>` only. Without `<meta name="viewport" content="width=device-width, initial-scale=1">`, mobile browsers lay the page out in a ~980px virtual viewport and scale it down.

- **User group**: low vision (primary), plus every mobile user.
- **Concrete effect**: `.portal-header`'s `flex-wrap` (`:164`), `.section-nav`'s `flex-wrap` (`:173`), and `.portal-main { max-width: 760px }` (`:216`) are all written for narrow viewports and none of them ever fire on a phone — the layout viewport is never narrow. The 760px column is centered inside 980px and scaled to the device width, rendering body text at roughly 40% of its intended size. A low-vision user recovers it only by pinch-zooming and then panning in two dimensions.
- **Expected**: WCAG 2.2 **1.4.10 Reflow (AA)** — content must be presentable at a 320 CSS px equivalent width without two-dimensional scrolling. (1.4.4 Resize Text is not failed: zoom is not disabled, since there is no `user-scalable=no` — because there is no viewport meta at all.)
- **Why automated testing misses it**: axe-core's `meta-viewport` rule inspects an *existing* viewport meta for `user-scalable=no` / `maximum-scale`. A missing tag makes the rule inapplicable — no violation is reported. This is exactly the "scan is green, design fails" class.
- **Fix**: add `<meta name="viewport" content="width=device-width, initial-scale=1" />` to `:148-151`.
- **Confidence**: HIGH that the tag is absent (the document is quoted complete, `<!doctype>` through `</html>`); **MEDIUM** that the snippet is authoritative. **This is the one finding a developer could refute with context** — the comment at `:145` frames the HTML as included to show the title mechanism, so it may be abridged. If the real `index.html` has the tag, this finding collapses and the verdict is a clean ACCEPT. I am reporting it rather than deferring it because the stylesheet's responsive work is dead code without it, which couples the two files.

---

**Minor Findings**

**1. The skip link's destination has no focus indicator, while the route-change destination does.**
`spa-route-change-clean.md:81` gives `<main id="main-content" tabIndex={-1}>` — a second programmatic focus target. The focus-visible group at `:193-199` covers `.nav-link`, `.skip-link`, `.primary`, and `.view-heading`, but not `.portal-main`.

Feature 5 (`:270`) states the governing principle explicitly: a programmatic focus target keeps an indicator "so that a sighted user who navigated by keyboard can see where focus landed." That principle is applied to the `<h1>` and not to `<main>`, which is the target of the only bypass mechanism on the page (`:58-60`).

- **User group**: sighted keyboard-only.
- **Realistic behavior**: Tab reveals the skip link, Enter moves focus to `<main>`, the skip link vanishes, and nothing anywhere indicates focus moved. On `/accounts` there is nothing focusable inside `<main>`, so the next Tab exits to browser chrome — the user gets no confirmation the skip worked at any point in the sequence.
- **WCAG**: 2.4.7 Focus Visible does not strictly apply (`<main>` is not keyboard-operable), which is the same reasoning `:270` uses — and then declines to follow. Cite it as a coherence gap against the file's own stated principle, supported by 2.4.1 Bypass Blocks: the bypass exists but gives sighted keyboard users no feedback.
- **Fix**: use plain `:focus`, not `:focus-visible`, for this one:
  ```css
  .portal-main:focus { outline: 3px solid #0b4fa8; outline-offset: 2px; }
  ```
  The `:focus-visible` heuristic is the right call for `.view-heading` (a mouse click on a nav link should not paint an outline on the new heading), but it is browser-dependent for fragment-navigation focus, and `<main>` is not in the tab order — so a plain `:focus` rule can never fire from mouse interaction and is the more robust choice here.
- **Confidence**: HIGH on the absence and the reasoning; MEDIUM on how uniformly `:focus-visible` would have matched across browsers, which is why the fix routes around the question.

**2. `/` renders the Accounts view with no section marked current.**
`spa-route-change-clean.md:132` maps the index route to `AccountsView`; `:70` gives every `NavLink` the `end` prop, so on `/` the `/accounts` link is not active — no `.is-active` styling (`:187-191`) and no `aria-current="page"` (contradicting the claim at `:258` for this one URL).

- **User group**: all users equally (nothing is lost programmatically that is present visually, so this is not a 1.3.1 failure), with a specific screen-reader interaction cost below.
- **Realistic behavior**: a user landing on `/` sees no highlighted section, so they activate "Accounts." The pathname changes, the effect at `:46-54` fires, and focus lands on an `<h1>` reading "Accounts" — the same heading they were already on. For a screen reader user the announcement is indistinguishable from having gone nowhere.
- **The rationale at `:266` is correct and I am not asking you to reverse it.** I checked the redirect path: `previousPath` initializes to `/` (`:40`), a `<Navigate replace>` would then flip pathname to `/accounts`, the effect would see a changed path, and focus would move on the most common cold entry — precisely the failure described. The redirect is genuinely off the table; the cost of not redirecting just needs paying elsewhere.
- **Fix**: mark the Accounts entry current on `/` without changing the route table. `pathname` is already in scope at `:34`:
  ```jsx
  const isAccounts = path === '/accounts' && pathname === '/';
  <NavLink to={path} end
    aria-current={isAccounts ? 'page' : undefined}
    className={({ isActive }) => (isActive || isAccounts ? 'nav-link is-active' : 'nav-link')}>
  ```
- **Confidence**: HIGH.

---

**Enhancements**

- **`ViewHeading` will silently produce a broken title for non-string children** (`:23`). `` `${children} — ${SITE}` `` works only because every call site passes a bare string. A future `<ViewHeading>Accounts <span>(3)</span></ViewHeading>` yields `"[object Object] — Ridgeline Credit Union"` with no warning, and the document title is a Level A requirement (2.4.2 Page Titled). Low likelihood, silent failure mode; a `title` prop separate from `children`, or a dev-mode `typeof children === 'string'` assertion, removes the trap.
- **No fallback when the destination has no `<h1>`** (`:51`). Optional chaining means focus silently stays on the activated nav link while `window.scrollTo` (`:50`) still fires — focus and viewport desync with no error. Every view here has a heading and the catch-all covers unmatched URLs, so this is belt-and-braces: `?? mainRef.current` costs nothing and `<main>` is already `tabIndex={-1}`.
- **Back/Forward navigation loses scroll position** (`:50`). The effect fires on any `pathname` change, including history traversal, so returning to a long list always lands at the top. Not a WCAG failure; a real cognitive-load cost for users who rely on spatial memory, and unmentioned in the feature list. Gating the `scrollTo` on `useNavigationType() !== 'POP'` would preserve it.
- **Currency amounts carry no programmatic label** (`:93-94`, `:97-98`). "$2,418.06" reaches a screen reader as a bare number — balance, available, pending, minimum due? Deliberately rated low: there is no visible column header either, so sighted users infer from context identically. Not a differential disadvantage, so not a finding — but a visible "Balance" label would help both groups.
- **The rationale at `:268` cites a hazard that does not exist in this stylesheet.** `preventScroll` is justified partly by focus "skip[ping] past sticky header chrome," but nothing here is `position: sticky` (`:162-169`). The decision is correct; the stated reason is generic. Worth tightening, because a reader auditing this file will go looking for the sticky header and not find it.

---

**What's Missing**

- **Viewport meta** — the Major above.
- **Focus style for the skip-link destination** — Minor 1.
- **Current-section state on `/`** — Minor 2.
- **No `@media (forced-colors: active)` block.** Checked and *not* a finding: the focus indicator uses `outline` (survives forced colors, unlike `box-shadow`), the active nav state carries `font-weight: 600` alongside its border color (`:190`), and `.primary` has a real `border` (`:243`) so it stays visible when its background is forced. The design happens to be HCM-safe without the block.
- **No loading, error, or busy state anywhere.** Correct for the code as given — every view is synchronous with no data fetching. Flagging the boundary, not the code: the moment `AccountsView` fetches balances, this design has no `aria-busy`, no `role="status"`, and no announcement path, and the focus effect will fire against an empty `<main>` before the data arrives.
- **No `<footer>` / contentinfo landmark.** No footer content exists; not a gap.
- **No reverse skip-link.** Not warranted at this content length.

---

**Multi-Perspective Notes**

- **Screen reader user**: Well served on the file's core subject. Landmarks are correct — `<header>` still maps to banner despite the `<div>` nesting (it is not inside `article`/`aside`/`main`/`nav`/`section`), `<nav>` is labeled without the redundant word "navigation" (`:64`), one `<h1>` per view with the brand as a `<span>` (`:63`) so nothing competes. `role="list"` on all three `<ul>`s (`:65`, `:91`, `:115`) is earned, not cargo-culted: `list-style: none` is applied to every one of them (`:175`, `:228`), which is exactly the condition under which Safari/VoiceOver strips list semantics. Focusing an `h1[tabindex="-1"]` is the canonical announcement technique and correctly preferred over a live region. The one rough edge is the `/` case in Minor 2, where a navigation announces the heading the user just left.
- **Keyboard-only user**: Tab order is DOM order and matches the visual layout. The skip link uses off-screen positioning (`:201-204`), not `visibility: hidden` or `display: none`, so it stays in the tab order — the correct technique. Focus is never trapped; there is no modal, no roving-tabindex widget, no arrow-key shortcut to discover. `tabIndex={-1}` on the `<h1>` (`:27`) keeps the programmatic target out of the tab sequence. The gap is feedback, not operability: Minor 1 means the bypass mechanism runs silently for sighted keyboard users.
- **Low vision (200%/400% zoom, high contrast, magnifier)**: This is where the review lands. In a correctly-sized viewport the CSS holds up — I traced reflow at a 320px equivalent and the un-wrapped `.account-list li` flex row (`:232-238`) still fits, because flex items resolve `min-width: auto` to min-content and the longest words plus the 16px gap come to ~156px against 288px available. Contrast is comfortable: `#0b4fa8` on white measures **7.78:1** (nav active state, button background, and every focus outline — well past both 4.5:1 for text and 3:1 for the non-text indicator). Target sizes clear 2.5.8: nav links are ~31px tall, and the ~19px statement links pass via the spacing exception with 40px center-to-center separation (`:236-238`). All of that is undone on mobile by the missing viewport meta.
- **Cognitive**: Consistent and calm. Every navigation does the same three things in the same order; the title always names the view that rendered; there are no timeouts, no destructive actions, no motion (`window.scrollTo` at `:50` omits `behavior: 'smooth'`, so nothing animates and `prefers-reduced-motion` has nothing to suppress). The not-found view is a real page with a real heading and a recovery instruction rather than a dead end (`:122-127`). Two small frictions: "Choose a section from the menu above" (`:125`) says "menu" for a region labeled "Account sections," and "above" is a spatial reference — harmless here since DOM order matches, but "from the Account sections navigation" would be exact. The Back-navigation scroll reset noted under Enhancements is the more substantive cognitive cost.

---

**Verdict Justification**

The component does the hard thing correctly and, unusually, does it for defensible reasons that survive checking. I verified three of its non-obvious claims rather than accepting them: the StrictMode guard at `:40` genuinely is idempotent under mount-effect replay where a boolean would not be; the no-redirect decision at `:266` is not a rationalization — I traced the `<Navigate replace>` path and it does fire focus on cold load exactly as claimed; and the `role="list"` attributes are justified by the `list-style: none` rules in the same file. Feature claims 1, 2, 3, 4, and 6 verify. Claim 5 verifies for the target it names and exposes the gap in Minor 1 by not extending to the other one.

**Severity recalibrations under Realist Check:**
- Minor 1 (skip-link focus indicator) was drafted **MAJOR** and downgraded. *Mitigated by:* the nav is three links, so the bypass saves almost nothing when it fails, and screen reader users get `<main>` and the heading announced normally. The affected group is narrow (sighted keyboard-only) and the workaround (tab through three links) is immediate. It stays the highest-value fix in this review — one selector — but it is friction, not a barrier.
- The Major (viewport meta) was tested for downgrade and **holds**. Content remains reachable via pinch-zoom, so it is not CRITICAL, but there is no in-page workaround: two-dimensional scrolling to read body text is the failure state 1.4.10 exists to define, and it affects a whole user category on the most common device class.
- The unlabeled currency amounts were drafted as a 1.3.1 finding and removed to Enhancements. *Mitigated by:* no visible column header exists either, so screen reader users are not disadvantaged relative to sighted users. Reporting it as a finding would have been a manufactured violation.

**To upgrade to ACCEPT**: add the viewport meta. The two Minors are worth fixing and neither blocks — I would ship the component with them open. **If the `index.html` at `:144-157` is abridged for the fixture and the real document has a viewport tag, this is an ACCEPT with two minor notes.**

---

**Open Questions (unscored)**

1. Is `index.html` (`:144-157`) the complete shipped document or a snippet included to show the title mechanism? The whole Major turns on this, and the comment at `:145` reads as illustrative.
2. Do any routes become lazy/Suspense-wrapped later? The single `requestAnimationFrame` at `:49` is sufficient for a synchronous commit but not for a heading that arrives on a later frame or after a Suspense boundary resolves. Not a defect in this code — a constraint the design carries forward.
3. Will anything else write to `document.title` (a notification counter, an analytics wrapper)? `ViewHeading` assumes exclusive ownership at `:23`, with no coordination mechanism if a second writer appears.
4. Are the account amounts ever something other than a current balance (pending, available, minimum due)? If the column can change meaning, the Enhancement about labeling becomes a real 1.3.1 finding.

---

## Provenance

I read exactly one file:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-clean.blind.md` (read in full, 273 lines, via the Read tool)

No other file was opened. I ran no Grep, Glob, Bash, or git command in this session, and issued no other tool call of any kind — the Read above is the only tool invocation. Nothing under `evals/suites/` was accessed, no `*.metadata.yaml` or `*.rubric.yaml` was accessed, and I did not search the repository or its history for this fixture. All line citations refer to the numbering of the file as given to me.

Contrast ratios in the low-vision section were computed from the hex values in the file's CSS using the WCAG relative-luminance formula, not measured in a browser — a live axe-core `color-contrast` run would upgrade them from calculation to measurement. Reflow, target size, and forced-colors conclusions are likewise derived from the CSS by reasoning about layout, not observed in a rendered page; a keyboard-a11y-tester journey run or an `agent-browser` session at a 320px viewport would convert them to measured evidence, and is the natural next step for confirming the Major.