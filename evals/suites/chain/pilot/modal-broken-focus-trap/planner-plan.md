# Subscribe Modal Accessibility Design Plan

> **For Claude:** Use a11y-planner protocol. Review with a11y-critic after implementation.
> **Compliance target:** WCAG 2.2 AA
> **Users who need accessibility:** Screen reader users (NVDA, JAWS, VoiceOver), keyboard-only users, low-vision users, voice-control users, switch-access users, users with cognitive load sensitivity.
> **Assistive technologies:** NVDA + Firefox/Chrome, JAWS + Chrome, VoiceOver + Safari, keyboard-only (no AT), screen magnifier, Dragon NaturallySpeaking.

**Feature:** A "Subscribe Now" trigger that opens a modal dialog containing a newsletter sign-up form (name + email), with a success confirmation state.
**Risk Level:** High (modal dialog with focus trap, focus restoration, background inerting, multi-state form, and a state swap to a success view — every one of these is a high-frequency a11y failure point).
**Component Type:** Modal Dialog + Form + Status Message.

---

## Scope & Context

**What:** A two-button page (`Subscribe Now` trigger + background nav) that opens a modal dialog. The dialog holds a form with two required text inputs (name, email), a Cancel button, and a Subscribe submit button. On submit, the dialog content swaps in-place to a success confirmation with a close button.

**Why:** Newsletter capture. The modal interrupts the page to collect two fields, then confirms success. Because it is an interruption that takes over the viewport, it MUST behave as a modal dialog per the WAI-ARIA APG — focus contained, background inert, dismissible, and focus restored on close.

**Who needs accessibility:** All users. Specifically:
- **Screen reader users** — need the dialog announced as a dialog with a name on open, focus moved inside, the success state announced, and the close button named.
- **Keyboard-only users** — need focus to move into the dialog, stay trapped inside it, Escape to dismiss, and focus to return to the trigger.
- **Low-vision / magnifier users** — need the focus to physically move to the dialog (so the magnified viewport follows it), and need the dialog to reflow at 400% zoom.
- **Voice-control users** — need every control to have a spoken-name target ("click Close", "click Subscribe").
- **Cognitive** — need a clear, specific success confirmation and clear error recovery.

**Compliance target:** WCAG 2.2 AA.

**Risk level:** High. Justification:
- Modal dialog with focus trap = the single most common high-severity a11y defect class.
- The component swaps the dialog body to a success view on submit (`component.jsx:14-23`) — a dynamic content change that needs a live announcement.
- `noValidate` (`component.jsx:40`) disables native validation with no replacement — empty submissions silently "succeed."

**What this modifies / extends (current state, with evidence):**

This is a redesign of an existing broken implementation. Current accessibility state:

| Current behavior | Evidence (file:line) | Problem |
|---|---|---|
| Trigger ref captured but focus never restored | `component.jsx:86-92` (explicit comment: `// Missing: triggerRef.current?.focus();`) | Focus is lost to `<body>` on close. WCAG 2.4.3. |
| Modal container is a plain `<div>` | `component.jsx:27` | No `role="dialog"`, no `aria-modal`, no name. Not announced as a dialog. WCAG 4.1.2. |
| Heading has `id="modal-title"` but it is never referenced | `component.jsx:30-31` | Dialog has no accessible name. WCAG 4.1.2. |
| Background `<main>` + `<nav>` stay interactive | `component.jsx:95-116` | Keyboard and screen-reader users can leave the modal and operate the page behind it. WCAG 2.4.3, 1.3.1. |
| No Escape key handling | (absent in `component.jsx`) | Standard dismiss affordance missing. APG Modal Dialog. |
| Focus never moves INTO the modal on open | (absent — `isOpen` toggles at `component.jsx:102`, nothing moves focus) | Screen reader / magnifier users are not taken to the dialog. WCAG 2.4.3. **(Not in scout recon — found on source read.)** |
| Close button label is the `×` character | `component.jsx:19`, `component.jsx:32-37` | `×` (U+00D7) announces as "times" or is skipped. No accessible name. WCAG 4.1.2, 1.1.1. **(Not in scout recon.)** |
| Success state is a second nameless dialog with no announcement | `component.jsx:14-23` | Submission success is silent to screen readers; the new dialog has no name/heading/role. WCAG 4.1.3, 4.1.2. **(Not in scout recon.)** |
| `noValidate` with no custom validation | `component.jsx:40` | Empty / malformed submits silently succeed. No error identification. WCAG 3.3.1. **(Not in scout recon.)** |

**Constraints:**
- React function components with `useState` / `useRef` / `useEffect` (already imported, `component.jsx:1`). No third-party modal library is in use — focus management must be authored or a vetted library (`react-focus-lock`, `focus-trap-react`, Radix `Dialog`) adopted. This plan specifies the behavior; the implementation may satisfy it with a library, but the acceptance criteria below are library-agnostic.
- Existing focus styles are a single `3px solid #1565c0` outline (`styles.css:19-22, 68-71, 93-97, 117-119, 133-136, 156-159`). See Visual Accessibility Plan for the contrast caveat.
- No design-system tokens present; colors are hardcoded hex.

**What this plan does NOT cover (negative space):**
- The newsletter backend / network submission. `handleSubmit` (`component.jsx:9-12`) is a stub that sets local state. Loading/error states from a real async request are designed here as states to communicate, but the network layer itself is out of scope.
- The background page's own structure beyond what is needed to inert it. The `<h1>`/`<p>`/`<nav>` are correct as-is (`component.jsx:95-113`).
- Cookie/consent UX, double opt-in email flows, and anti-spam — product concerns, not a11y.

---

## Semantic Structure Plan

### Landmarks
- `<main className="page-main">` — primary landmark (exists, `component.jsx:95`). Keep.
- `<nav className="background-nav">` — navigation landmark (exists, `component.jsx:109`). Keep, but it MUST become inert while the modal is open (see Focus Management).
- The dialog itself is NOT a landmark. It is a `role="dialog"` region rendered into the DOM. WCAG 1.3.1.

### Heading hierarchy
- `<h1>Newsletter</h1>` (`component.jsx:96`) — page title. Keep.
- `<h2 id="modal-title">Subscribe to Updates</h2>` (`component.jsx:31`) — dialog title. Keep, and wire it as the dialog's accessible name.
- **Success state needs a heading.** Currently the success message is a bare `<p>` (`component.jsx:18`). Add an `<h2>` so the success dialog has a title and a name. The dialog's name must update to point at the success heading when the view swaps. WCAG 1.3.1, 2.4.6.

This yields `h1 → h2` with no skips, whether the dialog shows the form or the success view.

### Document outline / DOM placement
- The dialog markup currently renders as a child of `<main>` (`component.jsx:115`). This is acceptable for a React-rendered modal as long as the background is inerted. A portal to `document.body` is an alternative; if a portal is used, the inert target becomes the page-root wrapper, not `<main>`. **Document the choice** — it changes which element receives `inert`.

### Form structure
- The two inputs are each in a `.form-group` with an associated `<label htmlFor>` (`component.jsx:43-66`). Labels are correct — keep them.
- Wrap the two inputs in a `<fieldset>` with a `<legend>` ONLY if a shared group label adds meaning. For two fields under a dialog already titled "Subscribe to Updates," a fieldset is unnecessary and adds verbosity. **Decision: no fieldset.** WCAG 1.3.1 is already satisfied by the dialog title + per-field labels.

### Skip navigation
- Not applicable at the component level. A modal does not need a skip link; the focus trap is the bypass mechanism. WCAG 2.4.1 is satisfied at the page level (out of scope here).

### HTML structure stub (structure + ARIA only — NOT implementation code)

Form state:
```
<main class="page-main">           <!-- inert when modal open -->
  <h1>Newsletter</h1>
  <p>…</p>
  <button class="btn-open" aria-haspopup="dialog">Subscribe Now</button>
  <nav class="background-nav"> … </nav>   <!-- inert when modal open -->
</main>

<!-- rendered when isOpen; sibling of (or portal out of) page-main -->
<div class="modal-backdrop">           <!-- visual only, presentational -->
  <div
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-title"
  >
    <div class="modal-header">
      <h2 id="modal-title">Subscribe to Updates</h2>
      <button class="modal-close" aria-label="Close subscribe dialog">
        <span aria-hidden="true">×</span>
      </button>
    </div>

    <form novalidate>
      <!-- error summary slot: rendered only when errors exist -->
      <div role="alert" id="form-errors"> … </div>   <!-- conditional -->

      <div class="form-group">
        <label for="modal-name">Your name</label>
        <input id="modal-name" type="text"
               required aria-required="true"
               aria-invalid="false"
               aria-describedby="modal-name-error" />   <!-- describedby only when invalid -->
        <span id="modal-name-error" class="field-error"> … </span>  <!-- conditional -->
      </div>

      <div class="form-group">
        <label for="modal-email">Email address</label>
        <input id="modal-email" type="email"
               required aria-required="true"
               aria-invalid="false"
               aria-describedby="modal-email-error" />
        <span id="modal-email-error" class="field-error"> … </span>  <!-- conditional -->
      </div>

      <div class="modal-actions">
        <button type="button" class="btn-secondary">Cancel</button>
        <button type="submit" class="btn-primary">Subscribe</button>
      </div>
    </form>
  </div>
</div>
```

Success state (same dialog node, swapped body):
```
<div class="modal-backdrop">
  <div
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-success-title"
  >
    <h2 id="modal-success-title" class="modal-success-title">You're subscribed</h2>
    <p class="modal-success">Thanks, {name}! Check your inbox to confirm.</p>
    <button class="modal-close" aria-label="Close dialog">
      <span aria-hidden="true">×</span>
    </button>
  </div>
</div>
```

Note: `aria-labelledby` switches from `modal-title` to `modal-success-title` when the view swaps, so the dialog always has a correct name. WCAG 4.1.2.

---

## Interaction Pattern Design

**Governing pattern:** WAI-ARIA APG — Dialog (Modal) Pattern: <https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/>

The form fields follow native HTML semantics (no APG widget pattern needed — native `<input>` and `<button>` are correct, `component.jsx:45-75`).

### Interactive Elements Table

| Widget | APG Pattern | Keyboard | ARIA | WCAG |
|--------|-------------|----------|------|------|
| `Subscribe Now` trigger | Native button + dialog opener (APG Dialog "opening" guidance) | `Enter` / `Space` opens dialog | `aria-haspopup="dialog"` (exists, `component.jsx:103`) | 2.1.1, 4.1.2 |
| Dialog container | [APG Dialog (Modal)](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) | `Esc` closes; `Tab`/`Shift+Tab` cycle within | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` | 2.1.1, 2.1.2, 2.4.3, 4.1.2 |
| Close (`×`) button | Native button | `Enter` / `Space` closes | `aria-label="Close…"`; inner `×` is `aria-hidden` | 2.1.1, 1.1.1, 4.1.2 |
| Name input | Native text input | Standard text editing | `aria-required`, `aria-invalid`, `aria-describedby` (when invalid) | 1.3.1, 3.3.1, 4.1.2 |
| Email input | Native email input | Standard text editing | `aria-required`, `aria-invalid`, `aria-describedby` (when invalid) | 1.3.1, 3.3.1, 4.1.2 |
| Cancel button | Native button | `Enter` / `Space` closes | none beyond name | 2.1.1, 4.1.2 |
| Subscribe (submit) button | Native button | `Enter` / `Space` submits; `Enter` in a field also submits | `aria-busy` on form during async submit (if real network added) | 2.1.1, 4.1.3 |

### Keyboard interaction model (Dialog)

Per APG Dialog (Modal):
- **On open:** move focus into the dialog. Target = the first interactive element (the name input) OR the dialog container itself if you want the title read first. **Decision: focus the first input (`#modal-name`).** Rationale: a two-field form's purpose is to be filled; the dialog title is read as the dialog's accessible name when focus enters, so the user still hears "Subscribe to Updates, dialog." Do NOT auto-focus the Close button (a destructive-looking first target). WCAG 2.4.3.
- **`Tab`** from the last interactive element (Subscribe) wraps to the first (Close, or name input — must match DOM order; see Focus Management). **`Shift+Tab`** from the first wraps to the last. WCAG 2.1.2 (No Keyboard Trap is satisfied because Escape always provides an exit — the trap is intentional and escapable).
- **`Esc`** closes the dialog and restores focus to the trigger. Must work from any field, including while an input has focus. WCAG 2.1.2, 2.4.3.
- **`Enter`** inside a text input submits the form (native behavior; do not suppress it). The submit handler must run validation first.

### Screen reader experience (intended)
- **On trigger focus:** "Subscribe Now, button, has pop-up dialog."
- **On open:** focus lands on name input; AT announces "Subscribe to Updates, dialog" (from `aria-labelledby` + `role`/`aria-modal`) then "Your name, edit, required."
- **On invalid submit:** the error summary (`role="alert"`) is announced immediately, e.g. "2 errors. Your name is required. Email address is required." Then on focusing a field: "Your name, edit, required, invalid, Your name is required."
- **On success:** the dialog body swaps; the success state is announced (see State Communication — this is the critical fix). Then "You're subscribed, dialog" with the success text.
- **On close:** focus returns to "Subscribe Now, button" — the user is oriented back where they started. WCAG 2.4.3.

---

## Focus Management Plan

This is the heart of the fix. Five distinct behaviors, each currently missing.

### 1. Logical tab order (inside the open dialog)
1. Close button (`×`) — `component.jsx:32`
2. Name input — `component.jsx:45`
3. Email input — `component.jsx:58`
4. Cancel button — `component.jsx:70`
5. Subscribe button — `component.jsx:73`

This matches DOM order and visual top-to-bottom order. WCAG 2.4.3, 1.3.2. No `tabindex` reordering needed.

### 2. Focus move INTO the dialog on open (currently missing entirely)
- On `isOpen` transition to `true`, move focus to `#modal-name`.
- Implement with a `ref` on the name input and `useEffect(() => inputRef.current?.focus(), [])` in the modal component (the modal only mounts when open, so a mount effect is correct). Use `focus({ preventScroll: false })` so a magnified viewport follows the focus into the dialog. WCAG 2.4.3.
- **Branch coverage:** this applies to the FORM state on mount. The success state is reached by an in-place swap, not a remount — see behavior #5.

### 3. Focus trap (containment) — currently missing
- While the dialog is open, `Tab` and `Shift+Tab` must cycle only among the dialog's interactive elements. Two acceptable implementations:
  - **Preferred:** adopt a vetted, maintained library (`focus-trap-react`, `react-focus-lock`, or Radix `Dialog`) rather than hand-rolling. Hand-rolled traps routinely miss radio groups, dynamically inserted nodes, and shadow DOM. Per `CLAUDE.md` research rule: prefer battle-tested libraries.
  - **If hand-rolled:** query focusable descendants on each `Tab`, detect first/last, and wrap. Recompute the focusable set after each render (the error summary and field-error nodes appear/disappear, changing the set). Do NOT cache the focusable list once at open.
- The trap MUST be escapable via Escape (so it is not a WCAG 2.1.2 keyboard trap). WCAG 2.1.2, APG Modal Dialog.

### 4. Background inerting (currently missing)
- While the dialog is open, the background (`<main>` and its `<nav>`, `component.jsx:95-116`) MUST be non-interactive AND hidden from the accessibility tree.
- **`aria-hidden="true"` alone is NOT sufficient** — it hides from AT but does not remove elements from the tab order. The three nav links (`component.jsx:110-112`) would still be reachable by `Tab`.
- **Strategy decision:** apply the `inert` attribute to the background container. `inert` removes descendants from the tab order AND from the a11y tree in supporting browsers (broadly supported as of 2026). Belt-and-suspenders: pair with `aria-hidden="true"` for any legacy AT that lags on `inert`.
  - If the dialog is rendered as a sibling of `<main>` (current structure, `component.jsx:115`): apply `inert` to `<main>` only.
  - If the dialog is portaled to `body`: wrap the rest of the page in a single root element and apply `inert` to that root, NOT to the dialog's own wrapper.
  - **Do not apply `inert` to an ancestor that also contains the dialog** — that would inert the dialog itself (catch-22). Document which element gets `inert` in the implementation.
- WCAG 2.4.3 (Focus Order), 1.3.1, 4.1.2.

### 5. Focus on the success-state swap (currently missing announcement AND focus handling)
- When `submitted` flips true (`component.jsx:11`), the dialog body swaps from form to success message. The form's focused element (Subscribe button) is unmounted.
- **Plan:** move focus to the success dialog's close button after the swap, OR to the success heading (`#modal-success-title` with `tabindex="-1"`). **Decision: focus the success heading** (`tabindex="-1"`, `focus()` in a mount/update effect keyed on `submitted`). Rationale: the heading is the success message's anchor; focusing it both moves the magnified viewport to the confirmation and gives screen-reader users the heading text. The close button remains the next `Tab` stop. WCAG 2.4.3.
- This focus move is in ADDITION to the live-region announcement (State Communication) — focus move alone is not a reliable announcement across all AT, and the announcement alone does not reposition the magnifier. Both are required.
- **Timing:** because this is a React re-render (state swap, not remount), defer the `focus()` with a `useEffect` keyed on `submitted`; if timing is flaky, wrap in a `setTimeout(…, 0)` to run after paint. WCAG 2.4.3.

### 6. Focus restoration on close (currently missing — `component.jsx:88-92`)
- On close — via Close button, Cancel button, Escape, OR success-state close — restore focus to the trigger (`triggerRef`, already captured at `component.jsx:100`).
- The `handleClose` stub (`component.jsx:89-92`) already has the exact line commented out: add `triggerRef.current?.focus();`.
- **Branch coverage — ALL of these close paths must restore focus:**
  - Close `×` button (form state) — `component.jsx:34`
  - Cancel button — `component.jsx:70`
  - Escape key (new handler)
  - Close `×` button (success state) — `component.jsx:19`
  - (If added) click on backdrop to dismiss
- Restoring focus to the trigger is the APG Modal Dialog standard, and it is correct here: the trigger is a persistent, meaningful return point. WCAG 2.4.3.

### 7. Focus indicator visibility
- Focus indicators exist on all controls (`styles.css:19, 68, 93, 117, 133, 156`). See the Visual Accessibility Plan for the single-color contrast caveat and the fix. WCAG 2.4.7.

### 8. Roving tabindex
- Not applicable. There is no composite widget (no tabs, listbox, menu, or radio group). All controls are independently tabbable. Native focus order is correct.

---

## State Communication Design

### State Communication Table

| State | Visual | Programmatic | ARIA | WCAG |
|-------|--------|--------------|------|------|
| Dialog closed | Backdrop absent | Dialog node not in DOM | — | — |
| Dialog open | Backdrop dims page (`styles.css:25-33`) | `role="dialog"` + `aria-modal="true"` present; background `inert` | `role`, `aria-modal`, `aria-labelledby` | 4.1.2, 1.3.1 |
| Field required | `font-weight:600` label (`styles.css:77-82`); add a visible "required" cue (text or `*` with legend) | `required` + `aria-required="true"` (exist, `component.jsx:51,64`) | `aria-required` | 1.3.1, 3.3.2 |
| Field valid | Default border `#ccc` (`styles.css:87`) | `aria-invalid="false"` | `aria-invalid` | 4.1.2 |
| Field invalid | Red border + error icon + error text below field (color is NOT the only cue) | `aria-invalid="true"` + `aria-describedby` → error id | `aria-invalid`, `aria-describedby` | 1.4.1, 3.3.1, 1.3.1, 4.1.2 |
| Form has errors (on submit) | Error summary block at top of form, visible, with list of errors | `role="alert"` container announces immediately | `role="alert"` (≡ `aria-live="assertive"`) | 4.1.3, 3.3.1 |
| Submitting (if real async) | Subscribe button shows spinner/disabled look | `aria-busy="true"` on form; submit button `aria-disabled` | `aria-busy` | 4.1.3 |
| Submit succeeded | Body swaps to success heading + message (green text, `styles.css:138-143`) | Announced via live region; focus moved to success heading | `role="status"` on success region OR `aria-live="polite"`; `aria-labelledby` points to success heading | 4.1.3, 4.1.2 |

### The `×` close button symbol (currently a bare character — `component.jsx:19, 37`)
- The `×` (U+00D7 multiplication sign) is announced by screen readers as "times" or dropped. It is a decorative glyph standing in for "close."
- **Plan:** wrap the glyph in `<span aria-hidden="true">×</span>` and put the real name on the button via `aria-label="Close subscribe dialog"` (form state) / `aria-label="Close dialog"` (success state). Per planner hard gate: use `aria-label`, NEVER `title`. WCAG 4.1.2, 1.1.1.

### The success announcement (THE critical missing state — `component.jsx:14-23`)
- Currently: the body swaps to `<p>Thanks, {name}! You're subscribed.</p>` with no role, no live region, no focus move. A screen reader user gets silence. They filled a form and have no idea it worked.
- **Plan — two mechanisms, both required:**
  1. Render the success region with `role="status"` (polite live region) so AT announces the confirmation text when it appears. `role="status"` is correct (not `alert`) because success is not an error/urgent. WCAG 4.1.3.
  2. Move focus to the success heading (`#modal-success-title`, `tabindex="-1"`) per Focus Management #5, so magnifier users are repositioned and the heading is read.
- **Live-region placement rule (planner pitfall #1):** the success `role="status"` region exists exactly once (the success view renders one dialog). It is NOT inside a loop. Safe. The error summary `role="alert"` likewise renders once at the top of the form — NOT per field. Per-field feedback uses `aria-describedby` + `aria-invalid`, never a per-field live region.

### Validation & error identification (currently absent — `noValidate` at `component.jsx:40`)
- `noValidate` (`component.jsx:40`) disables the browser's native validation bubbles. Nothing replaces it, so `handleSubmit` (`component.jsx:9-12`) sets `submitted=true` regardless of input — an empty form "succeeds."
- **Plan:** on submit, validate both fields BEFORE setting `submitted`:
  - Name: non-empty after trim.
  - Email: non-empty AND matches a basic email shape (or rely on `type="email"` + a JS check; do not over-engineer the regex).
  - If invalid:
    - Set `aria-invalid="true"` on each failing field. WCAG 4.1.2.
    - Render a per-field error `<span id="…-error">` with a SPECIFIC, fix-oriented message ("Email address is required" / "Enter an email address like name@example.com"), associated via `aria-describedby`. WCAG 3.3.1, 3.3.3, 1.3.1.
    - Render the error-summary `role="alert"` block at the top of the form listing the errors, and move focus to it (or to the summary's first link). WCAG 3.3.1, 4.1.3.
    - Do NOT set `submitted`.
  - Keep `noValidate` (so native bubbles don't double up with custom messages) — but ONLY because custom validation now fully replaces it. WCAG 3.3.1.

### Backdrop semantics (`styles.css:25-33`)
- The dimming backdrop is purely visual ("modal open" for sighted users). The programmatic equivalent — that everything behind is unavailable — is carried by `inert` + `aria-modal="true"`, not by the backdrop. The backdrop `<div>` is presentational; it needs no role. (If click-to-dismiss is added, the backdrop gets an `onClick` but remains non-focusable; the keyboard equivalent is Escape, which already covers WCAG 2.1.1.)

---

## Visual Accessibility Plan

### Color contrast (WCAG 1.4.3, 1.4.11)
- Body/title text `#1a1a1a` on `#fff` (`styles.css:55, 110-112`): ~16.9:1. Pass.
- Primary buttons: white on `#1565c0` (`styles.css:9-11, 122-127`): ~5.0:1. Pass for normal text.
- Success text `#2e7d32` on `#fff` (`styles.css:139`): ~4.8:1. Pass (normal text ≥ 4.5:1). Do NOT lighten it.
- Close `×` `#424242` on `#fff` (`styles.css:62`): ~9:1. Pass.
- **Input border `#ccc` on `#fff` (`styles.css:87`): ~1.6:1 — FAILS the 3:1 non-text contrast requirement for the input boundary.** WCAG 1.4.11. The form border must be darkened (e.g. `#767676` gives ~4.5:1) so low-vision users can perceive the field edges.

### Focus indicator — the single-color caveat (WCAG 2.4.7)
- Every focus style is `outline: 3px solid #1565c0` (`styles.css:19-22, 68-71, 93-97, 117-119, 133-136, 156-159`).
- On the **primary buttons**, whose background IS `#1565c0` (`styles.css:9, 122`), a `#1565c0` outline is nearly invisible against the button's own blue — the focus ring blends into the control.
- **Plan:** use a two-color (double-ring) focus indicator — a dark outline plus a light `box-shadow` offset (or invert on dark controls). Example approach (CSS, not implementation code): `outline: 3px solid #1565c0; box-shadow: 0 0 0 6px #fff;` so there is always a contrasting ring regardless of the element's own color. Switch the trigger to `:focus-visible` to avoid showing the ring on mouse click. WCAG 2.4.7, 2.4.11 (Focus Appearance).

### Color is never the sole indicator (WCAG 1.4.1)
| Element | Color cue | Required non-color cue |
|---|---|---|
| Required field | (none currently) | Add visible text "(required)" or `*` with a legend explaining it |
| Invalid field | Red border | + error icon + error message text below the field |
| Success | Green text | + heading "You're subscribed" + checkmark icon (icon `aria-hidden`) |
| Primary vs secondary button | Blue vs grey | Different labels ("Subscribe" / "Cancel") already distinguish them — OK |

Nav links (`styles.css:151-154`) are already underlined — link-in-content distinction satisfied. WCAG 1.4.1.

### Font sizing & reflow (WCAG 1.4.4, 1.4.10)
- Fonts are fixed `px` (`styles.css:9, 51, 57, 81, 89, 122, 139`). For AA, the page must still reflow and zoom to 200%/400%. The modal `max-width: 440px` + `width: 100%` (`styles.css:39-40`) reflows acceptably. **Recommend** (not strictly required for AA) migrating to `rem` so the modal scales with user font preferences. At 400% zoom, verify the dialog does not exceed the viewport and that the action buttons (`styles.css:99-104`, `justify-content: flex-end`) wrap rather than overflow. WCAG 1.4.10.

### Touch targets (WCAG 2.5.8)
- Close button: `font-size:24px` + `padding:4px 8px` (`styles.css:57-66`) is roughly 32x28px — **below the 44×44 minimum.** Increase padding (or add a min-size) so the hit area reaches 44×44 CSS px. WCAG 2.5.8.
- Other buttons (`padding:10-12px`, `styles.css:9, 107, 123`) are close; verify computed height ≥ 44px or rely on the AA spacing exception only if spacing genuinely qualifies.

### Motion (WCAG 2.3.3)
- No animations are defined currently. If an open/close transition is added, gate it behind `@media (prefers-reduced-motion: reduce)` and disable it. WCAG 2.3.3.

### Dark mode
- No `prefers-color-scheme` support and none required for AA. If added later, re-verify all contrast ratios in dark mode. Out of scope.

---

## Content Accessibility Plan

- **Close button name (WCAG 1.1.1, 4.1.2):** `aria-label="Close subscribe dialog"` (form) / `"Close dialog"` (success). The `×` glyph is `aria-hidden`. No `title`.
- **Link text (WCAG 2.4.4):** nav links "Home / About / Contact" (`component.jsx:110-112`) are descriptive. OK. (They are inerted while the modal is open.)
- **Form labels (WCAG 1.3.1):** both inputs have visible `<label>` + `htmlFor` (`component.jsx:44, 57`). Keep BOTH the visible label AND any programmatic association — do not replace the visible label with `aria-label` (planner pitfall #3).
- **Error message clarity (WCAG 3.3.1, 3.3.3):** specific and fix-oriented — "Email address is required," "Enter an email address like name@example.com." Not "Invalid input."
- **Form instructions (WCAG 3.3.2):** indicate required fields with a visible convention (text or `*` + legend), associated where a per-field instruction is needed (`aria-describedby`).
- **Success message (WCAG 1.3.1):** "Thanks, {name}! Check your inbox to confirm." — confirms the action and tells the user what happens next. Keep it specific.
- **Language (WCAG 3.1.1):** `<html lang>` is a page-level concern, out of scope for this component.
- **Reading order (WCAG 1.3.2):** DOM order = visual order in both states (verified against `component.jsx:29-78` and the stub above). No CSS reordering.

---

## Testing Strategy

### Automated (axe-core via a11y-test / `npx playwright test`)
Run axe-core on **every state variant**: closed, open (form), open with validation errors, open (success). axe-core will catch:
- Missing `role`/name on the dialog, missing input labels, color-contrast on the input border (`styles.css:87`), `aria-*` misuse.
axe-core will NOT catch (must be manual): focus moving into the dialog, focus trap, Escape handling, focus restoration, the success live-region announcement, background inerting reachability.

### Manual keyboard testing (a11y-test / real key events via Playwright `page.keyboard.press()` or agent-browser CDP)
- [ ] `Tab` to trigger, `Enter`/`Space` opens dialog.
- [ ] On open, focus is on `#modal-name` (not lost to body).
- [ ] `Tab` through Close → name → email → Cancel → Subscribe → wraps to Close.
- [ ] `Shift+Tab` from Close wraps to Subscribe.
- [ ] While dialog open, `Tab` NEVER reaches the nav links or trigger (background inert).
- [ ] `Esc` closes from any field and from a button.
- [ ] After close (each path: ×, Cancel, Esc, success-×), focus is back on the trigger.
- [ ] Submit empty form → focus moves to error summary; nothing "succeeds."
- [ ] Submit valid form → focus moves to success heading.
- [ ] Focus ring is visible on the blue primary buttons (double-ring fix).

### Screen reader testing (NVDA+Firefox, JAWS+Chrome, VoiceOver+Safari — at least two)
- [ ] On open: "Subscribe to Updates, dialog" announced; then "Your name, edit, required."
- [ ] Invalid submit: error summary announced via `role="alert"`; focusing a bad field announces "invalid" + the specific message.
- [ ] Success: confirmation announced via `role="status"`; success heading read.
- [ ] Close button announces "Close subscribe dialog, button" — NOT "times."
- [ ] Background nav links are not reachable by the virtual cursor while the dialog is open.

### Visual regression
- [ ] Focus rings visible at default and 200% zoom on all controls, especially primary buttons.
- [ ] 400% zoom: dialog fits viewport, action buttons wrap, no horizontal scroll. WCAG 1.4.10.
- [ ] Input borders visible (post-contrast fix).

### DOM verification (planner pitfall #9 — REQUIRED, not optional)
Inspect the rendered DOM (via Playwright `page.locator(...).getAttribute(...)` or agent-browser snapshot) to confirm:
- [ ] `aria-labelledby` on the dialog resolves to an element whose text is the visible title (and switches to the success heading id after submit).
- [ ] `aria-describedby` on each invalid input resolves to the visible error span.
- [ ] `role="alert"` / `role="status"` land on the summary / success region, exactly once each.
- [ ] `inert` is on the background container and NOT on the dialog or its ancestor-that-contains-the-dialog.
- [ ] `aria-label` is on the close `<button>`, and the `×` span carries `aria-hidden="true"`.

### Acceptance criteria (pass = all of):
1. Dialog announces as a named dialog on open; focus is inside it.
2. Focus is contained (trap) and escapable via Escape.
3. Background is unreachable (keyboard + AT) while open.
4. Focus returns to the trigger on every close path.
5. Success and validation-error states are announced AND move focus.
6. Close button has a real accessible name.
7. axe-core: zero violations on all four state variants.

---

## Implementation Tasks

### Task 1: Convert the container into a real modal dialog (role + name + open-focus)
🔍 **Review checkpoint**

**Files:** `evals/suites/chain/targets/modal-broken-focus-trap/component.jsx`

**Structure Stub:**
```
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <h2 id="modal-title">Subscribe to Updates</h2>
  …
```
Add `ref` to `#modal-name`; `useEffect` on mount focuses it.

**ARIA Attributes:**
- `role="dialog"` — WCAG 4.1.2 Name, Role, Value
- `aria-modal="true"` — WCAG 4.1.2 (signals modality to AT)
- `aria-labelledby="modal-title"` referencing existing `component.jsx:31` — WCAG 4.1.2
- (Trigger `aria-haspopup="dialog"` already present, `component.jsx:103`)

**Keyboard Interactions:** Enter/Space on trigger opens; on open, focus lands on name input.

**Tests:** Dialog has accessible name (DOM: `aria-labelledby` resolves); focus on `#modal-name` after open; axe-core clean on open state.

**WCAG Criteria:** 4.1.2, 2.4.3, 1.3.1.

**a11y-critic checkpoint 🔍:** Verify APG Modal Dialog name wiring; `aria-labelledby` resolves to visible title; focus enters the dialog (not body); `aria-modal` present.

---

### Task 2: Focus trap + Escape + background inerting
🔍 **Review checkpoint**

**Files:** `component.jsx` (and `styles.css` only if a wrapper is added)

**Structure Stub:** Adopt `focus-trap-react`/`react-focus-lock`/Radix `Dialog` around the dialog content, OR hand-roll Tab/Shift+Tab wrap. Apply `inert` (+ `aria-hidden="true"`) to `<main>` (or the page-root wrapper if portaled) while open. Add a `keydown` Escape listener that calls `onClose`.

**ARIA Attributes:**
- `inert` on background container — WCAG 2.4.3, 1.3.1, 4.1.2
- `aria-hidden="true"` on the same container (legacy AT fallback) — WCAG 4.1.2

**Keyboard Interactions:** Tab cycles within dialog; Shift+Tab wraps; Escape closes; background unreachable.

**Tests:** Tab never reaches nav links / trigger (DOM + keyboard); Shift+Tab from first wraps to last; Escape closes from a field; recompute focusable set after error nodes appear.

**WCAG Criteria:** 2.1.2, 2.4.3, 1.3.1, 4.1.2.

**a11y-critic checkpoint 🔍:** Confirm the trap is escapable (not a 2.1.2 keyboard trap); `inert` is on the correct element (NOT the dialog's ancestor-that-contains-it); background genuinely unreachable; focusable set recomputed after dynamic error insertion.

---

### Task 3: Focus restoration on every close path
🔍 **Review checkpoint**

**Files:** `component.jsx` (`handleClose`, `component.jsx:89-92`)

**Structure Stub:** In `handleClose`, add `triggerRef.current?.focus();` (the commented line at `component.jsx:91`). Ensure Close ×, Cancel, Escape, and success-× all route through `handleClose`.

**ARIA Attributes:** none new — this is behavior.

**Keyboard Interactions:** After each close path, focus is on the trigger.

**Tests:** Four close paths (×, Cancel, Escape, success-×) each return focus to the trigger (DOM `document.activeElement` === trigger).

**WCAG Criteria:** 2.4.3.

**a11y-critic checkpoint 🔍:** Verify ALL close branches restore focus (pitfall #4 — enumerate every branch); no path leaves focus on `<body>`.

---

### Task 4: Name the close button; hide the `×` glyph
🔍 **Review checkpoint**

**Files:** `component.jsx` (`component.jsx:19, 32-37`)

**Structure Stub:**
```
<button class="modal-close" aria-label="Close subscribe dialog">
  <span aria-hidden="true">×</span>
</button>
```
Apply to BOTH the form-state close (`component.jsx:32-37`) and the success-state close (`component.jsx:19`).

**ARIA Attributes:**
- `aria-label="Close…"` on the button — WCAG 4.1.2, 1.1.1 (NEVER `title`)
- `aria-hidden="true"` on the `×` span — WCAG 1.1.1

**Tests:** Screen reader announces "Close subscribe dialog, button," not "times" (DOM: button has `aria-label`; `×` span has `aria-hidden`).

**WCAG Criteria:** 4.1.2, 1.1.1.

**a11y-critic checkpoint 🔍:** Both close buttons named; `×` hidden from AT; `aria-label` (not `title`) used.

---

### Task 5: Validation, error identification, and error association
🔍 **Review checkpoint**

**Files:** `component.jsx` (`handleSubmit`, `component.jsx:9-12`; the two `.form-group`s, `component.jsx:43-66`)

**Structure Stub:** Add an error-summary `role="alert"` block (conditional, top of form) and per-field `<span id="…-error">` (conditional). On submit, validate; if invalid set `aria-invalid="true"` + `aria-describedby` and move focus to the summary; do NOT set `submitted`.

**ARIA Attributes:**
- `aria-invalid="true"|"false"` per input — WCAG 4.1.2
- `aria-describedby="…-error"` (only when invalid) — WCAG 1.3.1
- `role="alert"` on the summary (renders once, not per field) — WCAG 4.1.3, 3.3.1

**Keyboard Interactions:** Invalid submit moves focus to the summary; valid submit proceeds to success.

**Tests:** Empty submit does NOT set success; error summary announced (`role="alert"`); `aria-describedby` resolves to visible message (DOM); `aria-invalid` toggles correctly.

**WCAG Criteria:** 3.3.1, 3.3.3, 1.3.1, 4.1.2, 4.1.3.

**a11y-critic checkpoint 🔍:** `role="alert"` exists exactly once (NOT per-field — pitfall #1); per-field uses `aria-describedby` + `aria-invalid`; messages are specific and fix-oriented; `noValidate` is justified because custom validation fully replaces native.

---

### Task 6: Announce the success state + move focus to it
🔍 **Review checkpoint**

**Files:** `component.jsx` (`component.jsx:14-23`)

**Structure Stub:**
```
<div role="dialog" aria-modal="true" aria-labelledby="modal-success-title">
  <h2 id="modal-success-title" tabindex="-1">You're subscribed</h2>
  <p role="status" class="modal-success">Thanks, {name}! Check your inbox to confirm.</p>
  <button aria-label="Close dialog"><span aria-hidden="true">×</span></button>
```
`useEffect` keyed on `submitted` focuses `#modal-success-title`.

**ARIA Attributes:**
- `role="status"` on the confirmation (polite, renders once) — WCAG 4.1.3
- `aria-labelledby="modal-success-title"` on the dialog (name updates on swap) — WCAG 4.1.2
- `tabindex="-1"` on the success heading (programmatic focus target) — WCAG 2.4.3

**Keyboard Interactions:** On success, focus moves to the success heading; Tab continues to the close button.

**Tests:** Success announced (`role="status"`); focus on success heading after submit; dialog name switches to success title (DOM: `aria-labelledby` resolves to new id).

**WCAG Criteria:** 4.1.3, 4.1.2, 2.4.3.

**a11y-critic checkpoint 🔍:** Success is both announced (live region) AND focus-moved; `role="status"` (not `alert`) is correct for non-urgent success; dialog name updates on the swap; live region not duplicated/looped.

---

### Task 7: Visual fixes — input border contrast, focus ring on blue buttons, close-button target size
🔍 **Review checkpoint**

**Files:** `styles.css` (`:87` border; focus rules `:19, 68, 93, 117, 133, 156`; close-button sizing `:57-66`)

**Structure Stub (CSS targets, not implementation):**
- Darken input border from `#ccc` to ~`#767676` (`styles.css:87`).
- Add a contrasting second ring to focus styles (e.g. `box-shadow: 0 0 0 6px #fff;` alongside the existing outline) and switch to `:focus-visible`.
- Grow close-button hit area to ≥ 44×44 (`styles.css:57-66`).

**ARIA Attributes:** none — purely visual.

**Tests:** Input border ≥ 3:1 (axe-core / contrast tool); focus ring visible on `.btn-primary`/`.btn-open` (visual regression); close button ≥ 44×44 (computed box).

**WCAG Criteria:** 1.4.11, 2.4.7, 2.4.11, 2.5.8.

**a11y-critic checkpoint 🔍:** Border contrast passes 3:1; focus ring is visible against the blue button background (single-color caveat resolved); touch target meets 44×44.

---

## a11y-Critic Review Checkpoints

| Checkpoint | After Task | Focus |
|-----------|-----------|-------|
| 🔍 1 | Task 1 | Dialog role + name wiring; focus enters dialog; `aria-modal` present |
| 🔍 2 | Task 2 | Trap escapable (not 2.1.2 trap); `inert` on correct element; background unreachable; focusable set recomputed |
| 🔍 3 | Task 3 | ALL close branches restore focus to trigger (enumerate) |
| 🔍 4 | Task 4 | Both close buttons named via `aria-label` (not `title`); `×` hidden |
| 🔍 5 | Task 5 | One `role="alert"` (not per-field); `aria-describedby`+`aria-invalid` per field; specific messages |
| 🔍 6 | Task 6 | Success announced AND focus-moved; `role="status"` correct; name updates on swap |
| 🔍 7 | Task 7 | Input border 3:1; focus ring visible on blue buttons; 44×44 close target |
| 🔍 Final | All | Full APG Modal Dialog conformance; axe-core clean on 4 state variants; DOM verification of all aria-* placement |

---

### Contract Appendix (for spec-kitty-bridge WP translation)

### Architecture Overview
Convert a plain-`<div>` overlay (`component.jsx:27`) into a WAI-ARIA APG Modal Dialog. Semantic approach: `role="dialog"` + `aria-modal="true"` + `aria-labelledby` to the existing title (`component.jsx:31`), with a parallel success-state name. ARIA pattern choice: native HTML for form controls (already correct), APG Dialog for the container. Focus strategy: move focus in on open (to first input), trap focus inside (vetted library preferred over hand-roll), inert the background (`inert` + `aria-hidden` fallback), and restore focus to the captured trigger ref (`component.jsx:100`) on every close path. State communication: `role="alert"` error summary (once), per-field `aria-invalid`+`aria-describedby`, and a `role="status"` success region paired with a programmatic focus move to the success heading.

### Implementation Tasks

#### Task 1: Convert container into a real modal dialog
Estimated Effort: low (3 attribute additions on `component.jsx:27` + 1 focus effect; 1 component touched)
Depends on: none

#### Task 2: Focus trap + Escape + background inerting
Estimated Effort: medium (library adoption or hand-rolled trap + inert wiring + keydown listener; 1 component, possibly 1 wrapper element)
Depends on: Task 1

#### Task 3: Focus restoration on every close path
Estimated Effort: low (1 line in `handleClose` at `component.jsx:91` + route all 4 close paths through it; 1 component)
Depends on: Task 1, Task 2 (Escape path created in Task 2)

#### Task 4: Name the close button; hide the `×` glyph
Estimated Effort: low (2 buttons: `component.jsx:19` and `component.jsx:32-37`; 1 component)
Depends on: none

#### Task 5: Validation, error identification, and error association
Estimated Effort: medium (validation logic in `handleSubmit` `component.jsx:9-12` + 2 error spans + 1 summary + state; 1 component)
Depends on: Task 1

#### Task 6: Announce success + move focus to it
Estimated Effort: medium (restructure success view `component.jsx:14-23` + live region + focus effect + name switch; 1 component)
Depends on: Task 1, Task 3 (success-state close routes through restoration)

#### Task 7: Visual fixes (border contrast, focus ring, target size)
Estimated Effort: low (3 CSS edits in `styles.css`; 1 file)
Depends on: none

#### Test Strategy for Task 1
axe-core on open state; DOM check `aria-labelledby` resolves to visible title; keyboard check focus on `#modal-name` after open.

#### Test Strategy for Task 2
Keyboard: Tab never reaches nav/trigger; Shift+Tab wraps; Escape closes from a field. DOM: `inert` on background container, not on dialog ancestor. Verify focusable set recomputes after error nodes mount.

#### Test Strategy for Task 3
Four close paths (×, Cancel, Escape, success-×) each leave `document.activeElement` === trigger.

#### Test Strategy for Task 4
DOM: both close buttons have `aria-label`; `×` spans have `aria-hidden="true"`. SR: announces "Close…, button," not "times."

#### Test Strategy for Task 5
Empty submit does not set success; `role="alert"` summary present exactly once and announced; `aria-describedby` resolves to visible message; `aria-invalid` toggles per field.

#### Test Strategy for Task 6
`role="status"` present once and announced on success; `document.activeElement` === success heading after submit; dialog `aria-labelledby` resolves to the success title id.

#### Test Strategy for Task 7
Contrast tool: input border ≥ 3:1; visual regression: focus ring visible on `.btn-primary`/`.btn-open`; computed close-button box ≥ 44×44.

#### Acceptance Criteria for Task 1
Dialog exposes role `dialog`, is modal (`aria-modal="true"`), has an accessible name from the visible title, and focus is inside it on open. (WCAG 4.1.2, 2.4.3, 1.3.1)

#### Acceptance Criteria for Task 2
`Tab`/`Shift+Tab` cycle only within the dialog; Escape exits (no keyboard trap); background is unreachable by keyboard and AT. (WCAG 2.1.2, 2.4.3, 1.3.1, 4.1.2)

#### Acceptance Criteria for Task 3
Every close path returns focus to the trigger button. (WCAG 2.4.3)

#### Acceptance Criteria for Task 4
Both close buttons have a programmatic accessible name via `aria-label`; the `×` glyph is not announced. (WCAG 4.1.2, 1.1.1)

#### Acceptance Criteria for Task 5
Invalid submit is blocked, identifies each error specifically, associates each message with its field, and announces a single error summary; valid submit proceeds. (WCAG 3.3.1, 3.3.3, 1.3.1, 4.1.2, 4.1.3)

#### Acceptance Criteria for Task 6
Submission success is announced via a live region AND focus is moved to the success heading; the dialog name updates to the success title. (WCAG 4.1.3, 4.1.2, 2.4.3)

#### Acceptance Criteria for Task 7
Input border meets 3:1; focus indicator is visible on blue-background buttons; close-button target is ≥ 44×44 CSS px. (WCAG 1.4.11, 2.4.7, 2.4.11, 2.5.8)

### Failure Modes
- **Inert applied to the wrong element** — inerting an ancestor that also contains the dialog disables the dialog itself (catch-22). Inert only the background (`<main>` or page-root wrapper if portaled).
- **Focus trap not escapable** — a trap without an Escape exit becomes a WCAG 2.1.2 keyboard trap; Escape must always close.
- **Focusable set cached at open** — error spans and the summary mount dynamically; a stale focusable list lets Tab escape or skip nodes. Recompute per render.
- **Success swap leaves focus on a detached node** — the Subscribe button unmounts; without a focus move, focus falls to `<body>`. Move to the success heading.
- **Live region duplicated or looped** — `role="alert"`/`role="status"` placed inside a repeating template fires multiple/garbled announcements. Each renders exactly once.
- **`aria-label` regression to `title`** — `title` is a tooltip, not a reliable accessible name. Never use `title` for the close button.
- **Focus-restore missing on one branch** — Escape or success-close bypassing `handleClose` leaves focus orphaned. Route ALL close paths through the restore.
- **Single-color focus ring invisible on blue buttons** — the `#1565c0` outline vanishes on `#1565c0` button backgrounds; needs a second contrasting ring.
