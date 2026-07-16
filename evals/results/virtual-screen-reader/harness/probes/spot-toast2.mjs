import { JSDOM } from "jsdom";
const dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`, { pretendToBeVisual: true, url: "https://fixture.local/" });
globalThis.window = dom.window; globalThis.document = dom.window.document;
for (const k of ["Node","Element","HTMLElement","MutationObserver","getComputedStyle"]) globalThis[k] = dom.window[k];
const { virtual } = await import("@guidepup/virtual-screen-reader");

async function capture(fn) {
  document.body.innerHTML = `<main><h1>Order page</h1><button>Save order</button></main>`;
  await virtual.start({ container: document.body });
  await virtual.next();
  const before = (await virtual.spokenPhraseLog()).length;
  await fn();
  await new Promise((r) => setTimeout(r, 150));
  const log = await virtual.spokenPhraseLog();
  await virtual.stop();
  return log.slice(before);
}

// A. Insert EMPTY role=alert, next tick set textContent (robust toast pattern)
const emptyThenFill = await capture(async () => {
  const t = document.createElement("div");
  t.setAttribute("role", "alert");
  document.body.appendChild(t);
  await new Promise((r) => setTimeout(r, 50));
  t.textContent = "Item saved";
});

// B. Pre-existing live container in initial DOM, insert a child node with content (aria-live parent pattern)
const intoExistingContainer = await capture(async () => {
  const region = document.createElement("div");
  region.setAttribute("aria-live", "assertive");
  document.body.appendChild(region);
  await new Promise((r) => setTimeout(r, 50));
  const child = document.createElement("p");
  child.textContent = "Item saved via child insertion";
  region.appendChild(child);
});

console.log(JSON.stringify({ emptyThenFill, intoExistingContainer }, null, 2));
