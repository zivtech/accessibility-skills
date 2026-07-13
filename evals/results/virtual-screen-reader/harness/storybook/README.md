# Storybook lane validation (2026-07-13)

Undefers the assessment's "Storybook as a documented path | defer until run" matrix row by running it:
VSR play-function assertions executed through Storybook's own CI-shaped test runner
(`@storybook/addon-vitest`, Vitest browser mode, headless Playwright Chromium). Result: **12/12 tests
pass** (our 4 validation stories + the scaffold's 8 default-story smoke tests) in ~2s.

## Environment (as run)

storybook 10.4.6 · @storybook/react-vite 10.4.6 · @storybook/addon-vitest 10.4.6 · vitest 4.1.10 ·
@vitest/browser-playwright 4.1.10 · playwright 1.61.1 · react 19.2.7 · vite 8.1.1 ·
@guidepup/virtual-screen-reader 0.32.1 (exact pin) · Node 24.13, macOS.

## Reproduce

```bash
npm create vite@latest storybook-vsr -- --template react
cd storybook-vsr && npm install
npx create-storybook@10.4.6 --yes --no-dev
npm install -D -E @guidepup/virtual-screen-reader@0.32.1
# copy ToastStatus.jsx + ToastStatus.stories.js (this directory) into src/stories/
npx vitest run --project=storybook          # expected: 12 passed
```

Version note: `storybook@latest init` (10.5.0 on the run date) was refused by the user-level npm
supply-chain guard `min-release-age=7` — the init error itself names the guard-compliant pin
(`create-storybook@10.4.6`), which is what ran. Re-runs on a later date may use a newer compliant
version; re-verify the four stories if so.

## What the four stories verify

| Story | Verifies |
|---|---|
| `AnnouncesOnSave` | The headline: `virtual.start({container: canvasElement})` inside `play`, a real `userEvent.click`, then `"polite: Item saved"` captured in `spokenPhraseLog()` — live-region announcement assertion as a story, no URL, no separate test file. |
| `ReadingOrder` | Bounded walk (max-step guard) over the story canvas: heading phrase present, `$29.00` read before `button, Save order`. |
| `NaiveMountToastStaysSilent` | Calibration rule 3 transfers to the Storybook lane: a `role="alert"` toast mounted **with** its content is in the DOM (`findByText` succeeds) but never announced. |
| `IsolationCheck` | With `finally`-stop discipline, no spoken-phrase leakage across stories sharing the browser page. |

## Missing-stop characterization (measured, probes not committed)

Two temporary probe stories (deliberately-failing play functions written in upstream's no-`finally`
example style) measured what a missing `virtual.stop()` actually does across stories:

- **No wedge:** the next story's `virtual.start()` recovers cleanly — nothing hangs (unlike the
  Vitest fake-timer wedge, which is a different mechanism: timer starvation).
- **But the log leaks:** the spoken-phrase log **survives** the start-over-missing-stop restart —
  the failed story's `"polite: Item saved"` appeared in the next story's `spokenPhraseLog()`
  (asserted: the leak-check story failed on contamination).

Consequence, encoded in the story template: `try { … } finally { await virtual.stop(); }` in every
play function — it protects **log integrity between stories**, not against crashes. Upstream's own
example omits the `finally`; don't copy that shape.

## Files

- `ToastStatus.jsx` / `ToastStatus.stories.js` — component + the four stories, verbatim as run
  (comment header records the missing-stop measurement).
- `package.json` — full dependency record of the scaffold as run.
