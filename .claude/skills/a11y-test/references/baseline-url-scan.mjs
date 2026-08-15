#!/usr/bin/env node

/**
 * Baseline URL-list scan — sequential axe-core sweep across a list of URLs.
 *
 * Promoted from a one-off harness written for the 2026-08-13 EPA public-sites
 * engagement — the zivtech/a11y-audits repo (private),
 * 2026-08-13-epa-public-sites/evidence/harness/audit-pages.mjs, run against
 * 40 views. Drops that harness's engagement-specific extras (structure
 * inventory, ARIA snapshot, keyboard tab-trace, text-spacing probe,
 * per-node XPath) to stay a focused baseline tool.
 * DETECTOR output only — candidate findings for human review, never a
 * conformance verdict. See the a11y-test SKILL.md "Baseline URL-list scan".
 *
 * Peer deps (install in your own project — never here; repo is prompt-only):
 *   npm install -D playwright @axe-core/playwright && npx playwright install chromium
 * Exact-pin @axe-core/playwright in your project — rule availability is
 * per-axe-core-version; this script records whatever version it resolves
 * (axe_core_version in summary.json) but does not control which one runs.
 *
 * Usage:
 *   node baseline-url-scan.mjs --urls-file urls.txt --out ./baseline-scan-output
 *   node baseline-url-scan.mjs --out ./out https://example.com https://example.org/page
 * urls.txt: one absolute http(s) URL per line; blank/#-prefixed lines ignored.
 * --viewports WxH[,WxH...] (default 1280x800,320x800, the EPA harness's
 * desktop+narrow lineage) scans every URL at each listed viewport. Confirm
 * you're authorized to test third-party sites and check robots.txt/terms;
 * raise --delay (default 500ms) for rate-limited or robots-restricted targets.
 *
 * --census enables DOM-census heuristics (empty paragraphs, autocomplete
 * absence on known-purpose inputs, duplicate ids), reported under a
 * `census` key on each viewport record — separate from axe violations,
 * always a detector heuristic, never a conformance verdict. Implementation
 * lives in the sibling ./census.mjs to keep this file within its line budget.
 * --alt-snapshot writes alt-snapshot.json: one img/svg[role=img] selector
 * map per page (src-or-title + alt), captured once per URL. Diff two runs'
 * alt-snapshot.json files to catch silent alt-text regressions — recipe in
 * the a11y-test SKILL.md quickstart.
 */

import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import { collectPageSignals } from './census.mjs';

const DEFAULT_DELAY_MS = 500;
const DEFAULT_OUT_DIR = './baseline-scan-output';
const DEFAULT_VIEWPORTS = '1280x800,320x800';
const SAMPLE_SELECTOR_LIMIT = 3;
const NAV_TIMEOUT_MS = 60000;
const NETWORK_IDLE_TIMEOUT_MS = 8000;
// This bundle's WCAG 2.2 AA default target (SKILL.md §4 / EPA harness tags).
const WCAG_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'];

const { urls, outDir, delayMs, viewports, census, altSnapshot } = await parseArgs(process.argv.slice(2));
await mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = [];
const altSnapshotPages = [];
try {
  for (const [index, url] of urls.entries()) {
    console.log(`[${index + 1}/${urls.length}] ${url}`);
    const result = await scanUrl(browser, url, viewports, { census, altSnapshot });
    results.push(result);
    if (altSnapshot) altSnapshotPages.push({ url, images: extractAltSnapshot(result) });
    await writeJson(path.join(outDir, `${slug(url, index)}.json`), result);
    if (index < urls.length - 1) await delay(delayMs);
  }
} finally {
  await browser.close();
}

const summary = buildSummary(urls, viewports, results, { census });
await writeJson(path.join(outDir, 'summary.json'), summary);
if (altSnapshot) await writeJson(path.join(outDir, 'alt-snapshot.json'), altSnapshotPages);
console.log(JSON.stringify(summary.totals, null, 2));

// alt-snapshot is page-level (§ Usage above), pulled from the first
// viewport scanned for the URL rather than duplicated across viewports.
function extractAltSnapshot(result) {
  for (const vp of Object.values(result.viewports)) {
    if (vp.alt_snapshot) return vp.alt_snapshot;
  }
  return [];
}

// ---- per-URL scan (every viewport) ----
async function scanUrl(browser, url, viewports, options = {}) {
  const record = { url, started: new Date().toISOString(), viewports: {} };
  for (const [index, viewport] of viewports.entries()) {
    console.log(`  viewport ${viewport.key}`);
    // alt-snapshot is captured once per URL (first viewport only); census
    // runs on every viewport since responsive layouts can change the DOM.
    const vpOptions = { census: options.census, altSnapshot: options.altSnapshot && index === 0 };
    record.viewports[viewport.key] = await scanViewport(browser, url, viewport, vpOptions);
  }
  const measured = Object.values(record.viewports).filter((v) => v.status === 'measured').length;
  record.status = measured === viewports.length ? 'measured' : measured > 0 ? 'partial' : 'error';
  record.finished = new Date().toISOString();
  return record;
}

async function scanViewport(browser, url, viewport, options = {}) {
  const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height } });
  const page = await context.newPage();
  const record = { status: 'started' };
  try {
    const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: NAV_TIMEOUT_MS });
    // Many sites never reach true network idle (ads, polling, live data);
    // a bounded wait here is recorded honestly rather than assumed reached.
    await page.waitForLoadState('networkidle', { timeout: NETWORK_IDLE_TIMEOUT_MS }).catch(() => {});
    record.http_status = response?.status() ?? null;
    record.final_url = page.url();
    record.title = await page.title();
    const axeResults = await new AxeBuilder({ page }).withTags(WCAG_TAGS).analyze();
    record.axe_core_version = axeResults.testEngine?.version || null;
    record.violations = summarizeRules(axeResults.violations);
    record.incomplete = summarizeRules(axeResults.incomplete);
    record.passes_count = axeResults.passes.length;
    record.inapplicable_count = axeResults.inapplicable.length;
    if (options.census || options.altSnapshot) {
      // Detector heuristics only — kept under their own keys, never folded
      // into axe's violations/incomplete.
      const signals = await collectPageSignals(page, options);
      if (signals.census) record.census = signals.census;
      if (signals.alt_snapshot) record.alt_snapshot = signals.alt_snapshot;
    }
    record.status = 'measured';
  } catch (error) {
    record.status = 'error';
    record.error = String(error?.message || error).slice(0, 2000);
  } finally {
    await context.close();
  }
  return record;
}

function summarizeRules(rules) {
  return rules.map((rule) => ({
    id: rule.id,
    impact: rule.impact,
    help: rule.help,
    help_url: rule.helpUrl,
    tags: rule.tags,
    node_count: rule.nodes.length,
    sample_selectors: rule.nodes.slice(0, SAMPLE_SELECTOR_LIMIT).map((node) => node.target.join(' ')),
  }));
}

// ---- aggregation (across all viewports of all URLs) ----
function buildSummary(urls, viewports, results, options = {}) {
  const impacts = { critical: 0, serious: 0, moderate: 0, minor: 0, unknown: 0 };
  const byRule = new Map();
  // Detector heuristics, aggregated separately — never merged into the axe
  // impact/rule tallies above.
  const censusTotals = { empty_paragraphs: 0, autocomplete_absence: 0, duplicate_ids: 0 };
  let violationNodes = 0;
  let measuredScans = 0;
  let erroredScans = 0;
  let axeCoreVersion = null;
  for (const result of results) {
    for (const vp of Object.values(result.viewports)) {
      if (vp.status !== 'measured') {
        erroredScans += 1;
        continue;
      }
      measuredScans += 1;
      axeCoreVersion = axeCoreVersion || vp.axe_core_version;
      for (const rule of vp.violations) {
        violationNodes += rule.node_count;
        impacts[rule.impact || 'unknown'] = (impacts[rule.impact || 'unknown'] || 0) + rule.node_count;
        const aggregate = byRule.get(rule.id) ||
          { rule_id: rule.id, impact: rule.impact, help_url: rule.help_url, pages: new Set(), nodes: 0 };
        aggregate.pages.add(result.url);
        aggregate.nodes += rule.node_count;
        byRule.set(rule.id, aggregate);
      }
      if (vp.census) {
        censusTotals.empty_paragraphs += vp.census.empty_paragraphs.count;
        censusTotals.autocomplete_absence += vp.census.autocomplete_absence.count;
        censusTotals.duplicate_ids += vp.census.duplicate_ids.count;
      }
    }
  }
  return {
    schema_version: '1.2',
    generated: new Date().toISOString(),
    axe_core_version: axeCoreVersion,
    totals: {
      urls_scanned: urls.length,
      viewports_per_url: viewports.map((v) => v.key),
      viewport_scans: urls.length * viewports.length,
      measured: measuredScans,
      errors: erroredScans,
      violation_nodes: violationNodes,
      violation_nodes_by_impact: impacts,
      ...(options.census ? { census_totals: censusTotals } : {}),
    },
    violations_by_rule: [...byRule.values()]
      .map((item) => ({ ...item, pages: [...item.pages].sort(), page_count: item.pages.size }))
      .sort((a, b) => b.nodes - a.nodes || a.rule_id.localeCompare(b.rule_id)),
  };
}

// ---- CLI / input handling ----
async function parseArgs(argv) {
  let urlsFile = null;
  let outDir = DEFAULT_OUT_DIR;
  let delayMs = DEFAULT_DELAY_MS;
  let viewportsArg = DEFAULT_VIEWPORTS;
  let census = false;
  let altSnapshot = false;
  const positional = [];
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--urls-file') urlsFile = argv[++index];
    else if (arg === '--out') outDir = argv[++index];
    else if (arg === '--delay') delayMs = Number(argv[++index]);
    else if (arg === '--viewports') viewportsArg = argv[++index];
    else if (arg === '--census') census = true;
    else if (arg === '--alt-snapshot') altSnapshot = true;
    else if (arg.startsWith('--')) throw new Error(`Unknown flag: ${arg}`);
    else positional.push(arg);
  }

  const urls = urlsFile ? await readUrlsFile(urlsFile) : positional;
  if (urls.length === 0) throw new Error('No URLs given. Pass --urls-file <path> or list URLs as arguments.');
  const invalid = urls.filter((url) => !/^https?:\/\//.test(url));
  if (invalid.length > 0) throw new Error(`URLs must start with http:// or https://: ${invalid.join(', ')}`);
  if (!Number.isFinite(delayMs) || delayMs < 0) throw new Error(`--delay must be non-negative, got: ${delayMs}`);
  return { urls, outDir, delayMs, viewports: parseViewports(viewportsArg), census, altSnapshot };
}

function parseViewports(arg) {
  return arg.split(',').map((spec) => {
    const match = spec.trim().match(/^(\d+)x(\d+)$/i);
    if (!match) throw new Error(`Invalid --viewports entry: "${spec}" (expected WxH, e.g. 1280x800)`);
    return { key: `${match[1]}x${match[2]}`, width: Number(match[1]), height: Number(match[2]) };
  });
}

async function readUrlsFile(file) {
  const text = await readFile(file, 'utf8');
  return text
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#'));
}

function slug(url, index) {
  const cleaned = url
    .replace(/^https?:\/\//, '')
    .replace(/[^a-z0-9]+/gi, '-')
    .replace(/^-+|-+$/g, '')
    .toLowerCase();
  return `${String(index).padStart(3, '0')}-${cleaned.slice(0, 80)}`;
}

async function writeJson(file, value) {
  await writeFile(file, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
