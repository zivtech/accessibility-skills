# Accessibility Design Review — `BlogPost` (heading-hierarchy-skipped)

**VERDICT: REVISE**

**Overall Assessment**

This component is static prose with zero interactive elements, so its heading outline *is* its accessibility surface — and the outline is not merely skipped, it is inverted. The document declares `h1 → h3 → h3 → h3 → h3 → h2 → h2`. axe flags exactly one node for this (`heading-order` at `h3:nth-child(2)`), because axe's `heading-order` rule only penalizes level *increases* greater than one; a *decrease* from `h3` to `h2` is legal under the rule. So the automated scan reports 1 defective heading while 6 of the 7 headings sit at the wrong depth relative to each other. That gap between "1 moderate best-practice violation" and "the article's table of contents is a lie" is the entire reason this review exists.

The rest is clean and I am saying so with evidence, not politeness: reading order matches DOM order across all 33 census entries, the list is exposed with correct set-size, there are no broken ARIA references, no live regions are needed or missing, and axe measured zero contrast violations and zero contrast incompletes on this page.

---

## Phase 0 — Evidence Intake

**Prerequisite satisfied.** Automated scan evidence was supplied with the ask, so I am not blocking on the "have you run accessibility-testing first?" gate.

**Review type.** Fresh design pass, not a remediation. The a11y-test *Verification evidence contract* check (evidence-type mismatch on a claimed fix) therefore does not apply — there is no "before" state and no fix being asserted.

### In-scope artifacts (2 of 19)

| Artifact | Tier | What it establishes |
|---|---|---|
| `evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/013-127-0-0-1-8777-heading-hierarchy-skipped-html.json` | measured (axe-core 4.13.0, 1280×800, HTTP 200) | 3 violations (`heading-order`, `landmark-one-main`, `region`), all `moderate`, all `best-practice`-tagged. `incomplete: []`. 13 passes / 76 inapplicable. |
| `evals/results/context-utilization-phase3/raw/heading-hierarchy-skipped-kat-census/sr-census.json` | measured (keyboard-a11y-tester SR reading-order census, `truncated: false`) | 33-entry spoken-phrase sequence; `declared_live_regions: []`, `declared_broken_aria_refs: []`, `declared_alternate_reading_order: []`. |

### Out-of-scope artifacts (17 of 19) — explicitly not used as findings

The pack ships 17 axe scans for *different* fixture pages: `accordion-no-region-role`, `app-focus-order-illogical`, `async-form-vague-success`, `breadcrumb-navigation-no-nav-landmark`, `button-skip-link-clean`, `checkbox-group-no-fieldset`, `combobox-autocomplete-no-listbox-role`, `dashboard-heading-inconsistency`, `data-table-missing-scope`, `expandable-section-no-button`, `file-input-no-labels`, `form-field-vs-summary-errors`, `form-validation-missing-aria-describedby`, `image-carousel-no-region`, `infinite-scroll-no-announcement`, `interactive-dropdown-clean`, `interactive-dropdown-focus-bug`.

None of these describe the component under review. `target-size` on the carousel buttons, `label` on the file input, `aria-valid-attr-value` on the dropdowns, `bypass` on the breadcrumb page — **none of these are findings against `BlogPost`**, and importing any of them here would be fabrication, not thoroughness. They are cited below for exactly one legitimate purpose, and no other.

**Legitimate cross-artifact use — instrument liveness only.** The target page's short violation list could mean either "the page is nearly clean" or "the scan was degraded." The sibling rows settle it: the same batch, same axe version, same runner, fired `heading-order` on `dashboard-heading-inconsistency` (`.metric-card:nth-child(1) > h3`), `label` at `critical` impact on `file-input-no-labels`, `target-size` at `serious` on two pages, and `color-contrast` at `serious` on `dashboard-heading-inconsistency`. The rules that could have fired on a prose page were armed and firing elsewhere in the same run. Therefore the target's `violations: [3]` / `incomplete: []` reflects the page, not a broken scan. That is the only inference I draw from the sibling data, and it is an inference about the *instrument*, never about the component.

### keyboard-a11y-tester calibration rules applied

- **Rule 1 (batch-crawl 4.1.3 "silent live region" findings are prompts, not failures):** no 4.1.3 findings present. `declared_live_regions: []` is the *correct* state for static prose, not a defect. Not filed.
- **Rule 2 (name-presence checks miss UA-intrinsic names):** no form controls present. N/A.
- **Rule 3 (journey-level verdicts need their trace steps):** the pack contains a census only — no `trace.json`, no `deterministic-findings.json`. Every census entry I cite is a per-entry measured fact (index, spoken phrase, role, tag, selector). No journey-level verdict is available and none is asserted.
- **Rule 4 (`conformance_level` is a pass/fail gate, not the SC's WCAG level):** no findings file supplied. N/A.

### What the evidence pack does NOT contain

No keyboard trace, no focus-indicator measurement, no contrast ratio computed by AccessLint, no virtual-screen-reader component assertions, no Playwright spec results. Consequence: I have **no measured evidence about focus visibility or keyboard operability**. For this component that is moot — there are no focusable elements — but I am stating it rather than letting silence imply coverage.

---

## Phase 1 — Pre-commitment Predictions

Written before reading the source, from component type alone ("blog post / long-form static article"):

1. **Heading level chosen for visual weight rather than structure**, producing a skip. (Most common static-content defect.)
2. **Missing landmark** — content not inside `<main>`, and/or an `<article>` with no accessible name.
3. **Missing `lang` attribute** on the document root.
4. **Links in body copy distinguishable by color alone** (WCAG 1.4.1).
5. **No bypass mechanism / table of contents** for long-form reading.
6. **Images without `alt`** — an article *about* alt text is likely to contain figures.

Scored against reality in Phase 10.

---

## Phase 2 — Semantic HTML Audit

Reference frame: `BlogPost.jsx:N` = line N of the JSX block as supplied; `blog-post.css:N` = line N of the CSS block as supplied. No filesystem paths were provided with the fixture.

| Check | Result |
|---|---|
| Native elements vs. div+ARIA | **Clean.** Zero ARIA attributes in the component. Nothing is being masked. `<article>`, `<h1>`–`<h3>`, `<p>`, `<ul>`, `<li>` only. |
| `<article>` appropriate for a blog post | **Correct** (`BlogPost.jsx:3`). Census index 2 confirms role `article` is exposed. |
| List semantics | **Correct** (`BlogPost.jsx:16–20`). Census indices 13–23 confirm `list` → `listitem, level 1, position 1, set size 3` ×3 → `end of list`. Set size is announced accurately. |
| Tables | None. N/A. |
| Form labels | No form controls. N/A. |
| Heading hierarchy | **BROKEN.** See Major Finding 1. |
| Landmarks | `<article>` maps to role `article`, which is **not** a landmark. axe `region` fired on `#root`; `landmark-one-main` fired on `html`. Scope caveat below. |
| Hidden ARIA patching broken HTML | None present. |

**Heading sequence as authored and as spoken:**

| Source | Level | Census entry |
|---|---|---|
| `BlogPost.jsx:4` "Introduction to Web Accessibility" | h1 | index 3 — `heading, Introduction to Web Accessibility, level 1` |
| `BlogPost.jsx:6` "Why Accessibility Matters" | h3 | index 4 — `heading, Why Accessibility Matters, level 3` |
| `BlogPost.jsx:12` "WCAG Guidelines" | h3 | index 8 — `heading, WCAG Guidelines, level 3` |
| `BlogPost.jsx:15` "Common Issues" | h3 | index 12 — `heading, Common Issues, level 3` |
| `BlogPost.jsx:22` "Getting Started" | h3 | index 24 — `heading, Getting Started, level 3` |
| `BlogPost.jsx:24` "Tools and Resources" | h2 | index 25 — `heading, Tools and Resources, level 2` |
| `BlogPost.jsx:27` "Conclusion" | h2 | index 29 — `heading, Conclusion, level 2` |

The census is the hard evidence here: it is not my reading of the JSX, it is the measured spoken output.

---

## Phase 3 — ARIA Pattern Compliance Audit

**No interactive widgets exist in this component.** No tabs, menus, disclosure, combobox, dialog, toggle, or listbox. No `role`, no `aria-*`, no `tabindex` anywhere in `BlogPost.jsx:1–33`.

There is therefore no APG pattern to be 80% complete. `declared_broken_aria_refs: []` in the census confirms no dangling `aria-labelledby` / `aria-describedby` / `aria-controls` references exist to be checked.

**This is a clean result, not an unexamined one.** The correct finding for this phase is: nothing to report, and the absence of ARIA on static prose is the right call, not an omission. Native HTML first is satisfied by construction.

---

## Phase 4 — Focus Management Review

**No focusable elements exist.** No `<a>`, `<button>`, `<input>`, `<select>`, `<textarea>`, no `tabindex`, no `contenteditable`. The census's 33 entries contain zero interactive roles.

Consequences, each verified rather than assumed:

- Tab order: trivially correct — Tab passes through the component without stopping.
- Keyboard trap (2.1.2): impossible; nothing receives focus.
- Focus restoration / focus trap: no dynamic content, no modal, no route change. N/A.
- Focus visible (2.4.7) / Focus appearance (2.4.13) / Focus not obscured (2.4.11): **unmeasured and unmeasurable here** — no focusable target exists. I am not asserting pass or fail.
- Skip link / bypass (2.4.1): page-shell concern, and at seven short sections there is no repeated block to bypass. Not filed — filing it would be manufactured.

A screen-reader user *does* navigate this component, but by heading and browse mode, not by focus. That is why the whole weight of this review lands in Phases 2 and 6, not here.

---

## Phase 5 — State Communication Audit

There is no state. No loading, error, success, selected, expanded, checked, disabled, or readonly condition exists in `BlogPost.jsx:1–33` — the component is a pure render with no props, no hooks, no event handlers.

- `aria-live` / `role="status"`: correctly absent. `declared_live_regions: []` confirms none is declared, and none is needed. Per KAT calibration rule 1, I am not converting that empty array into a 4.1.3 finding.
- Visual-text-symbol state indicators (`+`/`−`/`×`/`>`): none present.
- Color-as-sole-indicator: the h3/h2 color split (`#666` vs `#0066cc`) is decorative, not semantic — it does not encode status. Not a 1.4.1 issue.

**Nothing to report. That is a real result.**

---

## Findings

### Critical Findings (blocks access)

**None.** All content in this component is reachable and readable by every user group. The census proves linear traversal delivers all 33 entries in DOM order. I considered and rejected inflating the heading defect to CRITICAL — see Phase 8.

---

### Major Findings (significantly degrades experience)

#### MAJOR-1 — Heading outline is inverted, not merely skipped: four sections are orphaned under a level that does not exist

**Evidence.** `BlogPost.jsx:4, 6, 12, 15, 22, 24, 27`. Authored sequence `h1, h3, h3, h3, h3, h2, h2`.

- Measured (axe): `heading-order`, impact `moderate`, `node_count: 1`, `sample_selectors: ["h3:nth-child(2)"]` — that selector resolves to `BlogPost.jsx:6` "Why Accessibility Matters", the first h3.
- Measured (census): index 3 `level 1` → index 4 `level 3`, adjacent, nothing between. And index 24 `heading, Getting Started, level 3` → index 25 `heading, Tools and Resources, level 2`, adjacent.

**Why axe under-reports this by a factor of six.** The `heading-order` rule penalizes an increase of more than one level. `h1 → h3` is such an increase, so it fires once. `h3 → h2` is a *decrease*, which the rule permits unconditionally. So the four orphaned `h3`s and the two trailing `h2`s that retroactively claim them as children are entirely invisible to the scanner. A team triaging on axe output alone would change one heading and believe the page fixed.

**User group impacted.** Screen reader users primarily; secondarily any user relying on a generated document outline (browser reader modes, extension outliners, "jump to heading" in reading apps).

**What actually happens.** In NVDA's elements list (Insert+F7) or JAWS's headings list, the outline renders as:

```
1  Introduction to Web Accessibility
   3  Why Accessibility Matters
   3  WCAG Guidelines
   3  Common Issues
   3  Getting Started
   2  Tools and Resources
   2  Conclusion
```

Two concrete failures follow:

1. A user pressing `2` from the top of the document to survey the article's top-level sections lands on **"Tools and Resources"** — silently skipping more than half the article, including its entire substantive body. Nothing tells them content was skipped.
2. A user reading the outline top-to-bottom must infer that "Why Accessibility Matters" through "Getting Started" are subsections of a level-2 section that was never announced. Then "Tools and Resources" arrives at level 2 *after* them, which reads as though those four were its children — while in document order they precede it. The structure the headings communicate contradicts the structure the content has.

**WCAG grounding.** 1.3.1 Info and Relationships (Level A) — the structural relationships conveyed programmatically must match those conveyed visually and in the content. Also relevant: 2.4.6 Headings and Labels (AA) — headings must describe topic *or purpose*, and a heading's level is part of its purpose; and 2.4.10 Section Headings (AAA, informative here).

**Fix (recommended).** Promote all four `h3`s to `h2` — `BlogPost.jsx:6, 12, 15, 22`. Resulting outline: `h1` with six `h2` siblings, which matches the article's actual flat structure. No CSS change is required for correctness, but see MINOR-1: the h2 rule (`blog-post.css:15–20`) will now apply its 24px/`#0066cc` treatment to all six, which is the honest visual consequence of the correct structure.

**Fix (alternative, only if the first four are genuinely subordinate).** Insert a real `h2` parent above `BlogPost.jsx:6` (e.g. "Background") and keep the four at `h3`. This is only correct if the author intends those four as children of one named section — nothing in the content suggests they are.

**Verification required.** Re-run *the same two instruments*: axe `heading-order` must report zero nodes, and the census heading levels must read `1, 2, 2, 2, 2, 2, 2`. A screenshot or a visual diff is not acceptable evidence for this fix — the defect is entirely in the accessibility tree.

- **Confidence: HIGH** — measured by two independent instruments.
- **Could the developer refute this with context I lack?** NO. There is no framing under which `h1 → h3 → … → h2` is the intended outline of this content.
- **GAP, not PREFERENCE.**

```
### A11y Evidence Finding
finding_id: blogpost-heading-outline-inverted
fingerprint: not-computed — stable input is sha1("heading-order|h3:nth-child(2)|http://127.0.0.1:8777/heading-hierarchy-skipped.html"); this review had no shell access, so the digest is stated as a recipe rather than invented
source: axe-core 4.13.0 rule `heading-order` (013-127-0-0-1-8777-heading-hierarchy-skipped-html.json) + keyboard-a11y-tester sr-census.json indices 3, 4, 8, 12, 24, 25, 29
wcag_or_apg: WCAG 2.2 SC 1.3.1 Info and Relationships (Level A); supporting SC 2.4.6 Headings and Labels (AA)
section_508_fpc_context: In scope if the project declares Revised Section 508 — 1.3.1 is WCAG 2.0 Level A and therefore inside the federal floor. This project's declared target is WCAG 2.2 AA; no 508 declaration was supplied with this ask, so treat the 508 line as context, not as a filed federal failure.
severity: MAJOR
perspective_alarms: screen-reader=HIGH, cognitive=MEDIUM, keyboard=LOW, low-vision=LOW, vestibular=LOW, auditory=LOW, environmental-contrast=LOW
evidence: BlogPost.jsx:4,6,12,15,22,24,27 — authored h1,h3,h3,h3,h3,h2,h2. axe: heading-order, impact moderate, node_count 1, selector "h3:nth-child(2)". census: index 3 "heading, Introduction to Web Accessibility, level 1" immediately followed by index 4 "heading, Why Accessibility Matters, level 3"; index 24 "heading, Getting Started, level 3" immediately followed by index 25 "heading, Tools and Resources, level 2".
reproduction_steps: 1) Load http://127.0.0.1:8777/heading-hierarchy-skipped.html in NVDA or VoiceOver. 2) Open the headings list (NVDA Insert+F7 / VO+U → Headings). 3) Observe the level-1 entry is followed directly by four level-3 entries and then two level-2 entries. 4) From the top of the document press "2" to jump to the next level-2 heading — focus lands on "Tools and Resources", skipping four sections.
expected_behavior: Heading levels descend by at most one and every heading's level reflects its true depth in the document. Jumping by level-2 headings surveys all top-level sections of the article.
actual_behavior: Level jumps 1→3. Four sections sit at level 3 with no level-2 parent. Two level-2 headings appear after them, implying a parent-child relationship that contradicts document order. Level-2 navigation skips the majority of the article without notice.
trend: new
```

*Contract note: this block is deliberately incomplete on one field. `fingerprint` requires a computed hex digest and I had no shell access; emitting a plausible-looking hex string would silently corrupt trend tracking for every future run that tried to match it. The recipe is stated so the value can be computed and backfilled.*

---

#### MAJOR-2 — Heading levels appear to have been selected for their visual treatment, contradicting the fixture's own accessibility claim

**Evidence.** `blog-post.css:9–13` (h1: 32px, `#0066cc`), `blog-post.css:15–20` (h2: 24px, `#0066cc`), `blog-post.css:22–27` (h3: 18px, `#666`). The submitted "Accessibility Features Present" list asserts "✓ No headings for visual styling only."

**The claim does not survive the CSS.** The h3 rule is the only heading rule that changes *color* as well as size — grey `#666` against the blue `#0066cc` shared by h1 and h2. So the level split is not "big / medium / small"; it is "blue and prominent" versus "grey and quiet." The four sections the author wanted to render quietly are exactly the four marked `h3`, and the two they wanted to render prominently are exactly the two marked `h2` — despite the quiet ones carrying the article's substance and the prominent ones being its closing matter. The most parsimonious explanation for `h1, h3, h3, h3, h3, h2, h2` is that levels were chosen by appearance, not by structure.

This matters more than MAJOR-1's mechanics, because it predicts the *wrong fix*. A team that believes "no headings are used for visual styling here" will read MAJOR-1 as a typo, patch one tag, and reintroduce the pattern on the next article. The correct remediation is to decouple heading level from visual weight — add a utility class (e.g. `.section-head--quiet`) for the grey/18px treatment and apply it to `h2` elements where the visual de-emphasis is genuinely wanted.

**User group impacted.** Screen reader and outline-dependent users take the direct hit. Cognitive-accessibility users take a secondary hit: the visual hierarchy and the programmatic hierarchy *agree with each other and are both wrong*, so there is no cross-check available to any user. This is worse than the usual "visual says one thing, code says another" mismatch — there is no correct signal anywhere in the artifact.

**WCAG grounding.** 1.3.1 Info and Relationships (A) — structure must be programmatically determinable and must reflect actual relationships, not presentation. WCAG technique F2 (failure due to using changes in text presentation to convey information without the corresponding structure) is the named failure mode.

**Fix.** Promote the four `h3`s per MAJOR-1, then restore the intended grey/18px look with a presentational class rather than a level change:

```css
.blog-post h2.section-head--quiet { font-size: 18px; color: #666; }
```

Verify `#666` on the page background still measures ≥ 4.5:1 after any background change (it is currently clean — see Enhancements).

- **Confidence: MEDIUM** — the CSS and the level sequence together make this the strongest available explanation, but authorial intent is an inference, not a measurement. I am filing it because the *remediation guidance* changes materially depending on which explanation is true, and because the fixture asserts the opposite as a fact.
- **Could the developer refute this with context I lack?** PARTIALLY — they could say the levels were a straightforward mistake and the CSS coincidence means nothing. That refutation still requires the same fix, and still leaves the fixture's "✓ No headings for visual styling only" claim unsupported.
- **GAP, not PREFERENCE.**

```
### A11y Evidence Finding
finding_id: blogpost-heading-level-selected-by-appearance
fingerprint: not-computed — stable input is sha1("F2-presentation-as-structure|.blog-post h3|http://127.0.0.1:8777/heading-hierarchy-skipped.html"); digest withheld rather than invented, per the note above
source: BlogPost.jsx:4,6,12,15,22,24,27 read against blog-post.css:9-13,15-20,22-27; corroborated by axe heading-order node and census levels
wcag_or_apg: WCAG 2.2 SC 1.3.1 Info and Relationships (Level A); WCAG failure technique F2
section_508_fpc_context: Same as MAJOR-1 — 1.3.1 is inside the WCAG 2.0 A/AA federal floor if a 508 scope is declared; none was declared for this ask.
severity: MAJOR
perspective_alarms: screen-reader=HIGH, cognitive=MEDIUM, low-vision=LOW, keyboard=LOW, vestibular=LOW, auditory=LOW, environmental-contrast=LOW
evidence: blog-post.css:22-27 is the only heading rule that changes color (#666) as well as size (18px); h1 and h2 share #0066cc. The four headings carrying the article's substance are the four styled quietly and marked h3; the two closing headings are styled prominently and marked h2. The submitted feature list claims "No headings for visual styling only."
reproduction_steps: 1) Read BlogPost.jsx heading sequence: h1,h3,h3,h3,h3,h2,h2. 2) Read blog-post.css heading rules and note the h3-only color change. 3) Correlate: level assignment tracks intended visual weight, not document depth.
expected_behavior: Heading level is chosen from document structure; visual weight is applied independently via CSS class.
actual_behavior: Heading level covaries with the intended visual treatment; the remediation the team will infer from an axe-only report ("change one h3") does not address the cause.
trend: new
```

---

### Minor Findings (friction, workaround exists)

**MINOR-1 — "Getting Started" heading labels a section with no content.**
`BlogPost.jsx:22`. Census confirms it as-rendered: index 24 `heading, Getting Started, level 3` is immediately followed by index 25 `heading, Tools and Resources, level 2` — zero entries between them.

A heading is a programmatic promise that a section follows. Here it does not. A screen reader user who jumps to "Getting Started" from the headings list arrives, hears the next heading, and must work out whether content failed to load, was skipped, or never existed. WCAG 1.3.1.

**Why MINOR and not MAJOR:** a sighted user hits the identical wall — the harm is not disproportionately borne by any assistive-technology user, and the fix is a content edit rather than a markup one. The disproportion that does exist (an SR user spends a navigation stop to discover the emptiness, where a sighted user sees it at a glance) is real but small.

**Needs user verification.** Both visible paragraphs in this fixture are elided with `...` (`BlogPost.jsx:13, 25`), so the source is plainly abridged. If "Getting Started" lost its body to the same abridgement, this is a fixture artifact and not a defect in the real component. Check against the unabridged source before filing a ticket. If the section is genuinely empty in production, either add its content or remove the heading.

**MINOR-2 — `<article>` has no accessible name.**
`BlogPost.jsx:3`. Census index 2 is spoken as bare `"article"` — role announced, name absent. Screen reader users encountering the region in a document containing more than one article (an index page, a feed, a related-posts rail) cannot tell them apart. Fix: `<h1 id="post-title">` at `BlogPost.jsx:4` and `<article className="blog-post" aria-labelledby="post-title">` at `:3`. The `id` must be unique per rendered instance — if this component is ever rendered more than once on a page, derive it from the post slug rather than hardcoding. WCAG 1.3.1 / 4.1.2.

---

### Enhancements (best practice, no access barrier)

- **Heading font sizes are absolute px** (`blog-post.css:10, 16, 23`). Browser *zoom* scales px normally, so SC 1.4.4 Resize Text is met and this is not a finding. But px ignores a user's configured default font size, which is a distinct preference from zoom and is the one many low-vision users actually set. `rem` would honor both. Enhancement only — I am explicitly not inflating this.
- **`line-height: 1.6`** (`blog-post.css:5`) already exceeds the 1.5 baseline that SC 1.4.12 Text Spacing requires content to tolerate. Noted as correct.
- **Contrast measures clean.** axe reported no `color-contrast` violation *and* no `color-contrast` incomplete for this page — that is the measured fact and it is what I am relying on. As a supporting estimate only, assuming a white page background (the CSS declares no `background`), `#666` computes to roughly 5.7:1 and `#0066cc` to roughly 5.6:1, both above the 4.5:1 normal-text threshold, with h1/h2 additionally qualifying as large text. The estimate is stated as an estimate; the background assumption is stated because the CSS does not fix it. **If a background color is introduced upstream, this must be re-measured.**
- **No `lang` attribute is verifiable** from a component that renders no `<html>` element. Owned by the page shell. Listed so it does not fall between the two scopes.

---

## Phase 7 — Gap Analysis (What's Missing)

- **A level-2 tier.** The document's outline has a hole where its top-level sections should be. This is the root gap, not a symptom of it.
- **A structural rule the team can apply next time.** Nothing in this component encodes "heading level comes from depth, visual weight comes from a class." Absent that, MAJOR-2's pattern recurs on the next article. Consider a lint rule (`jsx-a11y` has no heading-order rule; `eslint-plugin-jsx-a11y/heading-has-content` covers only empty headings — the ordering check has to come from axe in CI or a custom rule).
- **Content behind "Getting Started."** See MINOR-1.
- **An accessible name on the `<article>` region.** See MINOR-2.
- **Landmark structure — scope-caveated, deliberately not filed as a component defect.** axe fired `landmark-one-main` (`html`) and `region` (`#root`). `<article>` maps to role `article`, which is not a landmark, so the content genuinely sits outside any landmark *as rendered in this harness*. But `BlogPost` is a default-exported component; whoever mounts it owns the page shell. If the fixture page is itself the deliverable, these are real moderate findings against the page. If `BlogPost` is composed into a page that already provides `<main>`, they are harness artifacts and filing them against the component would be page-shell over-flagging. **Needs user verification:** confirm who renders the shell. Concrete check — inspect the deployed page for an element with role `main` wrapping `#root`.
- **Not filed, and here is why:** no skip link (seven short sections; no repeated block to bypass); no table of contents (would be manufactured at this length); no reverse skip-link (same); no `aria-current` (no navigation present); no reduced-motion query (verified: `blog-post.css:1–40` contains no `transition`, `animation`, or `transform` declaration — there is nothing to suppress); no touch-target sizing (no interactive targets exist). Each of these appears on the standard gap checklist and each would have been a false positive here.

---

## Phase 6 — Multi-Perspective Review

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Heading navigation is the primary skim path for long-form prose and it produces a false document map. Measured: census heading levels 1,3,3,3,3,2,2. |
| Keyboard-only | LOW | Zero focusable elements in `BlogPost.jsx:1–33`; census contains no interactive roles. Nothing to order, trap, or restore. |
| Low vision | LOW | No fixed widths (`max-width: 800px` is a cap that shrinks); no interactive targets to size; axe measured zero contrast violations and zero contrast incompletes. |
| Cognitive | **MEDIUM** | The article's information architecture misrepresents itself, and the visual hierarchy corroborates the misrepresentation rather than contradicting it — so no user has a correct signal to fall back on. One heading also promises a section that does not exist. |
| Vestibular & motion | LOW | Verified absence: no `transition`, `animation`, `transform`, parallax, or autoplaying content in `blog-post.css:1–40`. |
| Auditory access | LOW | No `<video>`, `<audio>`, or media player of any kind. |
| Environmental contrast | LOW | Color is never the sole carrier of meaning; the h3/h2 color split is decorative. Forced-colors mode overrides both declarations without information loss. Contrast measured clean. |

**Escalation:** Screen reader (HIGH) and Cognitive (MEDIUM) meet the threshold for deep review via `/perspective-audit`. Given that both trace to the same single root cause and that root cause has a six-line fix, my recommendation is to **fix first and escalate only if the outline defect survives remediation** — a perspective audit would spend its budget re-deriving MAJOR-1.

### Multi-Perspective Notes

**Screen reader user.** Linear reading is correct and complete — all 33 census entries in DOM order, `declared_alternate_reading_order: []`, so SC 1.3.2 Meaningful Sequence is measured-clean. Relationships are clean where they exist: the list announces `set size 3` accurately, and `declared_broken_aria_refs: []` means nothing references a missing id. The failure is exclusively at the navigation layer, which for a 1,000-word article is the layer that matters most: the headings list is the table of contents, and this one is wrong in a way that hides half the article from level-2 navigation. Secondary friction: the `<article>` region is announced without a name (MINOR-2), and one heading leads nowhere (MINOR-1). No redundant or repeated announcements were observed in the census.

**Keyboard-only user.** No findings, and this is a measured result rather than an unexamined phase. There is nothing focusable, so there is no tab order to get wrong, no trap to escape, no Escape handler to miss, no arrow-key convention to discover. Note the boundary precisely: I have **no** focus-indicator evidence in this pack (no trace, no deterministic findings), so if any link is added to this prose later, focus visibility becomes unmeasured and must be tested — the current clean state does not transfer.

**Low vision user (200% zoom, high contrast, magnifier).** Reflow is sound by inspection: `max-width: 800px` with `margin: 20px auto` caps but does not floor the width, `padding: 20px` and `margin-left: 20px` on the list are small and non-fixed, and no element declares a fixed width — no horizontal scroll is predicted at 320px CSS width. Contrast measured clean by axe. The one perspective-specific observation worth recording: because heading level and visual size are correlated here, a magnifier user scanning at 200% sees "Tools and Resources" render *larger and bluer* than the four substantive sections above it — the visual layout repeats the same inverted claim the accessibility tree makes. Fixing MAJOR-1 without MAJOR-2 would fix the tree and leave the visual lie intact.

**Cognitive accessibility.** No forms, no errors, no timeouts, no destructive actions, no authentication, no multi-step flow — SC 3.3.1, 3.3.3, 3.3.4, 3.3.7, 3.3.8 are all inapplicable. The relevant cognitive load here is document comprehension, and the heading structure actively degrades it: a reader building a mental model of the article from its headings builds a wrong one, and "Getting Started" sets an expectation the page never meets. Prose itself is clear and concise. Instructions are absent because none are needed.

---

## Phase 8 — Realist Check (Severity Calibration)

**MAJOR-1 tested against the four questions:**

1. *Realistic worst case if shipped as-is?* A screen reader user surveying the article by level-2 headings reads the closing sections and misses the body, without any signal that content was skipped. They may conclude the article is thin or that content failed to load. They can still recover by reading linearly.
2. *Which group?* Screen reader users and outline-dependent readers. Not keyboard-only, not low vision beyond the note above, not motor.
3. *Detection speed if it slipped through?* Slow. axe reports it as one `moderate` `best-practice` node — a severity that most CI gates do not fail on, and a node count that understates the damage sixfold. Realistically this reaches production and is caught by a manual audit or a user report, i.e. weeks, not minutes.
4. *Proportional, or inflated by review momentum?* Proportional at MAJOR.

**Considered CRITICAL, held at MAJOR.** CRITICAL requires that access be blocked entirely for a user category. It is not: reading order is measured-correct, every word is reachable in browse mode, and the workaround (read linearly instead of skimming by heading) exists and is obvious once the user is in the document. What is lost is efficient navigation and an accurate structural model — significant degradation, not exclusion. The protocol's bar for never downgrading (complete access loss, data loss, safety risk) is not met here.

**MAJOR-2 tested:** worst case is that the defect class recurs across every future article because the team's stated model of the problem ("we don't use headings for styling") is wrong. That is a durable, compounding harm to the same user group, which sustains MAJOR even though the finding is an inference rather than a measurement. Confidence is honestly recorded as MEDIUM rather than the severity being softened to compensate.

**MINOR-1 downgraded from MAJOR.** *Mitigated by:* harm is borne roughly equally by sighted and screen reader users, the fix is a content edit rather than a markup change, and the fixture's visible `...` elisions make abridgement a live alternative explanation.

**No upgrades applied.** No finding grew during the review.

**Recalibrations applied: 1 downgrade (MINOR-1), 0 upgrades, 1 explicit non-upgrade (MAJOR-1 held below CRITICAL).**

---

## Phase 9 — Self-Audit

| Finding | Confidence | Refutable by missing context? | Gap or preference? | Disposition |
|---|---|---|---|---|
| MAJOR-1 heading inversion | HIGH | NO | GAP | Keep |
| MAJOR-2 level chosen by appearance | MEDIUM | PARTIALLY — intent is inferred | GAP | Keep at MAJOR; inference labeled inline |
| MINOR-1 empty section | MEDIUM | YES — fixture may be abridged | GAP | Keep as MINOR, tagged Needs user verification |
| MINOR-2 unnamed article | HIGH | NO | GAP | Keep |
| Landmark absence | HIGH on the measurement, LOW on attribution to this component | YES — page shell may supply `<main>` | Ambiguous | **Moved to Open Questions**, not filed as a component finding |
| px font sizes | HIGH | NO | PREFERENCE-adjacent | Held at Enhancement |

**Nothing was manufactured.** Phases 3, 4, and 5 returned clean, and I reported them clean rather than reaching for something to say. Seven standard gap-checklist items (skip link, TOC, reverse skip-link, `aria-current`, reduced-motion, target size, live regions) were considered and explicitly declined with reasons.

---

## Phase 10 — Synthesis: Predictions vs. Findings

| # | Prediction | Outcome |
|---|---|---|
| 1 | Heading skip / level chosen for visual weight | **Hit, and understated.** I predicted a skip; the actual defect is a skip *plus* an inversion that no automated rule reports. |
| 2 | Missing landmark / unnamed article | **Half hit.** Unnamed `<article>` confirmed by census (MINOR-2). Missing `<main>` measured but attribution is ambiguous — moved to Open Questions rather than claimed. |
| 3 | Missing `lang` | **Unverifiable** from a component that renders no `<html>`. Recorded rather than asserted. |
| 4 | Links distinguishable by color alone (1.4.1) | **Miss.** There are no links at all in `BlogPost.jsx:1–33`. An article about accessibility with zero outbound references is a content observation, not an accessibility defect, and I am not converting it into one. |
| 5 | No bypass mechanism / TOC | **Miss.** Not applicable at seven short sections. Filing it would have been manufactured. |
| 6 | Images without `alt` | **Miss.** No images. The article discusses alt text; it does not contain any. |

**Two out of six predictions landed.** That ratio is the useful part of the exercise: four predicted defect classes did not exist, and the discipline of Phase 1 was mainly useful for *not* filing them.

**What surprised me, and it is the finding of record:** the divergence between what axe reports and what is wrong. axe returns `node_count: 1` on a `moderate`, `best-practice`-tagged rule — a signal most CI gates ignore — for a document whose entire structural map is inverted across six of seven headings. The rule is behaving exactly as specified; it simply does not model "decrease to a level that retroactively reparents everything above it." A team triaging on scanner output would fix one tag and ship. That is the precise class of design gap this critic exists to catch, and it is why the census artifact — which shows the *spoken* levels rather than the rule outcomes — carried more of this review than the scanner did.

**What I did not anticipate:** that the fixture's own "Accessibility Features Present" checklist would be wrong on a claim I would end up filing as a MAJOR. Self-reported feature lists are not evidence, and this one asserted the opposite of what the CSS shows.

---

## Verdict Justification

**REVISE.**

This component's only substantive accessibility responsibility is its document structure — it has no widgets, no state, no focus surface, no media, and no motion — and that one responsibility is discharged incorrectly in a way that produces a false navigational map for the user group most dependent on it. Two MAJOR findings, both tracing to one root cause, both fixable in roughly six lines.

Not **REJECT**: no access is blocked, reading order is measured-correct, every word is reachable, and the remediation is small and unambiguous.

Not **ACCEPT-WITH-RESERVATIONS**: the defect sits at the center of what this component does, not at its margin, and the automated evidence understates it badly enough that shipping on the scanner's `moderate` rating would be a mistake.

**To reach ACCEPT:**

1. Promote `BlogPost.jsx:6, 12, 15, 22` from `h3` to `h2` (or insert a real `h2` parent above line 6 if those four are genuinely subordinate — they do not appear to be).
2. Restore the grey/18px treatment, if it is still wanted, via a presentational class rather than a heading level (MAJOR-2).
3. Add content under "Getting Started" or remove the heading — after confirming the emptiness is not fixture abridgement (MINOR-1).
4. Give the `<article>` an accessible name via `aria-labelledby` (MINOR-2).
5. **Re-verify with the same two instruments**: axe `heading-order` at zero nodes, and a fresh census reading `1, 2, 2, 2, 2, 2, 2`. A screenshot is not acceptable evidence for a fix that lives entirely in the accessibility tree.

**Escalation note:** Screen reader (HIGH) and Cognitive (MEDIUM) alarm levels formally qualify for `/perspective-audit`. I recommend deferring it — both alarms trace to the single root cause already diagnosed here, and a deep audit before remediation would re-derive MAJOR-1 at cost. Escalate if the outline defect survives the fix, or if this component is one instance of a site-wide heading pattern, in which case the audit should target the pattern rather than this file.

**Evidence-scope statement.** This review rests on exactly two of the nineteen artifacts supplied. The other seventeen describe unrelated fixture pages and were used for one purpose only — confirming the scanner was armed and firing during the batch. No finding above imports a violation observed on a sibling page.

---

## Open Questions (unscored)

1. **Who owns the page shell?** axe measured `landmark-one-main` on `html` and `region` on `#root`. If the fixture page is the deliverable, both are real page-scope findings at `moderate` impact. If `BlogPost` is composed into a page that already provides `<main>`, both are harness artifacts and filing them against this component would be over-flagging. I have not filed them. Check: inspect the deployed page for an element with role `main` wrapping `#root`.
2. **Is "Getting Started" empty in production?** Both visible paragraphs in the supplied source are elided with `...`, so the fixture is abridged. MINOR-1 may be an artifact of that abridgement. Verify against unabridged source.
3. **Is a page background declared upstream?** `blog-post.css` declares no `background`. axe's clean contrast result was measured against whatever the harness rendered; my supporting hex arithmetic assumed white. If a background is introduced by a parent stylesheet, `#666` at 18px (`blog-post.css:22–27`) is the value closest to the 4.5:1 threshold and must be re-measured.
4. **Was the level choice deliberate or accidental?** MAJOR-2 infers intent from the CSS. The developer can settle it in one sentence, and the answer determines whether the fix is a one-file edit or a team convention. Either way the markup change is the same.
5. **Does `<html lang>` exist?** Not determinable from a component that renders no document root. Confirm at the shell.
6. **Is this component rendered more than once per page?** If so, the `id="post-title"` recommended in MINOR-2 must be derived per-instance (post slug or generated id) rather than hardcoded, or the duplicate ids will break `aria-labelledby` resolution on every instance after the first.
