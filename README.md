# Agent Skills: the 10 most popular skill repos, one install away

[![Stars refreshed](https://img.shields.io/badge/stars_refreshed-2026-09-04-blue)](catalog/stars.json)
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

We use these skills every day. [See what we built with them ↓](#built-with-these-skills)

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

Sorted by stars as of 2026-09-04.

| # | Repository | Stars | What it is | Flagship skill | License |
|---|---|---:|---|---|---|
| 1 | [obra/superpowers](https://github.com/obra/superpowers) | 281.7k | An opinionated software-development methodology delivered as composable skills: brainstorm, plan, TDD, debug, review, ship | `brainstorming` | MIT |
| 2 | [mattpocock/skills](https://github.com/mattpocock/skills) | 249.4k | Small, composable engineering skills straight from Matt's .agents directory | `grill-with-docs` | MIT |
| 3 | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 210.1k | A single skill distilled from Karpathy's observations on LLM coding pitfalls: think first, simplicity, surgical changes, goal-driven execution | `karpathy-guidelines` | Unlicensed (README says MIT) |
| 4 | [anthropics/skills](https://github.com/anthropics/skills) | 174.0k | The official reference collection, the Agent Skills spec, and the skill template | `skill-creator` | Per-skill (Apache-2.0 / proprietary) |
| 5 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 124.9k | Design intelligence for building professional UI across platforms: 192 reasoning rules, 79 searchable styles, a design-system generator | `ui-ux-pro-max` | MIT |
| 6 | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | 103.4k | Cuts about 65% of output tokens by making the agent talk like a caveman while keeping technical accuracy | `caveman` | MIT (skills) / BSL-1.1 (engine, proxy) |
| 7 | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 92.2k | Production-grade engineering skills organized as a lifecycle: define, plan, build, verify, review, ship | `spec-driven-development` | MIT |
| 8 | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 84.3k | Gives your AI good taste: stops generic frontend slop with brief inference, variance/motion/density dials, and a design-system map | `design-taste-frontend` | MIT |
| 9 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 74.5k | A curated awesome-list of about 180 skills plus 800+ app-automation skills for Composio's MCP gateway | `connect-apps` | Unlicensed (README says Apache-2.0) |
| 10 | [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | 27.1k | Ten output rules that stop the agent burying the answer: lead with the next action, number steps, cap lists at five, no preamble | `i-have-adhd` | MIT |

## Each repo

### Superpowers ([obra/superpowers](https://github.com/obra/superpowers))

by [Jesse Vincent (obra)](https://github.com/obra) · ⭐ 281.7k · 14 skills · MIT

An opinionated software-development methodology delivered as composable skills: brainstorm, plan, TDD, debug, review, ship. Session hooks make the agent actually use them.

**Flagship skill:** `brainstorming`. Forces intent and requirements exploration before any creative work. The entry point to the whole methodology.

**Why it's here:** Most-starred skills repo. Broadest harness support of any entry (13+ agents).

```bash
# Any agent (Claude Code, Codex, Cursor, Gemini, Copilot, OpenCode, 70+ more)
npx skills@1 add obra/superpowers

# Claude Code plugin
/plugin install superpowers@claude-plugins-official

# Codex
codex plugin marketplace add obra/superpowers-marketplace

# Gemini CLI
gemini extensions install https://github.com/obra/superpowers

# Cursor
/add-plugin superpowers
```


### Skills for Real Engineers ([mattpocock/skills](https://github.com/mattpocock/skills))

by [Matt Pocock](https://github.com/mattpocock) · ⭐ 249.4k · 37 skills · MIT

Small, composable engineering skills straight from Matt's .agents directory. Explicitly against process-owning frameworks.

**Flagship skill:** `grill-with-docs`. Interrogates you to close the alignment gap before building, then writes a shared-language CONTEXT.md and ADRs.

**Why it's here:** Second most-starred. Pushed most recently of the ten.

```bash
# Any agent (Claude Code, Codex, Cursor, Gemini, Copilot, OpenCode, 70+ more)
npx skills@1 add mattpocock/skills

# Claude Code plugin
claude plugins install mattpocock-skills
```

> Install via ONE path only. The upstream README warns against installing both the plugin and the npx copy.


### Andrej Karpathy Skills ([multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills))

by [multica-ai (formerly forrestchang)](https://github.com/multica-ai) · ⭐ 210.1k · 1 skill · Unlicensed (README says MIT)

A single skill distilled from Karpathy's observations on LLM coding pitfalls: think first, simplicity, surgical changes, goal-driven execution.

**Flagship skill:** `karpathy-guidelines`. Four rules that measurably reduce over-engineering.

**Why it's here:** Third most-starred; the canonical behavioral-guidelines skill.

```bash
# Any agent (Claude Code, Codex, Cursor, Gemini, Copilot, OpenCode, 70+ more)
npx skills@1 add multica-ai/andrej-karpathy-skills

# Claude Code plugin
/plugin marketplace add multica-ai/andrej-karpathy-skills && /plugin install andrej-karpathy-skills@karpathy-skills

# Cursor
Copy .cursor/rules/karpathy-guidelines.mdc from the repo
```

> **License note:** No LICENSE file in the repo. We link only.

### Anthropic Agent Skills ([anthropics/skills](https://github.com/anthropics/skills))

by [Anthropic](https://github.com/anthropics) · ⭐ 174.0k · 19 skills · Per-skill (Apache-2.0 / proprietary)

The official reference collection, the Agent Skills spec, and the skill template. Home of skill-creator and mcp-builder.

**Flagship skill:** `skill-creator`. Scaffolds and validates new skills. Apache-2.0.

**Why it's here:** The spec everything else follows.

```bash
# Any agent (Claude Code, Codex, Cursor, Gemini, Copilot, OpenCode, 70+ more)
npx skills@1 add anthropics/skills

# Claude Code plugin
/plugin marketplace add anthropics/skills && /plugin install example-skills@anthropic-agent-skills
```

> Not in our marketplace: the repo root has no plugin.json; use the command above.

> **License note:** docx, pdf, pptx and xlsx are all-rights-reserved and may not be redistributed. We link only; nothing is copied.

### UI/UX Pro Max ([nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill))

by [nextlevelbuilder](https://github.com/nextlevelbuilder) · ⭐ 124.9k · 7 skills · MIT

Design intelligence for building professional UI across platforms: 192 reasoning rules, 79 searchable styles, a design-system generator.

**Flagship skill:** `ui-ux-pro-max`. The umbrella design skill; design-system is the v2 headline.

**Why it's here:** Most-starred design skill; its own CLI supports about 20 agents.

```bash
# Any agent (Claude Code, Codex, Cursor, Gemini, Copilot, OpenCode, 70+ more)
npx skills@1 add nextlevelbuilder/ui-ux-pro-max-skill

# Claude Code plugin
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill && /plugin install ui-ux-pro-max@ui-ux-pro-max-skill

# Upstream CLI
npm i -g ui-ux-pro-max-cli && uipro init --ai claude
```

> **License note:** Requires Python 3 for its local search script (stdlib only, no network).

### Caveman ([JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman))

by [Julius Brussee](https://github.com/JuliusBrussee) · ⭐ 103.4k · 20 skills · MIT (skills) / BSL-1.1 (engine, proxy)

Cuts about 65% of output tokens by making the agent talk like a caveman while keeping technical accuracy. Plus subagent presets and memory-file compression.

**Flagship skill:** `caveman`. The namesake compression mode with lite, full and ultra intensities.

**Why it's here:** The token-efficiency skill everyone else copies.

```bash
# Any agent (Claude Code, Codex, Cursor, Gemini, Copilot, OpenCode, 70+ more)
npx skills@1 add JuliusBrussee/caveman

# Claude Code plugin
claude plugin marketplace add JuliusBrussee/caveman && claude plugin install caveman@caveman

# Gemini CLI
gemini extensions install https://github.com/JuliusBrussee/caveman
```

> **License note:** "Caveman" and the rock logo are trademarks of Julius Brussee. The optional CLI sends telemetry by default (DO_NOT_TRACK=1 disables it).

### Agent Skills by Addy Osmani ([addyosmani/agent-skills](https://github.com/addyosmani/agent-skills))

by [Addy Osmani](https://github.com/addyosmani) · ⭐ 92.2k · 25 skills · MIT

Production-grade engineering skills organized as a lifecycle: define, plan, build, verify, review, ship. Includes slash commands and agent personas.

**Flagship skill:** `spec-driven-development`. Spec before code; the head of the documented lifecycle.

**Why it's here:** The most complete lifecycle collection; clean MIT.

```bash
# Any agent (Claude Code, Codex, Cursor, Gemini, Copilot, OpenCode, 70+ more)
npx skills@1 add addyosmani/agent-skills

# Claude Code plugin
/plugin marketplace add addyosmani/agent-skills && /plugin install agent-skills@addy-agent-skills

# Codex
codex plugin marketplace add addyosmani/agent-skills

# Gemini CLI
gemini skills install https://github.com/addyosmani/agent-skills
```

> **License note:** Per-skill npx install drops the shared references/ dir (upstream issue #361). Install the whole repo.

### Taste Skill ([Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill))

by [Leonxlnx](https://github.com/Leonxlnx) · ⭐ 84.3k · 13 skills · MIT

Gives your AI good taste: stops generic frontend slop with brief inference, variance/motion/density dials, and a design-system map.

**Flagship skill:** `design-taste-frontend`. The default anti-slop frontend skill (v2).

**Why it's here:** Most-starred single-purpose design-taste skill.

```bash
# Any agent (Claude Code, Codex, Cursor, Gemini, Copilot, OpenCode, 70+ more)
npx skills@1 add Leonxlnx/taste-skill

# Only the flagship skill
npx skills@1 add Leonxlnx/taste-skill --skill design-taste-frontend
```


### Awesome Claude Skills ([ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills))

by [Composio](https://github.com/ComposioHQ) · ⭐ 74.5k · 865 skills · Unlicensed (README says Apache-2.0)

A curated awesome-list of about 180 skills plus 800+ app-automation skills for Composio's MCP gateway.

**Flagship skill:** `connect-apps`. Lets the agent take real actions across 1000+ apps via Composio.

**Why it's here:** The largest discovery list in the ecosystem.

```bash
# Claude Code plugin
git clone https://github.com/ComposioHQ/awesome-claude-skills && claude --plugin-dir ./awesome-claude-skills/connect-apps-plugin
```

> Not in our marketplace: the repo root has no plugin.json; use the command above.

> **License note:** No LICENSE file. Contains vendored copies of Anthropic's restricted document skills. We link only.

### I Have ADHD ([ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd))

by [ayghri](https://github.com/ayghri) · ⭐ 27.1k · 1 skill · MIT

Ten output rules that stop the agent burying the answer: lead with the next action, number steps, cap lists at five, no preamble.

**Flagship skill:** `i-have-adhd`. The only skill here about the shape of answers, and it helps everyone, not only ADHD users.

**Why it's here:** Fastest-growing single skill of 2026; packaged for seven harnesses.

```bash
# Any agent (Claude Code, Codex, Cursor, Gemini, Copilot, OpenCode, 70+ more)
npx skills@1 add ayghri/i-have-adhd

# Claude Code plugin
claude plugin marketplace add ayghri/i-have-adhd && claude plugin install i-have-adhd@i-have-adhd
```


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

## Built with these skills

The maintainers of this list ship three products, and the skills above are how we build them.
Here is what each one does and which skills did the work.

<table>
<tr>
<td width="104" align="center" valign="top">
<a href="https://geekbye.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card"><img src="assets/products/geekbye.png" width="88" height="88" alt="GeekBye logo"></a>
</td>
<td valign="top">

### [GeekBye](https://geekbye.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card): a real-time interview assistant

**How GeekBye helps you in interviews**

- **Before:** practice with the [interview question bank](https://geekbye.com/interview-questions?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card), where every question comes with a detailed answer, and build your resume in the [resume builder](https://geekbye.com/tools/resume-builder?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card).
- **During:** live help with coding, behavioral and system-design questions, based on your screen and the conversation. Works with Zoom, Microsoft Teams and Google Meet. No bot joins the call, and GeekBye stays out of screen shares and recordings.
- **After:** check your offer against market rates with the [salary negotiation calculator](https://geekbye.com/tools/salary-negotiation-calculator?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card).

**How we built it**

- [Superpowers](https://github.com/obra/superpowers): the in-call widget UX, the speech-to-text quality work, the meeting-mode orchestrator and the product docs hub were each brainstormed, written up as a spec and turned into an implementation plan before any code.
- [`frontend-design`](https://github.com/anthropics/skills/tree/main/skills/frontend-design) from Anthropic's skills: the docs hub layout.
- [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) and [Taste Skill](https://github.com/Leonxlnx/taste-skill): landing page design.
- [Caveman](https://github.com/JuliusBrussee/caveman): runs in every agent session to cut output tokens.

**[Try GeekBye →](https://geekbye.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card)**

</td>
</tr>
<tr>
<td width="104" align="center" valign="top">
<a href="https://keebye.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card"><img src="assets/products/keebye.png" width="88" height="88" alt="Keebye logo"></a>
</td>
<td valign="top">

### [Keebye](https://keebye.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card): push-to-talk dictation for people who drive coding agents

Hold a key, say the thing, and the text lands in whichever window has focus: Claude Code, Cursor,
a terminal, Slack. Speech-to-text runs on your Mac and audio never leaves the machine. Optional
synthetic typing works over SSH and inside tmux. macOS, with a 14-day free trial.

**How we built it**

- [Superpowers](https://github.com/obra/superpowers): the site rebuild, the billing and docs work, and the discount logic were each specced and planned before implementation.
- [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) and [Taste Skill](https://github.com/Leonxlnx/taste-skill): landing page design.
- [Caveman](https://github.com/JuliusBrussee/caveman): runs in every agent session to cut output tokens.

**[Try Keebye →](https://keebye.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card)**

</td>
</tr>
<tr>
<td width="104" align="center" valign="top">
<a href="https://pavleur.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card"><img src="assets/products/pavleur.png" width="88" height="88" alt="Pavleur logo"></a>
</td>
<td valign="top">

### [Pavleur](https://pavleur.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card): an AI meeting copilot for Mac

Captures every customer call (screen recording, transcript, screenshots, slides) and pulls out the
decisions and action items. Works with Zoom, Google Meet, Microsoft Teams and anything else on your
screen, and no bot joins the call. Recordings stay on your Mac or your own Google Drive, never on
our servers.

**How we built it**

- [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) and [Taste Skill](https://github.com/Leonxlnx/taste-skill): landing page design.
- [Caveman](https://github.com/JuliusBrussee/caveman): runs in every agent session to cut output tokens.

**[Try Pavleur →](https://pavleur.com?utm_source=github&utm_medium=readme&utm_campaign=agent-skills&utm_content=card)**

</td>
</tr>
</table>

---

<sub>Built by <a href="https://github.com/aiescu">aiescu</a>.</sub>
