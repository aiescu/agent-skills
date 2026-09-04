import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildMarketplace } from '../scripts/lib/marketplace.mjs';

const e = { repo: 'obra/superpowers', author: 'Jesse Vincent (obra)', authorUrl: 'https://github.com/obra', title: 'Superpowers', summary: 'S.', license: 'MIT', install: { claudePlugin: 'x' } };
const noPlugin = { ...e, repo: 'Leonxlnx/taste-skill', install: { skillsCli: 'Leonxlnx/taste-skill' } };

test('every plugin points at the upstream git URL and credits the original author', () => {
  const m = buildMarketplace([e]);
  assert.equal(m.name, 'aiescu-agent-skills');
  assert.equal(m.plugins.length, 1);
  const p = m.plugins[0];
  assert.equal(p.name, 'superpowers');
  assert.equal(p.source.source, 'url');
  assert.equal(p.source.url, 'https://github.com/obra/superpowers.git');
  assert.match(p.author.name, /^Jesse Vincent \(obra\) \(original\)/);
  assert.equal(p.author.url, 'https://github.com/obra');
  assert.equal(p.homepage, 'https://github.com/obra/superpowers');
});

test('entries without a plugin manifest are excluded', () => {
  assert.equal(buildMarketplace([e, noPlugin]).plugins.length, 1);
});

test('plugins are not pinned to a fake version', () => {
  const p = buildMarketplace([e]).plugins[0];
  assert.equal(Object.hasOwn(p, 'version'), false);
});

test('repos without a root plugin manifest are excluded', () => {
  const noRoot = { ...e, repo: 'anthropics/skills', install: { claudePlugin: 'x', pluginRoot: false } };
  assert.equal(buildMarketplace([e, noRoot]).plugins.length, 1);
});

test('colliding basenames get an owner prefix', () => {
  const a = { ...e, repo: 'mattpocock/skills' };
  const b = { ...e, repo: 'anthropics/skills' };
  const names = buildMarketplace([a, b, e]).plugins.map(p => p.name);
  assert.deepEqual(names, ['mattpocock-skills', 'anthropics-skills', 'superpowers']);
});
