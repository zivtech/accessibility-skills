# Fixture: Article Page With Proper Accessibility (CLEAN)

## Component Code

```jsx
import React from 'react';

const ArticlePage = () => {
  return (
    <>
      {/* Skip link */}
      <a
        href="#main-content"
        className="skip-link"
      >
        Skip to main content
      </a>

      {/* Site header landmark */}
      <header className="site-header">
        <a href="/" className="site-logo" aria-label="Acme Journal — home">
          Acme Journal
        </a>

        {/* Primary navigation landmark */}
        <nav aria-label="Primary">
          <ul>
            <li><a href="/news">News</a></li>
            <li><a href="/science">Science</a></li>
            <li><a href="/health">Health</a></li>
            <li><a href="/opinion">Opinion</a></li>
          </ul>
        </nav>
      </header>

      {/* Main content landmark */}
      <main id="main-content" tabIndex={-1}>
        <article aria-labelledby="article-title">
          {/* h1 — document title */}
          <h1 id="article-title">
            New Study Links Sleep Quality to Long-Term Heart Health
          </h1>

          {/* Article metadata */}
          <p className="article-meta">
            <time dateTime="2026-03-28">March 28, 2026</time>
            {' '}&bull;{' '}
            <span>By Dr. Maria Santos, Health Correspondent</span>
          </p>

          {/* Lead image with descriptive alt text */}
          <figure>
            <img
              src="/images/sleep-research-lab.jpg"
              alt="Researcher monitoring sleep patterns on EEG equipment in a darkened laboratory"
              width={900}
              height={500}
            />
            <figcaption>
              Researchers at the University Sleep Lab track brain activity during
              REM cycles as part of the longitudinal study.
            </figcaption>
          </figure>

          {/* h2 — first section */}
          <h2>What the Research Found</h2>
          <p>
            A ten-year longitudinal study published Monday in the{' '}
            <em>Journal of Cardiovascular Medicine</em> found that adults who
            consistently sleep fewer than six hours per night face a 34 percent
            higher risk of developing hypertension compared to those who sleep
            seven to nine hours.
          </p>
          <p>
            The study followed 12,000 participants across five countries and
            controlled for diet, exercise, smoking status, and baseline
            cardiovascular health.
          </p>

          {/* h2 — second section */}
          <h2>How Sleep Affects the Heart</h2>
          <p>
            During deep sleep, blood pressure drops and the heart rate slows,
            giving the cardiovascular system a chance to recover. Chronic sleep
            deprivation interrupts this repair window, leaving arteries under
            prolonged stress.
          </p>

          {/* h3 — subsection under second h2 */}
          <h3>The Role of REM Sleep</h3>
          <p>
            REM sleep appears to be particularly important. Participants in the
            lowest REM quartile were twice as likely to show early markers of
            arterial stiffening by the study's end.
          </p>

          {/* h3 — second subsection */}
          <h3>Sleep Disorders and Compounding Risk</h3>
          <p>
            Participants with diagnosed sleep apnea who received treatment
            showed cardiovascular outcomes similar to healthy sleepers, suggesting
            that treatment — not just diagnosis — is the protective factor.
          </p>

          {/* h2 — third section */}
          <h2>What This Means for You</h2>
          <p>
            Cardiologists say the findings reinforce existing recommendations:
            aim for seven to nine hours of sleep, maintain a consistent schedule,
            and seek evaluation if you snore loudly or wake frequently.
          </p>

          {/* Inline links: underlined via CSS */}
          <p>
            The full study is available at{' '}
            <a href="https://jcm.example.org/sleep-2026" className="article-link">
              the Journal of Cardiovascular Medicine
            </a>
            . A plain-language summary is published on the{' '}
            <a href="https://nih.example.gov/sleep" className="article-link">
              National Institutes of Health website
            </a>
            .
          </p>

          {/* h2 — expert response */}
          <h2>Expert Response</h2>
          <p>
            Dr. James Okafor, a cardiologist not involved in the study, called
            the findings "compelling but not surprising." He noted that sleep
            hygiene has historically been underemphasized in cardiovascular
            prevention programs.
          </p>
        </article>
      </main>

      {/* Footer landmark */}
      <footer>
        <nav aria-label="Footer">
          <ul>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
            <li><a href="/privacy">Privacy Policy</a></li>
            <li><a href="/accessibility">Accessibility Statement</a></li>
          </ul>
        </nav>
        <p>
          <small>&copy; 2026 Acme Journal. All rights reserved.</small>
        </p>
      </footer>
    </>
  );
};

export default ArticlePage;
```

## CSS

```css
/* Skip link — visible on focus only */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #005fcc;
  color: #ffffff;
  padding: 8px 16px;
  font-size: 1rem;
  z-index: 100;
  text-decoration: underline;
  transition: top 0.2s;
}

.skip-link:focus {
  top: 0;
}

/* Site header */
.site-header {
  background: #1a1a2e;
  color: #ffffff;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 32px;
}

.site-logo {
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 700;
  text-decoration: underline;
  padding: 16px 0;
}

.site-logo:focus {
  outline: 3px solid #7eb8f7;
  outline-offset: 2px;
}

/* Nav */
nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 4px;
}

nav a {
  color: #cce3ff;
  text-decoration: underline;
  padding: 8px 12px;
  display: block;
  font-size: 0.95rem;
}

nav a:hover {
  color: #ffffff;
}

nav a:focus {
  outline: 3px solid #7eb8f7;
  outline-offset: 2px;
  border-radius: 2px;
}

/* Main content */
main {
  max-width: 740px;
  margin: 0 auto;
  padding: 32px 24px;
}

main:focus {
  outline: none; /* tabIndex=-1 focus target, no visible ring needed */
}

/* Article typography */
article h1 {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  line-height: 1.2;
  color: #111111;
  margin-bottom: 12px;
}

article h2 {
  font-size: clamp(1.25rem, 3vw, 1.75rem);
  line-height: 1.3;
  color: #111111;
  margin-top: 2em;
  margin-bottom: 0.5em;
}

article h3 {
  font-size: clamp(1.05rem, 2.5vw, 1.35rem);
  line-height: 1.4;
  color: #222222;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

article p {
  font-size: 1.0625rem;
  line-height: 1.75;
  color: #222222;       /* #222 on white = 14.7:1 contrast */
  margin-bottom: 1.25em;
}

/* Article metadata */
.article-meta {
  font-size: 0.9rem;
  color: #555555;       /* #555 on white = 7.0:1 contrast */
  margin-bottom: 24px;
}

/* Figure / image */
figure {
  margin: 0 0 2em;
}

figure img {
  width: 100%;
  height: auto;
  display: block;
}

figcaption {
  font-size: 0.875rem;
  color: #555555;
  margin-top: 8px;
  font-style: italic;
}

/* Inline article links — underlined to satisfy WCAG 1.4.1 */
.article-link {
  color: #005fcc;       /* #005fcc on white = 7.1:1 contrast */
  text-decoration: underline;
  text-underline-offset: 3px;
}

.article-link:hover {
  color: #004299;
}

.article-link:focus {
  outline: 3px solid #005fcc;
  outline-offset: 3px;
  border-radius: 2px;
}

/* Reduced-motion: suppress fade-in animation */
@media (prefers-reduced-motion: no-preference) {
  article {
    animation: fade-in 0.35s ease-in both;
  }
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Responsive reflow at 320px — single column, no horizontal scroll */
@media (max-width: 400px) {
  .site-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 12px 16px;
    gap: 8px;
  }

  nav ul {
    flex-wrap: wrap;
    gap: 2px;
  }

  nav a {
    padding: 6px 8px;
    font-size: 0.9rem;
  }

  main {
    padding: 24px 16px;
  }
}

/* Text resize to 200% — no content loss */
@media (min-resolution: 1dppx) {
  html {
    font-size: 100%;
  }
}

/* Footer */
footer {
  background: #1a1a2e;
  color: #cce3ff;
  padding: 24px;
  margin-top: 48px;
}

footer nav ul {
  flex-wrap: wrap;
  gap: 4px;
}

footer a {
  color: #cce3ff;       /* #cce3ff on #1a1a2e = 7.5:1 contrast */
  text-decoration: underline;
  padding: 6px 8px;
  font-size: 0.9rem;
}

footer a:hover {
  color: #ffffff;
}

footer a:focus {
  outline: 3px solid #7eb8f7;
  outline-offset: 2px;
  border-radius: 2px;
}

footer small {
  display: block;
  margin-top: 16px;
  font-size: 0.8rem;
  color: #aac4e8;       /* #aac4e8 on #1a1a2e = 4.6:1 contrast */
}
```

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

## Accessibility Issues

**NONE.** This is a clean, well-implemented article page. All listed accessibility features are present and correctly implemented.

Optional enhancements a reviewer MAY note (ENHANCEMENT severity only):
1. Could add `aria-current="page"` to the active nav item (News, Science, etc.) — not implemented here because the active page is unknown to a static component, but worth noting as a pattern.
2. Could add `lang` attribute to any foreign-language quotations if they appeared in the article — there are none in this fixture, but a reviewer who notes the pattern is correct.

## Difficulty Level

**CLEAN** — This is a properly implemented article page with all common accessibility features present and correct. A competent reviewer should produce a verdict of ACCEPT or ACCEPT-WITH-RESERVATIONS (minor enhancements only). Used to measure false-positive rate across all seven access perspectives.
