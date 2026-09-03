I'll read the specified file.

---

## Verdict: **ACCEPT**

The thing this code is actually about — client-side route change announcement — is correct, and correct in the ways that are easy to get wrong. Title derives from the same `SECTIONS` source that renders the nav (`spa-route-change-clean.blind.md:26-28`), focus moves to a `tabIndex={-1}` `<h1>` after the DOM commits (`:33-43`, `:71-73`), first render is exempt, scroll and focus are separated with `preventScroll`, and nothing anywhere sets `outline: none`. My findings are all MINOR or below and none of them are in the route-change mechanism.

One caveat on the verdict, stated plainly: **finding 1 is an estimate, not a measurement.** If someone renders this at a 320px viewport and the header does overflow, that is a straight WCAG 2.2 AA failure and the verdict flips to REVISE. I have no browser evidence, only text-metric arithmetic.

## Findings

**1. MINOR — Header row cannot reflow to 320px (WCAG 1.4.10 Reflow, AA)**
`spa-route-change-clean.blind.md:132-146` (`.portal-header` / `.section-nav`), rendering `:51-67`

Neither flex container sets `flex-wrap`, and there are no media queries. Flex items won't shrink below `min-width: auto` (min-content), so the floor is roughly: "Ridgeline" (~72px) + 32px gap + the three nav labels at min-content (~216px) + 40px of gaps + 48px header padding ≈ **~408px**. At a 320px viewport (400% zoom on a 1280px screen) that overflows by ~90px, so a low-vision user gets a horizontal scrollbar to reach the nav. `<main>` reflows fine — this is header-only, which is why I rate it MINOR rather than MAJOR. Fix is one line: `flex-wrap: wrap` on both.

Confidence: moderate. Character-width arithmetic at a 16px default, not a measured render.

**2. MINOR — `list-style: none` strips list semantics in Safari/VoiceOver (WCAG 1.3.1, A — arguably accessibility-support rather than a strict failure)**
`spa-route-change-clean.blind.md:140-146`, `:193-198`

All three lists (`.section-nav`, `.account-list`, `.statement-list`) remove the marker. WebKit drops the `list` role when it does, so VoiceOver users lose "list, 3 items" on the nav and on the account/statement lists — the item count is exactly the orientation cue those lists exist to provide. The markup is correct; the browser discards it. Add `role="list"` to the three `<ul>`s.

I flag this knowing reasonable practitioners call it a WebKit bug rather than an authoring defect. It's still the highest-impact real thing in the file, and Safari+VoiceOver is not a fringe pairing.

**3. ENHANCEMENT — Skip-link target is not focusable**
`spa-route-change-clean.blind.md:47-49` → `:70`

`href="#main-content"` points at a `<main>` with no `tabIndex={-1}`. Current Chrome, Firefox, Safari and Edge handle this correctly via the sequential focus navigation starting point, so this is not a 2.4.1 failure today. Adding `tabIndex={-1}` to `<main>` costs nothing and removes the dependency on that behavior. Not a defect; a hardening.

**4. ENHANCEMENT — No index or catch-all route; the `'Not found'` branch is unreachable**
`spa-route-change-clean.blind.md:101-109`, `:72`

`PortalShell` is a pathless layout route whose only children are the three section paths. At `/`, or at any unmatched URL, no branch matches and `<Routes>` renders `null` — no shell, no nav, no heading, and the title effect never runs, so the document keeps whatever title it had. The `section ? section.title : 'Not found'` fallback at `:72` can never render. A screen reader user who lands there gets an empty document with a stale title and no landmarks to navigate out. This is a routing gap rather than a WCAG criterion violation, and it's plausibly a fixture artifact, so it does not affect the verdict.

Related latent inconsistency, same root: `section` is found by **exact** pathname match (`:22`) while `NavLink` marks active by **prefix** match (no `end` prop, `:57-61`). The moment a sub-route like `/accounts/checking` exists — and `:82-83` links to exactly that — the nav will report `aria-current="page"` on Accounts while the `<h1>` reads "Not found". Add `end` to the `NavLink`s, or match `section` by prefix, when sub-routes land.

## What I deliberately did not flag

Naming the negative space, since most of it reads like a defect to a mechanical pass:

- **No `aria-live` route announcer.** Correct. Focus moving to the heading announces it; an announcer alongside it would double-speak.
- **`tabIndex={-1}` on an `<h1>`.** Correct and standard — programmatic focus target, stays out of the Tab order.
- **First render doesn't move focus.** Correct, and the reasoning at `:30-32` is right: moving focus on load skips the skip link and nav for a user who hasn't seen either.
- **`preventScroll: true`.** Correct, because `:39` scrolls the window explicitly first. The heading is in view when it takes focus.
- **`:focus-visible`-only indicator on `.view-heading` (`:161-167`).** Works as claimed. Chromium's heuristic propagates `:focus-visible` through programmatic focus when the previously focused element matched it — so a keyboard activation of a nav link shows the outline and a mouse click doesn't. The heading isn't keyboard-operable, so 2.4.7 doesn't apply to it regardless.
- **`aria-current` duplicating `NavLink`'s own default.** Redundant, harmless — explicit `undefined` hits the destructuring default and still yields `"page"`.
- **Contrast.** `#0b4fa8` on white computes to **7.78:1** — passes AA and AAA for text, and the focus outline clears 1.4.11's 3:1 with room. `#1d2939` nav text is far darker. The `#d0d5dd` and `#eaecf0` borders are decorative and out of 1.4.11's scope.
- **Active nav state.** Color *plus* `font-weight: 600` *plus* `border-bottom` *plus* `aria-current` — not color alone, so 1.4.1 holds.
- **Target size (2.5.8).** Nav links are ~31px tall. The account/statement links are ~19px tall but their centers sit ~40px apart, clearing the 24px spacing exception.
- **`window.scrollTo` without `behavior: 'smooth'`.** Instant scroll — nothing for `prefers-reduced-motion` to suppress.
- **StrictMode double-invoking the focus effect** (dev-only focus move on initial load). Real, but doesn't ship.

I ran no tooling — no browser, no axe, no measurement. Everything above is source reading.

## Provenance

Files read (1):

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-clean.blind.md`

No other file was read, no search or `git` command was run, and no skill was invoked.