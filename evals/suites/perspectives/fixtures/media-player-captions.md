# Fixture: Media Player With Full Caption Support (CLEAN)

## Component Code

```jsx
import React, { useState, useRef } from 'react';

const MediaPlayer = () => {
  const videoRef = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.8);
  const [captionsOn, setCaptionsOn] = useState(true);

  const togglePlay = () => {
    if (playing) videoRef.current.pause();
    else videoRef.current.play();
    setPlaying(!playing);
  };

  const handleTimeUpdate = () => setCurrentTime(videoRef.current.currentTime);
  const handleLoadedMetadata = () => setDuration(videoRef.current.duration);
  const handleSeek = (e) => { videoRef.current.currentTime = Number(e.target.value); };
  const handleVolume = (e) => { const v = Number(e.target.value); setVolume(v); videoRef.current.volume = v; };

  const toggleCaptions = () => {
    const tracks = videoRef.current.textTracks;
    for (let i = 0; i < tracks.length; i++) {
      if (tracks[i].kind === 'captions') {
        tracks[i].mode = captionsOn ? 'disabled' : 'showing';
      }
    }
    setCaptionsOn(!captionsOn);
  };

  const formatTime = (s) => {
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return `${m}:${sec.toString().padStart(2, '0')}`;
  };

  return (
    <section className="media-section" aria-label="Video player">
      <h2>Tutorial: Getting Started</h2>

      <div className="video-wrapper">
        {/* tabIndex={-1} is correct — controls receive focus, not the video element */}
        <video
          ref={videoRef}
          tabIndex={-1}
          poster="/img/tutorial-poster.jpg"
          onTimeUpdate={handleTimeUpdate}
          onLoadedMetadata={handleLoadedMetadata}
          onPlay={() => setPlaying(true)}
          onPause={() => setPlaying(false)}
          autoPlay={false}
          preload="metadata"
        >
          <source src="/video/tutorial.mp4" type="video/mp4" />
          {/* Captions track with default — shows by default */}
          <track kind="captions" src="/video/tutorial-en.vtt" srcLang="en" label="English captions" default />
          <track kind="descriptions" src="/video/tutorial-desc.vtt" srcLang="en" label="Audio descriptions" />
        </video>
      </div>

      <div className="player-controls" role="toolbar" aria-label="Video controls">
        <button onClick={togglePlay} aria-label={playing ? 'Pause video' : 'Play video'}>
          {playing ? '⏸' : '▶'}
        </button>

        <label className="sr-only" htmlFor="seek-slider">Seek</label>
        <input
          id="seek-slider"
          type="range"
          min={0}
          max={duration}
          value={currentTime}
          onChange={handleSeek}
          aria-label={`Seek: ${formatTime(currentTime)} of ${formatTime(duration)}`}
          aria-valuetext={`${formatTime(currentTime)} of ${formatTime(duration)}`}
        />

        <span className="time-display" aria-live="off">
          {formatTime(currentTime)} / {formatTime(duration)}
        </span>

        <label className="sr-only" htmlFor="volume-slider">Volume</label>
        <input
          id="volume-slider"
          type="range"
          min={0}
          max={1}
          step={0.05}
          value={volume}
          onChange={handleVolume}
          aria-label={`Volume: ${Math.round(volume * 100)}%`}
          aria-valuetext={`${Math.round(volume * 100)}%`}
        />

        <button onClick={toggleCaptions} aria-label={captionsOn ? 'Turn off captions' : 'Turn on captions'} aria-pressed={captionsOn}>
          CC
        </button>
      </div>

      <details className="transcript-section">
        <summary>View full transcript</summary>
        <div className="transcript-content">
          <p><strong>0:00</strong> — Welcome to the Getting Started tutorial. In this video, we'll walk through setting up your workspace.</p>
          <p><strong>0:15</strong> — First, navigate to the Dashboard and click "New Project." Enter your project name and select a template.</p>
          <p><strong>0:30</strong> — Next, invite your team members via the Settings panel. Each member receives an email invitation.</p>
          <p><strong>0:45</strong> — Finally, configure your integrations. We support Slack, GitHub, and Jira out of the box.</p>
          <p><strong>1:00</strong> — That's it! Your workspace is ready. Check the documentation for advanced configuration.</p>
        </div>
      </details>
    </section>
  );
};

export default MediaPlayer;
```

```css
.media-section {
  max-width: 720px;
  margin: 0 auto;
  padding: 24px;
  font-family: system-ui, sans-serif;
}

.media-section h2 {
  font-size: 1.5rem;
  margin-bottom: 16px;
  color: #111;    /* #111 on white = 18.4:1 */
}

.video-wrapper {
  position: relative;
  background: #000;
  border-radius: 4px;
  overflow: hidden;
}

.video-wrapper video {
  width: 100%;
  display: block;
}

/* Fade-in respects reduced-motion */
@media (prefers-reduced-motion: no-preference) {
  .video-wrapper video { animation: fadeIn 0.3s ease; }
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.player-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #222;
  border-radius: 0 0 4px 4px;
}

.player-controls button {
  background: none;
  border: none;
  color: #fff;           /* #fff on #222 = 14.7:1 */
  font-size: 1.1rem;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
  min-width: 44px;
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.player-controls button:focus-visible {
  outline: 3px solid #80b3ff;
  outline-offset: 2px;
}

.player-controls button[aria-pressed="true"] {
  background: rgba(255,255,255,0.2);
}

.player-controls input[type="range"] {
  flex: 1;
  min-width: 80px;
  accent-color: #80b3ff;
}

.player-controls input[type="range"]:focus-visible {
  outline: 2px solid #80b3ff;
}

.time-display {
  font-size: 0.8rem;
  color: #ccc;          /* #ccc on #222 = 10.9:1 */
  white-space: nowrap;
  min-width: 60px;
}

.sr-only {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  border: 0;
}

.transcript-section {
  margin-top: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.transcript-section summary {
  padding: 12px 16px;
  font-weight: 600;
  cursor: pointer;
  color: #222;
}

.transcript-section summary:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: -3px;
}

.transcript-content {
  padding: 16px;
  font-size: 0.95rem;
  line-height: 1.6;
}

.transcript-content p { margin: 8px 0; }
.transcript-content strong { color: #1565c0; }
```

## Expected Behavior

- Video player with play/pause, seek slider, volume control, and caption toggle
- Captions track loads by default (showing on load)
- Audio descriptions track available
- Full transcript in expandable `<details>` section
- Keyboard controls for all player interactions

## Accessibility Features Present

- `<track kind="captions">` with `default` attribute — captions show on load
- `<track kind="descriptions">` for audio descriptions
- Full text transcript below video in `<details>` element
- Play/pause button with dynamic `aria-label` (changes based on state)
- Caption toggle with `aria-pressed` state
- Seek and volume sliders with `aria-label` and `aria-valuetext`
- `role="toolbar"` on controls group
- `tabIndex={-1}` on video element (controls receive focus, not video)
- `autoPlay={false}` — no autoplay
- Poster image on video element
- Focus-visible outlines on all controls
- 44x44px minimum touch targets on buttons
- `prefers-reduced-motion` respected on video fade-in
- All contrast ratios pass WCAG AA (documented in CSS)
- Transcript includes timestamps

## Accessibility Issues

**NONE.** This media player correctly implements all caption, description, transcript, and keyboard accessibility patterns.

Optional enhancements a reviewer MAY note:
1. Could add chapter markers for navigation within the video
2. Could add playback speed control for cognitive accessibility

## Difficulty Level

**CLEAN** — Comprehensive media accessibility. Tests whether reviewers correctly recognize a well-implemented media player.

## Frameworks

React 18+, CSS, HTML5 Video
