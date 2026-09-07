import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { test } from 'node:test';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const refs = path.join(root, '.claude/skills/a11y-content-judgment/references');
const cli = path.join(refs, 'review-content-judgments.mjs');
const builder = path.join(refs, 'build-judgment-rows.mjs');
const run = (script, args) => spawnSync(process.execPath, [script, ...args], { encoding: 'utf8' });
const unit = (id) => ({ id, product: 'Synthetic', type: 'title', name: 'Account settings',
  sc: '2.4.2', context: 'Manage your account', selector: 'title', href: 'https://example.test/account',
  views: ['S01'], view_count: 1, flags: [] });

async function setup(t, units = [unit('TITLE-01')]) {
  const dir = await mkdtemp(path.join(tmpdir(), 'content-return-test-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  const inventory = path.join(dir, 'inventory');
  const bundle = path.join(dir, 'bundle');
  await mkdir(path.join(inventory, 'batches'), { recursive: true });
  const source = { schema: 'judgment-units/v1', units, nav_consistency: [], views_ok: 1, views_skipped: [] };
  await writeFile(path.join(inventory, 'judgment-units.json'), JSON.stringify(source));
  await writeFile(path.join(inventory, 'batches/example.judged.jsonl'),
    units.map((u) => JSON.stringify({ id: u.id, judgment: 'unsure', rationale: 'Needs human context' })).join('\n'));
  assert.equal(run(builder, ['--merge', '--inventory', inventory]).status, 0);
  return { dir, inventory, bundle, source };
}

async function exported(ctx) {
  const result = run(cli, ['--export', '--inventory', ctx.inventory, '--out', ctx.bundle]);
  assert.equal(result.status, 0, result.stderr);
  return JSON.parse(await readFile(path.join(ctx.bundle, 'bundle.json'), 'utf8'));
}

const response = (bundle, changes = {}) => ({ bundle_id: bundle.bundle_id,
  decisions: [{ id: bundle.tasks[0].unit.id, unit_sha256: bundle.tasks[0].unit_sha256,
    ratified_by: 'Synthetic reviewer', ratified_judgment: 'yes',
    ratified_utc: '2026-09-07T00:00:00Z', ratifier_note: 'The title identifies the account settings page.',
    ...changes }] });

async function apply(ctx, payload) {
  const file = path.join(ctx.dir, 'response.json');
  await writeFile(file, JSON.stringify(payload));
  return run(cli, ['--apply', '--inventory', ctx.inventory, '--bundle', ctx.bundle, '--responses', file]);
}

test('export creates draft work items and blank human fields, without changing source files', async (t) => {
  const ctx = await setup(t);
  const before = await readFile(path.join(ctx.inventory, 'draft-judgments.json'));
  const bundle = await exported(ctx);
  assert.equal(bundle.tasks[0].next_action, 'human_content_review');
  assert.equal(bundle.tasks[0].base_decision_id, null);
  const template = JSON.parse(await readFile(path.join(ctx.bundle, 'return-template.json'), 'utf8'));
  assert.equal(template.decisions[0].ratified_by, '');
  assert.equal(template.decisions[0].ratified_judgment, '');
  assert.equal(template.decisions[0].ratifier_note, '');
  assert.match(await readFile(path.join(ctx.bundle, 'review-tasks.csv'), 'utf8'), /unit_id/);
  assert.match(await readFile(path.join(ctx.bundle, 'review-tasks.md'), 'utf8'), /DRAFT/);
  assert.deepEqual(await readFile(path.join(ctx.inventory, 'draft-judgments.json')), before);
  assert.equal(run(cli, ['--export', '--inventory', ctx.inventory, '--out', ctx.bundle]).status, 2);
});

test('human return applies, identical retry does not duplicate history, and merge ratifies', async (t) => {
  const ctx = await setup(t);
  const bundle = await exported(ctx);
  assert.equal((await apply(ctx, response(bundle))).status, 0);
  const history = await readFile(path.join(ctx.inventory, 'ratifications.jsonl'), 'utf8');
  assert.equal((await apply(ctx, response(bundle))).status, 0);
  assert.equal(await readFile(path.join(ctx.inventory, 'ratifications.jsonl'), 'utf8'), history);
  assert.equal(run(builder, ['--merge', '--inventory', ctx.inventory]).status, 0);
  const merged = JSON.parse(await readFile(path.join(ctx.inventory, 'draft-judgments.json'), 'utf8'));
  assert.equal(merged.rows[0].status, 'RATIFIED');
  assert.equal(merged.rows[0].ratified_judgment, 'yes');
});

test('changed source with the same unit ID rejects the stale returned observation', async (t) => {
  const ctx = await setup(t);
  const bundle = await exported(ctx);
  ctx.source.units[0].name = 'Different title';
  await writeFile(path.join(ctx.inventory, 'judgment-units.json'), JSON.stringify(ctx.source));
  const result = await apply(ctx, response(bundle));
  assert.equal(result.status, 2);
  assert.match(result.stderr, /stale/i);
  await assert.rejects(readFile(path.join(ctx.inventory, 'ratifications.jsonl')), { code: 'ENOENT' });
});

test('concurrent contrary return cannot overwrite the first reviewer', async (t) => {
  const ctx = await setup(t);
  const bundle = await exported(ctx);
  assert.equal((await apply(ctx, response(bundle))).status, 0);
  const before = await readFile(path.join(ctx.inventory, 'ratifications.jsonl'));
  const result = await apply(ctx, response(bundle, { ratified_judgment: 'no', ratified_by: 'Second reviewer' }));
  assert.equal(result.status, 2);
  assert.match(result.stderr, /stale|conflict/i);
  assert.deepEqual(await readFile(path.join(ctx.inventory, 'ratifications.jsonl')), before);
});

test('invalid second decision prevents the first decision from being applied', async (t) => {
  const ctx = await setup(t, [unit('TITLE-01'), unit('TITLE-02')]);
  const bundle = await exported(ctx);
  const payload = response(bundle);
  payload.decisions.push({ ...payload.decisions[0], id: 'unknown-unit' });
  assert.equal((await apply(ctx, payload)).status, 2);
  await assert.rejects(readFile(path.join(ctx.inventory, 'ratifications.jsonl')), { code: 'ENOENT' });
});

test('blank template, client-scope return, wrong bundle, and missing pin all refuse', async (t) => {
  const ctx = await setup(t);
  const bundle = await exported(ctx);
  const template = JSON.parse(await readFile(path.join(ctx.bundle, 'return-template.json'), 'utf8'));
  assert.equal((await apply(ctx, template)).status, 2);
  assert.equal((await apply(ctx, response(bundle, { scope: 'client' }))).status, 2);
  assert.equal((await apply(ctx, { ...response(bundle), bundle_id: 'different' })).status, 2);
  assert.equal((await apply(ctx, response(bundle, { unit_sha256: undefined }))).status, 2);
  assert.equal((await apply(ctx, response(bundle, { ratifier_note: '' }))).status, 2);
  assert.equal((await apply(ctx, response(bundle, { ratified_utc: '2026-09-07' }))).status, 2);
  await assert.rejects(readFile(path.join(ctx.inventory, 'ratifications.jsonl')), { code: 'ENOENT' });
});

test('an outstanding writer lock refuses without removing another process lock', async (t) => {
  const ctx = await setup(t);
  const bundle = await exported(ctx);
  const lock = path.join(ctx.inventory, '.content-review-return.lock');
  await writeFile(lock, 'other writer');
  assert.equal((await apply(ctx, response(bundle))).status, 2);
  assert.equal(await readFile(lock, 'utf8'), 'other writer');
});

test('bundle tampering and stale merged export are detected', async (t) => {
  const ctx = await setup(t);
  const bundle = await exported(ctx);
  bundle.tasks[0].unit.name = 'Tampered';
  await writeFile(path.join(ctx.bundle, 'bundle.json'), JSON.stringify(bundle));
  assert.equal((await apply(ctx, response(bundle))).status, 2);
  ctx.source.units[0].name = 'New source';
  await writeFile(path.join(ctx.inventory, 'judgment-units.json'), JSON.stringify(ctx.source));
  assert.equal(run(cli, ['--export', '--inventory', ctx.inventory, '--out', path.join(ctx.dir, 'new')]).status, 2);
});

test('spreadsheet formula prefixes are inert in CSV while bundle retains original text', async (t) => {
  const item = { ...unit('TITLE-01'), name: '=1+1' };
  const ctx = await setup(t, [item]);
  const bundle = await exported(ctx);
  assert.equal(bundle.tasks[0].unit.name, '=1+1');
  const csv = await readFile(path.join(ctx.bundle, 'review-tasks.csv'), 'utf8');
  assert.match(csv, /'=1\+1/);
});

test('completing an incomplete return names the draft it replaces', async (t) => {
  const ctx = await setup(t);
  await writeFile(path.join(ctx.inventory, 'ratifications.jsonl'),
    JSON.stringify({ id: 'TITLE-01', ratifier_note: 'Need product-owner context' }) + '\n');
  assert.equal(run(builder, ['--merge', '--inventory', ctx.inventory]).status, 0);
  const bundle = await exported(ctx);
  assert.match(bundle.tasks[0].base_decision_id, /^sha256:/);
  const payload = response(bundle, { supersedes: bundle.tasks[0].base_decision_id,
    supersession_reason: 'Owner supplied the missing context; reviewed the title again.' });
  assert.equal((await apply(ctx, payload)).status, 0);
  const history = (await readFile(path.join(ctx.inventory, 'ratifications.jsonl'), 'utf8')).trim().split('\n');
  assert.equal(history.length, 2);
  assert.equal(JSON.parse(history[0]).ratifier_note, 'Need product-owner context');
  assert.equal((await apply(ctx, payload)).status, 0);
});

test('a fresh explicit rereview can supersede a completed decision with a reason', async (t) => {
  const ctx = await setup(t);
  const first = await exported(ctx);
  assert.equal((await apply(ctx, response(first))).status, 0);
  assert.equal(run(builder, ['--merge', '--inventory', ctx.inventory]).status, 0);
  const updated = { ...ctx, bundle: path.join(ctx.dir, 'rereview') };
  assert.equal(run(cli, ['--export', '--all', '--inventory', ctx.inventory, '--out', updated.bundle]).status, 0);
  const bundle = JSON.parse(await readFile(path.join(updated.bundle, 'bundle.json'), 'utf8'));
  const payload = response(bundle, { ratified_judgment: 'no', ratified_utc: '2026-09-08T00:00:00Z',
    ratifier_note: 'The title omits which account is selected.', supersedes: bundle.tasks[0].base_decision_id,
    supersession_reason: 'Independent review found a missing distinction.' });
  assert.equal((await apply(updated, payload)).status, 0);
  assert.equal(run(builder, ['--merge', '--inventory', ctx.inventory]).status, 0);
  const merged = JSON.parse(await readFile(path.join(ctx.inventory, 'draft-judgments.json'), 'utf8'));
  assert.equal(merged.rows[0].ratified_judgment, 'no');
  assert.equal((await readFile(path.join(ctx.inventory, 'ratifications.jsonl'), 'utf8')).trim().split('\n').length, 2);
});

test('default export omits completed items and permits a partial return', async (t) => {
  const ctx = await setup(t, [unit('TITLE-01'), unit('TITLE-02')]);
  const bundle = await exported(ctx);
  assert.equal((await apply(ctx, response(bundle))).status, 0);
  assert.equal(run(builder, ['--merge', '--inventory', ctx.inventory]).status, 0);
  const next = await exported({ ...ctx, bundle: path.join(ctx.dir, 'next') });
  assert.deepEqual(next.tasks.map((task) => task.unit.id), ['TITLE-02']);
});

test('CLI refuses incomplete or mixed commands', () => {
  for (const args of [[], ['--export'], ['--apply', '--export'], ['--unknown'],
    ['--export', '--inventory', '/tmp', '--out'], ['--apply', '--all', '--inventory', '/tmp'],
    ['--export', '--export', '--inventory', '/tmp']]) {
    assert.equal(run(cli, args).status, 2, args.join(' '));
  }
});
