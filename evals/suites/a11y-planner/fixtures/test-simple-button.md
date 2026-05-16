# Fixture: Simple Component Testing

## Feature Description

You're planning accessibility testing for a custom `<PrimaryButton>` React component used throughout a SaaS dashboard. The component renders a styled `<button>` element with an optional leading icon, a required text label, and an optional loading spinner state. The component is already implemented — you need a testing plan, not an implementation plan.

The component:
- Renders a native `<button>` with text content and optional `aria-label` override
- Accepts a `disabled` prop (sets HTML `disabled` attribute)
- Accepts an `isLoading` prop (replaces icon with spinner, sets `aria-busy="true"`)
- Is used in form submissions, inline actions, and toolbar contexts
- Has a custom focus ring defined in CSS (2px offset, brand color)

## Context

- **Platform:** React web application (TypeScript)
- **Existing code:** Yes, component exists — needs accessibility testing added
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Single reusable component (`PrimaryButton`)
- **Constraints:** Tests must run in CI (GitHub Actions); Playwright already in the project; team has basic WCAG knowledge but no screen reader testing experience

## Requirement

Create a comprehensive accessibility testing plan that a QA engineer with basic accessibility knowledge can execute. The plan should be structured enough for consistent execution across team members.

The plan should cover:
- Automated testing setup (axe-core, Playwright)
- Keyboard interaction testing
- Screen reader testing methodology
- Visual regression testing
- Focus management verification
- ARIA state testing
- Test prioritization and execution order
- Acceptance criteria
- a11y-critic review checkpoints

## Scope Hints

This is a **TRIVIAL** difficulty fixture — a single well-understood component with a straightforward interaction model. Expected plan length is 1-2 pages. Focus on:

1. Specific axe-core rules that apply to buttons (`button-name`, `color-contrast`)
2. Keyboard test script: Tab to focus, Enter/Space to activate, verify focus indicator visible
3. Screen reader verification: name, role, and state (disabled, loading) announced correctly
4. Concrete acceptance criteria (e.g., "focus indicator must be visible with minimum 3:1 contrast against adjacent background")
5. Testing the `disabled` and `isLoading` states specifically — not just the default state

## What Success Looks Like

An excellent plan would:
- ✓ Name specific axe-core rule IDs (`button-name`, `color-contrast`, `aria-allowed-attr`) not just "run axe-core"
- ✓ Provide step-by-step keyboard test script (Tab → verify focus ring → Enter → verify action)
- ✓ Document screen reader verification steps for NVDA (Insert+F7 to inspect element list) and VoiceOver (VO+Space to activate)
- ✓ Include acceptance criteria for the `disabled` state (screen readers should announce "dimmed" or "unavailable")
- ✓ Include acceptance criteria for the `isLoading` state (aria-busy="true" announced, spinner not read as decorative text)
- ✓ Specify Playwright assertion syntax for checking ARIA attributes
- ✓ Define when a11y-critic review is triggered in the development workflow
- ✓ Stay concise — 1-2 pages for a single component

## What Would Be Below Expectations

- ✗ "Run axe-core on the component" with no specific rules called out
- ✗ Keyboard test described as "verify keyboard works" without step-by-step script
- ✗ No screen reader verification steps (which SR, which keystrokes, what to listen for)
- ✗ Testing only the default state and ignoring `disabled` and `isLoading`
- ✗ Acceptance criteria that can't be measured ("the button should be accessible")
- ✗ Suggesting `tabindex="0"` verification — native `<button>` is focusable by default; prescribing tabindex is a symptom of not knowing the platform
- ✗ Visual regression plan that captures the entire page rather than the component in each state
