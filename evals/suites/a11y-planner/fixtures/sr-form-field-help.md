# Fixture: Complex Form with Field-Level Help Text and Progressive Disclosure

## Feature Description

You're planning accessibility for a multi-section account registration form on a financial services platform. The form has these characteristics:

- **Standard fields** (Name, Email, Password): each has a static help text string beneath the input ("Must be 8+ characters, include one number")
- **Conditional fields**: selecting "Business Account" from an account type radio group reveals a Company Name field and Tax ID field; selecting "Personal Account" hides those fields. The hidden/revealed fields use a CSS `display: none` / `display: block` toggle.
- **Expandable help**: a "?" icon button next to the Tax ID field expands an inline help section ("What is a Tax ID? An Employer Identification Number (EIN)…") when clicked. The help text expands inline below the field, not in a tooltip or modal.
- **Inline validation errors**: shown after blur, co-located with each field ("Email is already in use")
- **Field dependency**: the Phone field has a "Same as primary phone" checkbox that, when checked, disables the Mobile Phone field and populates it with the primary phone value
- **Ambiguity**: The design spec does not specify whether help text should be linked to the input via `aria-describedby` immediately (so it's read on focus) or via a different mechanism. Engineering wants to know: should the help text always be announced on field focus, or only when the user asks? The plan must make and justify a decision.

## Context

- **Platform:** React form with Formik for state management; no existing accessibility implementation
- **Existing code:** No — this is a new form. Design specs exist with static wireframes but no ARIA specification.
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Help text announcement strategy, conditional field announcements, expandable help toggle, error vs help disambiguation, disabled field state
- **Constraints:** Help text visibility is ambiguous in spec — must decide whether to use aria-describedby (always announced) or a different pattern; conditional fields must announce when they appear/disappear; expandable help must communicate open/closed state; error and help text must be distinguishable to AT users

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- Help text association strategy: decide and justify `aria-describedby` (announced on focus) vs on-demand pattern
- Help text timing: when should help be announced relative to the field label?
- Conditional field announcements: when "Business Account" is selected, how does AT know new fields appeared?
- `display: none` behavior: fields hidden with `display: none` are correctly removed from accessibility tree — confirm this is the right approach
- Expandable help toggle: `aria-expanded` on the "?" button, `aria-controls` pointing to the help region, focus stays on button (help expands below)
- Error vs help disambiguation: when both an error and help text exist, AT must announce both in the correct order and distinguish them (error first, then help guidance)
- Disabled field state: `aria-disabled="true"` vs HTML `disabled` attribute — which to use and why
- `role="group"` / `<fieldset>` for the conditional Business fields that appear together
- WCAG citations with reasoning for each decision
- Testing strategy
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is an **AMBIGUOUS** difficulty fixture — the core ambiguity is the help text announcement strategy: `aria-describedby` announces help on every focus, which may be verbose for experienced users; alternatives (announcer-on-demand, tooltip-triggered) each have tradeoffs. The plan must make an explicit, justified decision. Expected plan length: 3-5 pages (varies with how thoroughly ambiguity is addressed). Focus on:

1. **Resolve the aria-describedby decision explicitly**: For a financial services form where help text contains actionable instructions (password rules, Tax ID explanation), `aria-describedby` is the right choice — it ensures critical guidance is not missed. Document this reasoning.
2. **Announcement order**: NVDA/JAWS read linked descriptions after the input's label and type. Multiple `aria-describedby` IDs are announced in DOM order — put error ID first, help text ID second: `aria-describedby="email-error email-help"`.
3. **Conditional fields**: use `aria-live="polite"` region surrounding the conditional section, OR move focus to the first revealed field. Both are valid — plan must choose one and justify.
4. **Expandable help toggle**: `<button aria-expanded="false" aria-controls="tax-id-help">What is a Tax ID?</button>` — the help section does NOT need `aria-live`; focus stays on button; AT discovers the expanded content via `aria-controls`.
5. **Disabled field**: use HTML `disabled` (removes from tab order entirely) not `aria-disabled="true"` (keeps in tab order but marks as disabled). For the "Same as primary phone" auto-fill case, `disabled` is correct.

## What Success Looks Like

An excellent plan would:
- ✓ Make an explicit, justified decision about `aria-describedby` for help text (not leave it open)
- ✓ Document the multiple-ID `aria-describedby` order rule: error ID before help text ID for combined announcements
- ✓ Confirm `display: none` correctly removes fields from accessibility tree — no additional ARIA needed to hide
- ✓ Choose and justify a conditional field announcement strategy (focus move to first field, or live region around the section)
- ✓ Specify `aria-expanded` + `aria-controls` on the expandable help button with correct behavior (expand does not move focus)
- ✓ Distinguish HTML `disabled` from `aria-disabled` — recommend `disabled` for the auto-filled Phone field with explanation
- ✓ Plan `<fieldset>/<legend>` for the Business Account conditional group ("Business Details")
- ✓ Note the ambiguity explicitly and document the resolution
- ✓ Cite WCAG 3.3.2 (Labels or Instructions), 3.3.1 (Error Identification), 1.3.1 (Info and Relationships), 4.1.2 (Name, Role, Value)
- ✓ Include testing: verify NVDA reads help text after label; verify error announcement order; verify conditional reveal is announced

## What Would Be Below Expectations

- ✗ Leaving the `aria-describedby` decision as "it depends" without resolving it — the ambiguity must be closed
- ✗ No announcement order plan for error + help text — just saying "link both with aria-describedby" without specifying ID order
- ✗ Using `aria-hidden="true"` on conditional fields instead of `display: none` — redundant and can cause issues in some AT
- ✗ Applying `aria-live` to the expandable help section — the help region is not a live region; `aria-expanded`/`aria-controls` is the correct pattern
- ✗ Using `aria-disabled="true"` for the auto-filled Phone field without justifying why it should stay in tab order (it shouldn't — use HTML `disabled`)
- ✗ No `<fieldset>/<legend>` for the Business Account conditional group
- ✗ No WCAG 3.3.2 citation for help text strategy
- ✗ Testing plan that only covers error messages — must also verify help text announcement and conditional field reveal
