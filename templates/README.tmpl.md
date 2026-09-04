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
