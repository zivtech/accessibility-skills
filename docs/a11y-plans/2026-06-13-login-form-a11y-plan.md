# Login Form Accessibility Design Plan

> **For Claude:** Use a11y-planner protocol. Review with a11y-critic after implementation.
> **Compliance target:** WCAG 2.2 AA
> **Users who need accessibility:** Screen reader users (NVDA, JAWS, VoiceOver), keyboard-only users, low-vision/zoom users, cognitive (clear error recovery), voice-control users.
> **Assistive technologies:** NVDA + Firefox/Chrome, JAWS + Chrome, VoiceOver + Safari, keyboard-only, 400% browser zoom, Windows High Contrast / forced-colors, Dragon NaturallySpeaking (voice control).

**Feature:** An email + password sign-in form with a "Remember me" checkbox, client-side validation, an error summary, and per-field error messages.
**Risk Level:** Medium (form with validation, dynamic error injection, focus management, and live-region announcement — the validation/announcement path is where this class of component most often breaks, even when static markup looks clean).
**Component Type:** Form with validation (WAI-ARIA standard form pattern with error identification and announcement).

**Source under design:** `evals/suites/chain/targets/login-form-clean/component.jsx`, `evals/suites/chain/targets/login-form-clean/styles.css`

---

## Scope & Context

**What.** A login form: two text inputs (email, password), one checkbox (remember me), a submit button, two help links (forgot password, create account). On submit, client-side validation runs; if it fails, an error summary lists each error (linked to its field) and each invalid field gets an inline error message. `noValidate` disables native browser validation intentionally so the app owns the error UX.

**Why.** Sign-in is a gateway task. If it is inaccessible, the entire application behind it is inaccessible — there is no "skip this and continue." Error recovery is the high-risk moment: a user who cannot perceive that validation failed, cannot find which field is wrong, or cannot navigate to fix it is fully blocked.

**Who needs accessibility.** All users. Highest-stakes sub-groups for this component:
- **Screen reader users** — must hear that submission failed, how many errors, which fields, and the specific fix.
- **Keyboard-only users** — must be able to reach and fix the offending field without a mouse, including from the error summary.
- **Low-vision / zoom users** — must read errors at 400% zoom without horizontal scroll and distinguish invalid fields by more than color.
- **Cognitive** — must get specific, actionable error text and an obvious recovery path.

**Compliance target.** WCAG 2.2 Level AA.

**Risk level: Medium.** Static markup is largely correct (the baseline already has labels, `aria-required`, conditional `aria-describedby`/`aria-invalid`, a `role="alert"` summary, and AA-passing contrast). The risk lives entirely in the *dynamic* behavior: (a) does the error announcement fire on **every** failed submit, not just the first; (b) does focus move so a keyboard/SR user knows errors appeared; (c) do the error-summary links actually **move focus** to the field (not just scroll the viewport, which is unreliable in an SPA); (d) does a successful submit communicate progress. These are invisible in a static read and are exactly the gaps this planner exists to close before coding.

**Baseline accessibility state (current code).** Already correct and to be preserved:
- `<main>` landmark — `component.jsx:30`.
- `<form aria-label="Sign in">` — `component.jsx:31`.
- `<h1>Sign In</h1>` then `<h2>` inside the error summary — `component.jsx:32`, `:36` (valid: h1 → h2, no skip).
- Every input has an associated visible `<label htmlFor>` — `:46`, `:63`, `:86`.
- Conditional `aria-describedby` wiring inputs to their error paragraph — `:52`, `:69`.
- Conditional `aria-invalid` driven by `submitted && !!errors.x` — `:53`, `:70`.
- `aria-required="true"` on email and password — `:54`, `:71`.
- `autoComplete="email"` / `"current-password"` — `:55`, `:72` (supports WCAG 1.3.5 Identify Input Purpose).
- Error summary `role="alert"` — `:35`.
- Contrast values are documented in CSS and pass AA (see Visual Accessibility Plan).

**Gaps this plan closes (engaged review, not checklist):**
1. **Error-summary links scroll but do not focus the target field.** `<a href="#email">` (`component.jsx:39`) relies on default in-page anchor behavior. A native fragment link moves focus to the target only if the target is focusable *and* the browser performs the navigation; in a React SPA with client routing this is unreliable, and even in plain HTML the anchor focuses the `<input id="email">` only because inputs are focusable — but the `id` here is on the input, which is good, yet there is no guarantee the SPA doesn't intercept. We will make focus movement explicit. WCAG 2.4.3.
2. **`role="alert"` may not re-announce on a second failed submit.** If the summary node persists and only its list children change, some AT will not re-fire. We design the announcement so it fires on every submit attempt. WCAG 4.1.3.
3. **Focus is never moved on failed submit.** After pressing "Sign In," focus stays on the button; a keyboard/SR user is not taken to the errors. We move focus to the error summary. WCAG 2.4.3.
4. **No success-path status.** A successful submit (`onSubmit` fires) gives no programmatic confirmation that something is happening. We add a polite status region for the pending/submitting state. WCAG 4.1.3.
5. **`aria-required` is hardcoded; no visible required/optional indication.** Scout flagged this. Sighted users get no cue which fields are required; SR users hear "required" but the visual has nothing. We add a visible required indicator with a non-color cue. WCAG 3.3.2.
6. **Help links open same-window (fine), but "Forgot password?" / "Create account" are mid-flow.** No change required for new-window (they are same-window), but we document link-text quality. WCAG 2.4.4.

**What this plan does NOT cover (negative space).**
- Server-side authentication errors ("incorrect email or password") returned *after* a successful client-side validation. This plan covers client-side validation + the *mechanism* for announcing a server error, but the exact server-error copy and the auth flow are out of scope. The live-region design here is reused for it — see State Communication.
- Password-strength meter, "show password" toggle, social login, CAPTCHA, multi-factor — not present in the component, not designed here.
- Rate-limiting / lockout messaging.
- Internationalization of error strings (English-only here).

**Constraints.**
- React function component with `useState`; no form library. We will introduce two `useRef`s (error summary, and a per-submit announce key) and one effect for focus — no new dependencies.
- `noValidate` is intentional and stays; the app owns validation and error UX.
- Must remain a single self-contained component (eval fixture); no design-system imports.

---

## Semantic Structure Plan

**Landmarks.** One `<main>` wraps the page (`component.jsx:30`). For a dedicated sign-in page this is correct and sufficient; the form is the primary content of the page. The `<form>` carries `aria-label="Sign in"` (`:31`), which gives it an accessible name and makes it a navigable form region for AT that exposes forms. **Keep both.** WCAG 1.3.1, 2.4.1 (the `<main>` is itself the bypass target on a single-form page; see Focus Management for the multi-region case).

**Heading hierarchy.**
- `<h1>Sign In</h1>` — page title (`:32`).
- `<h2>Please fix the following errors:</h2>` — error summary heading, only present when errors exist (`:36`).

This is valid: h1 → h2, no skipped levels. The h2 living inside a `role="alert"` is acceptable — the heading text becomes part of the alert announcement, which is desirable ("Please fix the following errors" is a useful thing to hear). WCAG 1.3.1, 2.4.6 (Headings and Labels).

**Form structure.**
- The three fields are independent inputs. They are **not** a semantic group that needs `<fieldset>/<legend>` — email, password, and remember-me are not a set of related choices (radio/checkbox groups want a fieldset; a sequence of distinct inputs does not). Adding a fieldset here would add announcement noise without structural meaning. **Decision: no fieldset.** WCAG 1.3.1 (use grouping only where a real relationship exists).
- Each field is a `<div class="form-field">` containing label → input → (conditional) error `<p>`. Keep.
- The checkbox field places the input before the label (`:80`–`:86`). For checkboxes, label-after-input is the conventional and correct visual order; the association is via `htmlFor`/`id`, so DOM order is fine. Keep.

**List structure.** The error summary uses `<ul><li>` (`:37`–`:41`) — correct: it is a list of errors, and SR users hear "list, N items," giving an error count for free. Keep.

**Skip navigation.** On this single-form page, the first focusable element is the email input (or the error-summary link after a failed submit). There is no repeated nav block to bypass, so a dedicated skip link is **not required** here (WCAG 2.4.1 Bypass Blocks applies to content repeated across pages). **If** this form is embedded in a layout with a site header/nav (i.e., the real app, not the fixture), a "Skip to main content" link targeting `<main>` is required — documented as a conditional task, not a fixture task.

**Document outline / reading order.** DOM order = visual order = logical order: heading → (errors) → email → password → remember-me → submit → help links. WCAG 1.3.2, 2.4.3. No CSS reordering is used that would break this (verified against `styles.css` — only `display:flex` on `.checkbox-field` with default source order). Keep.

**HTML structure stub** (semantic shape only — not implementation code):

```
<main>                                      ← landmark
  <form aria-label="Sign in" noValidate>
    <h1>Sign In</h1>

    <!-- Error summary: rendered only after a failed submit -->
    <div  role="alert"                      ← see State Communication for the
          tabindex="-1"                     ← announce-on-every-submit design
          ref={summaryRef}>
      <h2>Please fix the following errors:</h2>
      <ul>
        <li><a href="#email">{email error text}</a></li>
        <li><a href="#password">{password error text}</a></li>
      </ul>
    </div>

    <div class="form-field">
      <label for="email">Email address <span class="req" aria-hidden="true">*</span></label>
      <input id="email" type="email"
             aria-required="true"
             aria-invalid={…}
             aria-describedby={…}            ← "email-error" and/or "email-hint"
             autocomplete="email">
      <p id="email-error" class="field-error">…</p>   ← conditional
    </div>

    <div class="form-field">
      <label for="password">Password <span class="req" aria-hidden="true">*</span></label>
      <input id="password" type="password"
             aria-required="true"
             aria-invalid={…}
             aria-describedby={…}            ← "password-error" and/or "password-hint"
             autocomplete="current-password">
      <p id="password-error" class="field-error">…</p>  ← conditional
    </div>

    <div class="form-field checkbox-field">
      <input id="remember" type="checkbox">
      <label for="remember">Remember me</label>
    </div>

    <button type="submit">Sign In</button>

    <!-- Polite status region: empty in DOM at all times, text injected on submit -->
    <p class="visually-hidden" role="status" aria-live="polite"></p>

    <p class="help-links">
      <a href="/forgot-password">Forgot password?</a> |
      <a href="/register">Create account</a>
    </p>
  </form>
</main>
```

Note the `<span class="req">*</span>` is `aria-hidden` because the asterisk would otherwise be announced as "star"/"asterisk" and `aria-required="true"` already conveys "required" to AT. The visible `*` plus a legend ("* = required") is the *visual* non-color cue. See Content Accessibility for the required-field copy.

---

## Interaction Pattern Design

This component is built from standard form controls. The only composite-ish behaviors are the submit→validate→announce→focus cycle and the error-summary-link → focus-field cycle. Each interactive element maps to a native HTML semantic (the strongest "pattern" available — native controls beat ARIA recreations).

### Interactive Elements Table

| Widget | APG Pattern / Spec | Keyboard | ARIA | WCAG |
|--------|-------------------|----------|------|------|
| Email input | Native `<input type="email">` — no ARIA widget role needed. [WAI tutorial: Forms](https://www.w3.org/WAI/tutorials/forms/) | Tab to focus; type to edit; standard text-edit keys | `aria-required="true"`; `aria-invalid` (true on failed submit); `aria-describedby` → hint and/or error id; `autocomplete="email"` | 1.3.1, 1.3.5, 3.3.2, 4.1.2 |
| Password input | Native `<input type="password">` | Tab; type; standard text-edit keys | `aria-required="true"`; `aria-invalid`; `aria-describedby`; `autocomplete="current-password"` | 1.3.1, 1.3.5, 3.3.2, 4.1.2 |
| Remember-me checkbox | Native `<input type="checkbox">` — [APG Checkbox](https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/) (native satisfies it) | Tab to focus; **Space** toggles | Native `checked` state — **no `aria-checked`** (native checkbox exposes state itself; adding `aria-checked` is redundant/forbidden on native) | 2.1.1, 4.1.2 |
| Submit button | Native `<button type="submit">` — [APG Button](https://www.w3.org/WAI/ARIA/apg/patterns/button/) | Tab to focus; **Enter** or **Space** activates; **Enter** from within any field also submits the form (native form behavior) | Optionally `aria-disabled` + `aria-busy` while submitting (see State Communication); accessible name from text content "Sign In" | 2.1.1, 4.1.2 |
| Error-summary item link | Native `<a href="#fieldId">` — [WAI: Error notification tutorial](https://www.w3.org/WAI/tutorials/forms/notifications/) | Tab to focus; **Enter** activates → **moves focus to the target field** (see Focus Management) | Accessible name = the error message text (e.g., "Email address is required.") | 2.4.3, 2.4.4, 2.1.1 |
| Help links (Forgot / Create) | Native `<a href>` | Tab; Enter | Accessible name from link text | 2.4.4 |

**Screen reader experience, element by element:**
- **Email input on focus:** "Email address, required, edit text" (label + `aria-required` + role). After a failed submit: "Email address, invalid entry, Email address is required., required, edit text" (label + `aria-invalid` + `aria-describedby` error text + required + role). The `aria-describedby` is what reads the error inline when focus lands on the field. WCAG 3.3.1, 1.3.1.
- **Checkbox on focus:** "Remember me, checkbox, not checked." On Space: "checked." Native — nothing to add.
- **Submit button on focus:** "Sign In, button." While submitting (if we set `aria-busy`/disabled): "Sign In, dimmed/unavailable" — see State Communication for why we prefer a status region over a disabled button.
- **Error-summary link on focus:** "Email address is required., link." On Enter: focus jumps to the email input and the SR re-announces the email field (now including its error via `aria-describedby`).

**Why no custom ARIA widget anywhere:** every control here has a native HTML element that already exposes correct name/role/state. The failure mode this avoids: rebuilding a checkbox as `<div role="checkbox" aria-checked>` and then forgetting Space-key handling or `tabindex`. Native controls cannot have that bug. WCAG 4.1.2.

---

## Focus Management Plan

**Tab order (verified against DOM, `component.jsx:30`–`96`):**
1. (After failed submit only) Error-summary links, top to bottom — email link, then password link.
2. Email input.
3. Password input.
4. Remember-me checkbox.
5. Sign In button.
6. Forgot password link.
7. Create account link.

This matches visual top-to-bottom order. WCAG 2.4.3. No positive `tabindex` anywhere (none in source — keep it that way). WCAG 2.4.3.

**No focus traps.** This is an inline form, not a modal. Tab must flow out of the form into the rest of the page naturally. Do **not** add a focus trap. (Documented explicitly because the planner protocol requires a trap decision for every component — here the decision is "none, and that is correct.")

**Focus movement on FAILED submit (new — closes Gap 3).**
- On submit with errors, after React renders the error summary, move focus to the summary container.
- Implementation shape: give the summary `tabindex="-1"` and store a ref; in an effect that runs when `submitted && errorCount>0`, call `summaryRef.current.focus({ preventScroll: false })`. Defer with a microtask/`setTimeout(…, 0)` so focus lands after the node is in the DOM (React commit timing). WCAG 2.4.3, 3.3.1.
- Rationale: a keyboard/SR user who pressed "Sign In" is now taken directly to the list of what went wrong, hears the alert, and can Tab into the first error link or read the list. Without this, focus stays on the button below the errors and the user may never discover them.

**Focus movement from an error-summary link (new — closes Gap 1).**
- Default fragment-link behavior (`href="#email"`) is unreliable in an SPA and, even when it works, only happens to focus the input because inputs are focusable. We make it explicit and predictable.
- Implementation shape: the link's `onClick` calls `e.preventDefault()`, then focuses the target input by id/ref with `el.focus({ preventScroll: true })`, then optionally `el.scrollIntoView({ block: 'center' })`. WCAG 2.4.3, 2.1.1.
- Keep the `href="#email"` attribute so the link is a real link (right-click, middle-click, and "links" rotor all still work; voice control "click Email address is required" works), but override the navigation behavior. Progressive enhancement: if JS fails, the fragment link still moves the viewport and focuses the natively-focusable input.
- After focus lands on the field, the field's own `aria-describedby` causes the SR to read the specific error — so the user hears *why* the field is wrong the instant they arrive. WCAG 3.3.1.

**Focus on SUCCESSFUL submit.**
- When validation passes and `onSubmit` fires, this component hands control to the parent (`onSubmit` callback). Focus management for what happens next (navigation to the app, or a server round-trip) belongs to the parent and is out of scope.
- **Within scope:** while the submit is in flight (if the parent returns a promise we await), set the polite status region to "Signing in…" so progress is announced; do not move focus during this window (moving focus mid-submit is disorienting). WCAG 4.1.3. If the component does not await `onSubmit`, this reduces to a no-op and the status region stays empty — documented as conditional.

**Focus indicator.** Every focusable element has a visible focus style in `styles.css`: inputs `:focus` (`:61`), error-summary links `:focus` (`:35`), submit `:focus-visible` (`:98`), help links `:focus` (`:111`). See Visual Accessibility for the contrast and the two-color hardening recommendation. WCAG 2.4.7, 2.4.11 (Focus Not Obscured — not obscured here, single-column layout).

**Roving tabindex:** not applicable — there is no composite widget (no tablist, menu, listbox, grid, tree). All focusable elements are independently Tab-reachable. (Decision recorded per protocol.)

**Reverse skip-link / in-page anchors:** the only in-page anchors are the error-summary links, handled above. No long-form content, so no "back to top" link needed.

---

## State Communication Design

Every state below is communicated **both** visually and programmatically. The dynamic states (announcement, busy) are where this component earns its Medium rating.

### State Communication Table

| State | Visual | Programmatic | ARIA / mechanism | WCAG |
|-------|--------|--------------|------------------|------|
| Field required | Visible `*` after label + "* = required" legend | "required" announced on field focus | `aria-required="true"` on input (`:54`,`:71`); `*` span is `aria-hidden` | 3.3.2, 4.1.2 |
| Field valid (default) | Grey 2px border (`#767676`) | role + name only | native input | 1.4.11 |
| Field invalid | Red 2px border (`#b71c1c`, `styles.css:66`) **+ inline red error text** | "invalid entry" + error text announced on focus | `aria-invalid="true"` (`:53`,`:70`) + `aria-describedby`→error id (`:52`,`:69`) | 1.4.1, 1.3.1, 3.3.1, 4.1.2 |
| Validation failed (form-level) | Red-bordered error summary box appears at top, lists each error | Announced as an alert on **every** submit attempt; focus moves to summary | `role="alert"` + the announce-on-every-submit design below | 4.1.3, 3.3.1, 2.4.3 |
| Checkbox checked / unchecked | Native checkbox glyph | "checked"/"not checked" | native `checked` (no `aria-checked`) | 4.1.2 |
| Submitting / pending | Button text → "Signing in…" and/or spinner; button visually dimmed | "Signing in…" announced politely | `role="status" aria-live="polite"` region; optionally `aria-busy="true"` on form, `aria-disabled` on button | 4.1.3 |
| Submit success | (Parent handles next view) | Parent handles | out of scope (mechanism reused from status region) | — |
| Server auth error (future) | Same error-summary box, message "Email or password is incorrect." | Announced via the same alert path | reuse `role="alert"` summary path | 4.1.3, 3.3.1 |

### The announce-on-every-submit design (closes Gap 2 — the highest-value item in this plan)

**Problem.** `role="alert"` announces when the node is **inserted** or when its **text content changes**. On the first failed submit the summary is inserted → it announces. On a *second* failed submit with the *same* errors, React reconciles the existing node and its text may be byte-identical → some AT (notably JAWS, and NVDA in certain modes) will **not** re-announce. The user gets silence on their second failed attempt and may think nothing happened.

**Design (pick ONE; option A is preferred):**

- **Option A — Move focus to the alert on every submit (recommended).** Combined with the focus-move from the Focus Management section: every failed submit calls `summaryRef.current.focus()`. Moving focus to the alert causes the SR to read it on arrival *regardless* of whether the live-region change fired. Because we focus on *every* failed submit (not only the first), the user always hears the errors. This makes the announcement robust without fighting React reconciliation. The `role="alert"` is retained as a belt-and-suspenders for users who don't get focus-read behavior.

- **Option B — Force a content change with a submit counter.** Keep a `submitAttempt` counter; include an invisible, changing token (e.g., the count) inside the alert, or key the summary node on the attempt count so React remounts it each submit. Remounting re-inserts the node → `role="alert"` re-fires. Heavier-handed; only use if focus-move (A) is rejected.

**Decision: implement A.** It also solves Gap 3 (focus discovery) in the same motion. Reserve B as fallback if testing shows A insufficient on a target AT.

### Live-region rules (the known-pitfall guardrails)

- **One announcement region per event class — never one per field.** The single `role="alert"` error **summary** is the per-submit announcement. **Per-field** error `<p>`s are **NOT** alerts and must **NOT** carry `role="alert"` or `aria-live` — they are silent text associated to their input via `aria-describedby` and read when the field receives focus. This prevents 2–N simultaneous live-region announcements firing on one submit (the classic "every field error screams at once" bug). The per-field `<p id="email-error">` (`:58`) and `<p id="password-error">` (`:75`) stay plain. WCAG 4.1.3, 1.3.1.
- **The pending/status region is separate and polite.** `role="status"` (= `aria-live="polite"`) for "Signing in…". It must exist **empty in the DOM at all times** and have text injected — do not conditionally mount the region itself, or the first injection may be missed. WCAG 4.1.3.
- **Assertive vs polite:** the error summary (`role="alert"` = assertive) is appropriate because a failed submit is an error the user must address now. The submit-progress message is `polite` because it is non-urgent status. WCAG 4.1.3.

### Error-message association (re-verified)

- Each invalid field: `aria-invalid="true"` (`:53`,`:70`) **and** `aria-describedby` pointing at its error `<p>` id (`:52`,`:69`). Both present in baseline — keep.
- **DOM-verification requirement:** the `aria-describedby` value (`"email-error"`) must match the rendered `<p id="email-error">`. In the baseline these are conditional on different flags — `aria-describedby` keys off `errors.email` (`:52`) while the `<p>` renders on `errors.email` (`:57`); these are consistent. But `aria-invalid` keys off `submitted && !!errors.email` (`:53`) while `aria-describedby` keys off `errors.email` alone (`:52`). **Edge case to fix:** if `errors.email` is set but `submitted` is false (not possible in current code flow, but fragile), `aria-describedby` would point at a `<p>` that *is* rendered (it renders on `errors.email`), so the reference resolves — acceptable. Recommendation: drive **all three** (`aria-invalid`, `aria-describedby`, and the `<p>` render) off the **same** condition to eliminate any future divergence. The testing strategy must confirm `aria-describedby` resolves to a present node in the DOM.

---

## Visual Accessibility Plan

**Color contrast (WCAG 1.4.3 / 1.4.11).** Verified from `styles.css` (values annotated in source):
- Body/label text `#222` on white = 14.7:1 (`:48`) — passes AA (need 4.5:1). Pass.
- h1 `#111` on white = 18.4:1 (`:11`) — pass.
- Error text/heading/links `#b71c1c` on `#fff3f3` ≈ 6.0:1 (`:24`) — pass (need 4.5:1).
- Input border `#767676` on white = 4.54:1 (`:55`) — passes the **3:1** non-text UI component requirement (1.4.11) with margin. Pass.
- Invalid border `#b71c1c` on white > 5:1 — pass (1.4.11).
- Submit button text `#fff` on `#1565c0` = 5.4:1 (`:87`) — pass (4.5:1). Hover `#0d47a1` is darker → higher contrast — pass.
- Help links `#1565c0` on white = 5.4:1 (`:107`) — pass.
- **Large text:** h1 at 1.75rem (28px) is "large" (≥24px); its 18.4:1 far exceeds the 3:1 large-text minimum. No other text qualifies as large; all normal text meets 4.5:1.

**Focus indicator (WCAG 2.4.7, 2.4.11, 1.4.11).**
- All focus styles use a 3px outline at `#005fcc` (inputs, submit, help links) or `#b71c1c` (error links) with `outline-offset: 2px`.
- `#005fcc` on white = 5.6:1; the focus outline vs adjacent colors exceeds the 3:1 non-text requirement. Pass.
- **Hardening recommendation (not a defect):** the single-color outline `#005fcc` is invisible if this form is ever placed on a blue background or inside a themed container. **Plan a two-color (double-ring) focus indicator** — pair the `outline` with a contrasting `box-shadow` (e.g., `outline: 3px solid #005fcc; box-shadow: 0 0 0 5px rgba(255,255,255,0.9)` or a dark inner ring) so the indicator is visible on any background. WCAG 2.4.11.
- **`:focus` vs `:focus-visible` inconsistency:** inputs and links use `:focus` (`:61`,`:35`,`:111`); the submit button uses `:focus-visible` (`:98`). For consistency and to avoid showing rings on mouse-click for inputs (where it is arguably fine) — standardize. Recommendation: use `:focus-visible` for the button (keyboard-only ring) and keep `:focus` for inputs (inputs *should* show focus on click too, since users click into them). This is a deliberate split, not an accident — document it so a future dev doesn't "fix" it into inconsistency. WCAG 2.4.7.

**Color as sole indicator (WCAG 1.4.1).** Audit of every color-coded state:
- **Invalid field:** red border **+ red inline text** + `aria-invalid`. Not color-alone (the text message is the non-color cue). Pass.
- **Error summary:** red border + heading text "Please fix the following errors" + list. Not color-alone. Pass.
- **Required field:** currently **no visual indicator at all** beyond `aria-required` (which is invisible). This is the one place a sighted user gets no cue. **Add a visible `*` + a "* = required" legend** (non-color: it's a glyph + text, not a color). WCAG 3.3.2, 1.4.1.
- **Links in body text:** the help links and error-summary links are **underlined** (`:32`/`text-decoration: underline` at `:108`,`:32`) — distinguished by more than color. Pass (1.4.1 link-in-text rule). Note: `#1565c0` link vs `#222` body text — the links sit on their own line (`.help-links`), not inline in a paragraph of body text, so the in-text adjacency rule is less critical, but the underline satisfies it regardless.

**Font sizing / zoom (WCAG 1.4.4, 1.4.10).**
- All font sizes use `rem`/relative units (`1.75rem`, `1rem`, `0.875rem`, `0.9rem`) — verified, no fixed `px` font sizes in `styles.css`. Users can zoom text to 200% without breakage. Pass (1.4.4).
- **Reflow at 400% (1.4.10):** container is `max-width: 400px` (`:1`) and inputs are `width:100%` with `box-sizing:border-box` (`:53`,`:58`). At 400% zoom (320px effective viewport) the 400px max-width container exceeds the viewport → must not cause horizontal scroll. Because `max-width` (not fixed `width`) is used, the container shrinks to viewport width; inputs at `width:100%` follow. **Verify in testing** that nothing forces a min-width wider than 320px. The `margin: 40px auto` is fine (auto margins collapse). Likely passes; confirm by test.

**Responsive text / spacing (WCAG 1.4.12 Text Spacing).** No inline styles lock line-height or letter-spacing, so user stylesheets that bump spacing won't clip content. Inputs have generous padding. No fixed-height containers around text. Pass by construction; verify with the text-spacing bookmarklet in testing.

**Animation (WCAG 2.3.3).** No animations or transitions in `styles.css`. If a submit spinner is added (State Communication), it must respect `@media (prefers-reduced-motion: reduce)` — replace spin animation with a static "Signing in…" text. Documented as a constraint on the (optional) spinner.

**Dark mode / forced-colors (WCAG 1.4.11).** No `prefers-color-scheme` support currently. Not required for AA, but: under Windows High Contrast / `forced-colors`, the input border and focus outline must remain visible. `outline` survives forced-colors (it is not stripped); `border` colors are overridden by the OS but borders remain. The red invalid border will be replaced by the system color — **so the inline error text (not the border) is what carries the invalid state in forced-colors mode**, which is exactly why we never rely on the border alone. Pass by construction. Recommendation (optional): add `@media (forced-colors: active)` to ensure invalid state uses a system-respecting cue if desired.

**Touch targets (WCAG 2.5.8, AA).**
- Submit button: `width:100%` × ~`12px*2 + ~20px` line ≈ 44px tall — meets 44×44. Pass.
- Inputs: `width:100%` × ~`10px*2 + ~20px` ≈ 40px tall. **Slightly under 44px** but text inputs are exempt-adjacent (the 2.5.8 minimum is 24×24 for AA, not 44×44 — 44 is AAA 2.5.5). At 24×24 AA, all controls pass comfortably. The checkbox is the smallest target: native checkbox ~13–16px, but its `<label>` is clickable (via `htmlFor`) and the label text extends the activation area; combined target exceeds 24×24. Pass AA. **Recommendation:** bump inputs to ~44px tall and ensure the checkbox+label hit area is comfortable for motor-impaired users (exceeds AA, approaches AAA).
- Error-summary links and help links: inline text links are exempt from 2.5.8 ("inline" exception) but should have adequate line-height; current line-height is default (~1.4–1.5) — acceptable. Pass.

---

## Content Accessibility Plan

**Alt text (WCAG 1.1.1).** No images in the component. If a logo is added above the form, it must have `alt` describing the brand (or `alt=""` if purely decorative beside an adjacent text brand name). No `::before`/`::after` decorative content in `styles.css` to remediate. N/A for now.

**Link text quality (WCAG 2.4.4).**
- "Forgot password?" and "Create account" — both descriptive and self-explanatory out of context. Pass. (No "click here.")
- Error-summary links use the **full error message** as link text ("Email address is required.") — descriptive and unique. Pass. This is better than "Email" because the link text alone tells a rotor-browsing user both the field and the problem.
- The ` | ` separator between help links (`:93`) is a literal text node; SR may read "Forgot password? vertical bar Create account." Minor. **Recommendation:** wrap the separator in `aria-hidden="true"` or replace with CSS, OR make the two links separate list items / use a more natural separator. Low priority.

**Form labels (WCAG 1.3.1, 3.3.2).** Every input has a visible `<label htmlFor>` — verified (`:46`,`:63`,`:86`). **No `aria-label` substituting for a visible label anywhere** — correct (the known pitfall is using `aria-label` on a container instead of a real `<label>`; not present here). The form's `aria-label="Sign in"` (`:31`) names the *form region*, not a field — that is the correct use of `aria-label`. Keep all.

**Required/optional indication (WCAG 3.3.2).** Currently only `aria-required`. **Add:** a visible `*` per required label (`aria-hidden`) and a single legend near the top of the form, e.g., a small line "Fields marked * are required." associated by proximity. All three fields: email and password are required; remember-me is optional and needs no marker. WCAG 3.3.2.

**Error message clarity (WCAG 3.3.1, 3.3.3 Error Suggestion).** Current messages (`component.jsx:12`–`15`):
- "Email address is required." — identifies field + problem. Good (3.3.1).
- "Please enter a valid email address." — identifies problem. **Improve toward 3.3.3 (Error Suggestion, AA):** suggest the fix, e.g., "Enter an email address in the format name@example.com." Recommended.
- "Password is required." — good.
- "Password must be at least 8 characters." — identifies the rule and suggests the fix (length). Good (3.3.3).
- All messages are specific, not "Invalid input." Pass 3.3.1; tighten email message for 3.3.3.

**Form instructions (WCAG 3.3.2).** The 8-character password rule is currently only revealed *after* a failed submit. **Recommendation:** surface the password requirement up front as a hint associated via `aria-describedby` (e.g., `<p id="password-hint">Must be at least 8 characters.</p>` and add `password-hint` to the input's `aria-describedby`). This lets users meet the requirement before submitting (3.3.2), reducing error encounters entirely. When an error also appears, `aria-describedby` can reference both the hint and the error id (space-separated id list) — order them error-first so the problem is heard first. WCAG 3.3.2, 1.3.1.

**Language (WCAG 3.1.1, 3.1.2).** `<html lang="en">` is a document-level requirement owned by the page shell, not this component — documented as a host-page requirement. No foreign-language phrases in the component, so no `lang` attributes on parts needed. N/A within the component.

**Reading order (WCAG 1.3.2).** DOM = visual = logical (established in Semantic Structure). Pass.

**Autocomplete (WCAG 1.3.5, AA).** `autoComplete="email"` and `"current-password"` present (`:55`,`:72`) — lets password managers and browser autofill work, which is a major accessibility win for cognitive and motor users. Keep. Consider `autoComplete="off"` is **not** wanted here (we *want* autofill).

---

## Testing Strategy

Route execution through `a11y-test` (Playwright + axe-core) and real AT. The dynamic behaviors here cannot be validated by axe alone — they need keyboard simulation, DOM inspection, and screen-reader listening.

**1. Automated (axe-core via `a11y-test` / Playwright).**
- Run axe on **every state variant**, not just default:
  - (a) pristine form, (b) after failed submit (both errors), (c) after failed submit (one error), (d) submitting/pending state, (e) valid state pre-submit.
- axe **will** catch: missing labels, color contrast, `aria-*` referencing non-existent ids, invalid ARIA attribute/value, heading-order skips, `aria-required` on a role that forbids it.
- axe will **NOT** catch (must be covered manually): whether `role="alert"` actually re-announces on the second submit; whether focus moves to the summary; whether the error-link moves focus to the field; whether the SR reads the inline error on field focus; whether the status region announces "Signing in…". **Do not treat an axe pass as done.**
- **Specific axe assertion:** zero violations on all five variants; specifically `aria-valid-attr-value` (the `aria-describedby` ids resolve) and `color-contrast` pass.

**2. Manual keyboard (real key events — `npx playwright test` with `page.keyboard.press`, or `agent-browser` CDP; NOT Playwright MCP `browser_press_key`).**
- Tab order: Tab from page start lands email → password → checkbox → Sign In → Forgot → Create (and, after failed submit, the two error links come first). Assert exact order.
- Space toggles the checkbox; assert `checked` flips.
- Enter inside the email field submits the form (native behavior) — assert validation runs.
- Enter / Space on the Sign In button submits.
- **After a failed submit:** assert focus is on the error summary (`document.activeElement === summary`).
- **Error link → field focus:** focus the email error link, press Enter, assert `document.activeElement` is the email input (not just that the viewport scrolled).
- **Second failed submit:** submit twice with the same bad data; assert focus returns to the summary both times (the proxy for "re-announced").
- Focus indicator visible at each stop at 100% and 400% zoom (visual check / screenshot).

**3. Screen reader (real AT — NVDA+Firefox, JAWS+Chrome, VoiceOver+Safari).**
- Form region: navigating by form/landmark announces "Sign in, form" and "main."
- Field focus announces label + "required" + role; email type announced as appropriate.
- **Submit with errors:** the alert is announced ("Please fix the following errors, Email address is required., Password is required.") on the **first** submit. Repeat the bad submit; confirm it announces **again** (this is the JAWS/NVDA re-announce check — the core risk of this component).
- Move to a field via its error link; confirm the SR reads the field's inline error (via `aria-describedby`) on arrival.
- Checkbox: "Remember me, checkbox, not checked" → Space → "checked."
- Submitting state: confirm "Signing in…" is announced politely (if `onSubmit` is awaited).
- Confirm per-field error `<p>`s do **NOT** double-announce as live regions on submit (only the summary announces).

**4. Visual regression / responsive.**
- 200% text zoom: no clipping, no overlap (1.4.4).
- 400% page zoom @ 1280px (≈320px effective): single column, **no horizontal scroll**, all controls reachable (1.4.10).
- Text-spacing bookmarklet (line-height 1.5, letter 0.12em, word 0.16em, paragraph 2×): no clipped content (1.4.12).
- `prefers-reduced-motion`: if a spinner exists, it is static (2.3.3).
- `forced-colors: active` (Windows High Contrast): inputs, focus outline, and error text remain perceivable; invalid state still conveyed by inline text (not just border).

**5. DOM verification (the mandatory anti-pitfall step).**
- After a failed submit, dump the rendered DOM and assert:
  - The submit-time `aria-invalid="true"` lands on the *correct* input(s).
  - Each input's `aria-describedby` value matches the `id` of a `<p>` that is actually present in the DOM (reference resolves — no dangling `aria-describedby`).
  - The error summary has `role="alert"` and `tabindex="-1"` and contains one `<li>`/link per error.
  - Each error-summary link `href` (`#email`/`#password`) matches an existing input `id`.
  - The status region exists with `role="status"` even when empty.
  - The `*` required spans carry `aria-hidden="true"`.
- This step exists because static review and unit assertions can both pass while the attribute lands on the wrong element in the actual render. Confirm placement in the rendered output.

**Acceptance criteria (measurable):**
- axe-core: 0 violations across all 5 state variants.
- Keyboard: every interaction above passes with real key events; focus moves to summary on failed submit and to the field on error-link activation.
- Screen reader: error summary announces on **every** failed submit (verified on NVDA and JAWS); field error read on field focus.
- Reflow: no horizontal scroll at 400%/320px.
- DOM: all `aria-describedby` references resolve; `aria-invalid` on correct fields; `role="status"` region present.

---

## Implementation Tasks

### Task 1: Add visible required-field indication + password hint
🔍 **Review checkpoint**

**Files:** `evals/suites/chain/targets/login-form-clean/component.jsx`, `evals/suites/chain/targets/login-form-clean/styles.css`

**Structure stub:**
```
<label for="email">Email address <span class="req" aria-hidden="true">*</span></label>
…
<label for="password">Password <span class="req" aria-hidden="true">*</span></label>
<input id="password" … aria-describedby={[hintId, errorId].filter(Boolean).join(' ')}>
<p id="password-hint">Must be at least 8 characters.</p>
…
<p class="form-legend">Fields marked * are required.</p>   ← near top of form
```

**ARIA attributes:**
- `<span class="req">` → `aria-hidden="true"` (asterisk not announced; `aria-required` conveys it) — WCAG 4.1.2.
- Password input `aria-describedby` → space-separated id list, error id FIRST then hint id when both present — WCAG 1.3.1, 3.3.2.
- Keep existing `aria-required="true"` on email + password — WCAG 4.1.2 / 3.3.2.

**Keyboard interactions:** none new (informational content).

**State communication:** required state now has a visible (`*` + legend) and programmatic (`aria-required`) cue — closes the color/visibility gap.

**Tests:** DOM check that `*` spans are `aria-hidden`; SR check that field focus announces "required" once (not "required star"); password field focus reads the hint pre-submit.

**WCAG criteria:** 3.3.2 Labels or Instructions, 1.4.1 Use of Color, 4.1.2, 1.3.1.

**a11y-critic checkpoint 🔍:** Verify the asterisk is hidden from AT, the legend is present, `aria-describedby` id-list order is error-first, and no double-announce of "required."

---

### Task 2: Move focus to the error summary on every failed submit
🔍 **Review checkpoint**

**Files:** `component.jsx`

**Structure stub:**
```
<div role="alert" tabindex="-1" ref={summaryRef} className="error-summary"> … </div>

// effect: when submitted && errorCount > 0, after render:
//   setTimeout(() => summaryRef.current?.focus(), 0)
// run the effect on EVERY submit attempt (depend on a submit-attempt counter,
// not just on `errors`, so identical re-submits still re-fire)
```

**ARIA attributes:**
- `role="alert"` (keep, `component.jsx:35`) — WCAG 4.1.3.
- `tabindex="-1"` (new) so the container is programmatically focusable without entering the tab order — WCAG 2.4.3.

**Keyboard interactions:** after failed submit, focus lands on the summary; user can then Tab into the first error link or Shift+Tab back to the form.

**State communication:** this is the core fix — focus-move guarantees the errors are heard on every submit (including the second identical submit), independent of `role="alert"` reconciliation behavior.

**Tests:** keyboard — `document.activeElement === summaryRef` after first AND second failed submit. SR — alert content heard on every submit on NVDA and JAWS.

**WCAG criteria:** 2.4.3 Focus Order, 3.3.1 Error Identification, 4.1.3 Status Messages.

**a11y-critic checkpoint 🔍:** Verify the effect depends on a submit-attempt counter (re-fires on identical re-submit), focus deferral survives React commit timing, `tabindex="-1"` present, and the summary is not added to the natural tab order.

---

### Task 3: Make error-summary links move focus to their field
🔍 **Review checkpoint**

**Files:** `component.jsx`

**Structure stub:**
```
<li><a href="#email" onClick={focusField('email')}>{errors.email}</a></li>

// focusField(id) => (e) => {
//   e.preventDefault();
//   const el = document.getElementById(id);  // or refs map
//   el?.focus({ preventScroll: true });
//   el?.scrollIntoView({ block: 'center' });
// }
```

**ARIA attributes:** none added; link accessible name = error text (keep). Retain `href="#fieldId"` for real-link semantics and progressive enhancement.

**Keyboard interactions:** Enter on the error link moves focus to the matching input; the input's `aria-describedby` then causes the SR to read the specific error on arrival.

**State communication:** the user lands ON the broken field and immediately hears why it's broken — direct error recovery path.

**Tests:** keyboard — focus email error link, Enter, assert `activeElement` is the email input (not merely that the page scrolled). SR — on arrival the email error text is read. Progressive enhancement — with JS disabled the fragment link still focuses the (focusable) input.

**WCAG criteria:** 2.4.3 Focus Order, 2.4.4 Link Purpose, 2.1.1 Keyboard, 3.3.1.

**a11y-critic checkpoint 🔍:** Verify `preventDefault` + explicit focus (not reliance on default anchor), `href` retained for link semantics/voice-control, focus lands on the input itself, and `preventScroll` doesn't leave the field off-screen.

---

### Task 4: Add a polite submit-progress status region
🔍 **Review checkpoint**

**Files:** `component.jsx`, `styles.css` (add `.visually-hidden` utility)

**Structure stub:**
```
<p className="visually-hidden" role="status" aria-live="polite">{statusMsg}</p>
// region present at all times (empty string when idle)
// on submit success path, if onSubmit returns a promise:
//   setStatusMsg('Signing in…'); await onSubmit(...); (parent navigates)
// .visually-hidden = clip-rect off-screen technique (not display:none, which kills announcement)
```

**ARIA attributes:** `role="status"` (= `aria-live="polite"`) — WCAG 4.1.3. Region must be in the DOM continuously (text injected, not the node mounted) so the first message is reliably announced.

**Keyboard interactions:** none — do not move focus during submit.

**State communication:** "Signing in…" announced politely; reuses the same region for a future server-error message routed through the alert summary instead.

**Tests:** SR — "Signing in…" announced on submit (if awaited). DOM — region present with `role="status"` even when empty; `.visually-hidden` uses clip technique, not `display:none`/`visibility:hidden`. axe — region valid.

**WCAG criteria:** 4.1.3 Status Messages.

**a11y-critic checkpoint 🔍:** Verify the region is persistently mounted (not conditionally rendered), uses an announcement-safe hiding technique, is `polite` (not assertive), and that no focus move happens during the pending window. If `onSubmit` is not awaited, confirm this degrades to a harmless no-op.

---

### Task 5 (Conditional — only if embedded in a full page layout): Skip link
🔍 **Review checkpoint**

**Files:** host page shell (NOT the fixture component) + `styles.css`

**Structure stub:**
```
<a href="#main" class="skip-link visually-hidden-until-focus">Skip to main content</a>
…
<main id="main"> … </main>
```

**ARIA attributes:** none; native anchor. Visible on focus.

**Keyboard interactions:** first Tab on the page reveals and focuses the skip link; Enter moves focus past the nav to `<main>`.

**State communication:** n/a.

**Tests:** keyboard — first Tab reveals skip link; Enter focuses `<main>`.

**WCAG criteria:** 2.4.1 Bypass Blocks.

**a11y-critic checkpoint 🔍:** Only required if repeated navigation precedes the form. On the standalone fixture this task is N/A — do not add a skip link to a single-form page with no preceding nav (it would be a focus stop to nowhere useful).

---

### Task 6 (Hardening): Two-color focus indicator + focus-style consistency
🔍 **Review checkpoint**

**Files:** `styles.css`

**Structure stub:**
```
input:focus, a:focus, button:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
  box-shadow: 0 0 0 5px rgba(255,255,255,0.9);  /* second ring for any-background visibility */
}
```

**ARIA attributes:** none (visual only).

**State communication:** focus is visible on any background, not just white.

**Tests:** visual — focus visible at 100% and 400% zoom; if the form is themed onto a colored background, the ring is still visible. Contrast — outline ≥ 3:1 against adjacent colors.

**WCAG criteria:** 2.4.7 Focus Visible, 2.4.11 Focus Appearance, 1.4.11 Non-text Contrast.

**a11y-critic checkpoint 🔍:** Verify two-color technique, `:focus-visible` for button vs `:focus` for inputs is a deliberate documented split, and the box-shadow ring color contrasts with likely backgrounds.

---

## a11y-Critic Review Checkpoints

| Checkpoint | After Task | Focus |
|-----------|-----------|-------|
| 🔍 1 | Task 1 | Required indication: `*` is `aria-hidden`, legend present, `aria-describedby` id-list order (error-first), no "required star" double-announce |
| 🔍 2 | Task 2 | Focus-to-summary fires on EVERY failed submit (submit-counter dep), survives React commit timing, `tabindex="-1"`, summary not in natural tab order |
| 🔍 3 | Task 3 | Error link uses `preventDefault` + explicit `.focus()` on the input, `href` retained, field lands on-screen |
| 🔍 4 | Task 4 | Status region persistently mounted, announcement-safe hiding, `polite`, no focus move during submit, no-op when `onSubmit` unawaited |
| 🔍 5 | Task 5 | Only if preceded by nav; otherwise correctly omitted |
| 🔍 6 | Task 6 | Two-color focus ring, deliberate `:focus`/`:focus-visible` split, ring contrast |

**Escalation to perspective-audit:** if any checkpoint surfaces a MEDIUM/HIGH concern for a specific access perspective (e.g., the second-submit re-announce fails on JAWS = screen-reader perspective HIGH; reflow clips at 400% = low-vision perspective MEDIUM), escalate that perspective to `perspective-audit` per the lifecycle in `CLAUDE.md`.

---

### Contract Appendix (for spec-kitty-bridge WP translation)

### Architecture Overview
A native-HTML login form (no ARIA widget recreations) hardened on its dynamic path. Semantic structure is already sound (landmark, heading order, associated labels, list-based error summary). The work concentrates on three dynamic behaviors that static markup cannot guarantee: (1) error announcement that fires on **every** failed submit via a focus-move to a `tabindex="-1"` `role="alert"` summary; (2) error-summary links that explicitly move focus to their target field (not relying on fragment-anchor default behavior); (3) a persistently-mounted polite `role="status"` region for submit progress. Plus visual hardening (required-field indication, two-color focus ring) and content improvements (email error suggestion, up-front password hint). One announcement region per event class; per-field errors stay silent and are read via `aria-describedby` on field focus.

### Implementation Tasks

#### Task 1: Add visible required-field indication + password hint
Estimated Effort: low
Depends on: none

#### Test Strategy for Task 1
DOM: `*` spans carry `aria-hidden="true"`; password `aria-describedby` id-list resolves and is error-first. SR: field focus announces "required" once; password hint read pre-submit. WCAG 3.3.2, 1.4.1, 4.1.2, 1.3.1.

#### Acceptance Criteria for Task 1
Visible `*` on email + password labels, hidden from AT; "Fields marked * are required." legend present; password hint associated via `aria-describedby`; SR announces required without reading the asterisk.

#### Task 2: Move focus to the error summary on every failed submit
Estimated Effort: medium
Depends on: none

#### Test Strategy for Task 2
Keyboard: `activeElement === summary` after first AND second failed submit. SR: alert heard on every submit (NVDA + JAWS). WCAG 2.4.3, 3.3.1, 4.1.3.

#### Acceptance Criteria for Task 2
Summary has `role="alert"` + `tabindex="-1"`; focus moves to it on each failed submit (effect keyed on a submit-attempt counter); summary absent from natural tab order; focus deferred to survive React commit.

#### Task 3: Make error-summary links move focus to their field
Estimated Effort: low
Depends on: Task 2

#### Test Strategy for Task 3
Keyboard: Enter on email error link → `activeElement` is the email input. SR: field error read on arrival. Progressive enhancement: works (focuses input) with JS disabled. WCAG 2.4.3, 2.4.4, 2.1.1, 3.3.1.

#### Acceptance Criteria for Task 3
Link `onClick` calls `preventDefault` then `.focus()` on the target input; `href="#fieldId"` retained; field scrolled into view; SR reads the inline error via `aria-describedby` on arrival.

#### Task 4: Add a polite submit-progress status region
Estimated Effort: low
Depends on: none

#### Test Strategy for Task 4
SR: "Signing in…" announced on submit (when `onSubmit` awaited). DOM: `role="status"` region present even when empty; hiding via clip technique, not `display:none`. axe: region valid. WCAG 4.1.3.

#### Acceptance Criteria for Task 4
Persistently-mounted `role="status"` `aria-live="polite"` region; text injected (node not conditionally mounted); announcement-safe hiding; no focus move during submit; harmless no-op if `onSubmit` is not awaited.

#### Task 5: Skip link (conditional)
Estimated Effort: low
Depends on: none

#### Test Strategy for Task 5
Keyboard: first Tab reveals skip link; Enter focuses `<main>`. WCAG 2.4.1.

#### Acceptance Criteria for Task 5
Only implemented if repeated navigation precedes the form; otherwise correctly omitted from the standalone form.

#### Task 6: Two-color focus indicator + focus-style consistency
Estimated Effort: low
Depends on: none

#### Test Strategy for Task 6
Visual: focus visible at 100%/400% and on a colored background. Contrast: outline ≥ 3:1 vs adjacent. WCAG 2.4.7, 2.4.11, 1.4.11.

#### Acceptance Criteria for Task 6
`outline` + `box-shadow` double ring on focus; deliberate `:focus` (inputs) vs `:focus-visible` (button) split documented; ring contrasts on likely backgrounds.

### Failure Modes
- **Second-submit silence:** `role="alert"` does not re-fire on an identical re-submit; mitigated by focus-move keyed on a submit-attempt counter (Task 2). If the counter dependency is dropped, the bug returns.
- **Error-link scroll-without-focus:** relying on fragment-anchor default behavior scrolls the viewport but leaves focus on the link in an SPA; mitigated by explicit `.focus()` (Task 3).
- **Multiple live regions firing at once:** if per-field error `<p>`s are given `role="alert"`/`aria-live`, every error announces simultaneously on submit; prevented by keeping per-field errors silent (one region per event class).
- **Dangling `aria-describedby`:** if the error `<p>` and the `aria-describedby` value diverge in their render conditions, the reference points at a missing node; prevented by driving `aria-invalid`, `aria-describedby`, and the `<p>` render off the same condition + the DOM-verification test step.
- **Status region missed announcement:** conditionally mounting the `role="status"` node (instead of injecting text into an always-present node) can drop the first message; prevented by persistent mounting (Task 4).
- **Focus lands off-screen:** `focus({preventScroll:true})` without a follow-up `scrollIntoView` can move focus to a field outside the viewport; prevented by pairing focus with scroll (Task 3).
- **Reflow clip at 400%:** any fixed min-width wider than 320px causes horizontal scroll; prevented by `max-width`/`width:100%` (already in baseline) + the reflow test.
- **Disabled-button trap on submit:** if the submit button is set `disabled` (not `aria-disabled`) during submit while focus is on it, focus is lost to `<body>`; if a busy state is added, prefer `aria-disabled` + ignored activation, or keep focus managed — covered by "no focus move during submit" in Task 4.
