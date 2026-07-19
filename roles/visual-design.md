# Visual Design

## Responsibility

Visual design determines whether the visual presentation of content is accessible — contrast ratios, text readability at zoom, focus indicator visibility, target sizes, motion handling, and whether information is conveyed through visual means alone.

## Also Known As

Visual designer, UI designer, graphic designer, brand designer, motion designer.

## What This Role Sees

- Text contrast ratios (4.5:1 normal, 3:1 large text)
- Non-text element contrast (3:1 for UI components, focus indicators, form borders)
- Information conveyed through color alone (no supplementary encoding)
- Text readability at 200% zoom and 400% reflow
- Focus indicator visibility and sufficiency (2px perimeter, 3:1 contrast)
- Animation and motion respect for `prefers-reduced-motion`
- Target sizes meeting 24×24 CSS pixel minimum
- Forced-colors / high-contrast mode rendering
- Images of text that should be actual text
- Spacing and layout under text spacing overrides

## Blind Spots (What This Role Misses)

| Gap | Ask instead |
|-----|-------------|
| Whether semantic HTML matches the visual presentation | Front-End Development |
| Whether content is clear and understandable | Content Authoring |
| Whether interaction patterns work with keyboard/screen reader | UX Design |
| Whether the page works with real assistive technology | Testing |

## ARRM Task Ownership

### Primary (30 tasks)

Key areas:
- **Contrast** — Text contrast, non-text contrast, UI component boundaries (1.4.3, 1.4.6, 1.4.11)
- **Color use** — Color not sole indicator of meaning (1.4.1)
- **Focus indicators** — Visible, sufficient contrast, minimum area (2.4.7, 2.4.11, 2.4.13)
- **Target size** — Minimum 24×24 CSS pixels (2.5.5, 2.5.8)
- **Reflow** — Layout adapts without horizontal scroll at 320px (1.4.10)
- **Text spacing** — Content adapts to user overrides (1.4.12)
- **Motion** — Animations respect reduced-motion preference (2.3.3)

### Secondary (22 tasks)

Supports UX Design and Front-End Dev on:
- Hover/focus content persistence and dismissibility (1.4.13)
- Zoom behavior up to 200% without loss (1.4.4)
- Orientation flexibility (1.3.4)
- High-contrast mode rendering

### Contributor (8 tasks)

Advises on sensory characteristics in instructions (1.3.3), consistent identification (3.2.4), and status messages (4.1.3).

## Key WCAG Criteria

| SC | Level | What it requires |
|----|-------|-----------------|
| 1.4.3 | AA | Normal text ≥ 4.5:1, large text ≥ 3:1 |
| 1.4.11 | AA | Non-text contrast ≥ 3:1 (UI components, graphical objects) |
| 1.4.1 | A | Color not sole means of conveying information |
| 1.4.10 | AA | Reflow — no 2D scrolling at 320px equivalent |
| 1.4.12 | AA | Text spacing overrides don't break content |
| 2.4.7 | AA | Focus indicator visible |
| 2.4.11 | AA | Focus not obscured (minimum) |
| 2.4.13 | AAA | Focus appearance — minimum area and contrast |
| 2.5.8 | AA | Target size ≥ 24×24 CSS px |

## Review Checklist

When reviewing from this role's perspective, evaluate:

1. **Contrast** — Measure actual ratios for body text, headings, placeholder text, disabled states, UI borders, icons, and focus indicators
2. **Color independence** — Every color-coded state (error, success, warning, selected, active) has a non-color supplement (icon, pattern, text, shape)
3. **Zoom resilience** — Content at 200% has no overflow, truncation, or overlap; at 400% reflow content is single-column without horizontal scroll
4. **Focus visibility** — Every focusable element has a visible focus indicator that meets 3:1 contrast against adjacent colors and covers ≥2px of the perimeter
5. **Target size** — All interactive targets ≥ 24×24 CSS px, or have sufficient spacing from adjacent targets
6. **Motion safety** — All animations: can be paused/stopped, respect `prefers-reduced-motion`, and no content flashes more than 3 times per second
7. **Forced colors** — Interface remains functional in Windows High Contrast / forced-colors: icons visible, focus indicators present, interactive elements distinguishable
8. **Text spacing** — Applying 1.5× line height, 2× paragraph spacing, 0.12em letter spacing, 0.16em word spacing causes no content loss

## Collaboration Points

| Role | What to share | What to ask them |
|------|---------------|-----------------|
| Front-End Dev | CSS values, token specifications | "Can forced-colors mode be tested?" |
| Content Authoring | Visual hierarchy requirements | "Does heading visual weight match semantic level?" |
| UX Design | Focus indicator design specs | "Is the interaction pattern clear without color?" |
| Testing | Contrast measurements, zoom screenshots | "Does this pass in real AT at these values?" |
| Business Analysis | Accessibility metrics dashboard | "Are we tracking contrast compliance over time?" |
