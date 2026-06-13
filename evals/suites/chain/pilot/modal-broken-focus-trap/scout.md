## Scout Recon: Subscribe Modal (Broken Focus Trap)

**Component type**: Modal dialog with form
**APG pattern match**: WAI-ARIA Dialog (Modal Dialog), but pattern NOT implemented
**Complexity**: Medium

**Files** (paths only):
- evals/suites/chain/targets/modal-broken-focus-trap/component.jsx
- evals/suites/chain/targets/modal-broken-focus-trap/styles.css

**Existing ARIA inventory**:
- aria-haspopup="dialog" (line 103, trigger button)
- aria-required="true" (line 51, 64, form inputs)
- id="modal-title" (line 31, heading, but never referenced)

**Existing semantic HTML**:
- <button> elements: 4 (trigger, close, cancel, submit) — all real buttons
- <nav> landmark: 1 (background nav, remains interactive)
- <main> landmark: 1 (page-main)
- Heading hierarchy: h1 (Newsletter) → h2 (Subscribe to Updates) — correct
- Form labels: all associated via htmlFor/id (2/2)

**Notable patterns**:
- Trigger ref captured (`triggerRef`) but focus NOT restored on modal close (line 91, comment: "Missing: triggerRef.current?.focus();")
- Modal container lacks role="dialog" attribute
- Modal NOT marked aria-modal="true"
- Modal title has id but NO aria-labelledby on dialog
- Background content (nav links) fully interactive while modal open — no inert/disabled state

**Flags for reviewer**:
- **Focus trap NOT implemented** — no role="dialog", no aria-modal, no focus containment logic, no focus restore on close
- **Background not inert** — page nav interactive behind modal; no aria-hidden or inert attribute on <main>
- **Dialog lacks accessible name** — id exists but no aria-labelledby wiring
- **Escape key handling missing** — no listener to close on Escape press
- Test fixture: intentionally broken to validate critic detection of focus management failures
