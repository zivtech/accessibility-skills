# UX Design

## Responsibility

UX design determines whether interactions, navigation, and information architecture work for all users — including people with cognitive, motor, and sensory disabilities. This role owns the interaction patterns, focus order, error flows, state communication design, and consistency that make experiences navigable and predictable.

## Also Known As

UX designer, interaction designer, user researcher, product designer, information architect, service designer.

## What This Role Sees

- Whether navigation patterns are logical and predictable
- Whether interaction patterns match WAI-ARIA APG expectations
- Whether error states and success states are communicated clearly
- Whether forms guide users through completion and recovery
- Whether dynamic content updates are announced appropriately
- Whether timing and animation respect user preferences
- Whether focus order matches visual/reading order
- Whether consistent patterns are used across similar interactions
- Whether skip links and landmark navigation exist
- Whether personalization options exist (font size, contrast, motion)

## Blind Spots (What This Role Misses)

| Gap | Ask instead |
|-----|-------------|
| Whether the code matches the design intent | Front-End Development |
| Whether the writing is clear and understandable | Content Authoring |
| Whether visual contrast meets minimums | Visual Design |
| Whether the implementation works with real AT | Testing |

## ARRM Task Ownership

### Primary (96 tasks)

This is the largest role in the ARRM data. Key areas:
- **Forms** — Error prevention, error identification, labels, instructions, input purpose (3.3.1–3.3.9)
- **Navigation** — Consistent navigation, multiple ways, focus order, skip links (2.4.1–2.4.13)
- **Interaction patterns** — Keyboard operability, no keyboard traps, pointer gestures (2.1.1, 2.1.2, 2.5.1–2.5.4)
- **Predictability** — On focus, on input, consistent identification, change on request (3.2.1–3.2.6)
- **Timing** — Adjustable timing, pause/stop/hide, no timing essential (2.2.1–2.2.6)
- **Status** — Status messages communicated without focus change (4.1.3)
- **Structure** — Info and relationships, meaningful sequence, identify purpose (1.3.1, 1.3.2, 1.3.5, 1.3.6)

### Secondary (40+ tasks)

Supports Visual Design on layout/reflow decisions, Content Authoring on heading hierarchy and link text patterns, Front-End Dev on ARIA pattern selection.

### Contributor (15+ tasks)

Advises on alt text strategy, language identification, and media alternatives approach.

## Key WCAG Criteria

| SC | Level | What it requires |
|----|-------|-----------------|
| 2.1.1 | A | All functionality keyboard-accessible |
| 2.1.2 | A | No keyboard traps |
| 2.4.3 | A | Focus order matches meaning |
| 2.4.7 | AA | Focus visible |
| 3.2.1 | A | No unexpected context change on focus |
| 3.2.2 | A | No unexpected context change on input |
| 3.2.3 | AA | Consistent navigation across pages |
| 3.2.6 | AA | Consistent help location |
| 3.3.1 | A | Error identification |
| 3.3.2 | A | Labels or instructions |
| 3.3.3 | AA | Error suggestion |
| 3.3.4 | AA | Error prevention (legal, financial, data) |
| 4.1.3 | AA | Status messages via role/property, not focus |

## Review Checklist

When reviewing from this role's perspective, evaluate:

1. **Pattern selection** — Does the interaction match a WAI-ARIA APG pattern? If custom, is the interaction model documented and defensible?
2. **Focus management** — Where does focus go on open/close/error/success? Is it intentional or accidental? Does it return to trigger on dismiss?
3. **State communication** — Are expanded/collapsed, selected/unselected, checked/unchecked, loading/loaded states communicated programmatically?
4. **Error recovery** — Do error messages explain what went wrong, where, and how to fix? Are they associated with the right field?
5. **Consistency** — Are similar interactions handled the same way throughout? Same patterns, same positions, same terminology?
6. **Keyboard completeness** — Can every interaction be completed without a mouse? Are custom keyboard shortcuts documented?
7. **Focus order** — Does tab order match visual/reading order? Are dynamically inserted elements in logical position?
8. **Timing** — Any time-limited interactions: can they be extended? Are users warned before timeout?
9. **Status updates** — Do loading states, success confirmations, and live updates reach screen reader users without stealing focus?
10. **Skip navigation** — Can users bypass repeated content blocks? Are landmarks properly defined?

## Collaboration Points

| Role | What to share | What to ask them |
|------|---------------|-----------------|
| Visual Design | Focus indicator specs, state visuals | "Does the visual treatment meet contrast for all states?" |
| Front-End Dev | Pattern requirements, ARIA expectations | "Is this pattern implementable with native elements?" |
| Content Authoring | Error message requirements | "Is this error message clear enough for recovery?" |
| Testing | Expected interaction flows | "Does the flow work as designed in real AT?" |
| Business Analysis | Feature requirements, user stories | "Do requirements include accessibility acceptance criteria?" |
