# Fixture: Account Activity Panel with Retry

## Component Code

```jsx
// Presentational: the request lifecycle belongs to the container above it.
// This component's whole job is to say what happened, in a way assistive
// technology hears.
const AccountActivityPanel = ({ status, transactions, onRetry }) => (
  <section className="activity-panel" aria-labelledby="activity-heading">
    <header className="panel-header">
      <h2 id="activity-heading">Account Activity</h2>
      <button type="button" className="retry" onClick={onRetry}>
        Retry
      </button>
    </header>

    <div className="panel-body">
      {/* Persistent status region. It stays mounted in every state, so text
          written into it is announced. A region that mounts with its message
          already inside it is frequently not spoken at all. */}
      <div className="panel-status" role="status" aria-live="polite" aria-atomic="true">
        {status === 'loading' && (
          <>
            <span className="spinner" aria-hidden="true" />
            Loading activity…
          </>
        )}
        {status === 'ready' && (
          transactions.length > 0
            ? `Loaded ${transactions.length} transactions.`
            : 'No activity in this period.'
        )}
      </div>

      {/* Persistent alert region, a sibling of the status region rather than a
          replacement for it — so the recovery message still has somewhere to
          land after a failure. Assertive, because it names an action the user
          has to take. */}
      <div className="panel-error" role="alert">
        {status === 'error' && (
          <>We couldn&rsquo;t load your activity. Select Retry to try again.</>
        )}
      </div>

      {status === 'ready' && transactions.length > 0 && (
        <ul className="txn-list" role="list">
          {transactions.map(t => (
            <li key={t.id}>
              <span className="txn-payee">{t.payee}</span>
              <span className="txn-amount">{t.amount}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  </section>
);
```

## CSS

```css
.panel-status {
  color: #475467;
}

.panel-error {
  color: #b42318;
}

.retry {
  color: #0b5fff;
  border: 1px solid #0b5fff;
  background: #fff;
  padding: 6px 14px;
}

.retry:focus-visible {
  outline: 3px solid #0b5fff;
  outline-offset: 2px;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #eaecf0;
  border-top-color: #0b5fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .spinner { animation: none; border-top-color: #0b5fff; }
}

.txn-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.txn-list li {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 8px 0;
}
```

## Expected Behavior

- The parent owns the request. This component renders one of four states — `loading`, `error`, `ready` with transactions, `ready` with none — and reports each one.
- The status region and the alert region are both in the DOM in every state; text is written into them rather than mounted with them.
- A failure is announced assertively and names the control that recovers from it. A recovery after Retry is announced politely, as is an empty result.
- The Retry control is in the header and never unmounts, so no state change destroys the user's focus position. Whether it is disabled during a request, and whether a press while one is already in flight is acknowledged, belong to the parent that owns the request.
- The parent is expected to mount this component before starting the first request. A panel that first renders already in `loading` puts the message into the region in the same commit that creates it, which is the one case the persistent-region pattern cannot cover.

## Accessibility Features Present

1. **Persistent live regions** — `.panel-status` (`role="status"`) and `.panel-error` (`role="alert"`) are in the DOM in every state (`async-retry-recovery-clean.md:22`, `:40`), with text written into them rather than being mounted alongside their own content. This is what makes every *transition* announce: a live region that appears with its message already inside is frequently not spoken. The one case it cannot cover on its own is the first paint, which is why mounting before the first request is stated above as the parent's contract.
2. **Recovery has somewhere to land** — the two regions are siblings rather than alternatives, so the `error` → `loading` → `ready` sequence produces a spoken outcome instead of the status region having been replaced by the error.
3. **Politeness matched to urgency** — a failure that requires a user action is `role="alert"` (assertive); a routine result count is `role="status"` (polite).
4. **The empty result is a message, not a blank panel** (`:31-32`) — a successful response with no transactions says so, rather than announcing a count of zero or nothing at all.
5. **The error names its remedy** (`:42`) — "Select Retry to try again" matches the visible button label, so a user who hears the failure knows the exact control to look for.
6. **Focus survives every state change** — the Retry control is in the header (`:13`), outside the region that swaps, so it never unmounts.
7. **Decorative spinner hidden** (`:25`) — `aria-hidden="true"`, with the adjacent text inside the same region carrying the message; `prefers-reduced-motion` disables the animation.
8. **`role="list"` on the delisted list** (`:47`) — `list-style: none` makes WebKit drop the implicit list role, so a VoiceOver user would lose "list, N items"; the attribute restores it.

## Accessibility Issues

_Answer key: none planted (CLEAN baseline)._

None. This fixture is a CLEAN baseline with no planted defects. Everything from
this heading down is ground-truth material and is stripped from model prompts by
the blind protocol (`ANSWER_KEY_RE` in the runners).

## Difficulty Level

**CLEAN** — Baseline for false-positive avoidance on async status messages. The two live-region containers that are empty in most states, the two different politeness levels in one component, the `aria-hidden` spinner, and the `role="list"` on a `<ul>` are each a correct decision that reads like a defect to a reviewer scanning for patterns rather than reasoning about when and whether a message is spoken.
