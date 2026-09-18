import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, lstatSync } from 'node:fs';
import { createHash } from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const distribution = JSON.parse(readFileSync(path.join(root, 'catalog/distribution.json'), 'utf8'));

function files(dir, relative = '') {
  return readdirSync(path.join(dir, relative)).flatMap(name => {
    const next = path.join(relative, name);
    const stat = lstatSync(path.join(dir, next));
    assert.ok(!stat.isSymbolicLink(), `unresolved package symlink: ${next}`);
    return stat.isDirectory() ? files(dir, next) : [next];
  });
}

test('redistributed packages have unique install names, provenance, licenses and exact asset inventories', () => {
  const names = new Set();
  for (const entry of distribution.skills) {
    assert.match(entry.name, /^[a-z0-9]+(?:-[a-z0-9]+)*$/);
    assert.ok(!names.has(entry.name), `duplicate CLI name: ${entry.name}`);
    names.add(entry.name);
    assert.equal(entry.path, `skills/${entry.name}`);
    assert.match(entry.revision, /^[a-f0-9]{40}$/);
    assert.match(entry.sourceRepo, /^[\w.-]+\/[\w.-]+$/);
    assert.ok(entry.author && entry.license && entry.sourcePath);
    const dir = path.join(root, entry.path);
    const actual = files(dir).sort();
    assert.deepEqual(actual, Object.keys(entry.files).sort(), `unrecorded or missing asset: ${entry.name}`);
    for (const required of ['SKILL.md', 'LICENSE', 'UPSTREAM.md']) assert.ok(actual.includes(required), `${entry.name}: missing ${required}`);
    for (const file of actual) {
      assert.equal(createHash('sha256').update(readFileSync(path.join(dir, file))).digest('hex'), entry.files[file], `${entry.name}/${file}: hash changed`);
    }
    const skill = readFileSync(path.join(dir, 'SKILL.md'), 'utf8');
    const frontmatter = skill.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    assert.ok(frontmatter, `${entry.name}: missing frontmatter`);
    const name = frontmatter[1].match(/^name:\s*["']?([^\r\n"']+)/m)?.[1].trim();
    assert.equal(name, entry.name, `${entry.name}: CLI name differs from folder`);
    assert.match(frontmatter[1], /^description:\s*\S/m);
    assert.doesNotMatch(frontmatter[1], /^\s*internal:\s*true/m);
    const source = readFileSync(path.join(dir, 'UPSTREAM.md'), 'utf8');
    assert.ok(source.includes(entry.sourceRepo) && source.includes(entry.revision), `${entry.name}: missing source pin`);
  }
  assert.deepEqual(readdirSync(path.join(root, 'skills')).sort(), [...names, 'geekbye-cv-kit'].sort());
});
