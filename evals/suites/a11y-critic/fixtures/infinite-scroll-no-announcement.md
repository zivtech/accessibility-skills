# Fixture: Infinite Scroll Without Loading Announcements

## Component Code

```jsx
import React, { useState, useEffect, useRef, useCallback } from 'react';

const BuggyInfiniteScroll = () => {
  const [items, setItems] = useState([]);
  const [page, setPage] = useState(1);
  const observerTarget = useRef(null);
  // BUG: No aria-live region for loading announcements
  // BUG: No way to announce "more items loaded"

  const loadMore = useCallback(async () => {
    // Simulate API call
    const newItems = Array.from({ length: 10 }, (_, i) => ({
      id: page * 10 + i,
      text: `Item ${page * 10 + i}`,
    }));
    setItems((prev) => [...prev, ...newItems]);
    setPage((prev) => prev + 1);
    // BUG: No announcement that items were loaded
    // Screen reader user doesn't know page refreshed
  }, [page]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          loadMore();
        }
      },
      { threshold: 0.1 }
    );

    if (observerTarget.current) {
      observer.observe(observerTarget.current);
    }

    return () => observer.disconnect();
  }, [loadMore]);

  return (
    <div className="infinite-scroll-container">
      {/* BUG: No landmark or region wrapping the list */}
      <ul className="items-list">
        {items.map((item) => (
          <li key={item.id}>{item.text}</li>
        ))}
      </ul>

      <div ref={observerTarget} className="scroll-trigger">
        {/* BUG: No visible loading indicator or announcement */}
        {/* BUG: No accessible way to know items are loading */}
      </div>
    </div>
  );
};

export default BuggyInfiniteScroll;
```

## Expected Behavior

- Items load as user scrolls to bottom
- Screen reader announces when new items load
- Loading state visible and announced
- User can understand infinite scroll is working
- Landmark identifies list as main content

## Accessibility Features Present

✓ Semantic <ul> and <li> list structure
✓ Loading mechanism (Intersection Observer)

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing aria-live region for loading announcements** — No aria-live region to announce when new items load. Screen reader user doesn't know that content has been added to the list. Per WCAG 4.1.3 (Status Messages), loading status must be announced.
   - Evidence: `infinite-scroll-no-announcement.md:50-57` (no aria-live element)
   - User group: Screen reader users (critical)
   - Expected: aria-live="polite" region should announce "10 more items loaded"
   - Fix: Add aria-live="polite" region that announces loading completion

2. **CRITICAL: No loading state announcement** — While items load, no visual or accessible indication that loading is happening. Screen reader user cannot tell if page is still loading or if loading failed.
   - Evidence: `infinite-scroll-no-announcement.md:36-40` (loadMore completes silently)
   - User group: Screen reader users (critical)
   - Expected: Loading state should be announced (e.g., "Loading more items...")
   - Fix: Add aria-live region to announce loading start and completion

3. **MAJOR: No main landmark** — List is just a div+ul without main landmark. Screen reader user cannot quickly navigate to main content. Per landmark structure, main content region should be marked with <main> or role="main".
   - Evidence: `infinite-scroll-no-announcement.md:44-57` (div has no landmark role)
   - User group: Screen reader users
   - Expected: Container should have role="main" or be <main>
   - Fix: Wrap content in <main> or add role="main"

4. **MAJOR: Scroll-to-load mechanism not discoverable** — Screen reader user doesn't know that scrolling to bottom loads more items. No indication that infinite scroll is enabled or how to use it.
   - Evidence: `infinite-scroll-no-announcement.md:36-40` (Intersection Observer is silent)
   - User group: Screen reader users
   - Expected: Instructions or announcements should explain infinite scroll behavior
   - Fix: Add aria-live announcement or instructions explaining infinite scroll

## Difficulty Level

**HAS-BUGS** — Dynamic content loading without announcements. List structure is correct but state changes are invisible to screen reader users.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should identify that infinite scroll patterns require aria-live announcements to communicate dynamic content changes. Many developers miss this because the mechanism works visually but fails for AT users.
