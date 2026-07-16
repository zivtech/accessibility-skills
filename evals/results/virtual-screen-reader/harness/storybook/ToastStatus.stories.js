// VSR-in-Storybook validation stories (adoption assessment, Storybook lane).
// Discipline over upstream's example: virtual.stop() in finally. Measured basis:
// after a play fails WITHOUT stop, the next story's start() recovers (no wedge),
// but the spoken-phrase log SURVIVES the restart — prior-story announcements
// bleed into later stories' assertions. finally-stop is log-integrity, not crash hygiene.
import { expect, userEvent, waitFor } from "storybook/test";
import { virtual } from "@guidepup/virtual-screen-reader";
import { ToastStatus } from "./ToastStatus";

export default {
  title: "Validation/ToastStatus",
  component: ToastStatus,
};

// 1. Headline: live-region announcement captured after a real click, in a play function.
export const AnnouncesOnSave = {
  play: async ({ canvasElement, canvas }) => {
    await virtual.start({ container: canvasElement });
    try {
      await userEvent.click(await canvas.findByRole("button", { name: "Save order" }));
      await waitFor(async () => {
        expect(await virtual.spokenPhraseLog()).toContain("polite: Item saved");
      });
    } finally {
      await virtual.stop();
    }
  },
};

// 2. Reading order via bounded walk (calibration rule 1: never while-true).
export const ReadingOrder = {
  play: async ({ canvasElement }) => {
    await virtual.start({ container: canvasElement });
    try {
      const phrases = [];
      for (let i = 0; i < 40; i++) {
        await virtual.next();
        const p = await virtual.lastSpokenPhrase();
        phrases.push(p);
        if (p === "end of main") break;
      }
      expect(phrases).toContain("heading, Order editor, level 2");
      expect(phrases.indexOf("$29.00")).toBeLessThan(phrases.indexOf("button, Save order"));
    } finally {
      await virtual.stop();
    }
  },
};

// 3. Calibration rule 3 transfer: a toast mounted WITH content + role=alert stays silent.
export const NaiveMountToastStaysSilent = {
  args: { naive: true },
  play: async ({ canvasElement, canvas }) => {
    await virtual.start({ container: canvasElement });
    try {
      const before = (await virtual.spokenPhraseLog()).length;
      await userEvent.click(await canvas.findByRole("button", { name: "Save order" }));
      await canvas.findByText("Item saved"); // toast IS in the DOM...
      await new Promise((r) => setTimeout(r, 150));
      const after = (await virtual.spokenPhraseLog()).slice(before);
      expect(after.filter((p) => p.includes("Item saved"))).toEqual([]); // ...but never announced
    } finally {
      await virtual.stop();
    }
  },
};

// 4. Story-to-story isolation: with the finally-stop discipline, no phrase leakage.
export const IsolationCheck = {
  play: async ({ canvasElement }) => {
    await virtual.start({ container: canvasElement });
    try {
      await virtual.next();
      const log = (await virtual.spokenPhraseLog()).join(" | ");
      expect(log).not.toContain("polite: Item saved"); // story 1's announcement must not leak here
    } finally {
      await virtual.stop();
    }
  },
};
