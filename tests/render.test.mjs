import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fmtStars, renderTable, renderSection, renderSources } from '../scripts/lib/render.mjs';

const e = {
  repo: 'obra/superpowers', author: 'Jesse Vincent (obra)', authorUrl: 'https://github.com/obra',
  title: 'Superpowers', summary: 'Methodology. More.', license: 'MIT', licenseNote: '', type: 'framework',
  skillCount: 14, flagship: 'brainstorming', flagshipWhy: 'Entry point.',
  install: { skillsCli: 'obra/superpowers', claudePlugin: '/plugin install superpowers@claude-plugins-official' },
  whyIncluded: 'Most-starred.'
};
const stars = { fetchedAt: '2026-09-04', stars: { 'obra/superpowers': { stars: 281672 } } };

test('fmtStars', () => {
  assert.equal(fmtStars(281672), '281.7k');
  assert.equal(fmtStars(950), '950');
  assert.equal(fmtStars(undefined), 'n/a');
});

test('table sorts by stars desc and links upstream', () => {
  const low = { ...e, repo: 'x/y', title: 'Y' };
  const s = { ...stars, stars: { ...stars.stars, 'x/y': { stars: 10 } } };
  const out = renderTable([low, e], s);
  assert.ok(out.indexOf('obra/superpowers') < out.indexOf('x/y'));
  assert.match(out, /\[obra\/superpowers\]\(https:\/\/github\.com\/obra\/superpowers\)/);
  assert.match(out, /281\.7k/);
});

test('section includes install commands, flagship and license', () => {
  const out = renderSection(e, stars);
  assert.match(out, /npx skills@1 add obra\/superpowers/);
  assert.match(out, /\/plugin install superpowers@claude-plugins-official/);
  assert.match(out, /MIT/);
  assert.match(out, /\*\*Flagship skill:\*\* `brainstorming`/);
});

test('sources table has one row per entry', () => {
  const out = renderSources([e, { ...e, repo: 'x/y' }]);
  assert.equal(out.split('\n').filter(l => l.startsWith('| [')).length, 2);
});
