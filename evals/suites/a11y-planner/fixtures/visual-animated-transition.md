# Fixture: Animated Page Transition

## Feature Description

You're planning accessibility for a page transition system in a React SPA (single-page application). When a user navigates between routes, the outgoing page slides out to the left while the incoming page slides in from the right — a 300ms CSS transform animation. The product team also wants a "fade" variant (cross-dissolve, 200ms) for modal-like overlay routes. Both transitions use `framer-motion` for the animation layer. The app has no existing motion preference detection. After navigation, the new page's content should be available to screen readers and focus should land somewhere meaningful.

## Context

- **Platform:** React SPA with React Router v6 and framer-motion
- **Existing code:** Yes — transition animation is implemented with framer-motion `AnimatePresence`; no `prefers-reduced-motion` check, no post-navigation focus management
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Route transition wrapper component (`PageTransition`) applied to all routes; does not include in-page micro-animations
- **Constraints:** framer-motion must remain as the animation library; animation duration is designer-specified at 300ms (slide) and 200ms (fade); both slide and fade variants must be supported; the route change itself is instant (no server fetch delay)

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- Semantic structure
- ARIA implementation (pattern mapping, attributes)
- Keyboard interaction model
- Focus management
- State communication
- Visual accessibility (motion reduction, animation limits)
- Content accessibility
- Testing strategy
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is a **MODERATE** difficulty fixture — two independent concerns (motion sensitivity and post-navigation focus management) must both be addressed. The plan should be 3-4 pages. Focus on:

1. `prefers-reduced-motion` detection: what to replace animation with (instant switch or cross-fade at reduced duration), not just disabling it; cite WCAG 2.3.3 and SC 2.2.2
2. Focus management after route change: where does focus go, what technique (ref to `<main>`, document title announcement, or `aria-live` region for route announcements)
3. Content visibility during animation: is outgoing content in the DOM while incoming content renders, and can a screen reader accidentally read the outgoing page?
4. Animation duration compliance: 300ms slide is within WCAG 2.3.3 limits, but document the threshold
5. framer-motion implementation: how to pass `useReducedMotion()` hook result to `AnimatePresence` variants

## What Success Looks Like

An excellent plan would:
- ✓ Cite WCAG 2.3.3 (Animation from Interactions) and explain that user-triggered transitions must respect `prefers-reduced-motion`
- ✓ Distinguish between "disable animation" and "replace with instant transition or short cross-fade" — not just `animation: none`
- ✓ Specify `framer-motion`'s `useReducedMotion()` hook as the mechanism for reading system preference
- ✓ Define the reduced-motion alternative for the slide variant (instant route switch or ≤150ms opacity fade)
- ✓ Address post-navigation focus management: document a concrete strategy (focus `<main>` heading, route announcer pattern, or document title update with `<div aria-live="polite">`)
- ✓ Address DOM overlap: explain that `AnimatePresence` keeps outgoing page in DOM during exit animation and plan `aria-hidden="true"` on the exiting element or `inert` attribute
- ✓ Cite WCAG 2.4.3 (Focus Order) for the requirement that focus not remain on a now-invisible element
- ✓ Include test cases: keyboard nav through transition, screen reader announcement of new page, motion preference toggle

## What Would Be Below Expectations

- ✗ Treating `prefers-reduced-motion` as binary: "check the media query and disable animation" without specifying what the fallback experience is
- ✗ No focus management plan — just "animation plays, user continues navigating"
- ✗ Missing the DOM overlap problem (outgoing page readable by screen reader during exit animation)
- ✗ Citing only WCAG 2.3.3 without addressing that 300ms < the 5-second SC 2.2.2 threshold (worth noting they are different concerns)
- ✗ No mention of the framer-motion `useReducedMotion()` API or equivalent React hook
- ✗ No test case for reduced-motion preference (how to simulate in browser devtools)
- ✗ Over-focusing on animation design and under-addressing focus/AT concerns
