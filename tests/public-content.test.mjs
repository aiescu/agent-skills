import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

test('tracked public content excludes internal notes and machine-specific evidence', () => {
  const paths = execFileSync('git', ['ls-files', '-z'], { cwd: root, encoding: 'utf8' }).split('\0').filter(Boolean);
  for (const relative of paths) {
    const file = path.join(root, relative);
    if (!existsSync(file)) continue;
    assert.doesNotMatch(relative, /(?:^|\/)docs\/(?:superpowers\/)?plans\//, `internal plan: ${relative}`);
    assert.doesNotMatch(relative, /(?:^|\/)[^/]*(?:handoff|handover)[^/]*$/i, `internal handoff: ${relative}`);
    assert.doesNotMatch(relative, /(?:^|\/)\.env(?:\.|$)/, `environment file: ${relative}`);
    const bytes = readFileSync(file);
    if (bytes.includes(0)) continue;
    const text = bytes.toString('utf8');
    assert.doesNotMatch(text, /\/(?:Users|home)\/[A-Za-z0-9_.-]+\//, `personal path: ${relative}`);
    assert.doesNotMatch(text, /\/var\/folders\//, `machine-specific log: ${relative}`);
    assert.doesNotMatch(text, /aiescu\/geek-bye-(?:landing|backend)/, `private repository reference: ${relative}`);
    assert.doesNotMatch(text, /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, `private key: ${relative}`);
  }
});
