# Fixture: Video Tutorial Page Without Captions

## Component Code

```jsx
import React, { useState, useRef, useEffect } from 'react';

const VideoTutorialPage = ({ title, videoSrc, videoId }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [volume, setVolume] = useState(1);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [hasError, setHasError] = useState(false);
  const [hasCompleted, setHasCompleted] = useState(false);
  const videoRef = useRef(null);
  const progressRef = useRef(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleLoadedMetadata = () => setDuration(video.duration);
    const handleTimeUpdate = () => setCurrentTime(video.currentTime);
    const handleEnded = () => {
      setIsPlaying(false);
      setHasCompleted(true);
      // BUG: Audio-only success beep — no visual DOM change to signal completion
      const ctx = new AudioContext();
      const osc = ctx.createOscillator();
      osc.connect(ctx.destination);
      osc.frequency.value = 880;
      osc.start();
      osc.stop(ctx.currentTime + 0.15);
    };
    const handleError = () => {
      setHasError(true);
      // BUG: Audio-only error beep — no visual DOM change to signal the error
      const ctx = new AudioContext();
      const osc = ctx.createOscillator();
      osc.connect(ctx.destination);
      osc.frequency.value = 220;
      osc.type = 'sawtooth';
      osc.start();
      osc.stop(ctx.currentTime + 0.3);
    };

    video.addEventListener('loadedmetadata', handleLoadedMetadata);
    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('ended', handleEnded);
    video.addEventListener('error', handleError);

    return () => {
      video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('ended', handleEnded);
      video.removeEventListener('error', handleError);
    };
  }, []);

  const togglePlay = () => {
    const video = videoRef.current;
    if (!video) return;
    if (isPlaying) {
      video.pause();
    } else {
      video.play();
    }
    setIsPlaying(!isPlaying);
  };

  const toggleMute = () => {
    const video = videoRef.current;
    if (!video) return;
    video.muted = !isMuted;
    setIsMuted(!isMuted);
  };

  const handleVolumeChange = (e) => {
    const val = parseFloat(e.target.value);
    videoRef.current.volume = val;
    setVolume(val);
  };

  const handleSeek = (e) => {
    const val = parseFloat(e.target.value);
    videoRef.current.currentTime = val;
    setCurrentTime(val);
  };

  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <main className="tutorial-page">
      <h1>{title}</h1>

      <div className="video-wrapper">
        {/* BUG: aria-label is generic "video player" — does not describe content */}
        {/* BUG: No <track kind="captions"> element — WCAG 1.2.2 violation */}
        {/* BUG: No <track kind="descriptions"> for audio descriptions */}
        <video
          ref={videoRef}
          src={videoSrc}
          aria-label="video player"
          className="tutorial-video"
        />

        <div className="player-controls" role="group" aria-label="Video controls">
          {/* Keyboard-accessible play/pause — NOT a bug */}
          <button
            onClick={togglePlay}
            aria-label={isPlaying ? 'Pause video' : 'Play video'}
            className="btn-play"
          >
            {isPlaying ? '⏸' : '▶'}
          </button>

          {/* Keyboard-accessible seek bar — NOT a bug */}
          <input
            type="range"
            ref={progressRef}
            min={0}
            max={duration || 0}
            value={currentTime}
            step={1}
            onChange={handleSeek}
            aria-label="Seek"
            aria-valuetext={`${formatTime(currentTime)} of ${formatTime(duration)}`}
            className="seek-bar"
          />

          <span className="time-display" aria-live="off">
            {formatTime(currentTime)} / {formatTime(duration)}
          </span>

          {/* Keyboard-accessible volume controls — NOT a bug */}
          <button
            onClick={toggleMute}
            aria-label={isMuted ? 'Unmute' : 'Mute'}
            className="btn-mute"
          >
            {isMuted ? '🔇' : '🔊'}
          </button>

          <input
            type="range"
            min={0}
            max={1}
            step={0.05}
            value={volume}
            onChange={handleVolumeChange}
            aria-label="Volume"
            className="volume-slider"
          />

          {/* BUG: No caption toggle button — WCAG 1.2.2 requires user control for captions */}
        </div>
      </div>

      {/* BUG: No transcript section or link to transcript — WCAG 1.2.1 for audio-only,
              also best practice for 1.2.2 synchronized media */}

      <section className="tutorial-meta">
        <h2>About this tutorial</h2>
        <p>Duration: {formatTime(duration)}</p>
      </section>
    </main>
  );
};

export default VideoTutorialPage;
```

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

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing `<track kind="captions">` element** — The `<video>` element has no `<track>` child for captions. Users who are deaf or hard of hearing have no way to access the speech content. WCAG 1.2.2 (Captions, Prerecorded) requires synchronized captions for all prerecorded video with audio.
   - Evidence: `video-tutorial-no-captions.md:89-96` — `<video>` element with no `<track>` children
   - User group: Deaf and hard of hearing users
   - Expected fix: Add `<track kind="captions" src="/captions/tutorial.vtt" srclang="en" label="English" />`

2. **CRITICAL: No transcript available** — No transcript section exists on the page, and no link to an external transcript is provided. For synchronized media, WCAG 1.2.1 (Audio-only and Video-only, Prerecorded) and WCAG 1.2.3 (Audio Description or Media Alternative) require a text alternative. Transcripts also serve users in noise-sensitive environments and those with cognitive disabilities.
   - Evidence: `video-tutorial-no-captions.md:141-145` — `<section class="tutorial-meta">` contains only duration; no transcript
   - User group: Deaf and hard of hearing users; cognitive/attention users
   - Expected fix: Add a `<section>` with the full transcript text, or a visible link to a transcript page

3. **MAJOR: No caption toggle button in player UI** — The controls group has no button to enable or disable captions. Even if a `<track>` element were present, users need a UI control to turn captions on or off. WCAG 1.2.2 requires user-controllable captions.
   - Evidence: `video-tutorial-no-captions.md:135-137` — comment marks where caption toggle should be; no button rendered
   - User group: Deaf and hard of hearing users; users in quiet/noisy environments
   - Expected fix: Add a button that toggles `videoRef.current.textTracks[0].mode` between `'showing'` and `'hidden'`

4. **MAJOR: Audio-only error and completion signals with no visual DOM equivalent** — The `handleError` callback fires an audio beep (sawtooth wave at 220 Hz) with no visual DOM change to indicate the error state. The `handleEnded` callback fires a success beep (880 Hz) with no visible on-screen change. `hasError` and `hasCompleted` are set in state but never rendered. Deaf users, users with hearing loss, and users in muted environments receive no feedback.
   - Evidence: `video-tutorial-no-captions.md:31-43` — `handleEnded` sets `hasCompleted` but renders nothing; `handleError` sets `hasError` but renders nothing; both fire `AudioContext` beeps
   - User group: Deaf and hard of hearing users; users with audio disabled
   - Expected fix: Render visible status text (e.g., "Video complete" or "Error loading video") when `hasCompleted` or `hasError` is true

5. **MINOR: `aria-label` on video element is generic** — `aria-label="video player"` does not describe the content of the video. Screen reader users navigating by landmark or element will not know what the tutorial is about before interacting.
   - Evidence: `video-tutorial-no-captions.md:91` — `aria-label="video player"` is hardcoded and does not reference `title` or `videoId`
   - User group: Screen reader users
   - Expected fix: Set `aria-label={title}` or `aria-label={`Tutorial video: ${title}`}`

## Difficulty Level

**HAS-BUGS** — New dimension: auditory access. The player controls are fully keyboard-accessible (play, pause, seek, volume). All keyboard accessibility is intentionally correct to isolate the auditory dimension. A perspective-aware reviewer should distinguish between correct keyboard behavior and missing auditory access provisions.

## Frameworks

React 18+, Web Audio API, HTML5 video element, WebVTT (expected but absent)
