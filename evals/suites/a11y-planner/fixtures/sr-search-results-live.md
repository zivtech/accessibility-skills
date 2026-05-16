# Fixture: Search Results Page with Live-Updating Count

## Feature Description

You're planning accessibility for a search results page on a legal research platform. As the user types in the search box or applies filter chips, the result count updates instantly ("247 results" → "12 results"), the results list re-renders with matching items, and active filter chips appear above the results. The interface includes a search input with autocomplete suggestions, a horizontal strip of dismissible filter chips (Subject, Date Range, Jurisdiction), a sort control with options (Relevance, Date, Citation Count), a live-updating result count displayed as plain text above the result list, paginated result cards (title, summary, citation, date), and a "loading" spinner that appears during async fetches. The result count updates on every keystroke after a 300ms debounce. Filter chip additions and removals trigger immediate re-queries. The sort control change also triggers a re-query.

## Context

- **Platform:** Next.js 14 App Router with React Server Components; result fetching via React Suspense
- **Existing code:** Yes — search input and filter chips exist; result count is a plain `<p>` with no ARIA; sort control is a `<select>` element; loading state is a CSS spinner with no AT announcement; filter chips are `<button>` elements with no pressed state
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Search results page — live region for count, filter chip state communication, sort control state, loading announcement, result set announcement
- **Constraints:** 300ms debounce on keystroke; React Suspense loading states; filter chips appear/disappear dynamically; result count must not interrupt user typing; multiple simultaneous state changes possible (filter + sort + new query)

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- Semantic structure (search landmark, result list semantics)
- `aria-live` region strategy for result count (polite vs assertive, debounce timing)
- `aria-relevant` attribute decision for added/removed results
- `aria-atomic` decision for the result count region
- `aria-busy` pattern for loading states
- Filter chip state communication (`aria-pressed` for toggle state, dismissal announcement)
- Sort control state (`aria-sort` does not apply to a `<select>` — correct pattern)
- Result set grouping semantics (list, region, or table)
- Focus management after filter/sort changes
- Loading state announcement (spinner → "Loading results" → count update)
- Testing strategy for live announcements with multiple AT
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is a **MODERATE** difficulty fixture — the challenge is live region strategy design, not ARIA widget complexity. Expected plan length: 3-4 pages. Focus on:

1. Live region placement: the result count `<p>` needs `aria-live="polite"` with `aria-atomic="true"` — but HOW the DOM update is timed matters (the 300ms debounce must align with live region polling intervals in NVDA/JAWS)
2. `aria-relevant`: explain why `aria-relevant="additions text"` is the right value for a count that only grows/shrinks as text, not DOM nodes being added
3. `aria-busy="true"` on the results container during loading, set to `false` when results land
4. Filter chip `aria-pressed` for toggle state — and whether dismissed chips announce "removed" or just disappear
5. The sort `<select>` does not use `aria-sort`; `aria-sort` is for column headers in tables
6. Focus management decision: does focus move after filtering? (No — announce without moving focus)

## What Success Looks Like

An excellent plan would:
- ✓ Place `aria-live="polite" aria-atomic="true"` on the result count element with a WCAG 4.1.3 citation
- ✓ Explain the debounce timing constraint: live region updates should be debounced to avoid flooding the AT queue
- ✓ Correctly differentiate `aria-relevant="additions text"` from the default behavior and explain when to use each value
- ✓ Document `aria-busy="true"` on the results container during async fetches, citing that screen readers defer reading busy regions
- ✓ Specify `aria-pressed="true|false"` on filter chip buttons with a visible label that includes the filter name ("Subject: Case Law — remove filter")
- ✓ Correct the `aria-sort` misconception — `aria-sort` applies to `<th>` elements in sortable tables, not to `<select>` controls; the sort `<select>` needs a visible `<label>` and its selected `<option>` communicates the current state
- ✓ Plan the result list as `<ul>` / `<li>` with each result as a list item — not a table (results are not tabular data)
- ✓ Define a `role="search"` landmark wrapping the search input and filters
- ✓ Cite WCAG 4.1.3 (Status Messages), 1.3.1 (Info and Relationships), 2.4.3 (Focus Order)
- ✓ Include screen reader testing plan: verify count announced after filter change without focus move

## What Would Be Below Expectations

- ✗ Using `aria-live="assertive"` for the result count — interrupts user typing mid-search
- ✗ Not addressing the debounce timing constraint — live regions updated on every keystroke will flood NVDA/JAWS
- ✗ Applying `aria-sort` to the sort `<select>` — wrong element; aria-sort is a th attribute
- ✗ No `aria-busy` pattern for loading states — spinner is invisible to AT
- ✗ Filter chips with no `aria-pressed` — AT cannot communicate toggle state
- ✗ Focus moving to result list after every filter change — disruptive and fails WCAG 2.4.3
- ✗ No `role="search"` landmark wrapping the search interface
- ✗ No WCAG 4.1.3 citation for the live result count
