# Fixture: Status Indicator Dots

## Feature Description

You're planning accessibility for a status indicator component used throughout a project management dashboard. Each list item (task, team member, deployment) displays a small colored dot on its left edge: green for active/online/passing, yellow for warning/pending/degraded, red for inactive/offline/failing. The dots appear in sidebar navigation, table rows, and card headers. There is no text label adjacent to the dot — the color is the only visual indicator of status. The design team wants to add an optional "compact mode" that hides text labels to reduce visual noise, leaving only the colored dots.

## Context

- **Platform:** React web application (internal ops dashboard)
- **Existing code:** Yes — `<StatusDot color="green|yellow|red" />` component already shipped; no accessibility attributes present
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Single reusable `StatusDot` component and its usage in list items, table rows, and card headers
- **Constraints:** Design team requires the dot shape and color system remain unchanged; compact mode is a required feature; the same component must work in both full-label and compact modes

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- Semantic structure
- ARIA implementation (pattern mapping, attributes)
- Keyboard interaction model
- Focus management
- State communication
- Visual accessibility (contrast, non-color indicator)
- Content accessibility (text alternatives, icon labeling)
- Testing strategy
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is a **TRIVIAL** difficulty fixture — a well-known WCAG 1.4.1 failure with a small, well-understood solution space. The plan should be 1-2 pages. Focus on:

1. Why color alone fails WCAG 1.4.1 and what the non-color alternative must be
2. Choosing the right ARIA pattern for status semantics (role="img" with aria-label vs. visually-hidden text vs. title attribute — pick one and justify)
3. Contrast ratios for the dot color values against their backgrounds (1.4.11 Non-Text Contrast)
4. Compact mode: ensuring the text label is hidden visually but not from assistive technology
5. Avoiding over-engineering — this does not need keyboard interaction or focus management sections beyond a note that the dot itself is not focusable

## What Success Looks Like

An excellent plan would:
- ✓ Cite WCAG 1.4.1 (Use of Color) as the core failure and explain the user impact
- ✓ Specify a concrete non-color indicator strategy: either a visually-hidden `<span>` text label or `role="img" aria-label="Active"` on the dot element
- ✓ Cite WCAG 1.4.11 (Non-Text Contrast) and specify the minimum 3:1 ratio for the dot against its background
- ✓ Cite WCAG 1.1.1 (Non-Text Content) for the icon-as-image pattern
- ✓ Address compact mode explicitly: CSS `clip` / `sr-only` technique so the label is visually hidden but present for screen readers
- ✓ Document three status values and their text equivalents (green → "Active", yellow → "Warning", red → "Error" or equivalent — label set must match product terminology)
- ✓ Note that the dot itself is presentational (`aria-hidden="true"` on the SVG or `<span>`) when a sibling text label is present
- ✓ Include a test case for "change system color theme to high-contrast Windows — are status meanings still conveyed?"

## What Would Be Below Expectations

- ✗ `aria-label="red dot"` — describes the visual artifact, not the semantic status
- ✗ Only adding `title` attribute — tooltip is not a reliable screen reader announcement across all ATs
- ✗ Adding a text label without `aria-hidden="true"` on the dot, causing double-announcement ("green circle Active")
- ✗ No mention of the compact mode scenario
- ✗ Checking dot-to-white contrast but not dot-to-background contrast (1.4.11 requires 3:1 against adjacent colors)
- ✗ Over-engineering with aria-live regions or focus management (the dot is a static indicator, not an interactive widget)
- ✗ Five pages of planning for a 15-line component fix
