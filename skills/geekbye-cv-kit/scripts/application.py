#!/usr/bin/env python3
"""Portable source-grounded CV/letter rendering; no model, network or ATS score."""
import argparse
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from pack import VARIANTS, builder_data, compare_fields, escape_tex, parse_text, render_tex, render_text

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / 'assets/candidate.schema.json').read_text(encoding='utf-8'))
COLLECTIONS = ('experience', 'education', 'skills', 'projects', 'publications')
NUMBERS = re.compile(r'\d+(?:[.,]\d+)*%?')


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def schema_check(value, schema=SCHEMA, path='master'):
    kind = schema.get('type')
    if kind == 'object':
        if not isinstance(value, dict):
            raise ValueError(path + ' must be an object')
        missing = set(schema.get('required', [])) - value.keys()
        extra = value.keys() - schema.get('properties', {}).keys()
        if missing or (schema.get('additionalProperties') is False and extra):
            raise ValueError(f'{path}: missing fields {sorted(missing)}, extra fields {sorted(extra)}')
        for key, item in value.items():
            if key in schema.get('properties', {}):
                schema_check(item, schema['properties'][key], path + '/' + key)
    elif kind == 'array':
        if not isinstance(value, list):
            raise ValueError(path + ' must be an array')
        for i, item in enumerate(value):
            schema_check(item, schema['items'], path + '/' + str(i))
    elif kind == 'string' and not isinstance(value, str):
        raise ValueError(path + ' must be a string')


def pointer(master, ref):
    if not isinstance(ref, str) or not ref.startswith('/') or ref == '/':
        raise ValueError('Evidence must use a non-root JSON pointer: ' + repr(ref))
    value = master
    try:
        for token in ref[1:].split('/'):
            token = token.replace('~1', '/').replace('~0', '~')
            if isinstance(value, list):
                if not re.fullmatch(r'0|[1-9]\d*', token):
                    raise ValueError('Invalid array index')
                value = value[int(token)]
            elif isinstance(value, dict):
                value = value[token]
            else:
                raise ValueError('Pointer traverses a scalar')
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError('Unknown evidence pointer: ' + ref) from error
    return value


def strings(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [text for item in value for text in strings(item)]
    if isinstance(value, dict):
        return [text for item in value.values() for text in strings(item)]
    return []


def evidence(master, refs):
    if not isinstance(refs, list) or not refs or len(set(refs)) != len(refs):
        raise ValueError('A claim needs distinct evidence pointers')
    values = [pointer(master, ref) for ref in refs]
    if not any(text.strip() for value in values for text in strings(value)):
        raise ValueError('Empty evidence cannot support a claim')
    return values


def claim_check(master, claim, path):
    if not isinstance(claim, dict) or not isinstance(claim.get('text'), str):
        raise ValueError(path + ' must contain text')
    if claim.get('reviewed') is not True:
        raise ValueError(path + ' must be factually reviewed; set reviewed=true only after checking support')
    values = evidence(master, claim.get('evidence'))
    available = set(NUMBERS.findall(' '.join(text for value in values for text in strings(value))))
    invented = set(NUMBERS.findall(claim['text'])) - available
    if invented:
        raise ValueError(path + ': unsupported numeric tokens ' + repr(sorted(invented)))


def validate_application(master, app):
    schema_check(master)
    if not isinstance(app, dict):
        raise ValueError('application must be an object')
    job = app.get('job', {})
    for field in ('title', 'company', 'description'):
        if not isinstance(job.get(field), str) or not job[field].strip():
            raise ValueError('job/' + field + ' must be nonempty text')
    requirements = job.get('requirements')
    if not isinstance(requirements, list) or not requirements:
        raise ValueError('job needs explicit requirements')
    ids = []
    for requirement in requirements:
        for field in ('id', 'text', 'sourceQuote'):
            if not isinstance(requirement.get(field), str) or not requirement[field].strip():
                raise ValueError('requirement needs ' + field)
        if requirement['sourceQuote'] not in job['description']:
            raise ValueError('requirement sourceQuote must occur verbatim in job description')
        ids.append(requirement['id'])
    if len(set(ids)) != len(ids):
        raise ValueError('Requirement IDs must be distinct')
    selections = app.get('selections', {})
    if set(selections) != set(COLLECTIONS):
        raise ValueError('selections must list each canonical collection')
    for collection, refs in selections.items():
        if not isinstance(refs, list) or len(set(refs)) != len(refs):
            raise ValueError('Selections must be distinct pointers')
        for ref in refs:
            if not isinstance(ref, str) or not re.fullmatch('/' + collection + r'/(0|[1-9]\d*)', ref):
                raise ValueError('Selection must reference a whole ' + collection + ' entry')
            pointer(master, ref)
    rewrites = app.get('rewrites', {})
    if not isinstance(rewrites, dict):
        raise ValueError('rewrites must map description pointers to grounded claims')
    for ref, rewrite in rewrites.items():
        match = re.fullmatch(r'/(experience|projects)/(0|[1-9]\d*)/description', ref)
        if not match:
            raise ValueError('Only experience/project descriptions can be rewritten; metadata is immutable')
        record_ref = ref.rsplit('/', 1)[0]
        if record_ref not in selections[match.group(1)]:
            raise ValueError('A rewritten record must be selected')
        claim_check(master, rewrite, 'rewrites' + ref)
        if any(source != record_ref and not source.startswith(record_ref + '/') for source in rewrite['evidence']):
            raise ValueError('Rewrite evidence must come from the same source record; preserve role association')
    claim_check(master, app.get('summary'), 'summary')
    letter = app.get('letter', {})
    for field in ('salutation', 'closing'):
        if not isinstance(letter.get(field), str):
            raise ValueError('letter needs ' + field)
    if not isinstance(letter.get('paragraphs'), list) or not letter['paragraphs']:
        raise ValueError('letter needs paragraphs')
    for index, paragraph in enumerate(letter['paragraphs']):
        claim_check(master, paragraph, 'letter/paragraphs/' + str(index))
    mapping = app.get('requirementMap', [])
    if not isinstance(mapping, list) or sorted(row.get('requirementId', '') for row in mapping) != sorted(ids):
        raise ValueError('requirementMap must contain each requirement exactly once')
    for row in mapping:
        if not isinstance(row.get('evidence'), list):
            raise ValueError('Requirement evidence must be an array, including unsupported entries')
        status = row.get('status')
        if status not in ('supported', 'partial', 'unsupported'):
            raise ValueError('Unknown requirement status')
        if status in ('supported', 'partial') and not row.get('evidence'):
            raise ValueError('supported/partial requirement needs evidence')
        if row.get('evidence'):
            evidence(master, row['evidence'])
        if status == 'unsupported' and row.get('evidence'):
            raise ValueError('unsupported requirement must have empty evidence')
        if not isinstance(row.get('note'), str):
            raise ValueError('requirement map needs a note')
    preferences = app.get('preferences', {})
    for field in ('language', 'region', 'cvLength'):
        if not isinstance(preferences.get(field), str) or not preferences[field]:
            raise ValueError('preferences needs ' + field)
    word_range = preferences.get('letterWords', [250, 300])
    if (not isinstance(word_range, list) or len(word_range) != 2 or
            any(type(n) is not int or n < 1 for n in word_range) or word_range[0] > word_range[1]):
        raise ValueError('letterWords must be [minimum, maximum] positive integers')
    if preferences.get('paper', 'a4') not in ('a4', 'letter'):
        raise ValueError('paper must be a4 or letter')
    if preferences.get('layout', 'compact') not in VARIANTS:
        raise ValueError('Unknown layout')
    if not isinstance(app.get('questions', []), list) or any(not isinstance(q, str) for q in app.get('questions', [])):
        raise ValueError('questions must be a string array')
    warnings = []
    if not master['name'].strip():
        warnings.append('Candidate name is missing; no placeholder was invented.')
    for collection in ('experience', 'projects'):
        for ref in selections[collection]:
            item = pointer(master, ref)
            for key in ('startDate', 'endDate'):
                date = item[key]
                if date and not re.fullmatch(r'\d{4}(?:-(?:0[1-9]|1[0-2]))?|Present', date):
                    warnings.append(ref + '/' + key + ': ambiguous date retained verbatim; resolve before strict parsing.')
            if not item['startDate'] or not item['endDate']:
                warnings.append(ref + ': incomplete dates; confirm rather than infer.')
            if not NUMBERS.search(item['description']):
                warnings.append(ref + ': no measured outcome supplied; do not manufacture metrics.')
    words = len((' '.join(p['text'] for p in letter['paragraphs'])).split())
    if not word_range[0] <= words <= word_range[1]:
        warnings.append(f'Letter body has {words} words; requested range is {word_range[0]}–{word_range[1]}.')
    warnings += ['Requirement ' + row['requirementId'] + ' is ' + row['status'] + ': ' + row['note']
                 for row in mapping if row['status'] != 'supported']
    return {'status': 'validated-with-warnings' if warnings else 'validated',
            'warnings': warnings, 'letterBodyWords': words,
            'checks': {'schema': True, 'sourcePointers': True, 'jobQuotes': True,
                       'metadataPreserved': True, 'newNumericTokensAbsent': True},
            'factualSupport': 'Host-reviewed prose. Pointer and numeric checks do not prove semantic entailment.',
            'ats': 'Not scored; pack-specific parser checks are not vendor ATS evidence.'}


def tailored(master, app):
    candidate = copy.deepcopy(master)
    for collection in COLLECTIONS:
        candidate[collection] = [copy.deepcopy(pointer(master, ref)) for ref in app['selections'][collection]]
    for ref, rewrite in app.get('rewrites', {}).items():
        _, collection, index, field = ref.split('/')
        selected_index = app['selections'][collection].index('/' + collection + '/' + index)
        candidate[collection][selected_index][field] = rewrite['text']
    candidate['objective'] = app['summary']['text']
    return candidate


def letter_text(master, app):
    letter = app['letter']
    return '\n\n'.join([master['name'], master['email'], master['location'],
                         'Re: ' + app['job']['title'] + ' — ' + app['job']['company'],
                         letter['salutation'], *[p['text'] for p in letter['paragraphs']],
                         letter['closing'], master['name']]) + '\n'


def letter_tex(text, paper):
    header = (r'\documentclass[11pt,PAPERpaper]{article}' '\n'
              r'\usepackage[margin=20mm]{geometry}' '\n'
              r'\usepackage{fontspec}' '\n'
              r'\setmainfont{lmroman10-regular.otf}[BoldFont=lmroman10-bold.otf,Ligatures=NoCommon]' '\n'
              r'\pagestyle{empty}' '\n'
              r'\setlength{\parindent}{0pt}' '\n'
              r'\setlength{\parskip}{10pt}' '\n'
              r'\emergencystretch=2em' '\n'
              r'\begin{document}' '\n').replace('PAPER', paper)
    return header + '\n\n'.join(escape_tex(p) + r'\par' for p in text.split('\n\n')) + '\n' + r'\end{document}' + '\n'


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def compile_outputs(output, mode):
    if mode == 'never':
        return {'status': 'not-requested', 'pdfCreated': False}
    compiler = shutil.which('tectonic')
    if not compiler:
        return {'status': 'unavailable', 'pdfCreated': False,
                'reason': 'Tectonic not found on PATH. TEX, Markdown, text and JSON were produced.'}
    records = []
    for stem in ('cv', 'letter'):
        try:
            run = subprocess.run([compiler, '--keep-logs', str(output / (stem + '.tex'))],
                                 cwd=output, text=True, capture_output=True, timeout=120, check=False)
            log_path = output / (stem + '.log')
            log = log_path.read_text(encoding='utf-8', errors='replace') if log_path.exists() else ''
            records.append({'artifact': stem, 'returncode': run.returncode, 'overflow': 'Overfull' in log,
                            'missingGlyphs': 'Missing character' in log,
                            'pdfCreated': (output / (stem + '.pdf')).is_file()})
            (output / (stem + '.compile.txt')).write_text(run.stdout + run.stderr, encoding='utf-8')
        except subprocess.TimeoutExpired:
            records.append({'artifact': stem, 'error': 'Compilation exceeded 120 seconds', 'pdfCreated': False})
    passed = all(r.get('returncode') == 0 and r['pdfCreated'] and not r['overflow'] and not r['missingGlyphs'] for r in records)
    return {'status': 'passed' if passed else 'failed', 'pdfCreated': all(r['pdfCreated'] for r in records),
            'compiler': 'tectonic', 'artifacts': records}


def verify_pdf(output, candidate):
    pdf = output / 'cv.pdf'
    if not pdf.is_file():
        return {'status': 'unavailable', 'reason': 'No compiled CV PDF'}
    results = []
    poppler = shutil.which('pdftotext')
    if poppler:
        try:
            run = subprocess.run([poppler, str(pdf), '-'], text=True, capture_output=True, timeout=30)
            if run.returncode:
                results.append({'extractor': 'Poppler', 'status': 'failed', 'reason': run.stderr})
            else:
                (output / 'cv.poppler.txt').write_text(run.stdout, encoding='utf-8')
                actual = parse_text(run.stdout)
                differences = compare_fields(candidate, actual)
                results.append({'extractor': 'Poppler', 'status': 'passed' if not differences else 'failed',
                                'differences': differences})
        except (ValueError, subprocess.TimeoutExpired) as error:
            results.append({'extractor': 'Poppler', 'status': 'requires-review', 'reason': str(error)})
    else:
        results.append({'extractor': 'Poppler', 'status': 'unavailable'})
    try:
        from pypdf import PdfReader
    except ImportError:
        results.append({'extractor': 'pypdf', 'status': 'unavailable'})
    else:
        try:
            reader = PdfReader(pdf)
            text = '\n'.join(page.extract_text() or '' for page in reader.pages)
            (output / 'cv.pypdf.txt').write_text(text, encoding='utf-8')
            differences = compare_fields(candidate, parse_text(text))
            results.append({'extractor': 'pypdf', 'status': 'passed' if not differences else 'failed',
                            'differences': differences, 'pages': len(reader.pages)})
        except Exception as error:
            results.append({'extractor': 'pypdf', 'status': 'requires-review', 'reason': str(error)})
    available = [row for row in results if row['status'] != 'unavailable']
    status = 'unavailable' if not available else 'passed' if all(row['status'] == 'passed' for row in available) else 'requires-review'
    return {'status': status, 'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
            'extractors': results, 'scope': 'Exact pack grammar/field comparison; not a vendor ATS assessment.'}


def render_application(master, app, output, compile_mode='auto', master_sha256=None):
    validation = validate_application(master, app)
    output = Path(output).absolute()
    if output.is_symlink():
        raise FileExistsError('Output symlink already exists: ' + str(output))
    # Create the original destination exclusively before resolving it. Resolving
    # first would follow a dangling symlink and create its unrelated target.
    output.mkdir(parents=True, exist_ok=False)
    output = output.resolve()
    candidate = tailored(master, app)
    cv_text = render_text(candidate)
    letter = letter_text(master, app)
    paper = app['preferences'].get('paper', 'a4')
    tex = render_tex(candidate, app['preferences'].get('layout', 'compact'), sample=False)
    if paper == 'letter':
        tex = tex.replace(',a4paper]', ',letterpaper]', 1)
    (output / 'cv.tex').write_text(tex, encoding='utf-8')
    (output / 'cv.txt').write_text(cv_text, encoding='utf-8')
    (output / 'cv.md').write_text(cv_text, encoding='utf-8')
    (output / 'letter.tex').write_text(letter_tex(letter, paper), encoding='utf-8')
    for extension in ('txt', 'md'):
        (output / ('letter.' + extension)).write_text(letter, encoding='utf-8')
    write_json(output / 'cv.json', candidate)
    write_json(output / 'cv.builder.json', builder_data(candidate))
    write_json(output / 'master.json', master)
    write_json(output / 'application.json', app)
    write_json(output / 'requirement-map.json', {'requirements': app['job']['requirements'],
                                               'mapping': app['requirementMap'],
                                               'evidence': {ref: pointer(master, ref) for row in app['requirementMap']
                                                            for ref in row['evidence']}})
    canonical_hash = hashlib.sha256(json.dumps(master, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    write_json(output / 'change-log.json', {'masterCanonicalSha256': canonical_hash,
                                           'masterInputSha256': master_sha256,
                                           'changedPaths': compare_fields(master, candidate),
                                           'selectedSourceRecords': app['selections'],
                                           'summaryEvidence': app['summary'],
                                           'letterEvidence': app['letter']['paragraphs'],
                                           'rewrites': {ref: {'before': pointer(master, ref), **claim}
                                                        for ref, claim in app.get('rewrites', {}).items()},
                                           'factPolicy': 'Metadata exact; evidence-reviewed description rewrites and summary/letter prose in derived output only.'})
    write_json(output / 'questions.json', {'questions': app.get('questions', []),
                                         'automaticReviewItems': validation['warnings']})
    try:
        validation['textRoundtrip'] = {'status': 'passed' if not compare_fields(candidate, parse_text(cv_text)) else 'failed'}
    except ValueError as error:
        validation['textRoundtrip'] = {'status': 'requires-review', 'reason': str(error)}
    validation['compile'] = compile_outputs(output, compile_mode)
    validation['pdfRoundtrip'] = verify_pdf(output, candidate)
    write_json(output / 'validation.json', validation)
    return validation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('render', 'validate'):
        command = commands.add_parser(name)
        command.add_argument('--master', type=Path, required=True)
        command.add_argument('--application', type=Path, required=True)
        if name == 'render':
            command.add_argument('--output', type=Path, required=True)
            command.add_argument('--compile', choices=('auto', 'never', 'required'), default='auto')
    parse_command = commands.add_parser('parse', help='Strict pack grammar only, not arbitrary imported CVs')
    parse_command.add_argument('--text', type=Path, required=True)
    parse_command.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'parse':
            result = parse_text(args.text.read_text(encoding='utf-8'))
            schema_check(result)
            # Exclusive file open preserves existing artifacts.
            with args.output.open('x', encoding='utf-8') as handle:
                json.dump(result, handle, ensure_ascii=False, indent=2)
                handle.write('\n')
            return 0
        master, application = load(args.master), load(args.application)
        if args.command == 'validate':
            result = validate_application(master, application)
        else:
            if args.output.is_symlink():
                raise FileExistsError('Output symlink already exists: ' + str(args.output))
            output = args.output.resolve()
            # Prevent writing any files into a master/application input's parent tree.
            if any(path.resolve().is_relative_to(output) for path in (args.master, args.application)):
                raise ValueError('Output must not contain input files')
            result = render_application(master, application, args.output, args.compile,
                                        hashlib.sha256(args.master.read_bytes()).hexdigest())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command == 'render' and (result['compile']['status'] == 'failed' or
                args.compile == 'required' and result['compile']['status'] != 'passed'):
            return 1
        return 0
    except (ValueError, OSError, TypeError, AttributeError) as error:
        print('Error: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
