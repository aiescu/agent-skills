// Explicit network check: project-local installation, no agent execution or telemetry.
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, readdirSync, writeFileSync, statSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = process.argv[2] || root;
const sandbox = mkdtempSync(path.join(os.tmpdir(), 'aiescu-skills-install-'));
const env = { ...process.env, DISABLE_TELEMETRY: '1', DO_NOT_TRACK: '1', NO_COLOR: '1' };
delete env.GH_TOKEN;
delete env.GITHUB_TOKEN;
const manifest = JSON.parse(readFileSync(path.join(root, 'catalog/distribution.json'), 'utf8'));
const logs = [];
function run(args) {
  const result = spawnSync('npx', ['--yes', 'skills@1.5.26', 'add', source, ...args], {
    cwd: sandbox, env, encoding: 'utf8', timeout: 300000, maxBuffer: 32 * 1024 * 1024,
  });
  logs.push({ args, status: result.status, stdout: result.stdout, stderr: result.stderr });
  writeFileSync(path.join(sandbox, 'cli-log.json'), JSON.stringify(logs, null, 2));
  assert.equal(result.status, 0, `CLI failed: ${result.error || result.stderr}; log: ${sandbox}`);
  return result.stdout;
}
const listing = run(['--list']);
for (const entry of manifest.skills) assert.ok(listing.includes(entry.name), `not discovered: ${entry.name}`);
run(['--skill', '*', '--agent', 'codex', '--yes', '--copy']);
const installed = path.join(sandbox, '.agents/skills');
assert.deepEqual(readdirSync(installed).sort(), [...manifest.skills.map(e => e.name), 'geekbye-cv-kit'].sort());
function files(dir, relative = '') {
  return readdirSync(path.join(dir, relative)).flatMap(name => {
    const next = path.join(relative, name);
    return statSync(path.join(dir, next)).isDirectory() ? files(dir, next) : [next];
  });
}
let assetCount = 0;
for (const entry of manifest.skills) {
  const dir = path.join(installed, entry.name);
  assert.deepEqual(files(dir).sort(), Object.keys(entry.files).sort(), `installed inventory: ${entry.name}`);
  for (const [relative, expected] of Object.entries(entry.files)) {
    assert.equal(createHash('sha256').update(readFileSync(path.join(dir, relative))).digest('hex'), expected, `installed asset: ${entry.name}/${relative}`);
    assetCount++;
  }
}
console.log(`Discovered and installed ${manifest.skills.length + 1} skills; verified ${assetCount} redistributed assets. No upstream code executed; telemetry disabled. Local logs: ${sandbox}`);
