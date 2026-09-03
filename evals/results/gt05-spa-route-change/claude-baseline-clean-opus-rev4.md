I'll read the file and analyze it.

---

## Verdict: **ACCEPT**

No CRITICAL or MAJOR defects. The route-change handling is correct on all three traces. Findings below are one MINOR and four ENHANCEMENTs — none blocks ship.

---

## Traces

**Cold load (`/accounts`, or any deep link)** — `previousPath` is initialized to the current pathname (`:40`), so the guard at `:47` returns before the rAF is ever scheduled. Focus stays where the browser put it; no scroll jump. Child effects run before parent effects, so `ViewHeading` sets `document.title` (`:23`) in the same commit. Correct, and the StrictMode reasoning at `:36-39` holds — the ref survives the double-invoke because React reuses the fiber rather than remounting, so both runs hit the early return.

**In-app navigation (`/accounts` → `/transfers`)** — `PortalShell` stays mounted via `Outlet` (`:82`). `AccountsView` unmounts, `TransfersView` mounts, its `ViewHeading` effect rewrites the title, then the shell's effect fires: guard passes, ref updates, rAF defers to after DOM commit so `querySelector('h1')` (`:51`) resolves against the *new* view. `window.scrollTo` then `focus({preventScroll: true})` in that order (`:50-51`) is the right sequence. `tabIndex={-1}` (`:27`) makes the `<h1>` a programmatic-only target. Heading text is announced; next Tab lands inside the new content. Correct.

**Unmatched URL (`/`, `/Accounts`, `/accounts/`)** — React Router's own matching decides, and the title is derived from the view that rendered rather than a second `pathname === path` lookup, so `/accounts/` and `/Accounts` render Accounts *and* are titled Accounts. The catch-all (`:135`) is inside the layout route, so the shell renders and `NotFoundView` owns its own `<h1>` and title. No URL yields an untitled or mis-titled document. Correct — this is the part most implementations get wrong.

---

## Findings

**1. MINOR — Back/Forward navigations are treated as forward navigations; restored scroll position is destroyed**
`spa-route-change-clean.blind.md:46-54`
The effect keys on `pathname` alone and cannot distinguish PUSH from POP. Pressing Back from `/transfers` to a `/statements` view the user had scrolled down in resets scroll to top (`:50`) and yanks focus to the `<h1>` (`:51`). Native browser behavior would restore both. For a user with working-memory or attention constraints, "go back" no longer returns them to where they were.
**No SC maps cleanly** — 2.4.3 Focus Order is arguably still satisfied (the destination is meaningful) and there is no SC for scroll restoration. I am reporting this as a real cognitive-access regression against browser-native behavior, not as a WCAG failure. Fix: read `useNavigationType()` and skip the scroll reset (keep the focus move, or skip both) on `POP`.

**2. ENHANCEMENT — `:focus-visible` on a programmatic focus target leaves mouse-initiated navigations with no visible landing point**
`spa-route-change-clean.blind.md:193-199` (specifically `:196`)
`.view-keading:focus-visible` only matches when the UA's heuristic says the interaction was keyboard-driven. Click a NavLink with a mouse and the link itself never matches `:focus-visible`, so the programmatically focused `<h1>` doesn't either — focus moves, the page scrolls, and nothing marks where focus went. This matters most for screen-magnifier users, who click with a pointer but then operate by keyboard.
**Not a 2.4.7 failure** — the `<h1>` is `tabIndex={-1}` and not keyboard-operable, so Focus Visible does not reach it. Contrast is fine either way: `#0b4fa8` on white measures ≈7.8:1, well past the 3:1 that 1.4.11 asks of indicators. This is a defensible design choice; switching to `:focus` guarantees the indicator at the cost of showing a ring to mouse users. Flagging so the tradeoff is deliberate rather than inherited.

**3. ENHANCEMENT — the `<main tabIndex={-1}>` fallback exists but is never used**
`spa-route-change-clean.blind.md:51` (target), `:81` (unused fallback)
`mainRef.current?.querySelector('h1')?.focus()` silently no-ops if a view lacks an `<h1>`. Focus then stays on the activated NavLink and the navigation is announced to nobody. Every current view routes through `ViewHeading`, so **this is not a live defect** — it's a failure mode with no guard. `:81` already provides `tabIndex={-1}` on `<main>`; chain to it: `(mainRef.current?.querySelector('h1') ?? mainRef.current)?.focus({preventScroll: true})`.

**4. ENHANCEMENT — account name/balance pairs carry a visual relationship with no programmatic counterpart**
`spa-route-change-clean.blind.md:92-99`, CSS `:232-239`
Two sibling `<span>`s laid out with `justify-content: space-between` read visually as label→value. A screen reader gets "Everyday Checking $2,418.06" from DOM order within the `<li>`, which is why I do **not** call this a 1.3.1 failure at two columns. It stops being adequate the moment a third column (available balance, account number) is added, at which point the visual grouping is real structure that isn't in the markup. `<dl>` now, or a `<table>` when columns grow.

**5. ENHANCEMENT — generic `<title>` on cold load until hydration; `/` renders "Page not found"**
`spa-route-change-clean.blind.md:150` (initial title), `:135` (catch-all), `:63` (brand is a non-interactive span)
A client-side deep link to `/statements` is titled "Ridgeline Credit Union" until the effect at `:23` runs — a window that is slow-connection-sized, not zero. **This does not fail 2.4.2**: a descriptive title is present, it just names the site rather than the view. Prerender/SSR the per-route title if the window matters. Separately, `/` renders "Page not found" and the brand at `:63` is a plain `<span>`, so there is no home affordance. **2.4.5 Multiple Ways (AA) is unjudgeable from this fragment** — the nav is one way; whether a search or sitemap exists elsewhere isn't visible here.

---

## Verified clean (not findings)

Stating these so the ACCEPT isn't read as "didn't look": `role="list"` is applied to all three `list-style: none` lists (`:65`, `:91`, `:115`) — the Safari semantics-stripping fix, correctly applied everywhere it's needed, not just once. Skip link is real and reachable (`:58-60`, CSS `:201-212` — off-screen via `left`, never `display:none`). Landmarks are complete and unnested (`<header>` inside plain `<div>`s still maps to `banner`). One `<h1>` per view, no skipped levels. No `outline: none` anywhere, so the unclassed PDF links at `:116-117` fall back to the UA focus ring rather than losing one. `aria-current="page"` comes from `NavLink`, and the active state carries color + border + weight, so it survives forced-colors. Target sizes pass 2.5.8: nav links ≈31px tall; the PDF links are ~19px tall but pass the spacing exception at ≈40px center-to-center. `flex-wrap` on both header and nav; no fixed heights, so 1.4.10 and 1.4.12 hold. `scrollTo` has no `behavior: 'smooth'`, so there's no reduced-motion exposure.

## Where my confidence drops

Contrast ratios are hand-computed from the hex values, not tool-measured. `:focus-visible` behavior on programmatic targets is a UA heuristic that differs across Chrome/Firefox/Safari and across versions — finding 2 would need a real browser to confirm rather than refute. And I judged announcement behavior from the pattern, not from a screen reader: "focus a `tabIndex={-1}` heading" is the well-established route-change pattern, but I did not run NVDA/JAWS/VoiceOver against it. I reviewed source only — nothing rendered, no AT, no axe run.

## Provenance

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-clean.blind.md` — read in full (273 lines). No other file read; no grep, no git, no skill invoked.