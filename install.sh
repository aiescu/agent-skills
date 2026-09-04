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
