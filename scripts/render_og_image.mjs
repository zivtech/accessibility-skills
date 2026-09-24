#!/usr/bin/env node
// Renders docs/og-image.png, the 1200x630 social-card image shared by every
// page on the GitHub Pages site (og:image / twitter:image).
//
// Usage: node scripts/render_og_image.mjs
// Needs Playwright with a Chromium build. Playwright is a peer tool here, not a
// repo dependency: install it in your own environment (npm i -g playwright) or
// point PLAYWRIGHT_MODULE at an existing install. Set CHROMIUM_PATH to use a
// specific browser binary.
//
// Colors come from docs/index.html's design tokens; fonts use local fallbacks
// so the render does not depend on network access.

import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.join(root, 'docs', 'og-image.png');

const pw = await import(process.env.PLAYWRIGHT_MODULE
  ? pathToFileURL(process.env.PLAYWRIGHT_MODULE).href
  : 'playwright');
const { chromium } = pw.default ?? pw;

const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><style>
  :root { --navy:#0f172a; --navy-mid:#1e293b; --navy-light:#334155; --teal:#0d9488; --teal-light:#ccfbf1; --slate-300:#cbd5e1; --white:#fff; }
  * { box-sizing:border-box; margin:0; }
  body { width:1200px; height:630px; background:var(--navy); color:var(--white);
         font-family:'Liberation Sans','DejaVu Sans',Helvetica,Arial,sans-serif;
         padding:72px 80px 64px; display:flex; flex-direction:column; }
  .eyebrow { font-family:'DejaVu Sans Mono','Liberation Mono',monospace; font-size:22px; letter-spacing:.06em;
             text-transform:uppercase; color:var(--teal-light); }
  h1 { font-family:Georgia,'DejaVu Serif','Liberation Serif',serif; font-size:92px; line-height:1.05; margin-top:28px; font-weight:700; }
  .sub { font-size:34px; line-height:1.35; color:var(--slate-300); margin-top:24px; max-width:1040px; }
  .badges { display:flex; flex-wrap:wrap; gap:12px; margin-top:auto; }
  .badge { font-family:'DejaVu Sans Mono','Liberation Mono',monospace; font-size:19px; padding:8px 14px;
           border:2px solid var(--navy-light); border-radius:8px; background:var(--navy-mid); color:var(--teal-light); }
  .foot { display:flex; justify-content:space-between; align-items:center; margin-top:32px;
          padding-top:24px; border-top:3px solid var(--teal); font-size:24px; color:var(--slate-300); }
  .foot strong { color:var(--white); }
</style></head><body>
  <div class="eyebrow">WCAG 2.2 AA · Section 508</div>
  <h1>Accessibility Skills</h1>
  <p class="sub">AI accessibility planning, testing, review, and audits for Claude&nbsp;Code</p>
  <div class="badges">
    <span class="badge">/a11y-planner</span><span class="badge">/a11y-critic</span>
    <span class="badge">/a11y-test</span><span class="badge">/perspective-audit</span>
    <span class="badge">/bug-reporting</span>
  </div>
  <div class="foot"><span>zivtech.github.io/accessibility-skills</span><span>Built by <strong>Zivtech</strong></span></div>
</body></html>`;

const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
await page.setContent(html);
await page.screenshot({ path: out, type: 'png' });
await browser.close();
console.log(`wrote ${path.relative(root, out)}`);
