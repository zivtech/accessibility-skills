# Operation-evidence package — OP-ESC + OP-RETURN + OP-AD + OP-OPTION + OP-LABEL (human-sourced)

You are reviewing the evidence package a person's walk-through produced for
five planned operations from the same session. A package is mixed by
default — decide admissibility for each operation independently, per the same
five operation-evidence rules applied to human-sourced fields; one
operation's evidence can stand while another's fails in the same package.
Judge the evidence, not the underlying component.

## Evidence package as submitted

**OP-ESC — dismiss the Details dialog with Escape (claim: PASS).**
```yaml
- operation: OP-ESC
  closes: rem-focus-return-2c7f0a1b
  version: "3.4.0"
  session: 2026-09-02-JR-a
  tooling: "Firefox 143 + NVDA 2026.1, keyboard only"
  before:
    reached_by: "Loaded the results view, Tab x5 to the 'Renew' row action, Enter to open the Details dialog"
    locus: "Details dialog open; focus on its heading 'Item details'"
    announced: "dialog, Item details, heading level 2"
  action: "Escape"
  expected: "Dialog closes; focus returns to the row-action trigger"
  observed: "Dialog closed; NVDA announced 'Renew, button'; visible focus ring on that button"
  observed_via: announcement
  target_reached: exact
  disposition: PASS
  claim_boundary: "Focus returned to the trigger on this dialog at 3.4.0 with NVDA. Nothing about other dialogs or 2.4.7 across the sample set."
```

**OP-RETURN — focus return to the Renew dialog trigger, a second finding on the same page (claim: PASS).**
- "Checked the Renew dialog; focus return works fine now — J.R."

That is the entire record — no `before`, no `action`, no `observed` detail,
and no `session`.

**OP-AD — audio description track for the training video (claim: PASS).**
- "The player's CC/AD menu lists a 'Described' track for the training video — J.R."

Nothing was played and nothing was heard.

**OP-OPTION — nested option state inside the filter combobox (claim: PASS).**
- "Tabbed to the filter and the highlighted option's selected state looked right — J.R."

No mapping is cited for how the option itself, rather than the combobox
owner, was reached.

**OP-LABEL — accessible name of the row-action button (claim: PASS).**
```yaml
- operation: OP-LABEL
  closes: rem-renew-button-name-51e0c9a7
  version: "3.4.0"
  session: 2026-09-02-JR-a
  tooling: "Firefox 143 + NVDA 2026.1, keyboard only"
  before:
    reached_by: "Loaded the results view, Tab x4 to the first row's action group"
    locus: "Focus on the first row-action control, before the 'Renew' control"
    announced: "button"
  action: "Tab"
  expected: "NVDA announces 'Renew, button' for the row action"
  observed: "As expected"
  observed_via: announcement
  target_reached: exact
  disposition: PASS
  claim_boundary: "Confirms the accessible name at 3.4.0 with NVDA. Nothing about other rows or other AT."
```

## What the walk asserts

OP-ESC PASS, OP-RETURN PASS, OP-AD PASS, OP-OPTION PASS, and OP-LABEL PASS —
closing out all five operations as passing confirmations from the same walk.
