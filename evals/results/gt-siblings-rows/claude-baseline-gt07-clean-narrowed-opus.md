I'll read the file first.

---

## Verdict: ACCEPT

The live-region architecture is genuinely correct, not just plausible-looking. Both regions are persistent siblings, politeness matches urgency, focus is structurally protected, and the contrast values pass AA (I computed them, below). Nothing here rises to CRITICAL or MAJOR. Four findings, all MINOR/ENHANCEMENT.

Citations use the fixture's own convention (`async-retry-recovery-clean.md:<line>`); line numbering in the prompt file is 1:1 with it — the file's own claims cite `:22`, `:25`, `:31-32`, `:42`, `:47`, and every one lands on the element it names.

---

## Findings

### F1 — MINOR — 1.3.1 Info and Relationships — `async-retry-recovery-clean.md:50-51`

Payee and amount are adjacent sibling spans with nothing between them. JSX strips whitespace-only text containing a newline between elements, so the rendered DOM is literally `<span>Acme Corp</span><span>-$42.00</span>` — no space. `.txn-list` (`:102-106`) sets only `list-style/margin/padding`; there is no rule for `.txn-payee` or `.txn-amount`, so no flex, no gap, no separator.

A screen reader reads the `li` as one run: "Acme Corp-$42.00". Two distinct data points delivered as a single string, where the hyphen of a negative amount can read as part of the payee name.

Fix: `display:flex; justify-content:space-between; gap:1rem` on the `li`, or `{' '}` between the spans.

**Boundary:** this degrades sighted output identically — it is a layout bug with an a11y consequence, not an a11y-only defect. I'm rating it MINOR rather than MAJOR because the information is all present and order is stable; only the parsing is ambiguous.

### F2 — ENHANCEMENT — no SC failure — `async-retry-recovery-clean.md:22-27`, claim at `:118`

The claim that the persistent region "is what makes the announcements reliable" holds for *transitions* but not for the component's *initial* mount. If this panel first renders with `status === 'loading'`, the region and its text enter the accessibility tree in the same commit — exactly the mount-with-content case the comment at `:19-21` warns against. Whether that happens is decided by the parent, which the component's boundary statement (`:6`, `:111`) hands off without stating the requirement.

This is not a WCAG failure: an unannounced initial page-load state is reachable by reading, and 4.1.3 concerns status messages arising from a change, not first paint. But the fixture's claim as written is broader than what the code can guarantee alone. If the contract matters, it belongs in the Expected Behavior list: *the parent must mount this component before the request begins.*

### F3 — ENHANCEMENT — no SC failure — `async-retry-recovery-clean.md:31`

`` `Loaded ${transactions.length} transactions.` `` yields "Loaded 1 transactions." for a single result. Content quality, not conformance.

### F4 — ENHANCEMENT — no SC failure — `async-retry-recovery-clean.md:13`

Retry is present and enabled in all four states, including first load and success, with no failure to retry and no busy state. Two consequences:

1. A user arriving cold hears "Retry, button" with no antecedent — retry *what*, and did something fail?
2. Activating it during `loading` produces **no announcement at all**. The status region's text is already "Loading activity…" and re-rendering an identical text node fires no live-region update, so the activation has no perceivable result.

Not 4.1.3 — a status message *is* presented (the pre-existing loading text) — but the missing activation feedback is real. Options: name it "Refresh activity" outside the error state, or `aria-disabled="true"` during `loading`.

### F5 — ENHANCEMENT — 1.4.3 (unverifiable as shipped) — `async-retry-recovery-clean.md:64-70`

Contrast is fine **against white**, which the CSS never declares for `.activity-panel` or `.panel-body`. Computed vs `#fff`:

| Selector | Color | Ratio | AA |
|---|---|---|---|
| `.panel-status` | `#475467` | 7.7:1 | pass (also AAA) |
| `.panel-error` | `#b42318` | 6.6:1 | pass |
| `.retry` text + border | `#0b5fff` | 5.2:1 | pass (also 1.4.11 non-text, 3:1) |
| `:focus-visible` outline | `#0b5fff`, offset 2px onto page ground | 5.2:1 | pass 1.4.11 |

Only `.retry` declares its own `background: #fff` (`:75`). The two status colors inherit an undeclared ground. On a tinted or dark panel these numbers move. Worth pinning the panel background in the fixture so the ratios are self-contained.

---

## Screen reader trace, four states

**loading**
- *By transition* (from `error` or `ready`): the polite region's text changes, so AT announces "Loading activity…". The spinner is `aria-hidden` (`:25`) and contributes nothing; `aria-atomic="true"` makes the region read as one unit.
- *On initial mount*: likely silent — see F2. The user hears it only on reaching the region.
- Browsing: "Account Activity, region" → "Account Activity, heading level 2" → "Retry, button" → "Loading activity…" → (alert region empty, skipped).

**error**
- Transition from `loading`: the `role="alert"` region goes empty → "We couldn't load your activity. Select Retry to try again." Assertive, so it interrupts. The polite region empties in the same commit; a clearing produces no utterance, so there is no competing announcement.
- Focus is undisturbed. If the user pressed Retry, focus is still on Retry — they hear the failure while already standing on the control that fixes it, and the message names that control by its exact visible label (`:42` vs `:14`), so there is no label-hunting.
- **Repeat failure** (`error → loading → error`): the alert's text node is removed and re-inserted, so the second failure re-announces rather than going silent — the classic same-message-twice trap is avoided here by the intervening `loading` state, not by anything in this file. If the parent ever transitions `error → error` directly, it goes silent.
- Browsing: region → h2 → "Retry, button" → (status region empty) → the error sentence.

**ready, with transactions**
- Transition: "Loading activity…" → "Loaded 5 transactions." Polite, queued behind speech in progress, does not interrupt. `aria-atomic` re-reads the region whole.
- The list mounts *below* the announcement. Focus is not moved — correct; the user is told content arrived and navigates on their own terms.
- Entering the list: "list, 5 items". The explicit `role="list"` (`:47`) is doing real work — `list-style: none` (`:104`) causes WebKit to drop the implicit role, so without it a VoiceOver user loses the item count entirely.
- Each item: "Acme Corp-$42.00, 1 of 5" — run together, per F1.
- With exactly one result: "Loaded 1 transactions." (F3).

**ready, with none**
- Transition: "Loading activity…" → "No activity in this period." Polite. This is the state most implementations get wrong — silence, or "Loaded 0 transactions." Neither happens here.
- Browsing: region → h2 → "Retry, button" → "No activity in this period." No empty `ul`, so no stray "list, 0 items" (`:46` guards on length, not just status).
- The user hears "Retry, button" with nothing having failed (F4).

---

## What I am not claiming

- **No runtime evidence.** Every announcement above is derived from documented AT behavior applied to the static markup, not from a measured NVDA/JAWS/VoiceOver trace. F2 in particular is the kind of claim that should be settled by a real mount, not by reading.
- **Component scope only.** The parent that owns `status` is unread and unreadable from here. F2 and the `error → error` gap both live at that seam.
- **Contrast assumes a white ground** (F5).
- **The list is not exercised at scale.** No virtualization, no pagination, no `aria-busy` during refresh — none of which this fixture claims to cover.

One process note: the file supplies its own "Accessibility Features Present" list (`:116-126`) *inside* the blind prompt. That is a strong prior toward ACCEPT. I checked each of the eight claims against the code independently rather than reading the list as an answer key — claims 1 through 8 hold, with claim 1 overstated for initial mount (F2). If this fixture is meant to test false-positive resistance, the embedded claim list is a hint, and it undercuts what the blind condition is trying to measure.

## Provenance

Files read (one, in full, via the Read tool):

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt-siblings-rows/prompts/async-retry-recovery-clean.blind.md`

No other file was opened, no grep, no git, no skill invoked, no subagent spawned. Contrast ratios were computed by hand from the sRGB relative-luminance formula against `#ffffff`.