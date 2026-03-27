# Fixture: Live Region Content Updates

## Feature Description

You're planning accessibility for a component that displays real-time content updates using ARIA live regions:
- Notification banner that updates when events occur
- Status messages that appear and disappear dynamically
- Search results count that updates as user filters
- Loading states and completion messages
- Error alerts that need screen reader announcement
- Multiple live regions on the page (some polite, some assertive)

## Context

- **Platform:** React web application with real-time updates
- **Existing code:** No, new component pattern
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA, JAWS, VoiceOver, keyboard-only users
- **Scope:** Live region implementation pattern
- **Constraints:** Multiple concurrent updates possible; Timing of announcements critical; aria-live vs aria-alert decisions needed

## Requirement

Create a comprehensive accessibility design plan covering:
- aria-live regions (polite vs assertive)
- aria-atomic for complete vs partial updates
- aria-relevant for added/removed/text changes
- Timing of announcements (immediate vs debounced)
- Multiple live regions coordination
- Announcement clarity (what gets announced, when, how often)
- Error and success message strategies
- WCAG citations
- Testing approach for live announcements

## Scope Hints

This is a **MODERATE** difficulty fixture. Live regions require understanding of screen reader behavior and announcement timing. Plan should be 3 pages:

1. aria-live attributes (polite, assertive) with WCAG citations
2. aria-atomic and aria-relevant documentation
3. Announcement strategy (what gets announced, timing, frequency)
4. Error and success message handling
5. Multiple region coordination
6. Testing strategy for live announcements
7. Implementation guidance with code stubs

## What Success Looks Like

An excellent plan would:
- ✓ Document aria-live values with WCAG 4.1.3 citations
- ✓ Explain aria-atomic for complete message announcements
- ✓ Plan announcement timing (immediate vs debounced)
- ✓ Document aria-relevant for content changes
- ✓ Address error message announcements separately
- ✓ Plan multiple region coordination
- ✓ Include HTML structure examples
- ✓ Test cases for timing, multiple updates, interruptions

## What Would Be Below Expectations

- ✗ No WCAG 4.1.3 citation for status messages
- ✗ aria-live without explanation of polite vs assertive
- ✗ No mention of aria-atomic
- ✗ Vague about announcement timing
- ✗ No testing strategy for live regions
- ✗ Missing error handling in announcements
- ✗ No consideration of multiple updates
