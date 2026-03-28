# Perspective JTBD Checklists

Reference file read by the perspective-audit companion at invocation time.
Only load the sections for perspectives escalated to MEDIUM or HIGH.

---

## 1. Magnification & Reflow

**WCAG criteria (AA):** 1.4.4, 1.4.10, 1.4.12, 1.4.13, 2.4.11
**Aspirational AAA:** 2.4.12

**JTBD checklist:**
- [ ] Content reflows to single column at 320px equivalent — no horizontal scrollbar (1.4.10)
- [ ] Focused elements are never obscured by sticky headers, footers, or banners (2.4.11)
- [ ] Text scales to 200% without overflow, truncation, or broken layout (1.4.4)
- [ ] Content adapts to user text spacing overrides: 1.5x line height, 2x paragraph spacing, 0.12em letter spacing, 0.16em word spacing (1.4.12)
- [ ] Hover/focus-triggered content (tooltips, popovers) is dismissible (Escape), hoverable (pointer can reach it), and persistent (doesn't vanish on its own) (1.4.13)

**Red flags (auto-CRITICAL):**
- Two-axis scrolling at 320px equivalent viewport
- Text completely hidden or overlapping at 200% zoom
- Tooltip disappears before magnifier user can reach it

**Evidence required to pass:**
- Visual regression screenshots at 200% and 400% zoom show no overflow or overlap
- All sticky/fixed elements tested with keyboard focus — focus target never obscured

---

## 2. Environmental Contrast

**WCAG criteria (AA):** 1.3.3, 1.4.1, 1.4.3, 1.4.11
**Aspirational AAA:** 1.4.6

**JTBD checklist:**
- [ ] Normal text contrast ≥ 4.5:1 against background (1.4.3)
- [ ] Large text (≥18pt or ≥14pt bold) contrast ≥ 3:1 (1.4.3)
- [ ] UI component boundaries and states contrast ≥ 3:1 against adjacent colors (1.4.11)
- [ ] Color is never the sole indicator of meaning — shape, text, pattern, or icon supplements it (1.4.1)
- [ ] Instructions don't rely solely on sensory characteristics (shape, size, visual location, orientation, sound) (1.3.3)
- [ ] Interface remains functional in Windows High Contrast Mode / forced-colors: icons visible, focus indicators present, interactive boundaries clear

**Red flags (auto-CRITICAL):**
- Body text below 3:1 contrast ratio
- Error state communicated only by red color with no icon or text
- Interactive element indistinguishable from surrounding content in forced-colors mode

**Evidence required to pass:**
- Contrast ratios measured (DevTools or axe-core) for: body text, headings, placeholder text, UI borders, focus indicators
- Non-color indicators present for every color-coded state (errors, success, warnings, selections)

---

## 3. Vestibular & Motion Sensitivity

**WCAG criteria (AA):** 2.2.2, 2.3.1, 2.5.4
**Aspirational AAA:** 2.3.3

**JTBD checklist:**
- [ ] All non-essential animations suppressed when `prefers-reduced-motion: reduce` is active
- [ ] Essential animations (progress indicators, loading) reduced to opacity/fade only under reduced-motion
- [ ] Auto-playing content >5 seconds has visible pause/stop/hide control (2.2.2)
- [ ] No content flashes more than 3 times per second (2.3.1)
- [ ] Any functionality triggered by device motion (shake, tilt) has a UI button alternative and can be disabled (2.5.4)
- [ ] Parallax scrolling either removed or disabled under reduced-motion
- [ ] Video auto-play disabled or controlled by user

**Red flags (auto-CRITICAL):**
- Flashing content above 3 flashes/second threshold
- `prefers-reduced-motion` media query absent when animations exist
- No pause control on auto-playing carousel or video

**Evidence required to pass:**
- CSS/JS audit confirms `prefers-reduced-motion` media query wraps all animation
- Manual test with reduced-motion enabled shows no sliding, bouncing, or parallax
- All auto-playing media has visible pause button in first focus order position

---

## 4. Auditory Access

**WCAG criteria (AA):** 1.2.1, 1.2.2, 1.2.3, 1.2.5, 1.4.2

**JTBD checklist (code-level — enforceable):**
- [ ] Every `<video>` with speech has `<track kind="captions">` with valid `src` (1.2.2)
- [ ] Every `<audio>` has transcript section or link to transcript in adjacent markup (1.2.1)
- [ ] Media player controls (play, pause, volume, caption toggle) are keyboard-operable (2.1.1)
- [ ] Visual indicators accompany all auditory alerts/notifications
- [ ] No audio auto-plays, or auto-play has immediate pause/stop within first focusable element (1.4.2)

**JTBD checklist (content-level — flag for human verification):**
- [ ] Caption accuracy and timing — "Needs content author verification"
- [ ] Transcript includes speaker identification — "Needs content author verification"
- [ ] Audio descriptions cover visual-only information (1.2.3, 1.2.5) — "Needs content author verification"

**Red flags (auto-CRITICAL):**
- `<video>` with speech and no `<track>` element
- Media player with no keyboard controls
- Audio auto-plays with no visible stop control

**Severity calibration:**
- CRITICAL: Complete absence of captions/transcripts on media with speech
- MAJOR: Infrastructure present but incomplete (auto-generated placeholder captions)
- MINOR: Captions present but styling could improve (contrast, positioning)

**Evidence required to pass:**
- Each `<video>` with speech has `<track kind="captions">` with valid `src`
- Each audio element has adjacent transcript markup or visible link
- Keyboard test: Tab to player → Space plays/pauses → C toggles captions

---

## 5. Keyboard & Motor Access

**WCAG criteria (AA):** 1.3.4, 2.1.1, 2.1.2, 2.4.1, 2.4.3, 2.4.7, 2.4.13, 2.5.1, 2.5.2, 2.5.3, 2.5.7, 2.5.8

**JTBD checklist:**
- [ ] All interactive elements reachable and operable by keyboard alone (2.1.1)
- [ ] No keyboard traps — Tab and Shift+Tab always move focus forward/backward (2.1.2)
- [ ] Skip link present and functional, targets main content (2.4.1)
- [ ] Focus order follows logical reading/interaction sequence (2.4.3)
- [ ] Focus indicator visible: ≥2px outline, ≥3:1 contrast change against adjacent (2.4.7, 2.4.13)
- [ ] Multi-point gestures (pinch, multi-finger swipe) have single-pointer alternatives (2.5.1)
- [ ] Activation fires on up-event, not down-event — user can abort by moving pointer off (2.5.2)
- [ ] Visible label text matches accessible name for voice control compatibility (2.5.3)
- [ ] Every drag operation has a click-based alternative (2.5.7)
- [ ] Interactive targets ≥ 24x24 CSS px with adequate spacing (2.5.8)
- [ ] Content displays in both portrait and landscape unless specific orientation is essential (1.3.4)

**Red flags (auto-CRITICAL):**
- Interactive element unreachable by keyboard
- Keyboard trap (focus cannot escape a component)
- Drag-only interaction with no click alternative
- `outline: none` / `outline: 0` with no replacement focus style

**Evidence required to pass:**
- Full keyboard walkthrough: every interactive element reached via Tab, operated via Enter/Space/Arrows
- Focus indicator visible on every focused element (screenshot evidence)
- Drag operations tested: alternative click/button path completes same task

---

## 6. Screen Reader & Semantic Structure

**WCAG criteria (AA):** 1.1.1, 1.3.1, 1.3.2, 2.4.2, 2.4.4, 2.4.6, 3.1.1, 3.1.2, 3.3.1, 3.3.2, 4.1.2, 4.1.3

**JTBD checklist:**
- [ ] Landmark regions present and correctly used: `<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>` (1.3.1)
- [ ] Heading hierarchy is logical — no skipped levels, `<h1>` present, headings describe content (2.4.6)
- [ ] Every informative image has descriptive `alt`; decorative images have `alt=""` (1.1.1)
- [ ] DOM/source order matches visual reading order (1.3.2)
- [ ] Page has unique, descriptive `<title>` (2.4.2)
- [ ] Link text describes destination or purpose in context (2.4.4)
- [ ] `lang` attribute on `<html>` matches page language (3.1.1)
- [ ] Foreign-language phrases wrapped in `lang` attribute (3.1.2)
- [ ] Every form input has a visible `<label>` with programmatic association (3.3.2)
- [ ] Error messages identify the field in error and are associated via `aria-describedby` (3.3.1)
- [ ] Custom widgets use correct ARIA roles matching WAI-ARIA APG patterns (4.1.2)
- [ ] Status messages use `aria-live` with appropriate urgency level (4.1.3)
- [ ] SPA route changes: page title updates, focus managed, change announced

**Red flags (auto-CRITICAL):**
- No `<main>` landmark
- Form inputs without any label (no `<label>`, no `aria-label`, no `aria-labelledby`)
- Custom widget with no ARIA role
- Missing `lang` attribute on `<html>`

**Evidence required to pass:**
- Landmark audit: each region present and labeled if multiple of same type
- Heading outline: logical hierarchy with no skipped levels
- Image audit: every `<img>` has appropriate `alt`
- Form audit: every input has programmatic label, errors associated

---

## 7. Cognitive & Neurodivergent

**WCAG criteria (AA):** 1.3.5, 2.2.1, 2.4.5, 3.2.1, 3.2.2, 3.2.3, 3.2.4, 3.2.6, 3.3.3, 3.3.4, 3.3.7, 3.3.8
**Aspirational AAA:** 3.1.3, 3.1.4, 3.1.5, 3.3.6

**JTBD checklist:**
- [ ] Error messages suggest specific corrective action, not just "invalid input" (3.3.3)
- [ ] Multi-step forms do not re-ask information provided in earlier steps (3.3.7)
- [ ] Authentication does not require transcription, memorization, or puzzle-solving; paste and autofill work (3.3.8)
- [ ] Navigation appears in same relative position across all pages (3.2.3)
- [ ] Components with same function have consistent labels/icons across pages (3.2.4)
- [ ] Help mechanism appears in same location on every page (3.2.6)
- [ ] Focus on element does not auto-trigger context change (3.2.1)
- [ ] Changing form control value does not auto-submit or auto-navigate (3.2.2)
- [ ] Destructive actions have undo, confirmation, or review step (3.3.4)
- [ ] More than one way to reach any page (search, nav, sitemap, breadcrumbs) (2.4.5)
- [ ] Input fields for personal data have appropriate `autocomplete` attributes (1.3.5)
- [ ] Timeout warnings give ≥ 20 seconds to extend (2.2.1)
- [ ] Content avoids unexplained jargon, undefined abbreviations, complex sentences

**Neurodivergent-specific checks:**
- [ ] Page layout is predictable — main content in expected location, no layout shifts
- [ ] Visual hierarchy is clear — headings, spacing, and grouping guide reading order
- [ ] No autoplay media or unprompted modal dialogs
- [ ] Instructions don't rely on memory of previous steps

**Red flags (auto-CRITICAL):**
- CAPTCHA or cognitive function test with no accessible alternative
- Paste disabled on password or verification fields
- Multi-step form re-collecting name/email/address already provided
- Destructive action with no confirmation step

**Severity calibration:**
- CRITICAL: Auth requires cognitive test; paste blocked; no undo on destructive action
- MAJOR: Navigation inconsistency; no error suggestions; redundant entry
- MINOR: Jargon used but defined nearby; help location varies slightly
- ENHANCEMENT (AAA): Reading level could be simplified; abbreviations could be expanded

**Evidence required to pass:**
- Auth flow tested: paste works in password field; no CAPTCHA without alternative
- Multi-step form: data from step 1 pre-filled in step 3
- Navigation compared across 3+ pages: same elements in same order
- Destructive action: confirmation dialog or undo before irreversible commit
