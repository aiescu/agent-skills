// Regenerates README.md, SOURCES.md and the marketplaces from the catalog.
// --check: exit 1 if any generated file would change (CI gate).
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadCatalog, loadStars } from './lib/catalog.mjs';
import { renderTable, renderSection, renderSources, sortByStars } from './lib/render.mjs';
import { buildMarketplace } from './lib/marketplace.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const check = process.argv.includes('--check');
const { entries } = loadCatalog();
const stars = loadStars();
const updated = stars.fetchedAt ?? 'unknown';
const sorted = sortByStars(entries, stars);
const marketplace = JSON.stringify(buildMarketplace(sorted), null, 2) + '\n';

const outputs = {
  'README.md': readFileSync(path.join(ROOT, 'templates/README.tmpl.md'), 'utf8')
    .replaceAll('{{UPDATED}}', updated)
    .replace('{{TABLE}}', renderTable(entries, stars))
    .replace('{{SECTIONS}}', sorted.map(e => renderSection(e, stars)).join('\n\n')),
  'SOURCES.md': `# Sources and attribution\n\nGenerated ${updated}. Every entry links to its upstream repository; nothing is vendored here.\nIf you recognize your work and the credit is wrong, open an issue and it will be fixed first.\n\n${renderSources(sorted)}\n`,
  '.claude-plugin/marketplace.json': marketplace,
  '.agents/plugins/marketplace.json': marketplace,
};

let changed = 0;
for (const [rel, content] of Object.entries(outputs)) {
  const p = path.join(ROOT, rel);
  const current = existsSync(p) ? readFileSync(p, 'utf8') : null;
  if (current === content) continue;
  changed++;
  if (check) { console.error(`STALE: ${rel}`); continue; }
  mkdirSync(path.dirname(p), { recursive: true });
  writeFileSync(p, content);
  console.log(`wrote ${rel}`);
}
if (check && changed) { console.error(`${changed} generated file(s) out of date. Run: npm run build`); process.exit(1); }
if (!changed) console.log('up to date');
