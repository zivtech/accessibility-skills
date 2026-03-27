# Fixture: Video Player Without Caption Control

## Component Code

```jsx
import React, { useState, useRef } from 'react';

const BuggyVideoPlayer = ({ videoSrc, captions }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const videoRef = useRef(null);

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div className="video-player">
      {/* BUG: No track element for captions */}
      {/* BUG: No caption toggle button */}
      {/* BUG: aria-label doesn't describe video content */}
      <video
        ref={videoRef}
        src={videoSrc}
        aria-label="Video player"
        // Missing: proper video semantics for AT
      />

      <div className="controls">
        <button onClick={togglePlay} aria-label="Play or pause">
          {isPlaying ? 'Pause' : 'Play'}
        </button>
        {/* BUG: No caption toggle button visible or accessible */}
        {/* Captions data is available but user cannot enable/disable them */}
      </div>
    </div>
  );
};

export default BuggyVideoPlayer;
```

## Expected Behavior

- Video player with play/pause control
- Caption toggle button available and accessible
- Captions displayed when enabled
- Keyboard accessible controls
- Deaf/hard of hearing users can enable captions

## Accessibility Features Present

✓ aria-label on video element
✓ Play/pause button with aria-label
✓ Captions data available

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing <track> element for captions** — Video has captions data but no <track> element to expose them to browser and AT. Per HTML video semantics, <track kind="captions"> should be used for caption display and accessibility.
   - Evidence: `video-player-missing-captions.md:26-28` (video element has no track child)
   - User group: Deaf and hard of hearing users (critical)
   - Expected: Video should have <track kind="captions"> element
   - Fix: Add <track kind="captions" src={captionTrackUrl} />

2. **CRITICAL: Missing caption toggle button** — User has no control to enable/disable captions. Button should be visible, keyboard accessible, and announce caption state. Currently captions are unavailable to deaf/hard of hearing users.
   - Evidence: `video-player-missing-captions.md:33-36` (no caption control)
   - User group: Deaf and hard of hearing users (critical)
   - Expected: Visible caption toggle button should be provided
   - Fix: Add button with aria-label="Enable captions" or similar, connected to caption visibility

3. **MAJOR: Captions not announced or controllable** — Even though captions data exists, user cannot access it. No programmatic way to enable/disable captions. Missing WCAG 1.2.2 (Captions for all prerecorded audio in synchronized media).
   - Evidence: `video-player-missing-captions.md:24-28` (captions prop unused)
   - User group: Deaf and hard of hearing users
   - Expected: Captions should be controllable by user through UI
   - Fix: Implement caption toggle with visual UI and proper state management

## Difficulty Level

**HAS-BUGS** — Video player lacks caption accessibility. While technical captions exist, they're not accessible to users.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should identify that video accessibility requires captions (WCAG 1.2.2), not just video element presence. This tests understanding of media accessibility requirements.
