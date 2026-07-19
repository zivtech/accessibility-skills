# Business Analysis

## Responsibility

Business analysis ensures that organizational processes, requirements, and metrics support accessible outcomes. This role bridges what users need and what teams deliver — translating accessibility standards into actionable requirements, tracking compliance metrics, and ensuring procurement evaluates vendor accessibility.

## Also Known As

Business analyst, data analyst, digital performance analyst, operations, requirements analyst, systems analyst, project manager, product owner.

## What This Role Sees

- Whether accessibility requirements are defined in project scope and contracts
- Whether metrics exist to measure accessibility outcomes over time
- Whether time limits, error recovery, and CAPTCHA flows meet standards
- Whether procurement processes evaluate vendor accessibility claims (VPATs, ACRs)
- Whether gaps exist between organizational goals and actual implementation
- Whether accessibility is budgeted in project timelines and resource allocation

## Blind Spots (What This Role Misses)

| Gap | Ask instead |
|-----|-------------|
| How requirements translate to actual code | Front-End Development |
| Whether content is clear and understandable | Content Authoring |
| Whether interactions work with keyboard/screen reader | Testing |
| Whether the visual design supports accessibility | Visual Design |
| Whether the interaction pattern is the right one | UX Design |

## ARRM Task Ownership

### Primary (1 task)

- CAPTCHA alternatives — Alternate means of accessing CAPTCHA information are provided (audio, logical question, or equivalent) (1.1.1, IMG-016)

### Secondary (5 tasks)

- Error prevention for legal/financial data — confirmation screens, reversibility (3.3.4)
- Time limit management — users notified before expiry, option to extend (2.2.1)

### Contributor (3 tasks)

- Cognitive function tests provide alternatives during authentication (3.3.8, 3.3.9)
- Timing not essential to event or activity (2.2.3)

## Key WCAG Criteria

| SC | Level | What it requires |
|----|-------|-----------------|
| 3.3.4 | AA | Error prevention for legal, financial, data |
| 2.2.1 | A | Timing adjustable |
| 1.1.1 | A | CAPTCHA alternatives |
| 2.2.6 | AAA | Timeouts — warn users of data loss |
| 3.3.8 | AA | Accessible authentication (minimum) |

## Review Checklist

When reviewing from this role's perspective, evaluate:

1. **Requirements coverage** — Do project requirements include specific accessibility acceptance criteria? Not just "must be accessible" but testable criteria tied to WCAG levels.
2. **CAPTCHA** — If CAPTCHA exists: is there an audio alternative? A logical alternative? A way that doesn't require vision OR hearing OR cognition?
3. **Time limits** — Any time-limited interaction: can it be extended to at least 10× the default? Are users warned at least 20 seconds before timeout? Can timing be turned off entirely?
4. **Error prevention** — For legal/financial/data submissions: is there a confirmation step? Can submissions be reversed? Is data checked before final submit?
5. **Authentication** — Login doesn't require a cognitive function test (memorized password is fine; CAPTCHA puzzle is not) unless alternatives exist.
6. **Vendor evaluation** — Third-party components: do they have a current VPAT/ACR? Has the ACR been verified against actual testing?
7. **Metrics** — Is accessibility measured? Are there targets (e.g., zero critical axe violations per sprint)? Is regression tracked?
8. **Timeline** — Is accessibility work budgeted in sprints/timelines, or treated as "if we have time"?

## Collaboration Points

| Role | What to share | What to ask them |
|------|---------------|-----------------|
| Front-End Dev | Requirements, constraints | "Can this requirement be met with current technology?" |
| Content Authoring | Plain language requirements | "Is this error message understandable?" |
| UX Design | User research findings | "What do users actually need here?" |
| Visual Design | Design constraints | "Does this approach work visually?" |
| Testing | Acceptance criteria | "How do we verify this requirement is met?" |
