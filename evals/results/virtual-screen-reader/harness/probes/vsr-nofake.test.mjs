// @vitest-environment jsdom
// Real-harness validation (critic MAJOR-1): VSR 0.32.1 inside Vitest's jsdom environment,
// no manual global wiring — the environment a consuming project would actually use.
import { afterEach, describe, expect, test, vi } from "vitest";
import { virtual } from "@guidepup/virtual-screen-reader";

afterEach(async () => {
  // Teardown discipline under test (critic Minor 4): stateful singleton must be stopped per test.
  await virtual.stop().catch(() => {});
  document.body.innerHTML = "";
});

describe("VSR in Vitest+jsdom (real harness)", () => {
  test("persistent-container toast pattern announces (real timers, taught template)", async () => {
    document.body.innerHTML = `
      <main><h1>Orders</h1><button>Save order</button></main>
      <div role="status" id="toast-region"></div>
    `;
    await virtual.start({ container: document.body });
    document.getElementById("toast-region").textContent = "Item saved";
    await new Promise((r) => setTimeout(r, 100));
    expect(await virtual.spokenPhraseLog()).toContain("polite: Item saved");
  });

  test("microtask-only flush: is the 100ms wait even needed?", async () => {
    document.body.innerHTML = `<div role="status" id="r"></div>`;
    await virtual.start({ container: document.body });
    document.getElementById("r").textContent = "Microtask check";
    await Promise.resolve(); // single microtask yield, no timer
    const afterMicrotask = (await virtual.spokenPhraseLog()).includes("polite: Microtask check");
    await new Promise((r) => setTimeout(r, 100));
    const afterTimer = (await virtual.spokenPhraseLog()).includes("polite: Microtask check");
    console.log(JSON.stringify({ afterMicrotask, afterTimer }));
    expect(afterTimer).toBe(true);
  });


  test("wrong-name evidence: aria-label overriding visible text is surfaced", async () => {
    document.body.innerHTML = `<button aria-label="Close">Save</button>`;
    await virtual.start({ container: document.body });
    await virtual.next();
    // ACCNAME: aria-label wins — a screen reader user hears "Close" on a button that shows "Save".
    expect(await virtual.lastSpokenPhrase()).toBe("button, Close");
  });

  test("teardown isolation: previous tests' phrases do not leak into this log", async () => {
    document.body.innerHTML = `<p>Fresh page</p>`;
    await virtual.start({ container: document.body });
    await virtual.next();
    const log = await virtual.spokenPhraseLog();
    expect(log.join(" ")).not.toContain("Item saved");
    expect(log.join(" ")).not.toContain("Under fake timers");
  });
});
