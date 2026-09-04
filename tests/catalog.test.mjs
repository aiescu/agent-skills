import { test } from 'node:test';
import assert from 'node:assert/strict';
import { loadCatalog, validateEntry } from '../scripts/lib/catalog.mjs';

const base = { repo: 'a/b', author: 'x', authorUrl: 'u', title: 't', summary: 'ok', license: 'MIT', licenseNote: '', type: 'single', skillCount: 1, flagship: 'f', flagshipWhy: 'w', install: { skillsCli: 'a/b' }, whyIncluded: 'w' };

test('catalog has exactly 10 valid, unique entries', () => {
  const c = loadCatalog();
  assert.equal(c.entries.length, 10);
  const repos = c.entries.map(e => e.repo);
  assert.equal(new Set(repos).size, 10);
});

test('validateEntry rejects a promotional summary', () => {
  assert.throws(() => validateEntry({ ...base, summary: 'Try Keebye today!' }), /promotional/);
});

test('validateEntry rejects an entry with no install path', () => {
  assert.throws(() => validateEntry({ ...base, install: {} }), /no install path/);
});
