// Regenerates README.md, SOURCES.md and the marketplaces from the catalog.
// --check: exit 1 if any generated file would change (CI gate).
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadCatalog, loadStars } from './lib/catalog.mjs';
import { renderTable, renderSection, renderSources, sortByStars } from './lib/render.mjs';
import { distributionSummary, distributionInventory } from './lib/distribution.mjs';
import { buildMarketplace } from './lib/marketplace.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const check = process.argv.includes('--check');
const { entries } = loadCatalog();
const stars = loadStars();
const updated = stars.fetchedAt ?? 'unknown';
const sorted = sortByStars(entries, stars);
const distribution = JSON.parse(readFileSync(path.join(ROOT, 'catalog/distribution.json'), 'utf8'));
const marketplace = JSON.stringify(buildMarketplace(sorted), null, 2) + '\n';

const outputs = {
  'README.md': readFileSync(path.join(ROOT, 'templates/README.tmpl.md'), 'utf8')
    .replaceAll('{{UPDATED}}', updated)
    .replace('{{DISTRIBUTION_SUMMARY}}', distributionSummary(distribution))
    .replace('{{TABLE}}', renderTable(entries, stars))
    .replace('{{SECTIONS}}', sorted.map(e => renderSection(e, stars)).join('\n\n')),
  'SOURCES.md': `# Sources and attribution\n\nGenerated ${updated}. Every catalog entry links to its upstream repository. Redistributed skill packages retain their upstream licenses and notices; see [the pinned distribution inventory](docs/DISTRIBUTION.md).\nIf you recognize your work and the credit is wrong, open an issue and it will be fixed first.\n\n${renderSources(sorted)}\n\n## Original Aiescu skills\n\n\`skills/geekbye-cv-kit/\` is original work maintained by Aiescu, separate from this curated catalog.\nIts license and source credits ship inside the skill; ecosystem research is in\n[research.md](skills/geekbye-cv-kit/references/research.md). No upstream skill was copied for this kit.\n`,
  'docs/DISTRIBUTION.md': distributionInventory(distribution),
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
