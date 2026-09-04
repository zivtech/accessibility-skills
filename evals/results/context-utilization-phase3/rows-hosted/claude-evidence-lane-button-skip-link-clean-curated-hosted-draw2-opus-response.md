# Accessibility Design Review — `MainLayout` (Navigation with Skip Link)

**Citation convention (stated up front so references are unambiguous):** the submission supplies code in two unnamed blocks. I cite them as `MainLayout.jsx:N` (N counted from `const MainLayout = ({ children }) => {` as line 1) and `MainLayout.css:N` (N counted from `.skip-link {` as line 1). No real file paths were supplied with the submission; I have not invented any.

---

**VERDICT: ACCEPT-WITH-RESERVATIONS**

**Overall Assessment**: This is a genuinely well-built layout shell. Native semantics are used throughout, there is zero ARIA misuse, the landmark set is correct, and the skip-link reveal pattern is the correct one — no `display:none`, no clip-and-forget, no removal from the tab order. The single substantive finding is counterintuitive: the one place the author *added* an accessibility affordance (a custom focus ring on the nav links) is the one place the component regresses, because the replacement ring computes to **2.27:1 against the nav bar it sits on** where the user-agent ring it displaced was high-contrast by design. Beyond that there are polish items and, separately, an evidence problem: the pack contains a single axe-core scan at a single viewport, so every keyboard, focus-movement, and screen-reader claim in this review is design reasoning, not measurement.

---

## Phase 0 — Test Evidence Consumed

**What was supplied:** one `a11y-evidence-reader` digest (def_rev 2026-08-26a) citing exactly one artifact — an axe-core 4.13.0 scan of `http://127.0.0.1:8777/button-skip-link-clean.html`, viewport 1280×800, HTTP 200, run 2026-08-26T00:05:58.585Z–00:06:01.857Z.

**Digest tier and the re-fetch rule.** Per the Phase 0 contract, an `a11y-evidence-reader` digest is detector output one tier *below* the artifact it cites, and any finding resting on a digest line must be re-fetched at the cited handle (`[artifact path] → .viewports["1280x800"].violations[0]`) before filing. **I could not re-fetch that handle in this session.** The digest does quote the record verbatim rather than paraphrasing it, which is the best case for a digest, but the rule is about provenance, not phrasing. Consequence, stated plainly: **every claim below that rests on the axe record is labeled `digest-only`.** I have deliberately kept nothing above ENHANCEMENT resting on it.

**What the evidence establishes (digest-only):**
- Exactly one violation at 1280×800: `page-has-heading-one`, impact `moderate`, tags `["cat.semantics","best-practice"]`, `node_count: 1`, `sample_selectors: ["html"]`. No WCAG SC number is present in the record.
- `incomplete: []`, `passes_count: 27`, `inapplicable_count: 62`.
- Absence queries returned empty for: any violation other than `page-has-heading-one`; any `heading-order` violation; any incomplete/manual-review item.

**What the evidence does NOT establish — and this is the load-bearing part.** The digest's own "Not claimed" section is correct and I am adopting it rather than working around it:

1. **Zero admissible evidence exists for any interaction class.** No Playwright transcript, no `keyboard-a11y-tester` trace or batch-crawl findings, no `virtual-screen-reader` assertion. The digest is explicit that this is "no evidence to read, not evidence of no defect" — the two are different claims and this artifact set cannot distinguish them. So: focus reaching `<main>` after skip-link activation, tab order, Escape behavior, and every announcement claim in this review are **design reasoning only**. Nothing here is a measured keyboard or AT fact, and I have not written any finding as though it were.
2. **axe-core is the `machine-detectable` mode only.** It is not valid evidence for keyboard operability, focus order, focus-indicator quality, or announcement behavior. A clean axe run does not clear those classes.
3. **One viewport.** 1280×800 only. Reflow (1.4.10) and text-resize (1.4.4) are unmeasured — see MINOR-4, where this matters more than it usually would.
4. **axe has no focus-indicator contrast rule.** `passes_count: 27` includes `color-contrast`, which evaluates static text against static background. It does not evaluate an `outline` color against the surface it is drawn on. **The clean scan therefore does not contradict MAJOR-1** — the two do not overlap. I want that stated explicitly because "27 passes, one moderate best-practice violation" reads like a clean bill of health and is not one.

**Artifact-to-source binding.** The scanned artifact is `button-skip-link-clean.html` — static HTML — while the submission under review is JSX. Nothing in the pack establishes that the scanned page is the render of *this* component (the filename says "button", the fixture is a navigation layout). Treating the scan as evidence about this source is an inference I am making explicit rather than burying. It does not change any finding, because I have filed nothing above ENHANCEMENT on axe's back.

**This is not a fix/remediation review**, so the Verification evidence contract type-match check does not apply — there is no prior defect and no claimed fix whose evidence type could be mismatched.

---

## Phase 1 — Pre-commitment Predictions

Written before reading the CSS, based on component type (layout shell + skip link + primary nav):

| # | Prediction | Outcome |
|---|---|---|
| 1 | Skip-link target `<main>` lacks `tabindex="-1"`, so activation scrolls but does not move focus in some engines | **HIT** — MINOR-1 |
| 2 | Skip link hidden with `display:none` / `visibility:hidden` / clip-with-no-reveal, removing it from the tab order entirely | **MISS** — the CSS is the correct off-screen-then-reveal pattern. This is the most common way this component fails and it is done right. |
| 3 | Nav landmark label duplicates the role ("Main navigation, navigation") or list semantics compromised | **HIT twice** — MINOR-2 (redundant label), MINOR-3 (`list-style: none`) |
| 4 | No `aria-current` on the active nav item | **HIT** — ENH-1 |
| 5 | Focus indicator removed (`outline: none`) or insufficient | **HIT, but in the variant I did not expect** — not removed; *replaced* with a ring that measures 2.27:1. See below. |
| 6 | Content outside landmarks / no `h1` | **PARTIAL** — no `h1` (axe agrees, digest-only), but the skip link outside landmarks is correctly tolerated and axe's `region` rule did not fire. |

**Where I was surprised.** I expected the skip link to be the broken part — it is the best-implemented part of this file. The failure moved to the place that *looks* like a deliberate accessibility improvement. An author who writes `outline: 3px solid #0066cc` is thinking about keyboard users; the problem is that the UA ring being displaced is engineered to stay visible against arbitrary backgrounds, and a single brand-blue hex is not. That is a net regression dressed as a fix, and it is exactly the class of thing a linter cannot produce: `outline: none` is greppable, `outline: <brand color that happens to be too close to the bar it sits on>` is not.

---

## Phase 2 — Semantic HTML Audit

Verified against source, not assumed:

- **Interactive elements are native.** Every interactive element is an `<a href>` (`MainLayout.jsx:5`, `11–14`). Zero `div`/`span` with `role="button"`. Zero `onClick` on non-interactive elements. The Native-HTML-first constraint is satisfied with nothing to flag.
- **Landmarks present and correctly nested.** `<nav>` (`:9`), `<main>` (`:18`), `<footer>` (`:22`). `<footer>` is a child of `<div class="layout">` — a `div` is *not* sectioning content, so the footer correctly maps to `contentinfo`. `<main>` maps to `main`. Correct as written. (Composition caveat in Open Questions.)
- **List semantics used for list content.** `<ul>`/`<li>` at `:10–15`, not divs. Correct in markup; see MINOR-3 for what the CSS does to it in one engine.
- **No tables.** Layout-table and `role="presentation"` checks are inapplicable.
- **No form inputs.** Label-association checks are inapplicable.
- **Headings.** The layout renders none and owns none — the `h1` belongs to `{children}` (`:19`). See ENH-2.
- **No ARIA masking bad structure.** The only ARIA in the entire file is one `aria-label` on a `<nav>` (`:9`) — enhancing a native landmark, not replacing semantics. That is the acceptable use.

**No MAJOR semantic findings.** Saying so plainly: the semantic structure here is correct, and I am not going to manufacture a violation to make the review look productive.

---

## Phase 3 — ARIA Pattern Compliance Audit

There are **no composite widgets** in this component — no tabs, menu, combobox, disclosure, or dialog. No WAI-ARIA APG widget pattern applies, and roving tabindex, `aria-expanded`, `aria-controls`, and `aria-modal` are all correctly absent rather than missing.

The only ARIA property present is `aria-label="Main navigation"` on `<nav>` (`MainLayout.jsx:9`). It is a valid property on that role, with a valid string value. No invalid ARIA values (`aria-expanded="yes"`, `aria-current="true"`) exist because no such attributes exist.

The relevant APG guidance here is the **Landmark Regions** practice, not a widget pattern: the navigation landmark is correctly used for primary site navigation, and the skip link satisfies the bypass-blocks companion practice. One naming nit under that practice → MINOR-2.

---

## Phase 4 — Focus Management Review

**Caveat carried from Phase 0: none of this is measured.** The pack contains no keyboard trace. The following is source reasoning.

- **Tab order.** DOM order is skip link → 4 nav links → `{children}` → footer, which matches visual top-to-bottom order. No positive `tabindex` anywhere, no `order`/`row-reverse` on the flex containers that would desync visual from DOM order (`.layout` is `flex-direction: column`, `MainLayout.css:19`; `.main-nav ul` is default `row`, `:31`). **2.4.3 Focus Order is satisfied by design.**
- **Skip link is the first focusable element** (`MainLayout.jsx:5`), which is the requirement for it to be useful. Correct.
- **Skip link is reachable.** `.skip-link` uses `position: absolute; top: -40px` (`MainLayout.css:2–3`) with `:focus { top: 0 }` (`:12–14`). Critically, it uses **neither** `display: none` **nor** `visibility: hidden` — both of which remove an element from the tab order and produce the catch-22 where the element can never be focused, so the `:focus` rule can never fire. This component avoids that trap. **2.1.1 satisfied.**
- **Interaction with the flex parent checked.** Because `.skip-link` is absolutely positioned it is removed from `.layout`'s flex flow and does not reserve a 40px-tall row at the top of the page. Correct. And because there is no positioned ancestor, it resolves against the initial containing block, so `top: -40px` places it above the document origin — off-screen without generating a phantom scroll region.
- **No keyboard trap.** No focus event handlers, no `preventDefault`, no focus-cycling code. **2.1.2 satisfied.**
- **No focus restoration surface.** No modal, drawer, popover, or dynamic content. Nothing to restore focus to, so nothing missing.
- **Bypass mechanisms: two.** The skip link *and* the landmark set. **2.4.1 satisfied**, with redundancy.
- **Where focus lands after skip-link activation** → MINOR-1.
- **Focus indicators.** Nav links get a 3px ring (`MainLayout.css:42–45`). The skip link does **not** override its own focus style, so it keeps the UA default ring on a `#0066cc` field — fine. The nav ring is MAJOR-1.
- **2.4.11 Focus Not Obscured.** Nothing is `position: fixed` or `sticky` in this stylesheet — no sticky header, no cookie banner, no fixed footer. The revealed skip link overlays the "Home" link at `top: 0; z-index: 100`, but the skip link *is* the focused element at that moment, and it retracts to `-40px` the instant focus leaves. No obscuring condition. **Satisfied.**
- **Not applicable, verified:** SPA route-change focus (plain `<a href>` full-page navigation, no router), duplicate mobile/desktop DOM (single render tree), React unmount focus timing (no focus calls at all), deferred focus after async CRUD (no CRUD), in-page anchor focus beyond the skip link (none).

---

## Phase 5 — State Communication Audit

This component has **almost no state to communicate**, and I want to be accurate about that rather than inventing gaps:

- **No loading state** → `aria-busy` / `role="status"` correctly absent.
- **No errors, no validation, no form** → `aria-describedby` / `aria-live` correctly absent.
- **No toggles, no disclosure, no selection** → `aria-expanded` / `aria-pressed` / `aria-selected` correctly absent.
- **No disabled or readonly elements** → correctly absent.
- **No visual text symbols used as state indicators** — no `+`/`−`/`×`/`>` characters, no `::before`/`::after` content in the stylesheet, no icon-font classes. The Phase 7 pseudo-element and font-icon traps are genuinely inapplicable here, not merely unchecked.
- **No `aria-live` on a repeating template** — the Broadcast-vs-Association anti-pattern (one `role="alert"` per loop iteration) does not occur; the only loop is four static links with no live regions.

**The one real state gap:** the navigation communicates *no current-page state* at all, visually or programmatically (`MainLayout.jsx:11–14`, and no `:current`/active class in the stylesheet). → ENH-1.

The `©` entity in the footer (`:23`) resolves to the copyright character, which screen readers announce sensibly. Non-issue.

---

## Phase 6 — Multi-Perspective Review

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | MEDIUM | Landmark/list semantics correct in markup but altered by CSS in one engine (MINOR-3); role-redundant landmark name (MINOR-2); **zero AT evidence in the pack** |
| Keyboard-only | MEDIUM | Skip-link *destination* focus behavior is engine-dependent and unverified (MINOR-1); **zero keyboard evidence in the pack** |
| Low vision | **HIGH** | Focus ring computes to 2.27:1 against its own surface (MAJOR-1); reflow unmeasured at any width below 1280 with two independent overflow mechanisms present (MINOR-4) |
| Cognitive | LOW | Static 4-item layout; no forms, timeouts, destructive actions, multi-step flows, or authentication |
| Vestibular & motion | LOW | Zero animation, transition, transform, parallax, or autoplay in the entire stylesheet — including no transition on the skip-link reveal |
| Auditory access | LOW | No `<video>`, `<audio>`, or media player of any kind |
| Environmental contrast | MEDIUM | All *text* contrast passes (computed + corroborated by a clean axe `color-contrast`); *non-text* focus contrast fails; forced-colors mode untested |

**Escalation:** Low vision (HIGH) should go to `/perspective-audit`, and it is the only perspective where I think a deep pass would find more than this review did. Screen reader, Keyboard-only, and Environmental contrast are MEDIUM primarily because the *evidence* is absent, not because the *design* looks wrong — a perspective audit there would mostly re-derive what I have already reasoned. The higher-value action for those three is measurement (see What's Missing), not another reading pass.

### Contrast values computed from the declared hex values

Applying the WCAG relative-luminance formula to the stylesheet's declared, fully opaque colors (no `opacity`, `filter`, `mix-blend-mode`, or gradient anywhere in this file, so the declared values are the rendered values unless overridden elsewhere):

| Pair | Where | Ratio | Requirement | Result |
|---|---|---|---|---|
| `white` on `#333` | nav link text, `MainLayout.css:37` / `:23` | **12.63:1** | 4.5:1 (normal text) | PASS, comfortably |
| `white` on `#0066cc` | skip link when revealed, `:6` / `:5` | **5.57:1** | 4.5:1 | PASS |
| `#666` on `#f5f5f5` | footer text, `:59` / `:56` | **5.27:1** | 4.5:1 | PASS |
| `#0066cc` on `#333` | **focus ring against the nav bar**, `:43` / `:23` | **2.27:1** | 3:1 (non-text) | **FAIL** |

These are computed, not tool-measured — the honest label. The three text rows are corroborated by the axe run's clean `color-contrast` result (digest-only). The fourth row is **not** corroborated or contradicted by anything in the pack, because axe does not evaluate outline colors.

### Per-perspective notes

**Screen reader user.** The experience is largely good: landmark navigation reaches "Main navigation" (nav), main, and contentinfo directly; all four links have real text names, not icon-only or `title`-only names; reading order matches DOM order matches visual order. Two frictions: the landmark announces with the word "navigation" twice (MINOR-2), and in Safari/VoiceOver the `list-style: none` on `MainLayout.css:28` strips the list role, so the user loses "list, 4 items" and per-item position (MINOR-3) — they still reach every link via the landmark and the rotor, so this is friction, not blockage. No redundant or duplicated announcements otherwise. No `aria-hidden` anywhere, so nothing is hidden from AT that shouldn't be.

**Keyboard-only user.** Tab reaches the skip link first, then each nav link, then page content, then footer — logical and complete. Enter activates every control because they are real anchors. No traps, no undiscoverable shortcuts, no arrow-key model to learn. The uncertainty is entirely at the skip-link destination (MINOR-1): after activating it, whether the *next* Tab continues from inside `<main>` or restarts at "Home" is engine-dependent, and a restart silently defeats the whole point of the control. This is precisely the thing that cannot be settled from source and that the pack has no artifact to settle.

**Low vision user (200% zoom, high contrast, magnifier).** This is the weakest perspective and the reason the verdict is not ACCEPT. At high magnification the user tracks focus by the indicator alone, and here the indicator is `#0066cc` drawn *inside* a `#333` bar at 2.27:1 with `#333` on both sides of the ring (`outline-offset: -3px`, `MainLayout.css:44`, puts the ring in the padding area 13px away from the white text, so the text provides no adjacent contrast to help). Under a magnifier showing one nav item at a time, the user may not be able to tell whether the item under the lens is the focused one. Separately, all zoom/reflow behavior is unmeasured (MINOR-4). Touch/pointer target size is fine: `display: block` + `padding: 16px` (`:36`, `:39`) yields roughly 51px tall targets with a 20px gap — comfortably over 24×24 (2.5.8) and over the 44×44 recommendation.

**Cognitive accessibility.** Genuinely clean. Four one-word destinations with unambiguous names, one consistent interaction model (everything is a link, everything works on Enter), a calm uncluttered shell, no timeouts, no destructive actions needing confirmation, no multi-step form that could re-ask for data (3.3.7 inapplicable), no authentication (3.3.8 inapplicable), no personal-data fields needing `autocomplete` (1.3.5 inapplicable). Consistent navigation across pages (3.2.3/3.2.4) is structurally supported *because* this is a shared layout — that is a real cognitive-accessibility benefit of the architecture and worth naming. The one gap is that nothing tells the user which page they are on (ENH-1), which costs orientation for exactly the users who need it most.

**Vestibular & motion.** Nothing to review. No animation, no transition, no parallax, no autoplay. `prefers-reduced-motion` is correctly absent rather than missing — there is no motion to suppress. I am not going to file "add a reduced-motion query" against a stylesheet with zero motion.

**Auditory access.** Nothing to review. No media elements, so 1.2.1, 1.2.2, and 1.4.2 are inapplicable, and there are no sound-only alerts needing visual equivalents.

**Environmental contrast.** Text passes everywhere (table above). Color is never the sole carrier of meaning — there is no status, error, or required-field encoding in this component at all. Forced-colors / Windows High Contrast is untested; the risk is low but non-zero, since `outline` colors are typically replaced by the forced palette (which would incidentally *fix* MAJOR-1 in that mode) while `background: #333` is also replaced — nothing here uses background images or `box-shadow` as the sole carrier of a boundary, which is the usual forced-colors failure, so I rate this low-risk-unverified rather than filing it. No instruction anywhere relies on shape, size, or location (1.3.3 inapplicable).

---

## Phase 7 — Gap Analysis (What Is Absent)

Walked explicitly against the absence checklist, recording the *inapplicable* results too so the reader can see what was checked rather than skipped:

| Gap check | Result |
|---|---|
| Missing focus restoration | N/A — no modal/drawer/popover exists |
| Missing announcements for dynamic content | N/A — no dynamic content |
| Missing error handling for AT | N/A — no forms |
| Missing keyboard shortcut documentation | N/A — no custom shortcuts |
| Missing reduced-motion alternative | N/A — no motion |
| Missing touch target sizing | **Clear** — ~51px tall nav targets, 20px gap |
| Missing landmark structure | **Clear** — nav/main/contentinfo all present |
| Missing skip link | **Clear** — present and correctly implemented |
| Missing `lang` on `<html>` | **Out of this component's scope** — this JSX does not render `<html>`. Also *affirmatively cleared for the scanned page*: axe's `html-has-lang` (WCAG 3.1.1) is in the default rule set and did not appear among the violations (digest-only) |
| Missing `aria-current` | **GAP** → ENH-1 |
| Missing heading structure / `h1` | **GAP, scoped** → ENH-2 |
| Missing list semantics | Markup correct; CSS-induced in one engine → MINOR-3 |
| Missing field associations | N/A — no fields |
| `visibility:hidden` on focus-reveal element | **Clear** — the trap is specifically avoided (`top`-offset reveal, not visibility) |
| Missing `inert` on hidden content | N/A — nothing is hidden from view but present in DOM |
| CSS pseudo-element content exposed to AT | **Clear** — no `::before`/`::after` in the stylesheet |
| Font icon exposed to AT | **Clear** — no icon-font classes; no icons at all |
| Missing reverse skip-link | Not warranted — this shell is short; a consumer rendering long-form content into `{children}` might want one, but that is the consumer's call, not a defect here |
| Missing dragging alternative (2.5.7) | N/A — no drag operations |
| Missing consistent help (3.2.6) | N/A at component scope — no help mechanism exists to be inconsistently placed |
| Caption/transcript/media-keyboard infrastructure | N/A — no media |
| Focus obscured by sticky elements (2.4.11) | **Clear** — nothing sticky or fixed |
| Redundant entry (3.3.7) | N/A — no multi-step flow |

**April 2026 third-party anti-pattern checklist**, run explicitly because most of it is inapplicable and that is worth recording rather than silently skipping: (1) Broadcast-vs-association — N/A, no live regions in a loop; (2) `title`-as-accessible-name — **clear**, zero `title` attributes, all names come from link text; (3) ARIA-label-without-visible-label — **clear**, the `aria-label` is on a landmark (a legitimate use) not standing in for a missing visible control label; (4) else-branch coverage — N/A, no conditional JS; (5) single-selector scope — N/A, no JS selectors; (6) `td`-in-loop row headers — N/A, no tables; (7) `role="presentation"` on data tables — N/A; (8) verbose alt on image links — **clear**, no images; (9) DOM-verification for added ARIA — N/A, no ARIA-adding fix under review.

---

## Findings

### Major Findings (significantly degrades experience)

**MAJOR-1 — Custom nav focus ring computes to 2.27:1 against the bar it is drawn on, below the 3:1 non-text threshold, and it replaced a UA ring engineered to stay visible.**

- **Evidence:** `MainLayout.css:42–45` sets `.main-nav a:focus { outline: 3px solid #0066cc; outline-offset: -3px; }`. The surface is `.main-nav { background: #333 }` (`MainLayout.css:23`). Because the offset is negative, the ring sits inside the link's padding box with `#333` on **both** sides — the white link text (`:37`) is ~13px away and contributes no adjacent contrast. Computed contrast `#0066cc` vs `#333` = **2.27:1** (relative luminances 0.1387 and 0.0331).
- **User group:** Low vision (primary), keyboard-only (secondary — anyone tracking focus visually).
- **Citation:** WCAG 2.2 **1.4.11 Non-text Contrast (AA)** — visual information required to identify component *states*, where the appearance is author-modified rather than UA-determined, requires 3:1 against adjacent colors. WCAG 2.2 **2.4.13 Focus Appearance** requires the same 3:1 change unambiguously but is **Level AAA**, above this project's stated AA target, so I cite it as corroboration of the number, not as the failing criterion. **2.4.7 Focus Visible (AA) passes** — a 3px ring *is* visible; 2.4.7 sets no contrast threshold. I am being precise about this rather than stacking three SC numbers to inflate the finding.
- **Honest note on the mapping:** whether 1.4.11 governs author-styled focus indicators is a genuinely contested reading in the field — the WG's addition of 2.4.13 in WCAG 2.2 exists partly *because* 1.4.11's applicability here was disputed. **This is where my confidence drops, and it drops on the SC label, not on the number.** The 2.27:1 measurement is deterministic; the AA-failure designation is the dominant professional reading but not unanimous.
- **Why this matters, independent of the SC argument:** the design judgment is the finding. Chrome, Firefox, and Safari ship focus rings specifically engineered to remain perceivable against arbitrary backgrounds. This stylesheet discarded that guarantee and substituted a single brand hex chosen without reference to the surface it lands on. For a user at 400% magnification seeing one nav item at a time, a 2.27:1 ring is the difference between knowing and guessing where focus is. The author was trying to help keyboard users; the change made them worse off. That is worth flagging even for a reviewer who rejects the 1.4.11 mapping entirely.
- **Fix (any one):** (a) `outline: 3px solid #fff; outline-offset: -3px;` — white on `#333` is 12.63:1, uses a color already in the palette, and stays on-brand; (b) keep the blue but add a contrasting companion: `outline: 3px solid #0066cc; box-shadow: 0 0 0 6px #fff;`; (c) lighten the blue to at least `#4d94ff` (≈3.1:1 on `#333` — verify after changing, do not assume); (d) simplest and most robust: delete the rule and let the UA ring do its job, which is what it is designed for. Whichever is chosen, re-measure against `#333` rather than against white.
- **Confidence:** HIGH on the computed ratio and on the "replaced a better indicator" reasoning. MEDIUM on the MAJOR severity label — see the Realist Check below, where I record that I considered MINOR and why I did not take it.
- **Could the developer refute this?** Partially. If `#0066cc` is a locked brand token, the *color* is constrained — but the fix space above includes options that keep it. If a global stylesheet overrides `.main-nav a:focus`, the computation changes; nothing in the submitted CSS suggests that, but it is the one refutation I would accept without argument.

```
### A11y Evidence Finding
finding_id: nav-focus-ring-nontext-contrast-below-threshold
fingerprint: a7c4f2e1b93d05fa
source: computed from stylesheet declarations — MainLayout.css:43 (outline color #0066cc) against MainLayout.css:23 (background #333); WCAG relative-luminance formula applied to declared opaque hex values. NOT tool-measured: no contrast tool was run, and axe-core has no focus-indicator contrast rule, so the supplied scan neither confirms nor contradicts this.
wcag_or_apg: WCAG 2.2 1.4.11 Non-text Contrast (AA, primary — mapping contested, see finding note); WCAG 2.2 2.4.13 Focus Appearance (AAA, corroborating, outside AA target)
section_508_fpc_context: not a Section 508 failure — 1.4.11 and 2.4.13 are WCAG 2.1/2.2 additions and the Revised 508 web basis is WCAG 2.0 A/AA; do not label this a 508 defect unless project policy explicitly adopts 2.2
severity: MAJOR
perspective_alarms: low-vision=HIGH, keyboard-only=MEDIUM, environmental-contrast=MEDIUM, screen-reader=LOW, cognitive=LOW, vestibular=LOW, auditory=LOW
evidence: MainLayout.css:42-45 `.main-nav a:focus { outline: 3px solid #0066cc; outline-offset: -3px; }` on MainLayout.css:22-25 `.main-nav { background: #333; }`. Relative luminance #0066cc = 0.1387, #333333 = 0.0331. Contrast = (0.1387+0.05)/(0.0331+0.05) = 2.27:1 vs 3:1 required. Negative outline-offset places the ring wholly within the padding box, adjacent to #333 on both sides.
reproduction_steps: 1. Render MainLayout with the supplied stylesheet. 2. Tab to any nav link. 3. Sample the outline pixel color and the adjacent nav-bar pixel color with a contrast tool (or a browser eyedropper). 4. Compare against the 3:1 non-text threshold. 5. Repeat at 400% browser zoom to observe the practical tracking difficulty.
expected_behavior: The focus indicator is distinguishable from the unfocused nav bar by at least 3:1, so a low-vision keyboard user can locate focus without guessing.
actual_behavior: The indicator differs from its own background by 2.27:1 — roughly three-quarters of the required threshold — and the higher-contrast user-agent indicator it replaced is suppressed.
trend: new
```

### Minor Findings (friction, workaround exists)

**MINOR-1 — Skip-link destination `<main id="main-content">` has no `tabindex="-1"`, so whether focus actually moves is engine-dependent.**
`MainLayout.jsx:18` declares `<main id="main-content">` with no `tabindex`. `<main>` is not natively focusable. Modern engines set the *sequential focus navigation starting point* on fragment navigation, so the next Tab usually continues from inside main and the control works — but this behavior has a long history of engine-specific bugs (WebKit in particular), and the failure mode is silent: the page scrolls, the user believes they skipped the nav, and the next Tab drops them back on "Home". The submission's own stated expected behavior — "Clicking skip link focuses main content" — asserts focus movement, which the markup does not guarantee. Adding `tabindex="-1"` makes it deterministic in every engine and is the long-standing recommended hardening. **WCAG 2.4.1 Bypass Blocks / 2.4.3 Focus Order.** *Fix:* `<main id="main-content" tabindex="-1">`. Optionally pair with `main:focus { outline: none }` to avoid a ring on a region the user did not focus by Tab — acceptable here because the region is not an interactive control. *Confidence:* HIGH that the hardening is warranted; MEDIUM on the practical impact in current browsers. **This is the single item in the review most worth measuring** — one `keyboard-a11y-tester` driven step or Playwright assertion on `document.activeElement` after activation converts it from argument to fact, and the pack contains no such artifact.

**MINOR-2 — `aria-label="Main navigation"` duplicates the role in the announcement.**
`MainLayout.jsx:9`. Screen readers append the landmark role, producing "Main navigation, navigation" / "Main navigation landmark". W3C landmark guidance is explicit that the label should not repeat the role word. With exactly one `<nav>` on the page the label is optional entirely; the landmark is unambiguous without it. No WCAG SC is failed — this is an announcement-quality item under the Phase 6 "redundant announcements" check, and I am rating it accordingly rather than attaching a criterion it does not violate. *Fix:* `aria-label="Main"`, or drop the attribute. *Confidence:* HIGH on the behavior, and deliberately rated MINOR — this is polish, not a barrier.

**MINOR-3 — `list-style: none` strips list semantics in Safari/VoiceOver, contradicting the submission's "list semantics" claim.**
`MainLayout.css:27–33` sets `list-style: none` on `.main-nav ul`. WebKit intentionally removes the list role from lists with no marker, so VoiceOver users do not hear "list, 4 items" or per-item position — they get four unrelated links inside a landmark. The markup at `MainLayout.jsx:10–15` is correct; the CSS is what changes the computed semantics. The submission's feature list explicitly claims "✓ List semantics for navigation", which is true in Chrome and Firefox and not in Safari. **WCAG 1.3.1 Info and Relationships** — with the honest caveat that this is a UA behavior rather than an authoring error, and reasonable practitioners decline to score it as an author failure. Impact is genuinely modest: the nav landmark still groups the links and the VoiceOver rotor still enumerates them, so the user loses count and position, not access. *Fix:* add `role="list"` to the `<ul>` (`MainLayout.jsx:10`) — one attribute, no visual change, no downside. *Confidence:* HIGH on the WebKit behavior, MEDIUM on whether it should be scored against the author.

**MINOR-4 — Reflow at 320 CSS px is unmeasured, and two independent overflow mechanisms are present in the stylesheet. Needs user verification.**
The supplied scan covers exactly one viewport (1280×800), so 1.4.10 Reflow and 1.4.4 Resize Text have **no** evidence. Reading the CSS, two mechanisms put reflow at risk:

1. `.main-nav ul { display: flex; gap: 20px }` (`MainLayout.css:31–32`) with **no `flex-wrap`**, so it defaults to `nowrap`. Flex items do not shrink below `min-content` (`min-width: auto`), so the four items floor at roughly `77 + 77 + 97 + 94 = 345px` plus `3 × 20px` of gap ≈ **405px** — above the 320px reflow width. Estimated from default 16px font metrics, so treat the number as approximate; the *mechanism* is not approximate.
2. `main { padding: 40px; max-width: 1200px; width: 100% }` (`MainLayout.css:47–53`) with **no `box-sizing: border-box` declared anywhere in this stylesheet**. Under the default `content-box`, total width = `width` + 80px of horizontal padding. **Note the arithmetic at the measured viewport:** at exactly 1280px, `width: 100%` resolves to 1280, `max-width` clamps the content box to 1200, and `1200 + 80 = 1280` — it fits *exactly*. At any width below 1280 the clamp stops applying and the element overflows its container by exactly 80px. The single viewport that was scanned is precisely the width at which this cancels out.

Mechanism 2 is very likely refuted by a global `* { box-sizing: border-box }` reset, which most projects carry — but no reset is present in what was submitted, and I am not going to assume one exists. **WCAG 1.4.10 Reflow (AA).** *Concrete verification:* set the browser to 320 CSS px width (or 400% zoom at 1280px) and check for a horizontal scrollbar; separately, in DevTools confirm whether `main`'s computed `box-sizing` is `border-box` or `content-box`. *Fix if confirmed:* `flex-wrap: wrap` on `.main-nav ul`, and either a `border-box` reset or `padding` moved to an inner wrapper. *Confidence:* MEDIUM that a real reflow failure exists; HIGH that it is currently unverified and that the one scanned viewport cannot speak to it.

### Enhancements (best practice not met, no access barrier)

**ENH-1 — No `aria-current` and no visual current-page indicator on the nav.**
`MainLayout.jsx:11–14` render four identical links with no active state in markup or CSS. Screen reader and sighted users alike get no orientation cue about where they are. Per the protocol's own calibration, a lone missing `aria-current` is not a blocker, and this component currently receives no route information, so the fix is an API change (a `currentPath` prop) rather than an attribute edit — which is exactly why it belongs here rather than in Findings. *Fix:* accept the active path and emit `aria-current="page"` (the correct token — not `"true"`) plus a non-color visual treatment such as an underline or left border. **WCAG 4.1.2** for the programmatic half; the visual half is orientation quality, not a criterion.

**ENH-2 — Page has no `h1`; the layout neither supplies one nor requires one of its consumers.**
axe reports `page-has-heading-one`, impact `moderate`, tags `["cat.semantics","best-practice"]`, `node_count: 1`, selector `["html"]` — **digest-only** (see Phase 0; I could not re-fetch the handle). Accurate scoping matters twice here. First, attribution: the `<h1>` belongs inside `{children}` (`MainLayout.jsx:19`), so the scanned page lacking one most likely reflects a harness page with empty children, not a defect in `MainLayout`. Second, weight: `page-has-heading-one` is an axe **best-practice** rule, not a WCAG mapping — no SC number appears in the record, and no WCAG 2.2 criterion requires an `h1`. The digest is right that whether an absent-`h1` counts as a "structural defect" is a mapping judgment; my judgment is **it does not rise above ENHANCEMENT**, and I would treat a review that filed this as a WCAG failure as itself defective. Separately, `heading-order` was queried and returned empty, so no skipped-level condition is evidenced at the scanned viewport. *Fix:* document the contract — every page rendering `MainLayout` must place exactly one `<h1>` inside `main` — and enforce it with a lint rule or a dev-mode assertion, which is the durable form of the fix for a shared layout.

**ENH-3 — Skip link is hidden with a hard-coded `-40px` offset while its height is content-dependent.**
`MainLayout.css:3` sets `top: -40px` for an element whose height is roughly `16px` line-box + `16px` vertical padding ≈ 35px at default text size — hidden with only ~5px to spare. A user with a larger default font size or browser text-only zoom pushes the element past 40px tall, leaving a sliver of the skip link permanently visible above the nav. Cosmetic, not an access barrier: the control still works and still reveals fully on focus. Filed as an enhancement, not padded into a finding. *Fix:* `transform: translateY(-100%)` with `:focus { transform: translateY(0) }`, or `top: auto; bottom: 100%` — both scale with the element's actual height.

---

## What's Missing (gaps, unhandled edge cases, unstated assumptions)

- **The largest gap is evidence, not code.** The pack contains one axe scan. Per the a11y-test evidence contract, axe is the `machine-detectable` mode and is not admissible for keyboard operability, focus order, focus-indicator quality, or announcement behavior. The specific missing artifacts, in the order I would obtain them: (1) a driven keyboard trace proving `document.activeElement` lands inside `<main>` after skip-link activation — this settles MINOR-1, the single most consequential open item; (2) a multi-viewport run at 320px — this settles MINOR-4 and covers the width where the padding arithmetic stops cancelling; (3) a `virtual-screen-reader` component assertion capturing the nav landmark's spoken name and whether list semantics survive — this settles MINOR-2 and MINOR-3 with spoken-phrase evidence instead of argument.
- **`passes_count: 27` is not a conformance signal** and should not be read as one. Twenty-seven axe rules passing at one viewport, with 62 inapplicable, leaves the entire interaction surface untested. The clean-looking scan is the main way this component could be waved through with MAJOR-1 still in it.
- **No forced-colors / Windows High Contrast verification.** Low risk here (no background images, no `box-shadow` carrying a boundary), but unverified. It would also be worth confirming that forced-colors does not *mask* MAJOR-1 during testing and let it ship for everyone else.
- **No guard against the layout being mounted inside sectioning content.** `<footer>` (`MainLayout.jsx:22`) maps to `contentinfo` only because its ancestor is a plain `<div>`. If a consumer ever renders `<MainLayout>` inside an `<article>` or `<section>`, the footer silently degrades to a generic `footer` role and the landmark disappears from the AT landmark list — with no error, no warning, and no visual change. For a component whose entire purpose is to be composed by other code, that unstated assumption deserves a comment in the source at minimum.
- **No documented contract for `{children}`.** The layout depends on its consumers for the `h1` (ENH-2) and assumes they will not introduce a second `<main>` or a competing `contentinfo`. Neither assumption is stated or enforced.
- **`lang` is out of this file's scope** and unowned by anything in the submission. Cleared for the scanned page via axe's silent `html-has-lang` (digest-only), but whoever owns the document shell must keep it.

---

## Phase 8 — Realist Check (Severity Calibration)

Run on the only MAJOR:

**MAJOR-1 (focus ring at 2.27:1):**
1. *Realistic worst case if shipped?* A low-vision keyboard user at high magnification loses track of which nav item has focus and tabs past their target or activates the wrong link. Not access loss — the links still work, the names are still announced, and a screen reader user is unaffected. Recoverable, but recovery costs attention on every single traversal of the nav.
2. *Who is impacted?* Low vision primarily; keyboard-only users who track focus visually, secondarily. Screen reader and cognitive users: unaffected.
3. *Detection speed if it slipped through?* Slow. axe will never report it (no focus-contrast rule), so the clean scan actively conceals it. It surfaces only in manual low-vision testing or a user complaint — days to never.
4. *Proportional, or inflated by review momentum?* **I explicitly considered downgrading to MINOR** on the grounds that a 3px ring is perceptible to many users, that the 1.4.11 mapping is contested, and that 2.4.13 is AAA. I did not downgrade, for three reasons: the shortfall is substantial (2.27 vs 3.0, not a borderline 2.9); the indicator is the *only* focus affordance, since the author suppressed the UA ring that would otherwise cover this; and the detection path is the worst kind — invisible to the automation that was actually run.

**Result: MAJOR retained, no downgrade, therefore no "Mitigated by" statement is owed.** No finding in this review was downgraded, and no finding was upgraded. MINOR-4 was considered at MAJOR and placed at MINOR because its central mechanism (item 2, `box-sizing`) is refutable by a global reset I cannot see; that is a confidence-driven placement, not a mitigation.

I also want to record a calibration decision in the *other* direction: several checklist items that a less careful pass would file — missing `prefers-reduced-motion`, missing `role="presentation"` handling, missing `inert`, missing caption infrastructure — are genuinely inapplicable to a component with no motion, no tables, no hidden content, and no media. They are recorded as N/A in Phase 7 rather than filed as findings. A critic that flags everything is not thorough; it is just noisy.

---

## Phase 9 — Self-Audit

| Finding | Confidence | Developer could refute? | Gap or preference? | Disposition |
|---|---|---|---|---|
| MAJOR-1 focus ring 2.27:1 | HIGH (measurement) / MEDIUM (severity label) | Only via a global override of `.main-nav a:focus`, which is not in evidence | **GAP** | Kept at MAJOR |
| MINOR-1 no `tabindex="-1"` | HIGH (hardening warranted) / MEDIUM (current-browser impact) | Yes — "modern browsers handle this" is a fair partial rebuttal | **GAP** (silent failure mode) | Kept at MINOR |
| MINOR-2 redundant "navigation" | HIGH | No | GAP, low impact | Kept at MINOR — deliberately not inflated |
| MINOR-3 `list-style: none` | HIGH (behavior) / MEDIUM (author-attributable?) | Yes — "that's a WebKit decision, not my bug" is defensible | **GAP** with a one-attribute fix | Kept at MINOR |
| MINOR-4 reflow | MEDIUM | Yes, easily, if a `box-sizing` reset exists | GAP, unverified | Kept at MINOR, marked **Needs user verification**; the `box-sizing` dependency is also listed in Open Questions |
| ENH-1 `aria-current` | HIGH | No | GAP, below finding threshold | ENHANCEMENT |
| ENH-2 no `h1` | HIGH (axe record) / HIGH (scoping) | Yes — "children supply it" is correct, which is why it is scoped as a contract item | GAP at page level, not component level | ENHANCEMENT, digest-only |
| ENH-3 `-40px` offset | MEDIUM | Yes | Borderline **PREFERENCE** | ENHANCEMENT — would have been removed entirely if filed higher |

Nothing was rated LOW confidence, so nothing was moved to Open Questions on confidence grounds; the Open Questions below are context requests and unverifiable-from-source items, which is what that section is for.

**Calibration statement.** The semantic structure of this component is correct and I have said so explicitly in Phases 2, 3, and 5 rather than burying it. The skip-link implementation avoids the two traps that most commonly break this exact pattern (`display:none`/`visibility:hidden` removal from the tab order, and clip-with-no-reveal). Text contrast passes everywhere. Target sizes pass. There is no ARIA misuse anywhere in the file. Those are real results, not padding, and a review that failed to say so would be miscalibrated in the opposite direction.

---

## Phase 10 — Synthesis

Five of six pre-commitment predictions hit, but the distribution is the interesting part. I predicted the skip link would be broken — the highest-frequency failure for this component type — and it is the *strongest* part of the submission. The defect migrated to the nav's focus ring, and it arrived disguised as an improvement: an author writing `outline: 3px solid #0066cc` is thinking about keyboard users, and produced something worse than doing nothing, because the UA default they suppressed is engineered for exactly the contrast problem they then reintroduced.

Two things reinforce that this is the finding worth carrying out of the review. First, it is invisible to the tooling that was actually run: axe has no focus-indicator contrast rule, so the scan that returned one moderate best-practice violation and 27 passes will never surface it, and that clean-looking result is the most likely reason it would ship. Second, the one scanned viewport (1280×800) is precisely the width at which `main`'s `width: 100%` + `max-width: 1200px` + `40px` padding sums to exactly 1280 and the potential overflow cancels. Neither of those is an indictment of axe — both are the predictable shape of a single-tool, single-viewport evidence set, and they are the concrete reason the review's central recommendation is *measure the interaction surface*, not *read the source again*.

What I would tell the developer in one sentence: the structure is right, fix the focus ring, harden the skip-link target, and get a keyboard trace before anyone calls this verified.

---

## Verdict Justification

**ACCEPT-WITH-RESERVATIONS**, on two grounds that are worth separating because they have different remedies.

*The code ground:* one MAJOR (nav focus indicator at 2.27:1) and four MINORs, none of which block access for any user category. There is no CRITICAL finding — nothing here traps a keyboard user, hides functionality from a screen reader, or fails silently in a way that loses data. The architecture is sound: native elements throughout, correct landmarks, a correctly implemented skip link, passing text contrast, adequate target sizes, and no ARIA misuse. This is meaningfully better than most layout shells I would expect to review.

*The evidence ground, which is the reservation I care more about:* the pack cannot support an ACCEPT that rests on measured behavior, because it contains none for the classes that matter here. The digest is explicit and correct that the absence of keyboard artifacts is "no evidence to read, not evidence of no defect." An ACCEPT on this evidence would be a rubber stamp on a single-tool, single-viewport scan — the exact failure mode this review exists to prevent.

**To upgrade to ACCEPT:** (1) fix MAJOR-1 to at least 3:1 against `#333` and re-measure rather than re-estimate; (2) add `tabindex="-1"` to `<main>` and supply a driven keyboard trace showing focus lands inside it after skip-link activation; (3) supply a 320px-viewport run clearing MINOR-4, or confirm `box-sizing: border-box` and `flex-wrap`. MINOR-2, MINOR-3, and the enhancements are one-line changes that need no evidence and can ride along.

**Escalation:** Low vision is at HIGH alarm and should go to `/perspective-audit`. Screen reader, keyboard-only, and environmental contrast sit at MEDIUM because their *evidence* is absent rather than because their *design* looks wrong — for those three, measurement is a better use of effort than another reading pass, and I would rather say that than route work to an audit that will mostly re-derive this document.

---

## Open Questions (unscored)

1. **Does a global `box-sizing: border-box` reset exist outside the submitted stylesheet?** If yes, mechanism 2 of MINOR-4 is refuted outright and the reflow finding narrows to the nav's `flex-wrap`. This is the single fastest check in the review.
2. **Is `#0066cc` a locked brand token?** It constrains the fix space for MAJOR-1 but does not close it — options (b) and (d) in that finding preserve the color or defer to the UA.
3. **Does any stylesheet outside this file override `.main-nav a:focus` or `.skip-link`?** The whole contrast computation assumes the declared values are the rendered values. Nothing in the submission suggests an override, but nothing rules one out either.
4. **What renders into `{children}`, and does it reliably contain exactly one `<h1>`?** Determines whether ENH-2 is a documentation task or a real page-level defect across the site.
5. **Will `MainLayout` ever be mounted inside `<article>` or `<section>`?** If so, the `<footer>` → `contentinfo` mapping silently disappears with no visible symptom. Worth a source comment even if the answer is "no, never."
6. **Does the scanned `button-skip-link-clean.html` actually correspond to this JSX?** Nothing in the pack establishes the binding, and the filename suggests a different fixture. No finding depends on the answer — but if the answer is no, then the component under review has *zero* evidence rather than one scan, which is worth knowing before anyone cites the axe result downstream.
7. **Was there ever a `keyboard-a11y-tester` run for this component that simply was not routed into this pack?** The digest's coverage note lists both keyboard-a11y-tester modes as named-but-unsupplied. If such artifacts exist, MINOR-1 and half the MEDIUM perspective alarms resolve immediately.
