#!/usr/bin/env bash
# tests/install.test.sh: installer contract tests, no network
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }

expected=$(node -e "console.log(JSON.parse(require('fs').readFileSync('catalog/skills.json','utf8')).entries.filter(e=>e.install.skillsCli).map(e=>e.install.skillsCli).sort().join('\n'))")
actual=$(bash install.sh --list | LC_ALL=C sort)
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
