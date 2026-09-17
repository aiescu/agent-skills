#!/usr/bin/env python3
"""Reproduce the fixture matrix from a copied skill; write only a fresh output tree."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--compile', choices=['auto', 'never', 'required'], default='auto')
    args = parser.parse_args()
    output = args.output.resolve()
    if ROOT.is_relative_to(output) or output.is_relative_to(ROOT):
        parser.error('Choose an output outside the installed skill')
    output.mkdir(parents=True, exist_ok=False)
    installed = output / 'installed-skill'
    shutil.copytree(ROOT, installed, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'rendered', 'runtime-evidence.json'))
    cases = [(stem, layout) for stem in ['early-career', 'senior'] for layout in ['compact', 'research', 'extended']]
    cases += [('unicode-partial', 'research'), ('career-change', 'compact'), ('ambiguous-dates', 'compact')]
    results = []
    failed = False
    for stem, layout in cases:
        master = installed / 'examples' / (stem + '.json')
        app = json.loads((installed / 'examples' / (stem + '.application.json')).read_text(encoding='utf-8'))
        app['preferences']['layout'] = layout
        app_path = output / (stem + '-' + layout + '.application.json')
        app_path.write_text(json.dumps(app, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        destination = output / (stem + '-' + layout)
        mode = 'never' if stem == 'ambiguous-dates' else args.compile
        run = subprocess.run([sys.executable, str(installed / 'scripts/application.py'), 'render',
                              '--master', str(master), '--application', str(app_path),
                              '--output', str(destination), '--compile', mode],
                             cwd=output, text=True, capture_output=True, check=False)
        validation = json.loads((destination / 'validation.json').read_text()) if (destination / 'validation.json').exists() else {}
        record = {'fixture': stem, 'layout': layout, 'exitCode': run.returncode,
                  'masterSha256': sha(master), 'applicationSha256': sha(app_path), 'validation': validation,
                  'artifacts': {path.name: sha(path) for path in sorted(destination.glob('*')) if path.is_file()}}
        results.append(record)
        roundtrip = validation.get('pdfRoundtrip', {}).get('status')
        if run.returncode or (mode == 'required' and roundtrip != 'passed'):
            failed = True
            record['commandOutput'] = run.stdout + run.stderr
        print(stem, layout, validation.get('compile', {}).get('status'), roundtrip, flush=True)
    evidence = {'date': '2026-09-16', 'scope': 'Actual copied-install deterministic rendering and field extraction; no model evaluation or ATS score.',
                'command': 'python scripts/verify_examples.py --output <fresh-external-directory> --compile ' + args.compile,
                'copiedInstall': True, 'pythonVersion': sys.version.split()[0],
                'sourceSha256': {str(path.relative_to(ROOT)): sha(path) for path in sorted(ROOT.glob('scripts/*.py'))},
                'cases': results}
    (output / 'runtime-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Evidence:', output / 'runtime-evidence.json', flush=True)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
