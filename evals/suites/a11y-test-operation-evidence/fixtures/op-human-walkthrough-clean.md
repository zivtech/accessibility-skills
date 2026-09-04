# Operation-evidence package — OP-RETURN + OP-FLASH + OP-AD (human-sourced)

You are reviewing the evidence package a person's walk-through produced for
three planned operations, per the human verification walk-through reference —
not a machine collector run. Decide whether the package is admissible as
evidence for the claims it makes, per the same five operation-evidence rules,
applied to human-sourced fields. Judge the evidence, not the underlying
component.

## Evidence package as submitted

**OP-RETURN — dismiss the Details dialog with Escape (claim: PASS).**
```yaml
- operation: OP-RETURN
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
  claim_boundary: "Focus returned to the trigger on this dialog at 3.4.0 with NVDA. Nothing about other dialogs, other AT, or 2.4.7 across the sample set."
```
A second confirmation, a different person on a later date:
```yaml
- operation: OP-RETURN
  closes: rem-focus-return-2c7f0a1b
  version: "3.4.0"
  session: 2026-09-05-MS-a
  tooling: "Chrome 141 + VoiceOver, keyboard only"
  before:
    reached_by: "Loaded the results view, Tab x5 to the 'Renew' row action, Enter to open the Details dialog"
    locus: "Details dialog open; focus on its heading 'Item details'"
    announced: "dialog, Item details, heading"
  action: "Escape"
  expected: "Dialog closes; focus returns to the row-action trigger"
  observed: "Dialog closed; VoiceOver announced 'Renew, button'; visible focus ring on that button"
  observed_via: announcement
  target_reached: exact
  disposition: PASS
  claim_boundary: "Second confirmation: different person, later date, different AT. Same trigger, same version."
```

**OP-FLASH — homepage carousel transition (claim: BLOCKED, attended and indeterminate).**
```yaml
- operation: OP-FLASH
  closes: rem-carousel-flash-9a41
  version: "3.4.0"
  session: 2026-09-02-JR-b
  tooling: "Chrome 141, no AT, unaided viewing, no flash-frequency analyzer available"
  media: "Homepage promo carousel, autoplaying, transition observed 0:00-1:30 across three full cycles"
  played: "Watched the carousel's autoplay transition continuously for the full 1:30, uninterrupted"
  seen: "Each slide change includes a brief bright flash; the alternation looked rapid across the full 1:30"
  adequacy: "Cannot determine by eye whether the transition crosses the general or red flash threshold; that call needs a flash-frequency analyzer reading, which was not available for this session"
  disposition: BLOCKED
  claim_boundary: "The transition was watched continuously for three full cycles at 3.4.0. Whether it exceeds the flash threshold is undecided without an analyzer reading — nothing about other carousels or other pages."
```

**OP-AD — audio description track for the training video (claim: FAIL).**
```yaml
- operation: OP-AD
  closes: rem-video-ad-inadequate-77c2
  version: "3.4.0"
  session: 2026-09-03-MS-c
  tooling: "Chrome 141, built-in player, headphones; no AT"
  media: "Product walkthrough video on the training page, 3:40, player id 'walkthrough'"
  played: "0:00-1:10 with the 'Described' track selected from the CC/AD menu; 2:00-2:30 again without it"
  heard: "With the track selected: silence over the 0:40-0:55 stretch, the same as without it; the second voice speaks only once, at 1:02, to read the chapter title. Without the track: silence over the same stretch."
  seen: "Menu lists 'Described'; the on-screen error code at 0:44 is not spoken in the primary audio, and the description track plays silence over that stretch instead of speaking it"
  adequacy: "The description track is present in the menu but does not describe the settings panel or the error code during the silent stretch — it plays silence where the visual information is missing. The description does not convey what the primary audio omits."
  disposition: FAIL
  claim_boundary: "Description present in the menu but inadequate for the 0:40-0:55 stretch at 3.4.0 — it does not speak the content a listener would otherwise miss. The 2:00-2:30 stretch confirms silence again without the track selected; nothing about other videos."
```

## What the walk asserts

OP-RETURN PASS (two confirmations, different people, different dates),
OP-FLASH BLOCKED (watched, undecided without an analyzer), OP-AD FAIL
(played with and without the track; the description is present but
inadequate).
