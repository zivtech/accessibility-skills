#!/usr/bin/env node
// Portable, offline content-review handoff. No tracker writes or conformance outcomes.
import { createHash, randomUUID } from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import { decisionId, isCompleteWcag, parseRatifications, unitRevision, validateInventory } from './ratification-import.mjs';

const SCHEMA = 'content-review-bundle/v1';
const BOUNDARY = 'DRAFT review tasks, not findings, fix attestations, or conformance outcomes. '
  + 'Assignment and work status belong to the receiving tracker. A returned judgment is a human assertion; hashes do not authenticate a person.';
const hash = (value) => createHash('sha256').update(value).digest('hex');
const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
const text = (value) => typeof value === 'string' && value.trim().length > 0;
const object = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);
const fail = (message) => { throw new Error(message); };

function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (object(value)) return `{${Object.keys(value).sort().map((k) => `${JSON.stringify(k)}:${canonical(value[k])}`).join(',')}}`;
  return JSON.stringify(value);
}

async function readJson(file) {
  try { return JSON.parse(await fs.readFile(file, 'utf8')); }
  catch (error) { fail(`${file}: ${error.message}`); }
}

async function readHistory(inventory) {
  try { return await fs.readFile(path.join(inventory, 'ratifications.jsonl'), 'utf8'); }
  catch (error) { if (error.code === 'ENOENT') return ''; throw error; }
}

async function context(inventory) {
  const source = await readJson(path.join(inventory, 'judgment-units.json'));
  validateInventory(source);
  const history = await readHistory(inventory);
  const parsed = parseRatifications(history, source.units);
  return { source, history, parsed, source_sha256: hash(JSON.stringify(source)) };
}

function currentRecord(parsed, id) {
  return parsed.wcag.get(id) || parsed.drafts.get(`wcag:${id}`);
}

function taskFor(unit, row, parsed) {
  return { unit, unit_sha256: unitRevision(unit),
    base_decision_id: currentRecord(parsed, unit.id)?.decision_id || null,
    next_action: 'human_content_review', actor_kind: 'human',
    question: `Does this ${unit.type || 'content element'} serve its purpose in the captured context (${unit.sc || 'criterion in source'})? Record your observation before comparing the agent draft.`,
    draft: { judgment: row.session_draft_judgment || '', rationale: row.rationale || '',
      fix: row.fix || '', spot_check: row.spot_check || '' } };
}

function csvCell(value) {
  let raw = value == null ? '' : Array.isArray(value) ? value.join('; ') : String(value);
  if (/^[\s]*[=+@-]|^[\t\r\n]/.test(raw)) raw = `'${raw}`;
  return `"${raw.replaceAll('"', '""')}"`;
}

function csvTasks(bundle) {
  const columns = ['unit_id', 'unit_sha256', 'bundle_id', 'record_kind', 'next_action', 'actor_kind',
    'product', 'type', 'criterion', 'name', 'detail', 'context', 'selector', 'href', 'views', 'question', 'base_decision_id'];
  const rows = bundle.tasks.map((t) => [t.unit.id, t.unit_sha256, bundle.bundle_id, 'DRAFT_CONTENT_REVIEW',
    t.next_action, t.actor_kind, t.unit.product, t.unit.type, t.unit.sc, t.unit.name, t.unit.detail,
    t.unit.context, t.unit.selector, t.unit.href, t.unit.views, t.question, t.base_decision_id]);
  return [columns, ...rows].map((row) => row.map(csvCell).join(',')).join('\n') + '\n';
}

function markdown(value) {
  return String(value ?? '').replace(/[\\`*_{}[\]<>()#!|]/g, '\\$&').replace(/\r?\n/g, ' / ');
}

function markdownTasks(bundle) {
  const intro = ['# Content review worklist', '', BOUNDARY, '',
    `Bundle: \`${bundle.bundle_id}\``, '',
    'Use unit_id as the CSV primary key. CSV formula prefixes are escaped with an apostrophe; bundle.json retains exact source text.',
    'Assignments belong in your tracker. Return only the items you actually reviewed. Leave unreviewed template rows out of the response.',
    'Record your observation and rationale before consulting the agent draft in bundle.json. Nothing is pre-approved.', '',
    'A yes applies only to the captured sample; it does not establish Supports. Interaction and fix confirmation use their own evidence contracts.', ''];
  const tasks = bundle.tasks.flatMap((t) => [
    `## ${markdown(t.unit.id)}`, '', `Question: ${markdown(t.question)}`, '',
    `Content: ${markdown(t.unit.name)}`, `Detail: ${markdown(t.unit.detail)}`,
    `Context: ${markdown(t.unit.context)}`, `Views: ${markdown((t.unit.views || []).join(', '))}`,
    `Source/selector: ${markdown(t.unit.href || '')} ${markdown(t.unit.selector || '')}`, '',
    'Observed / rationale: ____________________', 'Decision (yes / no / unsure): ____________________',
    'Reviewed by and UTC timestamp: ____________________', '',
    'If sources disagree, record unsure with both references and name the deciding check in your tracker. Do not discard either observation.', '']);
  return [...intro, ...tasks].join('\n') + '\n';
}

function returnTemplate(bundle) {
  return { bundle_id: bundle.bundle_id, decisions: bundle.tasks.map((t) => ({
    id: t.unit.id, scope: 'wcag', unit_sha256: t.unit_sha256,
    ratified_by: '', ratified_judgment: '', ratified_utc: '', ratifier_note: '',
    ...(t.base_decision_id ? { supersedes: t.base_decision_id, supersession_reason: '' } : {}) })) };
}

async function exportBundle(args) {
  const ctx = await context(args.inventory);
  const merged = await readJson(path.join(args.inventory, 'draft-judgments.json'));
  if (merged.units_sha256 !== ctx.source_sha256) fail('Stale merged judgments: run build-judgment-rows.mjs --merge first');
  if (!Array.isArray(merged.rows)) fail('Merged judgments require rows');
  const rows = new Map(merged.rows.map((r) => [r.id, r]));
  if (rows.size !== ctx.source.units.length || ctx.source.units.some((u) => !rows.has(u.id))) fail('Merged rows do not match inventory');
  const tasks = ctx.source.units.filter((u) => args.all || !ctx.parsed.wcag.has(u.id))
    .map((u) => taskFor(u, rows.get(u.id), ctx.parsed));
  const payload = { schema: SCHEMA, source_sha256: ctx.source_sha256, claim_boundary: BOUNDARY,
    coverage: { viewport: ctx.source.viewport || null, caps: ctx.source.caps || null,
      views_ok: ctx.source.views_ok, views_skipped: ctx.source.views_skipped || [] }, tasks };
  const bundle = { ...payload, bundle_id: `sha256:${hash(canonical(payload))}` };
  await fs.mkdir(args.out); // Exclusive destination: preserve previously issued bundles.
  await fs.writeFile(path.join(args.out, 'bundle.json'), json(bundle), { flag: 'wx' });
  await fs.writeFile(path.join(args.out, 'review-tasks.csv'), csvTasks(bundle), { flag: 'wx' });
  await fs.writeFile(path.join(args.out, 'review-tasks.md'), markdownTasks(bundle), { flag: 'wx' });
  await fs.writeFile(path.join(args.out, 'return-template.json'), json(returnTemplate(bundle)), { flag: 'wx' });
  return { bundle_id: bundle.bundle_id, tasks: tasks.length, out: args.out, next_action: 'human_content_review', claim_boundary: BOUNDARY };
}

function verifyBundle(bundle, response, ctx) {
  if (!object(bundle) || bundle.schema !== SCHEMA || !Array.isArray(bundle.tasks)) fail('Invalid content review bundle');
  const { bundle_id, ...payload } = bundle;
  if (bundle_id !== `sha256:${hash(canonical(payload))}`) fail('Bundle hash mismatch');
  if (!object(response) || response.bundle_id !== bundle_id || !Array.isArray(response.decisions)) fail('Response must identify this bundle and carry decisions');
  if (bundle.source_sha256 !== ctx.source_sha256) fail('Stale source snapshot: export a fresh review bundle');
  const units = new Map(ctx.source.units.map((u) => [u.id, u]));
  const tasks = new Map();
  for (const task of bundle.tasks) {
    if (!object(task.unit) || tasks.has(task.unit.id) || !units.has(task.unit.id)) fail('Bundle has an unknown or duplicate unit');
    if (task.unit_sha256 !== unitRevision(task.unit) || task.unit_sha256 !== unitRevision(units.get(task.unit.id))) fail('Stale or altered unit snapshot');
    tasks.set(task.unit.id, task);
  }
  return tasks;
}

function validateReturns(response, tasks, ctx) {
  const seen = new Set();
  const additions = [];
  for (const record of response.decisions) {
    if (!object(record) || !tasks.has(record.id) || seen.has(record.id)) fail('Response has an unknown or duplicate unit');
    seen.add(record.id);
    const task = tasks.get(record.id);
    if (record.scope && record.scope !== 'wcag') fail('This return loop accepts WCAG content judgments only');
    if (record.unit_sha256 !== task.unit_sha256) fail(`${record.id}: missing or stale unit_sha256`);
    if (!isCompleteWcag(record) || !text(record.ratifier_note)) fail(`${record.id}: a complete human decision, UTC date, and observation/rationale are required`);
    const current = currentRecord(ctx.parsed, record.id)?.decision_id || null;
    const desired = decisionId(record);
    if (current !== task.base_decision_id && current !== desired) fail(`${record.id}: stale decision base; preserve the disagreement and export a fresh bundle`);
    if (task.base_decision_id && desired !== task.base_decision_id
      && (record.supersedes !== task.base_decision_id || !text(record.supersession_reason))) fail(`${record.id}: replacement needs supersedes and a reason`);
    additions.push(record);
  }
  const next = ctx.history + (ctx.history && !ctx.history.endsWith('\n') ? '\n' : '')
    + additions.map((r) => JSON.stringify(r)).join('\n') + (additions.length ? '\n' : '');
  parseRatifications(next, ctx.source.units); // Validate the entire history and every return before any write.
  const novel = additions.filter((r) => currentRecord(ctx.parsed, r.id)?.decision_id !== decisionId(r));
  return { novel, replayed: additions.length - novel.length };
}

async function saveHistory(inventory, ctx, records) {
  if (!records.length) return;
  const target = path.join(inventory, 'ratifications.jsonl');
  const temporary = path.join(inventory, `.ratifications-${randomUUID()}.tmp`);
  const next = ctx.history + (ctx.history && !ctx.history.endsWith('\n') ? '\n' : '')
    + records.map((r) => JSON.stringify(r)).join('\n') + '\n';
  try {
    await fs.writeFile(temporary, next, { flag: 'wx', mode: 0o600 });
    if (await readHistory(inventory) !== ctx.history) fail('Ratification history changed during import; no update applied');
    const latest = await readJson(path.join(inventory, 'judgment-units.json'));
    if (hash(JSON.stringify(latest)) !== ctx.source_sha256) fail('Source changed during import; no update applied');
    await fs.rename(temporary, target);
  } finally { await fs.rm(temporary, { force: true }); }
}

async function applyReturns(args) {
  const bundle = await readJson(path.join(args.bundle, 'bundle.json'));
  const response = await readJson(args.responses);
  const lockPath = path.join(args.inventory, '.content-review-return.lock');
  let lock;
  try { lock = await fs.open(lockPath, 'wx', 0o600); }
  catch (error) { if (error.code === 'EEXIST') fail('Another return writer holds .content-review-return.lock; retry after it finishes'); throw error; }
  try {
    await lock.writeFile(`pid=${process.pid}\n`);
    const ctx = await context(args.inventory);
    const tasks = verifyBundle(bundle, response, ctx);
    const { novel, replayed } = validateReturns(response, tasks, ctx);
    await saveHistory(args.inventory, ctx, novel);
    return { applied: novel.length, replayed, next_action: 'merge_judgments',
      merge: { script: 'build-judgment-rows.mjs', args: ['--merge', '--inventory', args.inventory] }, claim_boundary: BOUNDARY };
  } finally { await lock.close(); await fs.unlink(lockPath); }
}

function argumentsFor(argv) {
  const args = {};
  const flags = new Set(['--export', '--apply', '--all']);
  const values = new Set(['--inventory', '--out', '--bundle', '--responses']);
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    if (flag in args) fail(`Duplicate option ${flag}`);
    if (flags.has(flag)) args[flag] = true;
    else if (values.has(flag) && argv[i + 1] && !argv[i + 1].startsWith('--')) args[flag] = path.resolve(argv[++i]);
    else fail(`Unknown option or missing value: ${flag}`);
  }
  if (Boolean(args['--export']) === Boolean(args['--apply']) || !args['--inventory']) fail('Choose --export or --apply and supply --inventory');
  if (args['--export'] && (!args['--out'] || args['--bundle'] || args['--responses'])) fail('--export needs --out; --bundle/--responses are for --apply');
  if (args['--apply'] && (!args['--bundle'] || !args['--responses'] || args['--out'] || args['--all'])) fail('--apply needs --bundle and --responses');
  return Object.fromEntries(Object.entries(args).map(([k, v]) => [k.slice(2), v]));
}

try {
  const args = argumentsFor(process.argv.slice(2));
  const result = args.export ? await exportBundle(args) : await applyReturns(args);
  console.log(json(result));
} catch (error) {
  console.error(`Content review refused: ${error.message}`);
  process.exitCode = 2;
}
