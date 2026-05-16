# Fixture: Dark Mode Toggle

## Feature Description

You're planning accessibility for a dark mode implementation on a public-facing SaaS product documentation site. The site currently has a light-mode-only design system. The feature has two parts: a toggle button in the top navigation bar (sun/moon icon, no text label), and a system preference detection mechanism that applies dark mode on first load if `prefers-color-scheme: dark` is set. The toggle persists the user's choice to `localStorage`. The design team has provided dark-mode color tokens but has not validated contrast ratios in the dark palette. The focus indicator is currently implemented as a 2px solid `#0066CC` outline, which works in light mode but has not been evaluated against dark backgrounds.

## Context

- **Platform:** React + CSS custom properties (design tokens via `data-theme` attribute on `<html>`)
- **Existing code:** Yes — light mode design system is complete; dark mode color tokens are drafted but untested for contrast; toggle button component exists with icon only
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Dark mode toggle button, system preference detection/persistence, and contrast validation framework for the dark color token set
- **Constraints:** CSS custom properties architecture must remain; `data-theme` attribute approach must remain; no JavaScript-in-CSS solutions; forced-colors mode must be tested but is a separate concern from dark mode

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- Semantic structure
- ARIA implementation (pattern mapping, attributes)
- Keyboard interaction model
- Focus management
- State communication
- Visual accessibility (contrast in both modes, focus indicator in both modes, forced-colors)
- Content accessibility
- Testing strategy
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is a **MODERATE** difficulty fixture — three distinct concerns that must all be addressed: the toggle button ARIA pattern, contrast validation in both modes, and the distinction between dark mode and forced-colors. The plan should be 3-4 pages. Focus on:

1. Toggle button ARIA pattern: `aria-pressed` (toggle button) vs. `role="switch"` — pick one with justification; include `aria-label` since the button is icon-only
2. Contrast ratios in dark mode: the plan should call for validation of text-on-background, interactive element borders, and focus indicator against dark backgrounds — specific minimum ratios (4.5:1 for text, 3:1 for non-text)
3. Focus indicator visibility in dark mode: the existing `#0066CC` outline may not meet 3:1 against a dark background; plan must address this specifically
4. Forced-colors mode: a separate CSS media query (`forced-colors: active`) that overrides custom properties — plan must note this is a distinct mechanism from dark mode and requires its own testing, but does not need a full redesign
5. No information loss between modes: if any content is expressed via color alone in light mode (1.4.1), dark mode does not fix it

## What Success Looks Like

An excellent plan would:
- ✓ Specify `aria-pressed` (toggle button pattern) or `role="switch"` for the toggle, with explicit justification and `aria-label` for the icon-only button
- ✓ Cite WCAG 1.4.3 (Contrast — Minimum) and 1.4.11 (Non-Text Contrast) for dark palette validation requirements
- ✓ List the specific contrast requirements: 4.5:1 for normal text, 3:1 for large text, 3:1 for interactive element borders and focus indicators
- ✓ Flag the existing focus indicator (`#0066CC` outline) as requiring re-evaluation against dark backgrounds
- ✓ Identify WCAG 2.4.7 (Focus Visible) as applying to both modes independently
- ✓ Distinguish `prefers-color-scheme: dark` (dark mode preference) from `forced-colors: active` (Windows High Contrast / increased contrast mode) — note they are different mechanisms requiring different solutions
- ✓ Address localStorage persistence: the toggle state persists but `aria-pressed` must reflect the live DOM state, not a stale localStorage value
- ✓ Include a test matrix: contrast ratios in light mode AND dark mode for the key token pairs

## What Would Be Below Expectations

- ✗ Conflating dark mode (`prefers-color-scheme: dark`) with forced-colors mode — they are different mechanisms
- ✗ Checking contrast only in light mode (dark mode palette has not been validated)
- ✗ Using `aria-label="Toggle dark mode"` on a button that has `aria-pressed` but not checking the current state announcement
- ✗ Inverting light-mode colors without checking whether the inverted palette meets contrast requirements
- ✗ No mention of the focus indicator re-evaluation in dark mode
- ✗ Skipping the localStorage/aria-pressed synchronization issue
- ✗ Treating forced-colors as "dark mode with higher contrast" — they are architecturally different
