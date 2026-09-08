// page-audit.mjs — one-pass, per-page, multi-rule accessibility auditor.
//
// PURPOSE
//   A human reviewer works a page, not a rule: they load it once and read
//   headings, control names, images, tables and landmarks in a single pass,
//   then dispose of every finding on that page from that one look. This module
//   is the machine form of that. `auditPage()` runs entirely in the page's own
//   JS context and returns evidence for FIVE scanner-rule classes at once, so a
//   whole surface is characterized in one capture instead of one probe per
//   element per rule. Use it as the DEFAULT rendered-context recon step before
//   adjudicating a page's scanner occurrences (see a11y-test SKILL.md,
//   "Batched one-pass per-page audit").
//
// WHAT IT IS NOT
//   Detector output, not a verdict. It reports the DOM + accessibility-tree
//   facts a scanner rule keys on (empty names, missing alt, layout tables,
//   missing landmarks, empty headings); it does NOT assign WCAG SCs, severity,
//   or pass/fail, and it is not keyboard-operability or screen-reader-
//   announcement evidence. Cross-check the accessible name it computes against
//   the browser's OWN computed AX name (Playwright: page.accessibility.snapshot();
//   agent-browser: snapshot -i; Chrome DevTools: the Accessibility pane) before
//   mapping an empty-name finding to a criterion — a UA may compute a name this
//   function's precedence walk does not. It applies the ARIA accessible-name
//   precedence (aria-labelledby > aria-label > content/alt/title); an
//   aria-labelledby that resolves to an EMPTY element yields an empty name and
//   does not fall back to content, which is the common false-name seam.
//
// HOW TO RUN
//   Playwright (in a .spec.js / .mjs, page loaded and settled):
//     import { AUDIT_PAGE_SRC } from './references/page-audit.mjs';
//     const report = await page.evaluate(AUDIT_PAGE_SRC);
//   agent-browser (conversational recon):
//     agent-browser eval "$(node -e "import('./references/page-audit.mjs').then(m=>console.log(m.AUDIT_PAGE_SRC))")"
//   In-session browser JS tool: paste the body of auditPage() and call it.
//
//   Run it once per bound page/state (each SPA route/query state is a distinct
//   page). Sweeping a 4-state app is 4 calls, not 4 x (rules) probes.

/** Runs in the page context. Returns a compact per-rule evidence summary. */
export function auditPage() {
  const vis = (el) => {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return {
      shown: !(el.hidden || cs.display === 'none' || cs.visibility === 'hidden' || el.getAttribute('aria-hidden') === 'true'),
      w: Math.round(r.width), h: Math.round(r.height),
    };
  };
  // ARIA accessible-name precedence: labelledby > label > content > title.
  // An existing-but-empty labelledby target yields '' (does NOT fall back).
  const accName = (el) => {
    const lb = el.getAttribute('aria-labelledby');
    if (lb) {
      const t = lb.split(/\s+/).map((id) => {
        const n = document.getElementById(id);
        return n ? (n.textContent || '').trim() : '';
      }).join(' ').trim();
      return { source: 'aria-labelledby', name: t };
    }
    const al = el.getAttribute('aria-label');
    if (al && al.trim()) return { source: 'aria-label', name: al.trim() };
    const txt = (el.textContent || '').replace(/\s+/g, ' ').trim();
    if (txt) return { source: 'content', name: txt };
    const title = el.getAttribute('title');
    if (title && title.trim()) return { source: 'title', name: title.trim() };
    return { source: 'none', name: '' };
  };

  // --- LANDMARKS / REGIONS (region_missing) ---
  const lmSel = 'main,[role=main],nav,[role=navigation],header,[role=banner],footer,[role=contentinfo],[role=region],aside,[role=complementary],[role=search]';
  const landmarks = [...document.querySelectorAll(lmSel)].filter((e) => vis(e).shown)
    .map((e) => ({ tag: e.tagName, role: e.getAttribute('role'), name: accName(e).name, id: e.id }));

  // --- HEADINGS (heading_empty) ---
  const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6,[role=heading]')].map((h) => {
    const v = vis(h);
    return { tag: h.tagName, name: accName(h).name, shown: v.shown, outer: h.outerHTML.slice(0, 120) };
  });
  const emptyVisibleHeadings = headings.filter((h) => h.shown && h.name.trim() === '');

  // --- CONTROL NAMES (button_empty and other empty-name controls) ---
  const controls = [...document.querySelectorAll('button,[role=button],input[type=button],input[type=submit],a[href]')]
    .filter((b) => { const v = vis(b); return v.shown && b.getAttribute('aria-hidden') !== 'true' && b.tabIndex >= 0; });
  const emptyNameControls = controls.filter((b) => accName(b).name === '')
    .map((b) => ({ tag: b.tagName, role: b.getAttribute('role'), id: b.id, cls: (b.className || '').toString().slice(0, 40), box: (() => { const r = b.getBoundingClientRect(); return `${Math.round(r.width)}x${Math.round(r.height)}`; })() }));

  // --- IMAGES (alt_missing) ---
  const imgs = [...document.querySelectorAll('img')];
  const imgAlt = (im) => { const a = im.getAttribute('alt'); return a === null ? 'MISSING' : (a.trim() === '' ? 'DECORATIVE' : 'TEXT'); };
  const altMissingMeaningful = imgs.map((im) => ({
    alt: imgAlt(im), role: im.getAttribute('role'), ariaHidden: im.getAttribute('aria-hidden'),
    labelled: im.getAttribute('aria-label') || im.getAttribute('aria-labelledby'), v: vis(im), src: (im.getAttribute('src') || '').slice(0, 70),
  })).filter((i) => i.alt === 'MISSING' && i.role !== 'presentation' && i.role !== 'none' && i.ariaHidden !== 'true' && !i.labelled && i.v.shown && i.v.w >= 8 && i.v.h >= 8);

  // --- TABLES (table_layout) ---
  const tables = [...document.querySelectorAll('table')].map((t) => {
    const v = vis(t); const role = t.getAttribute('role');
    const dataLike = !!t.querySelector('th,caption,[scope],[headers]') || role === 'table' || role === 'grid';
    return { shown: v.shown, ariaHidden: t.getAttribute('aria-hidden'), role, dataLike, presentation: (role === 'presentation' || role === 'none'), rows: t.rows ? t.rows.length : 0 };
  });
  const layoutTablesExposed = tables.filter((t) => t.shown && t.ariaHidden !== 'true' && !t.dataLike && !t.presentation);

  return {
    url: location.href,
    viewport: { w: window.innerWidth, h: window.innerHeight },
    region_missing: { hasMain: !!document.querySelector('main,[role=main]'), exposedLandmarks: landmarks.length, landmarks },
    heading_empty: { total: headings.length, emptyVisible: emptyVisibleHeadings },
    button_empty: { exposedActionable: controls.length, emptyName: emptyNameControls },
    alt_missing: { totalImages: imgs.length, missingMeaningful: altMissingMeaningful.length, sample: altMissingMeaningful.slice(0, 10) },
    table_layout: { total: tables.length, dataTables: tables.filter((t) => t.dataLike).length, layoutExposed: layoutTablesExposed.length, layoutRowsHisto: layoutTablesExposed.reduce((a, t) => { a[t.rows] = (a[t.rows] || 0) + 1; return a; }, {}) },
  };
}

// Stringified IIFE for page.evaluate() / eval — resolves to the report object.
export const AUDIT_PAGE_SRC = `(${auditPage.toString()})()`;
