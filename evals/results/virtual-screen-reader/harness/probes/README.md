# Adoption-assessment probe scripts (archived verbatim)

The scripts behind the **Validation Performed** table in
[docs/virtual-screen-reader-adoption-assessment.md](../../../../../docs/virtual-screen-reader-adoption-assessment.md),
exactly as executed on 2026-07-11 against `@guidepup/virtual-screen-reader@0.32.1`
(Node 24.13, jsdom 29.1.1, Vitest 4.x, Playwright 1.61 + cached Chromium). Archived for
reproducibility — these are evidence artifacts, not CI tests; two of them fail or hang **by
design** because that failure is the finding.

Run from the harness directory (`npm install` there first — it provides jsdom, vitest, playwright):

| Script | Assessment probe(s) | How to run | Expected result (as measured) |
|---|---|---|---|
| `probe.mjs` | A (unnamed button), B (live-region capture), C (aria-modal trap), D (aria-hidden), E (shadow DOM) | `node probes/probe.mjs` | A: bare `"button"` vs `"button, Save document"`; B: `"polite: Draft saved"`, `"assertive: Session expired"`; C: walk cycles inside the dialog, never reaches `end of document` (intended trapping, upstream #54); D: hidden text absent; E: shadow content absent (upstream #182) |
| `probe2.mjs` | F (CSS-hidden under jsdom) | `node probes/probe2.mjs` | Only `"Shown"` announced — stylesheet-class and inline `display:none`/`visibility:hidden` all excluded |
| `spot-toast.mjs` | Toast fixture spot-validation, buggy + naive fix | `node probes/spot-toast.mjs` | Both `buggy_phrases_after_mount` and `fixed_phrases_after_mount` = `[]` — the naive `role="alert"` mount-with-content fix is silent too (calibration rule 3) |
| `spot-toast2.mjs` | Rule-3 boundary: robust patterns | `node probes/spot-toast2.mjs` | `emptyThenFill` and `intoExistingContainer` both announce `"assertive: …"` |
| `vsr.test.mjs` | Real-harness run incl. G (fake timers) and H (teardown); A2 (wrong name); microtask-flush measurement | `npx vitest run probes/vsr.test.mjs` | **3 failed / 2 passed by design**: the fake-timers test hangs and wedges the singleton, cascading timeouts into the two tests after it — the measured basis of calibration rule 4. Microtask check logs `{"afterMicrotask":true,…}` |
| `vsr-nofake.test.mjs` | Same suite minus fake timers | `npx vitest run probes/vsr-nofake.test.mjs` | **4/4 pass** — persistent-container template, microtask flush, wrong-name (`"button, Close"`), teardown isolation. (Derived from `vsr.test.mjs` by deleting the fake-timers test — the cascade-attribution control.) |
| `vsr-faketimer.test.mjs` | Pinpoint of the fake-timer wedge | `npx vitest run probes/vsr-faketimer.test.mjs` | Fails by design after logging `1: before start` and `2: start resolved? ok` — `start()` resolves under fake timers; the log read never does |
| `vsr-browser.html` + `browser-run.mjs` | Browser-mode ESM run (Chromium) | from `harness/`: `python3 -m http.server 8931 --bind 127.0.0.1 &` then `node probes/browser-run.mjs` (serves `node_modules` + the page; kill the server after) | `textChange: ["polite: Draft saved"]`, `mountWithContent: []` (rule 3 transfers to the real browser), `emptyThenFill: ["assertive: Filled after mount"]` |

Note: `browser-run.mjs` loads `http://127.0.0.1:8931/probes/vsr-browser.html`, and the page imports
`/node_modules/@guidepup/virtual-screen-reader/lib/esm/index.browser.js` — serve from the `harness/`
directory root so both paths resolve. Archive fidelity: all files are verbatim as executed except one
adjustment — the goto URL in `browser-run.mjs` gained the `/probes/` prefix because the original run
used a flat directory; the probe logic and page are untouched.

The fixture-sweep harness that executed Phase 2 lives one level up (`../sweep.mjs`); its raw output is
in `../../raw/`.
