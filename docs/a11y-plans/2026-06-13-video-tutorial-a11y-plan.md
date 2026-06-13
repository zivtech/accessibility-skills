# Video Tutorial Page Accessibility Design Plan

> **For Claude:** Use a11y-planner protocol. Review with a11y-critic after implementation.
> **Compliance target:** WCAG 2.2 AA (with AAA media alternatives noted where cheap to add)
> **Users who need accessibility:** Deaf and hard-of-hearing users (primary, currently blocked), deafblind users (braille display), low-vision users, keyboard-only users, screen reader users, users with audio off / in sound-sensitive environments
> **Assistive technologies:** NVDA + Firefox, JAWS + Chrome, VoiceOver + Safari, refreshable braille displays, keyboard-only

**Feature:** A React video tutorial page with a custom media player whose narration is currently inaccessible to anyone who cannot hear, and whose completion/error states are signalled by audio beeps with no visual or programmatic equivalent.

**Risk Level:** Medium — the keyboard/pointer control layer is already correct; the risk is concentrated in the **auditory dimension** (captions, transcript, audio-only status signals), which is a Level A failure today.

**Component Type:** Media Player (custom controls) + status messaging

**Source under review:** `evals/suites/chain/targets/video-tutorial-no-captions/component.jsx`

---

## Scope & Context

**What is being built.** Accessibility design for an existing custom video player. The player renders a `<video>` with no native controls and a custom control bar (play/pause, seek, time readout, mute, volume). The video carries **instructor narration** as its primary information channel.

**What user need it addresses.** Watching and understanding a tutorial. "Understanding" is the operative word: the information is in the spoken narration, so any user who cannot hear it cannot complete the job, regardless of how good the controls are.

**Who needs accessibility, and who is blocked today.**

| User group | Today's experience | Severity |
|---|---|---|
| Deaf / hard-of-hearing | Sees moving pictures, gets zero narration content. No captions, no transcript. Cannot complete the tutorial. | **Blocked (Level A failure)** |
| Deafblind (braille) | No audio, no captions, no transcript → nothing reaches the braille display. | **Blocked (Level A failure)** |
| Audio-off / quiet environment | Same as Deaf for this session. Completion/error beeps never heard. | Blocked for this session |
| Low vision | Emoji-only icons (▶ ⏸ 🔊 🔇) may not render or scale predictably; muted state hard to perceive. | Medium |
| Keyboard-only | Controls operable (native `<button>`/`<input type=range>`). **Not a defect.** Missing only the *conventional* media keyboard shortcuts. | Enhancement |
| Screen reader | Control names present. But video name is weak, and error state is never announced. | Medium |

**Compliance target.** WCAG 2.2 **AA**. Captions (1.2.2) and a media alternative / transcript (1.2.3) are both **Level A** — these are not "nice to have," they are the floor. Sign language (1.2.6) and extended audio description (1.2.7) are AAA and explicitly out of scope (see Negative Space).

**Risk level: Medium.** Not High, because focus management here is genuinely simple — there is no modal, no overlay, no dynamic content insertion that steals focus, no focus trap to build. Not Low, because there is a live Level A failure (no captions) affecting an entire user population, plus a status-message gap (audio-only error) that can leave a user stranded with no idea the video failed.

**What this modifies.** It extends the existing component — no rewrite. The control layer stays; we add a `<track>`, a captions toggle, a transcript region, a visible status region, and a few label refinements.

**Constraints.**
- Must keep the existing keyboard-correct control layer intact (the source comments mark play/seek/volume as deliberately correct — do not "fix" them into regressions).
- Captions require a caption file (`.vtt`). **This is a content dependency, not a code task** — flagged explicitly below. If no `.vtt` exists, the engineering work ships but the Level A failure is NOT resolved until content delivers the file. Do not mark 1.2.2 satisfied on code merge alone.
- `AudioContext` is created on every `ended`/`error`. Per **WCAG 1.4.2 Audio Control**, auto-playing audio longer than 3s needs a stop control; these beeps are <0.3s so 1.4.2 is not triggered — but the beep must not be the *only* signal (1.1.1 / 4.1.3).

---

## Semantic Structure Plan

**Landmarks.** The page already uses `<main>` (l91) and a `<section>` (l154). That is sound. We add one landmark consideration: the transcript. A transcript is supporting content for the video, so it belongs in a `<section>` with an accessible name, not a new `<main>` or `<aside>` (it is not tangential — it IS the content for non-hearing users).

**Heading hierarchy.** Current: `h1` (title, l92) → `h2` ("About this tutorial", l155). Correct, no skips. The transcript adds one `h2` ("Transcript") as a sibling of "About this tutorial". Final outline:

```
h1  {title}
  h2  About this tutorial
  h2  Transcript
```

This keeps a flat, scannable outline. WCAG 1.3.1 Info and Relationships; WCAG 2.4.6 Headings and Labels.

**Document structure stub** (structure only — not implementation):

```
<main>
  <h1>{title}</h1>

  <section> aria-label="Video player"        ← name the player region (see note)
    <video>
      <track kind="captions" srclang="en" label="English" default?>   ← NEW
    </video>

    <div role="group" aria-label="Video controls">
      <button>  play / pause
      <input type="range">  seek
      <span aria-live="off">  time readout      ← KEEP off (see State section)
      <button>  mute
      <input type="range">  volume
      <button>  captions on / off                ← NEW (toggle button)
    </div>

    <div role="status" aria-live="polite">         ← NEW visible status region
      (empty | "Video ended" | "Video failed to load. Try reloading the page.")
    </div>
  </section>

  <section aria-labelledby="meta-heading">
    <h2 id="meta-heading">About this tutorial</h2>
    <p>Duration: …</p>
  </section>

  <section aria-labelledby="transcript-heading">    ← NEW
    <h2 id="transcript-heading">Transcript</h2>
    <details> or always-visible region with the narration text
  </section>
</main>
```

**Note on the player `<section>` name.** The player wrapper is currently a bare `<div className="video-wrapper">` (l94). Promoting it to a named region (`<section aria-label="Video player">`) gives screen reader users a landmark to jump to. This is an enhancement, not a fix — document it as such.

**List structure.** None required.

**Form structure.** The two range inputs (seek, volume) are form controls but are part of a media widget, not a data-entry form. They do **not** need a `<fieldset>`/`<legend>` — `role="group"` + `aria-label="Video controls"` (already present, l102) is the correct grouping for a media control bar. See Known Pitfall #3 caveat below for why these `aria-label`-only sliders are acceptable *here* but would not be on a data form.

**Skip link.** A page-level skip-to-main-content link is a whole-page concern, not this component's responsibility. Note it as a page-template requirement (WCAG 2.4.1 Bypass Blocks) but out of this component's scope.

---

## Interaction Pattern Design

**Governing pattern: there is no single "media player" pattern in the WAI-ARIA APG.** The APG does not publish a media-player composite pattern. The correct approach (and what the existing code already does) is to compose the player from standard widgets, each mapped to its own APG pattern, and to lean on **native HTML semantics** (`<button>`, `<input type="range">`) which carry their roles, states, and keyboard behavior for free. This is the right call — do not rebuild these as ARIA widgets.

References:
- APG Button pattern: https://www.w3.org/WAI/ARIA/apg/patterns/button/
- APG Slider pattern: https://www.w3.org/WAI/ARIA/apg/patterns/slider/
- HTML `<video>` + `<track>`: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/track
- WAI Media tutorial (captions/transcripts): https://www.w3.org/WAI/media/av/

### Interactive Elements Table

| Widget | APG / spec pattern | Keyboard | ARIA | WCAG |
|--------|-------------------|----------|------|------|
| Play / Pause button | [APG Button](https://www.w3.org/WAI/ARIA/apg/patterns/button/) | Tab to focus; Enter / Space activate (native `<button>`) | Dynamic `aria-label` ("Play video" / "Pause video") — already correct (l106). Add `aria-pressed`? **No** — play/pause is a label-change toggle, not a pressed-state toggle; changing the label is the clearer pattern. Do not add `aria-pressed`. | 2.1.1, 4.1.2 |
| Seek slider | [APG Slider](https://www.w3.org/WAI/ARIA/apg/patterns/slider/) | Native range: ←/→ step by 1s, Home/End jump to start/end | `aria-label="Seek"` + `aria-valuetext` (l121-122) — already correct. `aria-valuetext` overrides the raw number so SR says "0:42 of 3:15" not "42". Keep. | 2.1.1, 4.1.2 |
| Time readout | (not interactive) | — | `aria-live="off"` (l126) — **intentionally correct**, see below | 4.1.3 |
| Mute toggle | [APG Button](https://www.w3.org/WAI/ARIA/apg/patterns/button/) | Enter / Space (native) | Dynamic `aria-label` ("Mute" / "Unmute", l133). Consider `aria-pressed` here: mute IS a binary on/off state, so `aria-pressed` is *defensible* — but the label already flips, and doubling up ("Unmute, toggle button, pressed") is redundant. **Pick ONE:** keep the label-flip approach for consistency with play/pause. Document the decision so the critic doesn't flag inconsistency. | 2.1.1, 4.1.2 |
| Volume slider | [APG Slider](https://www.w3.org/WAI/ARIA/apg/patterns/slider/) | Native range: ←/→ step 0.05 | `aria-label="Volume"` (l146). **Add `aria-valuetext`** to announce a percentage ("40%") instead of "0.4" — raw 0–1 float is opaque to SR users. | 1.4.2, 4.1.2 |
| **Captions toggle** (NEW) | [APG Button](https://www.w3.org/WAI/ARIA/apg/patterns/button/) | Enter / Space | This one **should use `aria-pressed`** (true/false) because it is a true on/off toggle with no destination change, and "Captions, toggle button, pressed" is the clearest announcement. `aria-label="Captions"` (static) + `aria-pressed` reflecting track mode. | 1.2.2, 4.1.2 |

**Why mute uses label-flip but captions uses `aria-pressed`:** this is a deliberate, defensible split, not an inconsistency. Mute's two states have distinct, meaningful verbs ("Mute" vs "Unmute" — the label tells you what the button *does next*). Captions' states do not ("Captions" stays "Captions"; only the on/off state changes), so it needs `aria-pressed` to carry the state. Document this rationale in the component so the critic does not flag it. (Per Known Pitfall #4: enumerate the toggle branches explicitly.)

**Optional enhancement — conventional media keyboard shortcuts.** Standard players support Space (play/pause) and ←/→ (seek) when the *player region* has focus, plus M (mute) and C (captions). These are an **enhancement, not a defect** — the controls are already individually operable by Tab + Enter/Space. If added: attach a `keydown` handler to the player region, respect that focus may be on a slider (where ←/→ already means "adjust slider" — do not hijack), and document the shortcut map visibly (e.g., in the "About" section). Do not let shortcut handlers swallow keys that native controls need. Defer unless requested; flag as a separate task.

### Screen reader experience (target)

- On focusing the player region: "Video player, region."
- On Tab to play button: "Play video, button." → activate → label becomes "Pause video, button."
- On Tab to seek: "Seek, slider, 0:42 of 3:15." → ←/→ → "0:41 of 3:15."
- On Tab to captions toggle: "Captions, toggle button, not pressed." → activate → "Captions, toggle button, pressed."
- On video end: status region announces "Video ended" once (polite).
- On load error: status region announces "Video failed to load. Try reloading the page." (polite — see severity discussion in State section).

---

## Focus Management Plan

This component is deliberately simple for focus, and that is worth stating plainly so the critic does not hunt for a focus trap that should not exist.

1. **Tab order** (matches visual L-to-R reading order, WCAG 2.4.3): play → seek → (time readout is not focusable) → mute → volume → captions toggle → transcript content. Verify the captions toggle is placed in the DOM at the end of the control group so tab order matches its visual position; if design places it elsewhere, move the DOM node, do not reorder with CSS (WCAG 1.3.2).
2. **No focus trap.** There is no modal or overlay. Building a focus trap here would be wrong. Explicitly: do NOT add one.
3. **No focus restoration logic needed.** Nothing opens or closes that moves focus. The captions toggle changes track visibility, not focus — focus stays on the toggle (correct; matches APG Button). Do not move focus on caption toggle.
4. **No focus stealing on status changes.** When the video ends or errors, the status region updates via `aria-live` — focus must NOT jump to it (WCAG 4.1.3 status messages are announced *without* moving focus, by design). Confirm the status `<div>` is never given `tabindex` and is never `.focus()`-ed.
5. **Focus indicators.** All five (soon six) controls must show a visible focus ring meeting **3:1 contrast** against the player background (WCAG 2.4.7, 1.4.11). The player background is typically dark (video chrome) — plan a **two-color focus ring** (dark `outline` + light `box-shadow`, or vice versa) so it survives both the dark control bar and any light fallback poster. Use `:focus-visible` (not `:focus`) so the ring does not appear on mouse click. The emoji buttons are `display: inline-block`-safe; confirm they are not `display: inline` (fragmented outline). Watch for framework/reset CSS overriding the ring — use sufficient specificity.
6. **Touch targets.** Each control ≥ **44×44 CSS px** (WCAG 2.5.8). The mute/play emoji buttons and the captions toggle must hit this; sliders need a ≥44px-tall hit area even if the visual track is thin.

No skip link, no roving tabindex (these are independent controls, not a single composite widget — each is its own tab stop, which is correct for a media bar).

---

## State Communication Design

This is the heart of the plan. The component's failure mode is **states that exist in audio but not in the DOM**.

### The audio-only status problem (core finding)

On `ended` (l20-29) and `error` (l30-39) the code plays an `AudioContext` beep — 880Hz for completion, 220Hz sawtooth for error — and updates `hasCompleted` / `hasError` state **that is never rendered to the DOM**. The state booleans exist in React but nothing in the returned JSX consumes them. So:

- A Deaf user gets no completion signal and **no error signal at all**.
- The error case is the more serious: a failed video load leaves the user staring at a blank player with zero indication that anything is wrong or what to do. That is a dead end with no escape hatch.

**Fix:** render `hasCompleted` and `hasError` into a visible `role="status"` region, AND keep (or drop) the beep as a redundant, non-sole channel. The beep is fine as an *enhancement* for sighted/hearing users; it just cannot be the *only* signal. WCAG 1.1.1 (non-text content has a text alternative), WCAG 4.1.3 (status messages programmatically determinable).

**Error severity nuance — assertive vs polite.** A load error is arguably urgent (the user is waiting on something that will never come). But `role="alert"` / `aria-live="assertive"` interrupts whatever the SR is currently reading. For a *completion* message, polite is clearly right (non-urgent). For an *error*, I recommend a single `role="status"` (polite) region that holds whichever message is current, because: (a) the user is not mid-task in a way that an interruption protects, and (b) one region is more robust than two competing live regions (see Known Pitfall #1 — never multiply live regions). If the team judges the error genuinely interruptive, upgrade the *error* path to `role="alert"` — but then use a **separate** alert element from the status element, and never put either inside a loop. Document the choice. WCAG 4.1.3.

### Why `aria-live="off"` on the time readout is CORRECT (not a bug)

The scout flagged "verify intent" on `aria-live="off"` (l126). **Verified: it is intentionally correct and must stay `off`.** The time readout updates on every `timeupdate` event — multiple times per second. If it were `polite` or `assertive`, a screen reader would attempt to announce "0:01… 0:02… 0:03…" continuously, flooding the user and making the page unusable. The current position is already available on demand via the seek slider's `aria-valuetext` ("0:42 of 3:15"), which the user hears when they focus or move the slider — that is the correct, on-demand delivery. **Do not change this to a live region.** Flagging it as a bug would be exactly the kind of checklist-driven dead output this repo warns against.

### State Communication Table

| State | Visual indicator | Programmatic indicator | ARIA | WCAG |
|-------|------------------|------------------------|------|------|
| Playing / Paused | Icon ▶ ⏸ (emoji) **+ recommend a text or SVG icon, see note** | Button `aria-label` flips "Play video"/"Pause video" | dynamic `aria-label` | 1.1.1, 4.1.2 |
| Muted / Unmuted | Icon 🔊 🔇 (emoji) **+ ensure a clear visual difference, see note** | Button `aria-label` flips "Mute"/"Unmute" | dynamic `aria-label` | 1.1.1, 1.4.1, 4.1.2 |
| Volume level | Slider thumb position | `aria-valuetext` → **"40%"** (add) | `aria-valuetext` | 4.1.2 |
| Seek position | Slider thumb position | `aria-valuetext` "0:42 of 3:15" (present) | `aria-valuetext` | 4.1.2 |
| Captions on / off | Toggle button visibly pressed/active state (border/fill) — **not color alone** | `aria-pressed` true/false; underlying `track.mode = showing/hidden` | `aria-pressed` | 1.2.2, 1.4.1, 4.1.2 |
| **Video ended** | **Visible text in status region** ("Video ended") | `role="status"` text content | `role="status"` (aria-live polite) | 1.1.1, 4.1.3 |
| **Load error** | **Visible text in status region** ("Video failed to load. Try reloading the page.") + ideally a visible error icon/border on the player | `role="status"` (or `role="alert"`) text content | live region | 1.1.1, 3.3.1, 4.1.3 |
| Time (current/total) | Visible text readout | Available via seek `aria-valuetext` on demand | `aria-live="off"` (KEEP) | 4.1.2 |

**Note on emoji icons (▶ ⏸ 🔊 🔇).** Emoji as the *sole* visual control glyph is fragile: rendering varies by OS/font, scaling under zoom is unpredictable, and high-contrast mode may drop or recolor them unexpectedly. The accessible *name* is fine (it comes from `aria-label`), so this is not a name/role/value failure — it is a **low-vision robustness** concern (WCAG 1.4.11 non-text contrast for the glyph, 1.4.4 resize). Recommendation: replace emoji with inline SVG icons (which scale crisply and can inherit `currentColor` for contrast/high-contrast support) wrapped in `aria-hidden="true"` (Known Pitfall: decorative glyph hidden from AT since the button's `aria-label` already names it). If emoji are kept, verify they render and scale at 200%/400% zoom and in forced-colors mode. Either way the emoji/SVG must carry `aria-hidden` or be inside a button that supplies the name, so the SR reads the label, not "play button emoji."

**Note on muted visual state (1.4.1 Use of Color).** Confirm the muted state is distinguishable by more than the emoji swap — e.g., a strike or a visibly different icon shape, not just a color change. A 🔊→🔇 swap is a *shape* change (sound waves vs crossed-out), which satisfies 1.4.1; verify the chosen icons actually differ in shape, not only color.

### Captions: the primary state, fully specified

This is the Level A fix. Plan:

1. **`<track kind="captions" srclang="en" label="English" src="...vtt">`** inside `<video>`. `kind="captions"` (not `kind="subtitles"`) because captions include non-speech audio cues (e.g., "[upbeat music]"), which matters when the *point* is that a non-hearing user gets everything the audio conveys. WCAG 1.2.2.
2. **Default state decision:** Should captions be ON by default? For a tutorial whose information is in the narration, defaulting captions **on** (`default` attribute or `track.mode = 'showing'` on load) is the more inclusive choice and removes a step for the population that needs them. Document the decision; if product wants them off-by-default, the toggle must be obvious and discoverable. WCAG 1.2.2.
3. **Captions toggle button** drives `track.mode` between `'showing'` and `'hidden'`, with `aria-pressed` mirroring it. Because the player uses *custom* controls (native controls are off), the browser's built-in caption menu is NOT available — so this custom toggle is **mandatory**, not optional. Without it, even a correct `<track>` is unreachable.
4. **Styling of caption text** (`::cue`): ensure caption text meets **4.5:1 contrast** against its background (WCAG 1.4.3) and resizes (1.4.4). A semi-opaque background box behind cue text is the robust pattern over video imagery.

---

## Visual Accessibility Plan

1. **Color contrast (WCAG 1.4.3 / 1.4.11).**
   - Caption `::cue` text: ≥ 4.5:1 against its backing box.
   - Control icons and the time readout against the (likely dark) control bar: ≥ 4.5:1 for the time text, ≥ 3:1 for icon glyphs and slider tracks/thumbs (non-text UI).
   - Status region text: ≥ 4.5:1. The error message in particular must be readable, not a faint gray.
   - Focus rings: ≥ 3:1 against adjacent colors (the two-color ring technique from Focus Management handles the dark-bar case).
2. **Color is never the sole indicator (WCAG 1.4.1).** Enumerated color-coded states and their non-color companions:
   - Captions on/off → button *pressed* visual + `aria-pressed` (shape/state, not just color).
   - Muted → distinct icon *shape* (crossed-out), not just a recolor.
   - Error → text message + icon/border, not just a red tint.
   - Completion → text message, not just a green tint.
3. **Font sizing (WCAG 1.4.4 / 1.4.10).** Time readout and caption text in `rem`/`em`, not fixed `px`. Must survive 200% zoom (1.4.4) and reflow without horizontal scroll at 400% / 320px-equivalent (1.4.10). The control bar should wrap or shrink gracefully at narrow widths — do **not** hide controls (especially the captions toggle) behind a desktop-only breakpoint. Captions must remain visible and legible at 400% zoom.
4. **Animation / motion (WCAG 2.3.3).** No essential animation here; if any control has transitions, respect `prefers-reduced-motion: reduce`.
5. **Forced-colors / high-contrast mode.** Emoji glyphs are the risk (see State note). Prefer SVG with `currentColor`; verify controls remain visible in Windows High Contrast / forced-colors.
6. **Touch targets (WCAG 2.5.8).** ≥ 44×44 px for every control including the new captions toggle (restated from Focus section because it is both a focus and a visual/pointer concern).

---

## Content Accessibility Plan

1. **Transcript (WCAG 1.2.3 Level A; 1.2.8 AAA for full equivalence).** Provide a text transcript of the narration in the new Transcript `<section>`. This is the **only** access path for deafblind (braille) users and a redundant path for everyone. A transcript also satisfies 1.2.3's "media alternative" prong. The transcript should be real text in the DOM (not an image, not a PDF-only link), so it is selectable, searchable, translatable, and reaches a braille display. If the transcript is long, an in-page `<details>` or a "Skip to transcript" affordance keeps it from burying the page — but the text must be in the DOM, not lazy-loaded behind a fetch that AT might miss.
   - **Content dependency:** the transcript text must be authored. Like the `.vtt`, this is a content deliverable; the code provides the region and the engineering is trivial, but 1.2.3 is not satisfied until the text exists.
2. **Captions file (WCAG 1.2.2 Level A).** The `.vtt` is a content deliverable (covered in State section). **Engineering merging the `<track>` element does not close the 1.2.2 gap by itself — the file must contain accurate, synchronized captions including non-speech cues.** Plan a content task with an owner.
3. **`<video>` accessible name (WCAG 1.1.1 / 4.1.2).** Current `aria-label="video player"` (l98) is weak and lowercase. The video's name should describe *this* video, e.g., `aria-label={`${title} — tutorial video`}` so SR users hear what the video is, not a generic "video player." Also confirm we are not double-naming: the wrapping region is named "Video player," so the `<video>` itself should carry the *content* name (the title), not repeat "player."
4. **Status message wording (WCAG 3.3.1 Error Identification).** The error message must be specific and actionable: "Video failed to load. Try reloading the page." — not "Error" or a beep. If a retry mechanism exists, name it. Completion message: "Video ended." (brief, polite).
5. **Language (WCAG 3.1.1).** `<html lang>` is a page-template concern (out of component scope), but the `<track srclang="en">` must match the caption language, and any transcript in another language needs `lang` on its container (3.1.2).
6. **Link text** — n/a unless the transcript is delivered as a link; if so, the link text must describe the destination ("Read the full transcript"), never "click here" (WCAG 2.4.4).
7. **Reading order (WCAG 1.3.2).** DOM order (player → about → transcript) matches visual order. Maintain it; do not CSS-reorder.

---

## Testing Strategy

Per Known Pitfall #9, automated + visual is **not sufficient** — the plan mandates DOM verification and real assistive-technology checks.

**1. Automated (axe-core via a11y-test / `npx playwright test`).** Run on every state variant: default, playing, paused, muted, captions-on, captions-off, **ended**, **error**. axe will validate: control name presence, contrast, heading order, region naming, `aria-pressed` validity on the captions toggle.
   - **axe will NOT catch:** absence of captions (no rule detects a missing `<track>` — a clean axe run does NOT mean 1.2.2 passes), absence of a transcript, the audio-only-status problem, or whether the live region actually announces. These require manual checks below. State this explicitly so a green axe run is not mistaken for compliance.

**2. DOM verification (mandatory, Known Pitfall #9).** Inspect rendered DOM to confirm:
   - `<track kind="captions">` is present inside `<video>` and `src` resolves (not 404).
   - The captions toggle's `aria-pressed` value actually tracks `track.mode` (inspect both before/after toggling).
   - On `ended`/`error`, the `role="status"` region's **text content is non-empty in the DOM** — i.e., `hasCompleted`/`hasError` are actually rendered, not just held in React state. (This is the specific defect: state exists but never reaches the DOM. The test must assert DOM text, not React state.)
   - The time readout retains `aria-live="off"`.
   - The volume slider has `aria-valuetext` showing a percentage.

**3. Manual keyboard (a11y-test / agent-browser, real key events).** Tab order play→seek→mute→volume→captions; Enter/Space activate each button; ←/→ and Home/End move sliders; focus ring visible on every control at 100%/200%/400% zoom; focus never trapped; focus never jumps to the status region on end/error.

**4. Screen reader (real AT — NVDA+Firefox, VoiceOver+Safari minimum).**
   - Player region announced as a named region.
   - Captions toggle announces "toggle button, pressed/not pressed" and toggling changes the announcement.
   - **Turn captions on and confirm caption text appears over the video** (the actual user outcome, not just the attribute).
   - Reach the end of the video → confirm "Video ended" is announced **once**, politely, without stealing focus.
   - Force a load error (point `src` at a 404) → confirm the error message is announced AND visibly present, not just beeped.
   - Time readout does NOT spam announcements during playback (confirms `aria-live="off"` is right).
   - Navigate to and read the transcript via braille/SR.

**5. Visual regression.** Focus rings present (dark + light backgrounds); 200%/400% zoom reflow with no horizontal scroll and captions still legible; muted state visually distinct; forced-colors mode keeps controls visible.

**6. Content verification (not a code test, but a gate).** A human confirms the `.vtt` captions are accurate and synchronized and that the transcript matches the narration. **Compliance for 1.2.2/1.2.3 is gated on this, not on code merge.**

### Acceptance criteria (measurable)

- [ ] `<video>` contains `<track kind="captions">` with a resolving, accurate, synchronized `.vtt`. (1.2.2)
- [ ] A captions toggle exists, is keyboard-operable, exposes `aria-pressed`, and visibly shows captions over the video when on. (1.2.2, 4.1.2)
- [ ] A text transcript of the narration is present in the DOM and reachable by SR/braille. (1.2.3)
- [ ] Video completion is communicated by **visible DOM text** in a `role="status"` region (announced once, no focus steal), in addition to any beep. (1.1.1, 4.1.3)
- [ ] Video load error is communicated by **visible, specific, actionable DOM text**, in addition to any beep. (1.1.1, 3.3.1, 4.1.3)
- [ ] Time readout remains `aria-live="off"` and does not flood the SR during playback. (4.1.3)
- [ ] Volume slider announces a percentage via `aria-valuetext`. (4.1.2)
- [ ] `<video>` accessible name describes the tutorial, not a generic "video player." (1.1.1)
- [ ] All controls (incl. captions toggle) ≥ 44×44px, ≥ 3:1 focus ring on the dark bar, operable by keyboard. (2.4.7, 2.5.8, 2.1.1)
- [ ] No focus trap, no focus steal on status change. (2.1.2, 2.4.3, 4.1.3)

---

## Implementation Tasks

### Task 1: Captions track + toggle  🔍 **Review checkpoint**

**Files:** `evals/suites/chain/targets/video-tutorial-no-captions/component.jsx` (extend); add a caption asset (`.vtt`, content deliverable).

**Structure Stub:**
```
<video aria-label={`${title} — tutorial video`}>
  <track kind="captions" srclang="en" label="English" src={captionSrc} default />
</video>
...
<button
  aria-label="Captions"
  aria-pressed={captionsOn}
  onClick={toggleCaptions}     // sets track.mode 'showing'|'hidden' + state
>
  <SvgCaptionIcon aria-hidden="true" />
</button>
```

**ARIA attributes:**
- `<track kind="captions">` — WCAG 1.2.2 Captions (Prerecorded)
- captions button `aria-pressed` (true/false) — WCAG 4.1.2 Name, Role, Value
- captions button accessible name "Captions" (static; state via `aria-pressed`) — WCAG 4.1.2
- `<video>` descriptive `aria-label` — WCAG 1.1.1, 4.1.2

**Keyboard:** Tab to captions button; Enter/Space toggles `track.mode` and `aria-pressed`. Focus stays on button (no focus move).

**Tests:** DOM has `<track>` with resolving src; toggling flips `aria-pressed` AND `track.mode`; captions visibly render over video when on (SR/visual); caption `::cue` contrast ≥ 4.5:1; button ≥ 44×44px with visible focus ring.

**WCAG:** 1.2.2, 1.4.3, 4.1.2, 2.1.1, 2.5.8

**a11y-critic checkpoint:** Verify `<track>` present and reachable via the custom toggle (native menu is off, so the toggle is mandatory); `aria-pressed` chosen correctly for *this* toggle (vs label-flip for mute — confirm the rationale is documented and consistent); caption default-on decision documented; emoji-vs-SVG glyph handled with `aria-hidden`.

---

### Task 2: Visible status region for completion + error  🔍 **Review checkpoint**

**Files:** `evals/suites/chain/targets/video-tutorial-no-captions/component.jsx`

**Structure Stub:**
```
<div role="status" aria-live="polite" className="player-status">
  {hasError
    ? 'Video failed to load. Try reloading the page.'
    : hasCompleted
    ? 'Video ended'
    : ''}
</div>
```
(Single region holds whichever message is current — one region, not one-per-event. The existing `hasError`/`hasCompleted` state is finally consumed by the DOM here. Keep the AudioContext beeps as a redundant channel; they are no longer the sole signal.)

**ARIA attributes:**
- `role="status"` (= polite live region) — WCAG 4.1.3 Status Messages
- If error is judged interruptive, a **separate** `role="alert"` element for the error path only (never share an element, never place in a loop) — WCAG 4.1.3

**Keyboard / focus:** none — the region is **not** focusable, never `.focus()`-ed; announcements happen without moving focus.

**Tests (DOM-level, the critical assertion):**
- Simulate `ended` → assert status region **text content** = "Video ended" (assert DOM text, not React state).
- Simulate `error` (404 src) → assert status region text = the error message; assert it is also visibly rendered.
- Assert focus does not move when these fire.
- SR: message announced once, politely.

**WCAG:** 1.1.1, 3.3.1, 4.1.3

**a11y-critic checkpoint:** This is the core finding. Verify the previously-orphaned `hasError`/`hasCompleted` state now reaches the DOM as visible text; ONE live region (Known Pitfall #1); polite vs assertive decision documented; no focus steal; beep retained only as redundancy, not sole signal; error wording specific and actionable.

---

### Task 3: Transcript region  🔍 **Review checkpoint**

**Files:** `evals/suites/chain/targets/video-tutorial-no-captions/component.jsx`; transcript text (content deliverable).

**Structure Stub:**
```
<section aria-labelledby="transcript-heading">
  <h2 id="transcript-heading">Transcript</h2>
  {/* real DOM text of the narration; <details> optional for length */}
</section>
```

**ARIA attributes:** named region via `aria-labelledby` to the `<h2>` — WCAG 1.3.1; heading continues the h1→h2 outline — WCAG 2.4.6.

**Keyboard:** if wrapped in `<details>`, the native `<summary>` is keyboard-operable (Enter/Space) — APG Disclosure semantics come free; no custom handler.

**Tests:** transcript text present in DOM (selectable/searchable, reaches braille); heading order h1→h2→h2 unbroken; if `<details>`, summary toggles via keyboard.

**WCAG:** 1.2.3, 1.3.1, 2.4.6

**a11y-critic checkpoint:** Transcript is real in-DOM text (not image/PDF-only), reachable by braille; outline intact; content dependency flagged (1.2.3 not satisfied until narration text is authored).

---

### Task 4: Label & slider value refinements  🔍 **Review checkpoint**

**Files:** `evals/suites/chain/targets/video-tutorial-no-captions/component.jsx`

**Changes:**
- Volume slider: add `aria-valuetext={`${Math.round(volume*100)}%`}` — WCAG 4.1.2 (raw 0–1 float is opaque).
- `<video>` `aria-label` → descriptive (Task 1 covers the attribute; this confirms wording).
- Promote `.video-wrapper` to `<section aria-label="Video player">` (named region) — WCAG 1.3.1 (enhancement).
- **Confirm `aria-live="off"` on the time readout stays `off`** — explicitly a no-change item, documented as correct.
- Confirm muted state icon differs by *shape*, not color only — WCAG 1.4.1.

**Tests:** volume SR announces "40%"; video name describes the tutorial; time readout does not spam SR during playback; player region announced as named landmark.

**WCAG:** 4.1.2, 1.3.1, 1.4.1, 4.1.3

**a11y-critic checkpoint:** Verify `aria-live="off"` was correctly *preserved* (not "fixed"); volume value humanized; no double-naming between region and `<video>`.

---

### Task 5 (Optional / deferred): Conventional media keyboard shortcuts

**Defer unless requested.** Space=play/pause, ←/→=seek, M=mute, C=captions when player region focused. Must not hijack ←/→ when focus is on a slider; document the shortcut map visibly. Enhancement only — controls are already operable. Flagged separately so it is not conflated with the Level A fixes.

---

## a11y-Critic Review Checkpoints

| Checkpoint | After Task | Focus |
|-----------|-----------|-------|
| 🔍 1 | Task 1 | `<track>` present + reachable via mandatory custom toggle; `aria-pressed` correct for captions vs label-flip for mute (documented, consistent); caption default-on decision; emoji/SVG glyph `aria-hidden`; caption contrast |
| 🔍 2 | Task 2 | **Core finding:** orphaned `hasError`/`hasCompleted` now render to DOM as visible text; ONE live region; no focus steal; beep redundant not sole; error wording actionable |
| 🔍 3 | Task 3 | Transcript real in-DOM text, braille-reachable; outline intact; content dependency flagged |
| 🔍 4 | Task 4 | `aria-live="off"` correctly preserved (not "fixed"); volume value humanized; no double-naming; muted shape-not-color |

---

### Contract Appendix (for spec-kitty-bridge WP translation)

#### Architecture Overview
Extend the existing custom React video player (no rewrite). The control layer is already keyboard-correct and stays. Work concentrates on the **auditory dimension**: (1) add an HTML `<track>` captions element driven by a custom toggle button (native controls are off, so the toggle is mandatory) using `aria-pressed`; (2) render the already-existing-but-orphaned `hasError`/`hasCompleted` React state into a single `role="status"` live region as visible DOM text, keeping the AudioContext beeps only as a redundant channel; (3) add an in-DOM text transcript section; (4) humanize slider values and the video name and *preserve* the deliberately-correct `aria-live="off"` on the time readout. Captions (1.2.2) and transcript (1.2.3) carry **content dependencies** (`.vtt` file and narration text) that gate Level A compliance independently of code merge.

#### Implementation Tasks

##### Task 1: Captions track + toggle
Estimated Effort: medium (engineering low — ~1 component file; the medium rating reflects the blocking `.vtt` content dependency and the captions-default + `::cue` styling decisions)
Depends on: none (code); blocked on `.vtt` content deliverable for 1.2.2 closure

##### Task 2: Visible status region for completion + error
Estimated Effort: low (single component file; the `hasError`/`hasCompleted` state already exists and only needs to be rendered to a `role="status"` region)
Depends on: none

##### Task 3: Transcript region
Estimated Effort: low (engineering trivial — one component file; blocked on narration transcript content deliverable for 1.2.3 closure)
Depends on: none (code); blocked on transcript text content deliverable

##### Task 4: Label & slider value refinements
Estimated Effort: low (single component file, attribute-level edits)
Depends on: none

##### Task 5 (optional): Media keyboard shortcuts
Estimated Effort: medium (event handling must avoid hijacking slider arrow keys; deferred)
Depends on: Task 1 (captions shortcut targets the Task 1 toggle)

#### Test Strategy for Task 1
DOM: `<track kind="captions">` present with resolving src; toggling flips both `aria-pressed` and `track.mode`. Visual/SR: captions render over video when on; `::cue` contrast ≥ 4.5:1. Keyboard: button ≥44×44px, focus ring visible, Enter/Space toggles. WCAG 1.2.2, 1.4.3, 4.1.2, 2.1.1, 2.5.8.

#### Acceptance Criteria for Task 1
Captions toggle is keyboard-operable, exposes correct `aria-pressed`, drives `track.mode`, and visibly shows accurate synchronized captions over the video. `<video>` has a descriptive accessible name. (1.2.2 closure also requires the `.vtt` content deliverable.)

#### Test Strategy for Task 2
DOM (critical): on `ended`, status region text content = "Video ended"; on `error`, text = specific actionable message AND visibly rendered — assert DOM text, not React state. Focus does not move on either event. SR: announced once, politely. WCAG 1.1.1, 3.3.1, 4.1.3.

#### Acceptance Criteria for Task 2
Both completion and load-error are communicated as visible DOM text in a single `role="status"` region (announced once, no focus steal), with the AudioContext beep demoted to a redundant non-sole channel. Error text is specific and actionable.

#### Test Strategy for Task 3
DOM: transcript is real selectable/searchable text reaching a braille display (not image/PDF-only); heading outline h1→h2→h2 unbroken; if `<details>`, `<summary>` toggles via Enter/Space. WCAG 1.2.3, 1.3.1, 2.4.6.

#### Acceptance Criteria for Task 3
A text transcript of the narration is present in the DOM and reachable by screen reader and braille. (1.2.3 closure also requires the narration-text content deliverable.)

#### Test Strategy for Task 4
SR: volume announces "40%" not "0.4"; `<video>` name describes the tutorial; time readout does NOT flood announcements during playback (confirms `aria-live="off"` preserved); player region announced as a named landmark. WCAG 4.1.2, 1.3.1, 1.4.1, 4.1.3.

#### Acceptance Criteria for Task 4
Volume value is human-readable, the video has a descriptive name without double-naming the region, the muted state differs by icon shape (not color alone), and the time readout's `aria-live="off"` is preserved.

#### Failure Modes
- **Green axe run mistaken for compliance.** axe-core has no rule for missing captions/transcript — a clean automated scan does NOT mean 1.2.2/1.2.3 pass. Manual + content verification is mandatory.
- **Code merged, content missing.** `<track>` element present but no real `.vtt`; transcript region present but no narration text. Level A failures remain open. Compliance is gated on content, not code.
- **`hasError`/`hasCompleted` still orphaned.** State updated in React but a test asserts React state instead of DOM text, so the "state never reaches the DOM" defect survives the test. Tests MUST assert rendered DOM text.
- **`aria-live="off"` "fixed" into a live region.** A checklist-driven reviewer changes the time readout to `polite`/`assertive`, flooding SR users with per-tick time announcements — a regression introduced by treating a correct decision as a bug.
- **Multiplied live regions.** Separate competing `aria-live` elements for completion and error (or a live region inside a loop) producing duplicate/garbled announcements (Known Pitfall #1).
- **Captions unreachable.** `<track>` added but no custom toggle — since native controls are off, the browser caption menu is absent and the captions can never be turned on.
- **Focus stolen on status change.** Status region given `tabindex` or `.focus()`-ed on end/error, yanking the user out of context (violates the no-focus-steal rule for 4.1.3).
- **Inconsistent toggle semantics flagged as a bug.** Mute (label-flip) vs captions (`aria-pressed`) split is deliberate and documented; a reviewer unaware of the rationale flags it. Rationale lives in the component and in Task 1's checkpoint.

---

## Negative Space — What This Plan Does NOT Cover

Stated explicitly to prevent scope drift and false confidence:

- **Audio description (WCAG 1.2.5 AA / 1.2.7 AAA).** If the video contains *visual-only* information the narration does not speak (e.g., on-screen code shown but not read aloud), a blind user misses it and audio description would be required. This plan assumes the narration is the primary channel and does not design audio description. **If the tutorial shows things it doesn't narrate, that is a separate gap not closed here.** Flag for content review.
- **Sign language interpretation (1.2.6 AAA)** — out of scope (AAA, not targeted).
- **The accuracy of the caption/transcript content itself** — this plan provides the mechanisms; it cannot guarantee the `.vtt` and transcript are correct, synchronized, and complete. That is a content-QA responsibility and a compliance gate.
- **Page-level concerns** — skip links, `<html lang>`, page landmarks beyond this component. These belong to the page template.
- **The "controls are already correct" claim is inherited from the source/recon, not re-derived from scratch here.** This plan trusts that the native `<button>`/`<input type=range>` keyboard behavior works and does not re-audit it; the Testing Strategy verifies it rather than assuming it. If that assumption is wrong, the control layer needs its own review.
- **Network/error-recovery UX beyond messaging** — whether a retry button or auto-retry should exist is a product decision; this plan only requires that the error be *communicated* accessibly, not that recovery be built.
