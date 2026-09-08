import { createHash } from 'node:crypto';

const ALLOWED = new Set([
  'id', 'scope', 'ratified_by', 'ratified_judgment', 'ratified_client_result',
  'ratifier_note', 'ratified_utc', 'ruling', 'unit_sha256', 'decision_id',
  'supersedes', 'supersession_reason',
]);
const JUDGMENTS = new Set(['yes', 'no', 'unsure']);
const text = (value) => typeof value === 'string' && value.trim() !== '';

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (!value || typeof value !== 'object') return value;
  return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])]));
}

function digest(value) {
  return `sha256:${createHash('sha256').update(JSON.stringify(canonical(value))).digest('hex')}`;
}

export function unitRevision(unit) {
  return digest(unit);
}

function normalizedRecord(record) {
  const scope = record.scope ?? 'wcag';
  const entries = Object.entries({ ...record, scope }).filter(([key]) => key !== 'decision_id');
  return Object.fromEntries(entries);
}

export function decisionId(record) {
  const excluded = new Set(['decision_id', 'supersedes', 'supersession_reason']);
  const entries = Object.entries(normalizedRecord(record)).filter(([key]) => !excluded.has(key));
  return digest(Object.fromEntries(entries));
}

function validUtc(value) {
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,9}))?Z$/.exec(value);
  if (!match) return false;
  const [, year, month, day, hour, minute, second] = match;
  const date = new Date(Date.UTC(+year, +month - 1, +day, +hour, +minute, +second));
  return date.getUTCFullYear() === +year && date.getUTCMonth() === +month - 1 &&
    date.getUTCDate() === +day && date.getUTCHours() === +hour &&
    date.getUTCMinutes() === +minute && date.getUTCSeconds() === +second;
}

function validDay(value) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) return false;
  const [, year, month, day] = match; const date = new Date(Date.UTC(+year, +month - 1, +day));
  return date.getUTCFullYear() === +year && date.getUTCMonth() === +month - 1 && date.getUTCDate() === +day;
}

function legacyDayAllowed(record) {
  return validDay(record.ratified_utc) && ['unit_sha256', 'decision_id', 'supersedes', 'supersession_reason'].every((key) => record[key] === undefined);
}

function requiredFields(record, scope) {
  const result = scope === 'client' ? 'ratified_client_result' : 'ratified_judgment';
  return ['ratified_by', result, 'ratified_utc'].filter((key) => !text(record[key]));
}

export function isCompleteWcag(record) {
  return requiredFields(record, 'wcag').length === 0 && JUDGMENTS.has(record.ratified_judgment) && validUtc(record.ratified_utc);
}

export function isCompleteClient(record) {
  return requiredFields(record, 'client').length === 0 && validUtc(record.ratified_utc);
}

function issue(line, code, message) {
  return { line, code, message };
}

function validateTypes(record, line, errors) {
  for (const key of ALLOWED) {
    if (record[key] !== undefined && typeof record[key] !== 'string') {
      errors.push(issue(line, 'invalid_type', `${key} must be a string`));
    }
  }
  for (const key of Object.keys(record)) {
    if (!ALLOWED.has(key)) errors.push(issue(line, 'unknown_field', `unsupported field ${key}`));
  }
}

function validateValues(record, line, units, errors) {
  const scope = record.scope ?? 'wcag';
  if (!['wcag', 'client'].includes(scope)) errors.push(issue(line, 'invalid_scope', `scope must be wcag or client`));
  if (scope === 'client' && record.ratified_judgment !== undefined) errors.push(issue(line, 'scope_field_mismatch', `client scope cannot carry ratified_judgment`));
  if (scope === 'wcag' && record.ratified_client_result !== undefined) errors.push(issue(line, 'scope_field_mismatch', `wcag scope cannot carry ratified_client_result`));
  if (!text(record.id) || !units.has(record.id)) errors.push(issue(line, 'unknown_id', `id is not present in judgment-units.json`));
  if (text(record.ratified_judgment) && !JUDGMENTS.has(record.ratified_judgment)) errors.push(issue(line, 'invalid_enum', `ratified_judgment must be yes, no, or unsure`));
  if (text(record.ratified_utc) && !validUtc(record.ratified_utc) && !legacyDayAllowed(record)) errors.push(issue(line, 'invalid_timestamp', `ratified_utc must be a real RFC 3339 UTC timestamp ending in Z, or an unpinned legacy day`));
  if (record.unit_sha256 !== undefined && !/^sha256:[0-9a-f]{64}$/.test(record.unit_sha256)) errors.push(issue(line, 'invalid_unit_revision', `unit_sha256 must be an exact sha256 digest`));
  else if (record.unit_sha256 !== undefined && units.has(record.id) && record.unit_sha256 !== unitRevision(units.get(record.id))) errors.push(issue(line, 'unit_revision_mismatch', `unit_sha256 does not match ${record.id}`));
}

function validateRecord(record, line, units, errors) {
  if (!record || Array.isArray(record) || typeof record !== 'object') {
    errors.push(issue(line, 'invalid_record', 'line must contain a JSON object'));
    return;
  }
  validateTypes(record, line, errors);
  validateValues(record, line, units, errors);
  const computed = decisionId(record);
  if (record.decision_id !== undefined && record.decision_id !== computed) errors.push(issue(line, 'decision_id_mismatch', `decision_id must equal ${computed}`));
}

export class RatificationImportError extends Error {
  constructor(errors) {
    super(errors.map((error) => `${error.code}: ${error.message}`).join('; '));
    this.name = 'RatificationImportError';
    this.errors = errors;
  }
}

export function validateUnits(unitObjects) {
  if (!Array.isArray(unitObjects)) throw new RatificationImportError([issue(0, 'invalid_units', 'units must be an array')]);
  const units = new Map(); const errors = [];
  unitObjects.forEach((unit, index) => {
    if (!unit || Array.isArray(unit) || typeof unit !== 'object') { errors.push(issue(index + 1, 'invalid_unit', 'unit must be an object')); return; }
    if (!text(unit.id)) { errors.push(issue(index + 1, 'invalid_unit_id', 'unit id must be a nonblank string')); return; }
    if (units.has(unit.id)) errors.push(issue(index + 1, 'duplicate_unit_id', `duplicate unit id ${unit.id}`));
    else units.set(unit.id, unit);
  });
  if (errors.length) throw new RatificationImportError(errors);
  return units;
}

export function validateInventory(inventory) {
  if (!inventory || Array.isArray(inventory) || typeof inventory !== 'object') throw new RatificationImportError([issue(0, 'invalid_inventory', 'inventory must be an object')]);
  if (inventory.schema !== 'judgment-units/v1') throw new RatificationImportError([issue(0, 'invalid_inventory_schema', 'schema must be judgment-units/v1')]);
  return validateUnits(inventory.units);
}

function parseLines(input, units) {
  const errors = []; const records = [];
  input.split(/\r?\n/).forEach((line, index) => {
    if (!line.trim()) return;
    try {
      const record = JSON.parse(line);
      validateRecord(record, index + 1, units, errors);
      records.push({ line: index + 1, record });
    } catch (error) {
      if (error instanceof SyntaxError) errors.push(issue(index + 1, 'invalid_json', error.message));
      else throw error;
    }
  });
  if (errors.length) throw new RatificationImportError(errors);
  return records;
}

function semanticRecord(record) {
  return JSON.stringify(canonical(normalizedRecord(record)));
}

function resolveRecords(records, diagnostics) {
  const current = new Map(); let retries = 0; let supersessions = 0;
  for (const entry of records) {
    const scope = entry.record.scope ?? 'wcag'; const key = `${scope}:${entry.record.id}`;
    const prior = current.get(key);
    if (!prior && (entry.record.supersedes !== undefined || entry.record.supersession_reason !== undefined)) throw new RatificationImportError([issue(entry.line, 'orphan_supersession', `${key} has supersession fields but no prior decision`)]);
    if (!prior) { current.set(key, entry); continue; }
    if (semanticRecord(prior.record) === semanticRecord(entry.record)) {
      retries += 1; diagnostics.push({ line: entry.line, level: 'info', code: 'identical_retry', message: `${key} repeats an identical record` }); continue;
    }
    const valid = entry.record.supersedes === decisionId(prior.record) && text(entry.record.supersession_reason);
    if (!valid) throw new RatificationImportError([issue(entry.line, entry.record.supersedes ? 'invalid_supersession' : 'conflicting_decision', `${key} differs from the current decision without an exact, reasoned supersession`)]);
    supersessions += 1; current.set(key, entry);
  }
  return { current, retries, supersessions };
}

function incompleteDraft(record, missing, datePrecision) {
  const note = text(record.ratifier_note) ? record.ratifier_note : `Incomplete return: missing ${missing.join(', ')}`;
  return { ratifier_note: note, ruling: record.ruling || '', unit_sha256: record.unit_sha256 || '', decision_id: decisionId(record), date_precision: datePrecision, missing };
}

export function parseRatifications(input, unitObjects) {
  const units = validateUnits(unitObjects);
  const diagnostics = []; const records = parseLines(input, units);
  const { current, retries, supersessions } = resolveRecords(records, diagnostics);
  const wcag = new Map(); const client = new Map(); const drafts = new Map();
  let pinned = 0; let unpinned = 0; let legacyDays = 0;
  for (const [key, { line, record }] of current) {
    const scope = record.scope ?? 'wcag'; const missing = requiredFields(record, scope); const datePrecision = !text(record.ratified_utc) ? '' : validDay(record.ratified_utc) ? 'day' : 'timestamp';
    if (datePrecision === 'day') { legacyDays += 1; diagnostics.push({ line, level: 'warning', code: 'legacy_day_precision', message: `${key} preserves a legacy day-only ratified_utc without inventing a time` }); }
    if (missing.length) {
      drafts.set(key, incompleteDraft(record, missing, datePrecision));
      diagnostics.push({ line, level: 'warning', code: 'incomplete_return', message: `${key} remains draft; missing ${missing.join(', ')}` });
      continue;
    }
    const effective = { ...record, scope, decision_id: decisionId(record), pin_status: record.unit_sha256 ? 'pinned' : 'legacy_unpinned', date_precision: datePrecision };
    (scope === 'client' ? client : wcag).set(record.id, effective);
    if (record.unit_sha256) pinned += 1;
    else { unpinned += 1; diagnostics.push({ line, level: 'warning', code: 'legacy_unpinned', message: `${key} has no unit_sha256; preserved as a legacy unpinned decision` }); }
  }
  return { wcag, client, drafts, diagnostics, summary: { records: records.length, complete_wcag: wcag.size, complete_client: client.size, drafts: drafts.size, pinned, unpinned_legacy: unpinned, legacy_day_precision_records: legacyDays, identical_retries: retries, supersessions } };
}
