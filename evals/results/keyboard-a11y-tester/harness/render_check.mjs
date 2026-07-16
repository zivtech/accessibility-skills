// Verify each built fixture page actually renders: root has content, no fatal JS errors.
import { chromium } from '/private/tmp/claude-501/-Users-AlexUA-1-claude-a11y-meta-skills/083549b3-a213-4de3-865a-02c09d7d8a7a/scratchpad/keyboard-a11y-tester/node_modules/playwright/index.mjs';
import fs from 'node:fs';

const PAGES = '/private/tmp/claude-501/-Users-AlexUA-1-claude-a11y-meta-skills/083549b3-a213-4de3-865a-02c09d7d8a7a/scratchpad/kat-eval/pages';
const BASE = 'http://127.0.0.1:8777';

const files = fs.readdirSync(PAGES).filter((f) => f.endsWith('.html')).sort();
const browser = await chromium.launch();
const ctx = await browser.newContext();
const results = [];
for (const f of files) {
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e).slice(0, 160)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().slice(0, 160)); });
  try {
    await page.goto(`${BASE}/${f}`, { waitUntil: 'load', timeout: 20000 });
    await page.waitForTimeout(2500); // babel transform + react mount
    const textLen = await page.evaluate(() => (document.getElementById('root')?.innerText || '').trim().length);
    const focusables = await page.evaluate(() =>
      document.querySelectorAll('a[href], button, input, select, textarea, [tabindex]').length);
    const fatal = errors.filter((e) => !e.includes('favicon') && !e.includes('Download the React DevTools') && !e.includes('404'));
    results.push({ f, textLen, focusables, errors: fatal.slice(0, 2) });
  } catch (e) {
    results.push({ f, textLen: -1, focusables: -1, errors: [String(e).slice(0, 160)] });
  }
  await page.close();
}
await browser.close();
for (const r of results) {
  const flag = r.textLen <= 0 || r.errors.length ? ' <-- CHECK' : '';
  console.log(`${r.f} text=${r.textLen} focusables=${r.focusables} err=${JSON.stringify(r.errors)}${flag}`);
}
