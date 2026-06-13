## Scout Recon: Video Tutorial Page

**Component type**: Video player with custom controls (React functional component)
**APG pattern match**: WAI-ARIA Media Player (partial — keyboard controls present, but missing captions/transcript patterns)
**Complexity**: Medium

**Files** (paths only):
- evals/suites/chain/targets/video-tutorial-no-captions/component.jsx (main component)
- evals/suites/chain/targets/video-tutorial-no-captions/README.md (spec)

**Existing ARIA inventory**:
- aria-label="video player" (line 98, `<video>`)
- role="group" (line 102, controls wrapper)
- aria-label="Video controls" (line 102, controls group)
- aria-label="Pause/Play video" (line 106, play button — dynamic)
- aria-label="Seek" (line 121, seek range input)
- aria-valuetext="{time} of {time}" (line 122, seek input)
- aria-label="Unmute/Mute" (line 133, mute button — dynamic)
- aria-label="Volume" (line 146, volume slider)
- aria-live="off" (line 126, time display)

**Existing semantic HTML**:
- `<button>` elements: 2 (play/pause, mute)
- `<main>` landmark: yes (line 91)
- `<section>` landmark: yes (line 154)
- Heading hierarchy: h1 → h2 (correct)
- Form labels: range inputs have aria-label; no associated `<label>` elements

**Notable patterns**:
- AudioContext synthesizer for completion + error audio feedback (no visual fallback)
- useState hooks for player state management
- useRef for video + progress bar DOM refs
- No keyboard event handlers (relies on native `<button>` and `<input type="range">` keyboard support)
- No focus trapping or focus restoration code

**Flags for reviewer**:
- No `<track>` element or captions — video contains narration but captions are missing
- No transcript or transcript link
- Audio completion/error beeps (AudioContext) have no visual equivalents in DOM
- Muted state communicated via aria-label only — no visual icon change confirmed
- aria-live="off" on time display — unlikely to need announcement but verify intent
