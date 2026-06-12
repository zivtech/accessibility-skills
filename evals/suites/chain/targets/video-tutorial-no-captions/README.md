# Video Tutorial Page Without Captions

## Description

React video tutorial page with a fully keyboard-accessible custom player. The video contains instructor speech but has no <track> element, no caption toggle, no transcript, and uses audio-only beeps for error and completion signals with no visual DOM equivalent. All keyboard controls (play, pause, seek, volume) are intentionally correct to isolate the auditory dimension.

## Expected Behavior

- Tutorial video page with a full custom player
- Video has speech content throughout (instructor narration)
- Player controls (play, pause, seek, volume, mute) are all keyboard-operable
- Captions can be toggled on/off by the user
- A transcript is available below or linked from the page
- Completion and error states are communicated visually as well as via audio

## Accessibility Features Present

- Play/pause button with descriptive aria-label (updates on state change)
- Seek bar with aria-label and aria-valuetext showing time positions
- Volume slider with aria-label
- Mute toggle with aria-label reflecting current state
- Controls grouped with role="group" and aria-label
- Focus management on all interactive elements is correct

---

_This directory contains component files extracted from the a11y eval suite for chain evaluation._
_Run `/a11y-workflow full evals/suites/chain/targets/video-tutorial-no-captions/component.jsx` to start the chain._
