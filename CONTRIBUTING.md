# Contributing

## Proposing a repo

Open a "Propose a repo" issue. To be listed, a repo must:

1. Ship SKILL.md-style skills installable via `npx skills add`, a plugin marketplace, or its own CLI.
2. Be among the most-starred in its category. The list stays at 10; entries rotate.
3. Have a license file, or be linkable without copying. We never vendor.
4. Have been installed and used by a maintainer. Say what it did for you.

Repos that are primarily vendored copies of other people's skills are not listed.

## Editing an entry

All content comes from `catalog/skills.json`. Edit that, run `npm run build`, commit the generated
files. Never edit `README.md`, `SOURCES.md`, or the marketplaces by hand; CI
rejects stale output. Star counts come from `npm run stars`; never type a number.

## Attribution problems

If you recognize your work and the credit, license, or description is wrong, open an
"Attribution" issue. It is fixed before anything else.

## Development

```bash
npm test
npm run build
npm run build:check
```
