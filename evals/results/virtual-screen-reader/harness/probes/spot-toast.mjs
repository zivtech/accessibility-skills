// Spot-validation: VSR vs critic fixture toast-notification-no-role (must-finds 1+2).
// DOM-layer replication of the React component: toast = element inserted after load.
import { JSDOM } from "jsdom";
const dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`, { pretendToBeVisual: true, url: "https://fixture.local/" });
globalThis.window = dom.window; globalThis.document = dom.window.document;
for (const k of ["Node","Element","HTMLElement","MutationObserver","getComputedStyle"]) globalThis[k] = dom.window[k];
const { virtual } = await import("@guidepup/virtual-screen-reader");

async function mountToastAndCapture(makeToast) {
  document.body.innerHTML = `<main><h1>Order page</h1><button>Save order</button></main>`;
  await virtual.start({ container: document.body });
  await virtual.next(); // cursor engaged, simulating a user mid-page
  const before = (await virtual.spokenPhraseLog()).length;
  makeToast(); // the BuggyToast/FixedToast mount
  await new Promise((r) => setTimeout(r, 150));
  const log = await virtual.spokenPhraseLog();
  await virtual.stop();
  return log.slice(before);
}

// 1. BUGGY (fixture as written): plain div, no role, no aria-live
const buggy = await mountToastAndCapture(() => {
  const t = document.createElement("div");
  t.className = "toast-notification";
  t.textContent = "Item saved";
  document.body.appendChild(t);
});

// 2. FIXED (rubric's expected fix): role="alert" — implicit assertive live region, inserted like a real toast
const fixed = await mountToastAndCapture(() => {
  const t = document.createElement("div");
  t.className = "toast-notification";
  t.setAttribute("role", "alert");
  t.textContent = "Item saved";
  document.body.appendChild(t);
});

console.log(JSON.stringify({
  buggy_phrases_after_mount: buggy,   // expect: NO live announcement -> machine evidence for must-finds 1+2
  fixed_phrases_after_mount: fixed,   // expect: assertive announcement -> fix verified by same test
}, null, 2));
