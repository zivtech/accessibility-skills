# Front-End Development

## Responsibility

Front-end development translates design and content into accessible HTML, CSS, and JavaScript. This role implements semantic markup, keyboard interactions, ARIA attributes, focus management, live regions, and the technical layer that makes interfaces operable for assistive technology users.

## Also Known As

Front-end engineer, full-stack developer, accessibility specialist, web developer, back-end engineer (when touching templates/output).

## What This Role Sees

- Whether semantic HTML elements are used correctly (or divs substitute for native elements)
- Whether all interactive elements are keyboard-accessible
- Whether focus management works in modals, dialogs, and dynamic content
- Whether ARIA attributes are correct, complete, and necessary
- Whether DOM order matches visual order
- Whether tab order is logical and predictable
- Whether CSS breaks in high-contrast or zoom modes
- Whether live regions announce dynamic updates appropriately
- Whether form controls have proper label associations
- Whether custom widgets implement the complete APG interaction model

## Blind Spots (What This Role Misses)

| Gap | Ask instead |
|-----|-------------|
| Whether the content makes sense to users | Content Authoring |
| Whether the interaction pattern is the right one | UX Design |
| Whether the visual design meets contrast requirements | Visual Design |
| Whether the implementation works with real AT in practice | Testing |

## ARRM Task Ownership

### Primary (90+ tasks)

Second-largest role in the ARRM data. Key areas:
- **Semantic HTML** — Proper element usage, document structure, lists, tables (1.3.1, 1.3.2)
- **ARIA** — Roles, states, properties, name/description computation (4.1.2)
- **Keyboard** — All keyboard interaction handlers, focus trapping, roving tabindex (2.1.1, 2.1.2)
- **Focus management** — Focus indicators CSS, focus trapping logic, restoration on dismiss (2.4.7, 2.4.11, 2.4.13)
- **Live regions** — aria-live, role=alert, status, log — appropriate politeness (4.1.3)
- **Forms** — Label associations, error associations, autocomplete attributes (1.3.5, 3.3.1, 3.3.2)
- **Media** — Player keyboard controls, caption rendering, audio description tracks (1.2.x)
- **Responsive** — CSS reflow, viewport meta, text resize handling (1.4.4, 1.4.10)
- **Motion** — prefers-reduced-motion media query, pause controls (2.2.2, 2.3.1)

### Secondary (50+ tasks)

Supports UX Design on interaction patterns, Visual Design on CSS contrast/forced-colors, Content Authoring on markup for alt text/headings.

### Contributor (20+ tasks)

Advises on content structure decisions, media alternative approaches, CAPTCHA implementations.

## Key WCAG Criteria

| SC | Level | What it requires |
|----|-------|-----------------|
| 4.1.2 | A | Name, role, value for all UI components |
| 1.3.1 | A | Info and relationships programmatically determined |
| 2.1.1 | A | Keyboard accessible — no mouse-only interactions |
| 2.1.2 | A | No keyboard trap |
| 2.4.7 | AA | Focus visible |
| 1.4.4 | AA | Resize text up to 200% without loss |
| 1.4.10 | AA | Reflow — single-column at 320px |
| 4.1.3 | AA | Status messages programmatically determined |
| 1.3.5 | AA | Identify input purpose (autocomplete) |
| 2.4.11 | AA | Focus not obscured (minimum) |

## Review Checklist

When reviewing from this role's perspective, evaluate:

1. **Semantic HTML** — Are native elements used where they fit (`<button>`, `<dialog>`, `<details>`, `<nav>`, `<main>`)? Is ARIA only supplementing, never replacing, available HTML semantics?
2. **ARIA completeness** — If a custom widget uses ARIA, is the full APG pattern implemented? (Not just role, but states, properties, keyboard interaction model, and name computation.)
3. **Keyboard** — Can every interactive element be reached and operated by keyboard? Are custom key handlers implemented per APG? No positive tabindex?
4. **Focus management** — On modal open: focus moves to first focusable or the dialog itself. On dismiss: focus returns to trigger. Focus is trapped inside while open. Escape closes.
5. **Live regions** — Dynamic updates that don't move focus: are they wrapped in appropriate `aria-live` (polite for status, assertive for errors)? Are they present in DOM before content changes?
6. **Label computation** — Every form control has an accessible name (explicit `<label>`, aria-label, or aria-labelledby). Every group has a group label. Placeholder is never the only label.
7. **Error association** — Error messages use `aria-describedby` pointing to the invalid field. `aria-invalid="true"` is set on the field.
8. **DOM order** — Source order matches visual order. Flexbox/grid `order` property does not create tab-order mismatches.
9. **CSS accessibility** — Focus indicators use outline (not removed), forced-colors mode tested, no `display:none` on focus indicators, no `overflow:hidden` clipping focused content.
10. **Responsive** — No horizontal scroll at 320px viewport. Content at 200% zoom has no overlap. Text spacing overrides don't break layout.

## Collaboration Points

| Role | What to share | What to ask them |
|------|---------------|-----------------|
| UX Design | Implementation constraints | "Is this pattern achievable with native elements?" |
| Visual Design | CSS implementation details | "Do these values meet the contrast specification?" |
| Content Authoring | Markup structure | "Is the heading level appropriate here?" |
| Testing | Implementation details for AT testing | "Can you verify this works in NVDA/VoiceOver?" |
| Business Analysis | Technical feasibility of requirements | "The CAPTCHA alternative needs server-side support — is that in scope?" |
