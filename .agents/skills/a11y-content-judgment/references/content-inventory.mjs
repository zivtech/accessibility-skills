#!/usr/bin/env node
// content-inventory.mjs — a11y-content-judgment, step 1 (inventory).
// For every URL in a list, at one viewport, captures the content a person
// relies on to orient and navigate: page title, headings (with a section
// preview), links in context, images with their alternatives, form fields
// with their computed labels, and the ordered link map of every navigation
// landmark. Nothing is activated. The output feeds build-judgment-rows.mjs.
// It is not coverage, not a scan result, and never a criterion outcome.
// Read-only public GETs, one worker, reducedMotion=reduce, 90s nav budget.
//
// Usage:
//   node content-inventory.mjs --urls-file views.txt --out ./content-inventory
//   node content-inventory.mjs --out ./out https://example.gov/ https://example.gov/about
// urls-file lines: `url` | `id<TAB>url` | `id,product,url[,settle_ms]`; `#` starts a comment.
// Options: --settle <ms> (default 2600) --viewport WxH (default 1440x900) --only ID,ID
//          --product <name> --engagement <label> --no-screenshots
// Peer dependency: playwright (resolved from the current working directory).
import { createHash } from 'node:crypto';
import fs from 'node:fs/promises';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const argv = process.argv.slice(2);
const argAfter = (flag) => (argv.includes(flag) ? argv[argv.indexOf(flag) + 1] : null);
const outDir = path.resolve(argAfter('--out') || './content-inventory-output');
await fs.mkdir(outDir, { recursive: true });
const DEFAULT_SETTLE = Number(argAfter('--settle') || 2600);
const [vw, vh] = (argAfter('--viewport') || '1440x900').split('x').map(Number);
const VIEWPORT = { id: `desktop-${vw}`, width: vw, height: vh };
const only = argAfter('--only')?.split(',') ?? null;
const productFilter = argAfter('--product');
const engagement = argAfter('--engagement') || null;
const screenshots = !argv.includes('--no-screenshots');
if (screenshots) await fs.mkdir(path.join(outDir, 'screenshots'), { recursive: true });
const NAV_TIMEOUT = Number(argAfter('--nav-timeout') || 90000);
const CAPS = { headings: 250, links: 500, images: 250, fields: 120, nav_links: 120 };

function parseViews() {
  const views = []; const file = argAfter('--urls-file');
  const add = (id, product, url, settle) => views.push({ view_id: id, product: product || (() => { try { return new URL(url).host; } catch { return 'unknown'; } })(), canonical_url: url, settle: settle ? Number(settle) : DEFAULT_SETTLE });
  if (file) {
    const lines = require_lines(file);
    lines.forEach((line, i) => {
      if (line.includes(',')) { const [id, product, url, settle] = line.split(',').map((x) => x.trim()); add(id || `V-${i + 1}`, product, url, settle); }
      else if (line.includes('\t')) { const [id, url] = line.split('\t').map((x) => x.trim()); add(id, null, url, null); }
      else add(`V-${String(i + 1).padStart(3, '0')}`, null, line.trim(), null);
    });
  }
  let positional = false;
  for (const a of argv) { if (a.startsWith('--')) { positional = ['--no-screenshots'].includes(a); continue; } if (positional || /^https?:\/\//.test(a)) { if (/^https?:\/\//.test(a)) add(`V-${String(views.length + 1).padStart(3, '0')}`, null, a, null); } }
  return views.filter((v) => (!only || only.includes(v.view_id)) && (!productFilter || v.product === productFilter));
}
function require_lines(file) { return readFileSync(file, 'utf8').split('\n').map((l) => l.trim()).filter((l) => l && !l.startsWith('#')); }
const VIEWS = parseViews();
if (!VIEWS.length) { console.error('No URLs. Pass --urls-file <path> or positional https:// URLs.'); process.exit(2); }

function inventory(CAPS) {
  const norm = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const clip = (s, n) => { s = norm(s); return s.length > n ? s.slice(0, n - 1) + '…' : s; };
  const visible = (el) => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const ariaHiddenAncestor = (el) => !!el.closest('[aria-hidden="true"]');
  const cssPath = (el) => {
    if (el.id) return `#${CSS.escape(el.id)}`;
    const parts = []; let cur = el; let depth = 0;
    while (cur && cur.nodeType === 1 && depth < 6) {
      let part = cur.tagName.toLowerCase();
      if (cur.id) { parts.unshift(`#${CSS.escape(cur.id)}`); break; }
      const parent = cur.parentElement;
      if (parent) { const sibs = [...parent.children].filter((c) => c.tagName === cur.tagName); if (sibs.length > 1) part += `:nth-of-type(${sibs.indexOf(cur) + 1})`; }
      parts.unshift(part); cur = parent; depth += 1;
    }
    return parts.join(' > ');
  };
  const landmark = (el) => {
    const l = el.closest('header,nav,main,footer,aside,[role=banner],[role=navigation],[role=main],[role=contentinfo],[role=dialog],[role=search],[role=complementary],form');
    if (!l) return null;
    const role = l.getAttribute('role') || l.tagName.toLowerCase();
    const label = (l.getAttribute('aria-labelledby') ? norm(document.getElementById(l.getAttribute('aria-labelledby'))?.textContent) : null) || l.getAttribute('aria-label');
    return label ? `${role}[${clip(label, 40)}]` : role;
  };
  const labelledBy = (el) => { const lb = el.getAttribute('aria-labelledby'); if (!lb) return ''; return norm(lb.split(/\s+/).map((id) => document.getElementById(id)).filter(Boolean).map((n) => n.textContent).join(' ')); };
  const imgAltIn = (el) => { const i = el.querySelector('img[alt], svg[aria-label], [role=img][aria-label]'); return i ? norm(i.getAttribute('alt') || i.getAttribute('aria-label')) : ''; };
  // Accessible-name approximation. Order follows accname for these cases; not a full computation.
  const accName = (el) => {
    const lb = labelledBy(el); if (lb) return { name: lb, source: 'aria-labelledby' };
    const al = norm(el.getAttribute('aria-label')); if (al) return { name: al, source: 'aria-label' };
    const t = norm(el.textContent); if (t) return { name: t, source: 'content' };
    const ia = imgAltIn(el); if (ia) return { name: ia, source: 'img-alt' };
    const ti = norm(el.getAttribute('title')); if (ti) return { name: ti, source: 'title' };
    return { name: '', source: 'none' };
  };
  const BLOCK = 'p,li,td,th,dd,dt,figcaption,h1,h2,h3,h4,h5,h6,blockquote,label,summary,article,section,div';
  const blockContext = (el, n) => {
    let cur = el.parentElement; let hops = 0;
    while (cur && hops < 6) { if (cur.matches(BLOCK)) { const t = norm(cur.textContent); if (t.length > norm(el.textContent).length + 3) return clip(t, n); } cur = cur.parentElement; hops += 1; }
    return '';
  };
  const nextText = (el, n) => {
    let cur = el.nextElementSibling; let hops = 0;
    while (cur && hops < 4) { const t = norm(cur.textContent); if (t) return clip(t, n); cur = cur.nextElementSibling; hops += 1; }
    const p = el.parentElement; if (p) { const t = norm(p.textContent).replace(norm(el.textContent), '').trim(); if (t) return clip(t, n); }
    return '';
  };
  const headingsSel = 'h1,h2,h3,h4,h5,h6,[role=heading]';
  const headings = []; let hi = 0;
  for (const el of document.querySelectorAll(headingsSel)) {
    if (headings.length >= CAPS.headings) break;
    const level = el.getAttribute('aria-level') ? Number(el.getAttribute('aria-level')) : Number(el.tagName[1]) || null;
    const nm = accName(el);
    headings.push({ i: hi++, level, text: clip(nm.name, 200), name_source: nm.source, selector: cssPath(el), visible: visible(el), aria_hidden: ariaHiddenAncestor(el), landmark: landmark(el), section_preview: nextText(el, 200) });
  }
  const links = []; let li = 0; let linksTotal = 0;
  for (const el of document.querySelectorAll('a[href],[role=link]')) {
    linksTotal += 1; if (links.length >= CAPS.links) continue;
    const hrefRaw = el.getAttribute('href') || '';
    let href = hrefRaw; try { href = new URL(hrefRaw, location.href).href; } catch {}
    const nm = accName(el);
    const txt = norm(el.textContent);
    const img = el.querySelector('img,svg,[role=img]');
    links.push({ i: li++, name: clip(nm.name, 160), name_source: nm.source, text: clip(txt, 160), title: clip(el.getAttribute('title'), 120) || null, href: clip(href, 240), href_raw: clip(hrefRaw, 120),
      same_page: hrefRaw.startsWith('#'), external: (() => { try { return new URL(href).host !== location.host; } catch { return false; } })(), target: el.getAttribute('target') || null,
      download: el.hasAttribute('download'), file_ext: (href.match(/\.(pdf|xlsx?|csv|docx?|pptx?|zip|json|xml|txt|sdf|mol|png|jpe?g|gif|svg|mp4)(?:$|[?#])/i) || [])[1]?.toLowerCase() || null,
      has_img: !!img, img_alt: img ? (img.getAttribute('alt') ?? img.getAttribute('aria-label') ?? null) : null,
      icon_only: !txt && !!img, empty_name: !nm.name, visible: visible(el), aria_hidden: ariaHiddenAncestor(el), landmark: landmark(el), selector: cssPath(el), context: blockContext(el, 220) });
  }
  const images = []; let ii = 0; let imagesTotal = 0;
  for (const el of document.querySelectorAll('img,svg,[role=img],input[type=image],area,picture,canvas,object[type^="image"],video')) {
    if (el.tagName === 'PICTURE') continue;
    if (el.tagName === 'SVG' && el.closest('svg') !== el) continue; // nested svg
    imagesTotal += 1; if (images.length >= CAPS.images) continue;
    const tag = el.tagName.toLowerCase();
    const alt = el.hasAttribute('alt') ? el.getAttribute('alt') : null;
    const a = el.closest('a[href],button,[role=button],[role=link]');
    const fig = el.closest('figure'); const cap = fig ? norm(fig.querySelector('figcaption')?.textContent) : '';
    const r = el.getBoundingClientRect();
    const src = el.getAttribute('src') || el.getAttribute('data-src') || (tag === 'svg' ? '(inline svg)' : '') || '';
    images.push({ i: ii++, tag, src: clip(src.startsWith('data:') ? 'data:…' : src, 160), src_basename: clip((src.split('?')[0].split('/').pop() || ''), 80),
      alt, alt_present: alt !== null, alt_empty: alt === '', role: el.getAttribute('role') || null, aria_label: clip(el.getAttribute('aria-label'), 160) || null, aria_labelledby_text: clip(labelledBy(el), 160) || null,
      aria_hidden: el.getAttribute('aria-hidden') === 'true' || ariaHiddenAncestor(el), title: clip(el.getAttribute('title'), 120) || null,
      svg_title: tag === 'svg' ? clip(el.querySelector('title')?.textContent, 120) || null : null,
      in_control: a ? { tag: a.tagName.toLowerCase(), name: clip(accName(a).name, 120), href: a.getAttribute('href') ? clip(a.getAttribute('href'), 120) : null, control_has_text: !!norm([...a.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join(' ')) || !!norm(a.textContent).replace(norm(el.textContent), '') } : null,
      figcaption: clip(cap, 160) || null, width: Math.round(r.width), height: Math.round(r.height), visible: visible(el), landmark: landmark(el), selector: cssPath(el), adjacent_text: blockContext(el, 200) });
  }
  const fields = []; let fi = 0;
  for (const el of document.querySelectorAll('input:not([type=hidden]),select,textarea')) {
    if (fields.length >= CAPS.fields) break;
    const type = el.tagName === 'INPUT' ? (el.getAttribute('type') || 'text') : el.tagName.toLowerCase();
    if (['submit', 'button', 'reset', 'image'].includes(type)) continue;
    const forLabel = el.id ? norm([...document.querySelectorAll(`label[for="${CSS.escape(el.id)}"]`)].map((l) => l.textContent).join(' ')) : '';
    const wrap = el.closest('label') ? norm(el.closest('label').textContent) : '';
    const al = norm(el.getAttribute('aria-label')); const lb = labelledBy(el);
    const label = al || lb || forLabel || wrap || '';
    const source = al ? 'aria-label' : lb ? 'aria-labelledby' : forLabel ? 'label[for]' : wrap ? 'wrapping-label' : el.getAttribute('placeholder') ? 'placeholder-only' : el.getAttribute('title') ? 'title-only' : 'none';
    fields.push({ i: fi++, type, name_attr: el.getAttribute('name') || null, id: el.id || null, label: clip(label, 160), label_source: source, placeholder: clip(el.getAttribute('placeholder'), 120) || null, required: el.required || el.getAttribute('aria-required') === 'true', describedby_text: clip(norm((el.getAttribute('aria-describedby') || '').split(/\s+/).map((id) => document.getElementById(id)?.textContent).join(' ')), 160) || null, fieldset_legend: clip(el.closest('fieldset')?.querySelector('legend')?.textContent, 120) || null, visible: visible(el), landmark: landmark(el), selector: cssPath(el) });
  }
  const navs = [];
  for (const el of document.querySelectorAll('nav,[role=navigation],header,[role=banner],footer,[role=contentinfo],[aria-label*="breadcrumb" i],.breadcrumb,.usa-breadcrumb')) {
    if (el.tagName === 'HEADER' && el.closest('nav')) continue;
    const role = el.getAttribute('role') || el.tagName.toLowerCase();
    const label = norm(el.getAttribute('aria-label')) || labelledBy(el) || '';
    const items = [...el.querySelectorAll('a[href],[role=link],button,[role=menuitem]')].slice(0, CAPS.nav_links).map((a) => ({ name: clip(accName(a).name, 80), href: a.getAttribute('href') ? clip(a.getAttribute('href'), 120) : null, tag: a.tagName.toLowerCase() }));
    navs.push({ role, label: clip(label, 80) || null, selector: cssPath(el), visible: visible(el), item_count: items.length, items });
  }
  const skip = [...document.querySelectorAll('a[href^="#"]')].filter((a) => /skip/i.test(norm(a.textContent) + (a.getAttribute('aria-label') || ''))).map((a) => ({ name: clip(accName(a).name, 80), href: a.getAttribute('href'), target_exists: !!document.querySelector(a.getAttribute('href') === '#' ? 'body' : a.getAttribute('href')) }));
  const html = document.documentElement;
  const meta = { lang: html.getAttribute('lang'), title: document.title, h1: [...document.querySelectorAll('h1')].map((h) => clip(h.textContent, 160)), h1_count: document.querySelectorAll('h1').length, meta_description: clip(document.querySelector('meta[name=description]')?.getAttribute('content'), 200) || null, main_count: document.querySelectorAll('main,[role=main]').length, search_landmark: !!document.querySelector('[role=search],form[role=search]'), skip_links: skip };
  const counts = { headings: headings.length, headings_visible: headings.filter((h) => h.visible).length, links: links.length, links_total: linksTotal, links_visible: links.filter((l) => l.visible).length, links_empty_name: links.filter((l) => l.empty_name).length, images: images.length, images_total: imagesTotal, images_missing_alt: images.filter((m) => m.tag === 'img' && !m.alt_present).length, images_empty_alt: images.filter((m) => m.alt_empty).length, fields: fields.length, fields_unlabeled: fields.filter((f) => !f.label).length, navs: navs.length };
  return { meta, counts, headings, links, images, fields, navs, capped: { headings: headings.length >= CAPS.headings, links: linksTotal > CAPS.links, images: imagesTotal > CAPS.images, fields: fields.length >= CAPS.fields } };
}

const browser = await chromium.launch({ headless: true });
const started = new Date().toISOString();
const views = [];
for (const view of VIEWS) {
  const context = await browser.newContext({ viewport: { width: VIEWPORT.width, height: VIEWPORT.height }, locale: 'en-US', reducedMotion: 'reduce' });
  const page = await context.newPage();
  let navError = null; const t0 = Date.now();
  try {
    await page.goto(view.canonical_url, { waitUntil: 'domcontentloaded', timeout: NAV_TIMEOUT });
    await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(view.settle);
  } catch (e) { navError = String(e).slice(0, 200); }
  const finalUrl = page.url();
  let onHost = false; try { onHost = new URL(finalUrl).host === new URL(view.canonical_url).host; } catch {}
  const rec = { view_id: view.view_id, product: view.product, url: view.canonical_url, viewport: VIEWPORT.id, nav_error: navError, final_url: finalUrl, stayed_on_route_host: onHost, load_ms: Date.now() - t0, inventory: null, screenshot: null };
  if (!navError && onHost) {
    rec.inventory = await page.evaluate(inventory, CAPS).catch((e) => ({ error: String(e).slice(0, 300) }));
    if (screenshots) { const shot = `screenshots/${view.view_id}__${VIEWPORT.id}.png`; await page.screenshot({ path: path.join(outDir, shot) }).catch(() => {}); rec.screenshot = shot; }
  }
  const c = rec.inventory?.counts;
  console.log(`${view.view_id}: ${navError ? 'NAV-ERROR ' + navError.slice(0, 80) : rec.inventory?.error ? 'EVAL-ERROR ' + rec.inventory.error : c ? `title="${rec.inventory.meta.title.slice(0, 50)}" h=${c.headings} links=${c.links}/${c.links_total} (empty ${c.links_empty_name}) imgs=${c.images}/${c.images_total} (noalt ${c.images_missing_alt}, alt="" ${c.images_empty_alt}) fields=${c.fields} (unlabeled ${c.fields_unlabeled}) navs=${c.navs}` : 'no inventory'} (${rec.load_ms}ms)`);
  views.push(rec);
  await context.close();
}
await browser.close();
const manifest = {
  schema: 'content-inventory/v1', engagement,
  run_started_utc: started, run_finished_utc: new Date().toISOString(),
  what_this_is: 'Content inventory (title, headings, links in context, images with alternatives, form labels, navigation link maps) for each listed URL at one viewport. Nothing was activated. Substrate for the draft-judgment pass; it is not coverage, not a scan result, and never a criterion outcome.',
  method_boundary: [
    'Accessible names are a DOM approximation (aria-label > aria-labelledby > text content > img alt > title), not a full accname computation.',
    'Link context is the nearest enclosing text block (p/li/td/dd/label/section/div) clipped to 220 chars; heading section_preview is the next sibling text clipped to 200 chars.',
    'Per-view caps: headings 250, links 500, images 250, fields 120, nav items 120 per landmark; capped views are flagged in `capped` and the true totals are recorded.',
    'One viewport. Navigation surfaces hidden at this width share the same DOM and are captured with visible:false.',
    'Read-only public GETs; one worker; reducedMotion=reduce; navigation budget as configured; a navigation error is an environment note, never product evidence.',
  ],
  urls_source: argAfter('--urls-file') || 'argv', viewport: VIEWPORT, caps: CAPS, view_count: views.length, views,
};
await fs.writeFile(path.join(outDir, 'inventory-run.json'), JSON.stringify(manifest, null, 1));
console.log('inventory-run.json sha256', createHash('sha256').update(JSON.stringify(manifest)).digest('hex'), 'views', views.length);
