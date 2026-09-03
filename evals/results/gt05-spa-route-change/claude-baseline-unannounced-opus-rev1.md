I'll read the specified file.

---

## Verdict: **REVISE**

The router is wired for sighted mouse users only. Every channel that tells a non-sighted user "the navigation worked" — focus, document title, live region — is absent, and the one bypass mechanism that exists (the skip link) lands on a non-focusable target.

---

### F1 — Route change produces no programmatic signal of any kind — CRITICAL
**WCAG:** 4.1.3 Status Messages (AA) is the conventional cite; 2.4.3 Focus Order (A) is the stronger hook for the focus half. Honest caveat: no single SC maps cleanly to SPA route changes, which is exactly why this defect survives automated scans.
**Where:** `spa-route-change-unannounced.blind.md:43` (`useLocation` is consumed only to compute a class/attribute), `:70-76` (`<main>` swaps children with no side effect), `:57-63`.

`PortalShell` subscribes to location but never reacts to it. When a screen reader user activates "Transfers", the virtual cursor and DOM focus both stay on the link in the header. `<main>` is replaced silently. There is no `useEffect` moving focus to the new view's `<h1>` or to `<main>`, no `role="status"`/`aria-live` region announcing the section, and no `tabindex="-1"` anywhere to receive focus.

`aria-current="page"` (`:60`) does not rescue this — screen readers do not reliably re-announce a changed `aria-current` on an already-focused element, so the attribute is correct and inert.

**Why CRITICAL rather than MAJOR:** the user cannot distinguish "route changed" from "activation did nothing." A sighted user gets the full answer instantly; a screen reader user gets zero bits. A reviewer could defensibly argue MAJOR — the content is still reachable by arrowing down or jumping by heading — and I'd accept that downgrade. I'm rating CRITICAL because this is a money-movement flow where acting on the wrong section has real consequences, and because all three confirmation channels fail simultaneously rather than one.

**Fix:** on `pathname` change, move focus to the view's `<h1>` (give it `tabindex="-1"`) or to `<main tabindex="-1">`, and set the title. Do not add a live region *and* move focus — that double-announces.

---

### F2 — Document title never changes across routes — MAJOR
**WCAG:** 2.4.2 Page Titled (Level A)
**Where:** `spa-route-change-unannounced.blind.md:85` (the comment states this outright), `:90`.

These are real routes with real URLs (`:190`), so each is a web page under WCAG's definition and each needs a title describing its topic. All three report "Ridgeline Credit Union." Consequences beyond screen readers: browser history entries are indistinguishable, tabs are indistinguishable, bookmarks are indistinguishable, and back/forward navigation (`:190`) gives no confirmation either. This one is normatively unambiguous — unlike F1, there is nothing to argue about.

---

### F3 — Skip-link target is not focusable — MAJOR
**WCAG:** 2.4.1 Bypass Blocks (Level A)
**Where:** `spa-route-change-unannounced.blind.md:47-49` (the link), `:70` (`<main id="main-content">` with no `tabindex="-1"`).

Fragment navigation to a non-focusable element scrolls reliably but sets focus inconsistently across browser/AT pairs — Safari historically leaves focus on the link, so the next Tab returns to the nav the user was trying to escape. The mechanism is present and looks correct in code review; it fails in delivery.

This compounds F1: the skip link is the natural focus destination after a route change, and it is broken in the one place a fix for F1 would want to reuse it. Add `tabindex="-1"` to `<main>`.

---

### F4 — Header does not reflow at narrow widths — MAJOR
**WCAG:** 1.4.10 Reflow (AA)
**Where:** `spa-route-change-unannounced.blind.md:102-108` (`.portal-header`, `display:flex`, `gap:32px`, no `flex-wrap`), `:110-116` (`.section-nav`, same).

Neither flex container wraps. Rough minimum content width: brand text (~150px) + 32px gap + three nav labels (~210px) + 40px of inter-item gaps + 48px horizontal padding ≈ 480px. At a 320px viewport — equivalently, 400% zoom on a 1280px display — the header forces horizontal scrolling of the whole page. Add `flex-wrap: wrap` to both, or collapse the nav below the brand under a breakpoint.

I have moderate confidence in the arithmetic (font stack and sizes aren't specified for the brand or nav), but the structural point holds regardless of exact metrics: nothing here can wrap.

---

### F5 — Two competing sources of truth for "current" — MINOR
**WCAG:** 1.3.1 Info and Relationships (A) — a weak fit; this is better read as a consistency/robustness defect than a clean SC failure.
**Where:** `spa-route-change-unannounced.blind.md:59-60`.

`NavLink` sets `aria-current="page"` itself using prefix matching, and line 60 hand-computes it with exact matching (`pathname === path`). Which one reaches the DOM depends on react-router's internal prop ordering — I am not confident enough in the version-specific source to state a winner, and that uncertainty *is* the finding: the visual `is-active` styling (`:59`, prefix-matched) and the programmatic current state (`:60`, exact-matched) can disagree on any nested path like `/accounts/checking`. Delete line 60 and let `NavLink` own the attribute.

---

### F6 — Content links leave the SPA and land on undefined routes — MAJOR
**WCAG:** No direct SC. This is a functional defect whose *resulting state* fails 2.4.2 and leaves the document with no `<h1>`.
**Where:** `spa-route-change-unannounced.blind.md:12-13`, `:30-31`, against the route table at `:36-40` and `:71-75`.

The account and statement links are plain `<a href>`, not `NavLink`/`Link`, so they trigger full page loads. `/accounts/checking`, `/statements/2026-08` etc. match no `<Route>`, and there is no catch-all or index route — so `<Routes>` renders nothing and the user lands on a page with an empty `<main>`, no heading, no error message, and the same generic title. Same result on initial load at `/`.

Flagging this because the failure mode is far worse for AT users than for sighted ones: a sighted user sees a blank page and hits back; a screen reader user gets a page with a nav, a brand, and nothing else, with no signal that anything went wrong.

---

### F7 — Brand text is not a home link — ENHANCEMENT
**Where:** `spa-route-change-unannounced.blind.md:52`.

`<span className="brand">` is inert. Users expect the masthead to return home; there is currently no route to return to (see F6). Low impact, listed for completeness.

---

## Checked and clean — not defects

Stating these explicitly so the negative space is as specific as the findings:

- **Color contrast.** `#0b4fa8` on white computes to ~7.8:1 — passes 1.4.3 AA for the active nav link, the focus outline (1.4.11, needs 3:1), and the white-on-blue `.primary` button. `#1d2939` on white is far above threshold.
- **Use of color alone (1.4.1).** Active state is carried by underline *and* weight *and* color *and* `aria-current` — not color alone.
- **Focus visibility (2.4.7).** No rule anywhere sets `outline: none`. `:focus-visible` outlines are added for three element classes; the account/statement links keep the UA default ring. Nothing is suppressed.
- **Target size (2.5.8 AA).** Nav links compute to ~31px tall. The list links are ~19px tall, under 24px, but `li` padding puts ~39px between target centers — clears the undersized-target spacing exception.
- **Heading structure.** Exactly one `<h1>` per rendered view, inside `<main>`. Correct.
- **`<section className="view">` without an accessible name.** Not exposed as a region by AT — harmless, not a finding.
- **`<nav aria-label="Account sections">`.** Correctly labeled; would only matter if a second `<nav>` existed, and the label is meaningful either way.
- **Off-screen skip-link technique (`left:-9999px` → repositioned on `:focus`).** Standard and correct — it is the *target*, not the link, that is broken (F3).

---

## Where my confidence drops

- **F1's severity.** The CRITICAL/MAJOR line here is a judgment call about whether "disoriented with no confirmation" counts as blocked. I've argued CRITICAL; I would not fight a MAJOR.
- **F1's SC citation.** SPA route changes have no well-fitting success criterion. Anyone who cites 4.1.3 confidently is citing a convention, not a normative mapping.
- **F5's actual runtime behavior.** I did not verify react-router's prop precedence for this version, and I was instructed not to read other files. The divergence risk stands either way.
- **F4's exact breakpoint.** Estimated from character counts without a specified font stack.

---

## Provenance

Files read (exactly one):

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-unannounced.blind.md`

No other file was read, no search or grep was run, no git command was run, and no skill was invoked.

---

Resending from F4 onward.

---

### F4 — Header does not reflow at narrow widths — MAJOR
**WCAG:** 1.4.10 Reflow (AA)
**Where:** `spa-route-change-unannounced.blind.md:102-108` (`.portal-header`, `display:flex`, `gap:32px`, no `flex-wrap`), `:110-116` (`.section-nav`, same).

Neither flex container wraps. Rough minimum content width: brand text (~150px) + 32px gap + three nav labels (~210px) + 40px of inter-item gaps + 48px horizontal padding ≈ 480px. At a 320px viewport — equivalently, 400% zoom on a 1280px display — the header forces horizontal scrolling of the whole page. Add `flex-wrap: wrap` to both, or collapse the nav below the brand under a breakpoint.

I have moderate confidence in the arithmetic (font stack and sizes aren't specified for the brand or nav), but the structural point holds regardless of exact metrics: nothing here can wrap.

---

### F5 — Two competing sources of truth for "current" — MINOR
**WCAG:** 1.3.1 Info and Relationships (A) — a weak fit; this is better read as a consistency/robustness defect than a clean SC failure.
**Where:** `spa-route-change-unannounced.blind.md:59-60`.

`NavLink` sets `aria-current="page"` itself using prefix matching, and line 60 hand-computes it with exact matching (`pathname === path`). Which one reaches the DOM depends on react-router's internal prop ordering — I am not confident enough in the version-specific source to state a winner, and that uncertainty *is* the finding: the visual `is-active` styling (`:59`, prefix-matched) and the programmatic current state (`:60`, exact-matched) can disagree on any nested path like `/accounts/checking`. Delete line 60 and let `NavLink` own the attribute.

---

### F6 — Content links leave the SPA and land on undefined routes — MAJOR
**WCAG:** No direct SC. This is a functional defect whose *resulting state* fails 2.4.2 and leaves the document with no `<h1>`.
**Where:** `spa-route-change-unannounced.blind.md:12-13`, `:30-31`, against the route table at `:36-40` and `:71-75`.

The account and statement links are plain `<a href>`, not `NavLink`/`Link`, so they trigger full page loads. `/accounts/checking`, `/statements/2026-08` etc. match no `<Route>`, and there is no catch-all or index route — so `<Routes>` renders nothing and the user lands on a page with an empty `<main>`, no heading, no error message, and the same generic title. Same result on initial load at `/`.

Flagging this because the failure mode is far worse for AT users than for sighted ones: a sighted user sees a blank page and hits back; a screen reader user gets a page with a nav, a brand, and nothing else, with no signal that anything went wrong.

---

### F7 — Brand text is not a home link — ENHANCEMENT
**Where:** `spa-route-change-unannounced.blind.md:52`.

`<span className="brand">` is inert. Users expect the masthead to return home; there is currently no route to return to (see F6). Low impact, listed for completeness.

---

## Checked and clean — not defects

Stating these explicitly so the negative space is as specific as the findings:

- **Color contrast.** `#0b4fa8` on white computes to ~7.8:1 — passes 1.4.3 AA for the active nav link, the focus outline (1.4.11, needs 3:1), and the white-on-blue `.primary` button. `#1d2939` on white is far above threshold.
- **Use of color alone (1.4.1).** Active state is carried by underline *and* weight *and* color *and* `aria-current` — not color alone.
- **Focus visibility (2.4.7).** No rule anywhere sets `outline: none`. `:focus-visible` outlines are added for three element classes; the account/statement links keep the UA default ring. Nothing is suppressed.
- **Target size (2.5.8 AA).** Nav links compute to ~31px tall. The list links are ~19px tall, under 24px, but `li` padding puts ~39px between target centers — clears the undersized-target spacing exception.
- **Heading structure.** Exactly one `<h1>` per rendered view, inside `<main>`. Correct.
- **`<section className="view">` without an accessible name.** Not exposed as a region by AT — harmless, not a finding.
- **`<nav aria-label="Account sections">`.** Correctly labeled; would only matter if a second `<nav>` existed, and the label is meaningful either way.
- **Off-screen skip-link technique (`left:-9999px` → repositioned on `:focus`).** Standard and correct — it is the *target*, not the link, that is broken (F3).

---

## Where my confidence drops

- **F1's severity.** The CRITICAL/MAJOR line here is a judgment call about whether "disoriented with no confirmation" counts as blocked. I've argued CRITICAL; I would not fight a MAJOR.
- **F1's SC citation.** SPA route changes have no well-fitting success criterion. Anyone who cites 4.1.3 confidently is citing a convention, not a normative mapping.
- **F5's actual runtime behavior.** I did not verify react-router's prop precedence for this version, and I was instructed not to read other files. The divergence risk stands either way.
- **F4's exact breakpoint.** Estimated from character counts without a specified font stack.

---

## Provenance

Files read (exactly one):

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-unannounced.blind.md`

No other file was read, no search or grep was run, no git command was run, and no skill was invoked.