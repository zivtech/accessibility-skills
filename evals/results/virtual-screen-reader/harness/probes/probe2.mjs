import { JSDOM } from "jsdom";
const dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`, { pretendToBeVisual: true, url: "https://fixture.local/" });
globalThis.window = dom.window; globalThis.document = dom.window.document;
for (const k of ["Node","Element","HTMLElement","MutationObserver","getComputedStyle"]) globalThis[k] = dom.window[k];
const { virtual } = await import("@guidepup/virtual-screen-reader");

// Probe F: CSS-hidden content under jsdom — stylesheet class rules vs inline styles
document.body.innerHTML = `
  <style>.hide{display:none}.vhide{visibility:hidden}</style>
  <p>Shown</p>
  <p class="hide">Class display-none</p>
  <p class="vhide">Class visibility-hidden</p>
  <p style="display:none">Inline display-none</p>
  <p style="visibility:hidden">Inline visibility-hidden</p>
`;
await virtual.start({ container: document.body });
const phrases = [];
for (let i = 0; i < 25; i++) {
  await virtual.next();
  const p = await virtual.lastSpokenPhrase();
  phrases.push(p);
  if (p === "end of document") break;
}
console.log(JSON.stringify(phrases, null, 1));
await virtual.stop();
