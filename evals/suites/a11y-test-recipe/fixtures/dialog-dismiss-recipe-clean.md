# Fixture: Delete-Report Dialog — Keyboard Dismiss Recipe

## Component Code

```jsx
import { useEffect, useRef, useState } from 'react';

const FOCUSABLE =
  'button:not([disabled]), [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

export function ReportsPage({ reports, onDelete, onCloseAccount }) {
  const [confirming, setConfirming] = useState(null);
  const triggerRef = useRef(null);

  function finish() {
    setConfirming(null);
    triggerRef.current?.focus();
  }

  return (
    <>
      <div id="app-root" inert={confirming ? '' : undefined}>
        <header className="toolbar">
          <h1>Reports</h1>
          <button type="button">New report</button>
          <button type="button" ref={triggerRef} onClick={() => setConfirming(reports[0])}>
            Delete report
          </button>
        </header>
        <ul className="report-list">
          {reports.map((r) => (
            <li key={r.id}>{r.title}</li>
          ))}
        </ul>
        <section className="account" aria-labelledby="account-heading">
          <h2 id="account-heading">Account</h2>
          <button type="button" className="account__close" onClick={onCloseAccount}>
            Close account
          </button>
        </section>
      </div>
      {confirming && (
        <DeleteReportDialog
          report={confirming}
          onCancel={finish}
          onConfirm={() => {
            onDelete(confirming.id);
            finish();
          }}
        />
      )}
    </>
  );
}

function DeleteReportDialog({ report, onCancel, onConfirm }) {
  const dialogRef = useRef(null);
  const cancelRef = useRef(null);

  useEffect(() => {
    cancelRef.current?.focus();
  }, []);

  function onKeyDown(e) {
    if (e.key === 'Escape') {
      e.preventDefault();
      onCancel();
      return;
    }
    if (e.key !== 'Tab') return;
    const items = dialogRef.current.querySelectorAll(FOCUSABLE);
    const first = items[0];
    const last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  return (
    <div className="backdrop">
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-title"
        aria-describedby="delete-desc"
        className="dialog"
        onKeyDown={onKeyDown}
      >
        <header className="dialog__header">
          <h2 id="delete-title">Delete this report?</h2>
          <button type="button" className="dialog__close" aria-label="Close dialog" onClick={onCancel}>
            <svg aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 16 16">
              <path d="M3 3l10 10M13 3L3 13" stroke="currentColor" strokeWidth="2" />
            </svg>
          </button>
        </header>
        <p id="delete-desc">
          “{report.title}” will be removed from every dashboard that uses it. This cannot be undone.
        </p>
        <footer className="dialog__footer">
          <button type="button" ref={cancelRef} onClick={onCancel}>
            Cancel
          </button>
          <button type="button" className="danger" onClick={onConfirm}>
            Delete
          </button>
        </footer>
      </div>
    </div>
  );
}
```

## CSS

```css
.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(20, 24, 31, 0.55);
  display: grid;
  place-items: center;
}
.dialog {
  background: #fff;
  color: #14181f;
  width: min(28rem, 90vw);
  padding: 1.25rem;
  border-radius: 0.5rem;
}
.dialog__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.dialog__close {
  width: 2rem;
  height: 2rem;
  background: none;
  border: 0;
  color: inherit;
}
.dialog__footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
button:focus-visible {
  outline: 3px solid #1a4fd1;
  outline-offset: 2px;
}
.danger {
  background: #b3261e;
  color: #fff;
}
```

## Keyboard Test Recipe

```js
// tests/dialog-dismiss.spec.js
const { test, expect } = require('@playwright/test');

const BASE_URL = process.env.BASE_URL;
if (!BASE_URL || !/^https?:\/\/.+/.test(BASE_URL)) {
  throw new Error('Keyboard tests require a real site. Set BASE_URL.');
}

test('delete-report dialog: close control is reachable by Tab and dismisses on Enter', async ({ page }) => {
  await page.goto(`${BASE_URL}/reports`);

  const trigger = page.getByRole('button', { name: 'Delete report' });
  await trigger.focus();
  await page.keyboard.press('Enter');

  const dialog = page.getByRole('dialog');
  await expect(dialog).toBeVisible();
  await expect(dialog).toHaveAccessibleName('Delete this report?');
  await expect(dialog.locator('p:has-text("cannot be undone")')).toBeVisible();
  await expect(dialog.getByRole('button', { name: 'Cancel' })).toBeFocused();

  // Close control under test — name taken from the census row for the header control.
  const close = dialog.getByRole('button', { name: 'Close dialog', exact: true });

  // Three focusable controls in the dialog; six presses is two full cycles.
  let reached = false;
  for (let i = 0; i < 6 && !reached; i++) {
    await page.keyboard.press('Tab');
    await page.waitForTimeout(100);
    reached = await close.evaluate((el) => el === document.activeElement);
  }
  await expect(close, '2.1.1 Keyboard: the dialog close control must be reachable by Tab').toBeFocused({ timeout: 500 });

  await page.keyboard.press('Enter');
  await expect(dialog).toBeHidden();
  await expect(trigger).toBeFocused();
});
```

## Run Output

`stdout`:

```
$ BASE_URL=http://localhost:3000 npx playwright test tests/dialog-dismiss.spec.js
Running 1 test using 1 worker

  ✓  1 tests/dialog-dismiss.spec.js:9:1 › delete-report dialog: close control is reachable by Tab and dismisses on Enter (1.6s)

  1 passed (2.3s)
```

`trace.json` (per keystroke: the element focused after the key, from the browser's accessibility tree):

```json
[
  { "step": 0, "keystroke": "Enter", "target": { "role": "button", "name": "Delete report" }, "focus_after": { "role": "button", "name": "Cancel" }, "focus_moved": true },
  { "step": 1, "keystroke": "Tab", "focus_after": { "role": "button", "name": "Delete" }, "focus_moved": true },
  { "step": 2, "keystroke": "Tab", "focus_after": { "role": "button", "name": "Close dialog" }, "focus_moved": true },
  { "step": 3, "keystroke": "Enter", "target": { "role": "button", "name": "Close dialog" }, "focus_after": { "role": "button", "name": "Delete report" }, "focus_moved": true, "dialog_open_after": false }
]
```

`screen-reader-census.json` (reading order of the dialog subtree while it is open):

```json
[
  { "role": "dialog", "name": "Delete this report?", "selector": "div.dialog" },
  { "role": "button", "name": "Close dialog", "selector": "div.dialog > header > button" },
  { "role": "heading", "level": 2, "name": "Delete this report?", "selector": "#delete-title" },
  { "role": "paragraph", "name": "“Q3 spend by region” will be removed from every dashboard that uses it. This cannot be undone.", "selector": "#delete-desc" },
  { "role": "button", "name": "Cancel", "selector": "div.dialog > footer > button:nth-of-type(1)" },
  { "role": "button", "name": "Delete", "selector": "div.dialog > footer > button:nth-of-type(2)" }
]
```

`findings.json` (filed by the harness from the assertions that ran):

```json
[
  {
    "finding_id": "kbd-dialog-close-reach",
    "wcag": "2.1.1",
    "outcome": "PASS",
    "selector": "getByRole('button', { name: 'Close dialog', exact: true })",
    "message": "close control focused on Tab press 2 of a 3-control cycle",
    "evidence": ["trace.json#step-2"],
    "source": "assertion:tests/dialog-dismiss.spec.js:32"
  },
  {
    "finding_id": "kbd-dialog-close-dismiss-focus-return",
    "wcag": "2.4.3",
    "outcome": "PASS",
    "selector": "getByRole('button', { name: 'Delete report' })",
    "message": "Enter on the close control hid the dialog and returned focus to the trigger",
    "evidence": ["trace.json#step-3"],
    "source": "assertion:tests/dialog-dismiss.spec.js:36"
  }
]
```

## Expected Behavior

- Activating **Delete report** opens a modal confirmation dialog; the rest of the page is made inert while it is open.
- Focus lands on **Cancel**, the least destructive action. Tab cycles through the dialog's three controls and wraps; Shift+Tab wraps the other way.
- The header close control, Escape, and **Cancel** all dismiss the dialog without deleting; **Delete** deletes and dismisses.
- On dismissal by any route, focus returns to the **Delete report** trigger.
- The recipe is meant to prove that the header close control is reachable by Tab and that Enter on it dismisses the dialog and returns focus to the trigger. Its recorded outcome is the two PASS rows in `findings.json`.

## Frameworks & Environment

- React 18.3 (function components, `inert` rendered as an attribute)
- Playwright 1.58, Chromium, real keyboard events via `page.keyboard.press`
- `trace.json` and `screen-reader-census.json` follow the a11y-test verification evidence contract (per-step keystroke and accessibility-tree focus target; reading-order census with role, name, selector)

## Accessibility Issues (None Planted — CLEAN Baseline)

None. This fixture is a CLEAN baseline with no planted defects, in the recipe or the component. Everything from this heading down is ground-truth material and is stripped from model prompts by the blind protocol (`ANSWER_KEY_RE` in the runners).

## Difficulty Level

**CLEAN** — Baseline for false-positive avoidance on a keyboard recipe whose selectors are derived from the accessible-name inventory. The correct decisions that read like defects to a reviewer looking for something to flag: `getByRole` with `exact: true` (not over-specification — it excludes substring matches on purpose), a `:has-text()` selector on a text-bearing paragraph (it resolves; text-content matching is exactly right for text content), an icon-only close button whose name is `aria-label`, an inert "Close account" button under the backdrop, and initial focus on Cancel rather than the heading.
