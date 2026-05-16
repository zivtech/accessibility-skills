# Fixture: Blog Article Page — Semantic Structure

## Feature Description

You're planning accessibility for a blog article page on a content-heavy editorial site. The page includes a site header with primary navigation, a main content area containing a long-form article, an author byline with a publication timestamp, four to six body images with varying levels of contextual relevance, three levels of heading hierarchy (H1 article title, H2 section headings, H3 sub-section headings), a blockquote pull-quote mid-article, a complementary sidebar with related articles, and a footer with site-wide links. The article renders from a Drupal CMS with a React front-end display layer. No interactive widgets — this is a reading experience.

## Context

- **Platform:** React/Next.js front-end rendering Drupal-sourced article content
- **Existing code:** Yes — existing Article component renders raw CMS HTML via `dangerouslySetInnerHTML`; no landmark regions defined; images use `alt=""` universally; heading levels are visually styled but semantically arbitrary
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Single article page — landmark regions, heading hierarchy, image alt strategy, time element, complementary sidebar
- **Constraints:** Alt text is authored in the CMS by editorial staff with no a11y training; heading levels are driven by visual design tokens, not document order; the same Article component renders on listing pages (teaser) and full article pages

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- Semantic structure (landmark regions, HTML5 sectioning elements)
- Heading hierarchy strategy (document outline, skipping levels, repair approach)
- Image alt text strategy (contextual vs decorative vs complex image decisions)
- `<time>` element with `datetime` attribute for publication date
- Landmark region coverage (`<main>`, `<nav>`, `<aside>`, `<footer>`, `<header>`)
- Skip navigation link targeting `<main>`
- Blockquote semantics and screen reader announcement behavior
- Focus management (keyboard-only reading path)
- Visual accessibility (text resize, line length, spacing)
- Content accessibility (reading level, link text, adjacent duplicate links)
- Testing strategy
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is a **TRIVIAL** difficulty fixture — the challenge is completeness and correct semantic choices, not complex ARIA patterns. No custom widgets, no live regions, no focus traps. Expected plan length: 1-2 pages. Avoid over-engineering. Focus on:

1. Correct landmark region structure with `<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>`, `aria-label` on secondary `<nav>` elements
2. Heading hierarchy — document outline principle (H1 → H2 → H3, no skips), repair strategy for CMS-driven content
3. Alt text decision tree: informative / decorative / complex (described in text or with `aria-describedby`)
4. `<time datetime="2026-05-15">May 15, 2026</time>` pattern
5. Skip link targeting `#main-content`

## What Success Looks Like

An excellent plan would:
- ✓ Map all landmark regions with correct HTML5 elements and `aria-label` disambiguation for multiple `<nav>` elements
- ✓ Document the heading outline rule (H1 = article title, H2 = sections, H3 = sub-sections) with WCAG 2.4.6 citation
- ✓ Provide a concrete alt text decision tree: decorative → `alt=""`, contextual → descriptive alt, chart/diagram → long description or `aria-describedby`
- ✓ Specify the `<time datetime>` pattern with ISO 8601 format requirement
- ✓ Address skip link targeting `<main id="main-content">`
- ✓ Note that `dangerouslySetInnerHTML` content bypasses React accessibility linting — recommend sanitized rendering with explicit heading mapping
- ✓ Cite WCAG 1.3.1 (Info and Relationships), 1.1.1 (Non-text Content), 2.4.1 (Bypass Blocks), 2.4.6 (Headings and Labels)
- ✓ Include a testing checklist: heading order check (axe), landmark audit (browser extension), image alt audit, keyboard tab through page

## What Would Be Below Expectations

- ✗ Generic "use semantic HTML" advice without specifying which elements go where
- ✗ Alt text strategy that only says "add descriptive alt text" — no decorative/complex image handling
- ✗ No mention of `aria-label` disambiguation for multiple navigation landmarks
- ✗ Heading hierarchy that ignores the CMS constraint (editorial staff controls H levels)
- ✗ Missing `<time datetime>` pattern — displaying "May 15, 2026" as plain text is not a failure, but the plan should note the machine-readable option
- ✗ WCAG citations absent or listed as numbers only without criterion names
- ✗ Plan that invents ARIA patterns for a static reading experience (over-engineering for TRIVIAL)
- ✗ No testing strategy at all
