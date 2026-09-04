// Builds a Claude Code / Codex plugin marketplace that references upstream repos by URL.
// Nothing is vendored. The author field credits the ORIGINAL author; crediting the
// curator here is what got ultimate-skills called out (issue #10).
//
// Schema: https://code.claude.com/docs/en/plugin-marketplaces
// `version` is deliberately omitted per plugin: setting it pins the plugin, so users
// would never receive upstream updates. Unpinned entries track the upstream default branch.
// Plugin names must be unique within a marketplace. Repos with a generic basename
// (two repos both called "skills") get an owner prefix.
function pluginNames(entries) {
  const counts = new Map();
  for (const e of entries) { const b = e.repo.split('/')[1]; counts.set(b, (counts.get(b) ?? 0) + 1); }
  return e => { const [o, b] = e.repo.split('/'); return counts.get(b) > 1 ? `${o.toLowerCase()}-${b}` : b; };
}

export function buildMarketplace(entries) {
  const eligible = entries.filter(e => e.install?.claudePlugin && e.install.pluginRoot !== false);
  const nameOf = pluginNames(eligible);
  return {
    name: 'aiescu-agent-skills',
    owner: { name: 'aiescu', url: 'https://github.com/aiescu' },
    metadata: {
      description: 'Curated marketplace of the most popular agent skills. Every plugin installs from its original upstream repository.',
      version: '1.0.0'
    },
    plugins: eligible
      .map(e => ({
        name: nameOf(e),
        description: e.summary,
        author: { name: `${e.author} (original), curated by aiescu`, url: e.authorUrl },
        homepage: `https://github.com/${e.repo}`,
        license: e.license,
        source: { source: 'url', url: `https://github.com/${e.repo}.git` }
      }))
  };
}
