const escape = text => String(text).replaceAll('|', '\\|').replaceAll('\n', ' ');

export function distributionSummary(distribution) {
  const groups = new Map();
  for (const entry of distribution.skills) {
    const group = groups.get(entry.sourceRepo) || { count: 0, licenses: new Set() };
    group.count++;
    group.licenses.add(entry.license);
    groups.set(entry.sourceRepo, group);
  }
  return [
    `${distribution.skills.length} upstream skill packages are included, in addition to \`geekbye-cv-kit\`.`,
    '',
    '| Original repository | Included skills | Licenses |',
    '|---|---:|---|',
    ...[...groups].sort(([a], [b]) => a.localeCompare(b)).map(([repo, group]) =>
      `| [${repo}](https://github.com/${repo}) | ${group.count} | ${[...group.licenses].sort().join(', ')} |`),
  ].join('\n');
}

export function distributionInventory(distribution) {
  return [
    '# Redistributed skills',
    '',
    'This is an Aiescu-maintained distribution of upstream skills. Original authors retain their credits and licenses; inclusion does not imply their endorsement.',
    'This inventory is generated from `catalog/distribution.json`; each package includes `UPSTREAM.md` and license terms.',
    '',
    'Install a package with `npx skills@1 add aiescu/agent-skills --skill <install-name>`. Use `--list` to discover the available names.',
    'Duplicate names receive an upstream-owner prefix. This avoids silently installing a different author’s version.',
    '',
    'The CLI installs instructions and assets; it does not install every upstream plugin, hook, external service or runtime.',
    'Read the chosen skill and its source notes before use. Service-backed automation skills require the provider accounts, connections and tools described in their instructions.',
    '',
    '## Included packages',
    '',
    '| Install name | Original author | License | Pinned source |',
    '|---|---|---|---|',
    ...distribution.skills.map(e => `| [\`${e.name}\`](../${e.path}/SKILL.md) | ${escape(e.author)} | ${escape(e.license)} | [${e.sourceRepo}@${e.revision.slice(0, 7)}](https://github.com/${e.sourceRepo}/tree/${e.revision}/${e.sourcePath}) |`),
    '',
    '## Exclusions and upstream alternatives',
    '',
    'Excluded packages remain available at their original source where the author’s terms permit use.',
    '',
    '| Source | Reason |',
    '|---|---|',
    ...distribution.excluded.map(e => `| [${escape(e.sourceRepo + (e.sourcePath ? '/' + e.sourcePath : ''))}](https://github.com/${e.sourceRepo}${e.revision ? '/tree/' + e.revision : ''}${e.sourcePath ? '/' + e.sourcePath : ''}) | ${escape(e.reason)} |`),
    '',
    '## Updates and verification',
    '',
    'Packages are pinned snapshots, not automatic mirrors. To update one, inspect the new upstream revision and any per-file license overrides, preserve required notices, carry forward documented path adaptations, and update the manifest file hashes.',
    'Run `npm test`, `npm run build` and `npm run build:check`. Run `npm run test:distribution-install` for isolated CLI discovery and installation checks. Automated checks disable telemetry and do not manufacture Skills.sh installation counts.',
    'Tests verify package discovery and asset integrity; they do not execute every upstream script or validate third-party service credentials. A Skills.sh listing must be observed separately after genuine user installations.',
    '',
  ].join('\n');
}
