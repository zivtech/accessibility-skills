# Component screen-reader assertions with virtual-screen-reader

**When to use:** you're implementing or fixing a component and need to assert what a screen reader computes and announces — accessible names, reading order, live-region announcements — in the project's own test suite, per PR, with no URL, journey, or deployed page. This is the `implement → test` layer: the cheapest point to catch the toast/async-status defect class. **When NOT to use:** keyboard operability (its interactions are synthetic `user-event` events — real-key evidence stays with `.spec.js`, agent-browser, or keyboard-a11y-tester), anything visual (jsdom has no layout), page/journey audits (→ keyboard-a11y-tester), rule scans (→ axe-core, §4), open-shadow-DOM components (invisible to it — upstream #182), `aria-busy` states (unsupported — upstream #36).

**What it is:** [guidepup/virtual-screen-reader](https://github.com/guidepup/virtual-screen-reader) — a screen-reader simulator as a library (MIT; adopted at npm `0.32.1`, exact-pinned). Walks the accessibility tree of any DOM, emits spoken phrases (`"button, Save document"`), captures live-region announcements with politeness prefixes (`"polite: Draft saved"`), and exposes SR quick-key emulation via `virtual.perform(virtual.commands.*)` — `moveToNextHeading`, `moveToNextLandmark`, per-level heading jumps, `jumpToErrorMessageElement` (aria-errormessage), aria-flowto reading-order commands. Spec-anchored (ACCNAME 1.2, CORE-AAM, HTML-AAM, WAI-ARIA 1.2) and WPT-tested upstream. It is already this stack's transitive SR engine inside keyboard-a11y-tester; this lane uses it directly. Validated in-repo 2026-07-11 in three environments — plain Node+jsdom, Vitest 4 jsdom environment, real Chromium via its ESM build — plus the Storybook lane 2026-07-13 (10.4.6 play functions via `@storybook/addon-vitest` browser mode, 12/12): `docs/virtual-screen-reader-adoption-assessment.md`. Jest+jsdom is expected to match Vitest but was not run — treat it as unvalidated until someone runs it.

### Install (Node ≥ 20)

```bash
npm install --save-dev @guidepup/virtual-screen-reader@0.32.1   # exact pin; re-verify calibration rules on any bump
```

### Core patterns (Vitest, jsdom environment — the verified harness)

```js
import { afterEach, expect, test } from "vitest";
import { virtual } from "@guidepup/virtual-screen-reader";

afterEach(async () => {
  await virtual.stop().catch(() => {});   // stateful singleton — mandatory, or phrase logs leak across tests
  document.body.innerHTML = "";
});

// 1. Announcement assertion — persistent-container pattern (the only reliable shape; see rule 3)
test("saving announces to screen reader users", async () => {
  document.body.innerHTML = `
    <main><button>Save</button></main>
    <div role="status" id="app-status"></div>  <!-- persistent, empty at mount -->
  `;
  await virtual.start({ container: document.body });
  document.getElementById("app-status").textContent = "Item saved";
  await Promise.resolve();   // microtask flush suffices (measured) — no arbitrary sleep needed
  expect(await virtual.spokenPhraseLog()).toContain("polite: Item saved");
});

// 2. Reading-order / name assertions — bounded walk (never while-true; see rule 1)
test("reads the expected sequence", async () => {
  document.body.innerHTML = `<h2>Cart</h2><p>$29.00</p><button>Buy now</button>`;
  await virtual.start({ container: document.body });
  const phrases = [];
  for (let i = 0; i < 40; i++) {           // max-step guard: aria-modal traps the cursor by design
    await virtual.next();
    const p = await virtual.lastSpokenPhrase();
    phrases.push(p);
    if (p === "end of document") break;
  }
  expect(phrases.indexOf("$29.00")).toBeLessThan(phrases.indexOf("button, Buy now"));
});
```

### Storybook stories as SR tests (verified 2026-07-13: Storybook 10.4.6 + `@storybook/addon-vitest` browser mode, Chromium)

Component libraries that live in Storybook can make announcement assertions part of the stories themselves — CI-shaped via `npx vitest run --project=storybook`, and visible in the dev-mode Interactions panel:

```js
import { expect, userEvent, waitFor } from "storybook/test";
import { virtual } from "@guidepup/virtual-screen-reader";

export const AnnouncesOnSave = {
  play: async ({ canvasElement, canvas }) => {
    await virtual.start({ container: canvasElement });   // scope to the story canvas
    try {
      await userEvent.click(await canvas.findByRole("button", { name: "Save order" }));
      await waitFor(async () =>
        expect(await virtual.spokenPhraseLog()).toContain("polite: Item saved"));
    } finally {
      await virtual.stop();   // mandatory — measured: the phrase log SURVIVES a missing stop and bleeds into the next story (start() itself recovers; the leak is the hazard)
    }
  },
};
```

Calibration rules 1–5 below apply unchanged in this lane (rule 3 re-verified in it). Upstream's own Storybook example omits the `finally` — don't copy that shape. Storybook 8 `@storybook/test-runner` setups are expected to work but were not run here. Validation record: `evals/results/virtual-screen-reader/harness/storybook/`.

### Calibration rules (measured 2026-07-11 at 0.32.1; environments noted)

1. **Never walk-to-end-of-document when `aria-modal="true"` is present** *(jsdom)*. The cursor traps inside the modal by design (upstream #54) — the walk never terminates. Scope `container` to the component and bound every walk with a max-step guard.
2. **A silent or short walk is not a clean pass — check for shadow roots first** *(jsdom)*. Open shadow DOM is invisible (upstream #182). If `element.shadowRoot` exists anywhere under the container, VSR evidence is partial: route to keyboard-a11y-tester or browser testing instead.
3. **Mount-with-content live regions read as silent — including correctly-fixed ones** *(jsdom AND Chromium — engine behavior, not a jsdom artifact)*. VSR announces mutations *inside* existing live regions (text changes, child insertions, mount-empty-then-fill) but not insertion of a pre-populated `role="alert"` element. Removal splits on `aria-atomic` *(measured, fixture sweep)*: clearing a non-atomic region is silent; clearing an `aria-atomic="true"` region announces an empty `"polite: "` phrase — an empty polite entry is a region-clear marker, not noise. Interpretive context (domain knowledge, not probed here): real screen readers are also inconsistent on pre-populated alert insertion, which is why robust toast guidance uses a persistent container. Consequences: assert via the persistent-container pattern; a silent log after mount-with-content of an alert is **inconclusive**, not proof the fix failed; buggy-component silence is defect evidence only alongside the structural fact (no role/aria-live present).
4. **Fake timers wedge the singleton — hard incompatibility** *(Vitest; Jest unmeasured, mechanism harness-independent)*. Under fake timers, `start()` resolves but log reads hang forever, and the wedged state cascades hangs into every later test in the file, teardown included. Never enable fake timers in a file that runs VSR. Components needing fake timers (auto-dismiss toasts) get announcement assertions in a separate real-timer file — natural with the persistent-container pattern (assert the announcement on show; the timed dismiss is a separate concern).
5. **Cite the VSR version in every piece of evidence** (`vsr@0.32.1 <test file>`). Both consumption routes are frozen (this exact pin; keyboard-a11y-tester's committed lockfile), so skew arises only on deliberate upgrade — the citation makes it detectable. Re-verify rules 1–4 on any version bump.

### Evidence

The artifacts are spoken-phrase logs plus the asserting test file — a11y-critic Phase 0 hard evidence (gate passed 2026-07-11: `evals/results/virtual-screen-reader/`; contract mapping in `docs/a11y-evidence-finding-contract.md`). Cite tool version + test file + the exact phrase or its absence, and pair silence with the structural fact (no role/aria-live present). Platform note: plain npm library — works from Claude Code and Codex.

