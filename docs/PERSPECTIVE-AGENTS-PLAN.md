# Accessibility Perspective Agents — Architecture Plan

**Status:** Revised (v2.1) — incorporates a11y-critic, proposal-critic (2 passes), test-critic feedback
**Date:** 2026-03-28
**Sources:**
- [CivicActions Accessibility Personas](https://accessibility.civicactions.com/personas/)
- [W3C WAI ARRM](https://www.w3.org/WAI/planning/arrm/) (Accessibility Roles and Responsibilities Mapping)
- a11y-meta-skills bundle (planner, critic, test)
- zivtech-meta-skills catalog

---

## 1. Design Principles

1. **Perspectives, not personas.** We extract access needs and AT interaction models — we don't roleplay named characters.
2. **Hybrid architecture.** Lightweight perspective hints in the planner/critic shape thinking at design time; a separate **perspective audit companion** does the deep 8-lens review when escalated. No skill file exceeds its size budget.
3. **Progressive escalation.** The planner/critic lightweight pass produces alarm levels (LOW/MEDIUM/HIGH) per perspective. Only perspectives at MEDIUM or HIGH get the full deep review from the companion audit. A text-only form doesn't need a deep vestibular review; a video player does need deep auditory.
4. **ARRM as reference, not inline.** The W3C ARRM role-responsibility mapping lives in a companion reference file — findings cite it for routing, but it doesn't bloat the skill prompts.
5. **Permanent + Temporary + Situational.** The perspective set covers the full spectrum — a condition isn't less real because it's temporary or environmental.
6. **Evidence over assertion.** Each perspective must cite a WCAG criterion or APG pattern, not just "this feels inaccessible."
7. **One primary owner per criterion.** Every WCAG 2.2 AA criterion has exactly one owning perspective. Secondary perspectives may flag issues from their angle, but the primary owner routes the finding.

---

## 2. The Access Perspectives

Seven first-class perspectives plus one cross-concern. Extracted from CivicActions personas and supplemented with WCAG/ARRM coverage analysis.

| # | Perspective | Derived From | Condition Spectrum | Primary AT/Mechanism |
|---|---|---|---|---|
| 1 | **Magnification & Reflow** | Avery (magnification, migraines) | Permanent low vision, temporary migraine, aging | Screen magnifier, browser zoom 200-400%, OS display scaling |
| 2 | **Environmental Contrast** | Darcy (sunlight/outdoor work) | Situational (ambient light), permanent low contrast sensitivity | OS high-contrast mode, display brightness, user stylesheets |
| 3 | **Vestibular & Motion Sensitivity** | Emery (monovision, vestibular) | Permanent vestibular disorder, temporary concussion, situational motion sensitivity | `prefers-reduced-motion`, image disable, reduced transparency |
| 4 | **Auditory Access** | Parker (hard of hearing) | Permanent deafness/HoH, temporary ear infection, situational (noisy/quiet environment) | Captions, transcripts, visual alerts, text-based communication |
| 5 | **Keyboard & Motor Access** | Quincy (temporary rotator cuff) | Permanent motor disability, temporary injury, RSI | Keyboard-only, switch access, voice control, head pointer |
| 6 | **Screen Reader & Semantic Structure** | (Existing in critic; deepened) | Permanent blindness, temporary eye injury, situational (eyes-busy driving) | NVDA, JAWS, VoiceOver, TalkBack, braille display |
| 7 | **Cognitive & Neurodivergent** | (Shallow in critic; significantly deepened) | Permanent (ADHD, autism, dyslexia, intellectual disability), temporary (fatigue, medication), situational (stress, multitasking) | Plain language, consistent UI, predictable patterns, extended time |
| — | **Bandwidth & Progressive Enhancement** | Raz (remote/low connectivity) | Situational (rural, travel, throttled data), permanent (underserved infrastructure) | Browser image disable, reader mode, text-only browsing |

**Bandwidth is a cross-concern**, not a first-class perspective in the a11y skills. Its WCAG-specific criteria (1.1.1 alt text) are owned by Screen Reader. Its performance criteria are owned by `perf-critic`. The perspective audit companion notes bandwidth implications when relevant but does not run a dedicated bandwidth lens.

---

## 3. Jobs-To-Be-Done per Perspective

### 3.1 Magnification & Reflow

| JTBD | Success Criteria | Failure Signal |
|---|---|---|
| When I zoom to 200%, I need content to reflow into a single column so I can read without horizontal scrolling | No horizontal scrollbar at 320px equivalent (WCAG 1.4.10) | Two-axis scrolling, clipped text, overlapping elements |
| When I use a screen magnifier, I need focus to remain in my viewport so I don't lose my place | Focused element is never obscured by sticky headers/footers (WCAG 2.4.11) | Focus moves behind fixed-position elements |
| When text is small, I need to resize it independently of layout so I can read comfortably | Text scales to 200% without loss of functionality (WCAG 1.4.4) | Text overflow, truncation, broken layout |
| When spacing is tight, I need to override it without breaking layout so I can reduce visual crowding | Content adapts to 1.5x line height, 2x paragraph spacing, 0.12em letter spacing (WCAG 1.4.12) | Overlapping text, hidden content, broken containers |
| When content appears on hover/focus, I need to be able to reach it and dismiss it so I can read it at my zoom level | Hover/focus content is dismissible, hoverable, persistent (WCAG 1.4.13) | Tooltip vanishes when I try to magnify it, can't dismiss with Escape |

**WCAG criteria owned (AA):** 1.4.4, 1.4.10, 1.4.12, 1.4.13, 2.4.11
**WCAG criteria owned (aspirational AAA):** 2.4.12 (Focus Not Obscured Enhanced)

### 3.2 Environmental Contrast

| JTBD | Success Criteria | Failure Signal |
|---|---|---|
| When ambient light reduces visibility, I need sufficient contrast so I can read without changing environments | Text at 4.5:1, large text at 3:1, UI components at 3:1 (WCAG 1.4.3, 1.4.11) | Washed-out text, invisible borders, lost state indicators |
| When color carries meaning, I need a non-color indicator so I don't miss the information | Shape, text, pattern, or icon supplements color (WCAG 1.4.1) | Error shown only in red, status only by color dot |
| When I use high-contrast mode, I need the interface to remain functional so I can complete my task | Forced colors respected; custom focus indicators survive; SVG icons adapt | Icons disappear, focus lost, custom theme breaks layout |
| When information is conveyed by shape or visual location alone, I need a text supplement | Instructions don't rely solely on shape, size, or position (WCAG 1.3.3) | "Click the round button on the left" with no other identifier |

**WCAG criteria owned (AA):** 1.3.3, 1.4.1, 1.4.3, 1.4.11
**WCAG criteria owned (aspirational AAA):** 1.4.6 (Contrast Enhanced 7:1)

### 3.3 Vestibular & Motion Sensitivity

| JTBD | Success Criteria | Failure Signal |
|---|---|---|
| When a page has animation, I need it to respect `prefers-reduced-motion` so I don't get motion sick | All non-essential animation suppressed; transitions reduced to opacity/instant | Parallax, sliding panels, bouncing elements ignore media query |
| When content auto-updates or moves, I need to pause/stop it so I can control my visual environment | Pause/stop/hide for any auto-playing content >5s (WCAG 2.2.2) | Carousels, news tickers, auto-scrolling with no control |
| When flashing content exists, I need it blocked so I don't trigger a seizure or vestibular episode | No more than 3 flashes/second; no red flash (WCAG 2.3.1) | Flashing ads, video content, animated GIFs |
| When functionality is triggered by device motion, I need a UI alternative so I can avoid the motion | Shake/tilt actions have button equivalents and can be disabled (WCAG 2.5.4) | "Shake to undo" with no alternative |

**WCAG criteria owned (AA):** 2.2.2, 2.3.1, 2.5.4
**WCAG criteria owned (aspirational AAA):** 2.3.3 (Animation from Interactions)

**Note:** Vestibular owns fewer criteria but has outsized impact when triggered — a single violation (uncontrolled animation, flashing) can make an entire interface unusable. The perspective audit's escalation threshold is LOW for static content, HIGH for any page with animation, video, or transitions.

### 3.4 Auditory Access

JTBD are split into **code-level** (what the critic can verify from source) and **content-level** (requires human review — flagged as "needs content author verification").

#### Code-Level (Enforceable by Critic)

| JTBD | Success Criteria | Failure Signal |
|---|---|---|
| When video elements exist, I need a `<track>` element for captions so the infrastructure for captions is present | `<track kind="captions">` on every `<video>` with speech (WCAG 1.2.2) | `<video>` with no `<track>` element |
| When audio/video exists, I need transcript markup in the page so the content is available as text | Transcript section exists near the media element (WCAG 1.2.1) | No transcript section, no link to transcript |
| When a media player exists, I need it keyboard-accessible so I can control playback | Play, pause, volume, caption toggle all keyboard-operable (WCAG 2.1.1) | Custom player with click-only controls |
| When an alert uses sound, I need a visual equivalent coded into the component | Visual indicator (icon, color change, text) accompanies audio signals | Error beep with no visual DOM change |

#### Content-Level (Flag for Human Verification)

| JTBD | Verification Needed | Flagged As |
|---|---|---|
| Captions are accurate and well-timed | Human review of caption content vs. audio | "Needs content author verification" |
| Transcript includes speaker identification | Human review of transcript completeness | "Needs content author verification" |
| Audio descriptions cover visual-only information | Human review of description coverage (WCAG 1.2.3, 1.2.5) | "Needs content author verification" |

**WCAG criteria owned (AA):** 1.2.1, 1.2.2, 1.2.3, 1.2.5, 1.4.2

### 3.5 Keyboard & Motor Access

| JTBD | Success Criteria | Failure Signal |
|---|---|---|
| When I can't use a mouse, I need all functionality available via keyboard so I can complete every task | All interactive elements reachable and operable by keyboard (WCAG 2.1.1) | Drag-only reordering, hover-only menus, click-only actions |
| When I navigate with keyboard, I need visible focus indicators so I know where I am | 2px+ focus ring, 3:1 contrast change against adjacent colors (WCAG 2.4.7, 2.4.13) | `outline: none` with no replacement, low-contrast dotted outlines |
| When I need to bypass repetitive content, I need skip links so I can get to the main content efficiently | Skip links present and functional, pointing to expected targets (WCAG 2.4.1) | No skip link, or skip link points to wrong target |
| When there are drag operations, I need a single-pointer alternative so I can complete the task without fine motor control | Click-based alternative for every drag operation (WCAG 2.5.7) | File upload only via drag, kanban reorder only via drag |
| When I use voice control, I need visible labels that match accessible names so my voice commands work | Visible text matches `aria-label` / `aria-labelledby` (WCAG 2.5.3) | Button says "Submit" visually but has `aria-label="btn-primary-action"` |
| When I use switch access, I need a logical scan order with large-enough targets so I can navigate efficiently | Interactive elements ≥24x24 CSS px, logical DOM order (WCAG 2.5.8) | Tiny close buttons, icon-only controls <24px, scattered tab order |
| When multi-point or path-based gestures are required, I need a single-pointer alternative | Pinch-to-zoom has button controls; swipe has arrow buttons (WCAG 2.5.1) | Pinch-only zoom on a map, swipe-only carousel |
| When I activate a control, I need to be able to cancel the action so mistakes aren't irreversible | Activation on up-event, not down-event; ability to abort (WCAG 2.5.2) | Down-event fires immediately with no cancel path |

**WCAG criteria owned (AA):** 1.3.4, 2.1.1, 2.1.2, 2.4.1, 2.4.3, 2.4.7, 2.4.13, 2.5.1, 2.5.2, 2.5.3, 2.5.7, 2.5.8

### 3.6 Screen Reader & Semantic Structure

| JTBD | Success Criteria | Failure Signal |
|---|---|---|
| When I navigate by landmarks, I need proper region structure so I can jump to the section I need | `<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>` used correctly (WCAG 1.3.1) | All content in `<div>` soup, multiple unlabeled `<nav>` elements |
| When I encounter a form, I need programmatic labels and error associations so I can fill it out | Every input has visible `<label>`, errors linked via `aria-describedby` (WCAG 1.3.1, 3.3.1) | Placeholder-only labels, error messages not associated with fields |
| When dynamic content changes, I need live region announcements so I know what happened | Status updates via `aria-live`, correct urgency (`polite` vs `assertive`) (WCAG 4.1.3) | Toast notifications invisible to screen reader, silent form validation |
| When I use a complex widget, I need correct ARIA roles and keyboard patterns so I can operate it | Widget matches WAI-ARIA APG pattern for its type (WCAG 4.1.2) | Custom dropdown with no `role="listbox"`, tab panel with no arrow key navigation |
| When I navigate a SPA, I need route changes announced so I know the page changed | Focus management on route change, page title update, announcement (WCAG 2.4.2) | Silent route changes, stale page titles, focus stays on old content |
| When content is in a different language, I need it marked so my screen reader pronounces it correctly | `lang` on `<html>` and on foreign-language phrases (WCAG 3.1.1, 3.1.2) | French phrase read with English pronunciation rules |
| When images convey information, I need text alternatives so I know what the image communicates | Informative images have descriptive alt; decorative images have `alt=""` (WCAG 1.1.1) | Missing alt, `alt="image"`, `alt="DSC_0042.jpg"` |
| When links exist, I need their purpose clear from context so I know where they go | Link text describes destination or purpose (WCAG 2.4.4) | "Click here", "Read more" with no context |

**WCAG criteria owned (AA):** 1.1.1, 1.3.1, 1.3.2, 2.4.2, 2.4.4, 2.4.6, 3.1.1, 3.1.2, 3.3.1, 3.3.2, 4.1.2, 4.1.3

### 3.7 Cognitive & Neurodivergent

| JTBD | Success Criteria | Failure Signal |
|---|---|---|
| When content is complex, I need plain language so I can understand it without specialized knowledge | Clear, simple language; jargon defined on first use | Dense paragraphs, undefined acronyms, legalese |
| When I fill out a form, I need it to not re-ask information I already provided so I can avoid frustration | Previously entered data pre-populated or auto-completed (WCAG 3.3.7) | Multi-step form re-asking name/address on every page |
| When a login requires authentication, I need it to not depend on cognitive function tests so I can sign in | No transcription, memorization, or puzzle-solving required; paste and autofill work (WCAG 3.3.8) | CAPTCHA with no alternative, password entry without paste support |
| When I make an error, I need specific suggestions so I can correct it | Error messages suggest valid input when the system knows the constraints (WCAG 3.3.3) | "Invalid input" with no guidance on what's valid |
| When navigation patterns change between pages, I need consistency so I don't get lost | Same navigation in same position across pages (WCAG 3.2.3, 3.2.4) | Nav that reorders between sections, inconsistent icon meanings |
| When an action is destructive, I need confirmation so I can catch mistakes | Undo, confirmation dialog, or review step for irreversible actions (WCAG 3.3.4) | One-click delete with no undo, immediate submission of financial data |
| When I'm easily distracted, I need a calm interface so I can maintain focus | No autoplay, minimal animation, clear visual hierarchy, predictable layout | Flashing notifications, cluttered layouts, unexpected popups |
| When focus moves or settings change, I need predictable behavior so I'm not disoriented | Focus does not trigger context changes; input changes don't auto-submit (WCAG 3.2.1, 3.2.2) | Tab to a field and the page scrolls away; selecting a dropdown auto-navigates |
| When help is available, I need it in the same place on every page so I can find it | Help mechanism appears in consistent relative location (WCAG 3.2.6) | Help link in footer on one page, header on another, absent on a third |
| When multiple paths to content exist, I need more than one way to find things so I can use what works for me | Search, nav, sitemap, or breadcrumbs — multiple mechanisms (WCAG 2.4.5) | Single nav menu with no search, no sitemap |
| When form fields ask for personal data, I need autocomplete support so I can fill them without retyping | Input fields have appropriate `autocomplete` attributes (WCAG 1.3.5) | Name/address/email fields with no autocomplete, forcing manual entry |

**WCAG criteria owned (AA):** 1.3.5, 2.4.5, 3.2.1, 3.2.2, 3.2.3, 3.2.4, 3.2.6, 3.3.3, 3.3.4, 3.3.7, 3.3.8
**WCAG criteria owned (aspirational AAA):** 3.1.3 (Unusual Words), 3.1.4 (Abbreviations), 3.1.5 (Reading Level), 3.3.6 (Error Prevention - All)

---

## 4. WCAG 2.2 AA Coverage Matrix

Every Level A and AA criterion has exactly one primary perspective owner. Criteria not listed are either Level AAA (see aspirational lists per perspective) or deprecated (4.1.1 removed in WCAG 2.2).

| WCAG SC | Name | Level | Primary Perspective |
|---|---|---|---|
| 1.1.1 | Non-text Content | A | Screen Reader |
| 1.2.1 | Audio-only / Video-only | A | Auditory |
| 1.2.2 | Captions (Prerecorded) | A | Auditory |
| 1.2.3 | Audio Description or Media Alternative | A | Auditory |
| 1.2.5 | Audio Description (Prerecorded) | AA | Auditory |
| 1.3.1 | Info and Relationships | A | Screen Reader |
| 1.3.2 | Meaningful Sequence | A | Screen Reader |
| 1.3.3 | Sensory Characteristics | A | Environmental Contrast |
| 1.3.4 | Orientation | AA | Keyboard & Motor |
| 1.3.5 | Identify Input Purpose | AA | Cognitive |
| 1.4.1 | Use of Color | A | Environmental Contrast |
| 1.4.2 | Audio Control | A | Auditory |
| 1.4.3 | Contrast (Minimum) | AA | Environmental Contrast |
| 1.4.4 | Resize Text | AA | Magnification |
| 1.4.5 | Images of Text | AA | Screen Reader |
| 1.4.10 | Reflow | AA | Magnification |
| 1.4.11 | Non-text Contrast | AA | Environmental Contrast |
| 1.4.12 | Text Spacing | AA | Magnification |
| 1.4.13 | Content on Hover or Focus | AA | Magnification |
| 2.1.1 | Keyboard | A | Keyboard & Motor |
| 2.1.2 | No Keyboard Trap | A | Keyboard & Motor |
| 2.1.4 | Character Key Shortcuts | A | Keyboard & Motor |
| 2.2.1 | Timing Adjustable | A | Cognitive |
| 2.2.2 | Pause, Stop, Hide | A | Vestibular |
| 2.3.1 | Three Flashes or Below | A | Vestibular |
| 2.4.1 | Bypass Blocks | A | Keyboard & Motor |
| 2.4.2 | Page Titled | A | Screen Reader |
| 2.4.3 | Focus Order | A | Keyboard & Motor |
| 2.4.4 | Link Purpose (In Context) | A | Screen Reader |
| 2.4.5 | Multiple Ways | AA | Cognitive |
| 2.4.6 | Headings and Labels | AA | Screen Reader |
| 2.4.7 | Focus Visible | AA | Keyboard & Motor |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | Magnification |
| 2.4.13 | Focus Appearance | AA | Keyboard & Motor |
| 2.5.1 | Pointer Gestures | A | Keyboard & Motor |
| 2.5.2 | Pointer Cancellation | A | Keyboard & Motor |
| 2.5.3 | Label in Name | A | Keyboard & Motor |
| 2.5.4 | Motion Actuation | A | Vestibular |
| 2.5.7 | Dragging Movements | AA | Keyboard & Motor |
| 2.5.8 | Target Size (Minimum) | AA | Keyboard & Motor |
| 3.1.1 | Language of Page | A | Screen Reader |
| 3.1.2 | Language of Parts | AA | Screen Reader |
| 3.2.1 | On Focus | A | Cognitive |
| 3.2.2 | On Input | A | Cognitive |
| 3.2.3 | Consistent Navigation | AA | Cognitive |
| 3.2.4 | Consistent Identification | AA | Cognitive |
| 3.2.6 | Consistent Help | A | Cognitive |
| 3.3.1 | Error Identification | A | Screen Reader |
| 3.3.2 | Labels or Instructions | A | Screen Reader |
| 3.3.3 | Error Suggestion | AA | Cognitive |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | Cognitive |
| 3.3.7 | Redundant Entry | A | Cognitive |
| 3.3.8 | Accessible Authentication (Minimum) | AA | Cognitive |

**Coverage:** 52 criteria mapped. Zero orphans at Level A or AA.

---

## 5. Skill Mapping Matrix

### 5.1 Existing Skill Coverage

| Perspective | Primary Skills (serve well) | Secondary Skills (partial) | Gap Level |
|---|---|---|---|
| Magnification & Reflow | a11y-planner (Phase 6), a11y-critic (low vision lens), a11y-test (visual regression) | ui-critic, web-design-critic | **Low** — needs WCAG 2.2 criteria (1.4.13, 2.4.11) wired in |
| Environmental Contrast | a11y-planner (contrast mentions), a11y-critic (low vision lens) | graphic-design-critic, dataviz-critic | **Medium** — no evidence-based contrast calculation |
| Vestibular & Motion | a11y-planner (reduced-motion mention), a11y-test (reduced-motion) | — | **Medium** — shallow, no explicit planning phase |
| Auditory Access | — | — | **Critical** — zero coverage in all 3 skills |
| Keyboard & Motor | a11y-planner (Phase 3,4), a11y-critic (keyboard lens), a11y-test (keyboard templates) | ui-critic, mobile-design-critic | **Low** — strongest coverage; needs more widget templates, switch/voice |
| Screen Reader & Semantic | a11y-planner (Phase 3,5), a11y-critic (screen reader lens), a11y-test (ARIA verification) | content-model-critic | **Low** — strong; needs actual SR test protocol and language criterion (3.1.1/3.1.2) |
| Cognitive & Neurodivergent | a11y-planner (shallow), a11y-critic (cognitive lens, shallow) | copy-critic, brand-voice-guide | **High** — exists but shallow, missing plain language, neurodivergent depth, 3.3.7/3.3.8 |

### 5.2 Skills Needing Enhancement

| Skill | What to Add | Lines Budget | Perspectives Served |
|---|---|---|---|
| **a11y-planner** | Lightweight perspective hints in Phases 3-7 (~2-3 lines per phase, total ~20 lines across all perspectives); new Phase 7b: Time-Based Media; wire WCAG 2.2 into Phase 4/5 | Max 900 total lines | Auditory, Cognitive, Magnification, Vestibular |
| **a11y-critic** | Expand alarm-level assessment from 4 to 7 perspectives; add time-based media to gap analysis; wire WCAG 2.2 criteria | Max 700 total lines | All 7 perspectives |
| **a11y-test** | Expand keyboard widget templates (+7); new Section 5: media test; new Section 6: SR test; contrast guidance | Max 600 total lines | Auditory, Screen Reader, Keyboard, Contrast |
| **perspective-audit** (NEW) | Deep 7-lens review — activated by escalation from planner/critic | ~400 lines | All 7 perspectives |

### 5.3 New Capabilities Needed

| Need | Type | Rationale | Perspectives Served |
|---|---|---|---|
| **Perspective audit companion** | New skill | Deep review without bloating existing skills | All |
| **Time-based media module** | Enhancement to all 3 skills | Auditory has zero coverage — largest gap | Auditory |
| **Contrast calculator integration** | MCP tool (AccessLint) | Evidence-based contrast, not assertion | Contrast, Magnification |
| **Mobile AT protocol** | New section in a11y-test | iOS VoiceOver, Android TalkBack | Screen Reader (mobile) |

---

## 6. ARRM Integration — Reference Mapping

The W3C ARRM role-responsibility framework is maintained as a **companion reference file** (`references/arrm-perspective-mapping.md`) rather than embedded in skill prompts. When a finding is raised, the audit companion cites the ARRM primary owner so the finding routes to the right team member.

### 6.1 Perspective-to-ARRM Role Mapping

| Perspective | ARRM Primary Owner | ARRM Secondary |
|---|---|---|
| Magnification & Reflow | Visual Design (layout, spacing) | Front-End Dev (CSS implementation) |
| Environmental Contrast | Visual Design (color, contrast) | Front-End Dev (forced-colors support) |
| Vestibular & Motion | UX Design (animation decisions) | Front-End Dev (prefers-reduced-motion) |
| Auditory Access | Content Author (captions, transcripts) | Front-End Dev (media player a11y) |
| Keyboard & Motor | Front-End Dev (keyboard implementation) | UX Design (focus order, interaction design) |
| Screen Reader & Semantic | Front-End Dev (semantic HTML, ARIA) | Content Author (alt text, heading text, link text) |
| Cognitive & Neurodivergent | Content Author (plain language) + UX Design (consistent patterns) | Front-End Dev (error prevention, autofill) |

### 6.2 ARRM Decision Tree for Finding Routing

When the perspective audit surfaces a finding, route it:

```
Is it about content (captions, alt text, language, reading level)?
  → Primary: Content Author

Is it about interaction patterns (focus order, animation, gestures)?
  → Primary: UX Design

Is it about visual presentation (contrast, spacing, focus indicators)?
  → Primary: Visual Design

Is it about implementation (semantic HTML, ARIA, keyboard, media player)?
  → Primary: Front-End Dev
```

---

## 7. Implementation Architecture

### 7.1 Hybrid Model: Lightweight Hints + Companion Audit with Progressive Escalation

```
┌──────────────────────────────────────────────────────────┐
│  LAYER 1: Lightweight Perspective Hints                   │
│  (2-3 lines per perspective, inline in existing skills)   │
│                                                           │
│  a11y-planner phases include:                            │
│    "Consider: [perspective] — [trigger question]"         │
│    Output: alarm level per perspective (LOW/MED/HIGH)     │
│                                                           │
│  a11y-critic lenses include:                             │
│    Quick-scan question per perspective                    │
│    Output: alarm level per perspective (LOW/MED/HIGH)     │
│                                                           │
│  Cost: ~20 lines added to planner, ~15 to critic         │
│  Value: Shapes thinking at design time; catches obvious   │
│         gaps; determines which perspectives need depth    │
└──────────────────────────┬───────────────────────────────┘
                           │
              Alarm levels: which perspectives ≥ MEDIUM?
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│  LAYER 2: Perspective Audit Companion                     │
│  (separate skill, ~400 lines)                            │
│                                                           │
│  Activated ONLY for perspectives at MEDIUM or HIGH alarm  │
│                                                           │
│  Per escalated perspective:                              │
│    • Full JTBD checklist from Section 3                   │
│    • WCAG criteria audit (primary-owned criteria)         │
│    • ARRM role routing (from reference file)              │
│    • Severity: CRITICAL / MAJOR / MINOR                   │
│    • Code-level vs content-level finding split            │
│    • Evidence required for each finding                   │
│                                                           │
│  Cost: Only runs the lenses that matter                   │
│  Value: Deep, thorough, perspective-specific review       │
└──────────────────────────────────────────────────────────┘
```

### 7.2 Escalation Rules

The planner/critic lightweight pass assesses alarm level per perspective based on content signals:

| Perspective | HIGH Alarm Triggers | MEDIUM Alarm Triggers | LOW (skip deep review) |
|---|---|---|---|
| Magnification & Reflow | Sticky headers/footers, complex layouts, data tables | Custom font sizing, responsive breakpoints | Text-only content, simple layout |
| Environmental Contrast | Custom color palette, branded colors, data visualization | Standard UI with default colors | Text on white/black backgrounds |
| Vestibular & Motion | Animation, video, parallax, transitions, carousels | CSS transitions on hover/focus | Static content, no motion |
| Auditory Access | `<video>`, `<audio>`, media player, podcast | Notification sounds, alert beeps | No audio/video content |
| Keyboard & Motor | Custom widgets, drag-and-drop, complex interactions | Standard forms with custom styling | Static content, simple links |
| Screen Reader & Semantic | Custom widgets, dynamic content, SPA routing, forms | Standard semantic HTML, simple pages | — (always at least MEDIUM for interactive content) |
| Cognitive & Neurodivergent | Multi-step flows, authentication, destructive actions, dense content | Standard forms, navigation patterns | Simple informational content |

### 7.2.1 Expected Alarm-Level Distributions

To calibrate whether escalation is working correctly, here are expected distributions for three archetype components:

| Archetype | Expected MEDIUM+ Perspectives | Typical HIGH | Typical LOW |
|---|---|---|---|
| **Static content page** (article, about page) | 1-2 | — | Vestibular, Auditory, Keyboard |
| **Interactive form** (checkout, settings, auth) | 3-4 | Cognitive, Keyboard | Vestibular, Auditory |
| **Media-rich SPA** (dashboard, video platform) | 5-6 | Auditory, Screen Reader, Keyboard, Cognitive | — |

If a component consistently triggers fewer or more perspectives than its archetype predicts, recalibrate the escalation triggers. If >5 perspectives fire on a simple form, triggers are too aggressive; if <2 fire on a media SPA, triggers are too conservative.

### 7.3 Lifecycle Integration

```
Plan (a11y-planner)        → Lightweight hints produce alarm levels
                           ↓
Critique Plan (a11y-critic) → Lightweight scan confirms/adjusts alarm levels
                           ↓
Perspective Audit           → Deep review of MEDIUM+ perspectives on the plan
                           ↓
Revise plan                 → Address audit findings
                           ↓
Implement                   → Build according to reviewed plan
                           ↓
Test (a11y-test)           → Automated + keyboard + visual + media + SR tests
                           ↓
Critique Implementation     → a11y-critic lightweight scan → alarm levels
                           ↓
Perspective Audit           → Deep review of MEDIUM+ perspectives on implementation
                           ↓
Fix                         → Address audit findings
                           ↓
Re-test                     → Verify fixes
```

### 7.4 Reference Perspective Voice: Auditory Access (Deep Review)

This is the fully instantiated template for the Auditory perspective in the companion audit. All perspectives follow this format.

```markdown
### Auditory Access — Deep Review

**Trigger:** Escalated at MEDIUM or HIGH alarm (media elements detected in component)

**JTBD checklist (code-level — enforceable):**
- [ ] Every `<video>` with speech has `<track kind="captions">` element
- [ ] Every `<audio>` has a transcript section or link to transcript in adjacent markup
- [ ] Media player controls (play, pause, volume, caption toggle) are keyboard-operable
- [ ] Visual indicators accompany all auditory alerts/notifications
- [ ] No audio auto-plays, or auto-play has immediate pause/stop control within first element in focus order

**JTBD checklist (content-level — flag for human verification):**
- [ ] Caption accuracy and timing — "Needs content author verification"
- [ ] Transcript speaker identification — "Needs content author verification"
- [ ] Audio description coverage of visual-only information — "Needs content author verification"

**WCAG criteria to audit (primary-owned):**
1.2.1 (Audio-only/Video-only), 1.2.2 (Captions), 1.2.3 (Audio Description or Alternative),
1.2.5 (Audio Description), 1.4.2 (Audio Control)

**ARRM primary owner:** Content Author (captions, transcripts, descriptions)
**ARRM secondary:** Front-End Dev (media player keyboard access, visual alert implementation)

**Red flags (auto-CRITICAL):**
- `<video>` element with speech content and no `<track>` element at all
- Media player with no keyboard controls
- Audio auto-plays with no visible stop control

**Severity calibration:**
- CRITICAL: Complete absence of captions/transcripts on media with speech
- MAJOR: Infrastructure present but incomplete (e.g., `<track>` exists but captions are auto-generated placeholder)
- MINOR: Captions present but styling could improve (contrast, positioning)

**Evidence required to pass:**
- Each `<video>` with speech has a `<track kind="captions">` with a valid `src`
- Each audio content element has adjacent transcript markup or visible link
- Keyboard test confirms: Tab to player → Space plays/pauses → C toggles captions
```

### 7.5 Reference Perspective Voice: Cognitive & Neurodivergent (Deep Review)

```markdown
### Cognitive & Neurodivergent — Deep Review

**Trigger:** Escalated at MEDIUM or HIGH alarm (multi-step flows, auth, dense content, destructive actions)

**JTBD checklist:**
- [ ] Error messages suggest specific corrective action, not just "invalid input" (3.3.3)
- [ ] Multi-step forms do not re-ask information provided in earlier steps (3.3.7)
- [ ] Authentication does not require transcription, memorization, or puzzle-solving; paste and autofill work (3.3.8)
- [ ] Navigation appears in the same relative position across all pages (3.2.3)
- [ ] Components with same function have consistent labels/icons across pages (3.2.4)
- [ ] Help mechanism (link, chat, phone) appears in same location on every page (3.2.6)
- [ ] Focus on an element does not auto-trigger context change (3.2.1)
- [ ] Changing a form control value does not auto-submit or auto-navigate (3.2.2)
- [ ] Destructive actions have undo, confirmation, or review step (3.3.4)
- [ ] More than one way to reach any page exists (search, nav, sitemap, breadcrumbs) (2.4.5)
- [ ] Input fields for personal data have appropriate `autocomplete` attributes (1.3.5)
- [ ] Content avoids unexplained jargon, undefined abbreviations, and unnecessarily complex sentences

**Neurodivergent-specific checks:**
- [ ] Page layout is predictable — main content in expected location, no layout shifts
- [ ] Visual hierarchy is clear — headings, spacing, and grouping guide reading order
- [ ] No autoplay media or unprompted modal dialogs
- [ ] Timeout warnings give ≥20 seconds to extend (2.2.1)
- [ ] Instructions don't rely on memory of previous steps

**WCAG criteria to audit (primary-owned):**
1.3.5, 2.2.1, 2.4.5, 3.2.1, 3.2.2, 3.2.3, 3.2.4, 3.2.6, 3.3.3, 3.3.4, 3.3.7, 3.3.8

**Aspirational AAA (report as ENHANCEMENT, not MAJOR/CRITICAL):**
3.1.3 (Unusual Words), 3.1.4 (Abbreviations), 3.1.5 (Reading Level), 3.3.6 (Error Prevention - All)

**ARRM primary owner:** Content Author (plain language, consistent labeling) + UX Design (predictable patterns, navigation consistency)
**ARRM secondary:** Front-End Dev (autocomplete attributes, error association, autofill support)

**Red flags (auto-CRITICAL):**
- CAPTCHA or cognitive function test with no accessible alternative
- Paste disabled on password or verification fields
- Multi-step form re-collecting name/email/address already provided
- Destructive action (delete, submit payment) with no confirmation step

**Severity calibration:**
- CRITICAL: Authentication requires cognitive test; paste blocked; no undo on destructive action
- MAJOR: Navigation inconsistency across pages; no error suggestions; redundant entry
- MINOR: Jargon used but defined nearby; help location varies slightly
- ENHANCEMENT (AAA): Reading level could be simplified; abbreviations could be expanded

**Evidence required to pass:**
- Authentication flow tested: paste works in password field; no CAPTCHA without alternative
- Multi-step form tested: data entered in step 1 appears pre-filled in step 3
- Navigation compared across 3+ pages: same elements in same order
- Destructive action tested: confirmation dialog or undo appears before irreversible commit
```

### 7.6 Size Budget

| Skill File | Current Lines | Max After Enhancement | Change Budget |
|---|---|---|---|
| a11y-planner SKILL.md | ~878 | 900 | +22 lines (lightweight hints only) |
| a11y-critic SKILL.md | ~634 | 700 | +66 lines (alarm assessment, time-based media) |
| a11y-test SKILL.md | ~400 | 600 | +200 lines (media protocol, SR protocol, widget templates) |
| **perspective-audit** (NEW) | 0 | 400 | New companion skill |
| **references/arrm-perspective-mapping.md** (NEW) | 0 | 100 | Reference file, not loaded into prompt |
| **references/perspectives.md** (NEW) | 0 | 250 | JTBD checklists the audit companion reads at invocation |

**Compression strategy:** The perspective audit companion reads `references/perspectives.md` and `references/arrm-perspective-mapping.md` at invocation time using the Read tool. This keeps the full JTBD checklists and ARRM mappings out of the prompt until needed, and means only escalated perspectives' content enters the context window.

---

## 8. Gap Analysis Summary

### 8.1 Fully Addressed After This Plan

| Gap | Resolution |
|---|---|
| Time-based media | Auditory perspective + planner Phase 7b + media test protocol |
| Cognitive depth | Deepened cognitive perspective with 11 AA criteria, neurodivergent checks, plain language |
| WCAG 2.2 new criteria | Complete coverage matrix; all AA criteria assigned to perspectives |
| Vestibular/motion | Explicit perspective with escalation triggers and testing |
| Screen reader testing | New SR test protocol in a11y-test |
| Orphaned WCAG criteria | Coverage matrix assigns all 52 A/AA criteria |

### 8.2 Partially Addressed (Needs Follow-Up)

| Gap | What This Plan Does | What Remains |
|---|---|---|
| Mobile AT | Noted as extension to SR perspective | Separate mobile AT test protocol — distinct gesture model |
| Contrast calculation | Guidance in a11y-test | Evidence-based requires AccessLint MCP integration |
| Switch access / voice control | JTBD in Keyboard & Motor perspective | Deep scanning-pattern protocol beyond scope |

### 8.3 Not Addressed (Out of Scope)

| Gap | Reason |
|---|---|
| Plain language scoring | Requires NLP tooling, not prompt-only |
| Real device testing | Requires hardware; skills are prompt-only guidance |
| Automated caption quality | Requires media processing tooling |
| Bandwidth/performance | Cross-concern; owned by perf-critic |

---

## 9. Evaluation Framework

### 9.1 Design

**Hypothesis:** Adding 7 explicit access perspectives via the hybrid model (lightweight hints + escalated companion audit) produces more findings in under-covered dimensions without reducing quality in already-strong dimensions.

**Method:** Paired before/after on a fixed fixture set. Three conditions: (A) current skills, (B) strong generic baseline (current skills + "also review for auditory, vestibular, cognitive, and contrast accessibility" appended to prompt), (C) enhanced skills with perspective audit.

Comparing A vs C measures whether adding perspectives helps. Comparing B vs C isolates whether the *structured JTBD/escalation approach* helps beyond simply naming the dimensions.

### 9.2 Fixture Set

**n = 25 fixtures** (matching existing eval suite standard). 3 repeats per fixture per condition. Total: 25 × 3 conditions × 3 repeats = 225 evaluations.

**Fixture composition:**
- 10 HAS-BUGS fixtures: components with planted issues in new dimensions (auditory, vestibular, cognitive, contrast)
- 6 HAS-BUGS fixtures: components with issues in existing-strength dimensions (keyboard, screen reader, ARIA) — regression detection
- 5 CLEAN fixtures: components where new dimensions are satisfied — false positive measurement
- 4 ADVERSARIAL fixtures: components with subtle, non-obvious issues that require perspective-specific reasoning

**Alarm-level calibration fixtures (additional):** 5 fixtures specifically testing whether the planner/critic lightweight pass produces correct alarm levels for known components. Each fixture has a documented expected alarm level per perspective. Scored on alarm-level accuracy (correct level per perspective), not downstream findings. These validate the escalation mechanism itself.

| Calibration Fixture | Expected HIGH | Expected MEDIUM | Expected LOW |
|---|---|---|---|
| C1. Static blog post (text + 1 image) | — | Screen Reader, Cognitive | Magnification, Contrast, Vestibular, Auditory, Keyboard |
| C2. Login form with CAPTCHA | Cognitive, Keyboard | Screen Reader | Magnification, Contrast, Vestibular, Auditory |
| C3. Video tutorial page | Auditory, Screen Reader | Cognitive, Keyboard | Magnification, Vestibular, Contrast |
| C4. Animated dashboard with charts | Vestibular, Contrast, Keyboard, Screen Reader | Magnification, Cognitive | Auditory |
| C5. Drag-and-drop kanban with dense content | Keyboard, Cognitive | Screen Reader, Magnification | Vestibular, Auditory, Contrast |

**Fixture sourcing:** At least 50% of the 25 main fixtures sourced from external accessibility audit failures (WebAIM survey patterns, Deque case studies, real GitHub issues). Remaining fixtures designed independently from Section 3 JTBD tables to prevent data leakage.

**Fixture metadata:** Each fixture has `metadata.yaml` with: source, planted issues with WCAG criteria, relevant perspectives, expected findings. Format matches existing `evals/suites/a11y-critic/` structure.

### 9.3 Scoring Protocol

| Metric | Definition | How Measured | Target |
|---|---|---|---|
| **Precision-weighted coverage** | Distinct WCAG criteria cited that correspond to real issues in the fixture | Rule-based: match cited criteria against planted-issues ground truth | C ≥ 1.3x A |
| **New-dimension precision** | % of findings in auditory/vestibular/cognitive/contrast dimensions that are correct | LLM judge (claude-sonnet-4-6) against rubric | C ≥ 80% |
| **New-dimension recall** | % of planted new-dimension issues found | Rule-based against ground truth | C ≥ 70% |
| **Existing-dimension TPR** | True positive rate in keyboard/screen reader/ARIA dimensions | Rule-based against ground truth | C ≥ A (no regression) |
| **False positive rate** | Findings that don't match any real issue (esp. on CLEAN fixtures) | LLM judge against rubric | C ≤ A + 10% |
| **Actionability** | % of findings that include: specific element reference, problem description, affected user group, fix suggestion | Rule-based: 4-point checklist per finding | C ≥ 85% |
| **Escalation accuracy** | % of alarm levels matching expected levels on calibration fixtures (5 fixtures × 7 perspectives = 35 assessments) | Rule-based: exact match or ±1 level | ≥ 80% exact, ≥ 95% within ±1 |

**Scoring method:** Hybrid — 70% rule-based (criteria matching, element reference detection), 30% LLM judge (finding quality, false positive adjudication). LLM judge: claude-sonnet-4-6, temperature 0. Matches existing eval suite methodology.

### 9.4 Statistical Design

- **Sample size:** n=25 fixtures. Power: ~80% for medium effect (d=0.5) at alpha=0.05 with Wilcoxon signed-rank. Matches existing a11y-critic eval suite.
- **Repeats:** 3 per fixture per condition. Report mean scores with within-fixture SD.
- **Test:** Wilcoxon signed-rank on mean fixture scores (paired, non-parametric).
- **Effect size:** Report Cohen's d (or r = Z/√N for non-parametric).
- **Multiple comparisons:** Bonferroni correction across 7 metrics (adjusted alpha = 0.007).
- **Confidence intervals:** Bootstrap with B=1000.
- **Model version:** Pin to claude-opus-4-6, temperature 0 for reproducibility.
- **Pilot:** Run 5 fixtures first as pilot validation before full evaluation.

### 9.5 Success Criteria

The enhancement is validated if (at Bonferroni-corrected alpha = 0.007 across 7 metrics):
- Precision-weighted coverage: C ≥ 1.3x A (significant improvement)
- New-dimension precision ≥ 80% (findings in new dimensions are real)
- New-dimension recall ≥ 70% (planted issues are found)
- Existing-dimension TPR: C ≥ A at non-inferiority margin of -5% (no regression)
- False positive rate: C ≤ A + 10% (precision preserved)
- Actionability ≥ 85% (findings are usable without ARRM tags required)
- Escalation accuracy ≥ 80% exact match on calibration fixtures (validates the progressive escalation mechanism)

---

## 10. Implementation Sequence

### Phase 1: Interface Contracts (before any skill editing)
- [ ] Finalize perspective names, WCAG criteria ownership, alarm trigger definitions
- [ ] Create `references/perspectives.md` with all 7 perspective JTBD checklists
- [ ] Create `references/arrm-perspective-mapping.md` with role routing reference
- [ ] This establishes the contracts that Phases 2-4 build against

### Phase 2: Companion Skill + Evaluation Baseline
- [ ] Create `perspective-audit` companion skill (~400 lines) with escalation protocol
- [ ] Define invocation model: planner/critic output includes alarm levels; user or orchestrator invokes `/perspective-audit` with the escalated perspectives as arguments
- [ ] Create 25 evaluation fixtures in `evals/suites/perspectives/`
- [ ] Create 5 alarm-level calibration fixtures in `evals/suites/perspectives/calibration/`
- [ ] Run pilot (5 main fixtures + 3 calibration fixtures) to validate scoring methodology
- [ ] Run current skills (condition A) and strong generic baseline (condition B) against all fixtures

### Phase 3: Skill Enhancement (all 3 skills as atomic change)
- [ ] a11y-planner: Add lightweight hints (~20 lines), new Phase 7b (time-based media), WCAG 2.2 criteria in Phase 4/5
- [ ] a11y-critic: Add alarm-level assessment, time-based media in gap analysis, WCAG 2.2 in Phase 7
- [ ] a11y-test: Expand keyboard templates (+7), add Section 5 (media), Section 6 (SR), contrast guidance
- [ ] Review all 3 as a single change to ensure alignment

### Phase 4: Evaluation Treatment
- [ ] Run enhanced skills (condition C) against same 25 fixtures, 3 repeats
- [ ] Score on 6 metrics with bootstrap CIs
- [ ] Compare A vs C (does it help?) and B vs C (does structure help beyond naming?)
- [ ] Report results; iterate on weak dimensions

---

## 11. Appendix A: Perspective-to-Persona Derivation

| Perspective | CivicActions Source | What We Extracted | What We Added |
|---|---|---|---|
| Magnification & Reflow | Avery (magnification, migraines) | Screen magnification, migraine triggers, text sizing | WCAG 2.2 focus-not-obscured, text spacing, content on hover/focus |
| Environmental Contrast | Darcy (sunlight/outdoor) | Outdoor visibility, contrast sensitivity | High-contrast mode, forced-colors, sensory characteristics |
| Vestibular & Motion | Emery (monovision, vestibular) | Motion sickness, prefers-reduced-motion | Seizure threshold, motion actuation alternative, animation inventory |
| Auditory Access | Parker (hard of hearing) | Caption dependency, phone-only frustration | Full 1.2.x coverage, code/content split, media player a11y |
| Keyboard & Motor | Quincy (temporary rotator cuff) | Keyboard-only navigation | Switch access, voice control, pointer gestures, pointer cancellation, target sizing |
| Screen Reader & Semantic | (Existing, deepened) | — | Language criteria, alt text ownership, link purpose, SPA patterns |
| Cognitive & Neurodivergent | (Existing, deepened) | — | 11 AA criteria, neurodivergent checks, plain language, auth, redundant entry |

## 12. Appendix B: Intersection Cases

The 7 perspectives cover single-dimension access needs. Some users experience intersections:

| Intersection | Example | How Handled |
|---|---|---|
| Deaf + Blind | Braille display user; needs both Auditory and Screen Reader perspectives | Both perspectives escalated; findings from each are complementary, not conflicting |
| Motor + Cognitive | User with cerebral palsy — keyboard navigation AND cognitive load concerns | Both perspectives escalated; Keyboard & Motor handles interaction, Cognitive handles content/flow |
| Low Vision + Vestibular | User with migraine — both magnification and motion sensitivity | Both perspectives escalated; Magnification handles zoom/reflow, Vestibular handles animation |

The escalation model handles intersections naturally: when multiple perspectives trigger MEDIUM or HIGH, all triggered perspectives run their deep review. No special intersection logic needed — the perspectives are designed to be orthogonal.
