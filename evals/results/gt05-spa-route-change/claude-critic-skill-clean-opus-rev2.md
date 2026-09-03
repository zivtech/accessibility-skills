I'll start by reading the fixture file — and only that file, per the blind protocol.

---

**VERDICT: REVISE**

**Overall Assessment**: The route-change design is deliberate and mostly excellent — the title/focus split, the `tabIndex={-1}` heading target, the `preventScroll` + `requestAnimationFrame` sequencing, and the StrictMode-resistant guard are all reasoned through rather than copied. One defect breaks a stated design guarantee: on a cold load of the application root, the first-render focus exemption does not fire, and focus is programmatically moved past the skip link and the entire nav. The guard logic is correct; the route table defeats it.

---

**Pre-commitment Predictions** (written before detailed trace)

For an SPA route-change component I expected: (1) focus moving on first load because the "have we mounted" guard is missing or broken; (2) title handled but focus not, or the reverse; (3) focus target lacking `tabindex="-1"`; (4) focus set synchronously before the new route's DOM commits, so it silently no-ops; (5) a live region used *instead of* focus, announcing the change but leaving the next Tab back in the nav; (6) `focus()` and scroll fighting each other.

Findings vs. predictions: 2, 3, 4, 5, and 6 are all handled correctly and explicitly commented. Prediction 1 hit — but through a mechanism I would have missed had I only audited the guard. The guard at `:39-40` is right. The redirect at `:113` is what breaks it. Worth flagging as a review-method note: checking the guard in isolation would have produced a false clean.

---

## Findings

### Major Findings

**1. On a cold load of `/`, the first-render focus exemption does not fire — focus is moved into the `<h1>`, past the skip link and all nav links.**

- **Evidence**: `spa-route-change-clean.md:113` renders `<Navigate to="/accounts" replace />` *inside* the layout route (`:112`), so `PortalShell` mounts at pathname `/` before the redirect. Traced:
  1. Render 1 at `/`: `previousPath = useRef(pathname)` (`:24`) initializes `current` to `'/'`.
  2. Commit 1: the focus effect (`:38-46`) evaluates `previousPath.current ('/') === pathname ('/')` → early return at `:39`. `current` stays `'/'`. Correct so far. `Navigate`'s effect fires `navigate('/accounts', {replace: true})`.
  3. Render 2 at `/accounts`: `useRef` is **not** re-initialized — `previousPath.current` is still `'/'`.
  4. Commit 2: dep `[pathname]` changed, effect re-runs. `'/' !== '/accounts'` → the guard does not return. `:43` calls `headingRef.current.focus({preventScroll: true})`.
- This is a production behavior, not a StrictMode dev artifact — the double-invoked mount effect returns early both times, and the redirect commit is a separate commit either way.
- **Contradicts the component's own stated contract**: `:237` ("The first page load leaves focus where the browser put it") and Feature 3 at `:247` ("the first render is deliberately exempt"). The guard satisfies `:237` only for direct section-URL loads (`/accounts`, `/transfers`, `/statements`, and the catch-all — all of which I verified pass). It fails on `/`, which `:113` establishes as the app's canonical entry point.
- **User groups impacted**: screen reader users, keyboard-only users, screen-magnifier users. A screen reader user opening the portal from a bookmark has their virtual cursor placed at "Accounts, heading level 1" — they never encounter the banner, the skip link, or the fact that three sections exist. A keyboard user's first Tab from the focused `<h1>` lands on the *next* focusable element in DOM order, which on `/accounts` is nothing (`AccountsView` at `:83-94` has no focusable content) — so Tab exits to browser chrome, with the entire nav behind them.
- **Expected behavior**: WCAG 2.2 **2.4.3 Focus Order** — focus sequence must preserve meaning and operability; placing the user past navigation they have not encountered on the entry view does not. Secondarily this undermines **2.4.1 Bypass Blocks**: the skip link at `:50-52` is rendered unreachable by forward Tab at the one URL where a user is most likely to want it.
- **Confidence: HIGH.** Code-traceable, not a judgment call. I stress-tested three refutations: `<Navigate>` must render to fire its effect, so `PortalShell` does mount at `/`; `useRef` initializes on render 1, before the effect that redirects; and commit 1 demonstrably ran (the guard's early return is what leaves `current` stale). None hold.
- **Realist Check → MAJOR, not CRITICAL.** *Mitigated by:* the nav remains reachable via Shift+Tab and via screen-reader landmark/heading navigation, so this is severe disorientation at the entry point rather than access loss. Not downgraded further: detection is silent — no axe rule covers it, and the natural Playwright assertion ("on load, focus is `document.body`") would be written against `/accounts` and pass.
- **Fix**: hoist the redirect out of the layout route so `PortalShell` never mounts at `/`:
  ```jsx
  <Routes>
    <Route path="/" element={<Navigate to="/accounts" replace />} />
    <Route element={<PortalShell />}>
      <Route path="/accounts" element={<AccountsView />} />
      {/* …unchanged… */}
    </Route>
  </Routes>
  ```
  `PortalShell` then mounts fresh at `/accounts`, `useRef(pathname)` initializes to `/accounts`, and the guard at `:39` fires correctly. This also removes a secondary symptom of the same root cause: today, commit 1 sets `document.title` to `"Page not found — Ridgeline Credit Union"` (via `:26-27, 31-33`) for one commit before correcting it. Same fix, so I am not counting it as a separate finding.
  If the route table must stay as-is, the alternative is to gate on navigation type rather than path equality — treat a `REPLACE` occurring before any user-initiated `PUSH`/`POP` as still-first-load (`useNavigationType()`), which is more logic for the same result.
- **Verification requirement**: this needs a keyboard/focus assertion, not a screenshot or an axe scan. Assert `document.activeElement === document.body` after loading `/` *and* after loading `/accounts`, then assert `activeElement` is the `<h1>` after an in-app link activation. A `virtual-screen-reader` phrase log would not settle it — this is operability evidence.

### Minor Findings

None that survived self-audit. Two candidates were moved to Open Questions below.

### Enhancements

- **Scroll position is destroyed on Back/Forward** (`:42`). `window.scrollTo({top: 0})` runs on every pathname change including POP, overriding native scroll restoration. Harmless on the two-item lists shown; a real regression risk once a statements list runs long — a user who scrolls, navigates away, and presses Back loses their place. Not a WCAG failure; a cognitive-load cost as content grows.
- **`scrollTo` uses default `behavior`** (`:42`), which resolves to the computed `scroll-behavior`. The CSS shown has no motion at all, so this is fine today — but if a global stylesheet later adds `html { scroll-behavior: smooth }`, every route change animates, and there is no `prefers-reduced-motion` query anywhere in this file to blunt it. `behavior: 'instant'` makes the intent explicit and immune.
- **Account name/balance pairing** (`:86-87`). Two sibling `<span>`s in a flex row; a screen reader reads "Everyday Checking $2,418.06" as one list item. Understandable, and the reading order matches the visual order — this is **not** a 1.3.1 failure. A `<dl>` or a visually-hidden "Balance" label would make the relationship explicit rather than inferred. Preference, not a gap.

---

**What's Missing** (gap analysis — verified absent, with severity honestly assigned)

I checked for the standard SPA/route-change absences. Most are present:

- `lang` attribute — present (`:128`).
- Skip link — present (`:50-52`), targets a focusable `<main>` (`:73`), uses `:focus` not `:focus-visible` (`:187`), which is correct for skip links.
- Landmark structure — `<header>` is not nested in a sectioning element (its `<div className="portal">` parent does not strip the role), so banner/navigation/main all resolve (`:54, 56, 73`).
- `role="list"` restored on every `list-style: none` list (`:57, 84, 104`) — the Safari/VoiceOver workaround, applied consistently.
- `aria-current="page"` on the active nav item — via `NavLink` (`:60`, asserted at `:240`).
- Non-color active-state indicator — border-bottom + font-weight, not color alone (`:168-172`), satisfying 1.4.1.
- Focus indicator contrast — `#0b4fa8` on white computes to **7.8:1**, comfortably over the 3:1 required by 2.4.11/2.4.7 (`:174-180`). Same value for the `.primary` button's white-on-blue text.
- Reflow — `flex-wrap: wrap` on both the header and the nav (`:145, 154`), no fixed heights, no horizontal overflow at 320px. 1.4.10 holds.
- Target size (2.5.8, Level AA in WCAG 2.2) — nav links compute to ~31px tall × 65-80px wide, over the 24×24 floor. The statement PDF links (`:105-106`) are inline and only ~19px tall, but the 21px of `li` padding plus border puts their centers ~40px apart, so the 24px-circle spacing exception applies. **Passes**; I checked this specifically because it is the easiest place to manufacture a false finding.

Genuinely absent, and correctly so: no live region for route announcements. Focus movement is the better choice here — it announces *and* repositions the Tab sequence, where a live region would announce while leaving the user's next Tab back in the nav.

---

**Multi-Perspective Notes**

- **Screen reader user**: Structure is clean — banner, labeled navigation, main, one `<h1>` per view whose text is the view identity. The title format at `:32` puts the section first, which is what gets heard first on a title query. The design correctly relies on focus rather than a live region. **The MAJOR finding lands hardest here**: entering at `/`, the virtual cursor is repositioned into the heading before the user has encountered the nav, and nothing announces that navigation exists.
- **Keyboard-only user**: Tab order matches DOM and visual order. No traps. Skip link works and its target is focusable. Focus indicator is present on every focusable element plus the programmatic heading target. **Broken only at the entry point**: loading `/` places focus mid-document, and on `/accounts` — which has no focusable content — the first Tab exits the page entirely.
- **Low vision (200% zoom, high contrast, magnifier)**: Reflow is deliberate and holds. All measured contrasts pass. Target sizes pass including the marginal inline PDF links. One consequence of the finding: a magnifier user loading `/` gets an unrequested viewport jump on first paint, since `:42` scrolls and focus relocates the magnifier's follow-point.
- **Cognitive**: Interaction model is consistent — every navigation does the same three things. The catch-all at `:117` keeps the shell mounted rather than dropping the user into an empty document, and the not-found state gets both a heading and a matching title rather than inheriting stale ones. No timeouts, no destructive actions. The scroll-reset-on-Back noted above is the one place consistency costs the user something.

---

**Verdict Justification**

REVISE rather than ACCEPT-WITH-RESERVATIONS: this is a behavioral defect on the application's canonical entry URL that invalidates one of the six accessibility features the component claims (`:247`), not a reservation about approach. It is also small — a three-line route restructure. Everything else in this component is above the bar, and several decisions (the pathname-comparison guard instead of a boolean, `preventScroll` with an explicit scroll, the rAF deferral) are correct for reasons that are commonly gotten wrong.

No severity recalibrations beyond the one recorded in the finding (CRITICAL → MAJOR, mitigated by Shift+Tab and structural-navigation recoverability). No findings were manufactured to fill sections — the Minor tier is empty because nothing survived self-audit there.

Upgrade to ACCEPT requires: the redirect moved out of the layout route, plus a focus assertion covering **both** `/` and a direct section URL. Testing only `/accounts` reproduces the blind spot that let this ship.

---

**Open Questions (unscored)**

1. **`:focus-visible` on a programmatically focused `<h1>`** (`:177`). Feature 5 (`:251`) claims the indicator shows "so that a sighted user who navigated by keyboard can see where focus landed." This depends on the UA heuristic that carries `:focus-visible` from the previously-focused element (the nav link) to a script-focused one. Chromium, Gecko, and WebKit all implement it, so I expect the claim holds — but the heuristic is descriptive in Selectors 4, not normative, and I cannot measure engine behavior from source. Confidence LOW; worth one `agent-browser` check (`focus` the nav link, press Enter, `get-attr` the computed outline on the `<h1>`) rather than a code change.
2. **Global stylesheet not in scope.** The reduced-motion and `scroll-behavior` note above assumes the CSS block at `:142-229` is the whole story. If a global reset or design-system sheet exists, the motion question needs re-asking against that file.
3. **Does any view ever gain a same-path content change** (query params, tab state within a section)? The guard at `:39` compares pathname only, so such a change would update content without moving focus. No such view exists today; this is a design constraint worth stating before the app grows.

---

## Provenance

Files read for this review — exactly one:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-clean.blind.md` (read in full, 254 lines, via the Read tool)

No other file was read. No `evals/suites/` path was accessed. No `*.metadata.yaml` or `*.rubric.yaml` was read. No grep, glob, or git command was run against this repository or any other. No web or documentation lookups were performed. All line citations refer to the file above, and all React/CSS/WCAG reasoning is from working knowledge applied to that source.