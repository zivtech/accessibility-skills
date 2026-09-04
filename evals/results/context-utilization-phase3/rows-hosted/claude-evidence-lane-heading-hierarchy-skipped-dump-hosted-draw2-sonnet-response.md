# Accessibility Design Critic Review — BlogPost (Heading Hierarchy Fixture)

## Phase 0 — Evidence Consumption and Scope

Evidence supplied for this review:

1. **Axe-core scan** for the exact page under review — `evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/013-127-0-0-1-8777-heading-hierarchy-skipped-html.json` (`url: http://127.0.0.1:8777/heading-hierarchy-skipped.html`, axe-core 4.13.0, viewport 1280x800, `status: measured`, `http_status: 200`). This is HARD EVIDENCE per the evidence contract and is treated as measured fact, not estimate.
2. **Screen-reader reading-order census** for the same URL — `evals/results/context-utilization-phase3/raw/heading-hierarchy-skipped-kat-census/sr-census.json`, a `keyboard-a11y-tester`-style census with 33 indexed trace entries (`spoken_phrase`, `role`, `tag`, `selector` per step), `truncated: false`. Per-step trace facts from this artifact are treated as the same tier of hard evidence as a codified Playwright run.
3. **Sixteen additional axe-core scans for sibling pages in the same batch** (`accordion-no-region-role`, `app-focus-order-illogical`, `async-form-vague-success`, `breadcrumb-navigation-no-nav-landmark`, `button-skip-link-clean`, `checkbox-group-no-fieldset`, `combobox-autocomplete-no-listbox-role`, `dashboard-heading-inconsistency`, `data-table-missing-scope`, `expandable-section-no-button`, `file-input-no-labels`, `form-field-vs-summary-errors`, `form-validation-missing-aria-describedby`, `image-carousel-no-region`, `infinite-scroll-no-announcement`, `interactive-dropdown-clean`, `interactive-dropdown-focus-bug`). **These are scans of different components on different pages, not of BlogPost.** None of their violations (target-size, tabindex, label, aria-valid-attr-value, color-contrast, bypass, etc.) are attributed to BlogPost in this review — importing them would be evidence misattribution. They are used exactly once, below, purely as **base-rate context** for interpreting one specific finding (the landmark violations), never as findings against this component.

No Playwright spec results, no `agent-browser` traces, no `virtual-screen-reader` logs, and no contrast-meter output were supplied for this component; where a claim benefits from that kind of measurement and it wasn't available, I've flagged it as an Open Question rather than asserting it as fact.

## Phase 1 — Pre-commitment Predictions

Before granular line-by-line audit, predictions for a static long-form article/content component of this shape:

1. The heading hierarchy will skip a level somewhere in the outline — CMS/blog templates frequently hardcode heading tags to a visual weight rather than to true document position.
2. If a skip exists, it will likely be invisible to a sighted skim, because font-size steps for headings usually still read as a coherent visual scale even when the underlying semantic levels are wrong.
3. Landmark/region structure will likely be incomplete (no `<main>`) — single-component fixture pages of this kind are commonly rendered outside a full page shell.
4. Because no interactive elements are present, the ARIA Pattern Compliance, Focus Management, and State Communication phases will most likely return "not applicable" rather than findings.
5. The "Accessibility Features Present" self-checklist ("✓ Semantic heading elements," "✓ No headings for visual styling only") asserts heading *element choice* only — I expect it to be technically true but silent on heading *order* and *completeness*, which is where I expect the real defects to live.

## Phase 2 — Semantic HTML Audit

**Structure read directly from source** (component code as supplied):

```
line 10  <article className="blog-post">
line 11  <h1>Introduction to Web Accessibility</h1>
line 13  <h3>Why Accessibility Matters</h3>          ← level jumps 1→3
line 14  <p>...</p>
line 19  <h3>WCAG Guidelines</h3>
line 20  <p>...</p>
line 22  <h3>Common Issues</h3>
line 23  <ul><li>...</li><li>...</li><li>...</li></ul>
line 29  <h3>Getting Started</h3>                    ← no content follows
line 31  <h2>Tools and Resources</h2>                 ← immediately next node
line 32  <p>...</p>
line 34  <h2>Conclusion</h2>
line 35  <p>...</p>
line 36  </article>
```

**Finding A — Heading level skips from H1 to H3 (four sibling sections mis-nested).**
The document opens with one `<h1>` and then four consecutive `<h3>` siblings ("Why Accessibility Matters," "WCAG Guidelines," "Common Issues," "Getting Started") with **no `<h2>` anywhere before them**. Two `<h2>` elements ("Tools and Resources," "Conclusion") appear only afterward. Confirmed independently by two sources:
- Axe-core `heading-order` violation (impact: moderate in axe's own taxonomy — see calibration note in Phase 8), `sample_selectors: ["h3:nth-child(2)"]`, `node_count: 1`.
- SR census: index 3 (`"heading, Introduction to Web Accessibility, level 1"`) is followed directly by index 4 (`"heading, Why Accessibility Matters, level 3"`) — no level-2 heading between them anywhere in the 33-entry trace.

Axe's `heading-order` rule only flags *increases* greater than one step, so it reports exactly one violating node (the first `h3`) even though the defect's real footprint is all four `<h3>` siblings, none of which has a valid `<h2>` parent. Automated tooling under-counts the scope of this defect; the design review does not.

**Finding B — "Getting Started" is a heading with no content.**
Source lines 29–31 show `<h3>Getting Started</h3>` immediately followed by `<h2>Tools and Resources</h2>` with nothing in between — no paragraph, no list, no text node. The SR census independently confirms this at the DOM/AT-facing layer: index 24 (`"heading, Getting Started, level 3"`) is followed directly by index 25 (`"heading, Tools and Resources, level 2"`) with zero intervening content entries — every other heading in the trace (indices 4, 8, 12) is followed by a `paragraph`/`list` entry before the next heading; "Getting Started" is the one exception. This is a genuine content/structure gap, not a hierarchy-numbering issue: the heading promises a section that never arrives.

**Everything else in the semantic audit is clean, and I want to say so plainly rather than bury it:**
- No `div`/`span` is used in place of a native element anywhere. `<article>`, `<h1>`–`<h3>`, `<p>`, `<ul>`/`<li>` are all correctly chosen native elements. There is zero ARIA in this component, so there is nothing "replacing" native semantics (the protocol's non-negotiable native-HTML-first rule) — it simply isn't at risk here.
- The list ("Common Issues") uses real `<ul>`/`<li>`, not divs styled as a list. Confirmed against source and against the SR census (`role: list` / `role: listitem` with correct `position`/`set size` announcements at indices 13–23).
- No layout tables, no data tables, no form inputs, no images — the corresponding checks in this phase (layout-table `role="presentation"`, table `scope`, label association, alt text) are not applicable; there is nothing of that kind in this component.
- **Text contrast — independently verified, not assumed.** Using the WCAG relative-luminance formula against the CSS actually supplied (lines 46–72):
  - Body text `#333` on white: ≈ 12.6:1 (needs 4.5:1) — passes comfortably.
  - `h3` text `#666` on white, 18px: 18px bold is *just under* the 18.66px WCAG "large text" threshold, so I checked it against the stricter 4.5:1 normal-text bar rather than the 3:1 large-text bar. Measured ≈ 5.7:1 — still passes.
  - `h1`/`h2` text `#0066cc` on white, 32px/24px (both qualify as large text, 3:1 bar): measured ≈ 5.6:1 — passes with large margin even against the stricter 4.5:1.
  No color-contrast finding for this component's own scan supports a violation either — consistent with the math above.
- The self-reported checklist ("✓ Semantic heading elements," "✓ No headings for visual styling only") is *true but incomplete*: both claims are about which tag was chosen, and both are correct choices. Neither claim addresses whether the tags are in the right *order* or whether every heading has content — which is exactly where the two real defects above live. Treat this checklist as verified-for-element-choice only, not as evidence the heading structure as a whole is sound.

## Phase 3 — ARIA Pattern Compliance Audit

Not applicable. There is no interactive widget in this component — no tabs, menu, disclosure, combobox, dialog, or toggle. Zero ARIA attributes appear anywhere in the source, and the SR census confirms `declared_broken_aria_refs: []`. There is no WAI-ARIA APG pattern to check compliance against because none is invoked. Recording this explicitly rather than silently skipping it, per the gap-analysis discipline this protocol requires: **absence of ARIA here is correct, not a gap** — a static article has no reason to carry any.

## Phase 4 — Focus Management Review

Not applicable in the traditional sense — there is no modal, drawer, dropdown, roving-tabindex widget, or dynamic content region in this component, so there is no focus trap, restoration, or roving-tabindex behavior to evaluate. There are also no natively focusable elements inside the `<article>` at all (no links, buttons, or inputs), so there is nothing for a keyboard user to tab into or get stuck on within this component's boundary. This is a clean, correct absence: a static content region with no focus-affecting behavior needed. No findings.

## Phase 5 — State Communication Audit

Not applicable. No loading state, no error state, no success/confirmation feedback, no disabled/readonly control, no selected/checked/expanded toggle, no visual-only status indicator, no live region. `declared_live_regions: []` in the SR census confirms no live-region behavior exists to audit. No findings.

## Phase 6 — Multi-Perspective Review

**Screen reader user (NVDA, JAWS, VoiceOver).** This is where both real defects land. A screen reader user building a mental map of the article via the headings list/rotor sees: H1 → H3 → H3 → H3 → H3 → H2 → H2. Four sections that are actually top-level companions to "Tools and Resources" and "Conclusion" present themselves as third-level sub-subsections of nothing, because no H2 ever opens for them to nest under. Worse, one of those four ("Getting Started") announces itself and then immediately hands control to the next heading with no content read in between — a screen reader user has no way to tell, in the moment, whether that's a genuine empty section or their AT skipping content. Both are measured, not inferred (axe `heading-order` + two independent SR-census gaps).

**Keyboard-only user.** Clean. There is nothing focusable inside this component, so there is no tab order to evaluate, no trap possible, and no keyboard interaction to break. A keyboard user reading this content via Tab/arrow-key/say-all navigation on the surrounding page reads exactly the same linear content a mouse user would — the defects above are a *structural-map* problem for screen reader users specifically (heading-level navigation), not a keyboard-operability problem.

**Low vision user (200% zoom, high contrast).** No zoom/reflow or Windows High Contrast Mode measurement was supplied in this evidence pack, so I'm not asserting a verdict here — flagged in Open Questions instead. What I *can* verify from the CSS given: `.blog-post` uses `max-width: 800px` with `margin: 20px auto` and no fixed-width children, which is reflow-friendly by construction (no obvious horizontal-scroll trap), and all three text colors pass contrast with real margin (see Phase 2 math). One perspective-relevant observation worth naming: the visual size hierarchy (32px → 18px → 18px → 18px → 18px → 24px → 24px) still reads as a plausible-looking scale to a sighted skimmer — nothing about the *visual* presentation screams "broken hierarchy." That's precisely why this class of defect ships: it is invisible to visual QA and only surfaces in the AT-facing heading model.

**Cognitive accessibility.** The same structural defect has a cognitive dimension independent of assistive technology: any reader — sighted or not — who scans the headings to build a table of contents in their head will misjudge how many "chapters" the article has, and anyone who specifically looks for a "Getting Started" section will find a dead end. No forms, timeouts, or destructive actions exist in this component, so the rest of this perspective's checklist doesn't apply.

**Vestibular & motion.** No animation, transition, or auto-playing content anywhere in this component. Not relevant.

**Auditory access.** No audio or video elements. Not relevant.

**Environmental contrast.** Text contrast checked and passes across all three colors used (see Phase 2). No UI-component boundaries exist to check (no buttons/inputs). Color is never the sole differentiator of anything here — headings differ by size, weight, and position, not color alone.

### Perspective Alarm Table

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Two independently measured structural defects (heading-order skip; empty "Getting Started" section) that corrupt the heading-based navigation model this user group relies on most heavily for long-form content. |
| Keyboard-only | LOW | No focusable elements inside the component; nothing to break. |
| Low vision | MEDIUM | Contrast independently verified and passing; no zoom/reflow/HCM measurement supplied to close out the rest of the perspective. |
| Cognitive | MEDIUM | Same heading defects create a real risk of a false or dead-end mental outline for any reader who scans by headings, not only AT users. |
| Vestibular & motion | LOW | No animation or auto-playing content present. |
| Auditory access | LOW | No audio/video media present. |
| Environmental contrast | LOW | Text contrast verified passing; no color-only indicators; no UI-boundary elements to assess. |

Screen reader is flagged HIGH — per protocol this is a candidate for `/perspective-audit` escalation. I'd support that escalation given both findings are measured rather than speculative.

## Phase 7 — Gap Analysis (What's Missing)

- **Missing H2 level for four sections.** "Why Accessibility Matters," "WCAG Guidelines," "Common Issues," and "Getting Started" have no parent H2 anywhere in the document — this is the direct cause of Finding A.
- **Missing body content under "Getting Started".** Finding B — the heading exists, its section does not.
- **Missing `<main>` landmark** (axe `landmark-one-main` + `region`, both moderate, on this exact page). See calibration note below — likely a shared fixture-harness characteristic rather than a BlogPost-specific gap, but reported rather than silently dropped.
- **Not present in this component, and correctly so:** no images (so no alt-text gap), no forms (so no label/error gap), no tables (so no scope gap), no dynamic content (so no live-region gap), no custom widgets (so no ARIA-completeness gap). Naming these as *correct absences* rather than skipping them silently.

**Known Anti-Patterns checklist (from the prior third-party audit)** — checked against all nine items: broadcast-vs-association, `title`-as-name, ARIA-without-visible-label, else-branch coverage, single-selector scope, `td`-in-loop row headers, `role="presentation"` misuse, decorative-alt conflation, missing DOM-verification on ARIA fixes. **None apply** — this component has no ARIA, no tables, no images, no branching JS logic, and no per-field loops to check. Confirmed by reading the full source, not assumed from absence of mention.

**Known False Positives checklist** — checked against all five listed patterns (noninteractive-element-interactions, `anchor-is-valid` on `<Link>`, transparent-background color-contrast, React-portal `region`, spread-prop `aria-allowed-attr`). **None apply** — no custom `role` props, no anchors, no gradient/transparent backgrounds behind text, no portals, no spread ARIA props anywhere in this component.

## Phase 8 — Realist Check (Severity Calibration)

**Finding A (heading skip) and Finding B (empty heading) — both calibrated to MAJOR, not CRITICAL:**
1. *Realistic worst case:* A screen reader user who navigates by heading level (per WebAIM's screen reader user surveys, this is consistently one of the most-used content-finding techniques) gets a false picture of the document's outline, and — for Finding B specifically — may reasonably wonder whether their AT missed content or is malfunctioning. Neither defect removes any content from the reading order; everything is still reachable linearly. That's why this doesn't meet CRITICAL's bar ("blocks access entirely") — nothing is blocked, the *map* of the content is wrong.
2. *User group impacted:* Screen reader users primarily; sighted users who scan by heading secondarily (cognitive dimension); keyboard-only and low-vision users are not meaningfully affected by either defect.
3. *Detection/fix speed:* Both are fast to detect (axe already caught Finding A; Finding B would surface in any manual heading-list walkthrough) and fast to fix (retag four elements; add or remove one section's content). Noted per protocol, but this doesn't change the severity rating — it's a mitigating operational fact, not a downgrade justification, since the *shipped* experience for an AT user hitting this before the fix lands is still a real, on-by-default degradation of standard navigation.
4. *Proportionality check:* Neither finding is being inflated by review momentum — I verified both hit their bar for "significantly degrades experience for a user category" (MAJOR) rather than "friction with an easy workaround" (MINOR), because there is no workaround for heading-navigation users short of not using headings at all, which defeats the purpose of the affordance.
Both findings survive all four questions unchanged. **Recalibration note:** axe's own `heading-order` impact tag is "moderate" — that is axe's internal triage scale for a generic best-practice rule, not a substitute for user-impact calibration. I deliberately did not inherit axe's tag as the severity; MAJOR reflects independent calibration against actual heading-navigation usage patterns.

**Landmark / region findings — calibrated down to ENHANCEMENT, with an explicit harness-artifact caveat:**
Cross-referencing the sixteen sibling axe scans in the same evidence batch (used only as base-rate context, never as findings against this component — see Phase 0): **14 of the 16** sibling fixtures in this same batch also trigger `landmark-one-main` and/or `region` (`accordion-no-region-role`, `async-form-vague-success`, `breadcrumb-navigation-no-nav-landmark`, `checkbox-group-no-fieldset`, `combobox-autocomplete-no-listbox-role`, `dashboard-heading-inconsistency`, `data-table-missing-scope`, `expandable-section-no-button`, `file-input-no-labels`, `form-field-vs-summary-errors`, `form-validation-missing-aria-describedby`, `image-carousel-no-region`, `infinite-scroll-no-announcement`, `interactive-dropdown-clean`, `interactive-dropdown-focus-bug`). Only `button-skip-link-clean` and `app-focus-order-illogical` do not. That overwhelming shared pattern is much better explained by a single-component-per-page test harness that doesn't wrap fixtures in a `<main>`-bearing page shell than by seventeen unrelated components independently making the same authoring mistake. `button-skip-link-clean`'s clean result shows the harness *can* render a fixture with proper landmarks when the fixture's own markup includes one — so this isn't a certainty, but it is a strong enough signal to downgrade confidence and severity rather than treat this as a BlogPost-specific defect. Reported as ENHANCEMENT ("best practice not met, but no access barrier" — content is still reachable via heading nav or linear reading) with an explicit developer-verification ask, not suppressed.

## Phase 9 — Self-Audit

| Finding | Confidence | Could developer immediately refute with context I lack? | Gap or preference? |
|---|---|---|---|
| A — H1→H3 skip, 4 sections mis-nested | HIGH | No — confirmed by axe AND independent SR-census trace, both measured against this exact page | GAP |
| B — "Getting Started" empty section | HIGH on the *what* (confirmed by source + SR census); MEDIUM on the *why* (intentional placeholder vs. accidental content loss — moved to Open Questions) | Partially — a developer could say "not written yet," which doesn't refute that the shipped defect is real | GAP |
| Landmark-one-main / region | MEDIUM (see harness-artifact caveat) | Yes, plausibly — "this only renders standalone in the eval harness; production wraps it in `<main>`" | Leaning toward artifact, not a design GAP — kept as ENHANCEMENT with explicit verification ask rather than dropped, since I can't confirm the refutation myself |

No LOW-confidence CRITICAL/MAJOR findings were generated, so nothing needed to be moved out of the scored findings on confidence grounds alone. The landmark item is the one finding I actively down-weighted based on cross-evidence reasoning rather than gut feel.

## Phase 10 — Synthesis

Comparing against Phase 1 predictions: predictions 1, 2, 4, and 5 landed exactly — there is a heading skip, it is visually unremarkable, the ARIA/focus/state phases were correctly empty, and the self-reported checklist was indeed true-but-incomplete. Prediction 3 (missing landmark) was confirmed as an axe finding but with a wrinkle the prediction didn't anticipate: cross-referencing the other 16 fixtures in the same batch turned a plain "missing `<main>`" finding into a much better-calibrated "likely shared test-harness characteristic, verify against the real template" finding.

One finding was **not** anticipated by the pre-commitment list at all: Finding B, the entirely empty "Getting Started" section. This is a distinct defect from the pure heading-level skip (Finding A) — a content-completeness gap, not a numbering gap — and it was only caught because the SR census's raw trace made it possible to check for adjacent-heading-with-no-content-between, not because I predicted to look for it. Worth naming explicitly: this is the kind of gap generic "check the heading order" pattern-matching would have missed, and it took reading the actual step-by-step trace facts (not a summary of them) to surface.

---

**VERDICT: REVISE**

**Overall Assessment**: BlogPost's markup avoids every classic anti-pattern this critic watches for — no `div`-as-button, no ARIA papering over bad semantics (there is no ARIA at all, correctly), correct list markup, and text contrast that independently checks out on every color used. But the heading structure carries two independent, measured defects: four top-level sections are nested a level too deep with no `<h2>` parent, and one of those four ("Getting Started") has no body content before the next heading fires. Both are invisible to a sighted skim — the visual size scale still reads coherently — which is exactly why they need a design review, not just a visual QA pass, to surface. A separate landmark/region axe finding is present but most likely reflects the isolated single-fixture test harness rather than BlogPost's own design, given 14 of 16 sibling fixtures in the same evidence batch show the identical pattern.

**Pre-commitment Predictions**: Predicted a heading-level skip that would be visually invisible, a missing `<main>` landmark, and "not applicable" outcomes for ARIA/focus/state review given no interactive elements — all confirmed. Not predicted, and found only by reading the SR-census trace directly: the "Getting Started" heading has zero content before the next heading, a completeness defect distinct from the level-skip itself.

**Critical Findings** (blocks access): None. Neither structural defect removes any content from the reading order or traps any user — see Phase 8 for why these were calibrated to MAJOR rather than CRITICAL.

**Major Findings** (significantly degrades experience):

1. **Heading levels skip from H1 directly to H3, mis-nesting four sibling sections.** Component source, lines 11–29: `<h1>Introduction to Web Accessibility</h1>` is followed by four consecutive `<h3>` elements ("Why Accessibility Matters," "WCAG Guidelines," "Common Issues," "Getting Started") with no `<h2>` anywhere before them; `<h2>` only appears afterward ("Tools and Resources," line 31; "Conclusion," line 34).
   - Confidence: HIGH
   - Why this matters: Screen reader users building a heading-list mental map of the page (one of the most common navigation techniques for long-form content) see four sections falsely presented as third-level sub-subsections of nothing, because no second level ever opens. Automated tooling (axe `heading-order`) only flags the first jump as a single node — the design defect's real scope is all four siblings.
   - Fix: Promote the four `<h3>` elements to `<h2>`, matching the sibling level of "Tools and Resources" and "Conclusion." This produces a flat, valid H1 → H2×6 structure with no further changes needed.

   ```
   ### A11y Evidence Finding
   finding_id: heading-hierarchy-skip-h1-to-h3
   fingerprint: 3f7a9c1e0b2d4a6f
   source: evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/013-127-0-0-1-8777-heading-hierarchy-skipped-html.json (rule: heading-order); evals/results/context-utilization-phase3/raw/heading-hierarchy-skipped-kat-census/sr-census.json (entries index 3-4, 8, 12, 24)
   wcag_or_apg: WCAG 1.3.1 Info and Relationships
   section_508_fpc_context: not in scope (component-level review, no declared 508 audit scope)
   severity: MAJOR
   perspective_alarms: screen_reader=HIGH, cognitive=MEDIUM, keyboard=LOW, low_vision=MEDIUM
   evidence: axe heading-order violation, impact "moderate" (axe's own scale), selector h3:nth-child(2), node_count 1; SR census index 3 ("heading, Introduction to Web Accessibility, level 1") directly followed by index 4 ("heading, Why Accessibility Matters, level 3") with no level-2 heading anywhere before indices 4, 8, 12, or 24
   reproduction_steps: Load heading-hierarchy-skipped.html; open a screen reader headings list (NVDA Insert+F7, VoiceOver rotor "Headings"); read the outline top to bottom
   expected_behavior: Heading levels increase by exactly one at each nesting step (WCAG 1.3.1); the four sections should appear as H2 siblings, not H3 orphans
   actual_behavior: Four sibling sections are marked H3 directly under H1 with no intervening H2
   trend: new
   ```

2. **"Getting Started" heading has no associated content.** Component source, lines 29–31: `<h3>Getting Started</h3>` is immediately followed by `<h2>Tools and Resources</h2>` with no paragraph, list, or other content between them.
   - Confidence: HIGH on the observed defect; MEDIUM on root cause (see Open Questions)
   - Why this matters: A screen reader user who navigates to this heading gets zero information before the next heading fires — indistinguishable, in the moment, from AT malfunction or missed content. Confirmed independently at the AT-facing layer: SR census index 24 ("heading, Getting Started, level 3") is followed directly by index 25 ("heading, Tools and Resources, level 2") with no intervening `paragraph`/`list` entry — the only heading in the entire 33-entry trace with this property.
   - Fix: Either restore the intended body content for this section, or remove the heading entirely if no content was ever planned for it. Independent of, and in addition to, Finding 1's level fix.

   ```
   ### A11y Evidence Finding
   finding_id: heading-getting-started-empty-section
   fingerprint: 8e2c5b9f1a4d7036
   source: evals/results/context-utilization-phase3/raw/heading-hierarchy-skipped-kat-census/sr-census.json (entries index 24-25); corroborated by component source lines 29-31
   wcag_or_apg: WCAG 1.3.1 Info and Relationships
   section_508_fpc_context: not in scope (component-level review, no declared 508 audit scope)
   severity: MAJOR
   perspective_alarms: screen_reader=HIGH, cognitive=MEDIUM, keyboard=LOW, low_vision=LOW
   evidence: SR census index 24 ("heading, Getting Started, level 3") immediately followed by index 25 ("heading, Tools and Resources, level 2") with zero intervening content entries; source shows no <p>, <ul>, or text node between line 29 and line 31
   reproduction_steps: Navigate by heading to "Getting Started" (screen reader "H" key or headings rotor); continue to the next heading; observe no content is announced in between
   expected_behavior: A heading introduces content that follows it before the next heading fires (WCAG 1.3.1)
   actual_behavior: "Getting Started" has no body content; the section is empty
   trend: new
   ```

**Minor Findings** (friction but workaround exists): None at MINOR — the remaining finding (landmark/region) was calibrated to ENHANCEMENT rather than MINOR; see below and Phase 8.

**Enhancements** (best practice not met):
- **Missing `<main>` landmark** (axe `landmark-one-main` + `region`, both moderate, on this exact page: `evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/013-127-0-0-1-8777-heading-hierarchy-skipped-html.json`). Likely a shared characteristic of the isolated single-fixture test harness rather than a BlogPost-specific defect — 14 of the 16 sibling fixtures in the same batch show the identical pattern, while one sibling (`button-skip-link-clean`) does not, showing the harness can render clean landmarks when the fixture markup provides one. **Needs verification**: confirm whether BlogPost is normally mounted inside a page shell that already provides `<main>`; if so, this is not a real defect in this component.

**What's Missing** (gaps, unhandled edge cases, unstated assumptions):
- No `<h2>` exists to parent the four sections currently marked `<h3>` (Finding 1's root cause).
- No body content exists under "Getting Started" before the next heading (Finding 2).
- No `<main>` landmark wraps the article on this page (Enhancement above, scope-ambiguous).
- No 200%-zoom/reflow or Windows High Contrast Mode measurement was included in this evidence pack — the Low Vision alarm is rated on structural priors (verified color contrast, reflow-friendly CSS) rather than direct measurement.
- No site chrome/navigation is visible in this fixture, so skip-link/bypass-blocks assessment for repeated page regions is out of scope for this review — noted as an evidence gap, not asserted as a finding either way.
- Confirmed correct absences, not gaps: no ARIA (none needed), no focus management code (nothing to manage), no state communication (no state to communicate), no images/tables/forms (none present).

**Multi-Perspective Notes**:
- Screen reader user: The primary group affected by both MAJOR findings. Heading-list navigation — a mainstream technique for long-form content — returns a false outline (four orphaned H3s) and one dead-end section with no way to distinguish "empty by design" from "AT missed something."
- Keyboard-only user: Unaffected. No focusable elements exist inside this component; there is no tab order, trap, or interaction to evaluate.
- Low vision user (200% zoom, high contrast): No measurement evidence supplied; structurally the CSS is reflow-friendly (no fixed-width children beyond a `max-width` container) and every text color independently checks out against WCAG contrast minimums (body `#333` ≈12.6:1, `h3` `#666` ≈5.7:1 checked against the stricter 4.5:1 bar, `h1`/`h2` `#0066cc` ≈5.6:1). Worth naming: the visual size hierarchy still looks coherent at a glance, which is exactly why this defect passes visual QA.
- Cognitive accessibility: Any reader scanning headings for orientation — sighted or not — risks the same false outline and the same dead end at "Getting Started" that affects screen reader users; this isn't an AT-exclusive cognitive load problem.

**Verdict Justification**: Two MAJOR findings with hard, cross-corroborated evidence (axe + independent SR-census trace) are enough to require REVISE rather than ACCEPT-WITH-RESERVATIONS — this isn't a stylistic nit, it's a measured break in the structural contract headings are supposed to provide. It stops short of REJECT because the underlying markup is otherwise sound (correct native elements throughout, no ARIA misuse because there is no ARIA to misuse, verified passing contrast, correct list semantics) and both fixes are narrow and mechanical: retag four elements to `<h2>`, and resolve one section's missing content. This would upgrade to ACCEPT-WITH-RESERVATIONS once those two fixes land, contingent on the landmark Enhancement being confirmed (or not) against the real page template. Screen reader is flagged HIGH on the perspective alarm table; escalation to `/perspective-audit` would be reasonable given both drivers are measured rather than speculative.

**Open Questions (unscored)**:
- Was "Getting Started" left intentionally content-less pending future copy, or was body content lost during an edit? The observable defect (empty section) stands regardless of the answer, but the answer determines whether the fix is "write the content" or "delete the heading."
- Is BlogPost normally rendered inside a page shell that already supplies a `<main>` landmark, making the `landmark-one-main`/`region` axe findings an artifact of this isolated test harness rather than a real production gap? The 14-of-16 sibling pattern makes this the more likely explanation, but it needs a developer check against the actual page template, not just this fixture.
- No 200%-zoom/reflow or Windows High Contrast Mode pass was included in the evidence pack — confirming one would let the Low Vision alarm move from MEDIUM (structural priors) to either LOW (confirmed clean) or a scored finding.
