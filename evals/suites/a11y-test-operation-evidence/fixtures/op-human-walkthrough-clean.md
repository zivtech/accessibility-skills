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

**OP-FLASH — homepage carousel transition (claim: BLOCKED).**
```yaml
- operation: OP-FLASH
  closes: rem-carousel-flash-9a41
  version: "3.4.0"
  session: 2026-09-02-JR-b
  tooling: "Chrome 141, no AT, unaided first look; no flash-frequency analyzer available"
  media: "Homepage promo carousel, autoplaying, slide transition at the top of the results view"
  expected: "Slide transitions do not flash more than three times in any one second, or stay below the general and red flash thresholds"
  played: "One capped first look at a single slide change, about two seconds, then looked away; no further attendance"
  seen: "The one slide change included a brief bright flash and a rapid alternation; that is all that was attended"
  adequacy: "Cannot determine by eye whether the transition crosses the general or red flash threshold, and no longer look would decide it; that call needs a flash-frequency analyzer reading"
  disposition: BLOCKED
  claim_boundary: "One slide change was looked at once at 3.4.0 and flashes. Whether it exceeds the flash threshold is undecided without an analyzer reading — nothing about other carousels or other pages."
```

**OP-AD — audio description track for the training video (claim: FAIL).**
```yaml
- operation: OP-AD
  closes: rem-video-ad-inadequate-77c2
  version: "3.4.0"
  session: 2026-09-03-MS-c
  tooling: "Chrome 141, built-in player, headphones; no AT"
  media: "Product walkthrough video on the training page, 3:40, player id 'walkthrough'"
  expected: "The 'Described' track speaks the settings panel and the on-screen error code during the silent stretch at 0:40-0:55, which the primary audio omits"
  played: "0:00-1:10 with the 'Described' track selected from the CC/AD menu; 0:35-1:00 again with the track deselected"
  heard: "With the track selected: silence over the 0:40-0:55 stretch, the same as without it; the second voice speaks only once, at 1:02, to read the chapter title. Without the track: silence over the same stretch."
  seen: "Menu lists 'Described'; the on-screen error code at 0:44 is not spoken in the primary audio, and the description track plays silence over that stretch instead of speaking it"
  adequacy: "The description track is present in the menu but does not describe the settings panel or the error code during the silent stretch — it plays silence where the visual information is missing. The description does not convey what the primary audio omits."
  disposition: FAIL
  claim_boundary: "Description present in the menu but inadequate for the 0:40-0:55 stretch at 3.4.0 — it does not speak the content a listener would otherwise miss; the same stretch was played with and without the track. Nothing about the rest of the video or other videos."
```

## What the walk asserts

OP-RETURN PASS (two confirmations, different people, different dates),
OP-FLASH BLOCKED, OP-AD FAIL
(played with and without the track; the description is present but
inadequate).
