I'll read the fixture file and run the full protocol.

---

## VERDICT: ACCEPT

**Overall Assessment**: This component's accessibility design is coherent and the reasoning behind it is correct — the persistent-live-region pattern, the status/alert sibling split, the header-anchored Retry control, and the `role="list"` restoration are all deliberate choices that hold up under scrutiny. I found no CRITICAL or MAJOR defects. The one real gap is that the component's central invariant ("text is written into the regions rather than mounted with them", `async-retry-recovery-clean.md:112`) is guaranteed only across state *transitions*, not at initial mount — an unstated dependency on parent behavior the file explicitly places out of scope.

---

**Phase 0 — Test evidence**: None attached. No axe run, no Playwright/agent-browser keyboard trace, no `virtual-screen-reader` spoken-phrase log. That matters here more than usual: this component's entire accessibility argument is about *what gets announced*, which is precisely what VSR component assertions measure. Every announcement claim below is design reasoning, not measured fact. Scope is component-level, so no WCAG-EM or ICT-baseline citations apply.

---

**Pre-commitment Predictions** (made before detailed reading, from "async panel with retry"):

| # | Predicted | Outcome |
|---|---|---|
| 1 | Live region mounted with its content → not announced | **Partially confirmed** — only at initial mount (Minor 1) |
| 2 | Retry control unmounts during loading → focus destroyed | **Refuted** — button is in the header (`:13`), outside the swapping region |
| 3 | Spinner announced as junk / loading state visual-only | **Refuted** — `aria-hidden` (`:25`) + text in the same region |
| 4 | Error not programmatically tied to the recovery control | **Confirmed as a soft gap** — no `aria-describedby` (Enhancement 1) |
| 5 | Empty result announces nothing, or "0" | **Refuted** — explicit message (`:32`) |
| 6 | Focus indicator suppressed or under-contrast | **Refuted** — `:focus-visible` present (`:79-82`), ~5.2:1 |

I was wrong on four of six. That is the useful signal: this file resists the defect classes its component type usually carries.

---

## Critical Findings

None.

## Major Findings

None.

---

## Minor Findings

**1. The persistent-region guarantee does not cover initial mount.** `async-retry-recovery-clean.md:22` and `:40`

The regions are persistent across *state changes* — but on the component's first mount, `<div role="status">Loading activity…</div>` (or `<div role="alert">We couldn't load…</div>`) enters the DOM as a single unit, content already inside. That is the exact anti-pattern the file's own comment warns against (`:19-21`) and claims to have solved (`:112`, `:118`). A live region must be present in the accessibility tree *before* its content changes for the change to be announced reliably.

- **User group**: Screen reader
- **WCAG**: 4.1.3 Status Messages
- **Confidence**: MEDIUM — the defect is real; whether it *occurs* depends on the parent, which `:6-8` and `:111` place out of scope. If the parent mounts the panel in a neutral state and then transitions to `loading`, this never fires.
- **Why it isn't MAJOR (Realist Check)**: the missed announcement is of a transient, low-stakes state, and every subsequent transition works. **Mitigated by**: the error text remains visible and in the DOM, reachable by browsing rather than waiting for the announcement.
- **The sharper edge**: mounting directly into `error` (SSR-rendered failure, cached error, error boundary re-render). A missed `role="alert"` on mount is the failure mode the file itself cites as the reason for the design.
- **Fix**: state the parent-side invariant explicitly — mount the panel before the request starts, so `status` is neither `loading` nor `error` on first paint. Verify with `virtual-screen-reader` using the persistent-container assertion shape (a mount-with-content alert reads silent in VSR by design; asserting on that silence without the structural check would be a false positive).

**2. Hardcoded `id="activity-heading"`.** `async-retry-recovery-clean.md:10, :12`

A presentational, reusable component (`:6`) with a fixed DOM id. Two instances on one page produce duplicate ids, and `aria-labelledby` resolves to the first — both panels announce as the same region.

- **User group**: Screen reader
- **WCAG**: 1.3.1 Info and Relationships (the label relationship becomes ambiguous). Note: not 4.1.1 — that criterion was removed in WCAG 2.2.
- **Confidence**: HIGH that the id is static; MEDIUM that multiple instances occur.
- **Mitigated by**: an account activity panel is typically singular per view. Downgraded from MAJOR on that basis.
- **Fix**: `const headingId = useId()`.

---

## Enhancements

**1. Panel state is announced once but not discoverable on focus.** `async-retry-recovery-clean.md:13, :40`

The Retry button is in the header, so it precedes both regions in reading order. A user who tabs to Retry — arriving after the alert fired, or returning to the panel — hears "Retry, button" with no indication the panel is in a failed state.

This is the cost side of a trade-off the file made deliberately and documented (`:114`, `:123`): focus stability was bought by placing the control *before* the context that explains it. Both placements have a price; this one is the cheaper price, and it's resolvable without moving the button.

Adding `aria-describedby="panel-error-id"` to the button resolves the tension — the description is empty and ignored in non-error states, and in the error state Tab announces "Retry, button, We couldn't load your activity. Select Retry to try again." **Mitigated by**: the error text is visible and only two nodes later in reading order, so a browsing user reaches it immediately. Not a barrier — which is why this is an enhancement and not a finding.

**2. Retry's accessible name is context-free.** `async-retry-recovery-clean.md:13`

"Retry" alone is ambiguous in a screen reader's button list on a page with several async panels (WCAG 2.4.6 Headings and Labels). **Constraint on the fix**: any `aria-label` must still contain the visible string "Retry" to satisfy 2.5.3 Label in Name, and to keep the error text's "Select Retry" (`:42`) matching what the user hears — `aria-label="Retry loading account activity"` satisfies both.

**3. `.retry` declares no `font-size` or `font-family`.** `async-retry-recovery-clean.md:72-77` — buttons don't inherit these from the UA stylesheet, so the label renders at ~13.3px Arial while the panel body uses the page font. A legibility nit for low-vision users. Target size still passes: ~29 × ~70px, above the 24×24 minimum (WCAG 2.5.8 AA).

---

## What's Missing

- **The parent-side contract for mount timing** is the load-bearing assumption and it is unstated. See Minor 1.
- **No background-color is declared** anywhere in the CSS (`:64-107`). Every contrast figure below is computed against an assumed `#fff`; on a tinted panel background these are unverified.
- **The fifth state.** `:111` enumerates four. If `status` is `undefined`, `idle`, or anything else, both regions render empty and the panel is a heading plus a Retry button with no explanation of what it does or why there's nothing there. Defensible if the parent's type contract is exhaustive — but the file doesn't say so.
- **"No activity in this period"** (`:32`) — the period is named nowhere in this component and no date context is rendered. Cognitive gap for a user who hears only this panel.
- **No `aria-describedby` from Retry to the error region** — see Enhancement 1.

---

## Multi-Perspective Notes

**Screen reader**: Structurally sound. `<section aria-labelledby>` (`:10`) produces a named `region` landmark. `<header>` at `:11` is *not* a `banner` landmark — `banner` maps only when the element is scoped to `<body>`, so there's no nested-landmark defect here (checked specifically; flagging one would have been a false positive). `role="list"` at `:47` is a correct and necessary WebKit workaround, not redundant ARIA. `role="status"` + explicit `aria-live="polite"` is redundant but harmless. `role="alert"` carries implicit `aria-atomic="true"`, so its omission at `:40` is correct. The spinner is `aria-hidden` inside an `aria-atomic` region, so the computed announcement is "Loading activity…" — correct. Announcement gaps: initial mount (Minor 1); repeated identical failures (Open Question 1).

**Keyboard-only**: One tab stop, native `<button type="button">`, Enter and Space work by default, no trap, no `tabindex` manipulation anywhere. The button never unmounts, so no state change destroys focus position — the file's claim at `:114` holds. `:focus-visible` is defined without any `outline: none` elsewhere, so browsers lacking `:focus-visible` still show the UA ring. No focus management is needed because nothing moves. Clean.

**Low vision (200% zoom, high contrast)**: Computed contrasts against assumed white — `.panel-status` #475467 ≈ **7.7:1** (AAA), `.panel-error` #b42318 ≈ **6.6:1** (AA), `.retry` #0b5fff ≈ **5.2:1** (AA text and 3:1 non-text for the border and the focus outline). All computed from hex, not measured. No fixed heights or absolute positioning, so reflow should hold. `prefers-reduced-motion` is honored (`:98-100`) and the static spinner losing its meaning is covered by the adjacent text carrying the message. Forced-colors mode: no `outline: none`, explicit colors get overridden by the UA — nothing to fix.

**Cognitive**: The error names its remedy in words that match the visible control (`:42` ↔ `:13`) — this is the single best decision in the file, and it's the one most implementations skip. The empty state is a sentence, not a blank panel. Weak spots: "this period" is unanchored, and there's no distinction between a first failure and a repeated one.

---

## Verdict Justification

ACCEPT. Nothing here blocks or significantly degrades access for any of the four perspectives, and the design decisions are internally coherent rather than incidentally compliant — the file reasons about *why* each choice is made, and the reasoning is correct.

**Severity recalibrations**: Minor 2 (duplicate id) was initially MAJOR, downgraded on single-instance likelihood. Enhancement 1 was initially MINOR, downgraded because the error text is fully reachable in reading order — inflating it would have been review momentum, not user impact. Minor 1 was held at MINOR rather than raised to MAJOR: the missed announcement is transient and the content stays visible and browsable.

**Calibration note**: I checked four things that a pattern-matching pass would have flagged as defects and that are actually correct — the nested `<header>` (not a landmark), `role="list"` on a `<ul>` (not redundant), the missing `aria-atomic` on the alert (implicit), and `:focus-visible` without a `:focus` fallback (no suppression elsewhere). Reporting any of these would have been a false positive.

**For an upgrade to unconditional confidence**, not a higher verdict: run `virtual-screen-reader` component assertions on the four documented states plus the mount-into-`loading` and mount-into-`error` paths, using the persistent-container pattern. That converts every announcement claim in this review — mine and the file's — from reasoning to measurement.

---

## Open Questions (unscored)

1. **Repeated identical failures.** `:42` renders the same string on every error. Some screen readers deduplicate consecutive identical live-region announcements. The intervening polite "Loading activity…" probably breaks the sequence, but I have no measurement and won't assert it. Testable with VSR.
2. **Initial/idle state.** What does the parent pass before the first request resolves? Determines whether Minor 1 fires and whether the fifth-state gap is real.
3. **`{t.amount}` formatting** (`:51`). A raw negative number announces as "minus 42.1" or "hyphen 42.1" depending on the AT. The parent supplies the value, so this may already be a formatted string — out of scope for a presentational component, but worth confirming upstream.
4. **`transactions` is dereferenced without a guard** (`:30`). A robustness concern, not an accessibility one — noted and not scored.

---

## Provenance

I read exactly one file:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt-siblings-rows/prompts/async-retry-recovery-clean.blind.md`

No other file was read. No `evals/suites/` path, no `*.metadata.yaml` or `*.rubric.yaml`, no grep or glob of the repository, no git commands, no web fetches, no subagents. Contrast ratios were computed by hand from the hex values in the file using the WCAG relative-luminance formula against an assumed `#fff` background; no measurement tool was run.