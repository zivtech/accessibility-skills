I'll read the single file I'm permitted to read.

---

# Verdict: REVISE

**Overall Assessment**: The semantic shell is sound — labelled `<section>`, correct heading, real `<button>`, decorative spinner properly hidden, and every measured color pair passes AA. But the component is a three-state machine in which **no state transition is ever announced to assistive technology**. The one live region exists only inside the `loading` branch, so it is mounted already-populated (never announces), and it does not exist at all in the two states a user actually needs to hear about: failure and recovery. The stated design decision at `async-retry-error-unannounced.md:148` — keeping Retry mounted so focus is never destroyed — is correct in itself, but it removes the only implicit signal a screen reader user would have gotten, which makes an explicit announcement mandatory rather than optional. That announcement was never built.

**Pre-commitment Predictions**

Note first: the fixture's own title (`:1`, "Async Request Failure and Recovery Are Never Announced") telegraphs the headline defect. I treated it as a hint, not a finding, and deliberately audited for issues *beyond* it — several below (mount-populated live region, no-op Retry during load, empty ready state, `list-style:none` semantics) are independent of the telegraphed one.

Predictions for an async fetch/error/retry panel, before line-by-line reading:
1. Error state rendered without a live region → **confirmed** (CRITICAL 1)
2. Success state after retry not announced, focus not moved → **confirmed** (MAJOR 1)
3. `aria-busy` present but incoherent with the live region → **confirmed, but weaker than predicted** (MINOR 1 + Open Question 1 — I could not justify the suppression claim at MAJOR)
4. Retry button lacking disabled/busy state during in-flight request → **confirmed, and worse than predicted** (MAJOR 4 — the press is a literal no-op)
5. Missing `prefers-reduced-motion` on the spinner → **confirmed but not a violation** (Enhancement; 2.2.2's essential-progress exception applies)

**Surprise I did not predict**: the live region is *conditionally mounted*, so even the loading announcement — the one the author clearly believed was working — does not fire. The component announces nothing in any state, ever. That is the coherent through-line and it is more severe than "the error branch was forgotten."

---

## Findings

### Critical Findings

**C1. The `error` state has no live region — a failed request is completely silent.**
`async-retry-error-unannounced.md:41-45`

```jsx
{status === 'error' && (
  <p className="error-text">
    We couldn&rsquo;t load your activity. Check your connection and try again.
  </p>
)}
```

The only `role="status" aria-live="polite"` element in the component is scoped inside the `loading` branch (`:35`). When `setStatus('error')` fires at `:18`, that region **unmounts** and this plain `<p>` mounts in its place. Nothing in the error branch is a live region, has `role="alert"`, or is otherwise announced.

- **User group**: screen reader users (all of them); compounding impact on cognitive accessibility.
- **WCAG**: 4.1.3 Status Messages (AA) — a status message conveying an error must be programmatically determinable through role or properties such that it is presented without receiving focus. Also 1.3.1 for the unassociated error text.
- **Why this matters**: The panel loads on mount (`:22`), unattended. A screen reader user hears nothing, then the spinner silently disappears. They are left in a labelled region containing a heading and — as far as any announcement is concerned — nothing. The realistic worst case is not friction: it is a user concluding their **account has no recent activity** when in fact the request failed. That is a wrong conclusion about financial data, produced silently.
- **Realist Check**: A browse-mode user (NVDA/JAWS virtual cursor) *can* arrow into the region and find the error text, so this is not total access loss and I considered downgrading to MAJOR. It holds at CRITICAL because nothing gives the user a reason to go look — the failure is indistinguishable from a completed empty load (see M5), and the mitigation evaporates entirely on iOS VoiceOver and for any user who has already moved past the region. Detection in production is slow: this fails silently, so it surfaces as a user complaint or not at all.
- **Confidence**: HIGH.
- **Fix**: Render a single **persistent** live region that is always in the DOM and populate it with text per state. Because this is an error, `role="alert"` (implicit `aria-live="assertive"`) is defensible, but a persistent `role="status"` is the safer default for a panel that also announces success — do not use `role="alert"` on a per-item basis or inside a loop. Additionally associate the message with the control that acts on it: give the `<p>` an `id` and reference it from the Retry button via `aria-describedby`, so a user who tabs to Retry hears *why* they are being asked to retry.

```jsx
// Always mounted, outside every conditional branch:
<div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
  {status === 'error' ? "Couldn't load account activity. Check your connection and try again."
   : status === 'ready' ? `Account activity loaded. ${transactions.length} transactions.`
   : 'Loading account activity…'}
</div>
```

---

### Major Findings

**M1. Successful recovery after Retry is never announced, and focus deliberately does not move.**
`async-retry-error-unannounced.md:47-57`, with the design intent stated at `:148`

The `ready` branch renders a `<ul>` with no announcement of any kind. Line 148 states that Retry "stays mounted in every state, so pressing it never destroys the user's focus position." That focus decision is *correct* — but it is only half of a pattern. When focus intentionally stays on the trigger, the resulting content change is invisible to a screen reader user unless it is announced. The component chose the stable-focus half and omitted the announcement half.

- **User group**: screen reader users.
- **WCAG**: 4.1.3 Status Messages (AA).
- **Why this matters**: The user presses Retry, focus stays on Retry, and nothing happens as far as they can perceive. They cannot distinguish "retry succeeded, 12 transactions loaded" from "retry did nothing" from "still loading." The only way to find out is to abandon their focus position and browse the region manually — which is exactly the cost the line-148 design was trying to avoid.
- **Confidence**: HIGH.
- **Fix**: Covered by the persistent live region in C1, announcing a count on success (`"Account activity loaded. 12 transactions."`). The count is the load-bearing part — it converts a silent DOM swap into a verifiable outcome.

**M2. The live region is conditionally mounted with its content already inside, so even the loading announcement does not fire.**
`async-retry-error-unannounced.md:34-39`

```jsx
{status === 'loading' && (
  <div className="loading" role="status" aria-live="polite" aria-atomic="true">
```

A live region must be present in the accessibility tree *before* its contents change for assistive technology to announce the change. Here the region node and its text `"Loading activity…"` (`:37`) enter the DOM in the same commit. Two consequences:

1. **Initial render**: `status` is initialised to `'loading'` at `:7`, so this region is present at first paint. Screen readers do not announce live region content that exists at page load — correct behavior on their part, silence on ours.
2. **Retry cycle**: `error → loading` unmounts the `<p>` and mounts a fresh, pre-populated region node. Insertion-with-content is the well-known unreliable case across NVDA and JAWS.

- **User group**: screen reader users.
- **WCAG**: 4.1.3 Status Messages (AA); WAI-ARIA live region authoring practice (persistent container, injected content).
- **Why this matters**: This is the finding that changes the shape of the review. Without it, the component reads as "loading works, error was forgotten." With it, the component announces **nothing in any state, ever** — and a fix that only adds a live region to the error branch would reproduce this same bug there.
- **Confidence**: HIGH for the initial-render case (spec-level certainty); MEDIUM-HIGH for the retry-remount case (screen-reader dependent).
- **Fix**: Same persistent container as C1. Keep the container mounted unconditionally and change only its text child.

**M3. Pressing Retry while a request is in flight is a perceptual no-op.**
`async-retry-error-unannounced.md:11` and `:28-30`

`load()` begins with `setStatus('loading')`. If `status` is already `'loading'`, React bails out on the identical state value, no re-render occurs, and the DOM is byte-identical before and after the press. The button is never disabled (`:28` has no `disabled` or `aria-disabled`) and there is no announcement, so activation produces **zero** perceivable feedback — visually, programmatically, or aurally.

- **User group**: cognitive accessibility (primary), screen reader users (secondary).
- **WCAG**: 4.1.3 Status Messages (AA) for the missing feedback; the disabled-state gap is 4.1.2 Name, Role, Value (A).
- **Why this matters**: "Did my press register?" is the canonical cognitive-accessibility failure. A user who is unsure will press repeatedly, firing concurrent `fetch` calls with no `AbortController` (`:13`) — so a slow first response can resolve after a fast second and overwrite fresher data with staler data. The a11y-visible symptom is silence; the underlying race makes it worse.
- **Confidence**: HIGH.
- **Fix**: Set `aria-disabled="true"` on the Retry button while `status === 'loading'` and early-return from `load()` when already loading. Prefer `aria-disabled` over the `disabled` attribute here so the button stays focusable and keeps its place in the tab order — removing a focused element from the tab order mid-interaction is its own focus-management defect. Add an `AbortController` for the underlying race.

**M4. The empty `ready` state renders nothing and is indistinguishable from failure.**
`async-retry-error-unannounced.md:47-57`, CSS `:98-101`

If the fetch succeeds and returns `[]`, `status` becomes `'ready'`, the `<ul>` renders with zero `<li>` children, and `.panel-body { min-height: 120px }` reserves a blank box. There is no empty-state message.

- **User group**: cognitive accessibility and screen reader users (both, for different reasons).
- **WCAG**: 1.3.1 Info and Relationships (A) — the "no results" state is conveyed only by visual absence; 4.1.3 for the unannounced transition.
- **Why this matters**: A sighted user at least sees an empty bordered container and can infer *something* resolved. A screen reader user gets nothing at all — which is byte-identical to the C1 error experience. Two completely different outcomes (request failed / account genuinely has no activity) produce the same perceptual result. In a financial context those are not interchangeable.
- **Realist Check**: This degrades the experience for sighted users too, which argues it is a general UX gap rather than an a11y-specific one. It holds at MAJOR because the *ambiguity with the error state* is exclusively an assistive-technology problem — sighted users have a visual channel that disambiguates, screen reader users do not.
- **Confidence**: HIGH that the gap exists; MEDIUM that `[]` is a reachable state (depends on the API contract, which I cannot see).
- **Fix**: Branch the `ready` state on `transactions.length` and render an explicit "No activity in this period." message, and include that string in the live region announcement.

---

### Minor Findings

- **`aria-busy` is applied incoherently.** `:33` sets `aria-busy` on `.panel-body`, whose *only* child while busy is the loading live region (`:35`) — so the attribute describes a container that has nothing to be busy about. When it flips to `false`, the state that actually warrants an announcement arrives with no announcement attached. This is a coherence problem rather than a demonstrated violation; see Open Question 1 for the suppression question I could not resolve without measurement. (4.1.2)
- **`list-style: none` strips list semantics in Safari/VoiceOver.** `:129` sets `list-style: none` on `.txn-list` with no `role="list"`. Safari removes the `list` role when list markers are removed, so VoiceOver users lose the "list, 12 items" announcement. That item count is the only signal of how much data loaded, which compounds M1. Fix: add `role="list"` to the `<ul>`. (1.3.1)
- **Hardcoded `id="activity-heading"` risks collision.** `:27` and `:25`. The component takes an `accountId` prop (`:6`), which strongly implies more than one instance may render per page. If it does, every instance's `aria-labelledby` resolves to the first heading and each region is announced with the same name. I am holding this at MINOR rather than MAJOR because the developer can legitimately refute it with "one per page" — but the fix is one line. Fix: `const headingId = useId()`. (1.3.1)
- **Transaction fields carry no programmatic labels.** `:51-53` — three sibling `<span>`s whose meaning (date / payee / amount) is conveyed purely by visual column position via `justify-content: space-between` (`:136`). A screen reader reads a run-on string. Convention makes it mostly parseable, so this is friction rather than a barrier. Fix: visually-hidden labels, or model as a `<table>` with `<th scope="col">` if this is genuinely tabular. (1.3.1)
- **The error message conflates all failure modes.** `:17-19` swallows `err` entirely and `:43` always advises "Check your connection." A 403 or 500 will tell the user to check a connection that is working fine, sending them into an unfixable retry loop. This is cognitive-accessibility friction; I am explicitly **not** citing 3.3.1 Error Identification, which scopes to input errors and does not apply here.

---

### Enhancements

- **No `prefers-reduced-motion` fallback for the infinite spinner** (`:110-121`). I am explicitly not scoring this as a violation: WCAG 2.2.2 Pause, Stop, Hide exempts content where movement is essential, and a loading indicator qualifies. Still worth adding a `@media (prefers-reduced-motion: reduce)` branch swapping the rotation for an opacity pulse or static indicator.
- **Retry's accessible name is generic** (`:29`). "Retry" alone is thin in a button list; `aria-label="Retry loading account activity"` is more useful out of context. The enclosing `<section aria-labelledby>` (`:25`) gives it a `region` landmark for orientation, so this is polish, not a defect.
- **Target size**: `.retry` computes to roughly 33px tall (`:90`, 6px padding + ~19px line-box + 2px border). This **passes** WCAG 2.5.8 Target Size (Minimum, 24×24, AA) and fails only 2.5.5 (Enhanced, 44×44, AAA). No AA finding — raising to 44px is optional.

---

### Verified Clean

Stating these explicitly, because a review that only lists defects gives no signal about what was actually checked:

- **Color contrast passes at AA on every pair I could compute.** `.error-text` #b42318 on white = **6.57:1** (`:125`); `.loading` #475467 on white = **7.69:1** (`:107`); `.retry` #0b5fff text and border on white = **5.13:1** (`:93-94`), which also clears the 3:1 non-text threshold of 1.4.11 for the border.
- **The focus indicator is not suppressed.** No `outline: none` anywhere in the stylesheet; the UA default focus ring survives on `.retry` (2.4.7 passes).
- **The spinner is correctly hidden from AT.** `:36` — decorative, empty, `aria-hidden="true"`. Correct, not a finding.
- **Native semantics throughout.** Real `<button type="button">` (`:28`), real `<ul>`/`<li>` (`:48-50`), real `<h2>` (`:27`). No `div role="button"` anti-pattern.
- **Region labelling is correct.** `<section aria-labelledby="activity-heading">` at `:25` correctly references `:27`, producing a properly-named `region` landmark.
- **`<header>` inside `<section>`** (`:26`) is scoped to a sectioning element and does **not** create a conflicting `banner` landmark. Not a finding.
- **`role="status"` plus `aria-live="polite"`** at `:35` is redundant (status has implicit polite) but harmless and arguably defensive. Not a finding.

---

## Multi-Perspective Notes

**Screen reader user** — HIGH alarm. This is where the component fails. Landmark and heading structure are good, so orientation works: they reach "Account Activity, region, heading level 2." From there they get silence in all three states — loading (M2), error (C1), and ready (M1). Empty-ready and error are perceptually identical (M4). Safari/VoiceOver additionally loses the item count (`list-style: none`). Every finding above at CRITICAL or MAJOR lands on this perspective.

**Keyboard-only user** — LOW alarm, and genuinely the strongest perspective. Tab order is trivially linear (Retry is the sole interactive control). The button is native, so Enter and Space both activate it. No focus trap, no `outline: none`, no `visibility: hidden` on focusable content, no modal to restore focus from. The line-148 decision to keep Retry mounted is *correct* keyboard design and I want to credit it explicitly — the failure is that it was treated as sufficient for screen reader users too. One gap: pressing Retry during load does nothing perceivable (M3).

**Low vision user (200% zoom, high contrast, magnifier)** — LOW alarm. All contrast ratios pass with margin (see Verified Clean). `max-width: 640px` with `margin: auto` (`:70-71`) reflows without horizontal scroll. The `.panel-header` flex row (`:77-79`) will crowd at very high zoom but has only two children, so it degrades gracefully. Under a magnifier the C1/M4 failure has a distinct flavor worth naming: with a narrow viewport onto the page, a user parked on the Retry button will not see the error text appear or the spinner vanish — they get the same silent-change problem as a screen reader user, for different reasons. Windows High Contrast Mode will drop `.spinner`'s `border-top-color` distinction, but since the spinner is `aria-hidden` decoration and the text label carries the meaning, that is acceptable.

**Cognitive accessibility** — MEDIUM alarm. The error copy is above average: it states the problem *and* suggests an action, which many implementations skip. Against that: pressing Retry during load gives zero feedback (M3), which is the single most reliable way to make a user doubt the interface; the empty state is a blank box with no explanation (M4); and the connection advice is wrong for auth or server failures, potentially trapping a user in a retry loop they cannot escape (Minor 5). No timeouts and no destructive actions, so 3.3.4 and timing criteria are not engaged.

---

## Verdict Justification

**REVISE.** One CRITICAL and four MAJOR findings, all converging on a single missing mechanism — a persistent, unconditionally-mounted live region — which means the remediation is small, well-scoped, and does not require restructuring the component. The semantic foundation, native element usage, contrast, and keyboard behavior are all sound and should be preserved as-is. This is not REJECT: nothing here is misarchitected, and the author's focus decision at `:148` is right. It is not ACCEPT-WITH-RESERVATIONS: shipping as-is means a screen reader user can silently conclude a financial account is empty when the request actually failed, and that is a correctness failure, not a friction point.

**To upgrade to ACCEPT**, the following must land together — a partial fix here reproduces the original bug in a new location:
1. A persistent live region outside every conditional branch, announcing all three states, with a transaction count on success (fixes C1, M1, M2).
2. `aria-disabled` on Retry during load plus an early return in `load()` (fixes M3).
3. An explicit empty state branched on `transactions.length` (fixes M4).

**Severity recalibrations performed:**
- **C1 held at CRITICAL** after considering the browse-mode mitigation. Downgrade rejected: the mitigation requires the user to know to go looking, and nothing signals that a change occurred. The realistic worst case is a wrong conclusion about financial data, not an inconvenience.
- **M4 held at MAJOR** despite also affecting sighted users. The a11y-specific harm is the *ambiguity with the error state*, which only exists for users without the visual channel.
- **`aria-busy` suppression downgraded from MAJOR to MINOR + Open Question.** I could not establish at HIGH confidence that ancestor `aria-busy` gates a descendant live region — the live region root here is `.loading` itself, which is not busy. Reporting the unverified version at MAJOR would have been alarmist. It is filed as a coherence MINOR plus an explicit measurement question.
- **Reduced motion and target size deliberately NOT scored as violations.** 2.2.2's essential-content exception covers the spinner, and the 33px button passes 2.5.8 (AA) — failing only the AAA 2.5.5. Both are listed as enhancements. Flagging either as a finding would have been a manufactured violation.

**Test evidence**: none was available for this review. No axe-core scan, no Playwright keyboard run, no `agent-browser` trace, no `virtual-screen-reader` spoken-phrase log. Every finding above is design reasoning from source, not measured fact. The findings most improved by measurement are M2 (does the retry-remount announce on NVDA/JAWS?) and Open Question 1 (does ancestor `aria-busy` suppress?) — both are `virtual-screen-reader` component-assertion questions and could be settled in a Vitest suite without deploying anything. Note that the keyboard findings here are thin precisely *because* keyboard behavior is good; they would not need Playwright to confirm.

---

## Open Questions (unscored)

1. **Does `aria-busy="true"` on `.panel-body` (`:33`) actually suppress the announcement of the live region nested inside it at `:35`?** The ARIA processing model attaches busy-gating to the live region root, and the live region root here is `.loading` — which is not itself busy. Screen reader implementations vary in whether they walk ancestors. Settling this needs a `virtual-screen-reader` spoken-phrase assertion, not reasoning. Noting the known blind spot: VSR does not model `aria-busy`, so this specific question may need a real-AT probe rather than the component lane. Reported as MINOR on coherence grounds only.

2. **Is `transactions === []` a reachable state?** M4 assumes the API can return an empty array for a valid account. If the endpoint 404s or errors on empty accounts instead, M4 collapses to a non-issue. Requires the API contract.

3. **Is more than one `AccountActivityPanel` rendered per page?** The `accountId` prop (`:6`) suggests a multi-account context, which would make the hardcoded `id` at `:27` a real collision. The developer can settle this immediately; `useId()` makes the question moot either way.

4. **What is the page-level heading context for the `<h2>` at `:27`?** I can only see the component. If it sits under an `<h1>` the hierarchy is correct; if it is dropped into a page whose nearest ancestor heading is an `<h3>`, it is a skip. Not scoreable at component scope.

5. **Is `<section>` at `:25` the right container?** It produces a `region` landmark, which is appropriate for a standalone panel but adds landmark noise if a page renders many of these. A design question, not a defect.

---

## Provenance

Files read: exactly one.

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt-siblings-rows/prompts/async-retry-error-unannounced.blind.md` — read in full (149 lines), via a single `Read` call.

No other file was opened. No `Grep`, `Glob`, or `Bash` call was made in this session — no git, no repository search, no `evals/suites/` access, no `*.metadata.yaml` or `*.rubric.yaml`. No browser or test tooling was invoked. All line citations refer to the line numbers of the file above, cited as `async-retry-error-unannounced.md:<line>` per instruction. Contrast ratios were computed by hand from the hex values at `:93-94`, `:107`, and `:125` using the WCAG relative-luminance formula; they are calculated, not measured by a tool, and assume a white page background (the stylesheet declares no background on `.activity-panel`).