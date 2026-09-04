**VERDICT: REVISE**

**Overall Assessment**: This component uses native semantics correctly everywhere except the one thing a static long-form article actually depends on — its heading outline. `<article>`, `<ul>/<li>`, real `<h1>`–`<h3>` elements, and zero ARIA are all the right calls, and there is no ARIA masking bad structure anywhere in the file. But the outline runs `h1 → h3 ×4 → h2 ×2`, which is not merely a skipped level: the four sections that appear first are marked as subordinate to a section that does not exist, and the two genuinely peer sections arrive afterward one level up. On a page that axe measured as having no landmarks at all, heading navigation is the only structural affordance a screen reader user has, and it is inverted. A second defect that no scanner can see — `<h3>Getting Started</h3>` labels a section with zero content — sits inside the same fix.

---

## Phase 0 — Evidence Intake and Provenance

**Review type**: fresh design pass, not a remediation. The a11y-test *Verification evidence contract* gate (which fires when a fix is offered with a mismatched evidence type) does not apply here, so nothing is reported under it.

**Evidence tier — this matters for how the findings below are weighted.** The attached pack is an `a11y-evidence-reader`-class digest. Per the protocol, a digest is one tier *below* the artifact it cites: a paraphrase, not the hard evidence. The protocol requires re-fetching at each cited handle before filing a finding that rests on a digest line. **I could not re-fetch** — this review was run with read access limited to the component/evidence prompt itself. Every axe and census value below is therefore labeled **digest-only** and must be re-verified at its handle before it is quoted in a bug report or ACR row.

The evidence map is favorable despite that constraint:

| Claim | Tier | Load-bearing? |
|---|---|---|
| Heading levels, order, element choice, empty section, CSS colors/sizes | **First-hand** — read directly from the component source and CSS in this prompt | Yes — MAJOR-1 and MINOR-1 stand on this alone |
| axe `heading-order` / `landmark-one-main` / `region`, versions, selectors | digest-only (cannot re-fetch) | Corroborative for MAJOR-1; **load-bearing for MINOR-2** |
| KAT census entries, index positions, four absence claims | digest-only (cannot re-fetch) | Corroborative only |

So the central finding does not depend on the digest at all. The one finding that *does* (MINOR-2, landmarks) is the one already flagged **Needs user verification** below. That is a deliberate placement, not a coincidence.

**Digest caveats I am honoring rather than overriding:**

1. The digest explicitly declines to assert that axe's `h3:nth-child(2)` and the census's `:nth-of-type` selectors name the same DOM node (the raw HTML was not supplied). I therefore do **not** claim "two tools agree on the same element." I claim only that two independent instruments describe the same defect *class* on the same URL.
2. The `region` rule's `tags` array contains `"cat.keyboard"`. The digest correctly flags this as axe's internal rule-taxonomy label. **No keyboard claim is derived from it.**
3. The census's four empty fields (`declared_live_regions`, `declared_broken_aria_refs`, `declared_alternate_reading_order`, and zero interactive-role entries) are informational. They are not clean bills of health for the announcement or keyboard classes — no instrument capable of testing those classes was run.
4. Census tool provenance is inferential (directory name + schema shape); the JSON does not self-declare tool or version, and `session.json`, which might carry it, was not opened. This does not change any finding, but the census cannot be cited by version.
5. axe results are reported at a **single viewport (1280x800)**. Since `heading-order` is viewport-independent, a second scanned viewport would have produced a second row; its absence implies one viewport was scanned. **There is no reflow evidence.** (Inference, flagged as such.)

**What the evidence set cannot answer** (the digest says this itself, and it is correct): `keyboard-operability`, `focus-order-indicator`, and `name-role-state` are all unaddressed, because neither supplied artifact is the prescribed instrument for them (Playwright keyboard transcript / KAT driven focus trace / virtual-screen-reader assertion output). I make no findings in those classes and no clean claims in them either. In this particular component that gap is nearly costless — the captured DOM contains no operable content — but "nothing to test" is a different statement from "tested and clean," and I am making the first one.

---

## Phase 1 — Pre-commitment Predictions

Written before reading the source, from the component type alone (static long-form content, "blog post"):

1. **Heading hierarchy skip or an outline chosen for visual weight** rather than structure — the single most common defect class in static article components.
2. **Missing landmark containment** — no `<main>`, article not labeled, content unreachable by landmark navigation.
3. **CSS driving heading levels** — a developer picking `h3` because it renders at the size the comp wants.
4. **Fixed `px` type and reflow risk** at 400% zoom; missing `lang`.
5. **Low ARIA risk, high under-markup risk** — a static component is unlikely to over-apply ARIA; the danger is semantics that are absent, not semantics that are faked. Correspondingly I predicted **no focus-management findings**, since nothing should be interactive.

Outcome against these is in Phase 10.

---

## Phase 2 — Semantic HTML Audit

Verified line by line against the source, not assumed.

**Correct, and worth stating plainly:**

- `<article>` wraps the post. Right element, not a `<div>`. (Note it is a document-structure role, not a landmark — see MINOR-2.)
- The Common Issues list uses `<ul>` with three `<li>`. Real list semantics, not divs styled as a list — so a screen reader announces "list, 3 items" and offers list navigation. The census corroborates `list/ul` and `listitem/li` roles present.
- Every heading is a real `<h1>`–`<h3>` element. No `role="heading"`, no `aria-level`, no styled `<p>` masquerading as a heading.
- Exactly one `<h1>`, and it is the article title. Correct.
- **Zero ARIA attributes in the entire component** — and for this component that is the right answer, not an omission. Native semantics carry the full load. The protocol's non-negotiable "native HTML first" rule is satisfied without qualification. There is nothing here where ARIA is papering over bad structure.
- No tables at all, so the layout-table / `role="presentation"` / `td-in-loop` anti-patterns do not arise.
- No form controls, so no label-association surface.

**Incorrect:** the heading hierarchy. `h1` → `h3` → `h3` → `h3` → `h3` → `h2` → `h2`. See MAJOR-1.

**Not verifiable from a component fragment:** `lang` on `<html>` — this component does not render the document element, so its absence here is not a defect. It is an integration question (Open Questions).

---

## Phase 3 — ARIA Pattern Compliance Audit

**No interactive widgets exist.** There is no disclosure, tablist, menu, combobox, dialog, or composite widget in this component. There is therefore no APG pattern to match against, no roving tabindex obligation, no `aria-expanded`/`aria-controls` pairing to verify, and no required-state checklist to run.

This is not a gap I am waving through — I checked for the inverse failure (ARIA present but incomplete) and for the "80% pattern" trap the protocol calls out, and neither applies because there is no ARIA at all. The census independently records zero interactive-role entries across all 33 entries (digest-only): no button, link, textbox, checkbox, combobox, or menuitem.

**Phase 3 finding count: zero.** Manufacturing an ARIA finding here would be exactly the failure mode this protocol warns against.

---

## Phase 4 — Focus Management Review

**Nothing in this component is focusable.** No links, no buttons, no controls, no `tabindex`, no modals, no dynamic content, no route changes, no async CRUD, no in-page anchors. There is no tab order to evaluate, no focus trap to check, no restoration to verify, and no focus indicator to measure.

Two honest boundaries on that statement:

- The census records no interactive roles (digest-only), which describes the captured DOM. It is consistent with the source, which I read first-hand.
- **No keyboard instrument was run.** Neither supplied artifact can produce focus-movement or key-press records — the digest's own absence claim confirms `grep -ioE "focus|keydown|keypress|tabindex|keyboard"` returns nothing on the census and matches only the `region` rule's taxonomy tag in the axe file. So this is "no operable content exists in the source or the captured DOM," not "keyboard operability was measured and passed."

**Phase 4 finding count: zero.** The one focus-adjacent gap worth naming is a page-level consequence, not a component defect: with no landmarks and no skip link anywhere in the captured page, a keyboard user arriving at this content has no bypass mechanism (WCAG 2.4.1). That is the host page's obligation, and it is folded into MINOR-2 rather than double-counted here.

---

## Phase 5 — State Communication Audit

**There is no state.** No loading, error, success, disabled, readonly, selected, checked, or expanded state exists in this component. No `aria-live`, `role="status"`, or `aria-busy` is present — and none is required, because nothing changes after render.

Checked and clear:

- No visual-text symbols used as state indicators (`+`/`−`/`×`/`>`), so the `aria-hidden` obligation on symbol glyphs does not arise.
- No `::before`/`::after` `content` anywhere in the CSS — verified by reading the full stylesheet. So the pseudo-element-exposed-to-AT gap does not apply.
- No icon-font classes (`.fa`, `.icon`, `.glyphicon`).
- Census records `declared_live_regions: []` and `declared_broken_aria_refs: []` (digest-only), consistent with the source.

**Phase 5 finding count: zero.**

---

## Phase 6 — Multi-Perspective Review

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Heading outline is the sole structural navigation affordance on a page axe measured as landmark-free, and the outline is inverted (h1 → h3×4 → h2×2). One heading labels an empty section. |
| Keyboard-only | **LOW** | Zero focusable elements in source and in the captured DOM. Nothing to operate. Caveat: no keyboard instrument was run — this is "nothing to test," not "tested clean." |
| Low vision | **MEDIUM** | Fixed `px` type throughout; no `background-color` declared, so contrast rests on an inherited value this file does not set; visual hierarchy faithfully reproduces the wrong outline, so magnifier users get the same broken mental model; **no reflow evidence** (single 1280x800 viewport scanned). |
| Cognitive | **MEDIUM** | Document structure is the primary comprehension scaffold for long-form reading and it misrepresents section relationships; a heading promises a section that delivers nothing. |
| Vestibular & motion | **LOW** | Verified by reading the full CSS: no `@keyframes`, no `transition`, no `animation`, no `transform`, no auto-playing content. The absence of a `prefers-reduced-motion` block is correct here, not a gap. |
| Auditory access | **LOW** | No `<video>`, `<audio>`, or media element in the source. Census records only `document/article/heading/paragraph/list/listitem` roles (digest-only) — no media role present. |
| Environmental contrast | **MEDIUM** | Heading level is signalled by size *and* colour (not colour alone — 1.4.1 is satisfied), but no `background-color` is declared, so forced-colors / user-stylesheet behavior is unverified and every computed ratio below rests on an assumed background. |

**Screen reader (HIGH) — escalate to `/perspective-audit`.** This is where the component actually fails. A user pressing `H`, or `1`/`2`/`3`, or opening NVDA's Elements List or VoiceOver's rotor, gets this outline:

```
level 1  Introduction to Web Accessibility
  level 3  Why Accessibility Matters      ← nested under nothing
  level 3  WCAG Guidelines
  level 3  Common Issues
  level 3  Getting Started                ← section is empty
level 2  Tools and Resources              ← arrives after its apparent children
level 2  Conclusion
```

Two distinct harms fall out of that. First, the rotor indents by level, so the first four sections render as children of a level-2 heading the user never heard; the trained response is to back up hunting for a missed heading, and there is nothing to find. Second, once "Tools and Resources" arrives at level 2, the user cannot tell whether it is a peer of the four preceding sections or a parent whose children were somehow printed before it. On a longer article that ambiguity determines what gets skipped. Because axe measured no landmarks on this page (digest-only), heading navigation is not one of several structural affordances here — it is the only one.

**Keyboard-only (LOW).** Nothing to navigate, nothing to trap, nothing to restore. Bounded as stated above.

**Low vision (MEDIUM).** Contrast, computed by me from the declared CSS against an **assumed white background** (the stylesheet declares no `background-color`):

- `#0066cc` on `#ffffff` (h1 at 32px, h2 at 24px) ≈ **5.57:1** — passes 4.5:1 normal-text and 3:1 large-text.
- `#666666` on `#ffffff` (h3 at 18px) ≈ **5.74:1** — passes 4.5:1.
- `#333333` on `#ffffff` (body) ≈ **12.6:1** — comfortable.

Corroborating (digest-only): axe reported neither a `color-contrast` violation nor any `incomplete` result (`incomplete: []`) on the rendered page, which is consistent with a measured pass on the real background. That inference assumes axe's default rule set ran, which the digest does not state explicitly.

`line-height: 1.6` already meets the 1.5× line-height target of WCAG 1.4.12 Text Spacing, and since no element in the stylesheet declares a fixed `height`, user-applied spacing overrides should not clip content. `max-width: 800px` keeps line length in a readable band. These are good defaults and I am not manufacturing a finding out of them. Reflow at 320px / 400% is **untested** — likely fine given `max-width` plus a 20px padding and no fixed widths, but no instrument measured it.

The one substantive low-vision point is that the CSS makes the four mis-levelled sections *look* subordinate (18px, `#666`) while the two correctly-levelled ones look primary (24px, `#0066cc`). Visual and programmatic hierarchies agree — and both misdescribe the content. That distinction is load-bearing for the fix: this is not a visual/programmatic mismatch that CSS can reconcile, so no styling change repairs it.

**Cognitive (MEDIUM).** For a reader who builds a mental map from structure, "Getting Started" followed immediately by "Tools and Resources" reads as content that failed to load. The inverted nesting makes the article's shape unrecoverable without reading it linearly, which is the exact work headings exist to save. No timeouts, no destructive actions, no multi-step flow, no authentication — 3.3.4, 3.3.7, and 3.3.8 do not arise.

---

## Phase 7 — Gap Analysis (What Is Absent)

- **No `<main>` and no landmark containment.** axe: `landmark-one-main` on `html` and `region` on `#root`, both moderate (digest-only). See MINOR-2 for the scoping argument.
- **Content for the "Getting Started" section.** See MINOR-1.
- **An accessible name on `<article>`.** `aria-labelledby` pointing at an `id` on the `<h1>` would name it. Payoff is modest — `article` is a document-structure role, not a landmark, so it does not appear in landmark navigation in most screen readers. Enhancement only; I am not inflating it.
- **Reflow evidence.** One viewport scanned. WCAG 1.4.10 is untested, not passed.
- **A declared `background-color`.** Every contrast number above, mine and axe's, depends on an ancestor this file does not control. Under a user stylesheet or a dark host theme, `#666` headings are the first thing to fall below 4.5:1.
- **`lang`.** Not this component's to render; integration question.
- **Keyboard and announcement instrumentation.** Not run. Costless here, but the evidence set cannot *prove* the component is inert; it can only show that the captured DOM contains nothing operable.

**Correctly absent — not gaps:** `prefers-reduced-motion` (no motion), `aria-live` (no dynamic content), focus management (nothing focusable), skip link *within this component* (no repeated blocks here), caption/transcript infrastructure (no media), `autocomplete` (no fields).

**Anti-pattern checklist from the April 2026 third-party audit** — all nine checked, none applicable: no `role="alert"`/`aria-live` in loops (1); no `title` attributes (2); no `aria-label` on containers (3); no if/else focus logic (4); no selector-scoped JS (5); no tables (6, 7); no images (8); no ARIA attributes to DOM-verify (9).

---

## Phase 8 — Realist Check (Severity Calibration)

**MAJOR-1 (heading hierarchy)** run through all four questions:

1. *Realistic worst case if shipped?* A screen reader user opens the article, calls up the heading list, and sees four sections nested under a phantom parent followed by two at a higher level. They backtrack looking for a heading that does not exist, then have to guess whether "Tools and Resources" is a peer or a parent. All content remains readable in linear order — nothing is unreachable.
2. *Who is impacted?* Screen reader users primarily; cognitive/structure-comprehension users secondarily; magnifier users tertiarily (they read the same wrong hierarchy visually).
3. *Detection speed?* axe flags the skip in seconds. **But axe flags only the skip** — not the inversion, not the empty section. A team that fixes to green can still ship a wrong outline. Fast detection, incomplete detection.
4. *Proportional?* Not CRITICAL — no access loss, no trap, no silent failure; linear reading delivers everything. Not MINOR either: the severity scale's own MINOR exemplar is *"heading hierarchy has gaps **but landmark structure is clear**,"* and that mitigation is measured absent here (axe: `landmark-one-main`, `region`). With no landmarks, the broken outline is a defect in the only structural navigation mechanism these users have. **MAJOR stands. No downgrade.**

**MINOR-1 (empty section)** was a candidate MAJOR and was downgraded. *Mitigated by:* the emptiness is equally evident to sighted and screen-reader users — both encounter two adjacent headings — so no user group is selectively disadvantaged, and no content is lost because there is no content to lose. The AT-specific amplification is real but small: a screen-reader user navigating by heading commits to a landing point before discovering it is empty, one heading later than a sighted scanner would. Friction, not degradation. Its value is that **no scanner can detect it** — axe's `empty-heading` rule fires on headings with no *text*, not headings with no *following content* — which is why it belongs in a design review rather than a scan.

**MINOR-2 (landmarks)** was a candidate MAJOR and was downgraded. *Mitigated by:* the evidence comes from an isolated fixture harness (`#root`), which cannot distinguish a component defect from a harness artifact; the component's own use of `<article>` is correct; and landmark provision is properly the host page's responsibility, not a reusable post component's. Flagged **Needs user verification** rather than suppressed.

---

## Phase 9 — Self-Audit

| Finding | Confidence | Developer could refute? | Gap or preference? | Disposition |
|---|---|---|---|---|
| MAJOR-1 heading hierarchy | **HIGH** | No — source read first-hand; "the design wants smaller headings" is answerable with CSS, since heading level must follow structure, not appearance | GAP | Keep as MAJOR |
| MINOR-1 empty section | **HIGH** on the fact | No | GAP (with a content-defect component) | Keep as MINOR |
| MINOR-2 landmarks | **MEDIUM** as a *component* finding | **Yes** — "the app shell provides `<main>`; this is a harness artifact" | GAP at page scope, possibly N/A at component scope | Keep as MINOR, flagged **Needs user verification**, cross-referenced in Open Questions |
| Contrast | MEDIUM (assumed background) | Yes | Passes — not a finding | Moved to perspective notes + Open Questions |
| `px` font sizing | HIGH on the fact, low on impact | Yes | PREFERENCE-adjacent | Downgraded to ENHANCEMENT |

MINOR-2 sits at the seam between two protocol rules — "developer could refute → Open Questions" and "suspected false positive → mark *Needs user verification*, do not suppress silently." I applied the second, because the underlying measurement is hard (axe genuinely found no landmark on the rendered page); what is uncertain is only whether the rendered page is representative. Suppressing it would lose a real page-level barrier; filing it flat would blame this file for the shell's omission.

---

## Findings

### Major Findings

**MAJOR-1 — Heading hierarchy skips level 2 and inverts section nesting; the article's outline misrepresents which sections are peers.**

Evidence (first-hand, component source in the review prompt):

```
line 4   <h1>Introduction to Web Accessibility</h1>
line 6   <h3>Why Accessibility Matters</h3>     ← level 2 skipped
line 12  <h3>WCAG Guidelines</h3>
line 15  <h3>Common Issues</h3>
line 22  <h3>Getting Started</h3>
line 24  <h2>Tools and Resources</h2>           ← level 2 arrives after its apparent children
line 27  <h2>Conclusion</h2>
```

All six section headings are peer top-level sections of the article — "Why Accessibility Matters" is no more a subsection of anything than "Conclusion" is. Four of them are marked `h3`, asserting subordination to a level-2 section that does not exist anywhere in the document.

Corroborating instruments (**digest-only** — not re-fetched at their handles):

- axe-core 4.13.0, `heading-order`, impact moderate, 1 node, sample selector `h3:nth-child(2)`, help text *"Heading levels should only increase by one."*
- KAT screen-reader reading-order census: heading entries walk `level 1 → 3 → 3 → 3 → 3 → 2 → 2`, with no level-2 heading between the level-1 and the four level-3s.

These two describe the same defect class on the same URL. Following the digest's own caveat, I do **not** assert the axe `:nth-child` selector and the census `:nth-of-type` selectors resolve to the same DOM node — the raw HTML was not supplied.

*User group*: screen reader users (primary), cognitive/structure comprehension (secondary), low-vision magnifier users (tertiary).

*WCAG grounding — and an honest note on which citation is sturdier.* The conventional mapping for heading-order defects is **1.3.1 Info and Relationships (A)**, and I cite it as primary. But it is contestable here on a strict reading, and the review is stronger for saying so: 1.3.1 requires that structure conveyed *through presentation* be programmatically determinable, and in this component the CSS and the markup **agree** — both present the four sections as subordinate. What is wrong is that both misdescribe the content's actual structure. The sturdier hook is therefore **2.4.6 Headings and Labels (AA)**: a heading's *level* is part of what it communicates, and a level-3 heading asserts "this is a subsection of the preceding level-2 section." That assertion is false four times over. (WCAG 2.4.10 Section Headings is AAA and outside the AA target; noted as context only.) Worth recording for anyone reading the axe row: axe itself tags `heading-order` `cat.semantics` + `best-practice` with **no WCAG tag**, which is precisely why a bare "violates 1.3.1" citation invites pushback and why the 2.4.6 argument should lead.

*Expected behavior*: heading levels descend by at most one and reflect the content's real containment, so that a rotor or elements-list rendering of the outline matches the article's actual section structure.

*Fix*: promote all four `<h3>` elements to `<h2>`. Final outline: one `h1` and five `h2` peers. Then restyle — if the design calls for the first four sections to read lighter, that is a class on the `h2` (`.blog-post h2.subsection`), not a level change.

**Two fixes to refuse, both of which turn the axe row green without repairing the outline:**

1. **Do not insert a filler `<h2>`** (visually hidden or otherwise) before "Why Accessibility Matters" to satisfy the linter. That manufactures a phantom section a screen reader user will navigate into and find empty — trading one structural lie for another.
2. **Do not demote the two trailing `<h2>` elements to `<h3>`.** It leaves `h1 → h3`, still failing the rule, and additionally flattens two real sections.
3. **Do not reach for `role="heading" aria-level="2"`.** Native `<h2>` is available; ARIA must not replace semantics HTML already provides.

- Confidence: **HIGH**
- Why this matters: on a page axe measured as having no landmarks, the heading outline is not one navigation affordance among several — it is the only one. Breaking it removes the sole structural map these users have, on a content type where structural navigation is the primary reading strategy.
- Fix: as above — four `h3` → `h2`, styling handled with a class.

```
### A11y Evidence Finding
finding_id: blogpost-heading-outline-inverted
fingerprint: DERIVATION RECORDED, VALUE NOT COMPUTED — recipe: sha256("BlogPost.jsx|heading-order|h1>h3-inverted-outline").
  Not computed in this read-only pass; a fabricated hex value would be worse than an honest gap, so the
  recipe is recorded instead. Do not treat this row as fingerprint-stable until the value is computed at fix time.
source: component source read first-hand in the review prompt (BlogPost.jsx, lines 4-27) — PRIMARY.
  Corroborating, DIGEST-ONLY (not re-fetched at handle):
  axe-core 4.13.0 rule "heading-order",
  evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/013-127-0-0-1-8777-heading-hierarchy-skipped-html.json;
  KAT screen-reader reading-order census, .../heading-hierarchy-skipped-kat-census/sr-census.json
wcag_or_apg: WCAG 2.2 SC 2.4.6 Headings and Labels (AA) — primary, sturdier hook;
  WCAG 2.2 SC 1.3.1 Info and Relationships (A) — conventional mapping, contestable on presentation-parity grounds
  because CSS and markup agree while both misdescribe the content. SC 2.4.10 (AAA) noted as context, out of AA target.
section_508_fpc_context: not in scope — no Section 508 conformance floor is declared for this review.
  Recorded for completeness: both cited SCs exist in WCAG 2.0 A/AA, so the finding would survive a 508-scoped re-read.
  No ICT Testing Baseline test ID is cited, and none should be at component scope.
severity: MAJOR
perspective_alarms: screen-reader=HIGH; cognitive=MEDIUM; low-vision=MEDIUM; environmental-contrast=MEDIUM;
  keyboard=LOW; vestibular=LOW; auditory=LOW
evidence: |
  FIRST-HAND (component source):
    <h1>Introduction to Web Accessibility</h1>
    <h3>Why Accessibility Matters</h3>   <h3>WCAG Guidelines</h3>
    <h3>Common Issues</h3>               <h3>Getting Started</h3>
    <h2>Tools and Resources</h2>         <h2>Conclusion</h2>
  DIGEST-ONLY (axe, .viewports."1280x800".violations[]):
    1280x800  heading-order  moderate  1  h3:nth-child(2)
    "help": "Heading levels should only increase by one"
  DIGEST-ONLY (census, .entries[] | select(.role=="heading")):
    index 3  level 1 | index 4  level 3 | index 8  level 3 | index 12 level 3
    index 24 level 3 | index 25 level 2 | index 29 level 2
reproduction_steps: |
  1. Render BlogPost and open the heading list (NVDA Elements List / JAWS heading list / VoiceOver rotor).
  2. Observe four level-3 entries indented beneath the level-1 title with no level-2 parent,
     followed by two level-3-preceded level-2 entries.
  3. Re-verify the digest-only rows at their handles before quoting:
     jq -r '.viewports|to_entries[]|.key as $vp|.value.violations[]?|[$vp,.id,.impact,.node_count,(.sample_selectors[0]//"-")]|@tsv' <axe-file>
     jq '.["http://127.0.0.1:8777/heading-hierarchy-skipped.html"].entries[] | select(.role=="heading")' <census-file>
expected_behavior: Heading levels descend by at most one and reflect real section containment; the rotor outline
  renders six peer sections under one title.
actual_behavior: Outline renders as h1 -> h3 x4 -> h2 x2. Four peer sections are announced as subsections of a
  level-2 section that does not exist; the two correctly-levelled sections arrive after their apparent children.
trend: new
```

### Minor Findings

**MINOR-1 — `<h3>Getting Started</h3>` labels a section with no content. No scanner can detect this.**

Source (first-hand), lines 22–24: `<h3>Getting Started</h3>` is followed immediately by `<h2>Tools and Resources</h2>`. There is no paragraph, list, or any other content between them.

Corroborating (digest-only): the census places "Getting Started" at index 24 and "Tools and Resources" at index 25 — **consecutive**, while every other heading-to-heading interval where the source shows intervening content is at least three entries wide (a `<p>` occupies three slots; the `<ul>` occupies eleven). I have not reconstructed the full 33-entry list — the digest lists only the seven heading entries — so I treat the gap *pattern* as corroboration of the source, not as an independent measurement (see Open Questions for a reconciliation discrepancy).

*Why this is a design-review finding rather than a scan finding*: axe's `empty-heading` rule fires on headings with no *text content*. This heading has text; what it lacks is a *section*. No automated rule in axe, Pa11y, or HTML-CS covers "heading introduces nothing," which is exactly the class this critic exists to catch.

*WCAG grounding*: **2.4.6 Headings and Labels (AA)** — a heading must describe the topic or purpose of the section it introduces; there is no section. Secondarily **1.3.1 (A)** — a structural relationship is asserted with no content on the other end of it.

- Confidence: **HIGH** on the fact; MEDIUM that it warrants an a11y label at all rather than a content-bug label.
- Why this matters: a screen-reader user navigating by heading commits to a landing point and discovers it empty one heading later; a sighted scanner sees both headings in a single glance. Real but modest AT amplification.
- Fix: supply the section's content, or remove the heading. If a "Getting Started" section is genuinely planned, ship it with a placeholder body rather than a bare heading. Bundle this with MAJOR-1 — once the four `h3`s become `h2`s, an empty `h2` is more conspicuous, not less.

**MINOR-2 — No landmark contains the page content; no `<main>` exists. Scoped to the host page, not to this component. Needs user verification.**

Evidence (**digest-only, and load-bearing** — this is the one finding that does not have first-hand backing):

- axe `landmark-one-main`, moderate, 1 node, selector `html` — *"Document should have one main landmark."*
- axe `region`, moderate, 1 node, selector `#root` — *"All page content should be contained by landmarks."*

Two things are true at once. The component is correct: `<article>` is the right element for a blog post, and a reusable post component should *not* render its own `<main>` — a page may hold several articles. And the page is wrong: with no landmark at all, a screen reader user gets no landmark navigation and no bypass mechanism (WCAG 1.3.1, 2.4.1). Note that `<article>` does not satisfy the `region` rule because `article` is a document-structure role, not a landmark — which is correct behavior on axe's part, not a false positive.

The selector `#root` is a React mount point, which strongly suggests the evidence was captured from an isolated fixture harness rather than a production shell. That is why this is filed as MINOR with a verification flag rather than as a MAJOR against this file.

- Confidence: **MEDIUM** as a component finding; **HIGH** that the *rendered page under test* had no landmark.
- **Needs user verification** — concrete check: open the production route that renders `BlogPost`, inspect the DevTools Accessibility tree, and confirm a `main` landmark contains this `<article>`. If it does, close this finding as a harness artifact. If it does not, re-file it at the page/layout level as MAJOR, where the missing bypass mechanism is a genuine barrier.
- Fix (at the host page, not here): wrap the route's content in `<main>`; keep `<article>` where it is.

### Enhancements

- **Name the `<article>`** — add an `id` to the `<h1>` and `aria-labelledby` on the `<article>`. Payoff is modest: `article` is not a landmark, so most screen readers will not surface the name in landmark navigation. Worth doing when the page holds more than one article; not otherwise urgent.
- **Move type from `px` to `rem`** — `32px`/`24px`/`18px` scale correctly under browser zoom, so this is **not** a WCAG 1.4.4 failure and I am not filing it as one. `rem` additionally honors a user's browser default font-size preference, which `px` ignores. Preference-adjacent; listed as an enhancement, not a finding.
- **Declare a `background-color` on `.blog-post`** — every contrast ratio in this review, mine and axe's, depends on a background this stylesheet does not set. Declaring it makes the `#666` headings' 4.5:1 margin the component's own guarantee rather than an inherited accident.
- **Test forced-colors mode** — with no `background-color` and colour-differentiated headings, Windows High Contrast is the most likely place for the visual hierarchy to collapse.

---

## What's Missing

- Content for the "Getting Started" section (MINOR-1).
- Landmark containment at the page level (MINOR-2).
- **Reflow evidence** — one viewport (1280x800) scanned. WCAG 1.4.10 at 320px / 400% is untested, not passed. Likely fine (`max-width` plus padding, no fixed widths, no fixed heights), but unmeasured.
- **A declared background colour** — all contrast conclusions rest on an assumption.
- **`lang`** — outside this fragment's control; an integration question, not a defect here.
- **Keyboard and announcement instrumentation** — not run and not obtainable from these two artifacts. Costless for this component, but the evidence set cannot prove inertness; it can only show the captured DOM holds nothing operable.

Correctly absent and deliberately **not** listed as gaps: `prefers-reduced-motion` (no motion exists), `aria-live` (nothing changes), focus restoration (nothing focusable), skip link within the component (no repeated blocks), captions/transcripts (no media), `autocomplete` (no fields). Listing these would be manufacturing gaps out of a component's correct scope.

---

## Multi-Perspective Notes

- **Screen reader user**: Semantic structure is *present* but *wrong*. Every element choice is correct — `article`, real headings, real list — and the rotor still produces an outline in which four peer sections read as children of a heading that was never announced, followed by two sections that arrive one level up. The user's likely behavior is backtracking to find a missed level-2 heading, then guessing at peer relationships. "Getting Started" is a landing point that delivers nothing. No live regions, no ARIA relationships, no announcements to evaluate — and none needed.
- **Keyboard-only user**: Nothing focusable exists, so there is no tab order, no trap, no restoration question, and no focus indicator to measure. Bounded honestly: no keyboard instrument was run, so this is "no operable content in source or captured DOM," not a measured pass.
- **Low vision user (200% zoom, high contrast)**: Contrast is comfortable against an assumed white background (≈5.57:1 headings, ≈5.74:1 h3, ≈12.6:1 body) and axe reported no contrast violation and no incomplete results. `line-height: 1.6` already satisfies 1.4.12's spacing target and no fixed heights threaten it. The real point is that the CSS faithfully renders the wrong hierarchy — magnifier users, who lean hardest on visual weight to orient, get the same broken map as screen reader users. No CSS change fixes that. Reflow is untested.
- **Cognitive accessibility**: Prose is clear, line length is controlled, there are no timeouts, no destructive actions, and no multi-step flow. The failure is the comprehension scaffold: the outline misrepresents the article's shape, and one heading opens a section that never arrives. Both cost the reader the exact work headings are supposed to save.

---

## Phase 10 — Synthesis: Predictions vs. Findings

- **Prediction 1 (heading skip / outline chosen for visual weight)** — hit, and worse than predicted. I anticipated a skip; the actual defect is an *inversion*, with the level-2 headings arriving after the level-3s. A plain skip is one wrong edge in the outline tree; this misassigns four sections and then contradicts itself.
- **Prediction 2 (missing landmark)** — hit, but the interesting part was the scoping. The measurement is real; whether it indicts this component is not determinable from a `#root` harness render. That became MINOR-2's verification flag.
- **Prediction 3 (CSS driving heading levels)** — partially hit, with a nuance I had not anticipated. I expected a visual/programmatic *mismatch*. What is here is agreement — the CSS mirrors the wrong markup faithfully — which is a different and harder problem, because it means the defect is invisible to a reviewer comparing rendered output against the DOM, and unfixable in CSS.
- **Prediction 4 (px sizing, reflow, lang)** — partially hit and appropriately downgraded. `px` is real but scales under zoom, so ENHANCEMENT. `lang` turned out to be out of scope for a fragment. Reflow became a genuine evidence gap rather than a finding.
- **Prediction 5 (low ARIA risk, no focus findings)** — hit exactly. Zero ARIA, zero interactive elements, zero Phase 3/4/5 findings. Predicting this correctly is what kept me from manufacturing pattern findings in three consecutive phases.

**What I did not predict and should have**: the empty "Getting Started" section. It is the most interesting finding in the set precisely because no scanner produces it, and it never appeared in my pre-commitment list — I predicted defects in the heading *hierarchy* and missed defects in the heading *contract* (a heading promising content that exists). Worth carrying forward as a check for any long-form content component.

---

## Verdict Justification

**REVISE.** One MAJOR, two MINOR, four enhancements, no CRITICAL.

REVISE rather than ACCEPT-WITH-RESERVATIONS because MAJOR-1 is not a peripheral defect in an otherwise-sound component — it is a defect in the component's *entire accessibility contribution*. A static blog post has exactly one structural affordance to offer assistive technology: its heading outline. Everything else here is correct, and that correctness is what isolates the failure rather than excusing it. On a page axe measured as landmark-free, a wrong outline is not degraded navigation, it is the only navigation, degraded.

REVISE rather than REJECT because the fix is four characters, four times, plus a CSS class — and because nothing is unreachable. Linear reading still delivers every word.

*Recalibrations performed (Phase 8):* MINOR-1 downgraded from candidate MAJOR (mitigated by equal cross-group impact and zero content loss); MINOR-2 downgraded from candidate MAJOR (mitigated by harness-artifact ambiguity and correct component-level element choice); `px` sizing downgraded to ENHANCEMENT (mitigated by `px` scaling correctly under browser zoom, so no 1.4.4 failure). MAJOR-1 survived all four Realist Check questions unchanged, specifically because the severity scale's MINOR exemplar for heading gaps is expressly conditioned on landmark structure being clear, and axe measured that it is not.

**To upgrade to ACCEPT:** promote the four `<h3>` elements to `<h2>` (styling via class, not level); supply or remove "Getting Started"; confirm the host page wraps this in `<main>`. Re-run axe at a second viewport to close the reflow gap.

**Escalation:** screen reader perspective is **HIGH** — route to `/perspective-audit`. Low vision, cognitive, and environmental contrast are **MEDIUM** and warrant the same if the component ships into a themeable or high-contrast context.

**Evidence-integrity caveat, restated because it governs how these findings may be reused:** every axe and census value in this review is **digest-only**. The protocol requires re-fetching at the cited handle before a digest line supports a filed finding, and that re-fetch was not possible in this pass. MAJOR-1 and MINOR-1 are unaffected — both stand on the component source read first-hand. **MINOR-2 is load-bearing on un-re-fetched digest lines and must not be filed as a bug or serialized into an ACR row until `013-127-0-0-1-8777-heading-hierarchy-skipped-html.json` is opened at its handle.**

---

## Open Questions (unscored)

1. **Does the production page wrap this in `<main>`?** Determines whether MINOR-2 is a harness artifact or a page-level MAJOR. Check: DevTools Accessibility tree on the real route.
2. **What background does `.blog-post` inherit?** No `background-color` is declared. Every contrast figure in this review — and axe's silence on `color-contrast` — assumes white. Under a dark or themed host, `#666` at 18px is the first value to fail.
3. **Census entry-count reconciliation.** Modelling the census schema from the seven heading entries the digest exposes (headings = 1 slot; `<p>` = 3; `<ul>` with three `<li>` = 11) reconstructs to 34 entries against the digest's stated 33. The one-entry discrepancy means I cannot fully model the schema from the digest alone. It does not affect MINOR-1 — the index 24/25 adjacency is stated directly and the source shows the empty section independently — but it is the point where my confidence in the census arithmetic drops, and it is why I treated the gap pattern as corroboration rather than measurement.
4. **Are the truncated paragraphs (`"...provide a set of standards..."`, `"...help with accessibility testing..."`) fixture scaffolding or shipped content?** If shipped, that is a content-completeness issue rather than an accessibility one, though it compounds MINOR-1's impression of an unfinished page. Not filed as a finding.
5. **Is a "Getting Started" section planned?** Determines whether MINOR-1's fix is "add content" or "remove heading."
6. **Should the four promoted `<h2>` elements keep their lighter visual treatment?** A design decision, not an accessibility one — either answer is fine so long as the level follows the structure and the class carries the styling. Raised only to pre-empt the level being changed back to match a comp.
