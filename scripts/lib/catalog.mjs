import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
export const CATALOG_PATH = path.join(ROOT, 'catalog/skills.json');
export const STARS_PATH = path.join(ROOT, 'catalog/stars.json');

const REQUIRED = ['repo', 'author', 'authorUrl', 'title', 'summary', 'license', 'licenseNote', 'type', 'skillCount', 'flagship', 'flagshipWhy', 'install', 'whyIncluded'];
const PROMO = /\b(keebye|geekbye|pavleur|aiescu)\b|try .* today|sign up/i;

export function validateEntry(e) {
  for (const k of REQUIRED) if (!(k in e)) throw new Error(`${e.repo ?? '?'} missing ${k}`);
  if (!/^[\w.-]+\/[\w.-]+$/.test(e.repo)) throw new Error(`bad repo ${e.repo}`);
  if (PROMO.test(e.summary) || PROMO.test(e.whyIncluded) || PROMO.test(e.flagshipWhy)) throw new Error(`promotional text in ${e.repo}`);
  if (!e.install.skillsCli && !e.install.claudePlugin) throw new Error(`${e.repo} has no install path`);
  return e;
}

export function loadCatalog() {
  const c = JSON.parse(readFileSync(CATALOG_PATH, 'utf8'));
  c.entries.forEach(validateEntry);
  return c;
}

export function loadStars() {
  try { return JSON.parse(readFileSync(STARS_PATH, 'utf8')); }
  catch { return { fetchedAt: null, stars: {} }; }
}
