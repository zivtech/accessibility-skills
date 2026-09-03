# Fixture: Async Request Failure and Recovery Are Never Announced

## Component Code

```jsx
const AccountActivityPanel = ({ accountId }) => {
  const [status, setStatus] = useState('loading'); // 'loading' | 'error' | 'ready'
  const [transactions, setTransactions] = useState([]);

  const load = useCallback(async () => {
    setStatus('loading');
    try {
      const res = await fetch(`/api/accounts/${accountId}/activity`);
      if (!res.ok) throw new Error('Request failed');
      setTransactions(await res.json());
      setStatus('ready');
    } catch (err) {
      setStatus('error');
    }
  }, [accountId]);

  useEffect(() => { load(); }, [load]);

  return (
    <section className="activity-panel" aria-labelledby="activity-heading">
      <header className="panel-header">
        <h2 id="activity-heading">Account Activity</h2>
        <button type="button" className="retry" onClick={load}>
          Retry
        </button>
      </header>

      <div className="panel-body" aria-busy={status === 'loading'}>
        {status === 'loading' && (
          <div className="loading" role="status" aria-live="polite" aria-atomic="true">
            <span className="spinner" aria-hidden="true" />
            Loading activity…
          </div>
        )}

        {status === 'error' && (
          <p className="error-text">
            We couldn&rsquo;t load your activity. Check your connection and try again.
          </p>
        )}

        {status === 'ready' && (
          <ul className="txn-list">
            {transactions.map(t => (
              <li key={t.id}>
                <span className="txn-date">{t.date}</span>
                <span className="txn-payee">{t.payee}</span>
                <span className="txn-amount">{t.amount}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
};

export default AccountActivityPanel;
```

## CSS

```css
.activity-panel {
  max-width: 640px;
  margin: 24px auto;
  border: 1px solid #d0d5dd;
  border-radius: 8px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #d0d5dd;
}

.panel-header h2 {
  margin: 0;
  font-size: 1.125rem;
}

.retry {
  padding: 6px 14px;
  border: 1px solid #0b5fff;
  border-radius: 4px;
  background: #fff;
  color: #0b5fff;
  cursor: pointer;
}

.panel-body {
  padding: 16px;
  min-height: 120px;
}

.loading {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #475467;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid #eaecf0;
  border-top-color: #0b5fff;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-text {
  margin: 0;
  color: #b42318;
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
  border-bottom: 1px solid #eaecf0;
}
```

## Expected Behavior

- On mount, the panel fetches account activity and shows a loading indicator.
- If the request fails, the panel shows an error message and the user can press **Retry**.
- If the retry succeeds, the transaction list replaces the error message.
- The **Retry** button lives in the panel header and stays mounted in every state, so pressing it never destroys the user's focus position.

## Accessibility Issues (Planted)

1. **CRITICAL: Request failure is never announced** — The `loading` branch is a correct live region (`role="status"`, `aria-live="polite"`, `aria-atomic="true"`), but the `error` branch is a plain `<p className="error-text">` with no `role="alert"`, no `aria-live`, and no live-region ancestor. When the fetch rejects, the loading region unmounts and the error paragraph mounts silently. A screen reader user hears "Loading activity…", then nothing at all — no failure, no instruction, no reason to look for the Retry button. They are left believing the request is still in flight.
   - Evidence: `async-retry-error-unannounced.md:41-45` (error branch has no `role="alert"` / `aria-live`); contrast `:34-39` where the loading branch does.
   - WCAG citation: 4.1.3 Status Messages (an error that does not take focus must be presented as a status message)
   - User group: Screen reader users
   - Expected: The failure message should be exposed through an assertive live region (`role="alert"`) so it is announced without moving focus.
   - Fix: Render the failure text into a persistent `role="alert"` container that is present in the DOM in every state, rather than mounting a bare `<p>` at failure time.

2. **MAJOR: Recovery after a successful retry is silent** — When the user presses **Retry** and the second request succeeds, `status` moves `error` → `loading` → `ready`. The error paragraph unmounts and the `<ul className="txn-list">` mounts. Nothing announces that the error has cleared or that data has arrived: the list is not a live region, and the only live region in the component (`:34-39`) unmounts at the moment the results appear. The user who was never told the request failed is now also never told that it succeeded, and has no way to know whether pressing Retry did anything.
   - Evidence: `async-retry-error-unannounced.md:47-57` (results list mounts with no announcement; the sole live region at `:34-39` is gone by the time it renders)
   - WCAG citation: 4.1.3 Status Messages (the outcome of a user-initiated retry is a status change that must be announced)
   - User group: Screen reader users
   - Expected: A successful retry should announce both that the failure is resolved and what arrived (e.g. "Loaded 8 transactions.").
   - Fix: Keep a persistent `role="status"` region mounted across all three states and write the outcome into it, so the transition out of the error state is announced.

## Difficulty Level

**HAS-BUGS** — The happy path is instrumented correctly and the failure and recovery paths are not, which is the usual shape of this defect: `aria-busy` and the loading announcement are present, so an automated scan and a quick read both come back clean. Finding these two requires tracing the state machine through `error` and back out of it, not pattern-matching for a missing `aria-live`.
