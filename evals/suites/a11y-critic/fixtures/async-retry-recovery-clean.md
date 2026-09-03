# Fixture: Account Activity Panel with Retry

## Component Code

```jsx
const AccountActivityPanel = ({ accountId }) => {
  const [status, setStatus] = useState('loading'); // 'loading' | 'error' | 'ready'
  const [transactions, setTransactions] = useState([]);
  // The attempt number, so a retry writes different text than the first load.
  // Re-writing an identical string into a live region is not a DOM change and
  // is not announced, which would make a repeat press silent.
  const [attempt, setAttempt] = useState(0);
  // A superseded request must never reach the live regions. Without this, two
  // Retry presses (or an accountId change mid-flight) can let a slow failure
  // resolve after a fast success and interrupt assertively with "we couldn't
  // load your activity" over transactions the user was just told about.
  const requestId = useRef(0);

  const load = useCallback(async () => {
    if (requestId.current > 0 && status === 'loading') return;
    const id = ++requestId.current;
    setAttempt(a => a + 1);
    setStatus('loading');
    try {
      const res = await fetch(`/api/accounts/${accountId}/activity`);
      if (!res.ok) throw new Error('Request failed');
      const data = await res.json();
      if (id !== requestId.current) return;
      setTransactions(data);
      setStatus('ready');
    } catch (err) {
      if (id !== requestId.current) return;
      setStatus('error');
    }
  }, [accountId, status]);

  useEffect(() => {
    load();
    return () => { requestId.current += 1; };
  }, [load]);

  return (
    <section className="activity-panel" aria-labelledby="activity-heading">
      <header className="panel-header">
        <h2 id="activity-heading">Account Activity</h2>
        {/* aria-disabled rather than disabled: the control keeps its place in
            the Tab order and can still be found, but a press while a request is
            already in flight is announced as unavailable instead of doing
            nothing silently. */}
        <button
          type="button"
          className="retry"
          onClick={load}
          aria-disabled={status === 'loading'}
        >
          Retry
        </button>
      </header>

      {/* aria-busy deliberately NOT on this wrapper: it is the ancestor of both
          live regions, and an AT that honours ancestor busy state may withhold
          the very message being written into them. It sits on the results list
          below, which is the content that actually goes stale. */}
      <div className="panel-body">
        {/* Persistent status region. It stays mounted in every state, so text
            written into it is announced. A region that mounts with its message
            already inside is frequently not spoken at all. */}
        <div className="panel-status" role="status" aria-live="polite" aria-atomic="true">
          {status === 'loading' && (
            <>
              <span className="spinner" aria-hidden="true" />
              {attempt > 1 ? 'Retrying…' : 'Loading activity…'}
            </>
          )}
          {status === 'ready' && (
            transactions.length > 0
              ? `Loaded ${transactions.length} transactions.`
              : 'No activity in this period.'
          )}
        </div>

        {/* Persistent alert region. A failed request is actionable, so it is
            assertive; it is a sibling of the status region, never a replacement
            for it, so the recovery message still has somewhere to land. */}
        <div className="panel-error" role="alert">
          {status === 'error' &&
            'We couldn’t load your activity. Check your connection and press Retry.'}
        </div>

        {status === 'ready' && transactions.length > 0 && (
          <ul className="txn-list" role="list" aria-busy={status === 'loading'}>
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

.retry:focus-visible {
  outline: 3px solid #0b5fff;
  outline-offset: 2px;
}

.panel-body {
  padding: 16px;
  min-height: 120px;
}

.panel-status {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #475467;
}

.panel-error {
  color: #b42318;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid #eaecf0;
  border-top-color: #0b5fff;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}

@media (prefers-reduced-motion: reduce) {
  .spinner { animation: none; border-top-color: #0b5fff; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
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

- On mount the panel fetches account activity; the status region announces "Loading activity…".
- If the request fails, the alert region announces the failure and names the control that fixes it.
- If the user presses **Retry** and the second request succeeds, the alert region empties and the status region announces "Loaded 8 transactions." — so the user hears both that the failure is over and what arrived.
- If the successful response is empty, the status region announces "No activity in this period." rather than falling silent.
- The **Retry** button is in the panel header and stays mounted in every state, so pressing it never destroys the user's focus position.

## Accessibility Features Present

1. **Persistent live regions** — `.panel-status` (`role="status"`) and `.panel-error` (`role="alert"`) are in the DOM in every state, with text written into them rather than being mounted alongside their own content. This is what makes the announcements reliable; a live region that appears with its message already inside is frequently not spoken. The invariant covers every state *transition*; the very first paint is the one moment it cannot cover, since the panel mounts in its loading state, so the initial "Loading activity…" is the one message that may not be spoken. Every outcome — failure, recovery, empty result — is announced from a region that was already registered.
2. **Recovery is announced** — because the status region outlives the error state, the transition `error` → `loading` → `ready` produces a spoken outcome instead of silence.
3. **Politeness matched to urgency** — a failed request that requires a user action is `role="alert"` (assertive); a routine result count is `role="status"` (polite).
4. **`aria-busy` on the results list, not on the live regions' ancestor** — the list is the content that goes stale while a request is in flight. Putting it on the wrapper that also contains the status and alert regions would let an AT honouring ancestor busy state withhold the very message being written into them.
5. **Empty results announced** — the zero-length case has its own message rather than rendering nothing.
6. **A repeat Retry press is observable** — the control carries `aria-disabled` while a request is in flight, so a press during loading is announced as unavailable instead of doing nothing, and the in-flight message becomes "Retrying…" on later attempts. Re-writing an identical string into a live region is not a DOM change and is not announced, so a repeat press with the same text would have been silent.
7. **Focus preserved across state changes** — the Retry control never unmounts, and has a visible `:focus-visible` indicator.
8. **Decorative spinner hidden** — `aria-hidden="true"`, with the adjacent text inside the same region carrying the message; `prefers-reduced-motion` disables the animation.

## Accessibility Issues (None Planted — CLEAN Baseline)

None. This fixture is a CLEAN baseline with no planted defects. Everything from
this heading down is ground-truth material and is stripped from model prompts by
the blind protocol (`ANSWER_KEY_RE` in the runners).

## Difficulty Level

**CLEAN** — Baseline for false-positive avoidance on async status messages. The two mostly-empty live-region containers, the two different politeness levels in one component, and the `aria-hidden` spinner are each a correct decision that reads like a defect to a reviewer scanning for patterns rather than reasoning about announcement timing.
