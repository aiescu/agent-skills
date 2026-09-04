// scripts/fetch-stars.mjs
// Usage: node scripts/fetch-stars.mjs   (uses GITHUB_TOKEN if set, else `gh api`)
import { writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { loadCatalog, STARS_PATH } from './lib/catalog.mjs';

async function fetchRepo(repo) {
  if (process.env.GITHUB_TOKEN) {
    const r = await fetch(`https://api.github.com/repos/${repo}`, {
      headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}`, 'User-Agent': 'aiescu-agent-skills' }
    });
    if (!r.ok) throw new Error(`${repo}: HTTP ${r.status}`);
    return r.json();
  }
  return JSON.parse(execFileSync('gh', ['api', `repos/${repo}`], { encoding: 'utf8' }));
}

const { entries } = loadCatalog();
const stars = {};
for (const e of entries) {
  const d = await fetchRepo(e.repo);
  stars[e.repo] = { stars: d.stargazers_count, pushedAt: d.pushed_at, spdx: d.license?.spdx_id ?? null };
  console.log(`${e.repo}: ${d.stargazers_count}`);
}
writeFileSync(STARS_PATH, JSON.stringify({ fetchedAt: new Date().toISOString().slice(0, 10), stars }, null, 2) + '\n');
console.log(`wrote ${STARS_PATH}`);
