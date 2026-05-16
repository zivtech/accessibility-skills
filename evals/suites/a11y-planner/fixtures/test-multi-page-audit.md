# Fixture: Multi-Page Audit Plan

## Feature Description

You're planning a full accessibility audit for a 20-page government benefits portal that is preparing to publish a VPAT (Voluntary Product Accessibility Template) in 3 months. The portal serves citizens applying for public assistance programs and is expected to comply with WCAG 2.2 AA. The site was built 4 years ago and has had incremental accessibility fixes but never a systematic audit.

The site includes:
- Public-facing pages: Home, About, Program Listings, Program Detail (×3 variants), FAQ, News, Contact
- Authenticated application flows: Account creation, Login, Multi-step application form (6 steps), Document upload, Application status dashboard, Notification center
- Shared patterns used across pages: Global navigation with mega-menu, search with live results, in-page alerts/notifications, data tables (application history), file upload component, date picker, session timeout warning modal
- Third-party dependencies: reCAPTCHA v2 on login and contact forms, embedded YouTube videos on program pages, third-party analytics script

## Context

- **Platform:** Server-rendered HTML with progressive JavaScript enhancement (no SPA framework)
- **Existing code:** Yes, the site is live — this is a pre-VPAT audit
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), iOS VoiceOver, TalkBack (Android), keyboard-only users, Dragon NaturallySpeaking (voice input)
- **Scope:** 20 pages, 8 shared component patterns, 3 third-party integrations
- **Constraints:** 3-month deadline for VPAT publication; small QA team (2 engineers); government compliance documentation required; automated tools already licensed (axe DevTools Enterprise); VPAT template is ITTF VPAT 2.4 Rev 508

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

Additionally, this audit-scope plan must cover:
- Page sampling strategy (which 20 pages to test, in what order, why)
- Tool selection rationale (axe DevTools vs. WAVE vs. Lighthouse vs. manual)
- Testing matrix (which test types apply to which pages/components)
- Prioritization framework (CRITICAL → MAJOR → MINOR → ADVISORY)
- VPAT reporting template and conformance claim structure
- Third-party component handling (reCAPTCHA, YouTube, analytics)

## Scope Hints

This is a **COMPLEX** difficulty fixture — audit planning at site-level requires methodology decisions that go beyond single-component testing. Expected plan length is 5-7 pages. Focus on:

1. Page sampling rationale: Not all 20 pages need equal testing depth; authenticated application flows have highest risk; home and about have lowest
2. Tool selection: axe DevTools Enterprise (rule-based automated), WAVE (visual overlay for manual review), manual keyboard testing (the only way to test dynamic interactions), SR testing (human judgment)
3. WCAG-EM methodology reference: The W3C evaluation methodology provides the sampling and reporting framework for VPAT
4. Prioritization: CRITICAL = blocks completion of a user journey; MAJOR = significant friction but workaround exists; MINOR = inconvenience; ADVISORY = best practice
5. Third-party exceptions: reCAPTCHA and YouTube are third-party; VPAT must document them but cannot require remediation
6. Shared component leverage: Fixing the mega-menu navigation fixes it across all 20 pages

## What Success Looks Like

An excellent plan would:
- ✓ Reference WCAG-EM (Website Accessibility Conformance Evaluation Methodology) as the sampling framework
- ✓ Prioritize page sampling by risk: authenticated flows first, shared components second, public content pages third
- ✓ Define a testing matrix: which tool(s) and methods apply to which page types
- ✓ Specify axe DevTools Enterprise configuration (which rule sets, which exclusions)
- ✓ Document the prioritization framework with clear definitions for CRITICAL/MAJOR/MINOR/ADVISORY
- ✓ Address third-party components explicitly (reCAPTCHA, YouTube) with VPAT best-effort language
- ✓ Identify shared component leverage — fixing nav, search, and alerts covers the whole site
- ✓ Produce a VPAT reporting structure note (which WCAG criteria most commonly fail on government sites)
- ✓ Include screen reader test matrix (NVDA, JAWS, VoiceOver, iOS VO, TalkBack) with which SR covers which page types
- ✓ Define a11y-critic review checkpoints for each phase of the audit (automated, manual, SR, VPAT draft)

## What Would Be Below Expectations

- ✗ Page sampling strategy of "test all 20 pages equally" — this misunderstands audit methodology and is not feasible in 3 months with a 2-person team
- ✗ No reference to WCAG-EM — the W3C's own methodology for evaluating websites for conformance
- ✗ Tool selection that treats WAVE and axe as equivalent — they cover different things and should be used in complementary, not substitution, roles
- ✗ No handling of third-party components — reCAPTCHA inaccessibility is a VPAT documentation issue, not a remediation issue; omitting this will produce a legally incorrect VPAT
- ✗ Prioritization framework that ranks issues by WCAG criterion number rather than user impact
- ✗ Screen reader matrix that only lists desktop SRs and ignores mobile (iOS VoiceOver, TalkBack) — government portals have high mobile usage
- ✗ No VPAT reporting structure — the entire audit produces a VPAT; plans that don't connect to the output document are incomplete
- ✗ A plan that treats every page as a standalone test without identifying shared component leverage — this misses the efficiency that makes an audit achievable in 3 months
