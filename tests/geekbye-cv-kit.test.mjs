import test from 'node:test'
import assert from 'node:assert/strict'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

test('portable CV runtime grounding, preservation, copied-install and PDF regressions', () => {
  const scripts = fileURLToPath(new URL('../skills/geekbye-cv-kit/scripts/', import.meta.url))
  const result = spawnSync('python3', ['-m', 'unittest', 'discover', '-s', scripts, '-p', 'test_*.py'], {
    encoding: 'utf8',
    timeout: 180_000,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1' },
  })
  assert.equal(result.status, 0, result.stdout + result.stderr)
})
