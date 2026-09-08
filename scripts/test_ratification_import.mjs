import assert from 'node:assert/strict';
import { mkdtemp, readFile, rm, writeFile, mkdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';

import {
  decisionId,
  isCompleteClient,
  isCompleteWcag,
  parseRatifications,
  unitRevision,
  validateInventory,
} from '../.claude/skills/a11y-content-judgment/references/ratification-import.mjs';

const units = [{ id: 'unit-1', product: 'demo', type: 'link', name: 'Details' }, { id: 'unit-2', product: 'demo', type: 'image', name: 'Map' }];
const complete = (extra = {}) => ({ id: 'unit-1', ratified_by: 'Reviewer A', ratified_judgment: 'yes', ratified_utc: '2026-09-06T12:00:00Z', ...extra });
const lines = (...records) => records.map((record) => typeof record === 'string' ? record : JSON.stringify(record)).join('\n') + '\n';

test('unit revisions use canonical sorted-key JSON', () => {
  assert.equal(unitRevision({ b: 2, a: 1 }), unitRevision({ a: 1, b: 2 }));
});

test('inventory validation requires v1 schema and unique nonblank unit ids', () => {
  assert.doesNotThrow(() => validateInventory({ schema: 'judgment-units/v1', units }));
  assert.throws(() => validateInventory({ schema: 'other', units }), /invalid_inventory_schema/);
  assert.throws(() => validateInventory({ schema: 'judgment-units/v1', units: [{ id: 'dup' }, { id: 'dup' }] }), /duplicate_unit_id/);
  assert.throws(() => validateInventory({ schema: 'judgment-units/v1', units: [{ id: ' ' }] }), /invalid_unit_id/);
});

test('legacy complete WCAG records remain effective but are reported unpinned', () => {
  const result = parseRatifications(lines(complete()), units);
  assert.equal(result.wcag.get('unit-1').ratified_judgment, 'yes');
  assert.equal(result.summary.complete_wcag, 1);
  assert.equal(result.summary.unpinned_legacy, 1);
  assert.match(result.diagnostics[0].message, /unit_sha256/);
});

test('legacy date-only records retain day precision without weakening strict completeness', () => {
  const wcag = complete({ ratified_utc: '2026-09-02' });
  const client = { id: 'unit-2', scope: 'client', ratified_by: 'Reviewer B', ratified_client_result: 'meets-policy', ratified_utc: '2026-09-02' };
  const result = parseRatifications(lines(wcag, client), units);
  assert.equal(result.wcag.get('unit-1').date_precision, 'day');
  assert.equal(result.client.get('unit-2').date_precision, 'day');
  assert.equal(result.summary.legacy_day_precision_records, 2);
  assert.equal(result.diagnostics.filter((item) => item.code === 'legacy_day_precision').length, 2);
  assert.equal(isCompleteWcag(wcag), false);
  assert.equal(isCompleteClient(client), false);
});

test('date-only incomplete placeholder remains a sanitized draft', () => {
  const result = parseRatifications(lines({ id: 'unit-1', ratified_by: '', ratified_judgment: '', ratified_utc: '2026-09-02', ratifier_note: 'Deferred' }), units);
  const draft = result.drafts.get('wcag:unit-1');
  assert.equal(draft.date_precision, 'day');
  assert.deepEqual(draft.missing, ['ratified_by', 'ratified_judgment']);
  assert.equal(result.summary.legacy_day_precision_records, 1);
});

test('name-only return remains an incomplete draft', () => {
  const result = parseRatifications(lines({ id: 'unit-1', ratified_by: 'Reviewer A' }), units);
  assert.equal(result.wcag.size, 0);
  assert.equal(result.drafts.get('wcag:unit-1').ratified_by, undefined);
  assert.match(result.drafts.get('wcag:unit-1').ratifier_note, /Incomplete return/);
  assert.deepEqual(result.drafts.get('wcag:unit-1').missing, ['ratified_judgment', 'ratified_utc']);
  assert.equal(result.drafts.get('wcag:unit-1').date_precision, '');
});

test('complete client decision stays separate from WCAG', () => {
  const result = parseRatifications(lines({ id: 'unit-1', scope: 'client', ratified_by: 'Reviewer A', ratified_client_result: 'meets-policy', ratified_utc: '2026-09-06T12:00:00Z' }), units);
  assert.equal(result.wcag.size, 0);
  assert.equal(result.client.get('unit-1').ratified_client_result, 'meets-policy');
});

test('completeness predicates distinguish provenance from a name alone', () => {
  assert.equal(isCompleteWcag(complete()), true);
  assert.equal(isCompleteWcag({ id: 'unit-1', ratified_by: 'Reviewer A' }), false);
  assert.equal(isCompleteClient({ id: 'unit-1', scope: 'client', ratified_by: 'Reviewer A', ratified_client_result: 'meets-policy', ratified_utc: '2026-09-06T12:00:00Z' }), true);
  assert.equal(isCompleteClient({ id: 'unit-1', scope: 'client', ratified_by: 'Reviewer A' }), false);
  assert.equal(isCompleteWcag(complete({ ratified_utc: 'not-a-date' })), false);
  assert.equal(isCompleteClient({ id: 'unit-1', scope: 'client', ratified_by: 'Reviewer A', ratified_client_result: 'meets-policy', ratified_utc: 'not-a-date' }), false);
});

test('invalid syntax, id, scope, enum, timestamp, pin, and extra fields are rejected', () => {
  const cases = [
    ['{INVALID\n', 'invalid_json'],
    [lines(complete({ id: 'missing' })), 'unknown_id'],
    [lines(complete({ scope: 'other' })), 'invalid_scope'],
    [lines(complete({ ratified_judgment: 'pass' })), 'invalid_enum'],
    [lines(complete({ ratified_utc: '2026-02-30T12:00:00Z' })), 'invalid_timestamp'],
    [lines(complete({ ratified_utc: '2026-02-30' })), 'invalid_timestamp'],
    [lines(complete({ ratified_utc: '2026-09-06T08:00:00-04:00' })), 'invalid_timestamp'],
    [lines(complete({ ratified_utc: '2026-09-06', unit_sha256: unitRevision(units[0]) })), 'invalid_timestamp'],
    [lines(complete({ ratified_utc: '2026-09-06', supersedes: 'sha256:prior', supersession_reason: 'Correction' })), 'invalid_timestamp'],
    [lines(complete({ ratified_utc: '2026-09-06', supersession_reason: 'Correction' })), 'invalid_timestamp'],
    [lines(complete({ unit_sha256: `sha256:${'0'.repeat(64)}` })), 'unit_revision_mismatch'],
    [lines(complete({ unit_sha256: '   ' })), 'invalid_unit_revision'],
    [lines(complete({ ratified_client_result: 'meets-policy' })), 'scope_field_mismatch'],
    [lines(complete({ surprise: true })), 'unknown_field'],
  ];
  for (const [input, code] of cases) assert.throws(() => parseRatifications(input, units), (error) => error.errors.some((item) => item.code === code));
});

test('identical retry is idempotent but changed lineage is not silently ignored', () => {
  const record = complete();
  const retry = parseRatifications(lines(record, record), units);
  assert.equal(retry.wcag.size, 1);
  assert.equal(retry.summary.identical_retries, 1);
  const lineageChange = parseRatifications(lines(record, { ...record, supersedes: decisionId(record), supersession_reason: 'Correction' }), units);
  assert.equal(lineageChange.summary.identical_retries, 0);
  assert.equal(lineageChange.summary.supersessions, 1);
});

test('conflicts require an exact, reasoned supersession', () => {
  const first = complete();
  const second = complete({ ratified_by: 'Reviewer B', ratified_judgment: 'no', supersedes: decisionId(first), supersession_reason: 'Rechecked source context' });
  const result = parseRatifications(lines(first, second), units);
  assert.equal(result.wcag.get('unit-1').ratified_judgment, 'no');
  assert.equal(result.summary.supersessions, 1);
  assert.throws(() => parseRatifications(lines(first, { ...second, supersedes: 'sha256:stale' }), units), /invalid_supersession/);
  assert.throws(() => parseRatifications(lines(first, { ...second, supersession_reason: '' }), units), /invalid_supersession/);
});

test('orphan supersession fields are rejected before an initial record is accepted', () => {
  assert.throws(() => parseRatifications(lines(complete({ supersedes: 'sha256:orphan', supersession_reason: 'Correction' })), units), /orphan_supersession/);
  assert.throws(() => parseRatifications(lines(complete({ supersession_reason: 'Correction' })), units), /orphan_supersession/);
});

test('explicit supersession may return a decision to draft', () => {
  const first = complete();
  const withdrawal = { id: 'unit-1', ratifier_note: 'Needs another look', supersedes: decisionId(first), supersession_reason: 'Prior review used the wrong page state' };
  const result = parseRatifications(lines(first, withdrawal), units);
  assert.equal(result.wcag.size, 0);
  assert.equal(result.drafts.get('wcag:unit-1').ratifier_note, 'Needs another look');
  assert.equal(result.drafts.get('wcag:unit-1').decision_id, decisionId(withdrawal));
});

test('pinned decision includes the unit revision in its identity', () => {
  const pin = unitRevision(units[0]);
  const pinned = complete({ unit_sha256: pin });
  assert.notEqual(decisionId(pinned), decisionId(complete()));
  assert.equal(parseRatifications(lines(pinned), units).summary.pinned, 1);
});

test('pinned timestamp decision explicitly supersedes a legacy day decision', () => {
  const legacy = complete({ ratified_utc: '2026-09-02' });
  const legacyHash = decisionId(legacy);
  const modern = complete({ ratified_by: 'Reviewer B', ratified_utc: '2026-09-07T14:30:00Z', unit_sha256: unitRevision(units[0]), supersedes: legacyHash, supersession_reason: 'Re-reviewed against the pinned unit snapshot' });
  const result = parseRatifications(lines(legacy, modern), units);
  const effective = result.wcag.get('unit-1');
  assert.equal(legacy.ratified_utc, '2026-09-02');
  assert.equal(decisionId(legacy), legacyHash);
  assert.equal(effective.supersedes, legacyHash);
  assert.equal(effective.date_precision, 'timestamp');
  assert.equal(effective.pin_status, 'pinned');
  assert.equal(result.summary.supersessions, 1);
});

test('invalid import exits 2 without altering existing merge outputs', async () => {
  const dir = await mkdtemp(path.join(tmpdir(), 'ratification-import-'));
  try {
    await mkdir(path.join(dir, 'batches'));
    const unit = { ...units[0], sc: '2.4.4', view_count: 1, views: ['home'], href: '/details', detail: '', context: '', landmark: 'main', selector: 'a', visible: true, flags: [] };
    await writeFile(path.join(dir, 'judgment-units.json'), JSON.stringify({ schema: 'judgment-units/v1', units: [unit], views_ok: 1, views_skipped: [], nav_consistency: [] }));
    await writeFile(path.join(dir, 'batches', 'one.judged.jsonl'), lines({ id: 'unit-1', judgment: 'yes' }));
    await writeFile(path.join(dir, 'ratifications.jsonl'), '{INVALID\n');
    await writeFile(path.join(dir, 'draft-judgments.json'), 'sentinel');
    const script = path.resolve('.claude/skills/a11y-content-judgment/references/build-judgment-rows.mjs');
    const run = spawnSync(process.execPath, [script, '--merge', '--inventory', dir], { encoding: 'utf8' });
    assert.equal(run.status, 2);
    assert.match(run.stderr, /ratifications\.jsonl:1: invalid_json/);
    assert.equal(await readFile(path.join(dir, 'draft-judgments.json'), 'utf8'), 'sentinel');
  } finally { await rm(dir, { recursive: true, force: true }); }
});

test('invalid inventory schema and ids exit 2 without altering merge outputs', async () => {
  const invalidInventories = [
    { schema: 'other', units },
    { schema: 'judgment-units/v1', units: [{ ...units[0], id: 'dup' }, { ...units[1], id: 'dup' }] },
    { schema: 'judgment-units/v1', units: [{ ...units[0], id: '' }] },
  ];
  for (const inventory of invalidInventories) {
    const dir = await mkdtemp(path.join(tmpdir(), 'ratification-inventory-'));
    try {
      await mkdir(path.join(dir, 'batches'));
      await writeFile(path.join(dir, 'judgment-units.json'), JSON.stringify({ ...inventory, views_ok: 1, views_skipped: [], nav_consistency: [] }));
      await writeFile(path.join(dir, 'draft-judgments.json'), 'sentinel');
      const script = path.resolve('.claude/skills/a11y-content-judgment/references/build-judgment-rows.mjs');
      const run = spawnSync(process.execPath, [script, '--merge', '--inventory', dir], { encoding: 'utf8' });
      assert.equal(run.status, 2);
      assert.match(run.stderr, /judgment-units\.json: (?:invalid_|duplicate_unit_id)/);
      assert.equal(await readFile(path.join(dir, 'draft-judgments.json'), 'utf8'), 'sentinel');
    } finally { await rm(dir, { recursive: true, force: true }); }
  }
});
