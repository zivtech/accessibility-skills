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
