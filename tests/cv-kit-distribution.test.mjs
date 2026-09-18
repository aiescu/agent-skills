import { test } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync, realpathSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const skill = path.join(root, 'skills/geekbye-cv-kit');

test('original kit ships its callable runtime, schema, evidence and licensed examples', () => {
  for (const relative of [
    'SKILL.md', 'LICENSE', 'SOURCE.md', 'assets/candidate.schema.json', 'assets/empty.json',
    'scripts/application.py', 'scripts/pack.py', 'references/research.md',
    ...['early-career', 'senior', 'career-change', 'unicode-partial', 'ambiguous-dates']
      .flatMap(name => [`examples/${name}.json`, `examples/${name}.application.json`]),
  ]) {
    const file = path.join(skill, relative);
    assert.ok(existsSync(file), `missing installed asset: ${relative}`);
    assert.ok(realpathSync(file).startsWith(`${realpathSync(skill)}${path.sep}`), `asset escapes kit: ${relative}`);
  }
  const instructions = readFileSync(path.join(skill, 'SKILL.md'), 'utf8');
  assert.match(instructions, /^---\r?\nname: geekbye-cv-kit\r?\n/);
  assert.match(instructions, /\ndescription: [^\n]+/);
  assert.doesNotMatch(instructions, /internal:\s*true/);
  assert.match(readFileSync(path.join(skill, 'LICENSE'), 'utf8'), /MIT License/);
  function markdownLinks(dir) {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const file = path.join(dir, entry.name);
      if (entry.isDirectory()) { markdownLinks(file); continue; }
      if (!entry.name.endsWith('.md')) continue;
      const text = readFileSync(file, 'utf8');
      for (const match of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
        const target = match[1];
        if (/^(?:https?:|#)/.test(target)) continue;
        const linked = path.resolve(dir, target.split('#')[0]);
        assert.ok(linked.startsWith(`${skill}${path.sep}`), `relative link escapes installed kit: ${target}`);
        assert.ok(existsSync(linked), `broken installed link in ${entry.name}: ${target}`);
      }
    }
  }
  markdownLinks(skill);
});

test('original-kit documentation links its published listing and preserves telemetry choices', () => {
  const template = readFileSync(path.join(root, 'templates/README.tmpl.md'), 'utf8');
  const wrapper = readFileSync(path.join(root, 'install.sh'), 'utf8');
  assert.match(template, /npx skills@1 add aiescu\/agent-skills --skill geekbye-cv-kit/);
  assert.match(template, /https:\/\/www\.skills\.sh\/aiescu\/agent-skills\/geekbye-cv-kit/);
  assert.match(template, /DO_NOT_TRACK=1/);
  assert.doesNotMatch(template, /After this skill is published on main|No directory badge is added/);
  assert.match(wrapper, /DISABLE_TELEMETRY=1 \$SKILLS_CLI add "\$repo"/);
  assert.doesNotMatch(wrapper, /add aiescu\/agent-skills/);
  const originalSection = template.split('## Original Aiescu skill:')[1].split('## The list')[0];
  assert.doesNotMatch(originalSection, /https:\/\/(?:resume\.)?geekbye\.com/);
});
