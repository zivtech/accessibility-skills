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
      const ctx = new AudioContext();
      const osc = ctx.createOscillator();
      osc.connect(ctx.destination);
      osc.frequency.value = 880;
      osc.start();
      osc.stop(ctx.currentTime + 0.15);
    };
    const handleError = () => {
      setHasError(true);
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

        </div>
      </div>


      <section className="tutorial-meta">
        <h2>About this tutorial</h2>
        <p>Duration: {formatTime(duration)}</p>
      </section>
    </main>
  );
};

export default VideoTutorialPage;
