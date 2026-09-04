# Accessibility Design Review — `MainLayout` (Navigation with Skip Link)

**VERDICT: ACCEPT-WITH-RESERVATIONS**

**Overall Assessment**: This is a genuinely well-built layout. Native HTML carries every semantic (`nav`, `main`, `footer`, `ul`/`li`, real `<a>` elements), there is no ARIA masking bad structure, and the skip link uses the correct off-screen-plus-`:focus`-reveal technique rather than the `display:none`/`visibility:hidden` anti-pattern that silently removes skip links from the tab order. The reservations are narrow and concrete: the skip link's target is not focusable, so the component's headline feature is only partially wired; and the nav's flex row has no wrap guard, which is a likely reflow failure at the WCAG 1.4.10 measurement width. Both are one-line fixes. Nothing here blocks access.

A note on evidence discipline up front, because it shaped this review: the attached pack contains 21 axe-core artifacts, **20 of which are for other pages** in the same batch. Their violations do not transfer to this component, and importing them would have produced four fabricated findings.

---

## Phase 0 — Test Evidence Consumed

**Evidence type check.** This is a fresh design pass, not a review of a remediation, so the a11y-test Verification evidence contract's fix-verification requirements do not apply. No evidence-type mismatch to report.

**Target artifact (the only relevant one):**

`evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/004-127-0-0-1-8777-button-skip-link-clean-html.json`

- axe-core 4.13.0, viewport `1280x800`, `http_status: 200`, `status: measured`
- **Violations: 1** — `page-has-heading-one` (impact `moderate`, tags `cat.semantics` + `best-practice`, 1 node, selector `html`)
- **Incomplete: 0**
- `passes_count: 27`, `inapplicable_count: 62`

**The other 20 artifacts are sibling pages and their findings are NOT evidence about this component.** `landmark-one-main`, `region`, `target-size`, `heading-order`, `label`, `color-contrast`, and `bypass`-incomplete all appear in the pack, but on `accordion-no-region-role.html`, `pagination-no-nav-landmark.html`, `file-input-no-labels.html`, and others. None of those URLs is the component under review. I am recording this explicitly because a dump-shaped pack makes cross-contamination the single most likely failure mode of this review.

**The one legitimate use of the siblings — establishing that rules actually ran.** An absent rule in an axe result can mean "passed" or "never executed." The siblings settle it for the rules that matter here:

| Rule | Fires on sibling | Absent on target ⇒ |
|---|---|---|
| `target-size` (wcag22aa, wcag258) | `pagination-no-nav-landmark.html` (11 nodes), `image-carousel-no-region.html` (4 nodes) | Rule active in batch; nav + skip-link targets **pass** |
| `color-contrast` (wcag2aa, wcag143) | `dashboard-heading-inconsistency.html` (4 nodes) | Rule active; text pairs on target **pass** |
| `region` | 10+ siblings | Rule active; **all content is inside landmarks** on target |
| `landmark-one-main` | 12+ siblings | Rule active; `<main>` present and unique |
| `bypass` (wcag2a, wcag241) | `breadcrumb-navigation-no-nav-landmark.html` (incomplete) | Rule active; **bypass mechanism detected** on target |

**What the pack does NOT cover** (every claim below that rests on these is design reasoning, not measured fact, and I label it as such):

- **One viewport only** (`1280x800`). No 320 CSS px / 400% zoom measurement exists, so the reflow finding is unverified.
- **No keyboard trace.** No Playwright spec, no `agent-browser` snapshot/press trace, no `keyboard-a11y-tester` `trace.json`. The one behavior this component exists to provide — that activating the skip link lands the user in `<main>` — is **entirely unmeasured**.
- **No screen-reader evidence.** No `virtual-screen-reader` spoken-phrase log, no `screen-reader-census.json`.
- **No focus-indicator measurement.** axe's `color-contrast` rule evaluates text against its background; it does not evaluate an `outline` color against the adjacent surface. The focus-contrast finding below is therefore invisible to this scan by construction — which is precisely the class of gap this critic exists to catch.
- **Artifact/source mismatch.** The reviewed source is JSX (`MainLayout` with a `{children}` slot); the measured artifact is a static page, `button-skip-link-clean.html`, whose `<main>` contents I cannot see. Measured facts about the HTML page are a proxy for the component, not the component itself.

**Adjudicating the one real violation.** `page-has-heading-one` is tagged `best-practice` with **no `wcag*` tag** — it maps to no WCAG 2.2 success criterion (WCAG contains no requirement that a page have an `h1`). More importantly, `MainLayout` does not render page content; the `h1` would live inside `{children}`. This violation is attributable to the harness page's content, not to the component under review. Filing it against `MainLayout` would be a false positive. It survives only as an ENHANCEMENT about the component's undocumented content contract.

**On the optional `A11y Evidence Finding` blocks:** I am omitting them deliberately. The protocol reserves them for CRITICAL/MAJOR findings *backed by measured evidence*, and requires a stable fingerprint hash. None of my findings is backed by a measurement in this pack, and I will not emit an invented `fingerprint` value to make source-derived reasoning look instrumented.

---

## Phase 1 — Pre-commitment Predictions

Written before reading the source, from the component type ("navigation with skip link" — a layout shell, not a custom widget):

1. **Skip-link target not focusable** — no `tabindex="-1"` on the fragment target. The canonical 80%-complete skip link.
2. **Skip link hidden with `display:none` or `visibility:hidden`**, removing it from the tab order so it can never be revealed (catch-22).
3. **No `aria-current`** on the active nav item.
4. **Focus indicator contrast insufficient** against a dark nav bar.
5. **Nav overflow at narrow widths** — flex row with no wrap handling.
6. **Redundant "navigation" inside the nav's `aria-label`.**

Scored against what I actually found in Phase 10.

---

## Phase 2 — Semantic HTML Audit

Line numbers are relative to the fixture's code blocks (no file paths were supplied); I use `MainLayout.jsx:N` for the JSX block and `layout.css:N` for the CSS block.

| Check | Result |
|---|---|
| Interactive elements native? | **Yes.** Every interactive element is a real `<a href>` (`MainLayout.jsx:5`, `:11–14`). No `div role="button"`, no `span` with `tabindex`. |
| ARIA replacing or enhancing? | **Enhancing only.** The single ARIA attribute in the component is `aria-label` on `<nav>` (`MainLayout.jsx:9`), which names an already-correct landmark. No ARIA is masking anything. |
| Heading hierarchy | Not rendered by this component; supplied via `{children}` (`MainLayout.jsx:19`). Out of the component's control — see the ENHANCEMENT on the content contract. |
| Landmarks | `<nav>` (`:9`), `<main id="main-content">` (`:18`), `<footer>` (`:22`). |
| `<footer>` → `contentinfo`? | **Yes.** Its nearest sectioning ancestor is `<body>` — `div.layout` is neither sectioning content nor a sectioning root — so it maps to `contentinfo`, not a generic footer. Cross-checked: axe's `region` rule does not violate on the target page, which requires the footer subtree to sit inside a landmark. |
| List semantics | **Correct.** `<ul>`/`<li>` at `MainLayout.jsx:10–15`, not divs styled as a list. `list-style: none` (`layout.css:28`) removes the marker but not the `list`/`listitem` roles in any current browser except Safari with `list-style:none`, where the roles are stripped — see Open Questions. |
| Tables | None. Layout-table and `role="presentation"` checks are inapplicable. |
| Form labels | No form controls. Inapplicable. |
| Hidden ARIA patching broken HTML | None found. |

**No MAJOR semantic finding.** This section is clean, and I am saying so rather than manufacturing one. The structure is what the WCAG techniques actually ask for.

---

## Phase 3 — ARIA Pattern Compliance Audit

**No WAI-ARIA APG widget pattern applies to this component, and that is the correct outcome — not a gap.** There is no tablist, menu, disclosure, dialog, combobox, or listbox here. Site navigation and content-bypass are handled by native HTML landmarks and a fragment link; the APG's own guidance for this territory is to use native semantics rather than a widget pattern. Reaching for an APG pattern citation here would be exactly the checklist-driven review this protocol warns against.

The relevant references are therefore:

- **HTML-AAM landmark mappings** — `nav` → `navigation`, `main` → `main`, body-scoped `footer` → `contentinfo`. All three are satisfied.
- **WCAG 2.4.1 Bypass Blocks (Level A)**, technique **G1** — "Adding a link at the top of each page that goes directly to the main content area." The link exists (`MainLayout.jsx:5`), is the first focusable element in the layout, and targets an id that resolves (`main-content`, `MainLayout.jsx:18`). G1's test procedure additionally requires that activating the link *moves the reading position or focus* to the main content — that half is where this implementation is incomplete. See MAJOR-1.

ARIA value validity: `aria-label="Main navigation"` is a valid string value on a `navigation` role. No invalid enumerated values anywhere (no `aria-expanded="yes"`, no `aria-current="true"` misuse — there is no `aria-current` at all, addressed as an ENHANCEMENT).

**Critical calibration point:** axe's `bypass` rule does not violate on the target page. That rule checks for the *presence* of a bypass mechanism — a skip link with a resolvable target, a landmark, or a heading. **It does not verify that focus actually moves.** A skip link that scrolls but never focuses passes `bypass` cleanly. That gap between "axe is green" and "the pattern is complete" is the entire premise of this review, and it is the finding below.

---

## Phase 4 — Focus Management Review

| Check | Finding |
|---|---|
| Tab order logical? | **Yes.** DOM order is skip link → 4 nav links → `{children}` → footer, matching visual top-to-bottom order. No `tabindex` above 0 anywhere (contrast the sibling `app-focus-order-illogical.html`, which axe flags with `tabindex` at serious impact — that rule ran in this batch and is absent here). |
| Skip link reachable? | **Yes — and this is done right.** `.skip-link` uses `position: absolute; top: -40px` (`layout.css:2–3`), which keeps the element rendered, in the accessibility tree, and in the tab order. It is *not* `display:none` or `visibility:hidden`, either of which would make the `:focus` reveal at `layout.css:12–14` unreachable — the catch-22 this protocol lists as a known anti-pattern. Prediction #2 refuted; the developer chose the correct technique. |
| Skip link revealed on focus? | **Yes.** `top: 0` on `:focus` (`layout.css:13`). |
| Skip link focus indicator? | Present via the UA default ring — no `outline: none` reset exists anywhere in the CSS, and `.skip-link:focus` changes only `top`. Relying on the UA default here is preferable to a custom ring, since the default adapts to the `#0066cc` background. No finding. |
| **Does focus move to the target?** | **No.** `<main id="main-content">` (`MainLayout.jsx:18`) has no `tabindex="-1"`. See MAJOR-1. |
| Focus traps | None. No modal, no dialog, no focus-capturing script. WCAG 2.1.2 satisfied trivially. |
| Focus restoration | No dismissible surface exists, so nothing to restore. Not applicable — not a gap. |
| Focus indicators visible | Yes on nav links (`layout.css:42–45`), 3px solid outline. Contrast is the problem, not visibility — see MINOR-1. |
| Focus obscured (2.4.11) | No `position: sticky` or `position: fixed` anywhere in the CSS. Nothing can obscure a focused element. Not a finding. |
| Roving tabindex | Not applicable — no composite widget. Adding arrow-key navigation to a plain nav list would be an anti-pattern, not an improvement. |
| SPA route-change focus | The nav uses plain `href="/"`-style links (`MainLayout.jsx:11–14`) implying full page loads, so browser-native focus reset applies. If a router intercepts these, the analysis changes — see Open Questions. |

---

## Phase 5 — State Communication Audit

This is a static layout. There is no loading state, no error state, no success message, no disabled/readonly control, no selected/expanded/pressed toggle, and no dynamic region. `aria-live`, `aria-busy`, `role="status"`, `aria-describedby`, and `aria-pressed` are all correctly absent — adding any of them here would be noise.

The **one** state this component has is *which page am I on*, and it is communicated neither visually nor programmatically. Because it is absent in both channels, there is no visual-vs-programmatic mismatch — it is a uniform omission, filed as ENHANCEMENT-1 rather than a 4.1.2 state-communication failure.

No visual text symbols are used as state indicators (no `+`/`−`/`×`/`>` characters, no `::before`/`::after` content in the CSS, no icon-font classes). The Phase 7 checks for pseudo-element and font-icon leakage into the accessibility tree find nothing to flag.

---

## Phase 6 — Multi-Perspective Review

**Screen reader user (NVDA, JAWS, VoiceOver).** Landmark structure is clean and complete: three named regions, all page content inside them (confirmed by `region` not violating). Landmark navigation (NVDA `D`, JAWS `R`, VO rotor) gets the user to `main` in one keystroke — which is genuinely the primary bypass route for this population, and it works. The `<ul>` gives "list, 4 items" context. Link text is unambiguous. The gap is the skip link itself: with `<main>` unfocusable, `document.activeElement` stays on `<body>` after activation, so an AT that follows system focus announces nothing. Browse-mode virtual cursors in NVDA/JAWS on Chromium generally track the browser's scroll-and-focus-starting-point behavior, so those pairings largely work; VoiceOver + Safari is the historically unreliable case, and it is the dominant macOS/iOS pairing. **Unmeasured — the pack has no SR census.**

**Keyboard-only user.** Six tab stops, logical order, no traps, no undiscoverable shortcuts, Enter activates every link natively. Modern browsers set the sequential focus navigation starting point on fragment navigation, so for most keyboard-only users the next Tab after the skip link does continue from `<main>` even without `tabindex="-1"` — this is the mitigation that keeps MAJOR-1 out of CRITICAL. **Unmeasured — no keyboard trace in the pack.**

**Low vision user (200% zoom, forced colors, magnifier).** Three items converge here, which is why this is the perspective I would actually escalate. (a) Focus outline `#0066cc` on `#333` measures **2.27:1** — below the 3:1 threshold, and invisible to axe. (b) The nav's `display: flex` with no `flex-wrap` (`layout.css:31`) cannot wrap, so at 320 CSS px the row overflows and forces document-level horizontal scrolling. (c) The `-40px` off-screen offset is a fixed pixel value guarding a box whose height scales with text size — under user text scaling the hidden link can protrude. Forced-colors behavior is untested, though `outline` colors are UA-overridden in that mode, which typically improves rather than degrades this indicator.

**Cognitive accessibility.** Nothing to flag, and I checked rather than assumed. Link text is plain-language and destination-specific ("Skip to main content", not "Skip"). Four one-word nav labels. No timeouts, no destructive actions, no multi-step form, no re-asked information, no authentication, no CAPTCHA, no cluttered surface. Consistency across pages cannot be assessed from a single layout, but the layout is the mechanism that *produces* consistency, which is the right architecture.

**Vestibular & motion.** No `animation`, no `transition`, no `transform`, no parallax, no autoplay anywhere in the CSS. The skip-link reveal is an instantaneous `top` change. `prefers-reduced-motion` is correctly absent — there is no motion to suppress. Flagging its absence here would be a manufactured finding.

**Auditory access.** No `<video>`, no `<audio>`, no media player, no sound-based alerts. Entirely inapplicable.

**Environmental contrast.** Text pairs verified by hand from the declared hex values and cross-checked against axe reporting neither a violation nor an *incomplete* for `color-contrast` on this page (while the rule did fire on siblings, so it ran):

| Pair | Ratio | Requirement | Result |
|---|---|---|---|
| `#fff` on `#333` — nav links (`layout.css:23,37`) | **12.6:1** | 4.5:1 | Pass, wide margin |
| `#fff` on `#0066cc` — skip link (`layout.css:5–6`) | **5.57:1** | 4.5:1 | Pass |
| `#666` on `#f5f5f5` — footer (`layout.css:56,59`) | **5.27:1** | 4.5:1 | Pass |
| `#0066cc` outline on `#333` — focus ring (`layout.css:23,43`) | **2.27:1** | 3:1 | **Below threshold** |

Color is never the sole carrier of meaning: there is no status, error, or required-field indicator in this component at all. WCAG 1.4.1 is satisfied for the nav links despite `text-decoration: none` (`layout.css:38`) — links in a distinct navigation bar are exempt from the underline requirement, which applies to links embedded in body text. That is a deliberate non-finding, not an oversight.

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | MEDIUM | Skip target unfocusable (MAJOR-1); zero SR evidence in pack |
| Keyboard-only | MEDIUM | The component's headline behavior is unmeasured — no keyboard trace |
| Low vision | **HIGH** | Three converging items: 2.27:1 focus outline, unwrappable nav at 320px, fixed-px off-screen offset under text scaling |
| Cognitive | LOW | Static layout, plain-language links, no forms/timeouts/destructive actions |
| Vestibular & motion | LOW | No animation, transition, transform, or autoplay in the CSS |
| Auditory access | LOW | No media elements of any kind |
| Environmental contrast | MEDIUM | Focus indicator below 3:1; forced-colors untested |

**Escalation recommendation — triaged, not blanket.** Send **Low vision** to `/perspective-audit`; its three items are independent and two are unverified. **Environmental contrast** overlaps it entirely (same focus-indicator item) and can ride along rather than open a separate audit. **Screen reader** and **Keyboard-only** are both MEDIUM for a single shared reason — the skip link's focus behavior is untested — and that resolves faster with one `keyboard-a11y-tester` driven session or one Playwright assertion than with a full perspective audit. Opening four audits for what is really two questions would be process, not review.

---

## Phase 7 — Gap Analysis (What's Missing)

Scanning the protocol's absence checklist against this component:

- **Focus movement to the skip target** — absent. MAJOR-1.
- **`flex-wrap` guard on the nav row** — absent. MAJOR-2.
- **`aria-current` on the active nav item** — absent, and the component has no prop from which to derive it. ENHANCEMENT-1.
- **An `h1` contract for `{children}`** — absent. ENHANCEMENT-3.
- **`lang` on `<html>`** — not present, but `MainLayout` does not render the document shell. **Boundary note, not a finding against this component.** Verify it in the page shell that mounts this layout.
- **Skip link outside all landmarks** — true, and correct. axe's `region` rule specifically exempts a leading skip link, and screen reader users reach `main` via landmark navigation rather than via this link. Not a gap.
- **Checks that found nothing** (recorded so the absence is deliberate, not overlooked): missing `inert` on hidden content (no hidden content); CSS `visibility:hidden` on a focus-reveal element (correctly avoided — see Phase 4); pseudo-element `content` exposed to AT (no `::before`/`::after` in the CSS); font-icon elements exposed to AT (no icons); touch targets below 24×24 (nav links ≈ 51px tall with `padding:16px`, skip link ≈ 35px — and axe's `target-size` rule ran in this batch and did not fire here); dragging alternatives (no drag operations); caption/transcript infrastructure (no media); redundant entry (no forms); accessible authentication (no login).

**Anti-pattern checks from the April 2026 third-party audit** — all nine applied, none hit: no `role="alert"`/`aria-live` inside a loop (broadcast-vs-association, #1); no `title` used as an accessible name (#2); no `aria-label` on a wrapper substituting for a visible label (#3); no if/else focus branches to under-cover (#4); no selector-scoped JS hiding elements (#5); no `<td>` carrying row-identifying content (#6); no `role="presentation"` on a data table (#7); no images at all, so no verbose-alt-on-labelled-link issue (#8); #9 (DOM verification for added ARIA) applies prospectively to the `tabindex="-1"` fix recommended below, and I have carried it into that fix.

**Known false positives I checked and did not file:** `list-style: none` stripping list semantics is a Safari-specific behavior, not a code defect, and is a browser-support note rather than a finding (Open Questions). The `page-has-heading-one` violation in the measured artifact is not attributable to this component, as established in Phase 0.

---

## Findings

### Major Findings (significantly degrades experience)

**MAJOR-1 — Skip link scrolls to `<main>` but never focuses it; the target is not focusable.**

`MainLayout.jsx:5` renders `<a href="#main-content">`, and `MainLayout.jsx:18` renders `<main id="main-content">` with **no `tabindex="-1"`**. `<main>` is not natively focusable, so activating the skip link scrolls the document and sets the browser's sequential focus navigation starting point, but does not set `document.activeElement`. Assistive technology that follows system focus is told nothing happened.

- **User group:** Screen reader users primarily; keyboard-only users secondarily.
- **WCAG / technique:** 2.4.1 Bypass Blocks (Level A), sufficient technique **G1** — whose test procedure requires that activating the link move the reading position or focus to the main content, not merely scroll to it. Related: 2.4.3 Focus Order.
- **Why this matters:** This is the one feature the component exists to provide beyond its landmarks, and it is the textbook 80%-complete pattern — the visible half works, the assistive-technology half does not. Realistic worst case: a VoiceOver + Safari user activates "Skip to main content", hears nothing, and their virtual cursor is still on the skip link; the next arrow-right reads "Home, link". The skip silently did nothing. Detection is slow — this fails silently, passes axe's `bypass` rule (presence-only), and surfaces only in AT testing or a user report.
- **Mitigated by:** Current Chromium and Firefox set the sequential focus navigation starting point on fragment navigation, so keyboard-only users on those browsers generally do continue from `<main>` on the next Tab. And this nav has only **four** links, so the concrete cost of the failure in this specific layout is four extra tab stops, not lost access. That mitigation is why this is MAJOR and not CRITICAL.
- **Confidence:** HIGH (the source gap is unambiguous); the *magnitude* per AT/browser pairing is unmeasured.
- **Fix:**
  ```jsx
  <main id="main-content" tabIndex={-1}>
  ```
  Add a matching `main:focus { outline: none; }` only if the transient ring on a whole page region is undesirable — never a blanket `outline: none`. Then verify per anti-pattern #9: inspect the rendered DOM and confirm `document.activeElement` is the `<main>` element after activating the link, rather than trusting a unit test.

---

**MAJOR-2 — Nav flex row cannot wrap; likely horizontal scroll at the WCAG 1.4.10 measurement width. (Needs user verification.)**

`layout.css:27–33` sets `.main-nav ul { display: flex; gap: 20px; }` with **no `flex-wrap`**, so it defaults to `nowrap`. Flex items have `min-width: auto`, meaning they cannot shrink below their min-content width. At 320 CSS px — the width WCAG 1.4.10 Reflow specifies, equivalent to 400% zoom on a 1280px viewport — the four links (`padding: 16px` each side, `layout.css:39`) plus three 20px gaps come to roughly 395px by my estimate at a 16px base font. `.layout` sets no `overflow`, so the overflow propagates to the document and produces a horizontal scrollbar for the whole page.

- **User group:** Low vision users at high zoom; small-viewport users.
- **WCAG:** 1.4.10 Reflow (Level AA) — content must not require scrolling in two dimensions at 320 CSS px.
- **Confidence:** MEDIUM overall, decomposed honestly. That `flex-wrap: nowrap` prevents wrapping and forces overflow at *some* narrow width is **HIGH** confidence — the mechanism is literally in the source. *Where* the overflow begins is MEDIUM, because I am estimating glyph widths rather than measuring them. The developer cannot refute this from context alone; only a measurement settles it.
- **Why it is unverified:** The axe pack contains exactly one viewport, `1280x800`. No narrow-width measurement exists anywhere in the 21 artifacts.
- **Verification step:** Load the page at a 320px CSS viewport (or 1280px at 400% zoom) and check for a horizontal scrollbar on `<body>`. If confirmed, this is a hard AA failure.
- **Fix:** One line — `flex-wrap: wrap;` on `.main-nav ul` (`layout.css:27`). Zero visual change above the wrap point, and it removes the failure mode regardless of where the exact breakpoint falls.

### Minor Findings (friction but workaround exists)

**MINOR-1 — Nav focus indicator measures 2.27:1 against the bar it sits on.**

`layout.css:42–45` sets `outline: 3px solid #0066cc; outline-offset: -3px` on `.main-nav a:focus`. The negative offset draws the ring *inside* the link box, and because the link has no background of its own, `#333` (`layout.css:23`) is the adjacent color on **both** sides of the ring — so the comparison is unambiguous. `#0066cc` against `#333` computes to **2.27:1**, below the 3:1 threshold.

- **User group:** Low vision, keyboard-only.
- **WCAG:** 2.4.7 Focus Visible (Level AA) **is met** — an indicator exists and is clearly visible. The 3:1 requirement lives in **2.4.13 Focus Appearance, which is Level AAA in WCAG 2.2**. Practitioners commonly also anchor focus-indicator contrast in **1.4.11 Non-text Contrast (Level AA)** as a state indicator, but that reading is contested rather than settled, so I am not asserting an AA failure here. I would rather be accurate than alarming.
- **Why MINOR rather than MAJOR:** the ring is 3px (thicker than the UA default) and differs in hue as well as luminance, so most users will locate it. **Mitigated by:** thickness plus hue separation, and the fix is cosmetic-cost-free.
- **Why it escaped the scan:** axe's `color-contrast` rule evaluates text against its background; it never compares an `outline` color to the surrounding surface. This finding is structurally invisible to the tooling that produced the evidence pack.
- **Upgrade condition:** if the project targets AAA, or applies the 1.4.11 focus-indicator interpretation, treat this as a must-fix.
- **Fix:** use a light ring on the dark bar — `outline: 3px solid #fff` gives 12.6:1 — or add a contrasting `outline-offset` companion (`box-shadow: 0 0 0 3px #fff` inside the blue) for the two-color technique that survives any background.

**MINOR-2 — The `-40px` off-screen offset is a fixed pixel guard on a text-sized box.**

`layout.css:3` hides the skip link with `top: -40px`. At a 16px base font the link box is roughly 35px tall (≈19px line box + 8px padding top and bottom, `layout.css:7`), so 40px clears it with about 5px to spare. That margin is consumed by user text scaling: at a 200% text-only zoom the box grows to roughly 53px and about 13px of it — a blue sliver with clipped text — remains visible at the top-left of every page.

- **User group:** Low vision users with enlarged default text.
- **WCAG:** not a clean failure of any single criterion; it is a visual defect in the 1.4.4 Resize Text territory.
- **Confidence:** MEDIUM — the arithmetic depends on font metrics I cannot measure from these artifacts. Verify at 200% text-only zoom (browser font size, not page zoom).
- **Fix:** replace the fixed offset with a size-independent technique — `transform: translateY(-100%)` on the default state, or the standard visually-hidden `clip-path` pattern, both reverted on `:focus`.

### Enhancements (best practice not met, no access barrier)

**ENHANCEMENT-1 — No `aria-current` on the active nav item.** The four links at `MainLayout.jsx:11–14` carry no current-page marker, and the component receives no prop from which to derive one. Screen reader and cognitive users lose the "you are here" cue, which is also absent visually — so there is no visual/programmatic mismatch, just a uniform omission. Per WCAG 4.1.2 the correct value is `aria-current="page"` (never `"true"`). This needs a component API change (accept a `currentPath` prop) as much as a markup change, which is worth deciding now while the layout is young.

**ENHANCEMENT-2 — `aria-label="Main navigation"` reads as "Main navigation, navigation."** `MainLayout.jsx:9`. Screen readers append the role, so the word "navigation" is announced twice. `aria-label="Main"` is the conventional form. This is polish, not a gap — I am recording it because Phase 6's screen-reader lens asks about redundant announcements, not because it costs anyone access. Keeping *a* label is the right call even though there is currently only one nav, since `{children}` may introduce breadcrumb or footer navs later.

**ENHANCEMENT-3 — The `{children}` content contract is undocumented.** The measured artifact violates axe `page-has-heading-one` (best-practice tagged, mapping to no WCAG SC), which belongs to the page's content rather than to `MainLayout`. But the component is the natural place to state the contract: content passed into `<main>` should begin with an `h1`. A prop-types comment or a dev-mode warning makes the requirement visible at the point where it is actually violated.

---

## What's Missing

- **Focus movement on skip-link activation** — the assistive-technology half of the component's headline feature. MAJOR-1.
- **A wrap guard on the nav row** — the layout has no narrow-viewport behavior at all. MAJOR-2.
- **A current-page signal** in both the component's API and its markup. ENHANCEMENT-1.
- **A stated `h1` contract** for injected content. ENHANCEMENT-3.
- **`lang` on the document shell** — outside this component's render boundary; verify in whatever mounts `MainLayout`. Named as a boundary, not charged to the component.
- **Measured evidence for the one behavior that matters.** The pack proves the skip link *exists* (axe `bypass` clean) and proves nothing about whether it *works*. A single Playwright assertion closes this permanently:
  ```js
  await page.keyboard.press('Tab');            // skip link
  await page.keyboard.press('Enter');
  await expect(page.locator('#main-content')).toBeFocused();
  ```
  That test fails today and passes after MAJOR-1's fix — which makes it the right regression guard, not just a check.
- **Forced-colors / Windows High Contrast verification.** Untested. Low expected risk: `outline` colors are UA-overridden in forced-colors mode, so the focus ring should survive or improve.

---

## Multi-Perspective Notes

- **Screen reader user:** Semantic structure is genuinely clear — three landmarks, all content inside them, list semantics intact, unambiguous link text. Landmark navigation reaches `main` in one keystroke, which is the real bypass route for this population and it works. No live regions are needed and none are wrongly present. The gap is the skip link's silence on activation.
- **Keyboard-only user:** Six tab stops in visual order, no traps, no `tabindex` above 0, no undiscoverable shortcuts, Enter activates everything natively. The skip link is correctly reachable rather than hidden out of the tab order. Focus indicators are present everywhere; their contrast is the weak point.
- **Low vision user (200% zoom, high contrast):** The one perspective with real accumulation — a 2.27:1 focus ring, an unwrappable nav that likely forces horizontal scroll at 320px, and an off-screen offset that leaks under text scaling. All three are CSS-only fixes; none is architectural. Text contrast itself is comfortably clean (12.6:1, 5.57:1, 5.27:1).
- **Cognitive accessibility:** Nothing to fix. Plain-language destination-specific link text, four one-word nav labels, no timeouts, no destructive actions, no re-entry, calm uncluttered surface. The layout is itself the mechanism that delivers cross-page consistency (WCAG 3.2.3 / 3.2.4), which is the correct architecture.

---

## Phase 8 — Realist Check (Severity Calibration)

Applied to both MAJOR findings.

**MAJOR-1.** *Worst realistic case:* VoiceOver + Safari user's skip link silently does nothing; they arrow past four nav links. *Group:* screen reader, secondarily keyboard. *Detection:* slow — silent failure, invisible to axe. *Proportional?* Considered CRITICAL and rejected it: no access is lost, four extra tab stops is inconvenience, and modern Chromium/Firefox partly cover keyboard users. **Mitigated by:** sequential-focus-starting-point behavior in current browsers, plus this nav's small size. Considered MINOR and rejected that too — this is the component's defining feature, incomplete in the exact way this critic exists to catch, and downgrading it would be rubber-stamping. **MAJOR confirmed.**

**MAJOR-2.** *Worst realistic case:* a low-vision user at 400% zoom gets a two-dimensionally scrolling page. *Group:* low vision, small viewports. *Detection:* fast once anyone tests a narrow viewport; the current test setup never does. *Proportional?* A 1.4.10 AA failure is squarely MAJOR. The counterweight is that it is estimated rather than measured, which I have handled with a MEDIUM confidence rating and an explicit verification step rather than by softening the severity. The protocol's guidance for suspected-but-unconfirmed issues is to mark them **Needs user verification** with a concrete check and not suppress them silently — applied. **MAJOR retained, verification-gated.**

**One recalibration performed.** MINOR-1 (focus contrast) was drafted at MAJOR and downgraded. **Mitigated by:** the indicator satisfies the criterion that unambiguously applies at AA (2.4.7 Focus Visible), the 3:1 threshold lives in 2.4.13 which is **AAA** in WCAG 2.2, and the ring is 3px with hue separation so it remains locatable. Claiming an AA failure on a contested 1.4.11 reading would have been severity inflation dressed up as rigor. The upgrade condition is stated in the finding.

**No downgrade was applied** to anything involving complete access loss, data loss, or safety risk — nothing in this component reaches that tier.

---

## Phase 9 — Self-Audit

| Finding | Confidence | Developer could immediately refute? | Gap or preference? | Disposition |
|---|---|---|---|---|
| MAJOR-1 skip target unfocusable | HIGH | NO — visible in source | GAP | Keep |
| MAJOR-2 nav cannot wrap | MEDIUM (mechanism HIGH, breakpoint MEDIUM) | NO — needs a measurement, not context | GAP | Keep, verification-gated |
| MINOR-1 focus contrast 2.27:1 | HIGH on the number, MEDIUM on which SC governs | Partially — could argue 2.4.7 is met, which I have already conceded | GAP | Keep at MINOR |
| MINOR-2 off-screen offset | MEDIUM | Partially — "our base font is smaller" | GAP | Keep at MINOR with a verification step |
| ENHANCEMENT-1 `aria-current` | HIGH | NO | GAP (low stakes) | ENHANCEMENT — the severity scale names this exact case as ENHANCEMENT |
| ENHANCEMENT-2 label redundancy | HIGH | NO | **PREFERENCE** | Downgraded to ENHANCEMENT and labeled as polish |
| `page-has-heading-one` | HIGH | YES — not this component's render output | Not a gap in this component | **Not filed as a finding.** Reframed as ENHANCEMENT-3 |

Nothing was moved to Open Questions from the findings list; the Open Questions below are items that never reached finding status because they need developer context to evaluate at all.

**Calibration statement:** the semantics here are correct and I am saying so plainly. Native elements throughout, correct landmark mappings including the `contentinfo` scoping, correct list semantics, a skip link built with the right hiding technique, verified-clean text contrast, correct absence of ARIA that would have been noise. I did not manufacture a `prefers-reduced-motion` finding for a component with no motion, an APG pattern citation for a component with no widget, or a reverse-skip-link recommendation for a four-item nav.

---

## Phase 10 — Synthesis: Predictions vs. Findings

| # | Prediction | Outcome |
|---|---|---|
| 1 | Skip target not focusable | **Confirmed** — MAJOR-1, the review's headline finding |
| 2 | Skip link hidden with `display:none`/`visibility:hidden` | **Refuted** — the developer used off-screen positioning, the correct technique. Prediction was wrong and the code is better than expected |
| 3 | No `aria-current` | **Confirmed** — ENHANCEMENT-1 |
| 4 | Focus indicator contrast insufficient | **Confirmed** — 2.27:1, MINOR-1 |
| 5 | Nav overflow at narrow widths | **Confirmed** (mechanism), unverified (breakpoint) — MAJOR-2 |
| 6 | Redundant "navigation" in `aria-label` | **Confirmed** — ENHANCEMENT-2, polish |

**Where I was surprised, in both directions.** Upward: the semantic layer was cleaner than the component type usually delivers — no div-soup, no ARIA compensating for structure, and the `<footer>` correctly scoped to `contentinfo` rather than buried in a `<section>`, which is a detail most layouts get wrong by accident. The skip link's hiding technique in particular is the thing this component type most often botches, and it is right.

Downward, and unpredicted: **the evidence pack's shape was itself the largest risk in this review.** Twenty of twenty-one artifacts describe other pages, and the single artifact that describes this one contains one violation that is not attributable to this component. A reviewer who skimmed the pack rather than reading the URLs would have filed `landmark-one-main`, `region`, `target-size`, and a `color-contrast` incomplete against a layout that has a `<main>`, has full landmark coverage, has 51px targets, and has 12.6:1 text — four confident, well-cited, entirely false findings. That the pack's only genuine signal turned out to be *negative* space — which rules ran elsewhere and therefore truly passed here — was the useful surprise.

---

## Verdict Justification

**ACCEPT-WITH-RESERVATIONS.**

The accessibility design is sound and, more importantly, was clearly reasoned rather than assembled from a checklist: native semantics throughout, correct landmark mappings, a skip link built with the technique that actually stays in the tab order, verified text contrast, and — the part that carries the most signal — a correct *absence* of ARIA, live regions, roving tabindex, and reduced-motion handling that a less disciplined implementation would have sprinkled in to look thorough.

It is not ACCEPT because MAJOR-1 leaves the component's defining feature half-wired in exactly the way this review exists to detect, and passing it would be rubber-stamping a known gap that the attached scan is structurally incapable of seeing. It is not REVISE because nothing needs redesign: the two MAJOR items are a `tabIndex={-1}` attribute and a `flex-wrap: wrap` declaration, and no finding blocks access for any user category.

**To upgrade to ACCEPT:**
1. Add `tabIndex={-1}` to `<main id="main-content">` and verify in the rendered DOM that `document.activeElement` becomes the `<main>` element after activating the skip link (per anti-pattern #9 — DOM verification, not a unit test).
2. Add `flex-wrap: wrap` to `.main-nav ul`, or measure at 320 CSS px and demonstrate no horizontal scroll.
3. Raise the nav focus indicator to at least 3:1 against `#333` — `#fff` gives 12.6:1.
4. Land the three-line Playwright assertion from *What's Missing* so the skip link's focus behavior stays measured rather than reasoned.

**Escalation:** Low vision is HIGH alarm and should go to `/perspective-audit`; Environmental contrast overlaps it and can ride along. Screen reader and Keyboard-only are MEDIUM for one shared reason — untested skip-link focus behavior — which item 4 above resolves more cheaply than a full audit would.

**Evidence-quality caveat on this entire review:** the attached pack measured one URL at one viewport with one tool. Every keyboard, screen-reader, zoom, and forced-colors claim above is design reasoning explicitly labeled as such, not measured fact. The only measured facts available were which axe rules fired and which did not.

---

## Open Questions (unscored)

1. **Is `MainLayout` ever nested inside a positioned ancestor?** `.skip-link` uses `position: absolute` (`layout.css:2`) but `.layout` sets no `position` (`layout.css:16–20`), so the link resolves against the initial containing block. That is correct for a top-level layout. If any wrapper introduces `position: relative`, the skip link's `top: 0` reveal would land wherever that wrapper sits rather than at the page top. Cheap insurance: add `position: relative` to `.layout` and make the containing block explicit.
2. **Do the nav links go through a client-side router?** They are written as plain `href="/"` paths (`MainLayout.jsx:11–14`), implying full page loads and native focus reset. If a router intercepts them, SPA focus management on route change becomes a live concern for this layout — focus would need to move to the new content — and MAJOR-1's fix becomes load-bearing for a second reason.
3. **Safari list-semantics behavior.** `list-style: none` (`layout.css:28`) causes Safari to drop `list`/`listitem` roles unless `role="list"` is restored on the `<ul>`. This is browser behavior rather than a code defect, and whether to add the belt-and-braces `role="list"` is a team convention call.
4. **Is there a design intent for the current-page state?** ENHANCEMENT-1 is currently absent both visually and programmatically. If a visual active state is planned, add `aria-current="page"` in the same change so the two never diverge — the visual/programmatic mismatch is far harder to fix once shipped than to prevent now.
5. **What renders the document shell?** `lang` on `<html>`, the page `<title>`, and viewport meta all sit outside this component. Worth confirming they are handled somewhere, since a layout component is where teams often assume they live.
