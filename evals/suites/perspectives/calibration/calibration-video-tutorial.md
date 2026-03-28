# Calibration Fixture C3: Video Tutorial Page

## Component Code

```jsx
import React, { useState, useRef } from 'react';

const VideoTutorial = ({ video, chapters }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentChapter, setCurrentChapter] = useState(0);
  const videoRef = useRef(null);

  const togglePlay = () => {
    if (videoRef.current) {
      isPlaying ? videoRef.current.pause() : videoRef.current.play();
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <main className="tutorial-page">
      <h1>{video.title}</h1>

      <div className="video-container">
        <video
          ref={videoRef}
          src={video.src}
          poster={video.poster}
          aria-label={video.title}
        >
          <track kind="captions" src={video.captionsSrc} srcLang="en" label="English" default />
          <track kind="descriptions" src={video.descriptionsSrc} srcLang="en" label="Audio descriptions" />
        </video>

        <div className="controls" role="toolbar" aria-label="Video controls">
          <button onClick={togglePlay} aria-label={isPlaying ? 'Pause' : 'Play'}>
            {isPlaying ? '⏸' : '▶'}
          </button>
          <button aria-label="Toggle captions">CC</button>
          <input
            type="range"
            min="0"
            max="100"
            aria-label="Volume"
            defaultValue="80"
          />
          <button aria-label="Fullscreen">⛶</button>
        </div>
      </div>

      <nav aria-label="Tutorial chapters">
        <h2>Chapters</h2>
        <ol>
          {chapters.map((ch, i) => (
            <li key={ch.id}>
              <button
                onClick={() => {
                  setCurrentChapter(i);
                  if (videoRef.current) videoRef.current.currentTime = ch.startTime;
                }}
                aria-current={i === currentChapter ? 'step' : undefined}
              >
                <span className="chapter-time">{ch.timestamp}</span>
                <span className="chapter-title">{ch.title}</span>
              </button>
            </li>
          ))}
        </ol>
      </nav>

      <section aria-label="Transcript">
        <h2>Full Transcript</h2>
        <div className="transcript">
          {chapters.map((ch) => (
            <div key={ch.id} className="transcript-segment">
              <h3>{ch.title}</h3>
              <p>{ch.transcript}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
};

export default VideoTutorial;
```

## Component Description

A video tutorial page with a custom player that includes captions (`<track kind="captions">`), audio descriptions (`<track kind="descriptions">`), keyboard-accessible controls (play, pause, CC toggle, volume, fullscreen), chapter navigation with `aria-current`, and a full transcript section. This is a well-implemented media page.

## Why This Is a Calibration Fixture

Video tutorial pages should trigger HIGH for Auditory and Screen Reader — these are the primary access concerns for media content. The component handles them well, but the escalation mechanism should still flag them for deep review because the component type warrants it (media always needs auditory review). Cognitive and Keyboard should be MEDIUM (chapter navigation complexity, player controls). Low-concern perspectives (Magnification, Vestibular, Contrast) should be LOW.

## Expected Alarm Levels

| Perspective | Expected Level | Rationale |
|---|---|---|
| Magnification & Reflow | LOW | Standard page layout, responsive video |
| Environmental Contrast | LOW | No color-coded information, standard text |
| Vestibular & Motion | LOW | No animation beyond video playback (user-initiated) |
| Auditory Access | HIGH | Video with speech content — captions and transcripts are critical |
| Keyboard & Motor | MEDIUM | Custom player controls need keyboard verification |
| Screen Reader & Semantic | HIGH | Video semantics, track elements, chapter navigation, toolbar role |
| Cognitive & Neurodivergent | MEDIUM | Multi-section page with chapters; reading level of transcript |
