# Perspective Agents — Domain Sampling Strategy

## Sampling Goals

1. **Perspective coverage:** Every perspective is the primary target of at least 2 fixtures
2. **Dimension balance:** 10 new-dimension + 6 existing-dimension + 5 CLEAN + 4 ADVERSARIAL
3. **Component type diversity:** Forms, media, widgets, content, navigation, data display
4. **External sourcing:** At least 50% from real audit failures (WebAIM, Deque, GitHub issues)
5. **No overlap with a11y-critic suite:** All fixtures are new designs

## Fixture Allocation by Perspective

| Perspective | Primary Fixtures | Secondary Fixtures | Total Exposure |
|---|---|---|---|
| Magnification & Reflow | 2 | 3 | 5 |
| Environmental Contrast | 2 | 3 | 5 |
| Vestibular & Motion | 2 | 2 | 4 |
| Auditory Access | 2 | 1 | 3 |
| Keyboard & Motor | 3 | 4 | 7 |
| Screen Reader & Semantic | 3 | 4 | 7 |
| Cognitive & Neurodivergent | 2 | 3 | 5 |

Keyboard and Screen Reader have higher allocation because they appear as both new-dimension and existing-dimension (regression) fixtures.

## Fixture Allocation by Category

### HAS-BUGS — New Dimensions (10 fixtures)

| # | Fixture | Primary Perspective | Domain |
|---|---|---|---|
| 1 | Video tutorial without captions | Auditory | Media & Content |
| 2 | Product carousel with autoplay | Vestibular | Interactive Widgets |
| 3 | Podcast player with audio-only content | Auditory | Media & Content |
| 4 | Data visualization with color-only encoding | Contrast | Data Display |
| 5 | Animated onboarding flow | Vestibular | Interactive Widgets |
| 6 | Dense admin panel with jargon | Cognitive | Data Display |
| 7 | Image gallery with small targets | Magnification | Interactive Widgets |
| 8 | Map interface with zoom controls | Magnification | Interactive Widgets |
| 9 | Chat interface with cognitive load | Cognitive | Interactive Widgets |
| 10 | Multi-column pricing table | Contrast | Content & Layout |

### HAS-BUGS — Existing Dimensions (6 fixtures)

| # | Fixture | Primary Perspective | Domain |
|---|---|---|---|
| 11 | Multi-step checkout form | Screen Reader | Form & Validation |
| 12 | Custom select/combobox | Keyboard | Interactive Widgets |
| 13 | Modal with broken focus trap | Keyboard | Interactive Widgets |
| 14 | Data table with sortable columns | Screen Reader | Data Display |
| 15 | Search results with dynamic update | Screen Reader | Dynamic Content |
| 16 | Tab panel with arrow keys | Keyboard | Interactive Widgets |

### CLEAN (5 fixtures)

| # | Fixture | Why Clean | Domain |
|---|---|---|---|
| 17 | Article page with proper a11y | All dimensions correct | Content & Layout |
| 18 | Login form with good labels | Form a11y correct | Form & Validation |
| 19 | Navigation menu with landmarks | Keyboard + SR correct | Navigation |
| 20 | Media player with captions | Auditory dimension correct | Media & Content |
| 21 | Dashboard with text status labels | Contrast dimension correct | Data Display |

### ADVERSARIAL (4 fixtures)

| # | Fixture | Why Adversarial | Domain |
|---|---|---|---|
| 22 | Color-only status indicators | Passes contrast, fails color-only | Data Display |
| 23 | Infinite scroll with cognitive load | Technically accessible, cognitively hostile | Dynamic Content |
| 24 | Hover-reveal navigation | Works for mouse, subtle keyboard gap | Navigation |
| 25 | Auto-complete with fast timeout | WCAG 2.2.1 edge case | Form & Validation |

## Pilot Fixtures (5 of 25)

Selected to cover: one new-dimension HAS-BUGS, one existing-dimension HAS-BUGS, one CLEAN, one ADVERSARIAL, plus one additional new-dimension.

| # | Fixture | Category | Primary Perspective |
|---|---|---|---|
| P1 | Video tutorial without captions | HAS-BUGS (new) | Auditory |
| P2 | Product carousel with autoplay | HAS-BUGS (new) | Vestibular |
| P3 | Article page (clean) | CLEAN | All |
| P4 | Multi-step checkout form | HAS-BUGS (existing) | Screen Reader |
| P5 | Color-only status indicators | ADVERSARIAL | Contrast |

## External Source Targets

- **WebAIM Million:** Common failures in headings, alt text, form labels, color contrast
- **Deque University case studies:** Complex widget patterns, ARIA misuse
- **GitHub accessibility issues:** Real component bugs from popular React libraries
- **W3C WAI tutorials:** Patterns that are commonly implemented incorrectly
- **CivicActions persona scenarios:** Real-world usage patterns from the persona research

Target: 13+ of 25 fixtures sourced from or inspired by external audit data.
