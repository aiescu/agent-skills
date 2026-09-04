# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`aiescu/agent-skills` is a public, curated **showroom** of the most-starred AI agent skill
repositories (SKILL.md-based instruction packs for Claude Code, Codex, Gemini CLI, Cursor, etc.),
plus a one-command installer that fetches the upstream skills into the right directory for each agent.

It is NOT a fork and NOT a re-host. Upstream skills are credited, linked, and pulled from their
original repos at install time (or vendored only where the upstream license permits, with the
upstream LICENSE kept alongside). Business goal: an honest, useful public repo that earns stars and
sends referral traffic to aiescu products. The SEO landing page is `aiescu.com/agent-skills` in the separate `aiescu/aiescu-landing` repo; it reads `catalog/*.json` from this repo on `main`.

## Hard rules

- **Never copy a skill from a repo that has no license.** Link to it only.
- **Every vendored file keeps its upstream LICENSE and a `SOURCE.md`** (repo URL, commit SHA, date).
- **Star counts and rankings in the README are generated, never hand-typed.** Run the sync script;
  do not edit numbers by hand.
- **Product links stay in one footer/"Built by" block.** No promotional text inside skill
  descriptions or install output.
- Never mention Claude, Claude Code, or Anthropic in commit messages or PR descriptions.
- Base branch is `main`. Work on feature branches; never push to `main` directly.

## Planning docs

Implementation plans live in `docs/superpowers/plans/`. Read the latest plan before starting work;
it defines the file layout, install conventions, and task order.

## Commands

```bash
npm test              # node:test suites + installer contract test
npm run stars         # refresh catalog/stars.json from GitHub API (needs gh or GITHUB_TOKEN)
npm run build         # regenerate README.md, SOURCES.md, marketplaces
npm run build:check   # CI gate: fail if generated files are stale
bash install.sh --agent claude-code --dry-run
node --test tests/render.test.mjs   # single test file
```

Run `gh` as `env -u GH_TOKEN -u GITHUB_TOKEN gh ...` so keyring auth is used.

## Architecture

`catalog/skills.json` is the only hand-edited content. `scripts/build.mjs` renders it through pure
functions in `scripts/lib/` (`catalog.mjs` load/validate, `render.mjs` markdown, `marketplace.mjs`
plugin manifest) into every user-facing file. `install.sh` carries a baked-in copy of the repo list
for the curl-pipe path; `tests/install.test.sh` fails if it drifts from the catalog. The marketplace
deliberately omits per-plugin `version`: a literal value would pin plugins instead of tracking upstream.
`.lycheeignore` holds the aiescu.com/agent-skills link until that page is live; remove it then.
