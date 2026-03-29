# Fixture: Animated Onboarding Wizard With Unguarded Transitions

## Component Code

```jsx
import React, { useState, useEffect, useRef } from 'react';

const STEPS = [
  { title: 'Welcome', content: 'Let\'s set up your workspace.' },
  { title: 'Profile', content: 'Tell us about yourself.' },
  { title: 'Preferences', content: 'Customize your experience.' },
  { title: 'Complete', content: 'You\'re all set!' },
];

const OnboardingWizard = () => {
  const [step, setStep] = useState(0);
  const [showConfetti, setShowConfetti] = useState(false);
  const canvasRef = useRef(null);

  const goNext = () => {
    if (step < STEPS.length - 1) {
      setStep(s => s + 1);
    } else {
      // BUG: Confetti animation — 200+ particles for 3 seconds, no reduced-motion check
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 3000);
    }
  };

  const goBack = () => step > 0 && setStep(s => s - 1);

  // BUG: Confetti particle animation — WCAG 2.3.1
  useEffect(() => {
    if (!showConfetti || !canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const particles = Array.from({ length: 200 }, () => ({
      x: Math.random() * canvas.width,
      y: -10,
      vx: (Math.random() - 0.5) * 4,
      vy: Math.random() * 3 + 2,
      color: ['#e63946', '#457b9d', '#2a9d8f', '#e9c46a', '#f4a261'][Math.floor(Math.random() * 5)],
      size: Math.random() * 6 + 2,
    }));
    let raf;
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(p => {
        p.x += p.vx; p.y += p.vy;
        ctx.fillStyle = p.color;
        ctx.fillRect(p.x, p.y, p.size, p.size);
      });
      raf = requestAnimationFrame(draw);
    };
    draw();
    return () => cancelAnimationFrame(raf);
  }, [showConfetti]);

  return (
    <div className="onboarding">
      {showConfetti && <canvas ref={canvasRef} className="confetti-canvas" />}

      {/* BUG: Step icons bounce on activation — no prefers-reduced-motion */}
      <div className="step-icons">
        {STEPS.map((s, i) => (
          <div
            key={i}
            className={`step-icon ${i === step ? 'active' : ''} ${i < step ? 'done' : ''}`}
          >
            {i + 1}
          </div>
        ))}
      </div>

      {/* BUG: Progress bar smooth-fill animation — no reduced-motion */}
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${(step / (STEPS.length - 1)) * 100}%` }} />
      </div>

      {/* BUG: Full-viewport slide transition — translateX(100%), no reduced-motion — WCAG 2.3.1 */}
      <div className="step-container">
        <div className="step-slider" style={{ transform: `translateX(-${step * 100}%)`, transition: 'transform 0.5s ease' }}>
          {STEPS.map((s, i) => (
            <div key={i} className="step-panel">
              <h2>{s.title}</h2>
              <p>{s.content}</p>
              {i === 1 && (
                <fieldset>
                  <legend>Your info</legend>
                  <label htmlFor="name">Name</label>
                  <input id="name" type="text" />
                  <label htmlFor="role">Role</label>
                  <input id="role" type="text" />
                </fieldset>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="onboarding-actions">
        {step > 0 && <button onClick={goBack} aria-label="Go back">Back</button>}
        <button onClick={goNext} aria-label={step === STEPS.length - 1 ? 'Finish setup' : `Next: ${STEPS[step + 1]?.title}`}>
          {step === STEPS.length - 1 ? 'Finish' : 'Next'}
        </button>
      </div>
    </div>
  );
};

export default OnboardingWizard;
```

```css
.onboarding {
  max-width: 640px;
  margin: 0 auto;
  padding: 32px;
  position: relative;
  /* BUG: Background gradient shift animation — subtle but continuous */
  background: linear-gradient(135deg, #f0f4ff, #e8f5e9);
  transition: background 0.8s ease;
}

.confetti-canvas {
  position: fixed;
  top: 0; left: 0;
  z-index: 100;
  pointer-events: none;
}

.step-icons {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 16px;
}

/* BUG: Bounce animation on active step icon — no reduced-motion guard */
.step-icon {
  width: 36px; height: 36px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 14px;
  background: #e0e0e0; color: #555;
}

.step-icon.active {
  background: #1565c0; color: #fff;
  animation: iconBounce 0.4s ease;
}

.step-icon.done { background: #2e7d32; color: #fff; }

@keyframes iconBounce {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.3); }
  100% { transform: scale(1); }
}

/* BUG: Progress bar smooth-fill — no reduced-motion override */
/* No @media (prefers-reduced-motion: reduce) anywhere in this stylesheet */
.progress-track {
  height: 6px; background: #e0e0e0; border-radius: 3px; margin-bottom: 24px;
}

.progress-fill {
  height: 100%; background: #1565c0; border-radius: 3px;
  transition: width 0.5s ease;
}

.step-container {
  overflow: hidden;
}

.step-slider {
  display: flex;
  /* transition defined inline — also no reduced-motion */
}

.step-panel {
  min-width: 100%;
  padding: 24px;
}

.step-panel h2 { font-size: 1.5rem; margin-bottom: 8px; }
.step-panel p { font-size: 1rem; color: #333; }

fieldset { border: 1px solid #ccc; padding: 16px; border-radius: 4px; margin-top: 16px; }
label { display: block; margin-top: 8px; font-weight: 600; }
input { width: 100%; padding: 8px; border: 2px solid #ccc; border-radius: 4px; margin-top: 4px; font-size: 1rem; box-sizing: border-box; }
input:focus { outline: 3px solid #1565c0; outline-offset: 2px; }

.onboarding-actions {
  display: flex; justify-content: flex-end; gap: 12px; margin-top: 24px;
}

.onboarding-actions button {
  padding: 10px 20px; border: none; border-radius: 4px;
  font-size: 1rem; font-weight: 600; cursor: pointer;
  background: #1565c0; color: #fff;
}

.onboarding-actions button:focus-visible {
  outline: 3px solid #005fcc; outline-offset: 2px;
}
```

## Expected Behavior

- 4-step onboarding wizard: Welcome, Profile, Preferences, Complete
- Animated slide transitions between steps
- Progress bar fills as user advances
- Confetti animation plays on final step completion
- Back/Next buttons navigate between steps

## Accessibility Features Present

- Next/Back buttons have descriptive aria-labels
- Step content uses h2 headings
- Form fields have labels
- Inputs have visible focus styles
- Button focus-visible outlines present

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Full-viewport slide transitions without prefers-reduced-motion — WCAG 2.3.1**
   `translateX(-${step * 100}%)` with `transition: transform 0.5s ease` applied inline. No `@media (prefers-reduced-motion)` block exists anywhere. Full-viewport translations are high-risk for vestibular symptoms.
   - Evidence: Line 82 — inline style with transition; no media query guard in CSS
   - User group: Vestibular disorder users (BPPV, migraine, motion sickness)
   - Fix: Wrap in `useReducedMotion()` hook; use instant swap or opacity crossfade for reduced-motion users

2. **CRITICAL: Confetti particle animation — 200+ moving elements for 3 seconds — WCAG 2.3.1**
   Canvas-based confetti spawns 200 particles with continuous movement via requestAnimationFrame. No prefers-reduced-motion check before starting animation.
   - Evidence: Lines 29-50 — confetti effect with no media query or JS matchMedia check
   - User group: Vestibular users, photosensitive users
   - Fix: Check `window.matchMedia('(prefers-reduced-motion: reduce)')` before starting; show static "Congratulations" instead

3. **MAJOR: Progress bar smooth-scrolling fill animation — WCAG 2.3.3**
   `.progress-fill` has `transition: width 0.5s ease` with no reduced-motion override.
   - Evidence: CSS line for `.progress-fill` — transition with no @media guard
   - User group: Vestibular users
   - Fix: `@media (prefers-reduced-motion: reduce) { .progress-fill { transition: none; } }`

4. **MAJOR: Step icons bounce/scale on activation — WCAG 2.3.3**
   `@keyframes iconBounce` runs on `.step-icon.active` with no reduced-motion guard.
   - Evidence: CSS `@keyframes iconBounce` and `.step-icon.active` animation
   - User group: Vestibular users, cognitive/attention users
   - Fix: `@media (prefers-reduced-motion: reduce) { .step-icon.active { animation: none; } }`

5. **MINOR: Background gradient shift animation on each step**
   `.onboarding` has `transition: background 0.8s ease`. Subtle but continuous.
   - Evidence: CSS `.onboarding` — transition on background
   - User group: Vestibular users
   - Fix: `@media (prefers-reduced-motion: reduce) { .onboarding { transition: none; } }`

## Difficulty Level

**HAS-BUGS** — New dimension: Vestibular & Motion. Keyboard navigation works correctly (buttons are labeled, form fields accessible). Every bug is in the motion/animation dimension. A reviewer checking only ARIA/keyboard patterns will find nothing wrong.

## Frameworks

React 18+, Canvas API, CSS transitions/keyframes
