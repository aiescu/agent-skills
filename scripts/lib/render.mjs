export function fmtStars(n) {
  if (n == null) return 'n/a';
  return n >= 1000 ? `${(n / 1000).toFixed(1)}k` : String(n);
}

const gh = repo => `https://github.com/${repo}`;
const starsOf = (e, s) => s.stars[e.repo]?.stars;

export function sortByStars(entries, s) {
  return [...entries].sort((a, b) => (starsOf(b, s) ?? -1) - (starsOf(a, s) ?? -1));
}

export function renderTable(entries, s) {
  const rows = sortByStars(entries, s).map((e, i) =>
    `| ${i + 1} | [${e.repo}](${gh(e.repo)}) | ${fmtStars(starsOf(e, s))} | ${e.summary.split('. ')[0].replace(/\.$/, '')} | \`${e.flagship}\` | ${e.license} |`);
  return ['| # | Repository | Stars | What it is | Flagship skill | License |', '|---|---|---:|---|---|---|', ...rows].join('\n');
}

function installBlock(i) {
  const lines = [];
  if (i.skillsCli) lines.push(`# Any agent (Claude Code, Codex, Cursor, Gemini, Copilot, OpenCode, 70+ more)\nnpx skills@1 add ${i.skillsCli}`);
  if (i.skillsCliOne) lines.push(`# Only the flagship skill\n${i.skillsCliOne}`);
  if (i.claudePlugin) lines.push(`# Claude Code plugin\n${i.claudePlugin}`);
  if (i.codex) lines.push(`# Codex\n${i.codex}`);
  if (i.gemini) lines.push(`# Gemini CLI\n${i.gemini}`);
  if (i.cursor) lines.push(`# Cursor\n${i.cursor}`);
  if (i.cli) lines.push(`# Upstream CLI\n${i.cli}`);
  return '```bash\n' + lines.join('\n\n') + '\n```' + (i.note ? `\n\n> ${i.note}` : '');
}

export function renderSection(e, s) {
  const plural = e.skillCount === 1 ? '' : 's';
  return [
    `### ${e.title} ([${e.repo}](${gh(e.repo)}))`,
    '',
    `by [${e.author}](${e.authorUrl}) · ⭐ ${fmtStars(starsOf(e, s))} · ${e.skillCount} skill${plural} · ${e.license}`,
    '',
    e.summary,
    '',
    `**Flagship skill:** \`${e.flagship}\`. ${e.flagshipWhy}`,
    '',
    `**Why it's here:** ${e.whyIncluded}`,
    '',
    installBlock(e.install),
    e.licenseNote ? `\n> **License note:** ${e.licenseNote}` : '',
  ].join('\n');
}

export function renderSources(entries) {
  const rows = entries.map(e => `| [${e.repo}](${gh(e.repo)}) | [${e.author}](${e.authorUrl}) | ${e.license} | ${e.licenseNote || '-'} |`);
  return ['| Repository | Author | License | Notes |', '|---|---|---|---|', ...rows].join('\n');
}
