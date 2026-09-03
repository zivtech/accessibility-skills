I'll start by reading the single file I'm permitted to read.

---

**VERDICT: REVISE**

**Overall Assessment**: The static structure of this shell is genuinely well built — correct landmarks, a working skip link, a legitimate `tabIndex={-1}` target, justified `role="list"`, focus indicators well above the 3:1 floor, and reflow-friendly wrapping. Everything that happens *at render time* is sound. Everything that should happen *at transition time* is absent: focus is never moved, the document title never changes, and no live region exists. The result is a route change that is completely silent to assistive technology while passing every static scan.

**Pre-commitment Predictions** (written before reading the code, from the component type "SPA route change"):
1. Focus stays on the activated `NavLink`; no `useEffect` on location → **confirmed**
2. `document.title` never updates per route → **confirmed**
3. No `aria-live`/`role="status"` route announcer → **confirmed**
4. `aria-current` missing on the active nav item → **wrong**, `NavLink` supplies it
5. Scroll position not reset between routes → **confirmed**, but latent at this content length

Not predicted, found anyway: the missing viewport meta (Major #3), and that `tabIndex={-1}` on `<main>` is legitimately load-bearing for the skip link rather than abandoned scaffolding.

---

## Critical Findings

**C1 — A client-side route change produces no programmatic signal of any kind.**

`spa-route-change-unannounced.md:80-88` — `<Routes>` swaps the children of `<main>` on navigation. The file contains no `useLocation`, no `useEffect`, no `ref`, and no `.focus()` call anywhere in `PortalShell` (`:55-90`). It also contains no `aria-live` region, no `role="status"`, and no `role="alert"`.

After a screen reader user activates "Transfers" (`:67-72`), focus and the virtual cursor remain on the link they just activated. The entire content region beneath them is replaced silently. The three channels that normally confirm a navigation — focus relocation, document title change, and a live-region announcement — are simultaneously absent.

- **User group**: screen reader users (primary); keyboard-only users (secondary — their next Tab goes to the next nav link, not the new content)
- **WCAG**: 2.4.3 Focus Order (A) is the anchor; 4.1.3 Status Messages (AA) applies to the missing announcement channel
- **Confidence**: HIGH
- **Why this matters**: The user receives no evidence their action succeeded. `NavLink` does update `aria-current="page"` on the focused element, but screen readers do not reliably re-announce an ARIA state change on an element that already holds focus — treat that as an unreliable channel, not a mitigation.
- **Fix**: Add a route-change focus effect targeting the existing `main`:
  ```jsx
  const { pathname } = useLocation();
  const mainRef = useRef(null);
  useEffect(() => {
    // setTimeout(0) so the assignment survives the route's render/unmount cycle
    const t = setTimeout(() => mainRef.current?.focus({ preventScroll: false }), 0);
    return () => clearTimeout(t);
  }, [pathname]);
  ```
  Attach `ref={mainRef}` at `:80`. Add `.portal-main:focus { outline: none; }` — acceptable here because focus arrives programmatically, not via Tab. Pair this with the title fix (M1); together they are sufficient and a live region becomes unnecessary. Do **not** add a live region *instead* of moving focus — it announces the change but leaves the user's reading position stranded in the nav.

**Realist Check** — survives as CRITICAL, but the counter-argument deserves stating. A workaround exists: an experienced screen reader user can press `H` to reach the new `<h1>` (`:10, :26, :34, :44`), or Shift+Tab back to the skip link (`:57`) which correctly targets `#main-content`. That workaround requires the user to *first suspect* a change occurred — and nothing tells them one did. A reviewer rating this MAJOR on workaround-availability is defensible; I hold CRITICAL because the failure is not one missing channel but every redundant channel missing at once, leaving no fallback signal for the one user group that depends on them.

---

## Major Findings

**M1 — `document.title` is static across four distinct routes.**

`spa-route-change-unannounced.md:96` states plainly that this is the only place a title is set, and `:101` sets `<title>Ridgeline Credit Union</title>` once. Four addressable views (`:8, :24, :32, :42`) with four real URLs (`:207` confirms real routes with working browser back/forward) share one non-descriptive title.

- **User group**: screen reader users (many announce document title on navigation), plus anyone using browser history, bookmarks, or tab switching — a history stack of four identical "Ridgeline Credit Union" entries is unusable
- **WCAG**: 2.4.2 Page Titled (A). *Precision note*: on the strict "one document = one page" reading, 2.4.2 arguably doesn't formally reach SPA view changes; the anchor then shifts to 2.4.3 and general orientation. The user harm is identical under either reading, so I would not litigate the citation before fixing it.
- **Confidence**: HIGH
- **Detection**: silent. An axe or Pa11y scan reads the loaded document's title and passes. This is exactly the "tests pass, design fails" class.
- **Fix**: The data already exists — `SECTIONS` carries `label` at `:49-53`. Set `document.title` in the same route-change effect as C1:
  ```jsx
  const section = SECTIONS.find(s => s.path === pathname);
  document.title = `${section?.label ?? 'Page not found'} — Ridgeline Credit Union`;
  ```

**M2 — The not-found state is reached silently on client-side navigation.**

`spa-route-change-unannounced.md:86` routes unmatched paths to `NotFoundView` (`:42-47`). On a hard page load this is fine — focus starts at document top. On a client-side transition to an unmatched route it inherits C1 entirely: no focus move, no announcement, and (per M1) a title that still reads "Ridgeline Credit Union". A screen reader user is left on a page whose error state they have no way to learn about.

- **User group**: screen reader users
- **WCAG**: 4.1.3 Status Messages (AA); 3.3.1-adjacent in spirit
- **Confidence**: MEDIUM — the harm is fully downstream of C1, and the C1+M1 fix resolves it as a side effect. Listed separately because the error case is the one where silence costs the most, and it should appear in the acceptance criteria for the fix.
- **Fix**: Covered by C1+M1. Verify explicitly by navigating client-side to an unmatched path and confirming both the focus move and the "Page not found" title.

**M3 — No viewport meta tag in `index.html`.**

`spa-route-change-unannounced.md:99-102` — the `<head>` contains `charset` and `title` only. Without `<meta name="viewport" content="width=device-width, initial-scale=1">`, mobile browsers render at a ~980px virtual viewport and scale down, so the careful `flex-wrap` reflow work at `:115` and `:124` never engages on a phone. Text renders below legible size and pinch-zoom becomes the only recourse.

- **User group**: low vision users, mobile users generally
- **WCAG**: 1.4.10 Reflow (AA); 1.4.4 Resize Text (AA)
- **Confidence**: MEDIUM. **Stated refutation path**: the developer can refute this in seconds if the real `index.html` includes the tag and the fixture elided it. I am reporting rather than deferring because the check is trivial and the impact if genuine is broad.
- **Fix**: Add the viewport meta to `<head>`. Do not add `user-scalable=no` or `maximum-scale`.

---

## Minor Findings

- **Account balances have no programmatic label.** `spa-route-change-unannounced.md:13-18` renders `<span class="acct-name">` and `<span class="acct-balance">` as siblings in an `<li>`, positioned by `justify-content: space-between` (`:185`). A screen reader reads "Everyday Checking $2,418.06" — the relationship is inferable, but *which* balance (current? available? posted?) is conveyed only by the reader's assumption. In a financial context that ambiguity has consequences. WCAG 1.3.1. Partly a content decision rather than a code defect; flagged as such. Fix: label the value, e.g. `<span class="acct-balance"><span class="visually-hidden">Current balance: </span>$2,418.06</span>`.
- **Scroll position is not reset on route change.** No `<ScrollRestoration>` or scroll effect exists in `:55-90`. React Router does not reset scroll on client navigation. At current content lengths this is invisible; it becomes a real orientation defect for cognitive and screen-magnifier users as any view grows past one screen. Latent, not yet biting. Fix: `window.scrollTo(0, 0)` in the same route effect, ahead of the focus call.

## Enhancements

- **Focus indicator styling is inconsistent.** `:144-149` defines a 3px custom outline for `.nav-link`, `.skip-link`, and `.primary` only. The statement links (`:36-37`) carry no class and fall back to the UA default ring. No rule sets `outline: none` anywhere, so nothing is *broken* — but a magnifier user gets two visually different focus treatments in one interface. Extend the `:focus-visible` rule to `.portal-main a`.
- **Nav targets pass AA but not AAA.** `.nav-link { padding: 6px 2px }` (`:133`) yields roughly 31px tall targets — comfortably over the 24×24 required by 2.5.8 Target Size (Minimum, AA), and the 8px row gap (`:125`) clears the spacing exception. It does not reach the 44×44 of 2.5.5 (Enhanced, AAA). Not a violation; worth 8px of horizontal padding for tremor and touch users.
- **File size is not disclosed on the PDF links** (`:36-37`). The link text correctly announces "(PDF)"; adding size helps users on metered connections decide before committing.

## What's Missing

- Any route-change effect at all — no `useLocation`, `useEffect`, `useRef`, or `.focus()` in `:55-90`
- Any `document.title` write (`:96` confirms the title is set once, statically)
- Any `aria-live` region, `role="status"`, or `role="alert"` in the entire file
- Any scroll reset between routes
- `<meta name="viewport">` in `:99-102`

Verified present and correct, so **not** gaps: `lang="en"` (`:98`); `<main>`, `<header>`, `<nav>` landmarks (`:61, :63, :80`); working skip link whose target is genuinely focusable (`:57` → `:80`); `aria-label` on the nav (`:63`); `replace` on the root redirect so history isn't polluted (`:82`); `role="list"` on every `<ul>` (`:11, :35, :64`), which is justified rather than redundant because `list-style: none` at `:126` and `:178` would otherwise strip list semantics in Safari/VoiceOver.

## Multi-Perspective Notes

**Screen reader user** — Static structure is good: landmarks are correct, each view carries its own `<h1>`, list semantics survive the `list-style: none`, and `aria-current="page"` is exposed. Then navigation happens and the experience collapses. No focus move, no title change, no announcement. The reading cursor stays on the nav link while the entire content region is replaced beneath it. This is the whole review in one sentence.

**Keyboard-only user** — Tab order matches visual order: skip link → three nav links → main content. No traps. Enter activates. The focus ring is a 3px `#0b4fa8` outline with 2px offset (`:144-149`) — roughly 7.8:1 against white, far past the 3:1 required by 2.4.11. The only friction is post-navigation: the next Tab lands on the next *nav link*, not the new content. A sighted user sees what changed and recovers instantly, so the C1 harm barely reaches this group.

**Low vision (200% zoom, high contrast)** — The zoom story is good *if* M3 is wrong: `flex-wrap: wrap` on both the header (`:115`) and the nav (`:124`), `max-width` with auto margins on main (`:164-168`). Windows High Contrast Mode holds up better than expected — the active-state underline at `:139` uses `border-bottom` against an inactive `transparent` border (`:135`), and forced-colors preserves `transparent` while forcing the visible border to system text color, so the active/inactive distinction survives. Focus outlines survive forced-colors too. If M3 is real, none of the reflow work reaches a phone.

*Contrast figures above are computed from the hex values at `:132`, `:139`, and `:146` against an assumed white page background — the CSS shown never sets a body background. These are calculations, not tool measurements; verify with axe's `color-contrast` rule.*

**Cognitive accessibility** — Genuinely strong where it's visible. The not-found copy (`:44-45`) states the problem and the next action in plain language with no error code. The interaction model is uniform across all three sections. No timeouts, no destructive actions needing confirmation, low visual clutter. The persistent orientation cues sighted users rely on — the active underline and the per-view `<h1>` — are all present. The cognitive harm here is real but AT-mediated: it lands on users who need the *non-visual* orientation cues, which is C1 again rather than a separate cognitive defect.

## Verdict Justification

**REVISE**, not REJECT: one CRITICAL and three MAJOR findings, but the foundation is sound and the remediation is small, localized, and mostly satisfied by a single `useEffect`. C1, M1, and M2 all resolve in one 10-line change plus a `ref`, precisely because the hard parts — the focusable `main` target, the landmark structure, the `SECTIONS` label data — are already in place.

To reach ACCEPT: land the route-change effect (focus + title + scroll), confirm the viewport meta, and verify with evidence — not a static scan, which passes today. Specifically: a `keyboard-a11y-tester` driven session or `virtual-screen-reader` assertion capturing what is spoken across a nav activation, plus a `document.title` assertion per route. A screenshot or an axe run is the wrong evidence type for an announcement fix and should be rejected as such.

**Severity recalibrations**: C1 was tested against the workaround argument (heading navigation, skip-link Shift+Tab) and held at CRITICAL — reasoning in the Realist Check above. No downgrades applied. One prediction was withdrawn during investigation: I initially read `tabIndex={-1}` at `:80` as abandoned focus-management scaffolding, then found it is load-bearing for the skip link at `:57`. That correction matters — it changes the fix from "add the missing infrastructure" to "wire up infrastructure that already exists."

**Phase 0 note**: No axe results, Playwright specs, `agent-browser` traces, `keyboard-a11y-tester` artifacts, or `virtual-screen-reader` logs were supplied. Every finding here is design reasoning from source. C1, M2, and M3 would each be materially stronger with measurement, and M3 would be settled outright by one look at the real `index.html`.

## Open Questions (unscored)

1. **Account row reflow at 320px / 400% zoom.** `.account-list li` is `display: flex` with no `flex-wrap` (`:183-184`). My estimate says min-content fits inside 288px with the 16px gap, so no horizontal scroll — but that is arithmetic on assumed font metrics, not a measurement. Confidence LOW; worth one resize check against 1.4.10.
2. **Does any current screen reader re-announce `aria-current="page"` when it changes on the already-focused element?** I assumed not, and built C1 on that assumption. If some AT does, it is a partial signal — still not sufficient, but it would slightly soften the "zero channels" framing. I don't have measured evidence either way.
3. **Is M3 real or a fixture elision?** Stated in the finding; repeating it here because it is the one item where a five-second check by the developer could remove a MAJOR entirely.
4. **Is `<span class="brand">` at `:62` meant to be a home link?** It is currently non-interactive text. If the design intends it as a route to `/accounts`, it needs to be an `<a>`. If it is purely a wordmark, it is correct as-is. Not a finding without knowing the intent.

## Provenance

Files read: exactly one.

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-unannounced.blind.md` (read in full, 208 lines, via Read)

No other file was read. No Grep, Glob, Bash, or git command was run at any point in this session. Nothing under `evals/suites/` was accessed, no `*.metadata.yaml` or `*.rubric.yaml` was accessed, and no search was performed for the fixture name or for related commits. All line citations above index the file as delivered.