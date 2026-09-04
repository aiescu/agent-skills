// Builds a Claude Code / Codex plugin marketplace that references upstream repos by URL.
// Nothing is vendored. The author field credits the ORIGINAL author; crediting the
// curator here is what got ultimate-skills called out (issue #10).
//
// Schema: https://code.claude.com/docs/en/plugin-marketplaces
// `version` is deliberately omitted per plugin: setting it pins the plugin, so users
// would never receive upstream updates. Unpinned entries track the upstream default branch.
export function buildMarketplace(entries) {
  return {
    name: 'aiescu-agent-skills',
    owner: { name: 'aiescu', url: 'https://github.com/aiescu' },
    metadata: {
      description: 'Curated marketplace of the most popular agent skills. Every plugin installs from its original upstream repository.',
      version: '1.0.0'
    },
    plugins: entries
      .filter(e => e.install?.claudePlugin)
      .map(e => ({
        name: e.repo.split('/')[1],
        description: e.summary,
        author: { name: `${e.author} (original), curated by aiescu`, url: e.authorUrl },
        homepage: `https://github.com/${e.repo}`,
        license: e.license,
        source: { source: 'url', url: `https://github.com/${e.repo}.git` }
      }))
  };
}
