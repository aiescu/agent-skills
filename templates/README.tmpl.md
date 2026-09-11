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
