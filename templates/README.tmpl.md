# Aiescu-maintained distribution of upstream skills

[![Stars refreshed](https://img.shields.io/badge/stars_refreshed-{{UPDATED}}-blue)](catalog/stars.json)
[![CI](https://github.com/aiescu/agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/aiescu/agent-skills/actions/workflows/ci.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC_BY_4.0-lightgrey.svg)](LICENSE-CONTENT)

Install reusable **agent skills** for Claude Code, Codex, Gemini CLI, Cursor, Copilot,
OpenCode and other supported agents. This repository distributes licensed upstream
skills with their original credits, alongside the original Aiescu CV kit.
Upstream skills remain the work of their original authors; inclusion does not imply
authorship by Aiescu or endorsement by the upstream maintainers.

Web version of this list: [aiescu.com/agent-skills](https://aiescu.com/agent-skills?utm_source=github&utm_medium=readme&utm_campaign=agent-skills).

The **Aiescu distribution** contains pinned copies of redistributable skills, each with
its own license and source record. The **upstream catalog** below still links to the
original projects and their full integrations. Original authors retain credit; Aiescu
maintains this distribution.

<sub>Maintained by <a href="https://github.com/aiescu">aiescu</a>. Star counts are fetched weekly from the GitHub API, never typed by hand.</sub>

[See what we built with agent skills ↓](#built-with-these-skills)

## Quick start

```bash
# Discover skills distributed from this repository
npx skills@1 add aiescu/agent-skills --list

# Install one skill, preserving its original author and license
npx skills@1 add aiescu/agent-skills --skill caveman

# Or choose skills interactively
npx skills@1 add aiescu/agent-skills
```

The Skills CLI requires Node.js 22.20 or newer. Review a skill before using it; scripts,
external services and runtime requirements vary. For the complete upstream frameworks:

```bash
# Upstream catalog installer (interactive picker)
curl -fsSL https://raw.githubusercontent.com/aiescu/agent-skills/main/install.sh | bash -s -- --agent claude-code

# One repo, any agent, via the skills CLI
npx skills@1 add obra/superpowers

# Plugin marketplace (installs upstream plugins)
/plugin marketplace add aiescu/agent-skills
```

## Redistributed skills

{{DISTRIBUTION_SUMMARY}}

See [the complete distribution inventory](docs/DISTRIBUTION.md) for install names,
original sources, pinned revisions, licenses and exclusions. Name collisions use an
upstream-owner prefix; the inventory gives the exact `--skill` value.

These are skill packages, not copies of every upstream plugin, hook or runtime.
Each package's `UPSTREAM.md` records packaging changes and external requirements.
Restricted skills remain available through their upstream links instead of being copied.

Standard CLI installs can contribute to Skills.sh discovery. Set `DISABLE_TELEMETRY=1`
or `DO_NOT_TRACK=1` to opt out. Automated installation checks disable telemetry and do
not count as evidence of directory indexing. Individual directory pages appear through
genuine user installations; inclusion here does not promise an indexing deadline.

## Original Aiescu skill: `geekbye-cv-kit`

[![Skills.sh: geekbye-cv-kit](https://img.shields.io/badge/Skills.sh-geekbye--cv--kit-black)](https://www.skills.sh/aiescu/agent-skills/geekbye-cv-kit)

Browse [Aiescu skills on Skills.sh](https://www.skills.sh/aiescu/agent-skills)
or open the [geekbye-cv-kit listing](https://www.skills.sh/aiescu/agent-skills/geekbye-cv-kit).

Turn verified candidate facts and a target job description into a tailored CV and matching
cover letter, with editable LaTeX, Markdown, plain text, candidate JSON and an evidence map.
Missing facts remain visible. The current Skills CLI needs Node.js 22.20 or newer.
Python 3 runs the portable example; compiling PDFs also needs Tectonic and its TeX bundle.
No account or provider key is required for rendering.

From a repository checkout, run the complete example without network access:

```bash
python3 skills/geekbye-cv-kit/scripts/application.py render \
  --master skills/geekbye-cv-kit/examples/early-career.json \
  --application skills/geekbye-cv-kit/examples/early-career.application.json \
  --output /tmp/my-cv-application --compile never
```

Use a fresh output directory for each job. Replace `never` with `auto` to try PDF compilation;
read the validation report to confirm whether a PDF was produced.

See [the skill](skills/geekbye-cv-kit/SKILL.md) for intake and usage,
[research and source review](skills/geekbye-cv-kit/references/research.md) for the original
synthesis, and [installation and publication evidence](docs/cv-kit-distribution.md) for
local checks and release gates.

```bash
# Discover and install just the original kit
npx skills@1 add aiescu/agent-skills --list
npx skills@1 add aiescu/agent-skills --skill geekbye-cv-kit

# To opt out of CLI telemetry, prefix the install command
DISABLE_TELEMETRY=1 npx skills@1 add aiescu/agent-skills --skill geekbye-cv-kit
```

The skill is published on the main branch. Both Skills.sh directory links above were
verified live on September 17, 2026.

Normal Skills CLI installs use its default telemetry settings; `DISABLE_TELEMETRY=1` or
`DO_NOT_TRACK=1` opts out. The curated `install.sh` wrapper continues to disable telemetry
for upstream installs. It installs the catalog, not this original kit.

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
the list and descriptions are CC BY 4.0. Upstream skills belong to their authors. The original
CV kit includes its own license and source notes inside its installable directory.

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

The original [`geekbye-cv-kit`](skills/geekbye-cv-kit/SKILL.md) prepares CVs and letters.
[Build and check your tailored CV](https://resume.geekbye.com/) and then use
[GeekBye interview preparation](https://geekbye.com/interview-questions) for the next step.
Campaign attribution for these links is pending verification; see the distribution evidence.

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
