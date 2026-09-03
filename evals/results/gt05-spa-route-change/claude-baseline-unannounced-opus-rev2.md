I'll read the specified file.

---

## Verdict: REVISE

Two defects in the same failure family — the app changes what page you are on without telling anyone who isn't looking at the screen. Everything else in this file is competent.

---

## Findings

### 1. Route change moves no focus and fires no announcement — MAJOR
**WCAG 2.4.3 Focus Order (A)** — with 4.1.3 Status Messages (AA) as a weaker secondary mapping
`spa-route-change-unannounced.blind.md:80-88`

`PortalShell` is a pure function with no `useLocation`, no `useEffect`, and no ref. Activating a `NavLink` swaps the subtree inside `<main>` (`:81`), and the nav stays mounted, so focus stays sitting on the link the user just activated. Nothing is focused in the new view, and there is no live region anywhere in the tree.

What a screen reader user experiences: press Enter on "Transfers", hear nothing. The `aria-current="page"` flip on the still-focused link is announced inconsistently across NVDA/JAWS/VoiceOver and is not a substitute for "you are now on Transfers." The user's next Tab lands in the *new* view's content with no `<h1>` ever read, so their mental model of where they are is stale until they manually browse backward to find the heading.

The `tabIndex={-1}` on `<main>` at `:80` is the tell. It exists so the skip link can target it — and it is exactly the hook a route-change focus handler would use, but nothing ever calls `.focus()` on it. Half the mechanism is built.

Not CRITICAL: the new content is still reachable and readable; this is a disorientation and efficiency barrier, not a lockout.

**Honest note on the SC mapping.** SPA route announcement has no clean single success criterion — this is a well-known gap in WCAG. 2.4.3 is the strongest fit (focus order after activation no longer preserves meaning). If your program requires an unambiguous normative citation, the defensible one is #2 below; treat this one as a best-practice failure with real user impact regardless of which number you file it under.

---

### 2. `document.title` never changes across routes — MAJOR
**WCAG 2.4.2 Page Titled (A)**
`spa-route-change-unannounced.blind.md:96, 101`

The comment at `:96` states it outright: `index.html` is the only place a title is set, and it is the static string `Ridgeline Credit Union` (`:101`). These are real routes with real URLs (`/accounts`, `/transfers`, `/statements`, plus a 404) — four distinct pages, one title.

Consequences that persist beyond the session: every browser-history entry, every bookmark, and every open tab reads identically, so the user cannot tell them apart later. The screen reader "read title" command (Insert+T / VO-Shift-I) — the standard recovery move when you are lost, and the one a user would reach for *because* of finding #1 — returns nothing useful. `NotFoundView` (`:42-47`) is the worst case: the error page announces itself as the bank's home page.

This is the cleanest normative failure in the file. 2.4.2 requires titles that describe topic or purpose; one title for four purposes does not.

---

### 3. Skip link is `position: absolute` against the document, not the viewport — MINOR
**WCAG 2.4.11 Focus Not Obscured (Minimum) (AA)**
`spa-route-change-unannounced.blind.md:151-162`

`.skip-link` is `position: absolute` (`:152`) and no ancestor establishes a containing block — `.portal`, `.portal-header`, and `.portal-main` all lack `position`. So `:focus` placing it at `top: 8px` (`:158`) pins it to the top of the *document*, not the viewport.

Scrolled to the bottom of a long statements list, a Shift+Tab back to the first focusable element focuses a skip link rendered entirely off-screen. Focus is visually lost with no indicator anywhere on screen. `position: fixed` fixes it.

Flagged MINOR rather than MAJOR because the reaching sequence is uncommon: the skip link is normally encountered at page top before any scrolling. I have not rendered this; the mechanism is read off the CSS cascade, and the finding is conditional on scroll position.

---

### 4. Account name/balance pairing relies on DOM adjacency only — ENHANCEMENT
`spa-route-change-unannounced.blind.md:12-19`

Each row is two bare `<span>`s inside an `<li>`. A screen reader reads "Everyday Checking $2,418.06" as one linear run, and visual order matches DOM order (`justify-content: space-between` does not reverse anything), so the relationship *is* conveyed.

**This is not a 1.3.1 violation** — the `<li>` grouping carries the relationship, and I am not claiming otherwise. A `<dl>` with `<dt>`/`<dd>`, or `<table>` if more columns arrive, would make the label/value roles explicit and would survive the row growing a third field. File it as design robustness, not a defect.

---

## What I checked and am deliberately not flagging

Naming the negative space so this doesn't get re-litigated:

- **`role="list"` on the `<ul>`s** (`:11, :35, :64`) — correct and intentional, not redundancy. The CSS sets `list-style: none` (`:126, :177`), which strips list semantics in WebKit; the explicit role restores them.
- **Focus indicators** — `#0b4fa8` on white is **7.8:1**, well past the 3:1 in 1.4.11 and 2.4.11. No `outline: none` appears anywhere in the file, so the statement PDF links keep the UA default ring. Fine.
- **Text contrast** — `#1d2939` and `#0b4fa8` on white, and white on `#0b4fa8` (7.8:1). All pass AA.
- **1.4.1 Use of Color** — the active nav link carries three cues: color, `border-bottom` underline (`:140`), and `font-weight: 600` (`:141`), plus `aria-current="page"` from `NavLink`. Passes.
- **2.5.8 Target Size (Minimum)** — nav links compute to ~31px tall. Statement links are ~19px tall but sit ~40px apart center-to-center (10px+10px padding + border), so 24px circles don't intersect: the spacing exception applies. Passes.
- **Landmarks and headings** — `<header>` is an unnested banner, `<nav>` is disambiguated by `aria-label="Account sections"`, `<main>` has the skip target, each view carries exactly one `<h1>`, and the brand is a `<span>` rather than a competing heading. All correct.
- **`<Navigate replace />`** (`:82`) — an immediate redirect with no delay; 2.2.1 and 3.2.5 don't engage.
- **"Choose a section from the menu above"** (`:45`) — a spatial reference, but the nav does precede `<main>` in DOM order, so it's accurate for linear readers too. Not worth a finding.

---

## The through-line

Findings #1 and #2 are one bug wearing two hats. The author built real routes with real URLs and real history — and then left the two things that tell a non-visual user *which* route they are on. Fixing them is one `useEffect` on `useLocation()`: set `document.title` from the matched section, and either focus the `<main>` that already has `tabIndex={-1}` waiting for it or push the view name into a polite live region. Fix one without the other and the user still has no orientation signal from a cold start.

## Provenance

Files read:
- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-unannounced.blind.md`

No other file was read. No grep, no git, no skill invocation, no browser. Contrast values were computed by hand from the hex codes in the file; target sizes and the skip-link containing block were derived from the CSS as written, not from a rendered page.