// @vitest-environment jsdom
import { test, vi } from "vitest";
import { virtual } from "@guidepup/virtual-screen-reader";

test("pinpoint fake-timer hang", { timeout: 8000 }, async () => {
  vi.useFakeTimers();
  document.body.innerHTML = `<div aria-live="assertive" id="r"></div>`;
  console.log("1: before start");
  const startP = virtual.start({ container: document.body });
  const raced = await Promise.race([startP, new Promise((r) => setTimeout(r, 1000, "START_HUNG"))]);
  console.log("2: start resolved?", raced === "START_HUNG" ? "HUNG" : "ok");
  if (raced !== "START_HUNG") {
    document.getElementById("r").textContent = "Under fake timers";
    await Promise.resolve();
    console.log("3: log after microtask:", JSON.stringify(await Promise.race([
      virtual.spokenPhraseLog(), new Promise((r) => setTimeout(r, 1000, "LOG_HUNG")),
    ])));
  }
  vi.useRealTimers();
  console.log("4: after real timers restored, stop:", await Promise.race([
    virtual.stop().then(() => "stopped"), new Promise((r) => setTimeout(r, 2000, "STOP_HUNG")),
  ]));
});
