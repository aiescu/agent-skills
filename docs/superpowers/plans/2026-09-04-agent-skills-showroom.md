# Agent Skills Showroom Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `aiescu/agent-skills`, a public, link-first "showroom" of the 10 most-starred AI agent skill repos with a one-command multi-agent installer, that earns stars honestly and sends referral traffic to aiescu products.

**Architecture:** One JSON catalog (`catalog/skills.json`) is the single source of truth. A dependency-free Node script generates the README table, the Claude/Codex plugin marketplaces, from it, refreshing star counts from the GitHub API with a datestamp. The installer is a thin wrapper around the de-facto standard `npx skills` CLI (Vercel Labs) plus native plugin-marketplace commands, so **we redistribute zero upstream bytes**: every entry points at the upstream repo by URL.

**Tech Stack:** Bash, Node 20+ (`node:test`, no npm deps), GitHub Actions. `npx skills@1` for installs. The SEO landing page lives in the separate `aiescu/aiescu-landing` Next.js 15 repo (the ecosystem hub) and reads the catalog from this repo.

---

## Research summary that shaped this plan

Three Opus research agents ran on 2026-09-04. Findings that decide the design:

1. **Link, don't vendor.** Claude Code and Codex `marketplace.json` accept `{"source":"url","url":"https://github.com/<owner>/<repo>.git"}` (verified in `obra/superpowers-marketplace`). A curated marketplace of third-party skills that vendors nothing is (a) the only unoccupied position in the space (the best existing one has 82 stars) and (b) immune to every licensing complaint. Every documented backlash case (Cisco vs ai-skill-scanner #3, hacker-bob/Mantis #49, claude-code-templates #121, ultimate-skills #10) was about vendoring without per-item license/provenance, and all played out in GitHub issues, not social media.
2. **Licenses are messy upstream.** `anthropics/skills` has no repo license; its `docx/pdf/pptx/xlsx` are "all rights reserved, no redistribution" (ComposioHQ vendors them anyway; do not copy that). `multica-ai/andrej-karpathy-skills` and `ComposioHQ/awesome-claude-skills` claim licenses in README prose only, with no LICENSE file. `caveman` is MIT skills + BSL-1.1 engine + trademarked name. Linking handles all of these.
3. **GitHub passes zero SEO link equity.** All README links are `rel="nofollow"`; `/tree/` is disallowed in robots.txt. What ranks: the **repo description** (becomes the Google title), **topics**, and a **page on a domain we own**. aiescu.com is live, is the ecosystem hub, and already has SEO rails (`/compare`, `/guides`, `/glossary`, `/free-tools`, sitemap, llms.txt). The showroom page goes there as `aiescu.com/agent-skills`, with dofollow links to the three products. Traffic comes from a Hacker News launch (peer-reviewed study: mean +289 stars at 7 days, best window 12:00–17:00 UTC weekdays, "Show HN" gives no advantage), Reddit r/ClaudeAI, and the skills.sh leaderboard badge.
4. **Never** buy/trade stars (GitHub AUP; 90% of flagged repos get deleted and fake stars produce negative long-term growth), credit ourselves as `author` in manifests, or fork `hesreallyhim/awesome-claude-code` (CC BY-NC-ND, explicitly anti-aggregator).
5. **Installer:** `npx skills` is MIT, ~9M weekly downloads, maintains a 77-agent path table. Wrap it, don't rewrite it. `~/.codex/skills` is deprecated; Codex reads `.agents/skills/`. Awesome-list norms: not AI-generated, CC license on the list content, `contributing.md`, inclusion criteria.
6. **Product link:** Keebye is the only aiescu product whose audience *is* terminal-driven agent users. It gets the primary footer link; Pavleur and GeekBye ride as a trailing mention. `aiescu/agent-skills` already exists, public, with empty description/homepage/topics.

**Prerequisite warning (outside this repo):** the research agent diffed the private `aiescu/super-ai-skills` repo and found its `NOTICE` says "No source files were copied" while `brainstorming`, `writing-plans`, `verification-before-completion` and others are near-verbatim from `obra/superpowers` (MIT, not listed in NOTICE), and the repo has no LICENSE. Fix that before anything from it is made public. This plan does not depend on it.

---

## The 10 repos (verified 2026-09-04)

| # | Repo | Stars | License | Type | Flagship skill |
|---|---|---:|---|---|---|
| 1 | obra/superpowers | 281,672 | MIT | SDLC methodology framework, 14 skills | `brainstorming` |
| 2 | mattpocock/skills | 249,257 | MIT | Personal engineering collection, 37 skills | `grill-with-docs` |
| 3 | multica-ai/andrej-karpathy-skills | 210,087 | none in repo (README says MIT) | Single skill | `karpathy-guidelines` |
| 4 | anthropics/skills | 173,958 | per-skill (Apache-2.0 / proprietary) | Official collection + spec | `skill-creator` |
| 5 | nextlevelbuilder/ui-ux-pro-max-skill | 124,905 | MIT | Design intelligence + CLI, 7 skills | `ui-ux-pro-max` |
| 6 | JuliusBrussee/caveman | 103,412 | MIT skills / BSL-1.1 engine | Token compression, 20 skills | `caveman` |
| 7 | addyosmani/agent-skills | 92,216 | MIT | Lifecycle collection, 25 skills | `spec-driven-development` |
| 8 | Leonxlnx/taste-skill | 84,252 | MIT | Anti-slop design, 13 skills | `design-taste-frontend` |
| 9 | ComposioHQ/awesome-claude-skills | 74,460 | none in repo (README says Apache-2.0) | Awesome list + vendored monorepo | `connect-apps` |
| 10 | ayghri/i-have-adhd | 27,064 | MIT | Single skill | `i-have-adhd` |

---

## File structure

```
agent-skills/
├── CLAUDE.md                        # exists; Commands section updated in Task 12
├── README.md                        # GENERATED from templates/README.tmpl.md + catalog
├── LICENSE                          # MIT, covers scripts/ install.sh tests/ only
├── LICENSE-CONTENT                  # CC BY 4.0, covers README prose and catalog descriptions
├── SOURCES.md                       # GENERATED attribution table
├── CONTRIBUTING.md                  # inclusion + exclusion criteria
├── CODE_OF_CONDUCT.md
├── package.json                     # scripts only, no deps
├── catalog/
│   ├── skills.json                  # single source of truth (hand-edited)
│   └── stars.json                   # GENERATED by fetch-stars, datestamped
├── templates/README.tmpl.md         # {{TABLE}} {{SECTIONS}} {{UPDATED}} markers
├── scripts/
│   ├── build.mjs                    # catalog -> README, SOURCES, marketplaces, site
│   ├── fetch-stars.mjs              # GitHub API -> catalog/stars.json
│   └── lib/
│       ├── catalog.mjs              # load + validate
│       ├── render.mjs               # pure render functions (tested)
│       └── marketplace.mjs          # pure manifest builder (tested)
├── tests/
│   ├── catalog.test.mjs
│   ├── render.test.mjs
│   ├── marketplace.test.mjs
│   └── install.test.sh
├── install.sh                       # wrapper over `npx skills add` per repo
├── .claude-plugin/marketplace.json  # GENERATED
├── .agents/plugins/marketplace.json # GENERATED (Codex and others)
└── .github/
    ├── ISSUE_TEMPLATE/{propose-repo,attribution}.md
    └── workflows/{ci,refresh-stars}.yml
```

The web page is NOT in this repo: `aiescu-landing` fetches `catalog/skills.json` and `catalog/stars.json` from `raw.githubusercontent.com` (Task 12). Everything user-facing is generated so numbers are never hand-typed (a hard rule in CLAUDE.md). Pure functions live in `scripts/lib/` so they are testable without network.

---

### Task 1: Repo scaffolding and licenses

**Files:**
- Create: `package.json`, `LICENSE`, `LICENSE-CONTENT`, `CODE_OF_CONDUCT.md`, `.gitignore`

- [ ] **Step 1: Create feature branch**

```bash
cd /Users/cristi/agent-skills
git checkout -b feat/showroom-v1
```

- [ ] **Step 2: Write `package.json`**

```json
{
  "name": "@aiescu/agent-skills",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "engines": { "node": ">=20" },
  "scripts": {
    "test": "node --test tests/ && bash tests/install.test.sh",
    "build": "node scripts/build.mjs",
    "build:check": "node scripts/build.mjs --check",
    "stars": "node scripts/fetch-stars.mjs"
  }
}
```

- [ ] **Step 3: Write `LICENSE`**

```
MIT License

Copyright (c) 2026 aiescu

This license covers the code in this repository (scripts/, install.sh, tests/). Catalog descriptions and README prose are licensed separately under
LICENSE-CONTENT (CC BY 4.0). Third-party skills are NOT contained in this
repository; each is linked and remains under its own license (see SOURCES.md).

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 4: Write `LICENSE-CONTENT`**

```
The curated list, catalog descriptions, and README prose in this repository are
licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/

Attribution: "aiescu/agent-skills - https://github.com/aiescu/agent-skills"

This does not cover the third-party skills listed here. They live in their own
repositories under their own licenses. See SOURCES.md.
```

- [ ] **Step 5: Write `CODE_OF_CONDUCT.md`** (Contributor Covenant 2.1)

```bash
curl -fsSL https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md -o CODE_OF_CONDUCT.md
sed -i '' 's/\[INSERT CONTACT METHOD\]/hello@geekbye.com/' CODE_OF_CONDUCT.md
grep -c geekbye CODE_OF_CONDUCT.md   # expected: 1
```

- [ ] **Step 6: Write `.gitignore`**

```
node_modules/
.DS_Store
```

- [ ] **Step 7: Commit**

```bash
git add package.json LICENSE LICENSE-CONTENT CODE_OF_CONDUCT.md .gitignore CLAUDE.md docs/
git commit -m "chore: scaffold repo with split code/content licenses"
```

---

### Task 2: The catalog (single source of truth)

**Files:**
- Create: `catalog/skills.json`, `scripts/lib/catalog.mjs`
- Test: `tests/catalog.test.mjs`

- [ ] **Step 1: Write the failing test**

```js
// tests/catalog.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { loadCatalog, validateEntry } from '../scripts/lib/catalog.mjs';

const base = { repo: 'a/b', author: 'x', authorUrl: 'u', title: 't', summary: 'ok', license: 'MIT', licenseNote: '', type: 'single', skillCount: 1, flagship: 'f', flagshipWhy: 'w', install: { skillsCli: 'a/b' }, whyIncluded: 'w' };

test('catalog has exactly 10 valid, unique entries', () => {
  const c = loadCatalog();
  assert.equal(c.entries.length, 10);
  const repos = c.entries.map(e => e.repo);
  assert.equal(new Set(repos).size, 10);
});

test('validateEntry rejects a promotional summary', () => {
  assert.throws(() => validateEntry({ ...base, summary: 'Try Keebye today!' }), /promotional/);
});

test('validateEntry rejects an entry with no install path', () => {
  assert.throws(() => validateEntry({ ...base, install: {} }), /no install path/);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tests/catalog.test.mjs`
Expected: FAIL with `Cannot find module '../scripts/lib/catalog.mjs'`

- [ ] **Step 3: Write `catalog/skills.json`**

```json
{
  "note": "Hand-edited source of truth. Star counts live in catalog/stars.json (generated). Never type numbers here.",
  "entries": [
    {
      "repo": "obra/superpowers",
      "author": "Jesse Vincent (obra)",
      "authorUrl": "https://github.com/obra",
      "title": "Superpowers",
      "summary": "An opinionated software-development methodology delivered as composable skills: brainstorm, plan, TDD, debug, review, ship. Session hooks make the agent actually use them.",
      "license": "MIT",
      "licenseNote": "",
      "type": "framework",
      "skillCount": 14,
      "flagship": "brainstorming",
      "flagshipWhy": "Forces intent and requirements exploration before any creative work. The entry point to the whole methodology.",
      "install": {
        "skillsCli": "obra/superpowers",
        "claudePlugin": "/plugin install superpowers@claude-plugins-official",
        "codex": "codex plugin marketplace add obra/superpowers-marketplace",
        "gemini": "gemini extensions install https://github.com/obra/superpowers",
        "cursor": "/add-plugin superpowers"
      },
      "whyIncluded": "Most-starred skills repo. Broadest harness support of any entry (13+ agents)."
    },
    {
      "repo": "mattpocock/skills",
      "author": "Matt Pocock",
      "authorUrl": "https://github.com/mattpocock",
      "title": "Skills for Real Engineers",
      "summary": "Small, composable engineering skills straight from Matt's .agents directory. Explicitly against process-owning frameworks.",
      "license": "MIT",
      "licenseNote": "",
      "type": "collection",
      "skillCount": 37,
      "flagship": "grill-with-docs",
      "flagshipWhy": "Interrogates you to close the alignment gap before building, then writes a shared-language CONTEXT.md and ADRs.",
      "install": {
        "skillsCli": "mattpocock/skills",
        "claudePlugin": "claude plugins install mattpocock-skills",
        "note": "Install via ONE path only. The upstream README warns against installing both the plugin and the npx copy."
      },
      "whyIncluded": "Second most-starred. Pushed most recently of the ten."
    },
    {
      "repo": "multica-ai/andrej-karpathy-skills",
      "author": "multica-ai (formerly forrestchang)",
      "authorUrl": "https://github.com/multica-ai",
      "title": "Andrej Karpathy Skills",
      "summary": "A single skill distilled from Karpathy's observations on LLM coding pitfalls: think first, simplicity, surgical changes, goal-driven execution.",
      "license": "Unlicensed (README says MIT)",
      "licenseNote": "No LICENSE file in the repo. We link only.",
      "type": "single",
      "skillCount": 1,
      "flagship": "karpathy-guidelines",
      "flagshipWhy": "Four rules that measurably reduce over-engineering.",
      "install": {
        "skillsCli": "multica-ai/andrej-karpathy-skills",
        "claudePlugin": "/plugin marketplace add multica-ai/andrej-karpathy-skills && /plugin install andrej-karpathy-skills@karpathy-skills",
        "cursor": "Copy .cursor/rules/karpathy-guidelines.mdc from the repo"
      },
      "whyIncluded": "Third most-starred; the canonical behavioral-guidelines skill."
    },
    {
      "repo": "anthropics/skills",
      "author": "Anthropic",
      "authorUrl": "https://github.com/anthropics",
      "title": "Anthropic Agent Skills",
      "summary": "The official reference collection, the Agent Skills spec, and the skill template. Home of skill-creator and mcp-builder.",
      "license": "Per-skill (Apache-2.0 / proprietary)",
      "licenseNote": "docx, pdf, pptx and xlsx are all-rights-reserved and may not be redistributed. We link only; nothing is copied.",
      "type": "official",
      "skillCount": 19,
      "flagship": "skill-creator",
      "flagshipWhy": "Scaffolds and validates new skills. Apache-2.0.",
      "install": {
        "skillsCli": "anthropics/skills",
        "claudePlugin": "/plugin marketplace add anthropics/skills && /plugin install example-skills@anthropic-agent-skills"
      },
      "whyIncluded": "The spec everything else follows."
    },
    {
      "repo": "nextlevelbuilder/ui-ux-pro-max-skill",
      "author": "nextlevelbuilder",
      "authorUrl": "https://github.com/nextlevelbuilder",
      "title": "UI/UX Pro Max",
      "summary": "Design intelligence for building professional UI across platforms: 192 reasoning rules, 79 searchable styles, a design-system generator.",
      "license": "MIT",
      "licenseNote": "Requires Python 3 for its local search script (stdlib only, no network).",
      "type": "collection",
      "skillCount": 7,
      "flagship": "ui-ux-pro-max",
      "flagshipWhy": "The umbrella design skill; design-system is the v2 headline.",
      "install": {
        "skillsCli": "nextlevelbuilder/ui-ux-pro-max-skill",
        "claudePlugin": "/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill && /plugin install ui-ux-pro-max@ui-ux-pro-max-skill",
        "cli": "npm i -g ui-ux-pro-max-cli && uipro init --ai claude"
      },
      "whyIncluded": "Most-starred design skill; its own CLI supports about 20 agents."
    },
    {
      "repo": "JuliusBrussee/caveman",
      "author": "Julius Brussee",
      "authorUrl": "https://github.com/JuliusBrussee",
      "title": "Caveman",
      "summary": "Cuts about 65% of output tokens by making the agent talk like a caveman while keeping technical accuracy. Plus subagent presets and memory-file compression.",
      "license": "MIT (skills) / BSL-1.1 (engine, proxy)",
      "licenseNote": "\"Caveman\" and the rock logo are trademarks of Julius Brussee. The optional CLI sends telemetry by default (DO_NOT_TRACK=1 disables it).",
      "type": "collection",
      "skillCount": 20,
      "flagship": "caveman",
      "flagshipWhy": "The namesake compression mode with lite, full and ultra intensities.",
      "install": {
        "skillsCli": "JuliusBrussee/caveman",
        "claudePlugin": "claude plugin marketplace add JuliusBrussee/caveman && claude plugin install caveman@caveman",
        "gemini": "gemini extensions install https://github.com/JuliusBrussee/caveman"
      },
      "whyIncluded": "The token-efficiency skill everyone else copies."
    },
    {
      "repo": "addyosmani/agent-skills",
      "author": "Addy Osmani",
      "authorUrl": "https://github.com/addyosmani",
      "title": "Agent Skills by Addy Osmani",
      "summary": "Production-grade engineering skills organized as a lifecycle: define, plan, build, verify, review, ship. Includes slash commands and agent personas.",
      "license": "MIT",
      "licenseNote": "Per-skill npx install drops the shared references/ dir (upstream issue #361). Install the whole repo.",
      "type": "collection",
      "skillCount": 25,
      "flagship": "spec-driven-development",
      "flagshipWhy": "Spec before code; the head of the documented lifecycle.",
      "install": {
        "skillsCli": "addyosmani/agent-skills",
        "claudePlugin": "/plugin marketplace add addyosmani/agent-skills && /plugin install agent-skills@addy-agent-skills",
        "codex": "codex plugin marketplace add addyosmani/agent-skills",
        "gemini": "gemini skills install https://github.com/addyosmani/agent-skills"
      },
      "whyIncluded": "The most complete lifecycle collection; clean MIT."
    },
    {
      "repo": "Leonxlnx/taste-skill",
      "author": "Leonxlnx",
      "authorUrl": "https://github.com/Leonxlnx",
      "title": "Taste Skill",
      "summary": "Gives your AI good taste: stops generic frontend slop with brief inference, variance/motion/density dials, and a design-system map.",
      "license": "MIT",
      "licenseNote": "",
      "type": "collection",
      "skillCount": 13,
      "flagship": "design-taste-frontend",
      "flagshipWhy": "The default anti-slop frontend skill (v2).",
      "install": {
        "skillsCli": "Leonxlnx/taste-skill",
        "skillsCliOne": "npx skills@1 add Leonxlnx/taste-skill --skill design-taste-frontend"
      },
      "whyIncluded": "Most-starred single-purpose design-taste skill."
    },
    {
      "repo": "ComposioHQ/awesome-claude-skills",
      "author": "Composio",
      "authorUrl": "https://github.com/ComposioHQ",
      "title": "Awesome Claude Skills",
      "summary": "A curated awesome-list of about 180 skills plus 800+ app-automation skills for Composio's MCP gateway.",
      "license": "Unlicensed (README says Apache-2.0)",
      "licenseNote": "No LICENSE file. Contains vendored copies of Anthropic's restricted document skills. We link only.",
      "type": "list",
      "skillCount": 865,
      "flagship": "connect-apps",
      "flagshipWhy": "Lets the agent take real actions across 1000+ apps via Composio.",
      "install": {
        "claudePlugin": "git clone https://github.com/ComposioHQ/awesome-claude-skills && claude --plugin-dir ./awesome-claude-skills/connect-apps-plugin"
      },
      "whyIncluded": "The largest discovery list in the ecosystem."
    },
    {
      "repo": "ayghri/i-have-adhd",
      "author": "ayghri",
      "authorUrl": "https://github.com/ayghri",
      "title": "I Have ADHD",
      "summary": "Ten output rules that stop the agent burying the answer: lead with the next action, number steps, cap lists at five, no preamble.",
      "license": "MIT",
      "licenseNote": "",
      "type": "single",
      "skillCount": 1,
      "flagship": "i-have-adhd",
      "flagshipWhy": "The only skill here about the shape of answers, and it helps everyone, not only ADHD users.",
      "install": {
        "skillsCli": "ayghri/i-have-adhd",
        "claudePlugin": "claude plugin marketplace add ayghri/i-have-adhd && claude plugin install i-have-adhd@i-have-adhd"
      },
      "whyIncluded": "Fastest-growing single skill of 2026; packaged for seven harnesses."
    }
  ]
}
```

- [ ] **Step 4: Write `scripts/lib/catalog.mjs`**

```js
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
```

- [ ] **Step 5: Run tests**

Run: `node --test tests/catalog.test.mjs`
Expected: 3 passing

- [ ] **Step 6: Commit**

```bash
git add catalog/skills.json scripts/lib/catalog.mjs tests/catalog.test.mjs
git commit -m "feat: add catalog of 10 skill repos with validation"
```

---

### Task 3: Star fetcher (datestamped, never hand-typed)

**Files:**
- Create: `scripts/fetch-stars.mjs`
- Generates: `catalog/stars.json`

- [ ] **Step 1: Write the script**

```js
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
```

- [ ] **Step 2: Run it**

Run: `env -u GH_TOKEN -u GITHUB_TOKEN node scripts/fetch-stars.mjs`
Expected: 10 lines of `owner/repo: N`, then `wrote .../catalog/stars.json`. `cat catalog/stars.json` shows `"fetchedAt": "2026-09-04"`.

- [ ] **Step 3: Commit**

```bash
git add scripts/fetch-stars.mjs catalog/stars.json
git commit -m "feat: fetch datestamped star counts from GitHub API"
```

---

### Task 4: Render functions

**Files:**
- Create: `scripts/lib/render.mjs`
- Test: `tests/render.test.mjs`

- [ ] **Step 1: Write the failing tests**

```js
// tests/render.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fmtStars, renderTable, renderSection, renderSources } from '../scripts/lib/render.mjs';

const e = {
  repo: 'obra/superpowers', author: 'Jesse Vincent (obra)', authorUrl: 'https://github.com/obra',
  title: 'Superpowers', summary: 'Methodology. More.', license: 'MIT', licenseNote: '', type: 'framework',
  skillCount: 14, flagship: 'brainstorming', flagshipWhy: 'Entry point.',
  install: { skillsCli: 'obra/superpowers', claudePlugin: '/plugin install superpowers@claude-plugins-official' },
  whyIncluded: 'Most-starred.'
};
const stars = { fetchedAt: '2026-09-04', stars: { 'obra/superpowers': { stars: 281672 } } };

test('fmtStars', () => {
  assert.equal(fmtStars(281672), '281.7k');
  assert.equal(fmtStars(950), '950');
  assert.equal(fmtStars(undefined), 'n/a');
});

test('table sorts by stars desc and links upstream', () => {
  const low = { ...e, repo: 'x/y', title: 'Y' };
  const s = { ...stars, stars: { ...stars.stars, 'x/y': { stars: 10 } } };
  const out = renderTable([low, e], s);
  assert.ok(out.indexOf('obra/superpowers') < out.indexOf('x/y'));
  assert.match(out, /\[obra\/superpowers\]\(https:\/\/github\.com\/obra\/superpowers\)/);
  assert.match(out, /281\.7k/);
});

test('section includes install commands, flagship and license', () => {
  const out = renderSection(e, stars);
  assert.match(out, /npx skills@1 add obra\/superpowers/);
  assert.match(out, /\/plugin install superpowers@claude-plugins-official/);
  assert.match(out, /MIT/);
  assert.match(out, /\*\*Flagship skill:\*\* `brainstorming`/);
});

test('sources table has one row per entry', () => {
  const out = renderSources([e, { ...e, repo: 'x/y' }]);
  assert.equal(out.split('\n').filter(l => l.startsWith('| [')).length, 2);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tests/render.test.mjs`
Expected: FAIL, module not found

- [ ] **Step 3: Write `scripts/lib/render.mjs`**

```js
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
```

- [ ] **Step 4: Run tests**

Run: `node --test tests/render.test.mjs`
Expected: 4 passing

- [ ] **Step 5: Commit**

```bash
git add scripts/lib/render.mjs tests/render.test.mjs
git commit -m "feat: pure render functions for README table, sections, sources"
```

---

### Task 5: Marketplace manifests (link-first, nothing vendored)

**Files:**
- Create: `scripts/lib/marketplace.mjs`
- Test: `tests/marketplace.test.mjs`

- [ ] **Step 1: Write the failing test**

```js
// tests/marketplace.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildMarketplace } from '../scripts/lib/marketplace.mjs';

const e = { repo: 'obra/superpowers', author: 'Jesse Vincent (obra)', authorUrl: 'https://github.com/obra', title: 'Superpowers', summary: 'S.', license: 'MIT', install: { claudePlugin: 'x' } };
const noPlugin = { ...e, repo: 'Leonxlnx/taste-skill', install: { skillsCli: 'Leonxlnx/taste-skill' } };

test('every plugin points at the upstream git URL and credits the original author', () => {
  const m = buildMarketplace([e]);
  assert.equal(m.name, 'aiescu-agent-skills');
  assert.equal(m.plugins.length, 1);
  const p = m.plugins[0];
  assert.equal(p.name, 'superpowers');
  assert.equal(p.source.source, 'url');
  assert.equal(p.source.url, 'https://github.com/obra/superpowers.git');
  assert.match(p.author.name, /^Jesse Vincent \(obra\) \(original\)/);
  assert.equal(p.author.url, 'https://github.com/obra');
  assert.equal(p.homepage, 'https://github.com/obra/superpowers');
});

test('entries without a plugin manifest are excluded', () => {
  assert.equal(buildMarketplace([e, noPlugin]).plugins.length, 1);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tests/marketplace.test.mjs`
Expected: FAIL, module not found

- [ ] **Step 3: Write `scripts/lib/marketplace.mjs`**

```js
// Builds a Claude Code / Codex plugin marketplace that references upstream repos by URL.
// Nothing is vendored. The author field credits the ORIGINAL author; crediting the
// curator here is what got ultimate-skills called out (issue #10).
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
        version: 'latest',
        author: { name: `${e.author} (original), curated by aiescu`, url: e.authorUrl },
        homepage: `https://github.com/${e.repo}`,
        license: e.license,
        source: { source: 'url', url: `https://github.com/${e.repo}.git` }
      }))
  };
}
```

- [ ] **Step 4: Run tests**

Run: `node --test tests/marketplace.test.mjs`
Expected: 2 passing

- [ ] **Step 5: Commit**

```bash
git add scripts/lib/marketplace.mjs tests/marketplace.test.mjs
git commit -m "feat: build link-first plugin marketplace manifest"
```

---

### Task 6: README template and build script

**Files:**
- Create: `templates/README.tmpl.md`, `scripts/build.mjs`
- Generates: `README.md`, `SOURCES.md`, `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`

- [ ] **Step 1: Write `templates/README.tmpl.md`**

````markdown
# Agent Skills: the 10 most popular skill repos, one install away

[![Stars refreshed](https://img.shields.io/badge/stars_refreshed-{{UPDATED}}-blue)](catalog/stars.json)
[![CI](https://github.com/aiescu/agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/aiescu/agent-skills/actions/workflows/ci.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC_BY_4.0-lightgrey.svg)](LICENSE-CONTENT)

A curated showroom of the most-starred **agent skills** (SKILL.md instruction packs) for
Claude Code, Codex, Gemini CLI, Cursor, Copilot, OpenCode and 70+ other agents, with a
one-command install for each.

Web version of this list: [aiescu.com/agent-skills](https://aiescu.com/agent-skills?utm_source=github&utm_medium=readme&utm_campaign=agent-skills).

**Nothing here is copied.** Every skill installs straight from its original repository, keeps
its original license, and credits its original author. This repo is the map, not the territory.

<sub>Maintained by <a href="https://github.com/aiescu">aiescu</a>. Star counts are fetched weekly from the GitHub API, never typed by hand.</sub>

## Quick start

```bash
# Everything, into the agent of your choice (interactive picker)
curl -fsSL https://raw.githubusercontent.com/aiescu/agent-skills/main/install.sh | bash -s -- --agent claude-code

# One repo, any agent, via the skills CLI
npx skills@1 add obra/superpowers

# As a Claude Code plugin marketplace (installs from upstream, nothing vendored)
/plugin marketplace add aiescu/agent-skills
```

## The list

Sorted by stars as of {{UPDATED}}.

{{TABLE}}

## Each repo

{{SECTIONS}}

## How repos get on this list

**Included if:** it ships SKILL.md-style skills, is publicly installable, and is among the
most-starred in its category. Every entry has been installed and used by a maintainer.

**Excluded if:** it has no license *and* no plugin or CLI install path (we won't tell you to copy
files nobody licensed), or it is primarily a vendored copy of someone else's work.

Propose a repo via [CONTRIBUTING.md](CONTRIBUTING.md). Recognize your work and think the credit is
wrong? [Open an issue](https://github.com/aiescu/agent-skills/issues/new?template=attribution.md).
It gets fixed first.

## Where skills go

| Agent | Skills directory | Install |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `npx skills@1 add <repo> -a claude-code` or `/plugin marketplace add` |
| Codex | `.agents/skills/` | `npx skills@1 add <repo> -a codex` |
| Gemini CLI | `~/.gemini/skills/` | `npx skills@1 add <repo> -a gemini-cli` |
| Cursor | `.cursor/skills/` | `npx skills@1 add <repo> -a cursor` |
| Copilot, OpenCode, Windsurf, Antigravity, 70+ more | see [vercel-labs/skills](https://github.com/vercel-labs/skills) | `npx skills@1 add <repo> -a <agent>` |

## Attribution

Per-repo attribution and license notes are in [SOURCES.md](SOURCES.md). Code in this repo is MIT;
the list and descriptions are CC BY 4.0. The skills themselves belong to their authors.

---

<sub>Built by <a href="https://github.com/aiescu">aiescu</a>, makers of
<a href="https://keebye.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills">Keebye</a>
(local push-to-talk dictation for people who drive coding agents from the terminal),
<a href="https://pavleur.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills">Pavleur</a>
(AI meeting copilot) and
<a href="https://geekbye.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills">GeekBye</a>
(real-time interview assistant).</sub>
````

- [ ] **Step 2: Write `scripts/build.mjs`**

```js
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
```

- [ ] **Step 3: Build and inspect**

Run: `npm run build && npm run build:check`
Expected: four `wrote ...` lines, then `up to date`. Open `README.md`: the table is sorted by stars with superpowers first, every section has an install block, the footer is the only place product names appear.

- [ ] **Step 4: Run all node tests**

Run: `node --test tests/`
Expected: 9 passing

- [ ] **Step 5: Commit**

```bash
git add templates scripts/build.mjs README.md SOURCES.md .claude-plugin .agents
git commit -m "feat: generate README, SOURCES and marketplaces from catalog"
```

---

### Task 7: Installer

**Files:**
- Create: `install.sh`
- Test: `tests/install.test.sh`

The installer wraps `npx skills@1` (pinned major, telemetry off). Because the curl-pipe path cannot read the catalog, the repo list is baked in; the test enforces it matches the catalog's `skillsCli` entries.

- [ ] **Step 1: Write the failing test**

```bash
#!/usr/bin/env bash
# tests/install.test.sh: installer contract tests, no network
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }

expected=$(node -e "console.log(JSON.parse(require('fs').readFileSync('catalog/skills.json','utf8')).entries.filter(e=>e.install.skillsCli).map(e=>e.install.skillsCli).sort().join('\n'))")
actual=$(bash install.sh --list | sort)
[ "$expected" = "$actual" ] || fail "install.sh --list differs from catalog"

count=$(printf '%s\n' "$expected" | wc -l | tr -d ' ')
out=$(bash install.sh --agent claude-code --dry-run)
n=$(printf '%s\n' "$out" | grep -c 'npx skills@1 add ' || true)
[ "$n" = "$count" ] || fail "expected $count npx lines, got $n"
printf '%s\n' "$out" | grep -q -- '-a claude-code' || fail "agent flag missing"
printf '%s\n' "$out" | grep -q 'DISABLE_TELEMETRY=1' || fail "telemetry not disabled"

if bash install.sh --agent nope --dry-run >/dev/null 2>&1; then fail "unknown agent accepted"; fi

out=$(bash install.sh --agent codex --only obra/superpowers --dry-run)
[ "$(printf '%s\n' "$out" | grep -c 'npx skills@1 add ')" = "1" ] || fail "--only did not limit"

echo "install.test.sh: OK"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `bash tests/install.test.sh`
Expected: FAIL (install.sh: No such file)

- [ ] **Step 3: Write `install.sh`**

```bash
#!/usr/bin/env bash
# aiescu/agent-skills installer
# Installs the most popular agent skill repos into the agent of your choice by
# delegating to the `skills` CLI (github.com/vercel-labs/skills, MIT).
# Nothing is downloaded from aiescu; every skill comes from its original repo.
#
# Usage:
#   install.sh [--agent <name>] [--only <owner/repo>] [--global] [--dry-run] [--list]
#   curl -fsSL https://raw.githubusercontent.com/aiescu/agent-skills/main/install.sh | bash -s -- --agent claude-code
set -euo pipefail

# Keep in sync with catalog/skills.json entries that have install.skillsCli
# (tests/install.test.sh enforces this).
REPOS=(
  "obra/superpowers"
  "mattpocock/skills"
  "multica-ai/andrej-karpathy-skills"
  "anthropics/skills"
  "nextlevelbuilder/ui-ux-pro-max-skill"
  "JuliusBrussee/caveman"
  "addyosmani/agent-skills"
  "Leonxlnx/taste-skill"
  "ayghri/i-have-adhd"
)
AGENTS=(claude-code codex gemini-cli cursor copilot opencode windsurf antigravity kiro amp)
SKILLS_CLI="npx skills@1"

agent="" only="" scope="" dry=0
while [ $# -gt 0 ]; do
  case "$1" in
    --agent) agent="$2"; shift 2 ;;
    --only) only="$2"; shift 2 ;;
    --global) scope="-g"; shift ;;
    --dry-run) dry=1; shift ;;
    --list) printf '%s\n' "${REPOS[@]}"; exit 0 ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
done

if [ -z "$agent" ]; then
  if [ -t 0 ]; then
    echo "Which agent?"
    select a in "${AGENTS[@]}"; do agent="$a"; break; done
  else
    echo "error: --agent <name> is required when not interactive. One of: ${AGENTS[*]}" >&2
    exit 2
  fi
fi
case " ${AGENTS[*]} " in
  *" $agent "*) ;;
  *) echo "error: unknown agent '$agent'. One of: ${AGENTS[*]}" >&2; exit 2 ;;
esac

if [ "$dry" = 0 ] && ! command -v npx >/dev/null; then
  echo "error: npx (Node 20+) is required" >&2; exit 1
fi

for repo in "${REPOS[@]}"; do
  if [ -n "$only" ] && [ "$only" != "$repo" ]; then continue; fi
  echo "DISABLE_TELEMETRY=1 $SKILLS_CLI add $repo -a $agent $scope -y"
  if [ "$dry" = 0 ]; then
    # shellcheck disable=SC2086
    DISABLE_TELEMETRY=1 $SKILLS_CLI add "$repo" -a "$agent" $scope -y
  fi
done

echo
echo "Done. Skills installed for $agent from their original repositories."
echo "Attribution and licenses: https://github.com/aiescu/agent-skills/blob/main/SOURCES.md"
```

`ComposioHQ/awesome-claude-skills` is absent from `REPOS` on purpose: its catalog entry has no `skillsCli`, so the test's filter matches.

- [ ] **Step 4: Run test**

Run: `chmod +x install.sh && bash tests/install.test.sh`
Expected: `install.test.sh: OK`

- [ ] **Step 5: Smoke test one real install in the scratchpad**

```bash
S=/private/tmp/claude-501/-Users-cristi-agent-skills/175edd75-a7ec-4ac8-ba24-9143412e3714/scratchpad/smoke
mkdir -p "$S" && cd "$S" && bash /Users/cristi/agent-skills/install.sh --agent claude-code --only ayghri/i-have-adhd
find . -name SKILL.md
```
Expected: a `SKILL.md` under `.claude/skills/i-have-adhd/`. If the `skills` CLI flags differ from `-a/-g/-y`, read `npx skills@1 add --help` and fix `install.sh` and the test together.

- [ ] **Step 6: Commit**

```bash
cd /Users/cristi/agent-skills
git add install.sh tests/install.test.sh
git commit -m "feat: add multi-agent installer wrapping the skills CLI"
```

---

### Task 8: CONTRIBUTING and issue templates

**Files:**
- Create: `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/propose-repo.md`, `.github/ISSUE_TEMPLATE/attribution.md`

- [ ] **Step 1: Write `CONTRIBUTING.md`**

````markdown
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
````

- [ ] **Step 2: Write `.github/ISSUE_TEMPLATE/propose-repo.md`**

```markdown
---
name: Propose a repo
about: Suggest a skill repo for the list
labels: proposal
---
**Repo URL:**
**Stars today:**
**License file present?** yes / no
**Install path (npx skills / plugin / CLI):**
**What it did for you when you used it:**
**Which current entry should it replace, and why?**
```

- [ ] **Step 3: Write `.github/ISSUE_TEMPLATE/attribution.md`**

```markdown
---
name: Attribution
about: The credit, license, or description of your work is wrong
labels: attribution, priority
---
**Entry:**
**What is wrong:**
**What it should say:**
```

- [ ] **Step 4: Commit**

```bash
git add CONTRIBUTING.md .github/ISSUE_TEMPLATE
git commit -m "docs: contributing guide with inclusion criteria and attribution path"
```

---

### Task 9: CI and weekly star refresh

**Files:**
- Create: `.github/workflows/ci.yml`, `.github/workflows/refresh-stars.yml`

- [ ] **Step 1: Write `.github/workflows/ci.yml`**

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm test
      - run: npm run build:check
      - run: shellcheck install.sh tests/install.test.sh
      - uses: lycheeverse/lychee-action@v2
        with:
          args: --no-progress README.md SOURCES.md
          fail: true
```

- [ ] **Step 2: Write `.github/workflows/refresh-stars.yml`**

```yaml
name: Refresh stars
on:
  schedule: [{ cron: '0 6 * * 1' }]
  workflow_dispatch:
permissions: { contents: write, pull-requests: write }
jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm run stars && npm run build
        env: { GITHUB_TOKEN: "${{ secrets.GITHUB_TOKEN }}" }
      - uses: peter-evans/create-pull-request@v6
        with:
          branch: chore/refresh-stars
          title: "chore: refresh star counts"
          commit-message: "chore: refresh star counts"
          body: "Automated weekly refresh from the GitHub API."
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows
git commit -m "ci: tests, stale-output check, link check, weekly star refresh"
```

---

### Task 10: Open the PR and validate the marketplace

- [ ] **Step 1: Pre-PR checks**

```bash
npm test && npm run build:check && git diff --check && git status -sb
```
Expected: all pass, tree clean.

- [ ] **Step 2: Push and open PR** (invoke the `pr-preparation` skill; base is `main`)

```bash
git push -u origin feat/showroom-v1
env -u GH_TOKEN -u GITHUB_TOKEN gh pr create --base main \
  --title "Showroom v1: catalog, generated README, installer, marketplace" \
  --body-file - <<'PRBODY'
Link-first showroom of the 10 most-starred agent skill repos.

- catalog/skills.json is the single source of truth; README, SOURCES, marketplaces and site are generated
- star counts fetched from the GitHub API and datestamped; CI rejects stale output
- install.sh wraps the skills CLI for 10 agents; nothing is vendored
- .claude-plugin/marketplace.json and .agents/plugins/marketplace.json point at upstream by URL

Every entry credits its original author and license. See SOURCES.md.
PRBODY
```

- [ ] **Step 3: Watch CI**

Run: `env -u GH_TOKEN -u GITHUB_TOKEN gh pr checks --watch`
Expected: all green. If lychee flags a URL, fix the catalog, rebuild, push.

- [ ] **Step 4: Validate the marketplace in Claude Code** (after merge, from main)

```
/plugin marketplace add aiescu/agent-skills
/plugin install superpowers@aiescu-agent-skills
```
Expected: install succeeds and the plugin author reads `Jesse Vincent (obra) (original), curated by aiescu`.

- [ ] **Step 5: Merge is the user's call.** Then `git checkout main && git pull`.

---

### Task 11: Repo settings and discoverability (no code)

- [ ] **Step 1: Set description, homepage, topics**

```bash
env -u GH_TOKEN -u GITHUB_TOKEN gh repo edit aiescu/agent-skills \
  --description "The 10 most popular agent skills for Claude Code, Codex, Cursor and Gemini CLI, with one-command install. Link-first: every skill installs from its original repo." \
  --homepage "https://aiescu.com/agent-skills" \
  --enable-discussions \
  --add-topic agent-skills --add-topic claude-code --add-topic codex --add-topic cursor \
  --add-topic gemini-cli --add-topic ai-agents --add-topic skills --add-topic claude \
  --add-topic awesome-list --add-topic developer-tools --add-topic llm --add-topic coding-agents \
  --add-topic openai-codex --add-topic github-copilot --add-topic opencode --add-topic antigravity \
  --add-topic prompt-engineering --add-topic mcp
```

---

### Task 12: `aiescu.com/agent-skills` landing page (in `aiescu/aiescu-landing`)

This is the SEO surface. It lives in the ecosystem hub repo, follows the existing `free-tools` page
pattern, and reads the catalog from `aiescu/agent-skills` on `main` at build time. Do this only after
Task 10 is merged, otherwise the fetch 404s.

**Files (in a fresh worktree of `aiescu/aiescu-landing`, branch `feat/agent-skills-page`):**
- Create: `src/lib/marketing/agent-skills.ts`, `src/lib/marketing/agent-skills.test.ts`
- Create: `src/app/[locale]/agent-skills/page.tsx`
- Modify: `src/lib/marketing/og-config.ts` (add `"agent-skills"` to the `OgSlug` union and its title entry, following the existing entries)
- Modify: `src/app/sitemap.ts` (`pages` array)
- Modify: `src/app/llms.txt/route.ts` (Pages list)

- [ ] **Step 1: Read the neighbours first**

```bash
sed -n '1,80p' src/app/[locale]/free-tools/page.tsx
sed -n '1,40p' src/lib/marketing/free-tools.ts
grep -n "OgSlug\|free-tools" src/lib/marketing/og-config.ts
```

- [ ] **Step 2: Write the failing test**

```ts
// src/lib/marketing/agent-skills.test.ts
import { describe, it, expect } from "vitest";
import { mergeCatalog, fmtStars } from "./agent-skills";

const catalog = { entries: [
  { repo: "obra/superpowers", author: "Jesse Vincent (obra)", authorUrl: "https://github.com/obra", title: "Superpowers", summary: "S.", license: "MIT", licenseNote: "", type: "framework", skillCount: 14, flagship: "brainstorming", flagshipWhy: "W.", install: { skillsCli: "obra/superpowers" }, whyIncluded: "Y." },
  { repo: "x/y", author: "x", authorUrl: "https://github.com/x", title: "Y", summary: "S.", license: "MIT", licenseNote: "", type: "single", skillCount: 1, flagship: "f", flagshipWhy: "W.", install: { skillsCli: "x/y" }, whyIncluded: "Y." },
] };
const stars = { fetchedAt: "2026-09-04", stars: { "obra/superpowers": { stars: 281672 }, "x/y": { stars: 10 } } };

describe("agent-skills", () => {
  it("merges stars and sorts descending", () => {
    const rows = mergeCatalog(catalog, stars);
    expect(rows[0].repo).toBe("obra/superpowers");
    expect(rows[0].stars).toBe(281672);
    expect(rows[1].stars).toBe(10);
  });
  it("formats stars", () => {
    expect(fmtStars(281672)).toBe("281.7k");
    expect(fmtStars(undefined)).toBe("n/a");
  });
});
```

- [ ] **Step 3: Run test to verify it fails**

Run: `npx vitest run src/lib/marketing/agent-skills.test.ts`
Expected: FAIL, cannot resolve `./agent-skills`

- [ ] **Step 4: Write `src/lib/marketing/agent-skills.ts`**

```ts
// Reads the public catalog from aiescu/agent-skills at build time. The GitHub
// repo is the source of truth; this page never hand-types a star count.
const RAW = "https://raw.githubusercontent.com/aiescu/agent-skills/main/catalog";
export const REPO_URL = "https://github.com/aiescu/agent-skills";

export interface SkillEntry {
  repo: string; author: string; authorUrl: string; title: string; summary: string;
  license: string; licenseNote: string; type: string; skillCount: number;
  flagship: string; flagshipWhy: string;
  install: { skillsCli?: string; claudePlugin?: string; codex?: string; gemini?: string; cursor?: string; cli?: string; note?: string };
  whyIncluded: string;
}
export interface Catalog { entries: SkillEntry[] }
export interface Stars { fetchedAt: string | null; stars: Record<string, { stars: number }> }
export type SkillRow = SkillEntry & { stars?: number };

export function fmtStars(n?: number): string {
  if (n == null) return "n/a";
  return n >= 1000 ? `${(n / 1000).toFixed(1)}k` : String(n);
}

export function mergeCatalog(catalog: Catalog, stars: Stars): SkillRow[] {
  return catalog.entries
    .map((e) => ({ ...e, stars: stars.stars[e.repo]?.stars }))
    .sort((a, b) => (b.stars ?? -1) - (a.stars ?? -1));
}

export async function loadAgentSkills(): Promise<{ rows: SkillRow[]; fetchedAt: string | null }> {
  const opts = { next: { revalidate: 60 * 60 * 24 } }; // daily ISR; the repo refreshes weekly
  const [c, s] = await Promise.all([
    fetch(`${RAW}/skills.json`, opts).then((r) => r.json() as Promise<Catalog>),
    fetch(`${RAW}/stars.json`, opts).then((r) => r.json() as Promise<Stars>),
  ]);
  return { rows: mergeCatalog(c, s), fetchedAt: s.fetchedAt };
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `npx vitest run src/lib/marketing/agent-skills.test.ts`
Expected: 2 passing

- [ ] **Step 6: Add the OG slug**

In `src/lib/marketing/og-config.ts`, add `"agent-skills"` to the `OgSlug` union and an entry with title `"The 10 most popular agent skills"` and subtitle `"One install for Claude Code, Codex, Cursor, Gemini CLI"`, matching the shape of the `free-tools` entry. Run `npm run typecheck` and fix any place the union is exhaustively matched.

- [ ] **Step 7: Write `src/app/[locale]/agent-skills/page.tsx`**

```tsx
import type { Metadata } from "next";
import { MarketingShell } from "@/components/marketing/MarketingShell";
import { fmtStars, loadAgentSkills, REPO_URL, type SkillRow } from "@/lib/marketing/agent-skills";
import { pageMetadata, SITE_URL } from "@/lib/marketing/seo";

export const revalidate = 86400;

export const metadata: Metadata = pageMetadata({
  title: "The 10 Most Popular Agent Skills for Claude Code, Codex, Cursor & Gemini — AIESCU",
  description:
    "Curated, link-first list of the most-starred agent skills (SKILL.md) with one-command install for 70+ AI coding agents. Nothing copied; every skill installs from its original repo.",
  path: "/agent-skills",
  ogSlug: "agent-skills",
});

function itemListLd(rows: SkillRow[]) {
  return {
    "@context": "https://schema.org",
    "@type": "ItemList" as const,
    "@id": `${SITE_URL}/agent-skills#itemlist`,
    url: `${SITE_URL}/agent-skills`,
    name: "Most popular agent skills",
    itemListElement: rows.map((r, i) => ({ "@type": "ListItem", position: i + 1, url: `https://github.com/${r.repo}`, name: r.title })),
  };
}

function SkillCard({ r, rank }: { r: SkillRow; rank: number }) {
  return (
    <article
      className="rounded-xl border p-6"
      style={{ background: "var(--color-marketing-bg-elev)", borderColor: "var(--color-marketing-border)" }}
    >
      <p className="eyebrow">#{rank} · ★ {fmtStars(r.stars)} · {r.skillCount} skill{r.skillCount === 1 ? "" : "s"} · {r.license}</p>
      <h3 className="mt-2 text-lg font-semibold text-[color:var(--color-text)]">
        <a href={`https://github.com/${r.repo}`} rel="noopener">{r.title}</a>{" "}
        <span className="text-sm font-normal text-[color:var(--color-text-muted)]">by <a href={r.authorUrl} rel="noopener">{r.author}</a></span>
      </h3>
      <p className="mt-2 text-sm leading-relaxed text-[color:var(--color-text-muted)]">{r.summary}</p>
      <p className="mt-2 text-sm text-[color:var(--color-text)]"><strong>Flagship skill:</strong> <code>{r.flagship}</code>. {r.flagshipWhy}</p>
      {r.install.skillsCli && (
        <pre className="mt-3 overflow-x-auto rounded-lg p-3 text-xs"><code>npx skills@1 add {r.install.skillsCli}</code></pre>
      )}
      {r.licenseNote && <p className="mt-2 text-xs text-[color:var(--color-text-muted)]">License note: {r.licenseNote}</p>}
    </article>
  );
}

export default async function AgentSkillsPage() {
  const { rows, fetchedAt } = await loadAgentSkills();
  return (
    <MarketingShell>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(itemListLd(rows)) }} />
      <div className="mx-auto w-full max-w-6xl px-6 py-16 md:py-24">
        <header className="mb-12">
          <p className="eyebrow">Agent skills</p>
          <h1 className="text-claim mt-4 text-[color:var(--color-text)]">The 10 most popular agent skills, one install away</h1>
          <p className="mt-4 max-w-2xl text-[color:var(--color-text-muted)]">
            The most-starred SKILL.md packs for Claude Code, Codex, Gemini CLI, Cursor and 70+ other coding agents.
            Nothing is copied: every skill installs from its original repository and keeps its author and license.
            Stars as of {fetchedAt ?? "today"}, refreshed from the GitHub API.
          </p>
          <pre className="mt-6 overflow-x-auto rounded-lg p-4 text-sm"><code>curl -fsSL https://raw.githubusercontent.com/aiescu/agent-skills/main/install.sh | bash -s -- --agent claude-code</code></pre>
          <p className="mt-3 text-sm">
            <a href={REPO_URL} rel="noopener">Installer, marketplace and sources on GitHub →</a>
          </p>
        </header>

        <div className="grid gap-6 md:grid-cols-2">
          {rows.map((r, i) => <SkillCard key={r.repo} r={r} rank={i + 1} />)}
        </div>

        <section className="mt-16 max-w-2xl">
          <h2 className="text-lg font-semibold text-[color:var(--color-text)]">How repos get on this list</h2>
          <p className="mt-2 text-sm text-[color:var(--color-text-muted)]">
            Included: ships SKILL.md-style skills, publicly installable, among the most-starred in its category, and
            used by us at least once. Excluded: no license and no install path, or primarily a vendored copy of someone
            else's work. Propose a repo or fix an attribution in the <a href={`${REPO_URL}/issues`} rel="noopener">GitHub issues</a>.
          </p>
        </section>

        <section className="mt-16 max-w-2xl">
          <h2 className="text-lg font-semibold text-[color:var(--color-text)]">Built by the makers of</h2>
          <ul className="mt-2 space-y-1 text-sm text-[color:var(--color-text-muted)]">
            <li><a href="https://keebye.com?utm_source=aiescu&utm_medium=agent-skills">Keebye</a>: local push-to-talk dictation for people who drive coding agents from the terminal.</li>
            <li><a href="https://pavleur.com?utm_source=aiescu&utm_medium=agent-skills">Pavleur</a>: AI meeting copilot for Mac, 40+ languages.</li>
            <li><a href="https://geekbye.com?utm_source=aiescu&utm_medium=agent-skills">GeekBye</a>: real-time interview assistant.</li>
          </ul>
        </section>
      </div>
    </MarketingShell>
  );
}
```

- [ ] **Step 8: Register in sitemap and llms.txt**

In `src/app/sitemap.ts`, add to the `pages` array:
```ts
  { path: "/agent-skills", priority: 0.8, changeFrequency: "weekly" },
```
In `src/app/llms.txt/route.ts`, add after the Free tools line:
```ts
    `- [Agent skills](${SITE_URL}/agent-skills): the 10 most popular agent skills, one install away`,
```

- [ ] **Step 9: Verify**

Run: `npm run verify && npm test`
Expected: lint, typecheck, build pass; vitest passes including the existing `sitemap.test.ts`. If `sitemap.test.ts` asserts an exact page list, add `/agent-skills` there.

Run: `npm run dev` then open `http://localhost:3000/agent-skills`. Expected: 10 cards sorted by stars, superpowers first, product links only in the last section.

- [ ] **Step 10: Commit and PR** (base per the landing repo's own CLAUDE.md; follow `pr-preparation`)

```bash
git add src/lib/marketing/agent-skills.ts src/lib/marketing/agent-skills.test.ts src/app/[locale]/agent-skills/page.tsx src/lib/marketing/og-config.ts src/app/sitemap.ts src/app/llms.txt/route.ts
git commit -m "feat: add /agent-skills page reading the public catalog"
```

---

### Task 13: CLAUDE.md update

**Files:**
- Modify: `CLAUDE.md` Commands section

- [ ] **Step 1: Replace the Commands section of `CLAUDE.md`** with:

````markdown
## Commands

```bash
npm test              # node:test suites + installer contract test
npm run stars         # refresh catalog/stars.json from GitHub API (needs gh or GITHUB_TOKEN)
npm run build         # regenerate README.md, SOURCES.md, marketplaces
npm run build:check   # CI gate: fail if generated files are stale
bash install.sh --agent claude-code --dry-run
node --test tests/render.test.mjs   # single test file
```

## Architecture

`catalog/skills.json` is the only hand-edited content. `scripts/build.mjs` renders it through pure
functions in `scripts/lib/` into every user-facing file. `install.sh` carries a baked-in copy of the
repo list for the curl-pipe path; `tests/install.test.sh` fails if it drifts from the catalog.
````

- [ ] **Step 2: Branch, commit, PR** (`chore/docs`, same flow as Task 10).

---

### Task 14: Launch checklist (user-driven, no code)

- [ ] Let the repo age a few days and collect a handful of organic stars from the team's own networks. Never buy or trade stars.
- [ ] Post to Hacker News on a weekday between 12:00 and 17:00 UTC. Plain post, not "Show HN". Suggested title: "The 10 most popular agent skills, one install away (link-first, nothing copied)".
- [ ] Same day: r/ClaudeAI, r/ChatGPTCoding, Console.dev, and a post from the Keebye account on X.
- [ ] Message each of the 10 authors: "You're #N on our list, install points at your repo, credit and license are in SOURCES.md, shout if anything's wrong." This turns potential complainants into amplifiers.
- [ ] Open PRs adding a "Curated marketplaces" entry to `sickn33/agentic-awesome-skills` and `ComposioHQ/awesome-claude-skills`. Do not touch `hesreallyhim/awesome-claude-code` (CC BY-NC-ND, anti-aggregator).
- [ ] Track GitHub Insights → Traffic, plus the existing Vercel Analytics on aiescu.com plus the UTM tags on product links.

---

## Self-review

- **Spec coverage:** 10 repos analyzed and listed (Task 2); nice README (Task 6); credit not copy (Tasks 2, 5, 6, 8: link-first, SOURCES.md, original-author manifests, attribution issue template); installer for popular agents (Task 7 plus marketplaces in Task 5); CLAUDE.md (exists, finalized in Task 12); "not being cancelled" (research summary, license split, no vendoring, no star gaming); SEO (Task 11 description and topics, Task 12 aiescu.com page, Task 14 launch).
- **Placeholder scan:** none; every code step has full content.
- **Type consistency:** `fmtStars`, `renderTable`, `renderSection`, `renderSources`, `sortByStars` used in `build.mjs` match `render.mjs` exports. `loadCatalog`, `loadStars`, `STARS_PATH` match `catalog.mjs`. `buildMarketplace(entries)` is consistent. Installer `REPOS` has 9 entries, matching the 9 catalog entries with `skillsCli` (Composio excluded in both). Test counts: 3 + 4 + 2 = 9 node tests.
- **Custom domain:** not needed. The owned SEO surface is `aiescu.com/agent-skills` (Task 12).
