# Testing

## Responsibility

Testing verifies that accessibility implementations actually work — with real assistive technology, real keyboards, real screen readers, and real user flows. This role validates the work of all other roles through automated scans, manual testing, AT testing, and regression checking.

## Also Known As

QA engineer, accessibility tester, quality assurance, test engineer, AT specialist, usability tester.

## What This Role Sees

- Whether automated tools (axe-core, Pa11y, Lighthouse) report violations
- Whether keyboard navigation actually works through entire flows
- Whether screen readers announce content correctly and in logical order
- Whether implementations match ARIA pattern expectations from APG
- Whether previously-fixed issues have regressed
- Whether test coverage exists for accessibility-critical flows
- Whether different AT/browser combinations produce different results

## Blind Spots (What This Role Misses)

| Gap | Ask instead |
|-----|-------------|
| Whether the underlying design decision is correct | UX Design |
| Whether the content is the right content | Content Authoring |
| Whether contrast values were intentional design choices | Visual Design |
| Whether requirements exist for what's being tested | Business Analysis |

## ARRM Task Ownership

### Primary (0 tasks)

Testing has zero primary tasks in the ARRM data. This reflects its nature as a verification role — it validates the work of other roles rather than producing its own accessibility artifacts.

### Secondary (varies)

Supports all other roles by verifying their outputs work in practice.

### Contributor (varies)

Advises all roles on what is testable, what breaks in real AT, and what has regressed.

## Key WCAG Criteria

Testing verifies ALL criteria. Its unique value is in criteria that only surface in real AT:

| SC | Level | Why testing catches it |
|----|-------|----------------------|
| 4.1.2 | A | Name computation differences across AT |
| 4.1.3 | AA | Live region announcement timing varies by AT |
| 2.1.1 | A | Keyboard traps only appear in actual traversal |
| 1.3.1 | A | Semantic relationships that look right in DOM but announce wrong |
| 2.4.3 | A | Focus order issues only visible in real tab traversal |
| 2.4.7 | AA | Focus indicator missing only in certain states |

## Review Checklist

When reviewing from this role's perspective, evaluate:

1. **Automated scan results** — Has axe-core / Pa11y been run? Are there zero critical/serious violations? Are violations triaged, not just suppressed?
2. **Keyboard traversal** — Every page tested with keyboard-only navigation. All interactive elements reachable, operable, and escapable. Tab order logical.
3. **Screen reader testing** — Tested with at least one SR (NVDA on Windows, VoiceOver on macOS). Headings, landmarks, forms, and dynamic content announce correctly.
4. **Regression** — Previously fixed a11y issues have tests preventing regression. New features don't break existing accessibility.
5. **Coverage** — All critical user flows have accessibility test coverage. Not just happy path — error states, edge cases, empty states tested.
6. **Cross-AT** — Results consistent across NVDA, VoiceOver, JAWS (when possible). Known differences documented.
7. **Zoom testing** — Page tested at 200% and 400% zoom. Content readable, interactive elements usable.
8. **Forced colors** — Interface tested in Windows High Contrast Mode or `forced-colors: active` emulation.

## Collaboration Points

| Role | What to share | What to ask them |
|------|---------------|-----------------|
| Front-End Dev | Bug reports with exact AT/browser combo | "What was the intended behavior here?" |
| UX Design | Interaction flow test results | "Is this the expected focus behavior?" |
| Content Authoring | Screen reader announcement output | "Is this what you intended to be announced?" |
| Visual Design | Contrast measurement results, zoom screenshots | "Are these values intentional?" |
| Business Analysis | Test coverage reports, compliance dashboards | "Do we have acceptance criteria for this?" |

## Relationship to a11y-test Skill

In this bundle, the `a11y-test` skill IS the testing role's execution layer:
- Playwright keyboard tests = keyboard traversal verification
- axe-core scans = automated scan results
- keyboard-a11y-tester journey audits = AT + keyboard flow verification
- virtual-screen-reader assertions = screen reader announcement verification

The testing role lens reviews whether testing is SUFFICIENT, not whether specific tests pass.
