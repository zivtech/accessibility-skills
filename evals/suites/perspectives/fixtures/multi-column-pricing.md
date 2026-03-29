# Fixture: Multi-Column Pricing Comparison Table

## Component Code

```jsx
import React, { useState } from 'react';

// CSS
/*
.pricing-page {
  font-family: system-ui, sans-serif;
  max-width: 960px;
  margin: 0 auto;
  padding: 40px 24px;
  background: #fff;
}

.pricing-page h1 {
  text-align: center;
  font-size: 28px;
  margin-bottom: 8px;
}

.pricing-page > p {
  text-align: center;
  color: #555;
  margin-bottom: 40px;
  font-size: 15px;
}

.pricing-table-wrapper {
  overflow-x: auto;
}

/* Correct semantic table — NOT a bug */
.pricing-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.pricing-table th {
  padding: 20px 16px 12px;
  text-align: center;
  border-bottom: 2px solid #e0e0e0;
  vertical-align: bottom;
}

.pricing-table td {
  padding: 12px 16px;
  text-align: center;
  border-bottom: 1px solid #f0f0f0;
}

.pricing-table tr:hover td {
  background: #fafafa;
}

.tier-name {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 4px;
}

.tier-price {
  /* BUG: 12px gray text #767676 on white — contrast ratio 4.54:1, barely passes AA
     for normal text (4.5:1 minimum) but fails AA for text this visually small and
     light at actual rendered weight */
  font-size: 12px;
  color: #767676;
  font-weight: 400;
  margin-bottom: 12px;
}

.tier-price .amount {
  font-size: 28px;
  font-weight: 700;
  color: #111;
  /* NOT a bug — large price amount has sufficient contrast */
}

.recommended-header {
  /* BUG: "Recommended" tier column is highlighted with background color only —
     no text label "Recommended", no aria-sort or aria-describedby pointing to
     a recommendation explanation */
  background: #ebf8ff;
  border-top: 3px solid #2b6cb0;
}

.most-popular-badge {
  display: inline-block;
  background: linear-gradient(90deg, #2b6cb0, #4299e1);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 99px;
  /* BUG: Shimmer animation on badge with no prefers-reduced-motion override */
  animation: shimmer 2s linear infinite;
  background-size: 200% 100%;
}

@keyframes shimmer {
  0%   { background-position: 200% center; }
  100% { background-position: -200% center; }
}

/* BUG: No @media (prefers-reduced-motion: reduce) to suppress shimmer */

.feature-check {
  /* BUG: Feature availability is indicated by green checkmark vs red X — color only.
     Both pass contrast individually, but the check vs X distinction relies entirely
     on color (green = available, red = unavailable) with no pattern or shape difference
     that would be distinguishable in monochrome. */
  font-size: 18px;
}

.feature-check.available {
  color: #38a169; /* green — passes contrast against white */
}

.feature-check.unavailable {
  color: #e53e3e; /* red — passes contrast against white */
}

.feature-row td:first-child {
  text-align: left;
  color: #333;
  font-size: 13px;
}

.feature-tooltip-trigger {
  /* BUG: Feature comparison tooltip is hover-only — no focus event triggers tooltip */
  cursor: help;
  text-decoration: underline dotted #999;
  position: relative;
}

.feature-tooltip {
  display: none;
  position: absolute;
  background: #222;
  color: #fff;
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 4px;
  white-space: nowrap;
  z-index: 10;
  bottom: 100%;
  left: 0;
}

.feature-tooltip-trigger:hover .feature-tooltip {
  display: block;
  /* BUG: :focus-within not added — tooltip does not appear on keyboard focus */
}

.cta-button {
  /* Keyboard-accessible CTA button — NOT a bug */
  display: block;
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 16px;
  background: #2b6cb0;
  color: #fff;
}

.cta-button:focus-visible {
  outline: 2px solid #2b6cb0;
  outline-offset: 2px;
}
*/

const TIERS = [
  {
    id: 'starter',
    name: 'Starter',
    price: 0,
    period: '/month',
    recommended: false,
    cta: 'Get started free',
  },
  {
    id: 'pro',
    name: 'Pro',
    price: 29,
    period: '/month',
    recommended: true,
    cta: 'Start free trial',
  },
  {
    id: 'business',
    name: 'Business',
    price: 79,
    period: '/month',
    recommended: false,
    cta: 'Contact sales',
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: null,
    period: 'Custom pricing',
    recommended: false,
    cta: 'Talk to us',
  },
];

const FEATURES = [
  { id: 'users', label: 'Team members', tooltip: 'Number of user seats included', tiers: [1, 5, 25, null] },
  { id: 'storage', label: 'Storage', tooltip: 'Cloud storage limit per workspace', tiers: [true, true, true, true] },
  { id: 'api', label: 'API access', tooltip: 'REST API and webhooks for integrations', tiers: [false, true, true, true] },
  { id: 'analytics', label: 'Advanced analytics', tooltip: 'Custom dashboards and export', tiers: [false, true, true, true] },
  { id: 'sso', label: 'SSO / SAML', tooltip: 'Single sign-on via SAML 2.0 or OIDC', tiers: [false, false, true, true] },
  { id: 'sla', label: 'SLA guarantee', tooltip: '99.9% uptime SLA with credits', tiers: [false, false, true, true] },
  { id: 'support', label: 'Priority support', tooltip: '4-hour response time SLA', tiers: [false, false, false, true] },
];

const FeatureCell = ({ value, tierName }) => {
  if (value === null) return <td className="feature-check">—</td>;
  if (typeof value === 'number') {
    return <td className="feature-check">{value}</td>;
  }
  return (
    <td className="feature-check">
      {/* BUG: check vs X distinction is color only — both ✓ and ✕ use the same Unicode
          characters but green/red color is the only differentiating signal.
          In grayscale or for color-blind users, ✓ and ✕ render as similar-weight marks.
          No aria-label on the cell to communicate "available" or "not available" */}
      <span
        className={`feature-check ${value ? 'available' : 'unavailable'}`}
        aria-hidden="true"
      >
        {value ? '✓' : '✕'}
      </span>
      {/* BUG: No visually-hidden text equivalent for screen readers; aria-hidden hides the icon */}
    </td>
  );
};

const TooltipFeatureLabel = ({ label, tooltip }) => (
  /* BUG: Tooltip is CSS hover-only — :focus-within not added; keyboard users cannot
     access tooltip content for feature descriptions */
  <span className="feature-tooltip-trigger">
    {label}
    <span className="feature-tooltip" role="tooltip">{tooltip}</span>
  </span>
);

const PricingTable = () => {
  const [, setSelectedTier] = useState(null);

  return (
    <div className="pricing-page">
      <h1>Choose your plan</h1>
      <p>Start free, scale as you grow. No credit card required.</p>

      <div className="pricing-table-wrapper">
        {/* Correct semantic table structure — NOT a bug */}
        <table className="pricing-table">
          <thead>
            <tr>
              <th scope="col">Features</th>
              {TIERS.map((tier) => (
                <th
                  key={tier.id}
                  scope="col"
                  className={tier.recommended ? 'recommended-header' : ''}
                >
                  <div className="tier-name">{tier.name}</div>
                  {tier.recommended && (
                    /* BUG: "Most popular" badge has shimmer animation with no reduced-motion */
                    <span className="most-popular-badge" aria-label="Most popular">
                      Most popular
                    </span>
                  )}
                  <div className="tier-price">
                    {tier.price !== null ? (
                      <>
                        {/* Large price amount has correct contrast — NOT a bug */}
                        <span className="amount">${tier.price}</span>
                        {/* BUG: 12px #767676 price period text — borderline contrast at 4.54:1 */}
                        {tier.period}
                      </>
                    ) : (
                      tier.period
                    )}
                  </div>
                  {/* Keyboard-accessible CTA — NOT a bug */}
                  <button
                    className="cta-button"
                    onClick={() => setSelectedTier(tier.id)}
                    aria-label={`${tier.cta} — ${tier.name} plan`}
                  >
                    {tier.cta}
                  </button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {FEATURES.map((feature) => (
              <tr key={feature.id} className="feature-row">
                <td>
                  <TooltipFeatureLabel label={feature.label} tooltip={feature.tooltip} />
                </td>
                {TIERS.map((tier, i) => (
                  <FeatureCell
                    key={tier.id}
                    value={feature.tiers[i]}
                    tierName={tier.name}
                  />
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PricingTable;
```

## Expected Behavior

- Pricing comparison table with 4 tiers and 7 feature rows
- Feature availability is communicated via text or visually-hidden labels, not color alone
- "Recommended" tier is identified with a text label ("Recommended") not background color alone
- Pricing sub-text has sufficient contrast at its rendered size and weight
- Feature comparison tooltips are accessible on both hover and keyboard focus
- "Most popular" badge animation respects `prefers-reduced-motion`
- Table uses correct `<thead>`, `<tbody>`, `<th scope>` structure (all correct — not a bug)
- CTA buttons have descriptive labels (all correct — not a bug)

## Accessibility Features Present

- Table uses semantic `<table>` with `<thead>`, `<tbody>`, and `<th scope="col">` on all headers
- CTA buttons have `aria-label` values identifying both action and plan name
- Large price amount (28px bold) has sufficient contrast (#111 on white) — not a bug
- "Most popular" badge has `aria-label="Most popular"` — text content is not hidden
- `pricing-table-wrapper` has `overflow-x: auto` for horizontal scroll on small viewports

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Feature availability indicated by color only** — Feature cells render a green `✓` (available) or red `✕` (unavailable) where the distinction is entirely color-dependent. Both icons are `aria-hidden="true"` with no visually-hidden text alternative. In grayscale, deuteranopia, or protanopia, the check and X render as similar-weight marks. WCAG 1.4.1 (Use of Color) prohibits using color as the only means of conveying information.
   - Evidence: `FeatureCell` component renders `<span aria-hidden="true">{value ? '✓' : '✕'}</span>` with color class only; no visually-hidden text in the cell; no `aria-label` on the `<td>`
   - User group: Users with color vision deficiencies (deuteranopia, protanopia); screen reader users; users in high-contrast mode
   - Expected fix: Add `<span className="sr-only">{value ? 'Available' : 'Not available'}</span>` alongside each icon, or set `aria-label` on the `<td>` element

2. **MAJOR: "Recommended" tier highlighted with background color only** — The recommended tier column header uses `background: #ebf8ff` and `border-top: 3px solid #2b6cb0` as its only differentiation. There is no text label "Recommended" in the header cell, and no `aria-describedby` pointing to a recommendation explanation.
   - Evidence: `recommended-header` CSS class applies background and border only; no text "Recommended" in the `<th>` beyond the tier name and badge
   - User group: Users with color vision deficiencies; screen reader users; users in high-contrast mode
   - Expected fix: Add visible text "Recommended" to the header cell, or ensure the existing visual badge also serves as the text label

3. **MAJOR: Pricing sub-text is 12px #767676 on white — borderline contrast** — The `tier-price` text (e.g., "/month", "Custom pricing") uses 12px regular weight at `color: #767676` on a white background, yielding a contrast ratio of approximately 4.54:1. WCAG 1.4.3 requires 4.5:1 for normal text; the current value passes by 0.04 ratio units. At 12px regular weight, WCAG 1.4.3 defines this as normal text (not large), making it a borderline failure that requires attention.
   - Evidence: `.tier-price { font-size: 12px; color: #767676 }` — 12px regular weight at #767676 on #fff yields ~4.54:1 ratio
   - User group: Users with low vision; users in non-ideal contrast environments (bright sunlight, glare)
   - Expected fix: Darken to `#595959` (7:1) or `#767676` at 14px bold (large text threshold at 18.67px bold — this does not qualify); increase font-size to 14px and add font-weight 600 to reach large-text threshold

4. **MINOR: Feature comparison tooltips are hover-only, not accessible on focus** — `TooltipFeatureLabel` uses CSS `:hover` to show the tooltip. No `:focus-within` rule is present, so keyboard users tabbing through feature labels receive no tooltip content. The `role="tooltip"` is present but the tooltip never appears for keyboard users.
   - Evidence: `.feature-tooltip-trigger:hover .feature-tooltip { display: block }` with no `:focus-within` equivalent; `/* BUG: :focus-within not added */` comment in CSS
   - User group: Keyboard-only users; motor-impaired users
   - Expected fix: Add `.feature-tooltip-trigger:focus-within .feature-tooltip { display: block }` to CSS, or switch to a JS-controlled tooltip visible on both hover and focus

5. **MINOR: "Most popular" badge has shimmer animation with no `prefers-reduced-motion` override** — The `.most-popular-badge` element uses a 2-second infinite shimmer gradient animation with no `@media (prefers-reduced-motion: reduce)` rule to suppress it.
   - Evidence: `.most-popular-badge { animation: shimmer 2s linear infinite }` with no reduced-motion media query; `/* BUG: No @media (prefers-reduced-motion: reduce) */` comment
   - User group: Users with vestibular disorders; users who have enabled reduced-motion
   - Expected fix: Add `@media (prefers-reduced-motion: reduce) { .most-popular-badge { animation: none; } }`

## Difficulty Level

**HAS-BUGS** — New dimension: contrast (color-only feature indicators, borderline pricing text). The table structure (`<thead>`, `<tbody>`, `<th scope>`), CTA button labels, and horizontal scroll wrapper are all correct and are intentional true negatives. The ✓ and ✕ icons are a nuanced case: both pass contrast individually, but the check-vs-X distinction is color-only, which is WCAG 1.4.1 not 1.4.3. A perspective-aware reviewer must cite the correct criterion.

## Frameworks

React 18+, CSS animations, HTML5 semantic table, `prefers-reduced-motion` (expected but absent)
