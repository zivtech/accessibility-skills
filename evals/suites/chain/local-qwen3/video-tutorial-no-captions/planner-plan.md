# Video Tutorial Page Accessibility Design Plan

> **For Claude:** Use a11y-planner protocol. Review with a11y-critic after implementation.
> **Compliance target:** WCAG 2.2 AA
> **Users who need accessibility:** Screen reader users, keyboard-only users, users with hearing impairments, users with cognitive disabilities
> **Assistive technologies:** NVDA, JAWS, VoiceOver, keyboard-only, screen magnifier, high contrast mode

**Feature:** Video tutorial page with custom player requiring auditory-to-visual state conversion
**Risk Level:** High
**Component/Page Type:** Video Player with Custom Controls

---

## Scope & Context

The component is a video tutorial page with a custom player that currently communicates completion/error states via audio-only beeps and lacks captions/transcripts. The existing keyboard-accessible controls (play/pause, seek, volume) are correct but need augmentation for full accessibility. The primary accessibility gaps are:

1. Missing captions for audio content (WCAG 1.2.2 Captions)
2. Missing visual indicators for audio signals (WCAG 1.2.3 Audio Description)
3. Missing transcript for video content (WCAG 1.2.3 Audio Description)
4. Missing visual feedback for completion/error states (WCAG 1.2.1 Audio-only)

## Semantic Structure Plan

### Structure Diagram

```html
<main class="tutorial-page" role="main" aria-labelledby="main-heading">
  <h1 id="main-heading">{title}</h1>
  
  <div class="video-wrapper">
    <video 
      ref={videoRef} 
      src={videoSrc} 
      aria-label="video player" 
      aria-describedby="video-description"
    />
    
    <div class="player-controls" role="group" aria-label="Video controls">
      <!-- Play/Pause Button -->
      <button 
        aria-label={isPlaying ? 'Pause video' : 'Play video'} 
        aria-pressed={isPlaying}
        aria-controls={videoId}
      >
        {isPlaying ? '⏸' : '▶'}
      </button>

      <!-- Seek Bar -->
      <input 
        type="range" 
        aria-label="Seek" 
        aria-valuetext={`${formatTime(currentTime)} of ${formatTime(duration)}`}
        aria-valuemin="0" 
        aria-valuemax={duration || 0} 
        aria-valuenow={currentTime}
      />

      <span class="time-display" aria-live="off">
        {formatTime(currentTime)} / {formatTime(duration)}
      </span>

      <!-- Mute Toggle -->
      <button 
        aria-label={isMuted ? 'Unmute' : 'Mute'} 
        aria-pressed={isMuted}
        aria-controls={videoId}
      >
        {isMuted ? '🔇' : '🔊'}
      </button>

      <!-- Volume Slider -->
      <input 
        type="range" 
        aria-label="Volume" 
        aria-valuemin="0" 
        aria-valuemax="1" 
        aria-valuenow={volume}
      />
    </div>
  </div>

  <!-- Visual State Indicators -->
  <div class="video-state" role="status" aria-live="polite" aria-atomic="true">
    {hasCompleted && <p>Video has completed playing</p>}
    {hasError && <p>Error playing video</p>}
  </div>

  <!-- Transcript Section -->
  <section class="tutorial-transcript" aria-label="Video transcript">
    <h2>Transcript</h2>
    <div id="transcript-content" role="document">
      {/* Transcript content goes here */}
    </div>
  </section>
</main>
```

## Interaction Pattern Design

| Widget | APG Pattern | Keyboard Model | ARIA Attributes | WCAG Citation |
|--------|-------------|----------------|-----------------|---------------|
| Play/Pause Button | Button | Tab, Enter/Space | role="button", aria-pressed, aria-controls | 2.1.1, 4.1.2 |
| Seek Bar | Slider | Tab, Arrow keys, Home/End | role="slider", aria-valuemin, aria-valuemax, aria-valuenow | 2.1.1, 4.1.2 |
| Mute Toggle | Button | Tab, Enter/Space | role="button", aria-pressed, aria-controls | 2.1.1, 4.1.2 |
| Volume Slider | Slider | Tab, Arrow keys, Home/End | role="slider", aria-valuemin, aria-valuemax, aria-valuenow | 2.1.1, 4.1.2 |
| Video State Announcements | Status | N/A | role="status", aria-live="polite" | 4.1.3 |

## Focus Management Plan

1. Tab order: Play button → Seek bar → Mute button → Volume slider (logical visual order)
2. Focus trap: Not needed (modal-free interface)
3. Focus restoration: None required (non-modal interface)
4. Skip link: Not needed (single main content area)
5. Composite widgets: Roving tabindex not needed (simple controls)

## State Communication Design

| State | Visual Indicator | Programmatic Indicator | ARIA Attribute | WCAG Citation |
|-------|------------------|------------------------|----------------|---------------|
| Playing | ▶ icon | aria-pressed="true" | aria-pressed | 4.1.2 |
| Paused | ⏸ icon | aria-pressed="false" | aria-pressed | 4.1.2 |
| Muted | 🔇 icon | aria-pressed="true" | aria-pressed | 4.1.2 |
| Unmuted | 🔊 icon | aria-pressed="false" | aria-pressed | 4.1.2 |
| Completion | "Video has completed" message | role="status" | aria-live="polite" | 4.1.3 |
| Error | "Error playing video" message | role="status" | aria-live="polite" | 4.1.3 |

## Visual Accessibility Plan

1. Color contrast: All text meets 4.5:1 ratio (WCAG 1.4.3)
2. Non-color indicators: Icons for play/pause/mute states
3. Font sizing: Relative units (rem) for all text
4. Responsive text: Line height 1.5× font size (WCAG 1.4.8)
5. Touch targets: All buttons ≥44×44px (WCAG 2.5.8)
6. Animation: No animations unless user prefers reduced motion (WCAG 2.3.3)

## Content Accessibility Plan

1. Alt text: Video has aria-label="video player"
2. Link text: Clear, descriptive labels for all interactive elements
3. Form labels: All input elements have appropriate aria-label
4. Error messages: Associated with video player via aria-describedby
5. Language: HTML lang="en" attribute set
6. Reading order: DOM order matches visual order (WCAG 1.3.2)

## Testing Strategy

1. Automated testing:
   - axe-core checks for ARIA attributes, contrast, and semantic structure
   - eslint-plugin-jsx-a11y for JSX-level ARIA patterns

2. Manual keyboard testing:
   - Tab through all controls, verify logical order
   - Test play/pause with Enter/Space
   - Test seek bar with arrow keys
   - Test volume slider with arrow keys

3. Screen reader testing:
   - Verify button states (playing/paused, muted/unmuted)
   - Verify slider values are announced
   - Verify status messages for completion/error

4. Visual regression testing:
   - Check focus indicators at 200% zoom
   - Verify state indicators are visible in high contrast mode

5. Acceptance criteria:
   - All controls keyboard-operable (2.1.1)
   - All state changes announced via screen reader (4.1.3)
   - All interactive elements have accessible names (4.1.2)
   - All text meets contrast requirements (1.4.3)
   - All visual state indicators have non-color alternatives (1.4.1)

## Implementation Tasks

### Task 1: Add Visual State Indicators
🔍 **Review checkpoint after this task**

**Files:**
- components/VideoTutorialPage.jsx

**Structure Stub:**
```jsx
<div class="video-state" role="status" aria-live="polite" aria-atomic="true">
  {hasCompleted && <p>Video has completed playing</p>}
  {hasError && <p>Error playing video</p>}
</div>
```

**ARIA Attributes:**
- role="status" (WCAG 4.1.3)
- aria-live="polite" (WCAG 4.1.3)
- aria-atomic="true" (WCAG 4.1.3)

**Tests:**
- Screen reader announces completion/error messages
- Visual messages appear simultaneously with audio signals

**WCAG Criteria:**
- WCAG 1.2.1 Audio-only
- WCAG 4.1.3 Status Messages

### Task 2: Add Video Transcript
🔍 **Review checkpoint after this task**

**Files:**
- components/VideoTutorialPage.jsx
- data/transcript.json

**Structure Stub:**
```jsx
<section class="tutorial-transcript" aria-label="Video transcript">
  <h2>Transcript</h2>
  <div id="transcript-content" role="document">
    {/* Transcript content goes here */}
  </div>
</section>
```

**ARIA Attributes:**
- role="document" (WCAG 1.3.1)
- aria-label="Video transcript" (WCAG 1.3.1)

**Tests:**
- Transcript is accessible via screen reader
- Transcript is linked from video player

**WCAG Criteria:**
- WCAG 1.2.3 Audio Description
- WCAG 1.3.1 Info and Relationships

### Task 3: Add Captions
🔍 **Review checkpoint after this task**

**Files:**
- components/VideoTutorialPage.jsx
- data/captions.vtt

**Structure Stub:**
```jsx
<video 
  ref={videoRef} 
  src={videoSrc} 
  aria-label="video player" 
  aria-describedby="video-description"
>
  <track 
    kind="captions" 
    src="data/captions.vtt" 
    srclang="en" 
    label="English" 
    default 
  />
</video>
```

**ARIA Attributes:**
- kind="captions" (WCAG 1.2.2)
- default (WCAG 1.2.2)

**Tests:**
- Captions appear when video plays
- Captions toggleable via UI

**WCAG Criteria:**
- WCAG 1.2.2 Captions
- WCAG 1.2.3 Audio Description

## a11y-Critic Review Checkpoints

| Checkpoint | After Task | Focus Areas |
|------------|------------|-------------|
| 🔍 1 | Task 1 | Verify visual state indicators match audio signals, status messages announced |
| 🔍 2 | Task 2 | Verify transcript is accessible and linked, document role correct |
| 🔍 3 | Task 3 | Verify captions appear and toggle correctly, track element implemented |

---

### Architecture Overview
The video player implements APG Button and Slider patterns for controls, with visual state indicators and transcript/captions for auditory content. Focus management follows logical tab order, and all state changes are announced via aria-live regions.

### Implementation Tasks
#### Task 1: Visual State Indicators
Estimated Effort: Medium
Depends on: none
#### Test Strategy for Task 1
- Screen reader announces completion/error messages
- Visual messages appear simultaneously with audio signals
#### Acceptance Criteria for Task 1
- WCAG 1.2.1 Audio-only
- WCAG 4.1.3 Status Messages

#### Task 2: Video Transcript
Estimated Effort: Medium
Depends on: none
#### Test Strategy for Task 2
- Transcript is accessible via screen reader
- Transcript is linked from video player
#### Acceptance Criteria for Task 2
- WCAG 1.2.3 Audio Description
- WCAG 1.3.1 Info and Relationships

#### Task 3: Captions
Estimated Effort: Medium
Depends on: none
#### Test Strategy for Task 3
- Captions appear when video plays
- Captions toggleable via UI
#### Acceptance Criteria for Task 3
- WCAG 1.2.2 Captions
- WCAG 1.2.3 Audio Description

### Failure Modes
- Missing visual indicators for audio signals
- Missing transcript for video content
- Missing captions for audio content
- Incomplete ARIA state communication
- Incorrect focus management

## References

- [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [WCAG 2.2 Specification](https://www.w3.org/WAI/WCAG22/quickref/)
- [a11y-critic skill](https://github.com/zivtech/a11y-meta-skills) — for post-implementation review
- [accessibility-testing skill](https://github.com/zivtech/zivtech-claude-skills) — for automated testing