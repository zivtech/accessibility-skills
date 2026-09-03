I'll read the single file I've been given and run the full protocol on it.

---

# VERDICT: ACCEPT

**Overall Assessment**: This is a correctly-designed async status/recovery component. The core pattern under review — persistent live regions written into rather than mounted with content, an assertive alert as a *sibling* of (not a replacement for) the polite status region, and a Retry control that never unmounts — is implemented as documented and matches how AT actually behaves. Semantics are native throughout; there is no ARIA masking a `div`. I found no CRITICAL or MAJOR defects. Three MINOR items and two enhancements are below; two further items are genuinely uncertain and sit in Open Questions rather than being reported as findings.

---

## Pre-commitment Predictions

Before reading the code, for an async-fetch panel with retry I predicted five failure modes:

| # | Prediction | Actual |
|---|---|---|
| 1 | Live region mounts with its message already inside → never spoken | **Partially landed** — true for the initial mount only (see MINOR-2); every subsequent transition is correct |
| 2 | Recovery is silent — the error region replaces the status region, so success after failure has nowhere to land | **Wrong.** Explicitly handled: the two regions are siblings (`:37`, `:54`), so `error → loading → ready` produces spoken output |
| 3 | Retry button lives inside the conditionally-rendered body → unmounts → focus destroyed | **Wrong.** Button is in `<header>` at `:28`, outside the `status`-gated body |
| 4 | Loading is visual-only (spinner, no programmatic signal) | **Wrong.** `aria-busy` at `:33` plus text in the status region; spinner is `aria-hidden` at `:40` |
| 5 | Zero-length success renders nothing and announces nothing | **Wrong.** Handled at `:47` |

Four of five predictions were defeated by the code. That is the honest signal here: the component was designed against exactly these failure modes, not merely decorated with ARIA.

---

## Critical Findings

None.

## Major Findings

None.

---

## Minor Findings

**MINOR-1 — `list-style: none` strips list semantics in Safari/VoiceOver**
`async-retry-recovery-clean.md:149` sets `list-style: none` on `.txn-list`. WebKit removes the implicit `list` role from a `<ul>` whose list-style is `none`, so VoiceOver users do not hear "list, 8 items" or item positions when arrowing through `:60`–`:68`.
- Confidence: HIGH (well-documented WebKit behavior; the CSS is verbatim in the file)
- WCAG: 1.3.1 Info and Relationships
- Impact: screen reader users on Safari/VoiceOver
- Mitigated by: the status region already announced "Loaded N transactions." at `:46`, so the count is still available, and every row remains readable. This is lost structure, not lost content — hence MINOR, not MAJOR.
- Fix: add `role="list"` to the `<ul>` at `:60`.

**MINOR-2 — The *initial* loading message is the one announcement not covered by the persistent-region invariant**
`useState('loading')` at `:7` means the first commit inserts `.panel-status` (`:37`) into the DOM **with** "Loading activity…" (`:41`) already inside it. That is precisely the case the component's own comment at `:34`–`:36` warns about. The invariant claimed at `:173` ("text written into them rather than being mounted alongside their own content") holds for every transition *except* the first one.
- Confidence: HIGH on the mechanism; MEDIUM on user impact (varies by whether the panel is present at page load or inserted after a route change)
- WCAG: 4.1.3 Status Messages
- Impact: screen reader users
- Mitigated by: `aria-busy="true"` at `:33` exposes the busy state to anyone navigating into the panel, and the *outcome* announcements (`ready`, `error`) are fully reliable because by then the region is registered. The user is not left uninformed of the result — only of the wait.
- Fix (if the first announcement matters): initialize `status` to `'idle'` and render an empty status region on the first paint, flipping to `'loading'` inside the effect at `:22`. One render tick is enough for the region to register.
- Note for the fixture's own prose: `:165` states the mount announcement as a certainty. That claim is stronger than the code supports.

**MINOR-3 — No stale-response guard; a late failure can fire a false assertive alert**
`load` at `:10`–`:20` has no `AbortController` and no request-generation check, and the effect at `:22` has no cleanup. If Retry is pressed while a request is in flight (`:28` stays enabled during `loading`), or if `accountId` changes mid-flight, an earlier failing response can resolve *after* a later successful one and call `setStatus('error')` at `:18`. The result is an assertive announcement of "We couldn't load your activity…" (`:56`) while the data is actually fine, and the transaction list at `:59` unmounting underneath it.
- Confidence: HIGH that the race exists in the code shown; MEDIUM that it fires in practice (requires activation during flight or a mid-flight prop change)
- WCAG: 4.1.3 Status Messages — an assertive region must not announce a state that is not current
- Impact: screen reader users most acutely (assertive interrupts); all users see content vanish
- Fix: capture a request id or `AbortController` in `load`, and ignore/abort resolutions that are not the latest. Optionally set `aria-disabled` (not `disabled` — keeps it focusable and discoverable) on Retry while `status === 'loading'`.

---

## Enhancements

- **Retry's accessible name is context-dependent.** `:28`–`:30` gives the button the name "Retry". Inside the region named "Account Activity" (`:25`, `:27`) this is clear, but in a screen reader's flat button list on a page with several such panels, several identical "Retry, button" entries are indistinguishable. WCAG 2.4.6. Fix if the page hosts more than one panel: `aria-label="Retry loading account activity"`, or a visually-hidden suffix. Not a violation as written — the region name is programmatically available.
- **One error message covers every failure class.** The `catch` at `:17` discards `err` and `:56` always says "Check your connection and press Retry." A 403 or 404 is not a connection problem, and the instruction misdirects. Cognitive accessibility / WCAG 3.3.3 Error Suggestion. Branching on `res.status` for at least auth-vs-network would make the suggestion actionable.
- **`.retry` measures roughly 33px tall** (`:101`–`:108`) — comfortably past WCAG 2.5.8 Target Size (Minimum, 24×24, AA). It is under the 44×44 of 2.5.5 (Enhanced, AAA). Noting the AA pass explicitly so it is not later misread as a gap.

---

## What's Missing

Checked and **present** (recording these so the clean result is legible, not assumed):
- `prefers-reduced-motion` handling for the spinner — `:140`–`:142`
- Empty-result announcement — `:47`
- Decorative spinner removed from the a11y tree — `:40`
- Programmatic busy state, not spinner-only — `:33`
- Visible focus indicator that is never suppressed — `:110`–`:113`; the CSS contains no `outline: none` anywhere, so browsers without `:focus-visible` still show the UA ring
- Named region + heading — `:25`, `:27`; `<header>` at `:26` is scoped inside `<section>` so it maps to `generic`, correctly avoiding a stray `banner` landmark
- Layout-shift suppression via `min-height: 120px` — `:117`
- No spurious announcement when the alert empties on recovery — default `aria-relevant` is `additions text`, so clearing `:54` is silent, and the design correctly routes the recovery news through the status region instead

Genuinely absent, and each judged not to be a defect: no `<time>` element for `:63`; no `aria-describedby` linking the error to the Retry button (the message names the control in prose instead, which is the better choice here — a describedby would re-announce the whole error on every focus of the button).

---

## Multi-Perspective Notes

- **Screen reader user**: Reaches a named region "Account Activity", heading level 2, then a Retry button. The failure→retry→success arc is fully spoken, in the right politeness for each event, which is the hard part and is done correctly. Two frictions: the first "Loading activity…" may pass silently (MINOR-2), and on Safari/VoiceOver the transaction list loses its list semantics (MINOR-1). Neither blocks the task.
- **Keyboard-only user**: One focusable element, always mounted (`:28`), so no focus is ever destroyed and none needs restoring — the design sidesteps focus management rather than getting it wrong, which is the correct call for this component. Focus indicator is 3px `#0b5fff` with 2px offset against white ≈ **5.1:1**, past the 3:1 of 1.4.11. Enter and Space both work (native `<button type="button">`). No traps, nothing to Escape from.
- **Low vision (200% zoom, high contrast)**: Body text `#475467` on white ≈ **7.7:1** (`:124`); error text `#b42318` on white ≈ **6.6:1** (`:128`) — both past AA, error past AAA. Error is conveyed by text, not color alone (1.4.1 satisfied). `max-width: 640px` with `auto` margins reflows cleanly at 200%. Note the contrast figures assume a white page background, which the file does not declare — `.activity-panel` at `:81` sets no `background`.
- **Cognitive accessibility**: The error message states the problem *and* names the control that fixes it (`:56`) — this is the strongest cognitive-accessibility decision in the file, and it is rare. Layout does not jump between states (`:117`). No timeouts, no destructive actions needing confirmation. The single weakness is the one-size-fits-all error text noted under Enhancements.

---

## Verdict Justification

ACCEPT. No finding rises to MAJOR under the Realist Check, and I declined to inflate any of the three MINORs:

- MINOR-1 costs structure, not content, and the item count is separately announced → held at MINOR rather than promoted for "list semantics broken."
- MINOR-2 affects one announcement out of the four the state machine produces, and `aria-busy` partially covers it → held at MINOR. I considered MAJOR on the grounds that it is the same defect class the component was built to avoid, and rejected that: severity tracks user impact, not irony.
- MINOR-3 has the highest per-occurrence impact of the three but requires activation during flight → held at MINOR on frequency.

**No recalibrations upward or downward were needed** — nothing entered the list at CRITICAL or MAJOR to begin with.

For an upgrade to a fully unqualified pass, MINOR-1 (`role="list"`) and MINOR-3 (stale-response guard) are both one-line-scale fixes. MINOR-2 is a design choice with a real cost either way and is legitimately arguable.

**Calibration statement**: I specifically looked for and did **not** find — the announcement-swallowing region swap, the unmounted-trigger focus loss, the visual-only loading state, and the silent empty-result case. Each was checked against the source, not assumed from the file's own claims. The file's "Accessibility Features Present" section (`:171`–`:179`) is accurate against the code with the single exception of the mount-time qualifier in item 1.

---

## Open Questions (unscored)

1. **Does `aria-busy="true"` on `.panel-body` (`:33`) suppress the polite announcement from `.panel-status` (`:37`) nested inside it?** The loading text is written into the status region during exactly the window when its *ancestor* is busy. ARIA specifies that a busy live region should hold announcements until busy clears, but `aria-busy` here sits **above** the live region root rather than on it, and whether AT walks past the live region root to check ancestors is implementation-defined. If it does, MINOR-2 has a second independent cause. If it does not, `aria-busy` here is purely additive. **This needs measurement, not reasoning** — a `virtual-screen-reader` spoken-phrase assertion across the `loading → ready` transition would settle it in one test. I have deliberately not reported this as a finding.
2. **Reflow at 400% zoom / 320 CSS px.** `.txn-list li` (`:154`–`:160`) is `display: flex` with `justify-content: space-between`, no `flex-wrap`, and no `min-width` on the three spans; `.panel-header` (`:88`–`:94`) is the same shape with no `flex-shrink: 0` on the button. Default `flex-shrink: 1` should wrap text inside each span rather than force horizontal scroll, so I expect 1.4.10 to pass — but "expect" is not evidence, and long payee strings are the realistic stressor. A rendered measurement at 320px would confirm or refute; a code-only claim here would be manufactured.
3. **Page background is undeclared** (`:81` sets no `background`). All contrast ratios above assume white. If this panel is placed on a tinted or dark surface, `#475467` (7.7:1 on white) degrades fast. Worth confirming against the host page rather than the component.

---

## Provenance

I read exactly one file:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt-siblings-rows/prompts/async-retry-recovery-clean.blind.md`

No other file was read. No `evals/suites/` path, no `*.metadata.yaml`, no `*.rubric.yaml`, no grep of the repo for this fixture's name, and no git commands were run. All line citations are to the line numbers of that file as read, and all contrast ratios were computed by hand from the hex values at `:105`, `:124`, and `:128`.