# Accessibility Design Review — `MainLayout` (skip link + page shell)

**VERDICT: REVISE**

**Overall Assessment**: The semantic architecture of this layout is genuinely correct — native elements throughout, no ARIA masking bad structure, landmarks properly nested, a real focusable skip link with a resolving target, and clear link text. There is nothing here for me to manufacture at the ARIA layer, and I am not going to. The defects are one layer down, in the CSS: the only focus indicator the component defines measures **2.27:1** against its own background (WCAG 1.4.11 requires 3:1), and the navigation is a `display: flex` row with no `flex-wrap`, which almost certainly fails 1.4.10 Reflow at 320px. Both are invisible to the axe-core scan that constitutes the entire evidence pack, and one of them (`main`'s box model) happens to be clean at exactly the one viewport that was scanned.

Separately and importantly: **the evidence pack contains zero evidence about the thing this component exists to do.** The pack is a single axe-core scan. Per the a11y-test evidence contract, axe-core is the `machine-detectable` mode only and is not admissible for keyboard-operability, focus-order, or announcement classes. Whether the skip link actually moves focus — the component's entire reason for existing — is unmeasured. The digest says this itself, correctly and explicitly, and I am carrying that forward rather than laundering it into a pass.

---

## Phase 0 — Evidence Consumed

**What was provided**: one `a11y-evidence-reader` digest (def_rev 2026-08-26a) summarizing one axe-core 4.13.0 scan of `http://127.0.0.1:8777/button-skip-link-clean.html`, viewport 1280×800, http_status 200.

**Digest tier handling** (mandatory): the digest is detector output, one tier BELOW the artifact it cites. The protocol requires re-fetching at the cited handle (`.viewports["1280x800"].violations[0]`) before filing any finding that rests on a digest line. **This review had no access to the artifact path**, so every axe-derived statement below is labeled **digest-only** and no finding is *founded* on one. The two MAJOR findings rest on the component source and CSS supplied directly in the review packet, not on the digest.

**What the axe scan says** (digest-only):
- Exactly one violation: `page-has-heading-one`, impact `moderate`, tags `["cat.semantics","best-practice"]`, `node_count: 1`, selector `html`.
- `incomplete: []`, `passes_count: 27`, `inapplicable_count: 62`.

**Calibration on that violation — three things must be said, and none of them is "axe found a WCAG failure":**
1. The record carries **no WCAG SC number**; its tags are `cat.semantics` and `best-practice`. No WCAG 2.2 success criterion requires an `<h1>`. Reporting this as a WCAG failure would be a citation, not a finding.
2. `page-has-heading-one` (page has no `<h1>` at all) is a *different rule* from `heading-order` (skipped levels). The digest checked for `heading-order` explicitly and it returned empty. The question's "heading-order violation" category is therefore **not** matched by this data point.
3. **Attribution**: `MainLayout` renders `{children}` into `<main>`. The layout does not and cannot own the page `<h1>`. The scanned page is a bare fixture harness with no page content, so an absent `<h1>` there is most likely an artifact of the harness, not a defect in the component. Charging it to `MainLayout` would be exactly the "the checklist said so" failure mode.

**What the axe scan cannot say.** `passes_count: 27` at one viewport is not a conformance statement. axe covers roughly 30–40% of WCAG issue classes and checks **none** of the three things I file below: it does not evaluate `outline` color contrast, it does not evaluate reflow, and it has no rule for an unmarked current page in navigation. So the clean axe result is fully consistent with my findings — there is no contradiction between the evidence and this review to resolve.

**Absence ≠ absence of defect.** The digest states plainly that no keyboard-a11y-tester trace, no batch-crawl findings file, no Playwright transcript, and no virtual-screen-reader assertion were in the set, and that this means sub-question A has *no evidence to read, not evidence of no defect*. That distinction is correct and load-bearing. It is why this review's keyboard and screen-reader conclusions below are stated as design reasoning, explicitly flagged as unmeasured, and why "Verified by measurement" appears nowhere in this document.

**Not a fix/remediation review**, so the evidence-contract type-mismatch check (mismatched evidence offered as proof of a fix) does not apply as a finding here.

---

## Phase 1 — Pre-commitment Predictions

Made before reading the CSS. Component type: page shell / skip-link + primary navigation.

| # | Prediction | Outcome |
|---|---|---|
| 1 | Skip-link target lacks `tabindex="-1"`, so focus never actually lands on `<main>` | **Confirmed**, but smaller than predicted — modern browsers move the sequential-focus starting point. MINOR. |
| 2 | Skip link hidden with a technique that removes it from the tab order (`display:none`, `visibility:hidden`, `clip` on a zero-size box) — would be CRITICAL | **Wrong.** Off-screen positioning is the correct technique; the link stays focusable. Credit where due. |
| 3 | No `aria-current` on the active navigation item | **Confirmed.** MINOR. |
| 4 | Focus indicator either removed (`outline: none`) or present-but-insufficient | **Confirmed, and worse than expected** — present, author-defined, and 2.27:1. MAJOR. |
| 5 | Nav flex row without `flex-wrap` → reflow failure at 320px | **Confirmed** in mechanism; magnitude estimated, not measured. MAJOR (needs verification). |
| 6 | Missing `<h1>` / no heading contract for `main` | Confirmed at the page level, but **not attributable to this component**. ENHANCEMENT. |
| 7 | `<footer>` nested inside sectioning content, so it never maps to `contentinfo` | **Wrong.** `<footer>` is a child of a plain `<div>`, so it maps to `contentinfo` correctly. |

**The surprise**: I predicted the skip link would be the defect, because it is the headline feature and the thing the fixture advertises. It is in fact the best-implemented part of the file. The defects are in the stylesheet — an outline color and a missing `flex-wrap` — the layer nobody reviews and no scanner in this evidence pack inspects.

---

## Phase 2 — Semantic HTML Audit

Verified against source, not assumed.

| Check | Result |
|---|---|
| Native interactive elements vs. div+ARIA | **Correct.** Every interactive element is a real `<a href>`. No `role="button"` on a `div`, no `tabindex` on non-interactive elements, no ARIA replacing native semantics anywhere. The non-negotiable "native HTML first" rule is satisfied. |
| Landmarks present | `<nav>` (JSX:9), `<main>` (JSX:18), `<footer>` (JSX:22). |
| Landmark nesting | `<footer>` is a direct child of `<div class="layout">` — not inside `article`/`section`/`aside`/`nav`/`main` — so it maps to `contentinfo`. Correct. `<main>` is unique on the page. Correct. |
| List semantics for nav | `<ul>` / `<li>` used (JSX:10–15), not divs. Structurally correct — but see MINOR 3 for what CSS does to it in Safari. |
| Form labels | No form controls. N/A. |
| Tables | None. The layout/data-table and `role="presentation"` checks are inapplicable. |
| Heading hierarchy | The component contains **no headings at all**; `{children}` supplies them. Not assessable from this artifact. See ENHANCEMENT 1. |
| Hidden ARIA patching broken HTML | None found. The only ARIA in the file is `aria-label` on `<nav>` — enhancing a native landmark, not replacing structure. Acceptable use. |
| `lang` attribute | Out of scope — this is a component fragment, not a document. Not a finding against this file. |

**No MAJOR semantic finding.** This is a genuine clean result at Phase 2 and I am recording it as one.

---

## Phase 3 — ARIA Pattern Compliance Audit

There are **no composite widgets** in this component — no tabs, menu, combobox, disclosure, or dialog. The APG pattern-completeness question, which is normally where this critic earns its keep, largely does not apply here, and inventing a pattern to grade would be manufacturing.

What is present:
- `<nav aria-label="Main navigation">` (JSX:9) — a landmark label, valid and correctly applied. See ENHANCEMENT 3 on the wording.
- `href="#main-content"` (JSX:5) → `id="main-content"` (JSX:18). **The association resolves.** Verified by reading both lines; the IDREF matches exactly and the target is in the same render tree. (Prior-audit anti-pattern #9 — "any fix adding ARIA/ID associations must be DOM-verified" — is satisfiable here by static reading because both ends are literals, not computed.)
- No `aria-expanded`, `aria-selected`, `aria-pressed`, `aria-controls`, or roving tabindex — and none are required, because there is no widget with state.

**Prior-audit anti-pattern sweep** (April 2026 list, 9 items): #1 broadcast-vs-association — no live regions, N/A. #2 `title` as sole accessible name — **no `title` attributes anywhere; passes**. #3 `aria-label` on a wrapper substituting for a visible label — the `aria-label` is on a landmark, and every link inside has visible text; **passes**. #4 else-branch coverage and #5 single-selector scope — no JavaScript in this component, N/A. #6 `td` row headers, #7 `role="presentation"` on data tables, #8 empty/decorative alt — no tables, no images, N/A.

**No CRITICAL or MAJOR ARIA finding. The ARIA that exists is correct and minimal, which is the right amount.**

---

## Phase 4 — Focus Management Review

- **Tab order**: DOM order is skip link → 4 nav links → children → (footer has no focusables). This matches visual top-to-bottom order. The skip link is the **first focusable element in the document**, which is the requirement people most often get wrong. Correct.
- **Focus traps**: none present, none needed. No modal, drawer, or popover in this component.
- **Focus restoration**: no component in this file opens or closes, so there is nothing to restore. Not a gap.
- **Skip navigation**: present and correctly built — see MINOR 1 for the one thing missing from it.
- **Focus indicators**: present on nav links, and **insufficient** — MAJOR 1.
- **Focus not obscured (2.4.11)**: nothing in the CSS is `position: fixed` or `sticky`; there is no sticky header, footer, or cookie banner to obscure a focused element. Passes by construction.
- **SPA route changes**: this is a React layout with hardcoded `<a href>` navigation, i.e. full page loads. If a router (`react-router` `<Link>`, Next `<Link>`) is later swapped in behind these hrefs, focus will *not* reset on navigation and this layout provides no focus-management hook for that. Flagged in What's Missing, not filed as a finding against current code.
- **Dynamic content, deferred focus after async CRUD, in-page anchor navigation beyond the skip link, duplicate mobile/desktop rendering, framework unmount timing**: none of these mechanisms exist in this file. Not applicable, and I am not going to invent them.

**No CRITICAL focus finding. One MAJOR (indicator contrast) and one MINOR (skip-link target focusability).**

---

## Phase 5 — State Communication Audit

There is almost no state in this component, which is the honest finding.

- No loading states, no error states, no success/confirmation messaging, no disabled or readonly controls, no toggle/expanded/selected states, no live regions. Nothing is communicated visually-only because nothing is communicated at all.
- No text symbols used as state indicators (`+`/`−`/`×`/`>`), so the aria-hidden-symbol check is inapplicable.
- **The one state that exists and is not communicated is location**: which of the four nav links is the current page. Neither programmatically (`aria-current`) nor visually (no active/current style anywhere in the CSS). See MINOR 2.

---

## Findings

### MAJOR 1 — Focus indicator on the primary navigation measures 2.27:1; WCAG requires 3:1

**Evidence** — `MainLayout.css:42–45` (CSS block, relative line numbers; the fixture supplies no file paths):

```css
.main-nav a:focus {
  outline: 3px solid #0066cc;   /* CSS:43 */
  outline-offset: -3px;         /* CSS:44 */
}
```

against `MainLayout.css:22–24`:

```css
.main-nav { background: #333; }
```

`.main-nav a` (CSS:35–40) declares `display:block; color:white; padding:16px` and **no background of its own**, so the anchor is transparent over `#333`. `outline-offset: -3px` draws the 3px ring *inside* the padding box, which means the adjacent color on **both** sides of the ring is `#333`.

**Computation** (sRGB relative luminance, WCAG 2.x formula, from the two declared hex values — no sampling, no estimation, both colors are literals in the stylesheet):

- `#0066cc` → L = 0.2126·0 + 0.7152·0.13292 + 0.0722·0.60387 = **0.13866**
- `#333333` → L = **0.03310**
- Contrast = (0.13866 + 0.05) / (0.03310 + 0.05) = 0.18866 / 0.08310 = **2.27:1**

**Threshold**: 3:1. **Result: FAIL, by a wide margin — 76% of the required ratio.**

**User group impacted**: low-vision keyboard users, users with reduced contrast sensitivity, and anyone operating the site in bright ambient light or on a low-quality display. Also every sighted keyboard user under glare.

**Why this matters**: this is the *only* focus indicator the component defines. The author `outline` declaration replaces the user-agent focus ring, so there is no fallback. A keyboard user tabbing through the primary navigation — on every page of the site, since this is the layout — has one dark-blue ring on dark grey to tell them which of four links they are on. When that ring is not perceivable, the user is navigating blind through the site's main nav and must activate a link to discover where they were.

**Citation** — stated precisely, because the precision matters here:
- **WCAG 2.2 1.4.11 Non-text Contrast (Level AA)** is the AA hook: its Understanding document lists focus indicators as visual information required to identify component state, at 3:1 against adjacent colors. I will note honestly that the normative reach of 1.4.11 to focus rings has been argued in both directions; WCAG 2.2 added 2.4.13 *because* AA coverage was considered ambiguous.
- **WCAG 2.2 2.4.13 Focus Appearance (Level AAA)** fails unambiguously — its 3:1 contrast-change requirement is explicit.
- **WCAG 2.2 2.4.7 Focus Visible (Level AA)** is arguably *satisfied* — an indicator exists. 2.4.7 specifies no ratio. I am not stacking it onto this finding.

Whichever citation a given auditor accepts, the user impact and the fix are identical.

**Fix** — one value:

```css
.main-nav a:focus-visible {
  outline: 3px solid #ffffff;   /* 12.63:1 against #333 */
  outline-offset: -3px;
}
```

`#ffffff` gives 12.63:1. If brand blue must be retained, `#9ecbff` or lighter clears 3:1 against `#333`; verify whatever value is chosen. Consider `:focus-visible` rather than `:focus` so mouse clicks don't paint the ring, and consider a two-tone ring (light outline + dark `box-shadow`) so the indicator survives a future background change.

- **Confidence: HIGH.** The arithmetic is deterministic over two literal hex values in the supplied stylesheet.
- **Refutable by the developer?** NO — not without producing a different stylesheet than the one under review.
- **GAP or PREFERENCE?** GAP.
- **Realist Check**: worst realistic case is significant degradation for a user subset, not complete access loss (links remain operable and labeled) → MAJOR, not CRITICAL. Detection speed argues *against* downgrading: axe-core does not evaluate outline contrast, this component's axe scan is clean, and nothing in the evidence pack would ever surface it. This is a silent failure. **No downgrade. MAJOR stands.**

*Note on the optional `A11y Evidence Finding` block*: I am deliberately omitting it. Its `fingerprint` field requires a computed stable hash and its `source` field a tool invocation. This finding rests on arithmetic over declared CSS values, not on a tool run, and synthesizing a hex fingerprint to make it look tool-produced would be inventing a field to make evidence look more complete than it is. The protocol explicitly forbids that.

---

### MAJOR 2 — Navigation flex row cannot wrap; probable 1.4.10 Reflow failure at 320px (Needs user verification)

**Evidence** — `MainLayout.css:27–33`:

```css
.main-nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;    /* CSS:31 */
  gap: 20px;        /* CSS:32 */
}
```

`flex-wrap` is not declared, so it is `nowrap`. Flex items shrink only to their `min-content` floor (`min-width: auto` on flex items), which for these `<li>` is the widest word plus the anchor's 32px horizontal padding (`.main-nav a { padding: 16px }`, CSS:39).

**Estimated width at the 1.4.10 measurement point (320 CSS px)**: 4 anchors × 32px padding = 128px, plus 3 × 20px gaps = 60px, leaving **132px for 24 characters** of link text ("Home", "About", "Services", "Contact"). At a 16px default font that text needs roughly 190px. Total ≈ **380px against a 320px viewport → ~60px of unavoidable horizontal overflow.** The margin is large enough that it does not hinge on exact font metrics.

**Compounding sub-point — `main`'s box model** (`MainLayout.css:47–53`):

```css
main {
  flex: 1;
  padding: 40px;       /* CSS:49 */
  max-width: 1200px;   /* CSS:50 */
  margin: 0 auto;
  width: 100%;         /* CSS:52 */
}
```

Under `content-box` sizing (the CSS default; **no `box-sizing` reset appears anywhere in the stylesheet provided**), an explicit `width: 100%` overrides flex `stretch`, so main's border box = container width + 80px. That overflows at **every viewport narrower than 1280px** — and at exactly 1280px the `max-width: 1200px` clamp makes it 1200 + 80 = 1280, a perfect fit. **The single viewport that was scanned is the one width at which this defect does not manifest.** That is worth stating plainly: the clean evidence is partly an artifact of where the ruler was placed.

**User group impacted**: low-vision users at 400% zoom (the 1.4.10 measurement condition), screen-magnifier users, and small-screen mobile users — who get bidirectional scrolling to read the page.

**Citation**: WCAG 2.2 **1.4.10 Reflow (Level AA)** — content must be presentable at 320 CSS px width without requiring horizontal scrolling.

**Fix**:
```css
.main-nav ul { flex-wrap: wrap; }
main { box-sizing: border-box; }   /* or a global *, *::before, *::after reset */
```

- **Confidence: MEDIUM.** The mechanism is certain from the CSS; the overflow magnitude is computed from typical font metrics, not measured from a render. The `box-sizing` sub-point dissolves entirely if a global border-box reset exists outside the excerpt provided.
- **Refutable by the developer?** PARTIALLY — "we have a border-box reset" kills the second half. It does not touch the `flex-wrap` half, which is independent of box sizing.
- **GAP or PREFERENCE?** GAP.
- **Needs user verification** — concrete check: load the page, set the viewport to 320 × 256 CSS px (or zoom to 400% at 1280px), and confirm whether a horizontal scrollbar appears on `<html>`. Then run `getComputedStyle(document.querySelector('main')).boxSizing` in DevTools to settle the second half in one line.
- **Realist Check**: content is not lost — horizontal scrolling recovers it — so MAJOR, not CRITICAL. Affects a well-defined and substantial user group at an AA criterion, and the evidence pack (one desktop viewport, a tool with no reflow rule) can never detect it. **MAJOR stands, gated on verification.**

*No `A11y Evidence Finding` block for this one either, and for a sharper reason: it is a predicted failure, not a measured one. Emitting a measured-evidence structure around an estimate would misrepresent its tier.*

---

### MINOR 1 — Skip-link target has no `tabindex="-1"`, so `<main>` never actually receives focus

**Evidence**: `MainLayout.jsx:5` (`<a href="#main-content">`) targets `MainLayout.jsx:18` (`<main id="main-content">`). `<main>` is not natively focusable and carries no `tabindex`.

Activating the link moves the **sequential focus navigation starting point** to `<main>` in current Chrome, Firefox, Edge, and Safari, so the next Tab press does land inside main — the mechanism required by **WCAG 2.4.1 Bypass Blocks** is present and 2.4.1 is met. What does *not* happen is `<main>` receiving DOM focus, which is what reliably relocates a screen reader's virtual cursor. VoiceOver's behavior on non-focusable fragment targets has historically been the weak point, and the evidence pack contains **no screen-reader output at all** to settle it for this component.

**Impact**: a screen reader user may hear the skip link activate, have the page scroll, and find their reading cursor still sitting at the top of the navigation — the exact block they asked to skip.

**Citation**: WCAG 2.2 2.4.1 Bypass Blocks (mechanism satisfied); 2.4.3 Focus Order (where the ambiguity lives).

**Fix**: `<main id="main-content" tabIndex={-1}>`, plus `main:focus { outline: none }` only if the ring is unwanted on programmatic focus. One attribute; removes the ambiguity across every browser/AT pair.

- **Confidence: HIGH** that the attribute is absent; **MEDIUM** on real-world impact, precisely because browser convergence has narrowed it and no AT evidence exists here.
- Rated MINOR rather than MAJOR because current browsers mitigate the keyboard case and the workaround (keep tabbing) exists. I would raise this to MAJOR the moment a VoiceOver transcript showed the cursor failing to move.

---

### MINOR 2 — No current-page indication, programmatic or visual

**Evidence**: `MainLayout.jsx:11–14` render four links with no `aria-current`, and the stylesheet defines no active/current state for `.main-nav a` (nothing between CSS:35 and CSS:45 addresses it).

This is not only an ARIA gap. **Sighted users cannot tell where they are either** — there is no visual current-page treatment anywhere in the CSS. The programmatic slice is `aria-current="page"` on the matching link (the correct token is `"page"`, not `"true"`).

**Impact**: orientation loss in the primary navigation for screen reader users (no announced location) and for cognitive-accessibility users (no "you are here" anchor). Every user group loses something.

**Citation**: WCAG 2.2 4.1.2 Name, Role, Value. (2.4.8 Location is Level AAA and I am not stacking it.)

**Fix**: compute the active route and emit `aria-current="page"` on the matching link, plus a non-color-only visual treatment (weight, underline, or a border — not color alone, per 1.4.1).

- **Confidence: HIGH** on absence; **MEDIUM** on severity. A developer could reasonably reply "the router supplies active state in the real app" — the fixture is static `<a href>` with no router. The finding as written is about the layout as supplied. The protocol's own calibration puts an isolated missing `aria-current` at MINOR, and I agree with it here.

---

### MINOR 3 — `list-style: none` strips list semantics from the nav in Safari/VoiceOver

**Evidence**: `MainLayout.css:28` sets `list-style: none` on `.main-nav ul` (`MainLayout.jsx:10`).

WebKit deliberately removes the implicit `list` role from a `<ul>` whose `list-style` is `none`, on the reasoning that a list that does not *look* like a list should not be *announced* as one. The practical result for a VoiceOver user is that the main navigation loses its "list, 4 items" announcement and its list-navigation shortcuts (`VO-Command-X` and friends stop treating it as a list).

This matters here specifically because the fixture's own feature list asserts "✓ List semantics for navigation." Structurally that is true. In the browser/AT pair a large share of screen-reader users actually run, it is not.

**Impact**: VoiceOver users lose the item count and the list boundaries for the primary nav. They still reach every link via the `navigation` landmark and the rotor, so this is friction, not blockage.

**Citation**: WCAG 2.2 1.3.1 Info and Relationships.

**Fix**: `<ul role="list">` on `MainLayout.jsx:10`. Explicitly re-asserting the role defeats the WebKit heuristic. (Also invisible to axe-core — it reads the DOM, not WebKit's accessibility-tree heuristics — so no scanner in this pack could have surfaced it.)

- **Confidence: MEDIUM-HIGH.** The CSS is certain; the behavior is a documented WebKit decision, and its exact scope varies with Safari version. Impact is correctly scoped to Safari/VoiceOver rather than claimed universally.

---

## Enhancements (best practice not met, no access barrier)

1. **No heading contract for `<main>`.** The component renders `{children}` into `<main>` with no structural guarantee that a page-level `<h1>` exists. The axe `page-has-heading-one` result (digest-only, `best-practice` tag, no WCAG SC) reflects the empty harness page, not a defect in this file — but the fixture's own claim "✓ Proper heading hierarchy (**if headings used in main**)" contains its own caveat, and that caveat is the gap. Consider documenting the contract, or having the layout accept a required `pageTitle` prop that renders the `<h1>`.

2. **Skip-link off-screen technique is fragile under text-only enlargement.** `top: -40px` (CSS:3) against an element roughly 35px tall (≈19px line box + 16px vertical padding) leaves only ~5px of clearance. Browser zoom scales both and is safe; a user stylesheet or Firefox's text-only zoom enlarges the text without scaling the offset, and the link's bottom edge can peek above the nav. A clip-based visually-hidden utility or `transform: translateY(-100%)` is height-independent.

3. **`aria-label="Main navigation"` repeats the landmark role.** Screen readers append the role, producing "Main navigation, navigation." `aria-label="Main"` is the conventional form. With only one `<nav>` on the page the label is arguably unnecessary altogether. This is polish, not a barrier — I am recording it as such rather than inflating it.

4. **Focus styling convention is applied inconsistently.** `MainLayout.css:42` defines an author focus ring for nav links; the skip link (CSS:1–14) has no author focus style and relies on the UA default ring over `#0066cc`. Relying on the UA ring is often the *better* choice, so this is a consistency observation, not a defect — but the two should be a deliberate decision rather than an omission. Verify the default ring is visible on the blue background in the browsers you support.

---

## What's Missing (gaps, unhandled edge cases, unstated assumptions)

- **Any keyboard or screen-reader evidence whatsoever.** The evidence pack is one axe-core scan. The component's headline feature — "clicking the skip link focuses main content," asserted in the fixture's Expected Behavior list — has **zero measured support**. This is the largest gap in the review and it is a gap in the *evidence*, not the code. One `keyboard-a11y-tester` driven session, or one Playwright spec pressing Tab then Enter and asserting `document.activeElement`, closes it.
- **Only one viewport measured.** 1280×800 — and per MAJOR 2, the one width at which `main`'s box model happens not to overflow. No 320px, no 400% zoom.
- **No forced-colors / Windows High Contrast check.** The nav's white-on-`#333` and the skip link's white-on-`#0066cc` both depend on author background colors that forced-colors mode replaces. `outline` generally survives forced-colors, but the skip link's *visibility mechanism* is positional rather than color-based, so it likely survives too. Unverified either way.
- **No SPA focus-management hook.** Hardcoded `<a href>` means full page loads today. Swap in a router `<Link>` and route changes will silently stop resetting focus, with nothing in this layout to catch it. Worth deciding now rather than discovering later.
- **No reverse skip link.** For long `{children}` content, there is no "back to navigation" affordance at the content boundary. Genuinely optional for a shell this small; noted because the protocol asks and because it becomes real if this layout wraps long-form pages.
- **No visible `:focus-visible` distinction.** `:focus` paints the ring on mouse click too. Cosmetic, but it is the reason teams later delete focus rings entirely.

---

## Multi-Perspective Notes

**Screen reader user (NVDA / JAWS / VoiceOver)** — Structure is genuinely good: three correct landmarks, one labeled `navigation`, a `contentinfo` footer, four links with clear text, and no ARIA noise to wade through. Landmark navigation works. Three degradations: the nav is not announced as a list in Safari/VoiceOver (MINOR 3); nothing says which page is current (MINOR 2); and the skip link's effect on the virtual cursor is unverified and possibly nil (MINOR 1). No redundant or repeated announcements — the label wording (ENHANCEMENT 3) is the only verbosity. **None of this is measured — no AT output exists in the evidence pack.**

**Keyboard-only user** — Tab order matches visual order. The skip link is first in the document, which is the requirement most implementations miss, and it is genuinely focusable rather than `display:none`'d out of the tab order. No traps, nothing to Escape from, no undiscoverable shortcuts, no arrow-key widgets. The problem is not *where* focus goes but whether you can *see* it: the only indicator is 2.27:1 (MAJOR 1). And whether Tab-after-skip-link actually lands in main is unmeasured (MINOR 1).

**Low vision user (200%/400% zoom, high contrast, magnifier)** — This is the worst-served perspective and the reason for the verdict. Focus indicator below threshold (MAJOR 1). Navigation that cannot wrap, plus a `main` whose border box exceeds its container below 1280px, giving probable horizontal scrolling at the 1.4.10 measurement point (MAJOR 2). Text contrast, by contrast, is fine everywhere I could compute it: nav links white-on-`#333` = **12.63:1**; skip link white-on-`#0066cc` = **5.57:1**; footer `#666`-on-`#f5f5f5` = **5.27:1**. All clear 4.5:1. Target sizes also pass comfortably: nav links are ~51px tall × 72–92px wide, skip link ~35 × 180px, all well above the 24×24 minimum (2.5.8). Nothing is `position: fixed` or `sticky`, so 2.4.11 Focus Not Obscured passes by construction.

**Cognitive accessibility** — The calmest part of this review. No forms, no errors, no timeouts, no destructive actions, no authentication, no multi-step flow, no redundant entry. Four plainly-named links in a stable shell, consistent by construction across every page that uses the layout — which is 3.2.3/3.2.4 satisfied structurally rather than by policy. The single gap is orientation: no "you are here" (MINOR 2). Nothing to flag under 3.3.x at all, and I am not going to invent something.

**Vestibular & motion** — Nothing. No `transition`, no `animation`, no `transform`, no parallax, no autoplay anywhere in the stylesheet. `.skip-link:focus { top: 0 }` is an instantaneous jump, which is the correct choice — a transition here would itself be a motion concern. No `prefers-reduced-motion` query is needed because there is no motion to reduce; adding one would be cargo cult.

**Auditory access** — No `<video>`, no `<audio>`, no media player, no sound-based alerts. Entirely inapplicable.

**Environmental contrast** — All *text* contrast passes (figures above). The failure is the *non-text* focus indicator at 2.27:1 (MAJOR 1). Color is never the sole carrier of meaning here, because no state is conveyed by color at all — the flip side of having no current-page indicator. Nav links use `text-decoration: none`, which is **exempt** under 1.4.1: the exemption covers navigation, menus, and obviously-interactive UI, and these are block-level items in a `<nav>` landmark on a distinct dark bar. Not a finding. No instruction anywhere relies on shape, size, or location (1.3.3). Forced-colors behavior is unverified.

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | MEDIUM | Correct landmarks/labels, but `list-style:none` semantics loss, no `aria-current`, unverified skip-link cursor movement — and zero AT output in the evidence pack |
| Keyboard-only | MEDIUM | Order and focusability are correct by construction, but no keyboard artifact of any kind exists to confirm the skip link's actual behavior |
| Low vision | **HIGH** | Focus indicator computed at 2.27:1 (<3:1); non-wrapping flex nav plus content-box `main` → probable 1.4.10 failure; only one viewport ever measured |
| Cognitive | LOW | No forms, timeouts, destructive actions, or authentication; stable consistent shell; single orientation gap |
| Vestibular & motion | LOW | No animation, transition, parallax, or autoplay in the component |
| Auditory access | LOW | No media elements of any kind |
| Environmental contrast | MEDIUM | All text contrast passes (5.27–12.63:1); the non-text focus indicator fails; forced-colors unverified |

**Low vision is HIGH → escalate to `/perspective-audit`.** Screen reader, keyboard, and environmental contrast are MEDIUM and warrant deep review, most usefully *after* the evidence gap is closed — a perspective audit on the keyboard and screen-reader lenses with no keyboard or SR artifacts would be reasoning about reasoning.

---

## Phase 8 — Realist Check (severity calibration record)

| Finding | Worst realistic case | Group | Detection if shipped | Outcome |
|---|---|---|---|---|
| MAJOR 1 (2.27:1 focus ring) | Low-vision keyboard user cannot track focus across the site's primary nav on every page; must activate a link to learn where they were. Not access loss — links stay operable and labeled. | Low vision + keyboard | **Never** by automation. axe has no outline-contrast rule; this component's axe scan is clean. Silent failure. | **No downgrade.** Not CRITICAL (no complete access loss); the silent-failure profile blocks any move to MINOR. **MAJOR.** |
| MAJOR 2 (reflow) | Bidirectional scrolling at 400% zoom / 320px; content recoverable by scrolling. | Low vision + mobile | Never by this pack — no reflow rule in axe, and the one scanned viewport is the one that fits. | **No downgrade**, but gated: **MAJOR (Needs user verification).** |
| MINOR 1 (`tabindex="-1"`) | SR user's cursor stays in the nav they tried to skip; keyboard case mitigated by modern browsers. | Screen reader | Days — a user reports "the skip link doesn't do anything." | Held at MINOR because browser convergence narrows the keyboard impact and no AT evidence exists to widen it. Would become MAJOR on a VoiceOver transcript showing cursor failure. |
| MINOR 2 (`aria-current`) | Users cannot tell which page they are on from the nav. | All | Days. | MINOR per protocol calibration; the co-absent *visual* indicator is what keeps it from being pure ARIA nitpick. |
| MINOR 3 (`list-style:none`) | VoiceOver users lose "list, 4 items" and list navigation for the nav; every link still reachable. | Screen reader (Safari/VO) | Never by automation — DOM is correct; the loss is in WebKit's a11y tree. | MINOR. Correctly scoped to one browser/AT pair rather than claimed universally. |

**No recalibrations were required in either direction.** Nothing was inflated by review momentum and nothing was softened. I want to name the temptation explicitly: this fixture arrives with a self-declared "Accessibility Features Implemented" checklist, and two of its checkmarks — "✓ Focus indicators visible on nav links" and "✓ List semantics for navigation" — do not survive contact with the CSS. A self-declared feature list is a claim, not evidence, and treating it as evidence is exactly the rubber-stamp failure mode.

## Phase 9 — Self-Audit

| Finding | Confidence | Developer could refute? | GAP or PREFERENCE? | Disposition |
|---|---|---|---|---|
| MAJOR 1 | HIGH | NO | GAP | Keep as filed |
| MAJOR 2 | MEDIUM | PARTIALLY (box-sizing half only) | GAP | Keep, flagged **Needs user verification** with a concrete two-step check |
| MINOR 1 | HIGH (absence) / MEDIUM (impact) | NO | GAP | Keep at MINOR |
| MINOR 2 | HIGH (absence) / MEDIUM (severity) | YES (router supplies it in a real app) | GAP | Keep at MINOR; refutability stated inline. MINOR-tier, so the Open Questions rule for CRITICAL/MAJOR does not apply |
| MINOR 3 | MEDIUM-HIGH | Partially (Safari version dependent) | GAP | Keep at MINOR, scoped to Safari/VO |
| ENHANCEMENT 3 (label wording) | HIGH | NO | **PREFERENCE** | Correctly held at ENHANCEMENT, not promoted |

Nothing was moved to Open Questions from the MAJOR tier. MAJOR 2 stays in the findings rather than moving to Open Questions because its *mechanism* (`flex-wrap` absent on a `nowrap` row) is certain from the source — only its magnitude is estimated — and the verification step is one browser resize.

---

## Verdict Justification

**REVISE**, not ACCEPT-WITH-RESERVATIONS, and not REJECT.

Not REJECT: nothing here blocks access for any user category. There is no keyboard trap, no unreachable control, no missing accessible name, no ARIA masking broken structure. The architecture is right — and that is not a consolation prize, it is the expensive part to fix and it is already correct. Native elements throughout, correct landmark nesting, a genuinely focusable skip link placed first in the document with a resolving target, real list markup, no invented ARIA. If I had been asked only "is the accessibility *design* sound," the answer is largely yes.

Not ACCEPT-WITH-RESERVATIONS, for two reasons. First, MAJOR 1 is a confirmed WCAG 2.2 AA failure on the focus indicator of the primary navigation of **every page** this layout wraps, and it is a failure no tool in the pipeline will ever report — the axe scan in evidence is clean and always will be. "Ship it and note this" is the wrong disposition for a silent, site-wide AA failure whose fix is one hex value. Second, MAJOR 2 is a probable second AA failure that the evidence pack structurally cannot rule out, because it measured one viewport and that viewport is the exact width at which the defect vanishes.

There is a third reason that is about the evidence rather than the code, and it is the one I would put to the team first. This component exists to do one thing: let a keyboard user skip the navigation. The evidence pack contains **no artifact capable of speaking to whether it does** — no trace, no transcript, no SR output. The digest is admirably explicit that this is *absence of evidence, not evidence of absence*, and I am declining to convert it. A verdict of ACCEPT on this component would be certifying its central claim on the strength of a scanner that cannot see keyboards.

**To upgrade to ACCEPT:**
1. Change `.main-nav a:focus` outline color to clear 3:1 against `#333` (`#ffffff` = 12.63:1). Re-verify the computed ratio.
2. Add `flex-wrap: wrap` to `.main-nav ul`, and confirm `box-sizing` on `main` at 320px width.
3. Add `role="list"` to the nav `<ul>` and `tabIndex={-1}` to `<main>`. Two attributes.
4. Add `aria-current="page"` plus a non-color-only active style to the current nav link.
5. **Produce one keyboard artifact** — a `keyboard-a11y-tester` driven session or a Playwright spec that presses Tab, Enter, Tab and asserts `document.activeElement` is inside `<main>`. This is the item that converts the review's central conclusion from reasoning to fact.

Items 1–4 are roughly six lines of change. Item 5 is the one that matters most and the one nobody ran.

**Escalation**: low vision is at HIGH alarm → `/perspective-audit` on that lens. Screen reader, keyboard, and environmental contrast are at MEDIUM; run those after item 5 exists, so the audit has something measured to work from.

---

## Open Questions (unscored)

1. **Does the skip link actually move the screen reader's virtual cursor?** Unanswerable from this evidence pack — no AT output exists. This is the single highest-value measurement available and it is cheap: one VoiceOver/Safari pass, one NVDA/Firefox pass.
2. **Does a global `box-sizing: border-box` reset exist outside the supplied CSS?** One DevTools line settles half of MAJOR 2. The CSS excerpt begins at `.skip-link` and may not be the whole stylesheet.
3. **`position: absolute` with no positioned ancestor.** `.layout` is `position: static`, so `.skip-link` resolves against the initial containing block — meaning `top: 0` on focus places it at the top of the *document*, not the viewport. Browsers scroll a newly-focused element into view, so this is very likely a non-issue, and skip links are conventionally at scroll-top anyway. Recording it rather than filing it, because I can construct a scenario (Shift+Tab back to the skip link from deep in a long page) where the resulting scroll jump is a surprise, and I cannot rule it out without a render.
4. **Is a router planned behind these `<a href>` links?** If yes, SPA route-change focus management becomes a real gap in this layout today, and the answer changes what item 5 above should test.
5. **Forced-colors / Windows High Contrast behavior**, particularly whether the skip link's off-screen-to-visible mechanism and the nav's focus ring both survive. Positional reveal should survive; the ring should too, since forced-colors preserves `outline`. Unverified.
6. **Was `page-has-heading-one` produced against a bare harness page or against real page content?** I have attributed it to the harness on the reasoning that `MainLayout` renders `{children}` and owns no heading. If the scanned page did include representative content, the finding becomes a real content-side gap and should be re-filed against the pages, not the layout. The digest handle was not re-fetchable in this review, so this attribution is reasoned, not verified — **digest-only**.
