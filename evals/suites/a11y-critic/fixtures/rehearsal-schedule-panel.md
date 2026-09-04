# Fixture: Rehearsal Schedule Panel

## Recent Changes (PR #482)

Closes ACC-118. This PR finishes the keyboard-accessibility pass on the staff
rehearsal schedule page: the calendar and section-call-times controls on each
rehearsal card now carry accessible names and follow a logical tab order, and
the conductor-notes indicator — previously invisible to screen reader and
keyboard users — is now reachable by keyboard as well, per the last
accessibility retest.

## Component Code

```jsx
import React, { useState } from 'react';
import { CalendarIcon, ShareIcon } from '../icons';
import './RehearsalSchedulePanel.css';

const REHEARSALS = [
  {
    id: 'reh-214',
    title: 'Mahler — Symphony No. 5',
    date: 'Tue, Sep 15',
    time: '7:00–9:30 PM',
    location: 'Ashford Hall, Studio A',
    conductor: 'Elena Voss',
    hasNotes: true,
  },
  {
    id: 'reh-215',
    title: 'Copland — Appalachian Spring',
    date: 'Thu, Sep 17',
    time: '7:00–9:00 PM',
    location: 'Ashford Hall, Studio A',
    conductor: 'Elena Voss',
    hasNotes: false,
  },
  {
    id: 'reh-216',
    title: 'Season Opener — Full Program',
    date: 'Sat, Sep 19',
    time: '10:00 AM–1:00 PM',
    location: 'Fairmont Civic Auditorium',
    conductor: 'Elena Voss',
    hasNotes: true,
  },
];

const RehearsalCard = ({ rehearsal }) => {
  const [detailsOpen, setDetailsOpen] = useState(false);

  return (
    <li className="rehearsal-card">
      <h3 className="rehearsal-title">{rehearsal.title}</h3>
      <p className="rehearsal-meta">
        {rehearsal.date} · {rehearsal.time} · {rehearsal.location}
      </p>
      <p className="rehearsal-conductor">Conductor: {rehearsal.conductor}</p>

      <div className="rehearsal-actions">
        <button
          className="icon-button"
          aria-label={`Add ${rehearsal.title} to calendar`}
          onClick={() => console.log('add to calendar', rehearsal.id)}
        >
          <CalendarIcon aria-hidden="true" />
        </button>

        <button
          className="details-toggle"
          aria-expanded={detailsOpen}
          aria-controls={`section-calls-${rehearsal.id}`}
          onClick={() => setDetailsOpen(!detailsOpen)}
        >
          {detailsOpen ? 'Hide section call times' : 'Show section call times'}
        </button>
      </div>

      <div
        id={`section-calls-${rehearsal.id}`}
        className="section-calls"
        hidden={!detailsOpen}
      >
        <p>Strings: 7:00 PM · Winds: 7:20 PM · Brass/Percussion: 7:40 PM</p>
      </div>

      {rehearsal.hasNotes && (
        <span className="notes-flag" tabIndex="0" title="Conductor notes attached">
          📝
        </span>
      )}
    </li>
  );
};

const RehearsalSchedulePanel = () => (
  <div className="staff-portal-layout">
    <section aria-labelledby="schedule-heading" className="rehearsal-schedule-panel">
      <h2 id="schedule-heading">Upcoming Rehearsals</h2>
      <ul className="rehearsal-list">
        {REHEARSALS.map((r) => (
          <RehearsalCard key={r.id} rehearsal={r} />
        ))}
      </ul>
    </section>

    <aside aria-labelledby="announcements-heading" className="season-announcements">
      <h2 id="announcements-heading">Season Announcements</h2>
      <ul className="announcement-list">
        <li>
          <p>Winter subscription renewals open October 1.</p>
          <a href="/announcements/renewals">Read more</a>
        </li>
        <li>
          <p>New parking arrangements at Fairmont Civic Auditorium starting this month.</p>
          <a href="/announcements/parking">Read more</a>
        </li>
        <li>
          <p>Guest conductor Elena Voss extends through the spring season.</p>
          <a href="/announcements/voss-extension">Read more</a>
        </li>
      </ul>
      <p className="brochure-line">
        <a href="/season-brochure.pdf">Click here</a> for the full season brochure.
      </p>
      <a href="/staff/schedule/share" className="icon-link">
        <ShareIcon aria-hidden="true" />
      </a>
    </aside>
  </div>
);

export default RehearsalSchedulePanel;
```

## CSS

```css
.staff-portal-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
  max-width: 1100px;
  margin: 24px auto;
}

.rehearsal-card {
  position: relative;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 16px;
}

.notes-flag {
  position: absolute;
  top: 10px;
  right: 12px;
  font-size: 18px;
}

.rehearsal-title {
  margin: 0 0 4px 0;
  font-size: 17px;
  color: #1e293b;
}

.rehearsal-meta,
.rehearsal-conductor {
  margin: 2px 0;
  font-size: 14px;
  color: #475569;
}

.rehearsal-actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.icon-button {
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  border-radius: 6px;
  padding: 8px;
  cursor: pointer;
}

.icon-button:focus-visible,
.details-toggle:focus-visible,
.notes-flag:focus-visible {
  outline: 3px solid #2563eb;
  outline-offset: 2px;
}

.details-toggle {
  border: 1px solid #cbd5e1;
  background: #ffffff;
  border-radius: 6px;
  padding: 8px 14px;
  cursor: pointer;
}

.section-calls {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #f1f5f9;
  font-size: 14px;
  color: #334155;
}

.season-announcements {
  border-left: 1px solid #e2e8f0;
  padding-left: 24px;
}

.announcement-list {
  list-style: none;
  padding: 0;
  margin: 0 0 16px 0;
}

.announcement-list li {
  margin-bottom: 16px;
}

.brochure-line {
  font-size: 14px;
  margin-bottom: 16px;
}

.icon-link {
  display: inline-block;
}
```

## Expected Behavior

- Staff and musicians view upcoming rehearsals as a list of cards (date, time, location, conductor).
- Each card offers a calendar shortcut and an expandable panel showing section call times.
- A small flag icon marks rehearsals that have conductor notes attached.
- A sidebar lists season announcements, a link to the full brochure, and a share shortcut.

## Accessibility Features Present

✓ Calendar button has aria-label naming the specific rehearsal
✓ Section-call-times toggle has aria-expanded and aria-controls
✓ Section-call-times panel uses the hidden attribute rather than conditional unmounting
✓ Rehearsal list and announcement list use ul/li semantics
✓ Both regions are headed by h2 elements and connected via aria-labelledby
✓ Calendar and section-call-times controls follow DOM/tab order matching their visual left-to-right position on the card

## Accessibility Issues

_Answer key: planted defects._

1. **MUST-FIND / MAJOR: Conductor-notes flag receives focus out of visual order and is not operable once reached.** The `<span className="notes-flag" tabIndex="0">` is the LAST focusable element in the card's DOM order (after the calendar button and the section-call-times toggle), but CSS `position: absolute; top: 10px; right: 12px` visually places it in the top-right corner of the card — where the title already is. A keyboard user tabs through the calendar button, then the section-call-times toggle, and only then lands on the notes flag — focus visibly jumps backward to the top of the card, out of the order a sighted keyboard user would predict from scanning top-to-bottom. Once focus lands there, Enter and Space do nothing: the span has no `role="button"`, no `onClick`, and no `onKeyDown`. The element is reachable but not actionable — a dead stop.
   - Evidence: `rehearsal-schedule-panel.md` — `tabIndex="0"` on the notes-flag span with no role or handler; CSS `.notes-flag { position: absolute; top: 10px; right: 12px; }` against `.rehearsal-card { position: relative; }`
   - WCAG: 2.4.3 Focus Order (focus order does not preserve meaning), 4.1.2 Name, Role, Value (focusable element has no role or operable behavior)
   - Impact: Screen reader and keyboard users are pulled to an element that visually reads as "back near the title" after already tabbing past two working controls, then find nothing happens when they try to activate it
   - User group: Keyboard users, screen reader users
   - Fix: Either make the flag a real control (`role="button"`, `tabIndex="0"`, `onClick`/`onKeyDown` that opens the conductor notes, and move it earlier in DOM order to match its visual position) or remove `tabIndex="0"` and expose the "has notes" state through the existing section-call-times toggle instead (e.g., append "— conductor notes attached" to its accessible name)

2. **SHOULD-FIND / MAJOR: Repeated "Read more" links give screen reader and switch users no way to distinguish destinations out of context.** All three season announcements end in identical link text ("Read more"), pointing to three different pages. A screen reader user pulling up a list of links (a common navigation strategy) hears "Read more, Read more, Read more" with no way to tell them apart without first reading each surrounding paragraph in full.
   - Evidence: `rehearsal-schedule-panel.md` — three `<a>Read more</a>` links inside `.announcement-list`, each with different `href` but identical visible text
   - WCAG: 2.4.4 Link Purpose (In Context), 2.4.9 Link Purpose (Link Only)
   - Impact: Users who navigate by pulling up a links list cannot tell the announcements apart; each link's purpose is only clear from surrounding prose, which a links-list view does not include
   - User group: Screen reader users navigating by links list, switch-access users using link menus
   - Fix: Give each link an accessible name that includes its subject, e.g. `aria-label="Read more about winter subscription renewals"`, or restructure the text to make the link itself descriptive ("Read about winter subscription renewals")

3. **SHOULD-FIND / MAJOR: Icon-only share link has no accessible name at all.** The `<a href="/staff/schedule/share">` wrapping the share icon has no text content and no `aria-label`; the icon inside is `aria-hidden="true"` (correctly hiding the decorative glyph). The combination leaves the link with an empty accessible name — screen readers announce it as "link" with no further information, or skip it silently depending on the AT.
   - Evidence: `rehearsal-schedule-panel.md` — `<a href="/staff/schedule/share" className="icon-link"><ShareIcon aria-hidden="true" /></a>` with no visible text and no aria-label on the anchor
   - WCAG: 4.1.2 Name, Role, Value; 2.4.4 Link Purpose (In Context)
   - Impact: Screen reader users cannot tell this link exists or what it does; it is present in the tab order but functionally anonymous
   - User group: Screen reader users
   - Fix: Add `aria-label="Share this rehearsal schedule"` to the anchor (the icon itself can remain `aria-hidden`)

## Difficulty Level

**HAS-BUGS** — The calendar button and section-call-times toggle are fully and correctly remediated: proper accessible names, correct `aria-expanded`/`aria-controls`, and a persistent (not conditionally-unmounted) panel. The notes-flag bug and the two link-text issues are clear, independently verifiable defects rather than subtle interaction gaps — but they are easy to miss if a reviewer only checks that "the interactive elements have accessible names" without walking the actual tab sequence against the visual layout, and without checking link text in the context a screen reader user actually experiences it (a links list, not surrounding prose).

This is the suite's first fixture covering WCAG 2.4.4 Link Purpose (In Context) — prior HAS-BUGS fixtures test ARIA pattern completeness and live-region gaps, not link-text ambiguity.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Notes

Three independent findings, one must_find and two should_find:

1. **Focus-order tracing** (must_find) — the bug only surfaces when a reviewer mentally walks the tab sequence against the rendered layout, the same skill tested by the FLAWED-tier `app-focus-order-illogical` fixture, but here surfacing as a HAS-BUGS-tier defect: clearly wrong once traced, not deeply hidden.
2. **Link-text ambiguity at the links-list level** (should_find) — requires imagining how a screen reader's "list of links" feature would present three identical strings, not just reading the links in page context where surrounding prose disambiguates them.
3. **Empty accessible name recognition** (should_find) — requires distinguishing "the icon is correctly hidden from AT" (true, and not itself a bug) from "the link that wraps it has no name" (the actual bug) — a reviewer who flags the `aria-hidden` on the icon itself would be raising a false positive.
