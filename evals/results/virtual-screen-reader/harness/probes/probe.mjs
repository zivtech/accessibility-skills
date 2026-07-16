// Hands-on probe of @guidepup/virtual-screen-reader 0.32.1 in plain Node + jsdom.
// Probes chosen for adoption-decision relevance:
//   A. unnamed icon button  -> does spoken output evidence a 4.1.2 defect?
//   B. aria-live mutation   -> is the announcement captured (CI-level 4.1.3 evidence)?
//   C. aria-modal dialog    -> is navigation contained (open issue #12 says no)?
//   D. aria-hidden          -> is hidden content excluded from the tree?
//   E. open shadow DOM      -> is shadow content reached (open issue #182 says no)?
import { JSDOM } from "jsdom";

const dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`, {
  pretendToBeVisual: true,
  url: "https://fixture.local/",
});

for (const key of [
  "window", "document", "Node", "Element", "HTMLElement", "HTMLInputElement",
  "MutationObserver", "getComputedStyle", "DOMParser", "CustomEvent", "KeyboardEvent",
  "navigator",
]) {
  if (!(key in globalThis) || key === "navigator") {
    try { globalThis[key] = dom.window[key] ?? dom.window; } catch { /* navigator readonly on some nodes */ }
  }
}
globalThis.window = dom.window;
globalThis.document = dom.window.document;

const { virtual } = await import("@guidepup/virtual-screen-reader");

const results = {};

async function walk(container, maxSteps = 40) {
  await virtual.start({ container });
  const phrases = [];
  for (let i = 0; i < maxSteps; i++) {
    await virtual.next();
    const phrase = await virtual.lastSpokenPhrase();
    phrases.push(phrase);
    if (phrase === "end of document") break;
  }
  return phrases;
}

// ---------- Probe A: unnamed icon-only button ----------
document.body.innerHTML = `
  <button><svg viewBox="0 0 16 16"><path d="M2 2h12v12H2z"/></svg></button>
  <button aria-label="Save document"><svg aria-hidden="true" viewBox="0 0 16 16"><path d="M2 2h12v12H2z"/></svg></button>
`;
results.A_unnamed_button = await walk(document.body);
await virtual.stop();

// ---------- Probe B: aria-live capture after real DOM mutation ----------
document.body.innerHTML = `
  <button id="save">Save</button>
  <div role="status" id="polite-region"></div>
  <div aria-live="assertive" id="assertive-region"></div>
`;
await virtual.start({ container: document.body });
await virtual.next(); // move off container
document.getElementById("polite-region").textContent = "Draft saved";
document.getElementById("assertive-region").textContent = "Session expired";
await new Promise((r) => setTimeout(r, 100)); // let MutationObserver flush
results.B_live_region_log = await virtual.spokenPhraseLog();
await virtual.stop();

// ---------- Probe C: aria-modal containment ----------
document.body.innerHTML = `
  <button id="outside-before">Outside before</button>
  <div role="dialog" aria-modal="true" aria-label="Confirm delete">
    <h2>Confirm delete</h2>
    <button>Cancel</button>
    <button>Delete</button>
  </div>
  <button id="outside-after">Outside after</button>
`;
results.C_modal_walk = await walk(document.body);
await virtual.stop();

// ---------- Probe D: aria-hidden exclusion ----------
document.body.innerHTML = `
  <p>Visible text</p>
  <p aria-hidden="true">Decorative hidden text</p>
  <p>More visible text</p>
`;
results.D_aria_hidden_walk = await walk(document.body);
await virtual.stop();

// ---------- Probe E: open shadow DOM ----------
document.body.innerHTML = `<p>Light DOM text</p><div id="host"></div><p>After host</p>`;
const host = document.getElementById("host");
const shadow = host.attachShadow({ mode: "open" });
shadow.innerHTML = `<button>Shadow button</button><p>Shadow paragraph</p>`;
results.E_shadow_walk = await walk(document.body);
await virtual.stop();

console.log(JSON.stringify(results, null, 2));
