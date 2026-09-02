#!/usr/bin/env node
// build-judgment-rows.mjs — a11y-content-judgment, step 2 (units + heuristics) and step 4 (merge).
//   --build : inventory-run.json -> judgment-units.json + batches/*.jsonl (judge worklists)
//   --merge : batches/*.judged.jsonl + judgment-units.json -> draft-judgments.json + CSVs
// Usage: node build-judgment-rows.mjs --build [--inventory <dir-or-file>] [--batch 90]
//        node build-judgment-rows.mjs --merge [--inventory <dir-or-file>]
// Deterministic heuristics are recorded as flags on every unit so the ratifier can see the
// machine's reasons separately from the model's judgment. Nothing here is a criterion outcome.
import { createHash } from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';

const argv = process.argv.slice(2);
const argAfter = (flag) => (argv.includes(flag) ? argv[argv.indexOf(flag) + 1] : null);
const invArg = path.resolve(argAfter('--inventory') || './content-inventory-output');
const dir = invArg.endsWith('.json') ? path.dirname(invArg) : invArg;
const invPath = invArg.endsWith('.json') ? invArg : path.join(invArg, 'inventory-run.json');
const argv_has = (f) => argv.includes(f);
const mode = argv.includes('--merge') ? 'merge' : 'build';
const BATCH = Number(argAfter('--batch') || 90);
const sha = (s) => createHash('sha256').update(s).digest('hex');
const norm = (s) => (s || '').toLowerCase().replace(/\s+/g, ' ').trim();
const GENERIC_LINK = /^(click here|here|read more|learn more|more|link|this page|this|download|view|details|go|see more|more info|info|continue|next|previous|back|home page|website|open|full article|full story|page)$/i;
const GENERIC_HEADING = /^(overview|details|detail|more|information|info|section|untitled|content|title|heading|description|summary|misc|other|general|notes?)$/i;
const GENERIC_ALT = /^(image|photo|picture|icon|logo|graphic|img|figure|banner|thumbnail|arrow|chevron|bullet|spacer|placeholder)$/i;
const FILE_WORDS = /pdf|xlsx?|excel|csv|zip|word|docx?|spreadsheet|download|kb|mb/i;
const NEW_WIN = /new (window|tab)|opens? in/i;
const urlPath = (h) => { try { const u = new URL(h); return (u.host + u.pathname).replace(/\/$/, '') + (u.search || '') + (u.hash || ''); } catch { return norm(h); } };
const PSEUDO_HREF = /^(javascript:|#?$|void\(0\))/i;

const push = (m, k, v) => { (m[k] ??= []).push(v); };
function unitId(type, product, key) { return `${type.toUpperCase()}-${product.slice(0, 2).toUpperCase()}-${sha(`${type}|${product}|${key}`).slice(0, 10)}`; }

function titleUnits(views) {
  const byProduct = {}; views.forEach((v) => push(byProduct, v.product, v));
  const out = [];
  for (const [product, vs] of Object.entries(byProduct)) {
    const titleCount = {}; vs.forEach((v) => { titleCount[norm(v.inventory.meta.title)] = (titleCount[norm(v.inventory.meta.title)] || 0) + 1; });
    for (const v of vs) {
      const m = v.inventory.meta; const t = m.title || ''; const flags = [];
      if (!t.trim()) flags.push('title_empty');
      if (titleCount[norm(t)] > 1) flags.push(`title_shared_by_${titleCount[norm(t)]}_views`);
      const h1 = (m.h1 || []).filter(Boolean); const h1Words = new Set(norm(h1.join(' ')).split(/\W+/).filter((w) => w.length > 3));
      if (h1.length && ![...h1Words].some((w) => norm(t).includes(w))) flags.push('title_shares_no_word_with_h1');
      if (m.h1_count === 0) flags.push('no_h1'); if (m.h1_count > 1) flags.push(`h1_count_${m.h1_count}`); if ((m.h1 || []).some((x) => !x)) flags.push('empty_h1');
      if (t.length > 120) flags.push('title_over_120');
      out.push({ id: unitId('title', product, v.view_id), type: 'title', sc: '2.4.2', product, views: [v.view_id], view_count: 1, name: t, detail: `h1: ${h1.join(' | ') || '(none)'}`, context: m.meta_description || '', landmark: null, selector: 'title', visible: true, href: v.url, flags });
    }
  }
  return out;
}

function headingUnits(views) {
  const map = {};
  for (const v of views) {
    const seenLevels = []; const textCount = {};
    v.inventory.headings.forEach((h) => { textCount[`${h.level}|${norm(h.text)}`] = (textCount[`${h.level}|${norm(h.text)}`] || 0) + 1; });
    for (const h of v.inventory.headings) {
      const flags = [];
      if (!h.text) flags.push('heading_empty');
      if (GENERIC_HEADING.test(h.text)) flags.push('heading_generic');
      if (/^[\d.,%\s-]+$/.test(h.text) && h.text) flags.push('heading_numeric_only');
      if (h.text.length > 120) flags.push('heading_over_120');
      if (textCount[`${h.level}|${norm(h.text)}`] > 1) flags.push('heading_repeated_in_page');
      const last = seenLevels[seenLevels.length - 1]; if (last && h.level > last + 1) flags.push(`level_skip_h${last}_to_h${h.level}`); if (h.level) seenLevels.push(h.level);
      if (h.name_source !== 'content') flags.push(`name_from_${h.name_source}`);
      const key = `${h.level}|${norm(h.text)}|${h.landmark || ''}`;
      const u = (map[`${v.product}|${key}`] ??= { id: unitId('heading', v.product, key), type: 'heading', sc: '2.4.6', product: v.product, views: [], view_count: 0, name: h.text, detail: `h${h.level}`, context: h.section_preview, landmark: h.landmark, selector: h.selector, visible: h.visible, href: null, flags: new Set() });
      u.views.push(v.view_id); u.view_count += 1; flags.forEach((f) => u.flags.add(f)); if (!u.context && h.section_preview) u.context = h.section_preview; if (h.visible) u.visible = true;
    }
  }
  return Object.values(map).map((u) => ({ ...u, flags: [...u.flags] }));
}

function linkUnits(views) {
  const map = {};
  for (const v of views) {
    const nameToHref = {}; v.inventory.links.forEach((l) => { (nameToHref[norm(l.name)] ??= new Set()).add(urlPath(l.href)); });
    for (const l of v.inventory.links) {
      const flags = [];
      if (l.empty_name) flags.push('link_empty_name');
      if (GENERIC_LINK.test(l.name)) flags.push('link_generic_text');
      if (l.name && (norm(l.name) === norm(l.href) || norm(l.name) === norm(l.href_raw) || /^https?:\/\//i.test(l.name))) flags.push('link_name_is_url');
      if (l.file_ext && !FILE_WORDS.test(l.name) && !FILE_WORDS.test(l.context || '')) flags.push(`file_${l.file_ext}_not_indicated`);
      if (l.target === '_blank' && !NEW_WIN.test(l.name) && !NEW_WIN.test(l.title || '')) flags.push('new_window_not_indicated');
      if (l.icon_only && (!l.img_alt || GENERIC_ALT.test(l.img_alt))) flags.push('icon_only_link_weak_alt');
      if (l.name && nameToHref[norm(l.name)].size > 1) flags.push('same_name_different_hrefs_in_page');
      if (l.title && norm(l.title) === norm(l.text)) flags.push('title_duplicates_text');
      if (l.name_source === 'title') flags.push('name_from_title_only');
      if (l.same_page && !l.href_raw.slice(1)) flags.push('href_hash_only');
      const key = `${norm(l.name)}|${urlPath(l.href)}|${sha(norm(l.context).slice(0, 120)).slice(0, 8)}`;
      const u = (map[`${v.product}|${key}`] ??= { id: unitId('link', v.product, key), type: 'link', sc: '2.4.4', product: v.product, views: [], view_count: 0, name: l.name, detail: `${l.name_source}${l.icon_only ? '; icon-only alt=' + JSON.stringify(l.img_alt) : ''}${l.file_ext ? '; file ' + l.file_ext : ''}${l.external ? '; external' : ''}${l.target === '_blank' ? '; new window' : ''}${l.title ? '; title=' + JSON.stringify(l.title) : ''}`, context: l.context, landmark: l.landmark, selector: l.selector, visible: l.visible, href: l.href, flags: new Set() });
      u.views.push(v.view_id); u.view_count += 1; flags.forEach((f) => u.flags.add(f)); if (l.visible) u.visible = true;
    }
  }
  return Object.values(map).map((u) => ({ ...u, flags: [...u.flags] }));
}

function imageUnits(views) {
  const map = {};
  for (const v of views) {
    for (const m of v.inventory.images) {
      const flags = []; const alt = m.alt; const functional = m.in_control && !m.in_control.control_has_text;
      const role = functional ? 'functional' : (m.aria_hidden || m.alt_empty || m.role === 'presentation' || m.role === 'none') ? 'decorative-declared' : 'informative?';
      if (m.tag === 'img' && !m.alt_present) flags.push('img_missing_alt_attr');
      if (alt && GENERIC_ALT.test(alt.trim())) flags.push('alt_generic');
      if (alt && (/\.(png|jpe?g|gif|svg|webp)$/i.test(alt.trim()) || norm(alt) === norm(m.src_basename.replace(/\.[a-z0-9]+$/i, '')))) flags.push('alt_is_filename');
      if (alt && alt.length > 150) flags.push('alt_over_150');
      if (functional && (m.alt_empty || (!alt && !m.aria_label && !m.aria_labelledby_text)) && !m.in_control.name) flags.push('functional_image_no_name');
      if (functional && alt && norm(alt) === norm(m.in_control.name) && m.in_control.control_has_text) flags.push('alt_duplicates_control_text');
      if (!functional && alt && m.adjacent_text && norm(m.adjacent_text).startsWith(norm(alt))) flags.push('alt_repeats_adjacent_text');
      if (m.tag === 'svg' && !m.svg_title && !m.aria_label && !m.aria_hidden && m.role !== 'presentation') flags.push('svg_unnamed_not_hidden');
      if ((m.tag === 'canvas' || /map|chart|graph|plot|structure|gauge|legend/i.test(`${m.src_basename} ${alt || ''}`)) && (!alt || alt.length < 40) && !m.figcaption) flags.push('complex_image_short_alt');
      if (m.width && m.width <= 20 && m.height <= 20 && alt) flags.push('tiny_image_with_alt');
      const key = `${m.src_basename}|${alt ?? '∅'}|${m.aria_label || ''}|${m.in_control?.name || ''}|${m.landmark || ''}`;
      const u = (map[`${v.product}|${key}`] ??= { id: unitId('image', v.product, key), type: 'image', sc: '1.1.1', product: v.product, views: [], view_count: 0, name: alt === null ? (m.aria_label || m.svg_title || m.aria_labelledby_text || '(no alt attribute)') : (alt === '' ? '(alt="")' : alt), detail: `${m.tag} ${m.width}x${m.height}; role:${role}${m.in_control ? '; in ' + m.in_control.tag + ' "' + m.in_control.name + '"' : ''}${m.figcaption ? '; figcaption "' + m.figcaption + '"' : ''}${m.aria_hidden ? '; aria-hidden' : ''}; src ${m.src_basename || m.src}`, context: m.adjacent_text, landmark: m.landmark, selector: m.selector, visible: m.visible, href: m.src, flags: new Set() });
      u.views.push(v.view_id); u.view_count += 1; flags.forEach((f) => u.flags.add(f)); if (m.visible) u.visible = true;
    }
  }
  return Object.values(map).map((u) => ({ ...u, flags: [...u.flags] }));
}

function fieldUnits(views) {
  const map = {};
  for (const v of views) {
    for (const f of v.inventory.fields) {
      const flags = [];
      if (!f.label) flags.push(`field_unlabeled_${f.label_source}`);
      if (f.label && /^(input|field|text|value|enter|select|search)$/i.test(f.label.trim())) flags.push('label_generic');
      if (f.required && !/required|\*/i.test(`${f.label} ${f.describedby_text || ''}`)) flags.push('required_not_in_label');
      const key = `${f.type}|${norm(f.label)}|${f.label_source}|${norm(f.placeholder)}|${f.name_attr || f.id || ''}`;
      const u = (map[`${v.product}|${key}`] ??= { id: unitId('field', v.product, key), type: 'field', sc: '2.4.6', product: v.product, views: [], view_count: 0, name: f.label || `(no label; ${f.label_source})`, detail: `${f.type}; label from ${f.label_source}${f.placeholder ? '; placeholder "' + f.placeholder + '"' : ''}${f.required ? '; required' : ''}${f.fieldset_legend ? '; legend "' + f.fieldset_legend + '"' : ''}${f.describedby_text ? '; describedby "' + f.describedby_text + '"' : ''}`, context: f.fieldset_legend || f.describedby_text || '', landmark: f.landmark, selector: f.selector, visible: f.visible, href: null, flags: new Set() });
      u.views.push(v.view_id); u.view_count += 1; flags.forEach((x) => u.flags.add(x)); if (f.visible) u.visible = true;
    }
  }
  return Object.values(map).map((u) => ({ ...u, flags: [...u.flags] }));
}

// 3.2.4 consistent identification: same destination, different names across a product's views.
function identUnits(views) {
  const byProduct = {}; views.forEach((v) => push(byProduct, v.product, v));
  const out = [];
  for (const [product, vs] of Object.entries(byProduct)) {
    const byHref = {};
    for (const v of vs) for (const l of v.inventory.links) { if (!l.name || l.same_page || PSEUDO_HREF.test(l.href_raw || '') || PSEUDO_HREF.test(l.href || '')) continue; const k = urlPath(l.href); (byHref[k] ??= {})[norm(l.name)] ??= { name: l.name, views: new Set(), landmark: l.landmark }; byHref[k][norm(l.name)].views.add(v.view_id); }
    for (const [href, names] of Object.entries(byHref)) {
      const variants = Object.values(names); if (variants.length < 2) continue;
      // In-page paired columns (an ID column and a name column both linking one record): every variant on the same views, all in main -> table pattern, not 3.2.4.
      const sig = (x) => [...x.views].sort().join(','); if (variants.every((x) => sig(x) === sig(variants[0]) && (!x.landmark || /^main/.test(x.landmark)))) continue;
      const all = new Set(variants.flatMap((x) => [...x.views]));
      out.push({ id: unitId('ident', product, href), type: 'ident', sc: '3.2.4', product, views: [...all], view_count: all.size, name: variants.map((x) => `"${x.name}" (${x.views.size} views${x.landmark ? ', ' + x.landmark : ''})`).join(' | '), detail: `${variants.length} names for one destination`, context: '', landmark: null, selector: null, visible: true, href, flags: ['same_href_multiple_names'] });
    }
  }
  return out;
}

// 3.2.3 consistent navigation: deterministic, no LLM. Per product + host, the shared navigation
// items (names present in >= half the views, all nav landmarks, DOM order, deduped) must keep the
// same RELATIVE ORDER on every view. Extra or missing items are informational; an order change is
// the 3.2.3 signal. Views whose group has one member cannot be compared.
function navConsistency(views) {
  const groups = {}; views.forEach((v) => push(groups, `${v.product}|${new URL(v.final_url || v.url).host}`, v));
  const rows = [];
  for (const [g, vs] of Object.entries(groups)) {
    const names = (v) => { const seen = new Set(); const out = []; for (const n of v.inventory.navs) if (/^(nav|navigation)/.test(n.role)) for (const i of n.items) { const k = norm(i.name); if (k && !seen.has(k)) { seen.add(k); out.push(k); } } return out; };
    const freq = {}; const pos = {}; const per = vs.map((v) => { const ns = names(v); ns.forEach((k, i) => { freq[k] = (freq[k] || 0) + 1; push(pos, k, i); }); return ns; });
    const shared = Object.keys(freq).filter((k) => freq[k] >= Math.max(2, Math.ceil(vs.length / 2)));
    const modal = shared.sort((a, b) => (pos[a].reduce((x, y) => x + y, 0) / pos[a].length) - (pos[b].reduce((x, y) => x + y, 0) / pos[b].length));
    const rank = Object.fromEntries(modal.map((k, i) => [k, i]));
    vs.forEach((v, vi) => {
      const present = per[vi].filter((k) => k in rank); const missing = modal.filter((k) => !present.includes(k));
      let firstViolation = null; for (let i = 1; i < present.length; i += 1) if (rank[present[i]] < rank[present[i - 1]]) { firstViolation = `"${present[i - 1]}" before "${present[i]}"`; break; }
      rows.push({ product: v.product, host: g.split('|')[1], view_id: v.view_id, views_in_group: vs.length, shared_items: modal.length, present_shared: present.length, missing_shared: missing.length, extra_items: per[vi].length - present.length, order_consistent: !firstViolation, first_order_violation: firstViolation, note: vs.length === 1 ? 'single view on this host; no comparison possible' : !modal.length ? 'no shared navigation items on this host (map/app shells)' : firstViolation ? `shared navigation items appear in a different relative order here: ${firstViolation}` : missing.length ? `same relative order; ${missing.length} shared item(s) absent on this view (informational)` : 'shared navigation items present in the same relative order' });
    });
  }
  return rows;
}

if (argv_has('--sample')) {
  const U = JSON.parse(await fs.readFile(path.join(dir, 'judgment-units.json'), 'utf8'));
  const judged = {}; for (const f of (await fs.readdir(path.join(dir, 'batches'))).filter((f) => f.endsWith('.judged.jsonl'))) for (const line of (await fs.readFile(path.join(dir, 'batches', f), 'utf8')).split('\n').filter(Boolean)) { try { const j = JSON.parse(line); judged[j.id] = j; } catch {} }
  const rnd = (id) => parseInt(sha(`spot|${id}`).slice(0, 8), 16) / 0xffffffff; // per-id, stable across re-samples
  const INFO = /^(no_h1|h1_count_|empty_h1|level_skip_|name_from_|title_duplicates_text|tiny_image_with_alt|new_window_not_indicated|heading_repeated_in_page|href_hash_only)/;
  const pick = []; for (const u of U.units) { const j = judged[u.id]; if (!j) continue; const flagged = u.flags.some((f) => !INFO.test(f)); const reason = j.judgment === 'unsure' ? 'unsure' : (flagged && j.judgment === 'yes') ? 'flagged-but-yes' : (!flagged && j.judgment === 'no') ? 'clean-but-no' : (rnd(u.id) < 0.1 ? 'random' : null); if (reason) pick.push({ reason, id: u.id, type: u.type, sc: u.sc, product: u.product, views: u.view_count, name: u.name, detail: u.detail, href: u.href, context: u.context, flags: u.flags, draft: j.judgment, confidence: j.confidence, rationale: j.rationale, fix: j.fix }); }
  await fs.writeFile(path.join(dir, 'spot-check-sample.jsonl'), pick.map((p) => JSON.stringify(p)).join('\n') + '\n');
  const by = {}; pick.forEach((p) => { by[p.reason] = (by[p.reason] || 0) + 1; }); console.log(JSON.stringify({ judged: Object.keys(judged).length, sampled: pick.length, by_reason: by }));
} else if (mode === 'build') {
  const run = JSON.parse(await fs.readFile(invPath, 'utf8'));
  const ok = run.views.filter((v) => v.inventory && !v.inventory.error);
  const skipped = run.views.filter((v) => !v.inventory || v.inventory.error).map((v) => ({ view_id: v.view_id, nav_error: v.nav_error, error: v.inventory?.error }));
  const units = [...titleUnits(ok), ...headingUnits(ok), ...linkUnits(ok), ...imageUnits(ok), ...fieldUnits(ok), ...identUnits(ok)];
  const nav = navConsistency(ok);
  await fs.writeFile(path.join(dir, 'judgment-units.json'), JSON.stringify({ schema: 'judgment-units/v1', built_utc: new Date().toISOString(), inventory_sha256: sha(JSON.stringify(run)), views_ok: ok.length, views_skipped: skipped, unit_count: units.length, units, nav_consistency: nav }, null, 1));
  await fs.mkdir(path.join(dir, 'batches'), { recursive: true }); for (const f of await fs.readdir(path.join(dir, 'batches'))) if (f.endsWith('.jsonl') && !f.endsWith('.judged.jsonl')) await fs.rm(path.join(dir, 'batches', f));
  const groups = {}; units.forEach((u) => push(groups, `${u.product}-${u.type}`, u));
  const summary = {};
  for (const [g, us] of Object.entries(groups)) {
    for (let i = 0; i < us.length; i += BATCH) {
      const name = `${g}-${String(i / BATCH + 1).padStart(2, '0')}.jsonl`;
      const lines = us.slice(i, i + BATCH).map((u) => JSON.stringify({ id: u.id, type: u.type, sc: u.sc, name: u.name, detail: u.detail, href: u.href, context: u.context, landmark: u.landmark, visible: u.visible, views: u.view_count, flags: u.flags }));
      await fs.writeFile(path.join(dir, 'batches', name), lines.join('\n') + '\n');
      summary[name] = lines.length;
    }
  }
  const byType = {}; units.forEach((u) => { byType[u.type] = (byType[u.type] || 0) + 1; });
  console.log(JSON.stringify({ views_ok: ok.length, skipped, unit_count: units.length, by_type: byType, flagged: units.filter((u) => u.flags.length).length, nav_rows: nav.length, nav_order_violations: nav.filter((r) => !r.order_consistent).length, batches: summary }, null, 1));
} else {
  const U = JSON.parse(await fs.readFile(path.join(dir, 'judgment-units.json'), 'utf8'));
  const judged = {}; const files = (await fs.readdir(path.join(dir, 'batches'))).filter((f) => f.endsWith('.judged.jsonl'));
  for (const f of files) for (const line of (await fs.readFile(path.join(dir, 'batches', f), 'utf8')).split('\n').filter(Boolean)) { try { const j = JSON.parse(line); judged[j.id] = { ...j, batch: f }; } catch (e) { console.error('bad line in', f, line.slice(0, 80)); } }
  const std = {}; try { for (const line of (await fs.readFile(path.join(dir, 'standards.jsonl'), 'utf8')).split('\n').filter(Boolean)) { const c = JSON.parse(line); std[c.id] = c; } } catch {}
  const rat = {}; try { for (const line of (await fs.readFile(path.join(dir, 'ratifications.jsonl'), 'utf8')).split('\n').filter(Boolean)) { const c = JSON.parse(line); rat[c.id] = c; } } catch {}
  const spot = {}; try { for (const line of (await fs.readFile(path.join(dir, 'spot-checks.jsonl'), 'utf8')).split('\n').filter(Boolean)) { const c = JSON.parse(line); spot[c.id] = c; } } catch {}
  const rows = U.units.map((u) => { const j = judged[u.id] || {}; const c = spot[u.id]; const sj = c?.spot_check === 'overturn' && c.judgment ? c.judgment : (j.judgment || ''); return { ...u, draft_judgment: j.judgment || '', confidence: j.confidence || '', rationale: j.rationale || '', fix: j.fix || '', needs_human: j.needs_human ?? (j.judgment ? false : ''), drafted_by: j.drafted_by || (j.judgment ? 'unknown' : ''), spot_check: c ? `${c.spot_check}${c.spot_check === 'overturn' ? '→' + c.judgment : ''}${c.note ? ': ' + c.note : ''}` : '', session_judgment: sj, ratified_by: rat[u.id]?.ratified_by || '', ratified_judgment: rat[u.id]?.ratified_judgment || '', ratifier_note: rat[u.id]?.ratifier_note || '', ratified_utc: rat[u.id]?.ratified_utc || '', ruling: rat[u.id]?.ruling || '', client_rules: (std[u.id]?.epa_rules || []).join(' '), client_result: std[u.id]?.epa_result || '', client_note: std[u.id]?.epa_note || '' }; });
  const missing = rows.filter((r) => !r.draft_judgment).length;
  const cols = ['id', 'product', 'type', 'sc', 'view_count', 'views', 'name', 'detail', 'href', 'context', 'landmark', 'selector', 'visible', 'flags', 'draft_judgment', 'confidence', 'rationale', 'fix', 'needs_human', 'drafted_by', 'spot_check', 'session_judgment', 'ratified_by', 'ratified_judgment', 'ratifier_note', 'ratified_utc', 'ruling', 'client_rules', 'client_result', 'client_note'];
  const esc = (v) => { const s = Array.isArray(v) ? v.join('; ') : v === null || v === undefined ? '' : String(v); return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
  const csv = (rs) => [cols.join(','), ...rs.map((r) => cols.map((c) => esc(r[c])).join(','))].join('\n') + '\n';
  const order = { title: 0, heading: 1, field: 2, link: 3, image: 4, ident: 5 }; const jo = { no: 0, unsure: 1, yes: 2, '': 3 };
  const sorted = [...rows].sort((a, b) => a.product.localeCompare(b.product) || order[a.type] - order[b.type] || jo[a.session_judgment] - jo[b.session_judgment] || b.view_count - a.view_count);
  for (const p of [...new Set(rows.map((r) => r.product))]) await fs.writeFile(path.join(dir, `draft-judgments-${p.replace(/[^a-z0-9.-]/gi, '_')}.csv`), csv(sorted.filter((r) => r.product === p)));
  await fs.writeFile(path.join(dir, 'draft-judgments.csv'), csv(sorted));
  const navCols = ['product', 'host', 'view_id', 'views_in_group', 'shared_items', 'present_shared', 'missing_shared', 'extra_items', 'order_consistent', 'first_order_violation', 'note'];
  await fs.writeFile(path.join(dir, 'nav-consistency.csv'), [navCols.join(','), ...U.nav_consistency.map((r) => navCols.map((c) => esc(r[c])).join(','))].join('\n') + '\n');
  const tally = {}; for (const r of rows) { const k = `${r.product}|${r.type}`; tally[k] ??= { yes: 0, no: 0, unsure: 0, missing: 0, needs_human: 0, spot_checked: 0, overturned: 0 }; tally[k][r.session_judgment || 'missing'] += 1; if (r.needs_human === true) tally[k].needs_human += 1; if (r.spot_check) tally[k].spot_checked += 1; if (r.spot_check.startsWith('overturn')) tally[k].overturned += 1; if (r.ratified_by) tally[k].ratified = (tally[k].ratified || 0) + 1; }
  await fs.writeFile(path.join(dir, 'draft-judgments.json'), JSON.stringify({ schema: 'draft-judgments/v1', built_utc: new Date().toISOString(), units_sha256: sha(JSON.stringify(U)), rubric: 'judgment-rubric.md', status: rows.some((r) => r.ratified_by) ? (rows.every((r) => r.ratified_by) ? 'RATIFIED' : 'PARTIALLY_RATIFIED') : 'DRAFT_NOT_RATIFIED', ratified_rows: rows.filter((r) => r.ratified_by).length, what_this_is: 'Agent-drafted per-row judgments for the content-inventory criteria (2.4.2, 2.4.6, 2.4.4, 1.1.1, 3.2.4) with deterministic heuristic flags. Every row awaits a named human ratifier; none of these is a criterion outcome.', tally, missing, rows, nav_consistency: U.nav_consistency }, null, 1));
  console.log(JSON.stringify({ rows: rows.length, missing, tally }, null, 1));
}
