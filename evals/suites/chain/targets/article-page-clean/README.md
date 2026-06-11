# Article Page With Proper Accessibility (CLEAN)

## Description

A React article page that correctly implements all common accessibility features across all seven access perspectives. Used to measure false-positive rate: a well-calibrated reviewer should not trigger findings against this page.

## Expected Behavior

- Skip link appears on keyboard focus and jumps focus to `#main-content`
- Landmark regions (header, nav ×2, main, footer) are navigable via screen reader
- Heading hierarchy is h1 > h2 > h3 throughout; no skips
- Images have descriptive alt text; figure has caption
- Inline links are underlined in body copy
- Page reflows to single column at 320px with no horizontal scroll
- Text scales to 200% browser zoom without loss of content or function
- Article fade-in animation is suppressed when `prefers-reduced-motion` is active
- No auto-playing media; no CAPTCHA; no time limits
- Color contrast: body text 14.7:1, meta/captions 7:1, links 7.1:1, footer links 7.5:1, footer small 4.6:1

## Accessibility Features Present

- Skip link to `#main-content` with `:focus` visibility
- `<header>` landmark
- `<nav aria-label="Primary">` landmark
- `<main id="main-content">` landmark with `tabIndex={-1}` for skip-link target
- `<article aria-labelledby="article-title">` with matching `id` on `<h1>`
- `<footer>` landmark
- `<nav aria-label="Footer">` inside footer
- Heading hierarchy: single h1, four h2s, two h3s — no skips
- All images have descriptive `alt` text (not empty, not filename, not "image of")
- `<figure>` and `<figcaption>` used correctly
- `<time datetime="2026-03-28">` for machine-readable date
- All inline links are underlined (`text-decoration: underline`) — WCAG 1.4.1
- Body text color contrast #222 on white = 14.7:1 — WCAG 1.4.3 AAA
- Meta/caption text #555 on white = 7.0:1 — WCAG 1.4.3 AA
- Link color #005fcc on white = 7.1:1 — WCAG 1.4.3 AAA
- Footer links #cce3ff on #1a1a2e = 7.5:1 — WCAG 1.4.3 AAA
- Footer small text #aac4e8 on #1a1a2e = 4.6:1 — WCAG 1.4.6 AA Large
- `prefers-reduced-motion` respected: animation only runs when no-preference active; disabled by default for reduced-motion users
- Fade-in is subtle (opacity + 6px translate, 0.35s) — not a distracting flash
- Responsive single-column layout at 320px — no horizontal scrollbar
- `clamp()` font sizes maintain readability at all viewport widths
- Text resizes to 200% without overflow or loss of functionality
- No auto-playing media (no `<video autoplay>`, no `<audio>`)
- No CAPTCHA
- No session time limits
- Content is time-independent (no countdown, no expiry warning)
- Reading level is straightforward: short paragraphs, clear section headings, plain language
- All focus indicators are visible (3px outline, sufficient contrast)

---

_This directory contains component files extracted from the a11y eval suite for chain evaluation._
_Run `/a11y-workflow full evals/suites/chain/targets/article-page-clean/component.jsx` to start the chain._
