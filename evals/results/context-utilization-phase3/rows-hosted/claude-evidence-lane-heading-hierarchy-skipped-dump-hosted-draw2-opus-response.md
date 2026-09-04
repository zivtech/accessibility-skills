# Accessibility Design Review — `BlogPost` (Blog Post with Skipped Heading Levels)

**Line reference convention.** `BlogPost.jsx:N` counts from `const BlogPost = () => {` as line 1. `blog-post.css:N` counts from `.blog-post {` as line 1. Both blocks are quoted inline for every finding so the reference is verifiable without the mapping.

---

## Phase 0 — Test Evidence Intake

**Fix-verification check (conditional):** This review is a **fresh design pass**, not a review of a remediation. The a11y-test Verification evidence contract check for mismatched evidence type therefore does not fire. No "fixed" claim is being asserted and no before/after pair was supplied, so there is nothing to type-check.

**Evidence supplied, by tier:**

| Artifact | Tier | Scope |
|---|---|---|
| `axe-batch-2026-08-25/013-...-heading-hierarchy-skipped-html.json` (axe-core 4.13.0, 1280x800, `status: measured`, HTTP 200) | Hard evidence | **On target** |
| `heading-hierarchy-skipped-kat-census/sr-census.json` (keyboard-a11y-tester reading-order census, `truncated: false`) | Hard evidence (structure); one tier below a real AT session for announcement *phrasing* | **On target** |
| 17 further axe scans (`000`–`012`, `014`–`017`) | Hard evidence — **about other pages** | **Off target** |

**Evidence-to-source correspondence — verified, not assumed.** The census selectors describe a React render into `#root`: `#root > article > h1`, `h3:nth-of-type(1)`–`(4)`, `h2:nth-of-type(1)`–`(2)`, `p:nth-of-type(1)`–`(4)`, `ul > li:nth-of-type(1)`–`(3)`. That is exactly one h1, four h3s, two h2s, four paragraphs and a three-item list — an exact structural match to `BlogPost.jsx:3–29`. Heading text in the census matches the JSX character-for-character. The scanned page is this component.

**Pack hygiene — stated because the pack invites the error.** 19 artifacts were supplied; **2 are about this component and 17 are about unrelated pages** (accordion, dropdowns, carousel, forms, data table, infinite scroll, breadcrumb, combobox, file input, dashboard). Nothing in those 17 files is evidence about `BlogPost`. Specifically: the `target-size` violations in `014-image-carousel`, the `color-contrast` violations in `007-dashboard-heading-inconsistency`, the `label` critical in `010-file-input-no-labels`, and the `tabindex` serious in `001-app-focus-order-illogical` are **not findings against this component** and are not reported as such below. The one legitimate cross-artifact use is as a control, described in the `landmark-one-main` / `region` analysis in **What's Missing**.

**Instrument note — census `role` field is unreliable on text nodes.** Census entries 6, 10, 15, 18, 21, 27 and 31 carry `"role"` values that are the element's *text content*, not an ARIA role (e.g. entry 6: `"role": "Web accessibility ensures that everyone"`, truncated relative to its own `spoken_phrase`), with `"tag": null` and `"selector": null`. These are text-node rows and a serializer artifact of the census, not page defects and not real roles. No finding is derived from a `role` value on a row where `tag` and `selector` are null, and none of those rows is a re-fetchable handle.

**Negative results are informative here.** For the target page axe reports `"incomplete": []` — no unresolved contrast, no unresolved ARIA. Sibling pages in the same batch *do* produce `incomplete` entries (`000` accordion, `016`/`017` dropdowns). So axe resolved this page's computed backgrounds and ARIA cleanly and still found nothing; the empty array is a measured negative, not a gap in coverage. Likewise `declared_live_regions: []`, `declared_broken_aria_refs: []`, `declared_alternate_reading_order: []`, and `truncated: false` — the census is **complete**, so claims of the form "there are no interactive elements" rest on a complete walk, not on a truncated sample.

**Measurement I do not have:** no keyboard trace, no focus-appearance measurement, no forced-colors render, no 200%-zoom capture, no real NVDA/JAWS/VoiceOver session. Where a claim below rests on reading rather than measurement, it says so.

---

## Phase 1 — Pre-commitment Predictions

Component type: static long-form content, no interactivity. Predicted before reading the source:

1. **Heading levels skip** (the fixture name says so; predicted h1→h3). — **Confirmed, and worse than predicted.** There is a second heading defect the name doesn't describe and axe cannot detect.
2. **No landmark structure** — content in a bare `<article>` with no `<main>`. — **Confirmed in the DOM, but not attributable to this component.** See What's Missing.
3. **Heading levels chosen for visual weight rather than structure**, with CSS confirming the intent. — **Confirmed.** `blog-post.css:22–27` gives h3 18px/#666 against h2 24px/#0066cc; the visual hierarchy encodes the same broken outline the markup does. Both are wrong in the same direction, which changes the fix.
4. **Contrast failure on the muted `#666` heading color.** — **Wrong. Refuted by computation and by measurement.** #666 on white is 5.74:1 at 18px normal text; axe found no contrast violation and no contrast `incomplete`. I predicted a violation and there isn't one; reported as clean below.
5. **An empty or orphaned section.** — Not predicted specifically, **found**: `<h3>Getting Started</h3>` labels nothing.

Prediction 4 is the one I got wrong, and it is worth naming: the "grey subhead" pattern reads as a contrast problem and, measured, is not one.

---

## Phase 2 — Semantic HTML Audit

Everything in this component uses native HTML. There is **no ARIA anywhere in the source** — no `role`, no `aria-*`, no `tabindex`. That is the correct outcome for this content type and it satisfies the non-negotiable native-HTML-first rule outright. There is no ARIA masking bad structure because there is no ARIA and the structure is elementwise sound:

- `<article>` (`BlogPost.jsx:3`) wraps the post — correct element, census entry 2 confirms `role: article` computed.
- Headings are real `<h1>`/`<h2>`/`<h3>` elements, not styled divs.
- List content is a real `<ul>`/`<li>` (`BlogPost.jsx:16–20`). Census entries 13–23 confirm the computed list: `listitem, level 1, position 1, set size 3` through `position 3, set size 3`, with `end of list`. Set size and positions are correct — a div-based fake list would produce none of this.
- Prose is in `<p>` elements; census entries 5/7, 9/11, 26/28, 30/32 confirm paired `paragraph` / `end of paragraph` boundaries.
- No tables, no forms, no inputs, no images. Layout-table, `role="presentation"`, `<th scope>` and `<label for>` checks are all inapplicable — stated rather than silently skipped.

**The one semantic defect is the heading outline**, reported as MAJOR-1. Note precisely what kind of defect it is: the *elements* are semantically correct; the *levels assigned to them* do not describe the document. Nothing here is masked by ARIA, so there is no MAJOR "bad semantics behind ARIA" finding to file.

**Prior-audit anti-pattern sweep (items 1–9): zero hits, and each for a structural reason, not by luck.** No `role="alert"`/`aria-live` anywhere (1). No `title` attributes and no `<a>`/`<button>` at all (2). No `aria-label` and no form (3). No JavaScript, no branches, no view modes (4, 5). No table (6, 7). No images (8). No ARIA attributes added, so nothing to DOM-verify (9).

---

## Phase 3 — ARIA Pattern Compliance Audit

**Nothing to audit, and that is the correct result.** There are no interactive widgets — no tabs, menus, disclosures, comboboxes, dialogs or toggles. Census entries 1–33 contain no `button`, `link`, `textbox`, `combobox`, `menuitem` or any other widget role, and the census is not truncated. No APG pattern applies to this component.

Consequently there is no roving tabindex to check, no `aria-expanded` to synchronize, no `aria-controls` to resolve, and no `aria-modal` to require. Filing any ARIA-pattern finding here would be manufacturing a violation.

**One label to read correctly, not as a defect:** the axe `region` violation carries the tag `cat.keyboard`. That is axe's own rule taxonomy, not evidence of a keyboard problem. The census independently confirms zero focusable elements on the page.

---

## Phase 4 — Focus Management Review

Also nothing to audit, for the same measured reason: **zero focusable elements**. Tab order is trivially correct because there is no tab order; there is no focus trap to build, no focus to restore, no dynamic content whose focus destination could be accidental, no SPA route change inside this component, no async CRUD, no in-page anchors, and no duplicate mobile/desktop rendering.

The CSS (`blog-post.css:1–40`) contains no `visibility:hidden`, no `opacity:0`, no `position:absolute` off-screen pattern, no `overflow:hidden` and no `z-index` — so the "focus-reveal element removed from tab order" catch-22 and the "`aria-hidden` without `inert`" gap both correctly do not fire. There are no `::before`/`::after` rules and no icon-font classes, so the pseudo-element and font-icon exposure checks do not fire either.

Focus-indicator sufficiency (2.4.7, 2.4.13) is **not evaluable and not applicable** — no element can receive focus.

---

## Phase 5 — State Communication Audit

**There is no state.** No loading, no error, no success, no disabled/readonly, no selected/checked/expanded, no status message. `declared_live_regions: []` in the census corroborates that no live region is declared, and — critically — none is *needed*, because nothing on this page changes after render. A missing-`aria-live` finding here would be a false positive.

No visual text symbols are used as state indicators (no `+`/`−`/`×`/`>`), so the aria-hidden-the-glyph check does not fire.

---

## Phase 6 — Multi-Perspective Review

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Confirmed broken heading outline (axe `heading-order` + census levels 1→3→3→3→3→2→2) on a page where headings are the **only** structural affordance — no landmarks, one list, zero interactive elements |
| Keyboard-only | LOW | Zero focusable elements in a complete (`truncated: false`) census; no tab order, no traps, no shortcuts |
| Low vision | LOW | Contrast verified passing by computation and by measured axe negative; fluid `max-width`, no fixed heights, `line-height: 1.6` |
| Cognitive | **MEDIUM** | Document shape is genuinely ambiguous — four small grey topics with no parent, then two large blue peers; plus a heading (`Getting Started`) that labels nothing |
| Vestibular & motion | LOW | No animation, transition, transform, parallax or auto-play anywhere in `blog-post.css:1–40` |
| Auditory access | LOW | No `<video>`, no `<audio>`, no media of any kind |
| Environmental contrast | LOW | No colour-only meaning: heading level is signalled redundantly by font-size (32/24/18px) and by element semantics, both of which survive forced-colors |

I am reading "alarm level" as impact-weighted, not purely pattern-complexity-weighted. By a strict pattern-complexity reading a static text component would top out at MEDIUM everywhere. That reading would rate the one perspective containing a *confirmed, measured* defect the same as the six that are clean, which is not useful. **Screen reader escalates to `/perspective-audit`; cognitive is borderline and can be folded into the same pass.**

---

## Phase 7 — Gap Analysis (What Is Absent)

Covered in the **What's Missing** section below, including the gaps I checked that correctly did **not** fire.

---

# VERDICT: REVISE

**Overall Assessment**: The markup is genuinely clean at the element level — native HTML throughout, zero ARIA and none needed, a correctly computed list, and reading order matching DOM order matching visual order. The single substantive defect is the heading outline, and it is worse than the automated scan reports: axe flagged one of the two heading defects, and the one it structurally *cannot* flag is the one that actually breaks the document's shape. The fix is not a level bump — it is an information-architecture decision the author has to make, and this review declines to make it for them.

**Pre-commitment Predictions vs. Findings**: 4 of 5 predictions confirmed. The miss is instructive: I predicted a contrast failure on the `#666` heading colour and there isn't one (5.74:1 measured-consistent, axe clean). The surprise is that the heading defect is two defects, and that the CSS agrees with the broken markup rather than contradicting it — which means the usual "the visuals show a hierarchy the markup doesn't" framing is the wrong diagnosis and would produce the wrong fix.

---

## Critical Findings (blocks access)

**None.** No user category is blocked. All content is present in DOM order, reachable by linear reading, and correctly announced element-by-element. Stating this plainly: a CRITICAL rating here would be severity inflation.

---

## Findings

### MAJOR-1 — Heading outline is structurally incoherent; axe detects only half of it

**Evidence — source.** `BlogPost.jsx:4–27`:

```jsx
4       <h1>Introduction to Web Accessibility</h1>
6       <h3>Why Accessibility Matters</h3>      <- level jumps 1 -> 3
12      <h3>WCAG Guidelines</h3>
15      <h3>Common Issues</h3>
22      <h3>Getting Started</h3>
24      <h2>Tools and Resources</h2>            <- level drops 3 -> 2, re-parenting everything above
27      <h2>Conclusion</h2>
```

**Evidence — measured, two independent instruments agreeing.**

- axe-core 4.13.0: `heading-order`, impact `moderate`, `node_count: 1`, `sample_selectors: ["h3:nth-child(2)"]`. In `<article>`, the h1 is child 1 and `<h3>Why Accessibility Matters</h3>` is child 2 — the selector resolves to `BlogPost.jsx:6`.
- keyboard-a11y-tester census, computed accessibility tree, in reading order: entry 3 `heading, Introduction to Web Accessibility, level 1` → entry 4 `heading, Why Accessibility Matters, level 3` → entry 8 `level 3` → entry 12 `level 3` → entry 24 `Getting Started, level 3` → entry 25 `heading, Tools and Resources, level 2` → entry 29 `heading, Conclusion, level 2`.

**The half axe cannot see.** axe's `heading-order` rule flags levels that *increase* by more than one. A *decrease* of any size is permitted by the rule — correctly, since closing several nesting levels at once is legitimate. That is why `node_count` is exactly **1**: only the h1→h3 jump at `BlogPost.jsx:6` is reported, and the h3→h2 transition at `BlogPost.jsx:22→24` is invisible to the scanner. But the h3→h2 transition is the more damaging of the two, because it does not merely skip a level — it **retroactively re-parents the first four sections into a level-2 container that never existed**, then closes it. The scanner's `node_count: 1` is accurate and is also an undercount of the problem; this is precisely the class of defect a design review exists to catch.

**What a screen reader user actually experiences.** Heading navigation is the primary skim mechanism for screen reader users. Opening the rotor (VoiceOver) or elements list (NVDA/JAWS) on this article yields:

```
level 1  Introduction to Web Accessibility
level 3  Why Accessibility Matters      -- child of what?
level 3  WCAG Guidelines
level 3  Common Issues
level 3  Getting Started
level 2  Tools and Resources            -- sibling of what?
level 2  Conclusion
```

The four level-3 items assert they are grandchildren of the h1 via a level-2 parent the user never encounters. The user's reasonable inferences are all wrong: that they entered the article mid-way, that a section heading failed to render, or that they should scroll back to find the parent. Then "Tools and Resources" arrives at level 2 as a peer of that phantom section, implying the four topics belong *inside* something that "Tools and Resources" sits beside — which is not the document's actual meaning. WCAG 1.3.1 requires that structure conveyed through presentation be programmatically determinable; here the programmatic structure asserts a containment relationship that does not exist in the content.

**Why MAJOR and not MINOR.** The mitigation that normally softens a heading defect — redundant structural affordances the user can fall back on — **is absent here, and that absence is measured, not assumed**. axe reports `landmark-one-main` and `region` on this page; the census shows the only container in the tree is an unnamed `article` (entry 2, `spoken_phrase: "article"`, no name); there is exactly one list and zero interactive elements. Headings are the sole navigational structure this document offers, and they are the thing that is broken. Removing the user's only skim mechanism on a document that has no other one is a significant degradation of a user category's experience, which is the MAJOR definition. I considered MINOR on the grounds that linear reading recovers everything, and rejected it: "read the whole thing linearly" is not a workaround for a navigation defect, it is the abandonment of navigation.

**Why not CRITICAL.** No content is unreachable and nothing fails silently in a way the user cannot detect. Access is degraded, not blocked.

**The fix is an IA decision, not a find-and-replace — and the CSS proves it.** `blog-post.css:9–27` styles h1 at 32px/#0066cc, h2 at 24px/#0066cc, h3 at 18px/#666. So the four broken sections render *visually subordinate* — small and grey — to "Tools and Resources" and "Conclusion". The markup and the visual presentation **agree with each other**, and both express the same incoherent outline. This rules out the usual diagnosis ("visuals show a hierarchy the markup contradicts") and means the author's intended information architecture was never actually decided. Two mutually exclusive fixes follow, and they produce different documents:

- **Fix A — the four topics are peer sections of the article.** Promote `BlogPost.jsx:6`, `:12`, `:15`, `:22` from `<h3>` to `<h2>`. Outline becomes `h1` + six `h2`s. Clears `heading-order`, clears the re-parenting, requires no new content. **Visual consequence the author must accept:** those four headings shift from 18px/#666 to 24px/#0066cc under the existing CSS rules and become visually heavier. If that appearance is unwanted, change the *styling* — never re-break the levels to recover it.
- **Fix B — the four topics are genuinely subsections of a group.** Insert a real `<h2>` above `BlogPost.jsx:6` naming that group (e.g. "Accessibility Fundamentals") and keep the four as `<h3>`. The existing `<h2>Tools and Resources</h2>` then correctly closes that section. **This requires authoring new content** — a section title that does not currently exist.

**The tell for choosing:** are "Tools and Resources" and "Conclusion" peers *of the four topics* (→ Fix A), or peers of a group *containing* them (→ Fix B)? On the visible content, Fix A is the more plausible intent — "Conclusion" concludes the whole article, not a subsection. But that is my inference from four paragraphs, not knowledge of the author's outline, so it is offered as a reading and not as the answer.

- Confidence: **HIGH** — two independent instruments, plus direct source inspection, plus internally consistent `node_count`.
- Could the developer refute this with missing context? **NO** for the defect. **PARTIALLY** for the fix: only the author knows the intended IA, which is exactly why both branches are given.
- GAP, not preference.

> The `fingerprint` below is a review-assigned stable token for traceability, **not** a tool-emitted digest. Replace it with the harness's canonical hash on ingestion.

```
### A11y Evidence Finding
finding_id: blogpost-heading-outline-incoherent
fingerprint: 4b7e1c9a3d520f68
source: axe-core 4.13.0 rule `heading-order` (013-127-0-0-1-8777-heading-hierarchy-skipped-html.json, viewport 1280x800) + keyboard-a11y-tester sr-census.json entries 3,4,8,12,24,25,29 + BlogPost.jsx:4-27
wcag_or_apg: WCAG 2.2 SC 1.3.1 Info and Relationships (Level A); supporting technique G141 (Organizing a page using headings). Secondary: SC 2.4.6 Headings and Labels (Level AA)
section_508_fpc_context: not in scope - no Revised Section 508 conformance floor was declared for this review. Noted for completeness: SC 1.3.1 exists in the WCAG 2.0 A/AA basis that Revised 508 incorporates, so this finding would carry over if 508 scope is later declared. Note also that axe tags `heading-order` `best-practice` with no WCAG tag - the SC citation here rests on the outline's misstatement of containment, not on the scanner's mapping.
severity: MAJOR
perspective_alarms: screen-reader=HIGH, cognitive=MEDIUM, keyboard=LOW, low-vision=LOW, vestibular=LOW, auditory=LOW, environmental-contrast=LOW
evidence: BlogPost.jsx:6 `<h3>Why Accessibility Matters</h3>` follows BlogPost.jsx:4 `<h1>` (axe selector `h3:nth-child(2)`, node_count 1). BlogPost.jsx:24 `<h2>Tools and Resources</h2>` follows BlogPost.jsx:22 `<h3>Getting Started</h3>`. Census computed levels in reading order: 1, 3, 3, 3, 3, 2, 2. Census `truncated: false`.
reproduction_steps: 1) Load the rendered component. 2) Run axe-core 4.13.0 -> `heading-order` moderate, 1 node at `h3:nth-child(2)`. 3) Open the screen reader heading list (NVDA elements list / VoiceOver rotor) and read levels top to bottom. 4) Observe four level-3 headings with no level-2 ancestor, then a level-2 heading arriving after them.
expected_behavior: The heading list describes the article's real section structure. Every heading below the h1 either sits at level 2 as a peer section, or sits at level 3 beneath an actual level-2 parent that the user encounters first.
actual_behavior: Four level-3 headings assert a level-2 parent that does not exist; the level-2 heading at BlogPost.jsx:24 then arrives as a peer of that phantom parent, implying the four preceding topics are contained by a section that sits beside "Tools and Resources". The automated scan reports only the first of the two transitions.
trend: new
```

---

## Minor Findings (friction, workaround exists)

**MINOR-1 — `<h3>Getting Started</h3>` labels a section that contains nothing.**

`BlogPost.jsx:22` is immediately followed by `BlogPost.jsx:24 <h2>Tools and Resources</h2>` with no intervening content. **Measured:** census entry 24 `heading, Getting Started, level 3` is directly adjacent to entry 25 `heading, Tools and Resources, level 2` — nothing between them, on a census with `truncated: false`, so this is a confirmed absence rather than a gap in the walk. A heading is a promise that content follows; this one makes the promise and breaks it. A screen reader user who selects "Getting Started" from the heading list and reads forward lands immediately in a different topic at a different nesting level. WCAG 1.3.1 (the heading declares a section relationship to content that does not exist); WCAG 2.4.6 secondarily (a heading that describes no topic cannot describe its topic).

Rated MINOR after Realist Check, not MAJOR. **Mitigated by:** reading forward recovers instantly and costs seconds; no content is being withheld, because there is no content; and sighted users encounter exactly the same empty section, so no user group is uniquely disadvantaged. It stays a finding because it compounds MAJOR-1 — the empty heading sits precisely at the point where the phantom level-2 section silently closes, so the user's two sources of confusion arrive together.

**This would be MAJOR if the section is meant to have content that is failing to render.** I cannot distinguish "intentionally empty draft heading" from "content dropped by a rendering bug" from the component source alone. Confirm with the author — see Open Questions.

- Confidence: HIGH on the absence (census-measured); MEDIUM on the interpretation.
- GAP, not preference.

---

## Enhancements (best practice not met, no access barrier)

- **`<article>` has no accessible name.** Census entry 2 spoken as bare `"article"` — measured, not inferred. Adding `id="post-title"` to `BlogPost.jsx:4` and `aria-labelledby="post-title"` to `BlogPost.jsx:3` makes the boundary identifiable as "Introduction to Web Accessibility, article" in the rotor. **Be precise about what this does not do:** `article` is a document-structure role, not a landmark role, and naming it does **not** satisfy axe's `region` rule or `landmark-one-main`. Anyone treating this as the landmark fix will ship a page that still has no landmark.
- **Headings have no `id` attributes.** No stable anchors means no deep-linking to sections and no table of contents can be built without editing the component. For a longer article this becomes a real navigation gap; at four paragraphs it does not.
- **Font sizes are declared in `px`** (`blog-post.css:10, 16, 23`). Stating the nuance correctly: this is **not** a WCAG 1.4.4 Resize Text failure — 1.4.4 is evaluated against browser zoom, and `px` values scale under zoom exactly as `rem` does. What `px` does cost is responsiveness to the user's *browser default font-size* preference, which some low-vision users rely on instead of zoom. `rem` is the better default. Filed as an enhancement specifically so it is not mistaken for a compliance failure.
- **No reverse skip-link / back-to-navigation affordance.** The protocol's deep-content gap check was run and **correctly does not fire**: this article is four paragraphs with zero focusable elements, so there is nothing to reverse-tab through.

---

## What's Missing

**Present in the DOM but not attributable to this component:**

- **No `<main>` landmark; content not contained by any landmark.** axe reports `landmark-one-main` (`moderate`, selector `html`) and `region` (`moderate`, selector `#root`). Both are real observations about the rendered page. **They are not filed as findings against `BlogPost`, and here is the reasoning, using the sibling scans as a control rather than as evidence:** across the 18 pages in the batch, `landmark-one-main` and `region` each appear on **16**. The two exceptions are `004-button-skip-link-clean` (a fixture that by its nature must contain a skip-link target, therefore a `<main>`) and `001-app-focus-order-illogical` (a full-page fixture). The pattern is not random — fixtures authored as isolated component snippets have no page shell, and fixtures authored as whole pages do. `BlogPost` is a component that renders into `#root`; supplying the document's `<main>` is the page shell's job, not this component's. Filing it here would be page-shell over-flagging.
  **The caveat matters:** if this component *is* the whole page in production, the missing `<main>` is a genuine WCAG 2.4.1 / 1.3.1 gap and belongs to whoever owns the shell. I cannot see the shell. See Open Questions.
- **No `lang` attribute** — document-level, outside component scope, not verifiable from what was supplied.

**Gaps checked that correctly do NOT fire** (recorded so the absence of these findings reads as a decision rather than an oversight):

| Gap check | Result | Why |
|---|---|---|
| Missing live region for dynamic content | Does not fire | Nothing changes after render; `declared_live_regions: []` |
| Missing focus restoration | Does not fire | No focus-moving interaction exists |
| Missing skip link | Does not fire | No repeated blocks to bypass; zero focusable elements |
| Missing `prefers-reduced-motion` | Does not fire | No animation/transition/transform in `blog-post.css:1-40` |
| Missing caption/transcript infrastructure | Does not fire | No media elements |
| Missing target sizing (2.5.8) | Does not fire | No pointer targets |
| Missing form label associations | Does not fire | No form controls |
| Missing `aria-current` in navigation | Does not fire | No navigation |
| Missing list semantics | Does not fire | Real `<ul>`/`<li>`; census confirms `set size 3` with correct positions |
| Missing `inert` on hidden content | Does not fire | Nothing hidden |
| CSS `visibility:hidden` focus catch-22 | Does not fire | No such rule in the CSS |
| Pseudo-element / font-icon AT exposure | Does not fire | No `::before`/`::after`, no icon-font classes |
| Broken ARIA references | Does not fire | `declared_broken_aria_refs: []`; no ARIA in source |
| Reading order overridden by CSS | Does not fire | `declared_alternate_reading_order: []`; no flex/grid/order/position in CSS |

---

## Multi-Perspective Notes

**Screen reader user (NVDA, JAWS, VoiceOver).** This is where the entire defect lives. Element-level announcement is clean — headings announce with correct text, the list announces with correct set size and positions, paragraph boundaries are paired, reading order matches DOM order matches visual order, and nothing is redundantly or spuriously announced. What fails is the *structural* layer: the heading list, which is this user's primary skim tool and this page's only structural affordance, describes a document that does not exist (MAJOR-1), and one of its entries leads nowhere (MINOR-1). One calibration note on the instrument: the census is a computed-tree walk, so its *level* and *set size* facts are reliable, but the exact spoken wording will vary by AT and verbosity setting — the structural claims above depend on the levels, not on the phrasing.

**Keyboard-only user.** Nothing to report, and this is a measured negative rather than an assumption: the complete (`truncated: false`) census contains zero focusable elements. No tab order, no traps, no Escape handling required, no undiscoverable shortcuts, no focus indicator to evaluate. The `cat.keyboard` tag on axe's `region` rule is taxonomy, not a keyboard defect.

**Low vision user (200% zoom, high contrast, magnifier).** Clean, and verified rather than waved through:
- Contrast, computed against white: body `#333` **12.6:1**; h1/h2 `#0066cc` **5.57:1** (at 32px/24px these are large text needing 3:1, so passing with margin); h3 `#666` **5.74:1** (at 18px this is *normal* text needing the stricter 4.5:1, and it passes). Corroborated by measurement: axe returned zero `color-contrast` violations **and** `"incomplete": []` on this page, where sibling pages in the same batch did produce contrast incompletes — so axe resolved the real computed backgrounds and found nothing. The CSS never declares a background colour, so my computation assumed white; the axe negative is what validates that assumption.
- Reflow: `max-width: 800px` is a maximum, not a fixed width, so the container shrinks below 800px with no horizontal scroll. No fixed heights, no `overflow: hidden`.
- Text spacing: `line-height: 1.6` (`blog-post.css:5`) exceeds the 1.5 that SC 1.4.12 asks content to survive, and no fixed-height container would clip enlarged text.
- Forced-colors: heading level is signalled redundantly by font-size and by element semantics, both of which survive the system colour override. The blue/grey distinction is lost, but no information is lost with it.
- **Note the honest miss:** I predicted a contrast failure on `#666` before measuring. There isn't one.

**Cognitive accessibility.** MEDIUM, and for one reason: the document's shape is genuinely hard to build a mental model of. Four small grey topics with no visible parent, then two large blue topics that appear to outrank them, then a heading that leads nowhere. A reader trying to answer "how is this article organised?" gets no consistent answer from either the visuals or the markup, because the two agree with each other and both are wrong. The prose itself is clear, plain, and short; there are no timeouts, no destructive actions, no multi-step flow, no authentication and no re-entry of information, so SC 3.3.1/3.3.3/3.3.4/3.3.7/3.3.8 are all inapplicable. Fixing MAJOR-1 and MINOR-1 resolves the cognitive concern; there is no separate cognitive finding to file.

**Vestibular & motion / Auditory access / Environmental contrast.** LOW across all three, with no findings. No animation of any kind, no media of any kind, and no colour-only meaning.

---

## Verdict Justification

**REVISE.** One MAJOR structural defect that requires an authoring decision before it can be fixed, plus one MINOR that may indicate unfinished content. Not ACCEPT-WITH-RESERVATIONS: the defect degrades the only navigation mechanism the document has and the fix path is not yet determined, so shipping-with-a-note is not the right disposition. Not REJECT: the component is otherwise well built — native HTML throughout, no ARIA misuse because no ARIA at all, correct list semantics, clean contrast, clean reading order, and six of seven perspectives with no findings.

**To upgrade to ACCEPT:** resolve MAJOR-1 by choosing Fix A or Fix B and applying it consistently, and resolve MINOR-1 by either giving "Getting Started" content or removing the heading. Re-run axe (expect `heading-order` to clear) **and** re-read the census heading levels — the census is the check that catches the h3→h2 half of the defect, which axe cannot see, so an axe-only re-test would not prove the fix.

**Escalation:** screen reader perspective at HIGH → `/perspective-audit`, with cognitive (MEDIUM) folded into the same pass.

### Recalibrations Applied

| Adjustment | Direction | Reasoning |
|---|---|---|
| MAJOR-1 considered for CRITICAL | **Rejected** | No access loss; all content reachable and correctly announced in DOM order. CRITICAL would be inflation. |
| MAJOR-1 considered for MINOR | **Rejected — held at MAJOR** | The usual mitigation (fall back to landmarks/nav/other structure) is measurably absent: `landmark-one-main` + `region` both fire, the only container is an unnamed `article`, and there are zero interactive elements. "Read it all linearly" abandons navigation rather than working around its loss. |
| MINOR-1 (empty heading) downgraded from MAJOR | **Downgraded** | **Mitigated by:** reading forward recovers in seconds; no content is withheld because none exists; sighted users hit the identical gap, so no group is uniquely disadvantaged. Flagged to rise to MAJOR if the section is supposed to contain content. |
| Missing `<main>` / `region` **not filed** as a component finding | **Withheld** | **Mitigated by:** page-shell ownership, corroborated by 16-of-18 uniformity across the batch with the two exceptions being precisely the full-page fixtures. Carried to Open Questions rather than suppressed. |
| Colour contrast **not filed** | **Withheld — prediction refuted** | Computed 12.6:1 / 5.57:1 / 5.74:1, all passing at their applicable thresholds; corroborated by axe reporting zero contrast violations **and** empty `incomplete` on this page while siblings produced incompletes. |
| `px` font sizes **not filed as SC 1.4.4** | **Downgraded to Enhancement** | 1.4.4 is evaluated against browser zoom, under which `px` scales normally. The real (smaller) cost is unresponsiveness to browser default-font-size preference. |
| 17 off-target axe artifacts **not used as findings** | **Excluded** | `target-size`, `color-contrast`, `label` and `tabindex` violations in the pack belong to other pages. Used only as a control for the landmark question. |

---

## Open Questions (unscored)

1. **Which information architecture is intended — Fix A (six peer h2 sections) or Fix B (an h2 group parent above four h3s)?** This determines the fix and only the author can answer it. My reading of the content favours Fix A, but that is an inference from four paragraphs.
2. **Is `<h3>Getting Started</h3>` an intentionally empty draft heading, a leftover, or a section whose content is failing to render?** Severity of MINOR-1 depends on the answer; the third case makes it MAJOR.
3. **Does the production page shell wrap this component in `<main>`?** If not, `landmark-one-main` and `region` are real gaps against the shell (SC 2.4.1 / 1.3.1). Not verifiable from component scope. Note again that naming the `<article>` does **not** resolve them.
4. **If Fix A is chosen, is the resulting visual change acceptable?** The four headings shift from 18px/#666 to 24px/#0066cc under the existing rules. If not, change the styling — do not restore the h3 levels to recover the appearance.
5. **Was the census produced by an emulated accessibility-tree walk rather than a real AT session?** The structural facts used above (levels, set size, ordering, adjacency) are safe under either reading. Real-AT announcement phrasing may differ and no phrasing claim depends on it.
6. **Background colour.** The supplied CSS never declares one; the contrast figures assume white. The axe negative validates the assumption for the scanned page, but a dark-theme or coloured-container context would need re-measurement — particularly for `#666` at 5.74:1, which has the least headroom of the three.
