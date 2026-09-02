#!/usr/bin/env node

/**
 * hash-evidence.mjs — append-only SHA-256 checksum manifest for an evidence tree.
 *
 * Retention rule reference: a11y-test SKILL.md § "Evidence retention
 * (append-only)" — never overwrite a captured evidence run; retention is
 * what makes silent errors findable. This script makes that rule
 * checkable: it writes a `checksums.json` manifest recording each file's
 * hash and size, and `--verify` recomputes every entry to report drift.
 *
 * Node stdlib only (node:crypto, node:fs/promises, node:path) — no
 * dependencies.
 *
 * Usage:
 *   node hash-evidence.mjs [--root <dir>] [--out <file>]
 *     Write a new manifest (default out: <root>/checksums.json). Refuses
 *     to overwrite an existing manifest (exit 2) unless --append is also
 *     given.
 *
 *   node hash-evidence.mjs --append [--root <dir>] [--out <file>]
 *     Add entries for files not yet listed. Never rewrites an existing
 *     entry. If a listed file's current hash differs from its recorded
 *     entry, that is drift, not an append — refused, exit 1, with every
 *     drifted path listed.
 *
 *   node hash-evidence.mjs --verify [--root <dir>] [--out <file>] [--json] [--strict]
 *     Recompute every listed entry against disk. Reports three classes:
 *       modified  — hash differs from the manifest
 *       missing   — listed in the manifest, absent from disk
 *       new       — present on disk, not in the manifest (informational
 *                   unless --strict, which promotes it to drift too)
 *     --json prints the drift report as JSON to stdout instead of the
 *     human-readable summary + listing.
 *
 * Exit codes:
 *   0  success — manifest written/appended cleanly, or --verify found no drift
 *   1  drift — --verify found modified/missing entries (or new entries
 *      under --strict), or --append found a changed listed file
 *   2  refusal/usage error — write mode targeted an existing manifest
 *      without --append, --append/--verify targeted a missing manifest,
 *      an unrecognized flag, or a --root that does not exist
 *
 * What this is NOT: not a signing or custody system, and it does not
 * prevent tampering. A manifest can be deleted by whoever can delete the
 * evidence it describes. It makes silent edits *findable*, not impossible.
 * Symbolic links inside the tree are not followed and are not listed —
 * a symlinked file is invisible to both write and --verify (even --strict).
 */

import { createHash } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const SCHEMA_VERSION = '1.0';
const ALGORITHM = 'sha256';
const DEFAULT_OUT_NAME = 'checksums.json';
const SKIP_DIRS = new Set(['node_modules', '.git']);

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  const root = path.resolve(opts.root ?? '.');
  const outFile = path.resolve(opts.out ?? path.join(root, DEFAULT_OUT_NAME));

  if (opts.verify) {
    process.exitCode = await cmdVerify(root, outFile, opts);
  } else if (opts.append) {
    process.exitCode = await cmdAppend(root, outFile);
  } else {
    process.exitCode = await cmdWrite(root, outFile);
  }
}

function parseArgs(argv) {
  const opts = { append: false, verify: false, strict: false, json: false };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--root') opts.root = argv[++i];
    else if (arg === '--out') opts.out = argv[++i];
    else if (arg === '--append') opts.append = true;
    else if (arg === '--verify') opts.verify = true;
    else if (arg === '--strict') opts.strict = true;
    else if (arg === '--json') opts.json = true;
    else throw new Error(`unrecognized argument: ${arg}`);
  }
  return opts;
}

async function walkFiles(root, skipAbsPaths) {
  const results = [];
  async function walk(dir) {
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const abs = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (SKIP_DIRS.has(entry.name)) continue;
        await walk(abs);
      } else if (entry.isFile() && !skipAbsPaths.has(abs)) {
        results.push(abs);
      }
    }
  }
  await walk(root);
  return results.map((abs) => path.relative(root, abs).split(path.sep).join('/')).sort();
}

async function hashFile(absPath) {
  const hash = createHash(ALGORITHM);
  let bytes = 0;
  await new Promise((resolve, reject) => {
    const stream = createReadStream(absPath);
    stream.on('data', (chunk) => {
      bytes += chunk.length;
      hash.update(chunk);
    });
    stream.on('end', resolve);
    stream.on('error', reject);
  });
  return { sha256: hash.digest('hex'), bytes };
}

async function buildEntries(root, relFiles) {
  const entries = {};
  for (const rel of relFiles) entries[rel] = await hashFile(path.join(root, rel));
  return entries;
}

function newManifest(root, entries) {
  return {
    schema_version: SCHEMA_VERSION,
    algorithm: ALGORITHM,
    root: path.relative(process.cwd(), root) || '.',
    generated_at: new Date().toISOString(),
    entries,
  };
}

async function loadManifest(outFile) {
  try {
    return JSON.parse(await readFile(outFile, 'utf8'));
  } catch (err) {
    if (err.code === 'ENOENT') return null;
    throw err;
  }
}

async function saveManifest(outFile, manifest) {
  await mkdir(path.dirname(outFile), { recursive: true });
  await writeFile(outFile, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
}

async function cmdWrite(root, outFile) {
  const existing = await loadManifest(outFile);
  if (existing) {
    console.error(`refusing to overwrite existing manifest: ${outFile}`);
    console.error('pass --append to add new entries without touching existing ones.');
    return 2;
  }
  const relFiles = await walkFiles(root, new Set([outFile]));
  const manifest = newManifest(root, await buildEntries(root, relFiles));
  await saveManifest(outFile, manifest);
  console.log(`wrote ${outFile}: ${relFiles.length} entries`);
  return 0;
}

async function cmdAppend(root, outFile) {
  const existing = await loadManifest(outFile);
  if (!existing) {
    console.error(`no manifest at ${outFile} to append to; run without --append first.`);
    return 2;
  }
  const relFiles = await walkFiles(root, new Set([outFile]));
  const onDisk = new Set(relFiles);
  const drifted = [];
  for (const rel of Object.keys(existing.entries)) {
    if (!onDisk.has(rel)) continue; // absence is --verify's 'missing', not append's concern
    const current = await hashFile(path.join(root, rel));
    if (current.sha256 !== existing.entries[rel].sha256) drifted.push(rel);
  }
  if (drifted.length > 0) {
    console.error('refusing to append: listed file(s) changed since capture (append-only, not an update):');
    for (const rel of drifted) console.error(`  modified: ${rel}`);
    return 1;
  }
  const newFiles = relFiles.filter((rel) => !(rel in existing.entries));
  const manifest = { ...existing, entries: { ...existing.entries, ...(await buildEntries(root, newFiles)) } };
  await saveManifest(outFile, manifest);
  console.log(`appended ${outFile}: ${newFiles.length} new entries (${Object.keys(existing.entries).length} unchanged)`);
  return 0;
}

async function cmdVerify(root, outFile, opts) {
  const existing = await loadManifest(outFile);
  if (!existing) {
    console.error(`no manifest at ${outFile} to verify.`);
    return 2;
  }
  const relFiles = await walkFiles(root, new Set([outFile]));
  const onDisk = new Set(relFiles);
  const listed = new Set(Object.keys(existing.entries));
  const modified = [];
  const missing = [];
  const added = relFiles.filter((rel) => !listed.has(rel));

  for (const rel of Object.keys(existing.entries)) {
    if (!onDisk.has(rel)) {
      missing.push(rel);
      continue;
    }
    const current = await hashFile(path.join(root, rel));
    if (current.sha256 !== existing.entries[rel].sha256) modified.push(rel);
  }

  const isDrift = modified.length > 0 || missing.length > 0 || (opts.strict && added.length > 0);
  if (opts.json) {
    const drift = modified.length > 0 || missing.length > 0 || (opts.strict && added.length > 0);
    console.log(JSON.stringify({ drift, modified, missing, new: added }, null, 2));
  } else {
    console.log(
      `verify: ${modified.length} modified, ${missing.length} missing, ${added.length} new` +
        (opts.strict ? ' (strict: new counts as drift)' : ' (new is informational)')
    );
    for (const rel of modified) console.log(`  modified: ${rel}`);
    for (const rel of missing) console.log(`  missing:  ${rel}`);
    for (const rel of added) console.log(`  new:      ${rel}`);
  }
  return isDrift ? 1 : 0;
}

main().catch((err) => {
  console.error(err.message ?? err);
  process.exitCode = 2;
});
