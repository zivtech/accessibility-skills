# Fixture: Podcast Player Without Transcripts

## Component Code

```jsx
import React, { useState, useRef, useEffect } from 'react';

// CSS
/*
.podcast-player {
  max-width: 720px;
  margin: 0 auto;
  font-family: system-ui, sans-serif;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.episode-list {
  list-style: none;
  margin: 0;
  padding: 0;
  border-bottom: 1px solid #e0e0e0;
}

.episode-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

.episode-item:hover,
.episode-item:focus-within {
  background: #f9f9f9;
}

.episode-item button {
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 600;
  text-align: left;
  cursor: pointer;
  padding: 0;
  color: #111;
  flex: 1;
}

.episode-duration {
  font-size: 13px;
  color: #666;
  margin-left: 16px;
}

.new-badge {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e53e3e;
  margin-right: 8px;
  flex-shrink: 0;
  /* BUG: "new episode" indicator is visual-only dot — no text equivalent, no aria-label */
}

.player-bar {
  padding: 16px;
  background: #f5f5f5;
  border-top: 1px solid #e0e0e0;
}

.player-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.player-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-control {
  background: #222;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.seek-bar {
  flex: 1;
  accent-color: #222;
}

.time-display {
  font-size: 12px;
  color: #555;
  white-space: nowrap;
}

.speed-control {
  /* NOT a bug — speed control has select element with label */
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
}

.speed-select {
  /* BUG: select shows current value visually but aria-label is static "Playback speed"
     — does not announce what speed is currently active to screen readers on change */
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 2px 4px;
  font-size: 13px;
}

.no-transcript-notice {
  /* BUG: This section does NOT exist — transcript is completely absent */
}
*/

const EPISODES = [
  { id: 'ep-42', title: 'Ep. 42: The Future of Urban Farming', duration: '38:12', isNew: true },
  { id: 'ep-41', title: 'Ep. 41: Soil Science Deep Dive', duration: '45:07', isNew: false },
  { id: 'ep-40', title: 'Ep. 40: Interview with a Market Gardener', duration: '52:30', isNew: false },
];

const PodcastPlayer = () => {
  const [currentEpisode, setCurrentEpisode] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [speed, setSpeed] = useState(1);
  const audioRef = useRef(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleLoaded = () => setDuration(audio.duration);
    const handleTime = () => setCurrentTime(audio.currentTime);
    const handleNewEpisode = () => {
      // BUG: "New episode available" notification is an audio chime only.
      // No visual indicator, no aria-live announcement, no text update in DOM.
      const ctx = new AudioContext();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.frequency.value = 660;
      osc.type = 'sine';
      gain.gain.setValueAtTime(0.3, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6);
      osc.start();
      osc.stop(ctx.currentTime + 0.6);
    };

    audio.addEventListener('loadedmetadata', handleLoaded);
    audio.addEventListener('timeupdate', handleTime);

    // Simulate new episode notification on mount
    handleNewEpisode();

    return () => {
      audio.removeEventListener('loadedmetadata', handleLoaded);
      audio.removeEventListener('timeupdate', handleTime);
    };
  }, [currentEpisode]);

  const selectEpisode = (episode) => {
    setCurrentEpisode(episode);
    setIsPlaying(false);
    setCurrentTime(0);
  };

  const togglePlay = () => {
    const audio = audioRef.current;
    if (!audio) return;
    if (isPlaying) {
      audio.pause();
    } else {
      audio.play().catch(() => {});
    }
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (e) => {
    const val = parseFloat(e.target.value);
    if (audioRef.current) audioRef.current.currentTime = val;
    setCurrentTime(val);
  };

  const handleSpeedChange = (e) => {
    const val = parseFloat(e.target.value);
    if (audioRef.current) audioRef.current.playbackRate = val;
    setSpeed(val);
    // BUG: speed state updates visually in the select, but screen readers are not
    // informed of the new speed value — no aria-live update, no aria-valuenow on control
  };

  const skipSeconds = (secs) => {
    if (!audioRef.current) return;
    audioRef.current.currentTime = Math.min(
      Math.max(0, audioRef.current.currentTime + secs),
      duration
    );
  };

  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="podcast-player">
      <h1 style={{ padding: '16px', margin: 0, fontSize: '18px', borderBottom: '1px solid #e0e0e0' }}>
        The Growing Edge Podcast
      </h1>

      {/* BUG: Each episode intro ("In this episode...") is described in the audio only.
          Episode descriptions are spoken in the first 30 seconds of audio but never
          rendered as visible text anywhere in the component. */}
      <ul className="episode-list" aria-label="Episodes">
        {EPISODES.map((ep) => (
          <li key={ep.id} className="episode-item">
            {ep.isNew && (
              /* BUG: Red dot has no text equivalent or aria-label — deaf/blind user
                 cannot determine which episodes are new without tooltip or visually-hidden text */
              <span className="new-badge" role="img" />
            )}
            {/* Keyboard-accessible episode button — NOT a bug */}
            <button
              onClick={() => selectEpisode(ep)}
              aria-pressed={currentEpisode?.id === ep.id}
            >
              {ep.title}
            </button>
            <span className="episode-duration">{ep.duration}</span>
          </li>
        ))}
      </ul>

      {/* Hidden audio element — source would be episode.audioSrc in real implementation */}
      <audio ref={audioRef} src={currentEpisode ? `/audio/${currentEpisode.id}.mp3` : undefined} />

      {currentEpisode && (
        <div className="player-bar">
          <p className="player-title">{currentEpisode.title}</p>

          <div className="player-controls" role="group" aria-label="Player controls">
            {/* Keyboard-accessible skip back — NOT a bug */}
            <button
              className="btn-control"
              onClick={() => skipSeconds(-15)}
              aria-label="Skip back 15 seconds"
            >
              ↺
            </button>

            {/* Keyboard-accessible play/pause — NOT a bug */}
            <button
              className="btn-control"
              onClick={togglePlay}
              aria-label={isPlaying ? 'Pause' : 'Play'}
            >
              {isPlaying ? '⏸' : '▶'}
            </button>

            {/* Keyboard-accessible skip forward — NOT a bug */}
            <button
              className="btn-control"
              onClick={() => skipSeconds(30)}
              aria-label="Skip forward 30 seconds"
            >
              ↻
            </button>

            {/* Keyboard-accessible seek bar — NOT a bug */}
            <input
              type="range"
              className="seek-bar"
              min={0}
              max={duration || 0}
              value={currentTime}
              step={1}
              onChange={handleSeek}
              aria-label="Seek"
              aria-valuetext={`${formatTime(currentTime)} of ${formatTime(duration)}`}
            />

            <span className="time-display" aria-live="off">
              {formatTime(currentTime)} / {formatTime(duration)}
            </span>

            <div className="speed-control">
              <label htmlFor="speed-select">Speed</label>
              {/* BUG: aria-label is static — does not announce current speed on change */}
              <select
                id="speed-select"
                className="speed-select"
                value={speed}
                onChange={handleSpeedChange}
                aria-label="Playback speed"
              >
                <option value={0.75}>0.75x</option>
                <option value={1}>1x</option>
                <option value={1.25}>1.25x</option>
                <option value={1.5}>1.5x</option>
                <option value={2}>2x</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {/* BUG: No transcript section anywhere in the component.
          WCAG 1.2.1 requires a text alternative for audio-only content.
          The entire spoken content of every episode is inaccessible to deaf users. */}
    </div>
  );
};

export default PodcastPlayer;
```

## Expected Behavior

- Podcast player with episode list, per-episode play controls, seek, skip, and speed
- Each episode has a transcript available below the player or via a linked transcript page
- Episode descriptions (spoken in audio intro) are also shown as visible text per episode
- "New episode" notification appears as a visible badge with text, not only a chime
- Speed control announces the newly selected speed to screen readers on change
- All player controls are keyboard-operable with descriptive labels

## Accessibility Features Present

- Episode list is a `<ul>` with `aria-label="Episodes"`
- Each episode button uses `aria-pressed` to reflect selection state
- Skip back/forward buttons have descriptive `aria-label` values with durations
- Play/pause button label updates on state change
- Seek bar has `aria-label` and `aria-valuetext` with formatted time
- Speed control uses a `<label>` associated to `<select>` via `htmlFor`/`id`
- Player controls grouped with `role="group"` and `aria-label`

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: No transcript for audio-only content** — The component renders no transcript section and provides no link to an external transcript. Every episode consists of spoken audio with no text alternative anywhere in the DOM. WCAG 1.2.1 (Audio-only and Video-only, Prerecorded) requires a text alternative for all prerecorded audio-only content.
   - Evidence: `podcast-audio-only.md` — no transcript `<section>`, no transcript link, `/* BUG: This section does NOT exist */` comment at line marking `no-transcript-notice`
   - User group: Deaf and hard of hearing users; users in noise-sensitive environments
   - Expected fix: Add a `<section aria-label="Transcript">` below the player for each episode, or a visible "Read transcript" link to a transcript page

2. **MAJOR: Episode descriptions are audio-only** — Each episode's spoken intro ("In this episode we cover...") conveys description content that is never rendered as text in the component. Users who cannot hear the audio have no way to understand episode contents before choosing to play.
   - Evidence: `podcast-audio-only.md` — `/* BUG: episode intro descriptions are spoken in audio but never rendered as visible text */` comment above episode list; no description field in episode list items
   - User group: Deaf and hard of hearing users
   - Expected fix: Add a `description` field to each episode object and render it as visible `<p>` text in the episode list item

3. **MAJOR: "New episode" notification is audio chime only, no visual indicator** — `handleNewEpisode` fires a Web Audio API chime on mount with no corresponding DOM update. The `isNew` badge renders as a small red dot (`<span class="new-badge">`) with `role="img"` but no `aria-label`, no visually-hidden text, and no `aria-live` region to announce new availability.
   - Evidence: `podcast-audio-only.md` — `handleNewEpisode` function fires `AudioContext` chime with no DOM change; `.new-badge` span has `role="img"` with no `aria-label` attribute
   - User group: Deaf and hard of hearing users; screen reader users
   - Expected fix: Add `aria-label="New episode"` to the badge span and add an `aria-live="polite"` region that announces new episode availability on mount

4. **MINOR: Speed control does not announce current speed to screen readers on change** — The `<select>` element carries a static `aria-label="Playback speed"` but does not surface the newly selected speed to assistive technology when changed. A screen reader user selecting 1.5x receives no confirmation of the active speed beyond the option text within the select itself.
   - Evidence: `podcast-audio-only.md` — `handleSpeedChange` updates `speed` state with no `aria-live` announcement; `<select aria-label="Playback speed">` label is static
   - User group: Screen reader users; motor-impaired users relying on keyboard
   - Expected fix: Add an `aria-live="polite"` status region that announces "Playback speed set to 1.5x" on change, or use `aria-valuenow` on a custom control

## Difficulty Level

**HAS-BUGS** — New dimension: auditory access. Keyboard controls (play/pause, skip, seek) are fully correct and intentional true negatives. The speed control has a label (`<label htmlFor>`) making it partially correct — the bug is specifically the missing change announcement. A perspective-aware reviewer must distinguish between the correctly associated label and the missing live region on change.

## Frameworks

React 18+, HTML5 audio element, Web Audio API, ARIA live regions (expected but absent)
