I'll start by reading the fixture file, then run the full review protocol.

---

**VERDICT: ACCEPT**

**Overall Assessment**: This is a correct client-side route-change implementation — the two things SPA route changes almost always get wrong (focus stranded on the activated link, and a title derived from a second URL match that desyncs from the rendered view) are both handled, and handled for the right reasons. I found no CRITICAL or MAJOR defects. What remains is three enhancement-tier robustness gaps and two items I cannot settle from source alone and have kept out of the findings rather than asserting them.

---

**Pre-commitment Predictions**

Before reading the code, for a "client-side route change" component I predicted these seven failure modes:

| # | Predicted failure | Found? |
|---|---|---|
| 1 | Focus never moves on navigation — stays on the clicked link | No — handled (`:45-53`) |
| 2 | `document.title` set from a second `pathname → label` lookup that desyncs from the rendered route | No — explicitly avoided (`:16-19`, `:20-30`) |
| 3 | Focus moves on first render too, skipping the user past nav and skip link | No — guarded (`:46`) |
| 4 | Focus target not programmatically focusable (missing `tabindex="-1"`) → `.focus()` silently no-ops | No — present (`:26`, `:77`) |
| 5 | Focus called before the new route's DOM has committed → focuses the *old* heading | No — `requestAnimationFrame` (`:48`) |
| 6 | Skip link present but target not focusable, or no skip link at all | No — both present and paired (`:57`, `:77`) |
| 7 | `aria-live` region used as the sole announcement mechanism instead of focus | No — focus is the mechanism; correct |

**Two genuine surprises** — things I did not predict and that most implementations miss:
- `preventScroll: true` paired with an explicit `window.scrollTo` (`:49-50`). Without it the browser's scroll-into-view heuristic picks the final position, and heading-with-offset-header layouts land wrong. This is a deliberate separation of two concerns most code conflates.
- The StrictMode-safe guard shape (`:35-39`). Comparing the previous pathname instead of flipping a `hasMounted` boolean is correct and non-obvious: a boolean set to `false` inside the first effect run reads `false` on React's dev-mode repeat mount run, so focus *would* fire on first load. I verified the reasoning holds — a path comparison is idempotent under that repeat.

---

**Critical Findings**: None.

**Major Findings**: None.

**Minor Findings**

1. **Scroll position is discarded on Back/Forward, not just on forward navigation.** `spa-route-change-clean.md:49` — the effect fires on every `pathname` change including `POP`, so returning to `/accounts` via browser Back resets the user to the top rather than to where they were. No SC is violated (2.4.3 concerns focus order, not scroll), and I am explicitly **not** claiming this is a WCAG failure. The accessibility-adjacent cost is real but modest: screen-magnifier and cognitive-load users pay the highest price for re-finding their position. Fix: branch on `useNavigationType() === 'POP'` and skip the `scrollTo` (keep the focus move), or adopt React Router's `ScrollRestoration`.
   - Confidence: HIGH that the behavior occurs; MEDIUM that it is worth changing (it's a defensible product choice).

**Enhancements**

- **No fallback when the queried heading is absent.** `spa-route-change-clean.md:50` — `mainRef.current?.querySelector('h1')?.focus(...)` fails silently. All three current views render a heading via `ViewHeading`, so this is not a live defect. It becomes one the moment someone adds a route that renders its `<h1>` after a data fetch, or code-splits a route with `React.lazy` — in both cases the `requestAnimationFrame` fires against a Suspense fallback, no heading exists, and focus stays on the nav link with no title change and no announcement. The fix is one expression: `(mainRef.current?.querySelector('h1') ?? mainRef.current)?.focus({ preventScroll: true })`. `<main>` is already focusable (`:77`) and already has a focus indicator (`:147`), so the fallback costs nothing and is already styled for.
- **`.skip-link` reveals on `:focus` but is outlined on `:focus-visible`** (`:126`, `:144`). Mouse-clicking the skip link makes it appear with its border but no outline. Cosmetic inconsistency only; the border at `:131` carries sufficient contrast on its own.
- **No `lang` attribute is observable in this file.** Out of the component's scope (it belongs on `<html>` in the shell document), noted so it isn't assumed covered. WCAG 3.1.1.

---

**What's Missing (gap analysis)**

I looked specifically for absences rather than defects:

- **Missing async-route handling** — covered above; the single highest-value one-line change in the file.
- **Missing scroll restoration** — covered above.
- **Not missing, and worth stating explicitly** (these are the gaps this class of component usually has):
  - Live region for route announcements — correctly **absent**. Focus-to-heading is the announcement mechanism; adding an `aria-live` region on top would produce a double announcement. Screen readers do not announce `document.title` changes on SPA navigation, which is exactly why the focus move at `:50` is load-bearing rather than decorative.
  - Focus indicator on programmatic targets — **present** on both (`:144-150`), which is the part almost everyone omits.
  - `aria-current` on the active nav item — **present** via `NavLink`'s default (`:65-69`), and backed by a non-color active treatment (underline + weight, `:138-142`) rather than color alone.
  - Cleanup of the scheduled frame (`:52`) — present, so rapid successive navigations cancel the stale frame and the *next* effect run still passes its guard and focuses the correct heading. I traced this case; it does not strand focus.

---

**Multi-Perspective Notes**

- **Screen reader user**: Activating a section link produces "Accounts, heading level 1" and the reading cursor lands at the top of the new content, with `<main>` as the containing landmark. Tab from there enters the new view (`:94`). The page-title command reports the view that actually rendered, because heading text and title come from the same string (`:22`, `:27`) rather than from two independent lookups. Structure is one `nav` (labeled, `:61`), one `main` (`:77`), one `h1` per view. The `&middot;` separator at `:87` is announced as nothing or "dot" depending on punctuation verbosity — "Everyday Checking $2,418.06" is understandable either way, so I am not raising it.
- **Keyboard-only user**: Tab order is skip link → nav links → main content, matching visual order. No traps. Enter on a nav link moves focus to the new heading; Shift+Tab from there returns to the nav. The skip link works because its target is focusable (`:77`) — an `id`-only target would scroll without moving focus, and this one doesn't have that bug. First page load deliberately leaves focus at the document start (`:46`), which is correct: moving it would take the user past the skip link they haven't seen yet.
- **Low vision (200% zoom, magnifier, forced colors)**: Focus indicator is 3px `#0b4fa8` with 2px offset (`:148-149`), measuring 7.8:1 against white — well over the 3:1 floor for 1.4.11. Active nav link is 7.8:1, inactive 14.7:1 against white. In Windows High Contrast, `outline-color`, `border-color`, and `background-color` are all UA-forced to system colors, so both the skip link and the focus rings survive; no `forced-colors` fallback is needed because nothing here relies on `box-shadow` or images for state. `left: -9999px` (`:123`) is the standard off-screen pattern and keeps the link in the tab order — unlike `visibility: hidden`, which would remove it. The scroll reset noted under Minor Findings is where this perspective is least well served.
- **Cognitive**: Interaction model is consistent across all three routes. The not-found view supplies a recovery instruction rather than a bare error (`:101`). No timeouts, no destructive actions, no motion. The one thing I'd raise with the product owner rather than the developer: the root URL `/` renders "Page not found" by design (`:110`, `:159`), so a user who bookmarks the bare domain hits a dead end. The recovery text mitigates it and I'm not scoring it as an accessibility finding — but it is the file's least defensible product decision, and the stated justification (avoiding a redirect that would read as a navigation) is solvable other ways, e.g. initializing `previousPath` from the post-redirect path.

---

**Verdict Justification**

ACCEPT. No finding reached MAJOR, so the Realist Check produced no recalibrations to report — there was nothing inflated to walk back. I ran the check anyway on the one Minor finding and on the async-fallback enhancement: neither blocks access for any user group, both have obvious workarounds (Back once more; every current route has a heading), and both would surface within minutes of the first route that trips them.

I want to be explicit about what I am *not* claiming, since a clean verdict is easy to hand out and worth nothing if it wasn't earned:

- I am not claiming the code is untestable-and-therefore-fine. I traced the StrictMode double-mount path, the rapid-navigation cancel path, the child-effect-before-parent-effect ordering (`ViewHeading`'s title effect at `:21` runs before `PortalShell`'s focus effect at `:45`, and the `rAF` puts focus after both regardless), and the same-pathname re-click case. All four behave as documented.
- I am not endorsing the fixture's own reasoning at `:172` uncritically. Its claim that "2.4.7 does not reach either" element because neither is keyboard-reachable is *arguable* — the competing reading is that an element receiving focus as the direct result of a keyboard action is within 2.4.7's scope. The dispute doesn't matter here because the file styles both targets anyway, landing on the right outcome under either reading. Litigating the SC boundary would be a stylistic disagreement, not a finding, so I'm not filing one.

For this to have been REVISE, I'd have needed to find the focus move absent or misordered, the title sourced from a second URL match, or the heading non-focusable. None of those are present.

---

**Open Questions (unscored)**

1. **Target size (2.5.8, AA) on the nav links — needs measurement, not inference.** `.nav-link` (`:134-136`) declares only `color`. If the rendered links inherit default `<li>` line-height with no padding, adjacent link centers sit roughly 19 CSS px apart vertically, and the 24×24 spacing exception fails (24px circles centered on each target would intersect). The inline-text exception at 2.5.8 does not obviously rescue a vertical link list — these are not targets "in a sentence." I am **not** filing this as a finding because the CSS block is explicitly partial and I cannot measure rendered geometry from source. Concrete check: render `/accounts`, measure the computed height and vertical center-to-center distance of the two `.nav-link` bounding boxes. If center spacing < 24px and neither box is ≥ 24×24, it's a real 2.5.8 failure with a one-line fix (`padding: 6px 4px; display: block` on `.nav-link`).
2. **Does `:focus-visible` actually match on the programmatically-focused heading across browsers?** The design at `:147` depends on the focus-visible propagation heuristic — an element focused via script matches `:focus-visible` if the previously focused element did. That gives the desired split (keyboard activation of a nav link → outline on the heading; mouse click → no outline), and I believe it holds in current Chrome and Firefox, but I have MEDIUM confidence on Safari and on the skip-link case at `:147`, where focus arrives via native fragment navigation rather than `.focus()`. Verification: keyboard-activate a nav link and then the skip link in Chrome, Firefox, and Safari, and confirm a visible ring on the `<h1>` and on `<main>` respectively. If Safari drops it, the fix is to add plain `:focus` for those two programmatic targets only — they're not mouse-focusable in normal use, so the usual over-showing objection doesn't apply.
3. **Was `/` → not-found a product decision or an artifact of the focus guard?** `:110` and `:159` state it's intentional, and the stated reason is that a root redirect would fire a second render the guard reads as navigation. That's true of the guard as written, but it's fixable (seed `previousPath` after the redirect resolves). Worth confirming with whoever owns the routing table that "bare domain shows Page not found" is the intended experience rather than an accepted cost.

---

## Provenance

**Files read (complete list):**
- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt05-spa-route-change/prompts/spa-route-change-clean.blind.md` — read once, in full (173 lines), via the Read tool.

**No other file was read.** No `evals/suites/` path was accessed. No `*.metadata.yaml` or `*.rubric.yaml` file was read. No Grep, Glob, or Bash/git call was made in this session — the only tool invocation was the single Read above. No repository search was performed for this fixture's name, and no test-evidence artifacts (axe-core, Playwright, keyboard-a11y-tester, virtual-screen-reader) were available or consulted.

**Phase 0 note:** No measured test evidence was attached to this review. Every finding above rests on source reasoning, and the two claims that would be materially stronger with measurement — target size and cross-browser `:focus-visible` behavior — are in Open Questions rather than Findings for exactly that reason. Contrast ratios cited (7.8:1, 14.7:1) are computed from the declared hex values against an assumed white page background, which the supplied CSS does not itself declare.