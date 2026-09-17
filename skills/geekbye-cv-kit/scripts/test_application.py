import copy
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from application import validate_application, render_application
from pack import parse_text, render_text

ROOT = Path(__file__).resolve().parents[1]


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.master = json.loads((ROOT / 'examples/early-career.json').read_text())
        self.app = json.loads((ROOT / 'examples/early-career.application.json').read_text())

    def test_grounded_rewrite_preserves_master_and_metadata(self):
        from application import tailored
        original = copy.deepcopy(self.master)
        self.app['rewrites'] = {'/experience/0/description': {
            'text': 'Added Node.js booking-conflict validation and regression tests for overlapping appointments.',
            'evidence': ['/experience/0/description'], 'reviewed': True}}
        validate_application(self.master, self.app)
        derived = tailored(self.master, self.app)
        self.assertEqual(self.master, original)
        self.assertNotEqual(derived['experience'][0]['description'], original['experience'][0]['description'])
        for key in ['company', 'title', 'startDate', 'endDate']:
            self.assertEqual(derived['experience'][0][key], original['experience'][0][key])
        self.app['rewrites']['/experience/0/description']['text'] += ' Saved 987% of costs.'
        with self.assertRaisesRegex(ValueError, 'numeric'):
            validate_application(self.master, self.app)

    def test_rewrites_cannot_change_dates_or_transfer_evidence(self):
        self.app['rewrites'] = {'/experience/0/startDate': {
            'text': '2020-01', 'evidence': ['/experience/0'], 'reviewed': True}}
        with self.assertRaisesRegex(ValueError, 'metadata'):
            validate_application(self.master, self.app)
        self.app['rewrites'] = {'/experience/0/description': {
            'text': 'Built a demo.', 'evidence': ['/projects/0'], 'reviewed': True}}
        with self.assertRaisesRegex(ValueError, 'same source record'):
            validate_application(self.master, self.app)

    def test_education_dates_are_neutral_and_legacy_labels_parse(self):
        from pack import render_tex
        for supplied_date in ['2028-06', '2020-06', '']:
            with self.subTest(date=supplied_date):
                master = copy.deepcopy(self.master)
                master['education'][0]['graduationDate'] = supplied_date
                text = render_text(master)
                tex = render_tex(master, 'compact', sample=False)
                self.assertIn(('Education date: ' + supplied_date).rstrip(), text)
                self.assertIn('Education date: ' + supplied_date, tex)
                self.assertNotIn('Graduated:', text)
                self.assertNotIn('Graduated:', tex)
                self.assertEqual(parse_text(text), master)
                legacy_text = text.replace('Education date:', 'Graduated:')
                self.assertEqual(parse_text(legacy_text), master)

    def test_supported_requirement_requires_evidence(self):
        self.app['requirementMap'][0]['evidence'] = []
        with self.assertRaisesRegex(ValueError, 'supported.*evidence'):
            validate_application(self.master, self.app)

    def test_unreviewed_claim_and_invented_metric_rejected(self):
        self.app['letter']['paragraphs'][0]['reviewed'] = False
        with self.assertRaisesRegex(ValueError, 'reviewed'):
            validate_application(self.master, self.app)
        self.app['letter']['paragraphs'][0]['reviewed'] = True
        self.app['letter']['paragraphs'][0]['text'] += ' I increased revenue by 987%.'
        with self.assertRaisesRegex(ValueError, 'numeric'):
            validate_application(self.master, self.app)

    def test_bad_pointer_and_requirement_quote_rejected(self):
        self.app['selections']['experience'] = ['/experience/100']
        with self.assertRaises(ValueError):
            validate_application(self.master, self.app)
        self.app = json.loads((ROOT / 'examples/early-career.application.json').read_text())
        self.app['job']['requirements'][0]['sourceQuote'] = 'not in job source'
        with self.assertRaisesRegex(ValueError, 'sourceQuote'):
            validate_application(self.master, self.app)

    def test_master_and_existing_outputs_are_preserved(self):
        before = copy.deepcopy(self.master)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'application'
            render_application(self.master, self.app, destination, 'never')
            original = (destination / 'cv.json').read_bytes()
            with self.assertRaises(FileExistsError):
                render_application(self.master, self.app, destination, 'never')
            self.assertEqual((destination / 'cv.json').read_bytes(), original)
            self.assertEqual(self.master, before)
            validation = json.loads((destination / 'validation.json').read_text())
            self.assertEqual(validation['compile']['status'], 'not-requested')
            self.assertFalse((destination / 'cv.pdf').exists())

    def test_dangling_output_symlink_is_rejected_by_library_and_cli(self):
        import sys
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / 'unrelated-target'
            output = root / 'output-link'
            output.symlink_to(target, target_is_directory=True)
            with self.assertRaises(FileExistsError):
                render_application(self.master, self.app, output, 'never')
            self.assertFalse(target.exists())
            master = root / 'master.json'
            application = root / 'application.json'
            master.write_text(json.dumps(self.master))
            application.write_text(json.dumps(self.app))
            run = subprocess.run([sys.executable, str(ROOT / 'scripts/application.py'), 'render',
                                  '--master', str(master), '--application', str(application),
                                  '--output', str(output), '--compile', 'never'],
                                 text=True, capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn('symlink', run.stderr)
            self.assertFalse(target.exists())
            self.assertTrue(output.is_symlink())

    def test_partial_unicode_publication_roundtrip(self):
        master = json.loads((ROOT / 'examples/senior.json').read_text())
        master['title'] = ''
        master['phone'] = ''
        master['projects'][0]['startDate'] = ''
        master['projects'][0]['endDate'] = ''
        master['experience'][0]['description'] = ''
        master['education'][0]['graduationDate'] = ''
        master['publications'] = [{'title': 'Synthetic Șerban publication', 'authors': 'Zoë Șerban',
                                   'venue': '', 'date': '', 'url': ''}]
        self.assertEqual(parse_text(render_text(master)), master)

    def test_copied_skill_has_no_checkout_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / 'installed'
            shutil.copytree(ROOT, installed, ignore=shutil.ignore_patterns('__pycache__'))
            output = Path(directory) / 'result'
            command = ['python3', str(installed / 'scripts/application.py'), 'render',
                       '--master', str(installed / 'examples/early-career.json'),
                       '--application', str(installed / 'examples/early-career.application.json'),
                       '--output', str(output), '--compile', 'never']
            result = subprocess.run(command, cwd=directory, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            for filename in ['cv.tex', 'cv.md', 'cv.txt', 'cv.json', 'letter.tex', 'letter.md',
                             'letter.txt', 'requirement-map.json', 'change-log.json', 'questions.json',
                             'validation.json', 'master.json']:
                self.assertTrue((output / filename).is_file(), filename)

    def test_year_only_dates_and_empty_projects_do_not_invent_data(self):
        from pack import render_tex, escape_tex
        self.master['experience'][0].update(startDate='2025', endDate='2026')
        self.master['projects'] = []
        self.master['experience'].append(copy.deepcopy(self.master['experience'][0]))
        self.assertEqual(parse_text(render_text(self.master)), self.master)
        self.master['name'] = ''
        tex = render_tex(self.master, 'extended', sample=False)
        self.assertNotIn(r'\newpage', tex)
        self.assertNotIn(r'\section*{Projects}', tex)
        self.assertNotIn('Your name', tex)
        self.assertNotIn('you@example.com', tex)
        self.assertNotIn('Your phone', tex)
        for key in ['email', 'phone', 'location', 'objective']:
            self.assertIn(escape_tex(self.master[key]), tex)
        self.assertIn('2025 - 2026', tex)

    def test_tex_commands_are_data_and_missing_compiler_is_explicit(self):
        from unittest.mock import patch
        from pack import escape_tex
        self.assertEqual(escape_tex(r'A&B_50%\input{x}'),
                         r'A\&B\_50\%\textbackslash{}input\{x\}')
        with tempfile.TemporaryDirectory() as directory, patch('application.shutil.which', return_value=None):
            result = render_application(self.master, self.app, Path(directory) / 'missing', 'auto')
            self.assertEqual(result['compile']['status'], 'unavailable')
            self.assertFalse(result['compile']['pdfCreated'])

    def test_compiled_optional_and_partial_values_extract(self):
        if not shutil.which('tectonic') or not shutil.which('pdftotext'):
            self.skipTest('Tectonic and Poppler unavailable')
        from pack import render_tex
        master = json.loads((ROOT / 'examples/unicode-partial.json').read_text())
        master['experience'][0]['startDate'] = '2023'
        with tempfile.TemporaryDirectory() as directory:
            tex = Path(directory) / 'probe.tex'
            tex.write_text(render_tex(master, 'research', sample=False), encoding='utf-8')
            result = subprocess.run(['tectonic', str(tex)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            extracted = subprocess.check_output(['pdftotext', str(tex.with_suffix('.pdf')), '-'], text=True)
            self.assertEqual(parse_text(extracted), master)
            try:
                from pypdf import PdfReader
            except ImportError:
                return
            extracted = '\n'.join(page.extract_text() for page in PdfReader(tex.with_suffix('.pdf')).pages)
            self.assertEqual(parse_text(extracted), master)


if __name__ == '__main__':
    unittest.main()
