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
