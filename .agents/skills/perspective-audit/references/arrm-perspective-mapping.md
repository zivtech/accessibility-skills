# ARRM Perspective-to-Role Mapping

Reference file for routing findings to responsible roles.
Based on W3C WAI ARRM (https://www.w3.org/WAI/planning/arrm/).

---

## Role Mapping

| Perspective | ARRM Primary Owner | ARRM Secondary |
|---|---|---|
| Magnification & Reflow | Visual Design (layout, spacing, reflow) | Front-End Dev (CSS implementation) |
| Environmental Contrast | Visual Design (color, contrast ratios) | Front-End Dev (forced-colors support) |
| Vestibular & Motion | UX Design (animation decisions, motion policy) | Front-End Dev (prefers-reduced-motion, pause controls) |
| Auditory Access | Content Author (captions, transcripts, descriptions) | Front-End Dev (media player keyboard access) |
| Keyboard & Motor | Front-End Dev (keyboard implementation, ARIA) | UX Design (focus order, interaction design) |
| Screen Reader & Semantic | Front-End Dev (semantic HTML, ARIA, live regions) | Content Author (alt text, heading text, link text) |
| Cognitive & Neurodivergent | Content Author (plain language) + UX Design (consistent patterns) | Front-End Dev (autocomplete, error association) |

---

## Decision Tree

Route each finding through this tree to identify the primary responsible role:

```
1. Is it about CONTENT (captions, alt text, transcripts, language, reading level, labels)?
   → Primary: Content Author
   → Secondary: whoever implements the markup

2. Is it about INTERACTION PATTERNS (focus order, animation, gestures, navigation consistency)?
   → Primary: UX Design
   → Secondary: Front-End Dev (implements the pattern)

3. Is it about VISUAL PRESENTATION (contrast, spacing, focus indicators, color use, reflow)?
   → Primary: Visual Design
   → Secondary: Front-End Dev (implements CSS)

4. Is it about IMPLEMENTATION (semantic HTML, ARIA roles, keyboard handlers, media player controls)?
   → Primary: Front-End Dev
   → Secondary: UX Design (defines the intended pattern)
```

If a finding spans multiple categories, use the **first matching** rule.

---

## Finding Output Format

When the perspective audit produces a finding, tag it:

```
**Finding:** [description]
**WCAG:** [criterion number and name]
**Perspective:** [which perspective surfaced this]
**Severity:** CRITICAL | MAJOR | MINOR | ENHANCEMENT
**Route to:** [ARRM primary role] (secondary: [role])
**Evidence:** [what was observed]
**Fix:** [recommended action]
```

---

## ARRM Role Definitions (from W3C)

| Role | Scope | Example Titles |
|---|---|---|
| Content Author | Text, media, alt text, captions, transcripts | Content Strategist, UX Writer, Video Producer |
| UX Design | Information architecture, wireframes, interaction patterns | UX Designer, Product Designer, Service Designer |
| Visual Design | Look and feel, color, typography, layout, spacing | Visual Designer, UI Designer, Graphic Designer |
| Front-End Dev | HTML, CSS, JavaScript, ARIA, keyboard handling | Front-End Developer, Web Developer, Full-Stack Dev |
