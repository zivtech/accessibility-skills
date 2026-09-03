<!-- GT-16 blind draw: condition=baseline (no skill slice), fixture=dialog-dismiss-recipe-clean, fixture revision 1 (cbd2f41), model=opus, agent=general-purpose, 2026-09-03. Verbatim; recovered from the agent's session transcript. Read only prompts/dialog-dismiss-recipe-clean.blind.md. -->

VERDICT: REVISE

The two filed PASS rows are internally well-formed — the `source` line references resolve exactly (spec line 32 = the 2.1.1 assertion, spec line 36 = the focus-return assertion, stdout's `:9:1` = the `test(` declaration), and the Tab sequence in `trace.json` is exactly what the component's DOM order and wrap logic predict. But the bundle contains one artifact that provably could not have been produced by the component under test, and one recorded outcome that the component's own code path contradicts. Both need resolving before these rows are filed as evidence.

---

## MAJOR — `screen-reader-census.json` reading order contradicts the component DOM

**dialog-dismiss-recipe-clean.blind.md:236**

The census places the close button (`div.dialog > header > button`) at index 1 and the `<h2 id="delete-title">` at index 2 (dialog-dismiss-recipe-clean.blind.md:237). The component renders the heading **first**: `<h2 id="delete-title">` at dialog-dismiss-recipe-clean.blind.md:97, the close button at dialog-dismiss-recipe-clean.blind.md:98. Reading order follows DOM order, and nothing in the CSS reorders them — `.dialog__header` is `display: flex; justify-content: space-between` (dialog-dismiss-recipe-clean.blind.md:138-142) with no `order` and no `row-reverse`, so visual order matches DOM order too.

This is not a sorting convention: the census is otherwise in strict DOM order (paragraph before Cancel before Delete), so there is no "focusables first" rule that would explain the inversion. Exactly one pair is swapped.

Why it matters for a benchmark row: the census is a recorded artifact declared to follow the a11y-test verification evidence contract (dialog-dismiss-recipe-clean.blind.md:281). If it misreports reading order for this component, it was not faithfully captured from it — and that is contagious to `trace.json`, which is the sole basis for both filed findings. A downstream reviewer reading only the census would conclude the close control precedes the heading and could file a spurious 1.3.2 finding, or credit a "close-first" design decision that does not exist.

*Not claiming:* this does not invalidate the accessible name the recipe took from the census (dialog-dismiss-recipe-clean.blind.md:189-190). "Close dialog" matches `aria-label` at dialog-dismiss-recipe-clean.blind.md:98, so the recipe's use of the census is correct even though the artifact is wrong.

---

## MAJOR — `trace.json` step 3 records a focus return the component cannot perform at that moment

**dialog-dismiss-recipe-clean.blind.md:227**

`finish()` (dialog-dismiss-recipe-clean.blind.md:17-20) calls `setConfirming(null)` and then, synchronously in the same event handler, `triggerRef.current?.focus()` (dialog-dismiss-recipe-clean.blind.md:19). The trigger lives inside `#app-root` (dialog-dismiss-recipe-clean.blind.md:28), which carries `inert` for as long as `confirming` is truthy (dialog-dismiss-recipe-clean.blind.md:24).

React 18.3 batches a state update inside a discrete event and flushes it *after* the handler returns, so at the instant `.focus()` runs, `#app-root` still has `inert=""` in the DOM. Inert content is not focusable, and a programmatic `focus()` on an inert element is a no-op. The dialog then unmounts, removing the currently-focused close button, and focus falls to `<body>` — not to the trigger.

The component makes the same move correctly on the way in: it restores focus via `useEffect` (dialog-dismiss-recipe-clean.blind.md:62-64), i.e. post-commit. The dismissal path is the one place it does it pre-commit. That asymmetry is where the code and the trace disagree.

So `trace.json` step 3's `"focus_after": { "role": "button", "name": "Delete report" }` and the `kbd-dialog-close-dismiss-focus-return` PASS (dialog-dismiss-recipe-clean.blind.md:258-265) rest on a behavior the component code does not predict. One of the two is wrong. Either the run was not against this code, or the timing analysis is. It cannot be filed until that is settled — re-run with `focus_after` captured from the accessibility tree after the React commit, or fix the ordering (restore focus in a `useEffect` cleanup, or after the unmount commit) and re-record.

*Confidence:* this is where my confidence drops — roughly 75-80%. It is a static inference about React flush timing and inert focus-blocking argued against a recorded browser trace, and a trace is normally primary. I am not claiming the trace is fabricated; I am claiming the two are irreconcilable as filed. Note also that `expect(trigger).toBeFocused()` (dialog-dismiss-recipe-clean.blind.md:203) auto-retries for the default 5s, so a *late* focus return would still have passed — the recipe cannot distinguish "returned immediately" from "returned eventually," which is precisely the axis in dispute.

---

## MINOR — finding 2 cites one assertion for a two-part claim

**dialog-dismiss-recipe-clean.blind.md:262**

The message asserts two things — "hid the dialog **and** returned focus to the trigger" — but `source` (dialog-dismiss-recipe-clean.blind.md:264) points only at spec line 36, the focus assertion (dialog-dismiss-recipe-clean.blind.md:203). The dismissal half is proven by spec line 35 (dialog-dismiss-recipe-clean.blind.md:202) and has no cited source. Split the finding, or cite both assertion lines.

---

## MINOR — hard-coded sleep inside the Tab loop makes the "press 2" evidence timing-dependent

**dialog-dismiss-recipe-clean.blind.md:196**

`await page.waitForTimeout(100)` after each Tab is an arbitrary wait. It is what makes `reached` (dialog-dismiss-recipe-clean.blind.md:197) and therefore the "close control focused on Tab press 2" message (dialog-dismiss-recipe-clean.blind.md:253) a function of wall-clock timing rather than of a settled focus state. Use `expect.poll` on the active element, or drop the sleep and let the locator assertion auto-wait — the loop already has a bounded escape at 6 presses.

---

## MINOR — the recipe cannot tell "dismissed" from "deleted and dismissed"

**dialog-dismiss-recipe-clean.blind.md:201**

Expected Behavior requires that the header close control dismiss **without deleting** (dialog-dismiss-recipe-clean.blind.md:273). After pressing Enter on the close control, the recipe asserts only that the dialog hid and focus returned. If the close button at dialog-dismiss-recipe-clean.blind.md:98 were miswired to `onConfirm` instead of `onCancel`, every assertion in this test would still pass while the report was destroyed — `onConfirm` also calls `finish()` (dialog-dismiss-recipe-clean.blind.md:48-51), producing an identical dialog-hidden + focus-returned signature.

The component is currently wired correctly, so this is a coverage gap, not a false claim — which is why it is MINOR rather than MAJOR. But for a destructive-confirmation dialog it is the cheapest high-value assertion available: check the report is still in `.report-list`, or that `onDelete` was not called.

---

## ENHANCEMENT — `FOCUSABLE` admits disabled controls that would silently break the trap

**dialog-dismiss-recipe-clean.blind.md:11**

The selector excludes disabled buttons (`button:not([disabled])`) but not disabled `input`, `select`, or `textarea`. If a disabled input were ever the first or last match, `first.focus()` / `last.focus()` (dialog-dismiss-recipe-clean.blind.md:76-82) would be a no-op and Tab would escape the dialog with `preventDefault` already called — focus stranded. Not reachable with the current three-button markup, so it is latent, not a live defect. Add `:not([disabled])` to each, and consider filtering on visibility.

---

## ENHANCEMENT — the cycle bound is a magic number tied to a comment

**dialog-dismiss-recipe-clean.blind.md:192**

"Three focusable controls in the dialog; six presses is two full cycles" is true today, but the `6` at dialog-dismiss-recipe-clean.blind.md:194 is not derived from anything the test measures. Add a fourth control and the bound silently stops meaning "two cycles." Compute it from `dialog.getByRole('button').count()`.

---

## ENHANCEMENT — declared-out-of-scope dismissal routes

**dialog-dismiss-recipe-clean.blind.md:272**

Escape, Cancel, and the Shift+Tab reverse wrap are all specified in Expected Behavior (dialog-dismiss-recipe-clean.blind.md:272-273) and all unexercised. The recipe scopes itself explicitly to the close control (dialog-dismiss-recipe-clean.blind.md:275), so this is not a defect against the recorded outcome — it is the obvious next recipe, and the Shift+Tab branch (dialog-dismiss-recipe-clean.blind.md:76-78) is currently the only untested half of the trap logic.

---

## What I am not flagging

Checked and sound, listed so the negative space is explicit: the Tab order in `trace.json` steps 1-2 is exactly what the DOM order and wrap logic produce from an initial focus on Cancel; the focus indicator (dialog-dismiss-recipe-clean.blind.md:155-158) clears 3:1 against both the white dialog and the red Delete button (#1a4fd1 on #fff ≈ 6.8:1), so 1.4.11 is met; the close control is 32×32 CSS px (dialog-dismiss-recipe-clean.blind.md:143-149), clearing SC 2.5.8's 24px minimum; `aria-modal` and `inert` are consistent because `.backdrop` is a sibling of `#app-root`, not a descendant; `toBeHidden()` on an unmounted locator is idiomatic and not a false pass here because `toBeVisible()` ran first; the `BASE_URL` guard (dialog-dismiss-recipe-clean.blind.md:171-174) correctly refuses to run against a synthetic fixture; and both WCAG mappings (2.1.1 for reachability, 2.4.3 for focus return) are defensible as filed.

---

## Provenance

- **File read:** `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe-clean.blind.md` (one `Read` call, complete file, 282 lines).
- **No other file was opened.** No `grep`, no `git`, no directory listing, no web access, no subagents, no skill invocations, no other tool calls of any kind.
- All line citations use that file's own line numbers as returned by the single read. Spec-file line numbers referenced inside `findings.json` `source` fields were resolved by counting within the fenced block beginning at line 168, not by opening any file.
- All reasoning about React 18.3 batching, `inert` focus semantics, Playwright assertion retry behavior, WCAG success criteria, and the sRGB contrast computation is from working knowledge, unverified against any external source in this session.