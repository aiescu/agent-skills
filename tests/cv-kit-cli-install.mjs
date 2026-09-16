// Explicit network check, excluded from npm test: isolates HOME, cache and project scope.
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = process.argv[2] || root;
const sandbox = mkdtempSync(path.join(os.tmpdir(), 'geekbye-cv-cli-'));
const project = path.join(sandbox, 'project');
mkdirSync(project);
const env = {
  ...process.env, HOME: path.join(sandbox, 'home'), XDG_CONFIG_HOME: path.join(sandbox, 'config'),
  npm_config_cache: path.join(sandbox, 'npm-cache'), DISABLE_TELEMETRY: '1', DO_NOT_TRACK: '1',
  PYTHONDONTWRITEBYTECODE: '1',
};
delete env.GH_TOKEN;
delete env.GITHUB_TOKEN;
const logs = [];
function run(command, args) {
  const result = spawnSync(command, args, { cwd: project, env, encoding: 'utf8', timeout: 180000 });
  logs.push({ command, args, exitCode: result.status, stdout: result.stdout, stderr: result.stderr });
  writeFileSync(path.join(sandbox, 'commands.json'), JSON.stringify(logs, null, 2) + '\n');
  assert.equal(result.status, 0, `${command} failed: ${result.error || result.stderr}\n${result.stdout}`);
  return result.stdout;
}
const cli = ['--yes', 'skills@1.5.26'];
assert.match(run('npx', [...cli, 'add', source, '--list']), /geekbye-cv-kit/);
run('npx', [...cli, 'add', source, '--skill', 'geekbye-cv-kit', '--agent', 'codex', '--yes', '--copy']);
const installed = path.join(project, '.agents/skills/geekbye-cv-kit');
assert.ok(existsSync(path.join(installed, 'SKILL.md')), 'targeted installation missing');
function files(dir, relative = '') {
  return readdirSync(path.join(dir, relative)).flatMap(name => {
    if (name === '__pycache__' || name.endsWith('.pyc')) return [];
    const next = path.join(relative, name);
    return statSync(path.join(dir, next)).isDirectory() ? files(dir, next) : [next];
  });
}
const localSource = path.join(root, 'skills/geekbye-cv-kit');
const hashes = {};
for (const relative of files(localSource)) {
  const expected = readFileSync(path.join(localSource, relative));
  const actual = readFileSync(path.join(installed, relative));
  assert.deepEqual(actual, expected, `asset differs: ${relative}`);
  hashes[relative] = createHash('sha256').update(actual).digest('hex');
}
const output = path.join(sandbox, 'example');
run(process.env.CV_KIT_PYTHON || 'python3', [path.join(installed, 'scripts/application.py'), 'render',
  '--master', path.join(installed, 'examples/early-career.json'),
  '--application', path.join(installed, 'examples/early-career.application.json'),
  '--output', output, '--compile', 'never']);
const artifacts = files(output);
for (const file of ['cv.tex', 'cv.md', 'cv.txt', 'cv.json', 'letter.tex', 'letter.md', 'letter.txt',
  'requirement-map.json', 'change-log.json', 'questions.json', 'validation.json']) {
  assert.ok(artifacts.includes(file), `missing output ${file}`);
}
assert.deepEqual(JSON.parse(readFileSync(path.join(output, 'master.json'), 'utf8')),
  JSON.parse(readFileSync(path.join(installed, 'examples/early-career.json'), 'utf8')), 'master changed');
assert.ok(!artifacts.some(file => file.endsWith('.pdf')), 'compile never must not claim PDF output');
writeFileSync(path.join(sandbox, 'evidence.json'), JSON.stringify({
  checkedAt: new Date().toISOString(), cliVersion: '1.5.26', source, scope: 'project',
  telemetry: 'disabled; test is not indexing activity', installed, output, hashes, artifacts,
  publicMainVerified: false, skillsShVisibilityVerified: false,
}, null, 2) + '\n');
console.log(`CLI discovery, targeted installation, ${Object.keys(hashes).length} assets and example passed. Evidence: ${sandbox}`);
