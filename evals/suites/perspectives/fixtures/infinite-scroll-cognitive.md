# Fixture: Infinite Scroll Feed With Cognitive Navigation Breakdown

## Component Code

```jsx
import React, { useState, useEffect, useRef, useCallback } from 'react';

const generateCards = (start, count) =>
  Array.from({ length: count }, (_, i) => ({
    id: start + i,
    title: `Article ${start + i}: ${['Breaking News', 'In-Depth Analysis', 'Opinion', 'Feature Story', 'Report'][i % 5]}`,
    excerpt: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    author: ['Jane Smith', 'Alex Chen', 'Maria Garcia', 'Sam Johnson', 'Lee Williams'][i % 5],
    timestamp: Date.now() - (start + i) * 120000,
    image: `/img/article-${(start + i) % 8}.jpg`,
  }));

const InfiniteScrollFeed = () => {
  const [cards, setCards] = useState(() => generateCards(1, 10));
  const [loading, setLoading] = useState(false);
  const sentinelRef = useRef(null);
  const containerRef = useRef(null);

  // BUG: Auto-loads on scroll — no "Load more" button alternative
  // Keyboard users get trapped in infinite Tab sequence
  const loadMore = useCallback(() => {
    if (loading) return;
    setLoading(true);
    setTimeout(() => {
      setCards(prev => [...prev, ...generateCards(prev.length + 1, 10)]);
      setLoading(false);
    }, 500);
  }, [loading]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => { if (entries[0].isIntersecting) loadMore(); },
      { threshold: 0.1 }
    );
    if (sentinelRef.current) observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [loadMore]);

  // BUG: Relative timestamps update every 60s — content shifts while reading
  const [, setTick] = useState(0);
  useEffect(() => {
    const interval = setInterval(() => setTick(t => t + 1), 60000);
    return () => clearInterval(interval);
  }, []);

  const relativeTime = (ts) => {
    const diff = Math.floor((Date.now() - ts) / 60000);
    if (diff < 1) return 'just now';
    if (diff < 60) return `${diff}m ago`;
    if (diff < 1440) return `${Math.floor(diff / 60)}h ago`;
    return `${Math.floor(diff / 1440)}d ago`;
  };

  return (
    <main className="feed-page">
      <h1>Your Feed</h1>

      {/* BUG: No position indicator, no "back to top", no page numbers —
          user cannot tell where they are in the feed — WCAG 2.4.8 */}

      <div className="feed-container" ref={containerRef}>
        {cards.map(card => (
          <article key={card.id} className="feed-card" aria-label={card.title}>
            <img src={card.image} alt="" className="card-image" />
            <div className="card-body">
              <h2><a href={`/article/${card.id}`}>{card.title}</a></h2>
              <p className="card-excerpt">{card.excerpt}</p>
              <div className="card-meta">
                <span className="card-author">{card.author}</span>
                <span className="card-time">{relativeTime(card.timestamp)}</span>
              </div>
            </div>
          </article>
        ))}

        <div ref={sentinelRef} className="load-sentinel">
          {loading && (
            <div aria-live="polite">
              <span className="sr-only">Loading more articles</span>
              <div className="spinner" />
            </div>
          )}
        </div>

        {/* BUG: No "end of feed" indicator — feed appears infinite */}
      </div>
    </main>
  );
};

export default InfiniteScrollFeed;
```

```css
.feed-page {
  max-width: 680px;
  margin: 0 auto;
  padding: 24px;
  font-family: system-ui, sans-serif;
}

.feed-page h1 {
  font-size: 1.75rem;
  margin-bottom: 24px;
  color: #111;
}

/* BUG: No position indicator UI — no page numbers, no "back to top" */
.feed-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feed-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fff;
}

.card-image {
  width: 120px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
  flex-shrink: 0;
}

.card-body { flex: 1; }

.card-body h2 {
  font-size: 1.1rem;
  margin: 0 0 8px;
}

.card-body h2 a {
  color: #1565c0;        /* 5.4:1 on white */
  text-decoration: underline;
}

.card-body h2 a:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

.card-excerpt {
  font-size: 0.9rem;
  color: #333;            /* 12.6:1 */
  line-height: 1.5;
  margin: 0 0 8px;
}

.card-meta {
  display: flex;
  gap: 12px;
  font-size: 0.8rem;
  color: #555;            /* 7.5:1 */
}

.load-sentinel {
  min-height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.spinner {
  width: 24px; height: 24px;
  border: 3px solid #e0e0e0;
  border-top-color: #1565c0;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.sr-only {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0,0,0,0); border: 0;
}

@media (max-width: 600px) {
  .feed-card { flex-direction: column; }
  .card-image { width: 100%; height: 160px; }
}
```

## Expected Behavior

- Vertically scrolling feed of article cards
- New cards auto-load when user scrolls near the bottom
- Each card shows title, excerpt, author, and timestamp
- Loading spinner appears during fetch

## Accessibility Features Present

- `<main>` landmark, h1 for page heading
- Each card is `<article>` with `aria-label`
- Card headings use `<h2>` with linked titles
- Links have descriptive text (article titles, underlined)
- Focus-visible outlines on all links
- Loading state announced via `aria-live="polite"` with sr-only text
- Images have `alt=""` (decorative)
- Responsive layout at 600px
- All contrast passes WCAG AA

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: No position indicator, no "back to top", no page numbers — WCAG 2.4.8 (Location)**
   User cannot determine where they are in the feed. No visible "back to top" button, no "showing 1-10 of N", no page counter. After scrolling, the only way back is manual scroll.
   - Evidence: No position UI in the component; `.feed-container` has no position indicator
   - User group: Cognitive users, all users
   - Fix: Add "Back to top" sticky button, feed position indicator, and "Page N of M" or "Showing 1-N" text

2. **MAJOR: Auto-loads on scroll — no "Load more" button alternative — WCAG 2.2.2 / 2.1.1**
   IntersectionObserver triggers auto-load with no explicit "Load more" button. Keyboard users tabbing through cards trigger loading when Tab reaches the sentinel, creating an infinite Tab sequence.
   - Evidence: Lines 25-35 — IntersectionObserver auto-loads; no button alternative
   - User group: Keyboard users, cognitive users
   - Fix: Add "Load more" button before sentinel; make auto-load an opt-in preference

3. **MAJOR: Virtual scrolling removes offscreen DOM nodes — WCAG 2.4.3 (Focus Order)**
   While this implementation appends (doesn't virtualize), a cognitive navigation breakdown occurs: user loses mental position, previously read content is unreachable by any navigation shortcut.
   - Evidence: Feed grows unboundedly; no way to navigate to "previously read" content
   - User group: Keyboard users, screen reader users, cognitive users
   - Fix: Implement pagination or bounded feed with "page" boundaries

4. **MINOR: Relative timestamps change while reading — Cognitive best practice**
   Timestamps like "3m ago" update every 60 seconds via setInterval, shifting content the user is reading.
   - Evidence: Lines 40-43 — setInterval re-renders timestamps every 60s
   - User group: Cognitive/attention users
   - Fix: Use static timestamps (e.g., "2:15 PM") or only update when off-screen

5. **MINOR: No "end of feed" indicator**
   Feed appears to extend infinitely. No empty state or "You've reached the end" message.
   - Evidence: No end-of-feed check or message in the component
   - User group: Cognitive users
   - Fix: Detect when server returns empty results; show "No more articles" message

## Difficulty Level

**ADVERSARIAL** — Passes automated scans (axe-core finds no issues). Individual card accessibility is excellent. The bugs are structural/cognitive: navigation breakdown, unbounded growth, auto-loading without user control. Requires perspective-level reasoning (cognitive, keyboard) to identify.

## Frameworks

React 18+, IntersectionObserver API, CSS
